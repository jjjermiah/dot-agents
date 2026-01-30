#!/usr/bin/env -S pixi exec --spec python=3.14 --spec tiktoken --spec rich -- python

from __future__ import annotations

import argparse
import json
import os
import stat
import sys
from dataclasses import dataclass
from typing import Iterable, List

import tiktoken
from rich.console import Console

DEFAULT_MAX_BYTES = 1_048_576
DEFAULT_ENCODING = "cl100k_base"
BINARY_PREFIX_BYTES = 32 * 1024


@dataclass
class InputItem:
    id: str
    kind: str  # "path" | "text"
    text: str | None = None
    path: str | None = None
    bytes_len: int | None = None


@dataclass
class ResultItem:
    id: str
    status: str  # "ok" | "skipped"
    tokens: int | None = None
    bytes_len: int | None = None
    reason: str | None = None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Estimate token counts for files or stdin using tiktoken.",
    )
    parser.add_argument("paths", nargs="*", help="File paths (use fd ... -X).")
    parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    parser.add_argument(
        "--max-bytes",
        type=int,
        default=DEFAULT_MAX_BYTES,
        help=f"Max file size to read (default {DEFAULT_MAX_BYTES}).",
    )
    parser.add_argument(
        "--encoding",
        default=DEFAULT_ENCODING,
        help=f"Tokenizer encoding (default {DEFAULT_ENCODING}).",
    )
    parser.add_argument(
        "--stdin",
        choices=["auto", "paths", "text", "ignore"],
        default=None,
        help=(
            "How to interpret stdin when piped. Default: auto when no args; "
            "ignore when args present."
        ),
    )
    parser.add_argument(
        "--fail-on-skip",
        action="store_true",
        help="Exit non-zero if any item is skipped.",
    )
    return parser


def parse_args(parser: argparse.ArgumentParser) -> argparse.Namespace:
    return parser.parse_args()


def choose_stdin_mode(args: argparse.Namespace) -> str:
    if args.stdin is not None:
        return args.stdin
    return "ignore" if args.paths else "auto"


def read_stdin_bytes() -> bytes:
    return sys.stdin.buffer.read()


def is_line_oriented(text: str) -> bool:
    return "\n" in text


def stdin_as_paths(text: str) -> List[str]:
    lines = [line.strip() for line in text.splitlines()]
    return [line for line in lines if line]


def detect_stdin_mode_auto(text: str) -> str:
    lines = stdin_as_paths(text)
    if not lines or not is_line_oriented(text):
        return "text"
    existing = sum(1 for line in lines if os.path.exists(line))
    ratio = existing / max(1, len(lines))
    return "paths" if ratio >= 0.8 else "text"


def parse_stdin(mode: str, stdin_bytes: bytes) -> List[InputItem]:
    text = stdin_bytes.decode("utf-8", errors="replace")
    if mode == "ignore":
        return []
    if mode == "text":
        return [
            InputItem(id="<stdin>", kind="text", text=text, bytes_len=len(stdin_bytes))
        ]
    if mode == "paths":
        return [
            InputItem(id=line, kind="path", path=line) for line in stdin_as_paths(text)
        ]
    if mode == "auto":
        auto_mode = detect_stdin_mode_auto(text)
        return parse_stdin(auto_mode, stdin_bytes)
    raise ValueError(f"Unknown stdin mode: {mode}")


def is_binary(path: str, max_bytes: int) -> bool:
    read_len = min(BINARY_PREFIX_BYTES, max_bytes)
    try:
        with open(path, "rb") as handle:
            chunk = handle.read(read_len)
    except OSError:
        return False
    return b"\x00" in chunk


def process_path(path: str, max_bytes: int, encoder: tiktoken.Encoding) -> ResultItem:
    try:
        st = os.stat(path)
    except OSError:
        return ResultItem(id=path, status="skipped", reason="not_a_file")

    if not stat.S_ISREG(st.st_mode):
        return ResultItem(id=path, status="skipped", reason="not_a_file")

    if st.st_size > max_bytes:
        return ResultItem(id=path, status="skipped", reason="too_large")

    if is_binary(path, max_bytes):
        return ResultItem(id=path, status="skipped", reason="binary")

    try:
        with open(path, "rb") as handle:
            data = handle.read(max_bytes)
    except OSError:
        return ResultItem(id=path, status="skipped", reason="not_a_file")

    text = data.decode("utf-8", errors="replace")
    tokens = len(encoder.encode(text))
    return ResultItem(
        id=path,
        status="ok",
        tokens=tokens,
        bytes_len=len(data),
    )


