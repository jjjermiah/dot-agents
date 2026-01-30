# Output Patterns

## Template Pattern

**Strict requirements** (API responses, data formats):

```markdown
## Report structure

ALWAYS use this exact template:

# [Title]

## Executive summary
[One paragraph]

## Key findings
- Finding 1 with data
- Finding 2 with data

## Recommendations
1. Actionable recommendation
2. Actionable recommendation
```

**Flexible guidance** (adaptation useful):

```markdown
## Report structure

Sensible default, use judgment:

# [Title]
## Executive summary
[Overview]

## Key findings
[Adapt based on discoveries]

## Recommendations
[Tailor to context]

Adjust as needed.
```

## Examples Pattern

For quality depending on examples, provide input/output pairs:

```markdown
## Commit message format

**Example 1:**
Input: Added user auth with JWT
Output:
```
feat(auth): implement JWT authentication

Add login endpoint and token validation
```

**Example 2:**
Input: Fixed date display bug
Output:
```
fix(reports): correct date timezone conversion

Use UTC timestamps consistently
```

Follow: type(scope): brief, then detail.
```

Examples clarify style and detail better than descriptions.
