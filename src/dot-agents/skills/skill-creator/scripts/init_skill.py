#!/usr/bin/env -S pixi exec --spec python=3.12 -- python
"""
Skill Initializer - Creates a new skill from template

Usage:
    init_skill.py <skill-name> --path <path>

Examples:
    init_skill.py my-new-skill --path skills/public
    init_skill.py my-api-helper --path skills/private
    init_skill.py custom-skill --path /custom/location
"""

import sys
from pathlib import Path


SKILL_TEMPLATE = """---
name: {skill_name}
description: |
  [TODO: WHAT it does AND WHEN to use it. Include specific triggers, scenarios, file types, or tasks.
  Example: "Use when working with [technology] for [tasks]. Triggers: 'keyword', 'phrase', requests for [feature]."]
---

# {skill_title}

## Purpose

[TODO: 1-2 sentences explaining what this skill enables and its primary goal.]

## [TODO: Core Content Section]

[TODO: Add your main content here. Choose a structure that fits:

**Workflow-Based** (sequential processes):
- Decision trees, step-by-step procedures
- Structure: ## Workflow → ## Step 1 → ## Step 2...

**Task-Based** (tool collections):
- Different operations/capabilities
- Structure: ## Quick Start → ## Task 1 → ## Task 2...

**Reference/Guidelines** (standards):
- Specifications, coding standards, policies
- Structure: ## Guidelines → ## Specifications...

Include:
- Code samples for technical skills
- Decision trees for complex workflows
- Concrete examples with realistic requests

Delete this TODO block when done.]

## References (Load on Demand)

[TODO: List references with clear guidance on WHEN to load each one. Format:

- **[references/example.md](references/example.md)** - Load when [specific scenario or need]

Delete unused reference files. Not every skill needs references.]
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
Example helper script for {skill_name}

Delete this file if not needed. Scripts are for:
- Deterministic operations rewritten repeatedly
- Token-efficient, tested, self-contained executables
- Run via shebang (never `python <script>`)
"""

def main():
    print("Example script for {skill_name}")
    # TODO: Add actual script logic or delete this file

if __name__ == "__main__":
    main()
'''

EXAMPLE_REFERENCE = """# Example Reference for {skill_title}

[TODO: Replace with actual reference content or delete this file.]

References are for detailed documentation loaded on-demand:
- API references
- Detailed workflow guides
- Complex multi-step processes
- Content too lengthy for SKILL.md

Link from SKILL.md with clear guidance on WHEN to load:
`- **[references/this-file.md](references/this-file.md)** - Load when [specific scenario]`
"""


def title_case_skill_name(skill_name):
    """Convert hyphenated skill name to Title Case for display."""
    return " ".join(word.capitalize() for word in skill_name.split("-"))


def init_skill(skill_name, path):
    """
    Initialize a new skill directory with template SKILL.md.

    Args:
        skill_name: Name of the skill
        path: Path where the skill directory should be created

    Returns:
        Path to created skill directory, or None if error
    """
    # Determine skill directory path
    skill_dir = Path(path).resolve() / skill_name

    # Check if directory already exists
    if skill_dir.exists():
        print(f"❌ Error: Skill directory already exists: {skill_dir}")
        return None

    # Create skill directory
    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"✅ Created skill directory: {skill_dir}")
    except Exception as e:
        print(f"❌ Error creating directory: {e}")
        return None

    # Create SKILL.md from template
    skill_title = title_case_skill_name(skill_name)
    skill_content = SKILL_TEMPLATE.format(
        skill_name=skill_name, skill_title=skill_title
    )

    skill_md_path = skill_dir / "SKILL.md"
    try:
        skill_md_path.write_text(skill_content)
        print("✅ Created SKILL.md")
    except Exception as e:
        print(f"❌ Error creating SKILL.md: {e}")
        return None

    # Create resource directories with example files
    try:
        # Create scripts/ directory with example script
        scripts_dir = skill_dir / "scripts"
        scripts_dir.mkdir(exist_ok=True)
        example_script = scripts_dir / "example.py"
        example_script.write_text(EXAMPLE_SCRIPT.format(skill_name=skill_name))
        example_script.chmod(0o755)
        print("✅ Created scripts/example.py")

        # Create references/ directory with example reference doc
        references_dir = skill_dir / "references"
        references_dir.mkdir(exist_ok=True)
        example_reference = references_dir / "example.md"
        example_reference.write_text(EXAMPLE_REFERENCE.format(skill_title=skill_title))
        print("✅ Created references/example.md")
    except Exception as e:
        print(f"❌ Error creating resource directories: {e}")
        return None

    # Print next steps
    print(f"\n✅ Skill '{skill_name}' initialized successfully at {skill_dir}")
    print("\nNext steps:")
    print(
        "1. Edit SKILL.md: complete the description (WHAT + WHEN) and Purpose section"
    )
    print("2. Add core content sections with your skill's instructions")
    print("3. Update References section with links and WHEN to load each")
    print("4. Delete unused example files in scripts/ and references/")
    print("5. Run quick_validate.py to check the skill structure")

    return skill_dir


def main():
    if len(sys.argv) < 4 or sys.argv[2] != "--path":
        print("Usage: init_skill.py <skill-name> --path <path>")
        print("\nSkill name requirements:")
        print("  - Hyphen-case identifier (e.g., 'data-analyzer')")
        print("  - Lowercase letters, digits, and hyphens only")
        print("  - Max 40 characters")
        print("  - Must match directory name exactly")
        print("\nExamples:")
        print("  init_skill.py my-new-skill --path skills/public")
        print("  init_skill.py my-api-helper --path skills/private")
        print("  init_skill.py custom-skill --path /custom/location")
        sys.exit(1)

    skill_name = sys.argv[1]
    path = sys.argv[3]

    print(f"🚀 Initializing skill: {skill_name}")
    print(f"   Location: {path}")
    print()

    result = init_skill(skill_name, path)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
