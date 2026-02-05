# Domain-Specific Patterns

Templates for applying diverge-converge to common contexts.

## Product/Feature Ideation

**When:** Generating roadmap ideas, feature brainstorms, product opportunities

**Diverge:**
- Target: 30-50 feature ideas
- Prompts: "What would make power users delighted?", "What would remove friction for new users?", "What would our competitor never do?"

**Cluster:**
- By user need or use case
- By feature type (acquisition, engagement, retention, revenue)
- By effort level (quick wins vs. big bets)

**Converge:**
- Matrix: Impact vs. Effort
- Criteria: User value, strategic alignment, technical feasibility, time to market
- Select: Top 3-5 for roadmap

**Output:**
```
## Selected Features
1. [Feature Name] - 8.5/10 (High impact, Med effort)
2. [Feature Name] - 8.0/10 (Med impact, Low effort)
3. [Feature Name] - 7.5/10 (High impact, High effort)

## Tradeoffs
- Selected X over Y because...
- Deprioritized Z due to...
```

---

## Problem-Solving

**When:** Open-ended technical or process problems

**Diverge:**
- Target: 20-40 solution approaches
- Prompts: "What's the dumbest solution?", "What would we do with unlimited resources?", "What if we couldn't use [obvious approach]?"

**Cluster:**
- By mechanism (how it solves the problem)
- By scope (quick fix vs. systemic change)
- By risk level (safe vs. experimental)

**Converge:**
- Matrix: Feasibility vs. Effectiveness
- Criteria: Solves root cause, implementation cost, side effects, reversibility
- Select: Top 2-3 to prototype

**Output:**
```
## Selected Approaches
1. [Approach] - 9/10 (High effectiveness, Med feasibility)
   - Prototype: [quick test]
   
2. [Approach] - 7/10 (Med effectiveness, High feasibility)
   - Fallback if #1 fails
```

---

## Research Questions

**When:** Academic or exploratory research, hypothesis generation

**Diverge:**
- Target: 25-40 potential questions
- Prompts: "What would disprove our assumption?", "What haven't others studied?", "What would [different field] ask?"

**Cluster:**
- By research method (experimental, observational, theoretical)
- By domain or variable
- By tractability (can we actually study this?)

**Converge:**
- Matrix: Novelty vs. Tractability (with impact as color)
- Criteria: Novelty, feasibility, impact, alignment with expertise
- Select: Top 3-5 to investigate

**Output:**
```
## Priority Questions
1. [Question] - Novelty: High, Tractability: Med, Impact: High
2. [Question] - Novelty: Med, Tractability: High, Impact: Med
3. [Question] - Novelty: High, Tractability: Low, Impact: High (long-term)
```

---

## Strategic Planning

**When:** Quarterly/annual planning, initiative prioritization

**Diverge:**
- Target: 20-30 strategic initiatives
- Prompts: "What would 10x our outcome?", "What would we do if starting over?", "What are we avoiding because it's hard?"

**Cluster:**
- By time horizon (Q1, H1, year, multi-year)
- By strategic pillar (growth, efficiency, risk, innovation)
- By investment level (low, medium, high)

**Converge:**
- Matrix: Strategic value vs. Resource requirements
- Criteria: Strategic alignment, ROI, risk, dependencies, capacity
- Select: Top 5 for quarterly planning

**Output:**
```
## Strategic Initiatives
Q1 Commitments:
1. [Initiative] - Value: High, Resources: Low
2. [Initiative] - Value: High, Resources: Med

H1 Pipeline:
3. [Initiative] - Value: Med, Resources: Med
4. [Initiative] - Value: High, Resources: High

Future Consideration:
5. [Initiative] - Value: Med, Resources: High (wait for capacity)
```

---

## Naming/Branding

**When:** Product names, project codenames, feature labels

**Diverge:**
- Target: 40-60 name ideas
- Prompts: Metaphors, compound words, invented words, foreign languages, unexpected domains

**Cluster:**
- By metaphor type (animal, nature, space, mechanical)
- By tone (serious, playful, technical, abstract)
- By length (short, medium, descriptive)

**Converge:**
- Criteria: Memorability, uniqueness, domain fit, pronunciation, availability (domains/handles)
- Filter: Must-haves first (available, pronounceable), then score on nice-to-haves
- Select: Top 3-5 for testing

**Output:**
```
## Candidate Names
1. [Name] - Score: 9/10 (Memorable, unique, fits domain)
2. [Name] - Score: 8/10 (Descriptive, available, clear)
3. [Name] - Score: 7.5/10 (Creative, short, needs validation)

## Rejected
- [Name] - taken on all platforms
- [Name] - hard to pronounce
```

---

## Experiment Design

**When:** A/B tests, validation experiments, prototype tests

**Diverge:**
- Target: 15-25 experiment variations
- Prompts: "What's the minimum viable test?", "What would prove we're wrong?", "What would maximize learning per dollar?"

**Cluster:**
- By hypothesis type (riskiest assumption, growth lever, user behavior)
- By method (qualitative, quantitative, mixed)
- By duration (hours, days, weeks)

**Converge:**
- Matrix: Learning value vs. Cost/effort
- Criteria: Validates key assumption, feasible to run, clear success metric, actionable result
- Select: Top 2-3 to run

**Output:**
```
## Selected Experiments
1. [Experiment] - Learning: High, Cost: Low (run first)
2. [Experiment] - Learning: High, Cost: Med (follow-up)

## Deprioritized
- [Experiment] - Low learning value
- [Experiment] - Too expensive for current stage
```
