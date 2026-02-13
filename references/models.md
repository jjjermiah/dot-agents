# Model pricing & capacity reference

## Anthropic / Claude lineup

### Haiku series (fastest Claude tier)
- **Models**: `anthropic/claude-3-5-haiku-20241022`, `anthropic/claude-3-5-haiku-latest`, `anthropic/claude-3-haiku-20240307`, `anthropic/claude-haiku-4-5`, `anthropic/claude-haiku-4-5-20251001`, `opencode/claude-3-5-haiku`, `opencode/claude-haiku-4-5`.
- **Context & speed**: Haiku models default to a 200k-token window and emit token-budget reminders; enterprise tiers can stretch to 500k or the beta 1M window when available via the `context-1m-2025-08-07` header. Haiku 4.5 is described as the fastest Claude model, making it ideal for high-throughput agent interactions.
- **Pricing**: Haiku 4.5 sits at $1 per million input tokens and $5 per million output tokens; older Haiku 3.x variants are deprecated and inherit similar per-request behavior but do not yet offer the 1M window beta.

### Sonnet series (intelligence + speed)
- **Models**: `anthropic/claude-3-5-sonnet-20240620`, `anthropic/claude-3-5-sonnet-latest`, `anthropic/claude-3-7-sonnet-20250219`, `anthropic/claude-3-7-sonnet-latest`, `anthropic/claude-3-sonnet-20240229`, `anthropic/claude-sonnet-4-0`, `anthropic/claude-sonnet-4-20250514`, `anthropic/claude-sonnet-4-5`, `anthropic/claude-sonnet-4-5-20250929`, `opencode/claude-sonnet-4`, `opencode/claude-sonnet-4-5`.
- **Context & speed**: Sonnet models keep the same 200k default window with the 1M beta option for Claude Sonnet 4.x. Sonnet 4.5 is promoted as combining "strong intelligence with fast performance," so use it when you need general-purpose reasoning with generous throughput.
- **Pricing**: Sonnet 4.5 costs $3 per million input tokens and $15 per million output tokens. Requests that exceed 200k input tokens (including prompt caching) automatically switch to the premium long-context rates for Sonnet 4.x.

### Opus series (top-end reasoning)
- **Models**: `anthropic/claude-opus-4-0`, `anthropic/claude-opus-4-1`, `anthropic/claude-opus-4-1-20250805`, `anthropic/claude-opus-4-5`, `anthropic/claude-opus-4-5-20251101`, `anthropic/claude-opus-4-6`, `opencode/claude-opus-4-1`, `opencode/claude-opus-4-5`, `opencode/claude-opus-4-6`.
- **Context & speed**: Opus 4.x models carry the same 200k-token default, while Opus 4.6 unlocks the 1M beta window (beta header required). Opus is positioned as the most advanced and intelligent model family, so expect higher latency than Haiku/Sonnet in exchange for deeper reasoning.
- **Pricing note**: Anthropic has not published a per-million token price for Opus 4.x in the publicly available docs we indexed; assume premium tiers similar to Sonnet 4.5 and confirm in the Claude Console if you need precise numbers. Long-context pricing applies to Opus 4.6 when a request goes beyond 200k input tokens, just like Sonnet 4.5.

### Rate limits & long-context guidance
- Haiku 4.5: 4M input tokens per minute, 800k output tokens per minute.
- Sonnet 4.x: aggregate rate limits per family (e.g., Sonnet 4.5 + Sonnet 4) with the same premium bucket that allows up to 200k input tokens before the beta rate kicks in.
- Opus 4.x: shared limit of 2M input tokens/minute and 400k output tokens/minute; long-context requests (1M window + >200k input) need tier-4/custom allowances.

## OpenAI / GPT-5 lineage
- **Models**: `openai/gpt-5`, `openai/gpt-5-codex`, `openai/gpt-5.1-codex`, `openai/gpt-5.1-codex-max`, `openai/gpt-5.1-codex-mini`, `openai/gpt-5.2`, `openai/gpt-5.2-codex`, `openai/gpt-5.3-codex`, `openai/gpt-5.3-codex-spark`, `opencode/gpt-5`, `opencode/gpt-5-codex`, `opencode/gpt-5-nano`, `opencode/gpt-5.1`, `opencode/gpt-5.1-codex`, `opencode/gpt-5.1-codex-max`, `opencode/gpt-5.1-codex-mini`, `opencode/gpt-5.2`, `opencode/gpt-5.2-codex`.
- **Core pricing & throughput (per OpenAI docs)**
  | Model | Context window | Input price / 1M | Output price / 1M | Speed note |
  | --- | --- | --- | --- | --- |
  | GPT-5 (base) | 400k tokens | $1.25 | not publicly detailed | general-purpose; default reasoning effort is `medium` with configurable verbosity |
  | GPT-5 mini | 400k tokens | $0.25 | $2.00 | cost-efficient, faster than base; ideal for precise prompts where low latency matters |
  | GPT-5 nano | 400k tokens | $0.05 | $0.40 | very fast / highest throughput; best for high-volume agent hops |
  | GPT-5 pro | 400k tokens, 272k max output | $15.00 | $120.00 | reasoning-first model (default `high` effort) with longer output budgets and background mode for very complex jobs |
- **Reasoning & speed tuning**: GPT-5.1 and GPT-5.2 allow the `reasoning.effort` parameter down to `none` for faster responses; GPT-5 pro only supports `high` effort. `text.verbosity` (`low/medium/high`) can throttle output token usage when speed is critical.