def process_text(item: InputItem, encoder: tiktoken.Encoding) -> ResultItem:
    text = item.text or ""
    tokens = len(encoder.encode(text))
    return ResultItem(
        id=item.id,
        status="ok",
        tokens=tokens,
        bytes_len=item.bytes_len
        if item.bytes_len is not None
        else len(text.encode("utf-8")),
    )


def collect_inputs(args: argparse.Namespace) -> List[InputItem]:
    stdin_bytes: bytes | None = None

    def ensure_stdin() -> bytes:
        nonlocal stdin_bytes
        if stdin_bytes is None:
            stdin_bytes = read_stdin_bytes()
        return stdin_bytes

    inputs: List[InputItem] = []
    if args.paths:
        for path in args.paths:
            if path == "-":
                data = ensure_stdin()
                inputs.append(
                    InputItem(
                        id="<stdin>",
                        kind="text",
                        text=data.decode("utf-8", errors="replace"),
                        bytes_len=len(data),
                    )
                )
            else:
                inputs.append(InputItem(id=path, kind="path", path=path))

        stdin_mode = choose_stdin_mode(args)
        if stdin_mode != "ignore" and "-" not in args.paths and not sys.stdin.isatty():
            inputs.extend(parse_stdin(stdin_mode, ensure_stdin()))
        return inputs

    if sys.stdin.isatty():
        return []

    stdin_mode = choose_stdin_mode(args)
    inputs.extend(parse_stdin(stdin_mode, ensure_stdin()))
    return inputs


def summarize(results: Iterable[ResultItem]) -> dict:
    total_tokens = sum(item.tokens or 0 for item in results if item.status == "ok")
    ok_count = sum(1 for item in results if item.status == "ok")
    skipped_count = sum(1 for item in results if item.status == "skipped")
    return {
        "tokens": total_tokens,
        "ok": ok_count,
        "skipped": skipped_count,
        "inputs": ok_count + skipped_count,
    }


def emit_human(
    results: List[ResultItem],
    totals: dict,
    out_console: Console,
    err_console: Console,
) -> None:
    for item in results:
        if item.status == "ok":
            out_console.print(
                f"{item.id} tokens={item.tokens} bytes={item.bytes_len}",
                highlight=False,
            )

    out_console.print(
        f"total tokens={totals['tokens']} ok={totals['ok']} skipped={totals['skipped']}",
        highlight=False,
    )

    for item in results:
        if item.status == "skipped":
            hint = " (hint: use fd)" if item.reason == "not_a_file" else ""
            err_console.print(
                f"SKIP {item.id} reason={item.reason}{hint}", highlight=False
            )


def emit_json(
    results: List[ResultItem],
    totals: dict,
    encoding: str,
    max_bytes: int,
) -> None:
    payload = {
        "encoding": encoding,
        "max_bytes": max_bytes,
        "items": [
            {
                "id": item.id,
                "status": item.status,
                **({"tokens": item.tokens} if item.tokens is not None else {}),
                **({"bytes": item.bytes_len} if item.bytes_len is not None else {}),
                **({"reason": item.reason} if item.reason else {}),
            }
            for item in results
        ],
        "total": totals,
    }
    sys.stdout.write(json.dumps(payload, indent=2) + "\n")


def main() -> int:
    parser = build_parser()
    args = parse_args(parser)

    if args.max_bytes < 0:
        parser.error("--max-bytes must be >= 0")

    inputs = collect_inputs(args)
    if not inputs:
        parser.print_help()
        return 2

    try:
        encoder = tiktoken.get_encoding(args.encoding)
    except Exception:
        sys.stderr.write(f"Unknown encoding: {args.encoding}\n")
        return 2

    results: List[ResultItem] = []
    for item in inputs:
        if item.kind == "text":
            results.append(process_text(item, encoder))
        else:
            results.append(process_path(item.path or "", args.max_bytes, encoder))

    totals = summarize(results)

    if args.json:
        emit_json(results, totals, args.encoding, args.max_bytes)
    else:
        out_console = Console(file=sys.stdout)
        err_console = Console(file=sys.stderr, stderr=True)
        emit_human(results, totals, out_console, err_console)

    if totals["ok"] == 0:
        return 1
    if args.fail_on_skip and totals["skipped"] > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
