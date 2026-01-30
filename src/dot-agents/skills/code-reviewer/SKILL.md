---
name: code-reviewer
description: |
  Provides structured code review against plans and standards. Use when a feature is complete and needs validation, when reviewing code before merge, or when assessing quality and test coverage—e.g., "finished step X", "ready for review", "validate architecture", "check quality and tests".
---

# Code Reviewer Skill

## Purpose

Validate completed work against original plans, identify deviations, assess code quality/maintainability/test coverage/security, and provide actionable recommendations with clear severity labels.

## Review Procedure

1. Plan alignment analysis
   - Compare the implementation against the original plan
   - Identify deviations and assess impact
   - Verify all planned functionality is present
2. Code quality assessment
   - Check correctness, error handling, and type safety
   - Evaluate maintainability, naming, and project conventions
   - Assess tests and coverage quality
   - Look for security and performance risks
   - Use **[references/checklists.md](references/checklists.md)** for detailed review checklists by domain (API, database, frontend, etc.)
3. Architecture and design review
   - Validate SOLID principles and separation of concerns
   - Check integration with existing systems
   - Assess scalability and extensibility
4. Documentation and standards
   - Verify comments and documentation are accurate and necessary
   - Confirm adherence to project standards
5. Issue identification and recommendations
   - Categorize findings and propose fixes
   - Provide code examples when useful
   - See **[references/examples.md](references/examples.md)** for sample reviews showing proper format and detail level
6. Communication protocol
   - Ask for confirmation on significant plan deviations
   - Recommend plan updates if the plan itself is flawed
   - Acknowledge strengths before issues

## Output Contract

Return the review in this structure:

1. Overview (1-3 sentences)
2. Findings (bulleted), each with:
   - Severity: critical | important | suggestion
   - Location: file path + line (if available)
   - Rationale: why it matters
   - Fix: specific recommendation
   - Ordering: sort findings by severity, then by location
3. Tests / verification suggestions (optional)

## References (Load on Demand)

- **[references/checklists.md](references/checklists.md)** - Load when reviewing specific domains (API, database, frontend, security)
- **[references/examples.md](references/examples.md)** - Load to see sample reviews demonstrating proper format and detail level