## OpenCode-native models & third-party providers
- Models such as `opencode/big-pickle`, `opencode/gemini-3-flash`, `opencode/gemini-3-pro`, `opencode/glm-4.6`, `opencode/glm-4.7`, `opencode/kimi-k2`, `opencode/kimi-k2-thinking`, `opencode/kimi-k2.5`, `opencode/kimi-k2.5-free`, `opencode/minimax-m2.1`, `opencode/minimax-m2.5-free` are powered by partner providers; consult each provider’s public docs for pricing and context windows because OpenCode acts as a router and does not own token rates.
- For the Claude and GPT families that OpenCode surfaces (`opencode/claude-*`, `opencode/gpt-*`), rely on the Anthropic and OpenAI pricing/context tables above since the OpenCode IDs map straightforwardly to the provider’s model IDs.

## Model selection decision tree (ASCII)

Use this as a quick, yes/no picker for agent/subagent model family selection.

```text
START
|
|-- Q0: Are you intentionally choosing an OpenCode partner model
|       (non-Claude / non-GPT; routed by OpenCode)?
|       |
|       +-- YES -> OpenCode partner models (e.g., `opencode/gemini-*`,
|       |         `opencode/kimi-*`, `opencode/glm-*`, `opencode/minimax-*`).
|       |         Note: pricing + context windows depend on the provider.
|       |
|       +-- NO  -> continue
|
|-- Q1: Do you need a context window > 400k tokens?
|       |
|       +-- YES -> Claude long-context path (1M beta window requires the
|       |         `context-1m-2025-08-07` header when available; some
|       |         enterprise tiers can stretch to ~500k).
|       |         |
|       |         |-- Q1a: Do you want deepest reasoning even if latency is
|       |         |        higher and pricing is a premium tier?
|       |         |        |
|       |         |        +-- YES -> `anthropic/claude-opus-4-6`
|       |         |        |
|       |         |        +-- NO  -> Q1b
|       |         |
|       |         |-- Q1b: Is throughput/latency the main priority?
|       |                  |
|       |                  +-- YES -> `anthropic/claude-haiku-4-5`
|       |                  |
|       |                  +-- NO  -> `anthropic/claude-sonnet-4-5`
|       |
|       +-- NO  -> continue
|
|-- Q2: Do you need a context window > 200k tokens (but <= 400k)?
|       |
|       +-- YES -> GPT-5 context path (400k context). Note: Claude families
|       |         default to 200k; requests that exceed 200k input tokens
|       |         switch to premium long-context rates for Claude 4.x.
|       |         |
|       |         |-- Q2a: Do you need a very long single response
|       |         |        (up to 272k output tokens)?
|       |         |        |
|       |         |        +-- YES -> GPT-5 pro family
|       |         |                 ($15.00 / 1M input, $120.00 / 1M output;
|       |         |                 note: does NOT support Code Interpreter)
|       |         |                 (`openai/gpt-5-pro`)
|       |         |
|       |         |        +-- NO  -> Q2b
|       |         |
|       |         |-- Q2b: Do you need Code Interpreter tool support?
|       |         |        |
|       |         |        +-- YES -> GPT-5 mini/nano family
|       |         |        |         (`openai/gpt-5-mini` or `openai/gpt-5-nano`)
|       |         |        |         (per OpenAI docs linked in Sources;
|       |         |        |         GPT-5 pro does not support this tool)
|       |         |        |
|       |         |        +-- NO  -> Q2c
|       |         |
|       |         |-- Q2c: Is cost sensitivity the primary constraint?
|       |                  |
|       |                  +-- YES -> GPT-5 nano or mini
|       |                  |         - nano: $0.05 / 1M input, $0.40 / 1M output
|       |                  |           (`openai/gpt-5-nano`, `opencode/gpt-5-nano`)
|       |                  |         - mini: $0.25 / 1M input, $2.00 / 1M output
|       |                  |           (`openai/gpt-5-mini`)
|       |                  |
|       |                  +-- NO  -> GPT-5 base
|       |                            - base: $1.25 / 1M input (output price not
|       |                              publicly detailed in the docs we indexed)
|       |                              (`openai/gpt-5`, `opencode/gpt-5`)
|       |
|       +-- NO  -> continue
|
|-- Q3: Is this mostly high-volume "agent hop" work where latency/
|       throughput matters more than deep reasoning?
|       |
|       +-- YES -> Q3a
|       |
|       |         |-- Q3a: Is lowest token cost the key driver?
|       |                  |
|       |                  +-- YES -> GPT-5 nano
|       |                  |         ($0.05 / 1M input, $0.40 / 1M output)
|       |                  |         (`openai/gpt-5-nano`, `opencode/gpt-5-nano`)
|       |                  |
|       |                  +-- NO  -> `anthropic/claude-haiku-4-5`
|       |                            ($1 / 1M input, $5 / 1M output; fastest
|       |                            Claude tier)
|       |
|       +-- NO  -> Q4
|
|-- Q4: Do you want a general-purpose default that balances reasoning
|       and speed for most agent tasks (<= 200k context)?
|       |
|       +-- YES -> `anthropic/claude-sonnet-4-5`
|       |         ($3 / 1M input, $15 / 1M output)
|       |
|       +-- NO  -> `openai/gpt-5-mini`
|                 ($0.25 / 1M input, $2.00 / 1M output)
```

## Sources
1. Anthropic Claude model overview & pricing: https://platform.claude.com/docs/en/about-claude/pricing and https://platform.claude.com/docs/en/about-claude/models/overview
2. Claude context windows / rate limits: https://platform.claude.com/docs/en/build-with-claude/context-windows and https://platform.claude.com/docs/en/api/rate-limits
3. OpenAI GPT-5 series specs & pricing: https://platform.openai.com/docs/models/gpt-5-mini, https://platform.openai.com/docs/models/gpt-5-nano, and https://platform.openai.com/docs/models/gpt-5-pro
