# Workflow Patterns

## Sequential Workflows

Give overview of process early in SKILL.md:

```markdown
Filling PDF forms:
1. Analyze form (run analyze_form.py)
2. Create field mapping (edit fields.json)
3. Validate mapping (run validate_fields.py)
4. Fill form (run fill_form.py)
5. Verify output (run verify_output.py)
```

## Conditional Workflows

Guide through decision points:

```markdown
1. Determine modification type:
   **Creating?** → Follow creation workflow
   **Editing?** → Follow editing workflow

2. Creation workflow: [steps]
3. Editing workflow: [steps]
```
