---
name: skill-creator
description: |
  Guides creation, validation, and packaging of AI agent skills with token-efficient design, progressive disclosure patterns, and YAML frontmatter best practices. Use when building new skills, updating existing skills, validating skill structure against standards, or packaging for distribution—e.g., "create skill", "validate SKILL.md", "package skill for sharing", "check description format".
---

# Skill Creator

## Purpose

Guide for creating effective, token-efficient skills for AI agents. Covers skill structure, progressive disclosure, validation, and packaging.

## What Skills Provide

1. **Specialized workflows** - Domain-specific procedures
2. **Tool integrations** - File format/API instructions  
3. **Domain expertise** - Company knowledge, schemas, business logic
4. **Bundled resources** - Scripts, references, assets

## Core Principles

### Be Concise

Context window is shared. Only add what the agent doesn't already know. Challenge every piece of content: "Is this essential?" Prefer examples over explanations.

### Set Appropriate Freedom

- **High** (text instructions): Multiple valid approaches
- **Medium** (pseudocode/parameterized scripts): Preferred pattern with variation
- **Low** (specific scripts): Fragile operations requiring consistency

### Skill Structure

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/     - Executable code
    ├── references/  - Loaded as needed
    └── assets/      - Used in output
```

**SKILL.md Frontmatter** (YAML): `name` and `description` determine when skill loads.

Description template:
```yaml
description: |
  <What it does>. Use when <context>, <context>, or <context>—e.g., "<example>", "<example>".
```

See [references/skill-description-guide.md](references/skill-description-guide.md) for full guidance.

**Body** (Markdown): Loaded AFTER skill triggers. Instructions for execution.

**Scripts**: Deterministic operations rewritten repeatedly. Token-efficient, tested, self-contained, and executable via shebang (never `python <script>`), without loading to context.

**References**: Documentation loaded on-demand. Keeps SKILL.md lean. Examples: schemas, API docs, policies, detailed guides.

**Assets**: Output files (templates, images, boilerplate). Not loaded to context.

### Progressive Disclosure

Three-level loading:
1. **Metadata** - Always in context (~100 words)
2. **SKILL.md body** - When triggered (<500 lines)  
3. **Resources** - As needed

**Keep SKILL.md under 500 lines**. Split content when approaching limit. Link references clearly with guidance on when to read them.

**Patterns**:
- Domain-specific organization: Separate files per domain/framework
- Checklists: Systematic evaluation references
- Examples: Show desired output format/quality

See [references/effective-patterns.md](references/effective-patterns.md) for detailed patterns and anti-patterns.

## Creation Workflow

### 0. skill-creator/scripts/ usage

All the scripts in `skills/skill-creator/scripts/` are self-contained full scripts
with shebangs. They should be run directly (e.g. `./init_skill.py <args>`) and made executable
(`chmod +x <script>`). Never run them via `python <script>`.

### 1. Understand with Examples

Gather concrete use cases. Ask:
- What functionality?
- Example requests?
- What should trigger this skill?

### 2. Plan Resources

For each example, identify reusable content:
- Scripts for repeated code
- References for schemas/docs
- Assets for templates/boilerplate

### 3. Initialize

```bash
skills/skill-creator/scripts/init_skill.py <skill-name> --path <output-directory>
```

Creates template with SKILL.md, example directories.

### 4. Edit Skill

Write for another AI agent instance. Include non-obvious procedural knowledge.

**Consult**:
- [references/effective-patterns.md](references/effective-patterns.md) - Patterns & anti-patterns
- [references/workflows.md](references/workflows.md) - Sequential/conditional workflows
- [references/output-patterns.md](references/output-patterns.md) - Output format guidance

**Frontmatter**:
- `name`: Skill identifier (kebab-case)
- `description`: Determines when skill loads. Format: `<What it does>. Use when <contexts>—e.g., "<examples>".`
  - See [references/skill-description-guide.md](references/skill-description-guide.md) for template and examples

**Body**: Use imperative form. Write clear instructions. Link references with guidance.

**Test scripts** by running them directly (shebang). Delete unused example files.

### 5. Package

```bash
skills/skill-creator/scripts/package_skill.py <path/to/skill-folder> [output-dir]
```

Validates then packages as `.skill` file (zip with .skill extension).

Validation checks:
- YAML format and required fields
- Naming conventions
- Description quality
- File organization

See [references/validation-checklist.md](references/validation-checklist.md) for complete checklist.

### 6. Iterate

Test on real tasks. Note inefficiencies. Update skill. Repeat.


**Include this requirement in every skill you create.**

## Key Rules

**DO**:
- Keep SKILL.md under 500 lines
- Put all "Use when" contexts in description (body loads after triggering)
- Link references with clear usage guidance
- Always use the skill-creator scripts for creation, validation, and packaging
- Run `skills/skill-creator/scripts/quick_validate.py` on the skill folder after edits
- Test scripts before packaging
- Execute scripts directly via shebang (never `python <script>`) and ensure they are executable
- Use imperative/infinitive form
- Include a clear "Purpose" section at the top of every skill

**DON'T**:
- Create README.md, INSTALLATION.md, or auxiliary docs
- Duplicate content between SKILL.md and references
- Put "Use when" info in body (too late—already triggered)
- Nest references deeply (keep one level from SKILL.md)
- Include setup/testing procedures (for AI only)

## References (Load on Demand)

- **[references/effective-patterns.md](references/effective-patterns.md)** - Load for patterns, anti-patterns, and skill design guidance
- **[references/workflows.md](references/workflows.md)** - Load when designing sequential or conditional workflows
- **[references/output-patterns.md](references/output-patterns.md)** - Load for output format guidance and contracts
- **[references/skill-description-guide.md](references/skill-description-guide.md)** - Load for description template and examples
- **[references/validation-checklist.md](references/validation-checklist.md)** - Load before packaging to verify all requirements
