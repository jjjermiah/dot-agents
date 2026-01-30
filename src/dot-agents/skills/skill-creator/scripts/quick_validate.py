#!/usr/bin/env -S pixi exec --spec python=3.12 --spec pyyaml -- python
"""
Quick validation script for skills - validates structure and standards
"""

import re
import sys
from pathlib import Path

import yaml


def validate_skill(skill_path):
    """Validate a skill against required structure and standards."""
    skill_path = Path(skill_path)
    warnings = []

    # Check SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found", []

    # Read and validate frontmatter
    content = skill_md.read_text()
    if not content.startswith("---"):
        return False, "No YAML frontmatter found", []

    # Extract frontmatter
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format", []

    frontmatter_text = match.group(1)
    body = content[match.end() :].strip()

    # Parse YAML frontmatter
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary", []
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in frontmatter: {e}", []

    # Define allowed properties
    ALLOWED_PROPERTIES = {"name", "description", "license", "allowed-tools", "metadata"}

    # Check for unexpected properties
    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return (
            False,
            (
                f"Unexpected key(s) in frontmatter: {', '.join(sorted(unexpected_keys))}. "
                f"Allowed: {', '.join(sorted(ALLOWED_PROPERTIES))}"
            ),
            [],
        )

    # Check required fields
    if "name" not in frontmatter:
        return False, "Missing 'name' in frontmatter", []
    if "description" not in frontmatter:
        return False, "Missing 'description' in frontmatter", []

    # Validate name
    name = frontmatter.get("name", "")
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}", []
    name = name.strip()
    if name:
        if not re.match(r"^[a-z0-9-]+$", name):
            return (
                False,
                f"Name '{name}' should be hyphen-case (lowercase, digits, hyphens only)",
                [],
            )
        if name.startswith("-") or name.endswith("-") or "--" in name:
            return (
                False,
                f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens",
                [],
            )
        if len(name) > 64:
            return False, f"Name too long ({len(name)} chars). Maximum is 64.", []

    # Validate description
    description = frontmatter.get("description", "")
    if not isinstance(description, str):
        return (
            False,
            f"Description must be a string, got {type(description).__name__}",
            [],
        )
    description = description.strip()
    if description:
        if "<" in description or ">" in description:
            return False, "Description cannot contain angle brackets (< or >)", []
        if len(description) > 1024:
            return (
                False,
                f"Description too long ({len(description)} chars). Maximum is 1024.",
                [],
            )
        # Check description quality - should include WHEN to use
        trigger_keywords = ["use when", "trigger", "use for", "use any time", "use if"]
        has_trigger = any(kw in description.lower() for kw in trigger_keywords)
        if not has_trigger:
            warnings.append(
                "Description should include WHEN to use (e.g., 'Use when...', 'Triggers...')"
            )

    # Validate body structure
    lines = body.split("\n")
    line_count = len(lines)

    # Check line count
    if line_count > 500:
        warnings.append(
            f"SKILL.md has {line_count} lines (recommended max: 500). Consider splitting to references."
        )

    # Check for Purpose section
    has_purpose = bool(re.search(r"^##\s+Purpose", body, re.MULTILINE))
    if not has_purpose:
        return False, "Missing required '## Purpose' section", warnings

    # Check for anti-pattern: "When to Use" in body (should be in description only)
    has_when_to_use = bool(
        re.search(r"^##\s+(When to Use|When to use)", body, re.MULTILINE)
    )
    if has_when_to_use:
        warnings.append(
            "'When to Use' section found in body - this info should be in description (frontmatter) only"
        )

    # Check references section format if it exists
    references_dir = skill_path / "references"
    if references_dir.exists() and list(references_dir.glob("*.md")):
        has_references_section = bool(
            re.search(r"^##\s+References", body, re.MULTILINE)
        )
        if not has_references_section:
            warnings.append(
                "references/ directory exists but no '## References' section found in SKILL.md"
            )
        else:
            # Check if references have "Load when" guidance
            ref_section_match = re.search(
                r"^##\s+References.*?(?=^##|\Z)", body, re.MULTILINE | re.DOTALL
            )
            if ref_section_match:
                ref_section = ref_section_match.group(0)
                if (
                    "load when" not in ref_section.lower()
                    and "load for" not in ref_section.lower()
                ):
                    warnings.append(
                        "References section should include guidance on WHEN to load each reference"
                    )

    # Check for broken reference links
    ref_links = re.findall(r"\[.*?\]\((references/[^)]+)\)", body)
    for ref_link in ref_links:
        ref_path = skill_path / ref_link
        if not ref_path.exists():
            return False, f"Broken reference link: {ref_link}", warnings

    if warnings:
        return True, "Skill is valid (with warnings)", warnings
    return True, "Skill is valid!", []


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: quick_validate.py <skill_directory>")
        sys.exit(1)

    valid, message, warnings = validate_skill(sys.argv[1])

    if valid:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")

    for warning in warnings:
        print(f"⚠️  Warning: {warning}")

    sys.exit(0 if valid else 1)
