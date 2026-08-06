# Matching Algorithm

## Overview

The purpose of the matching algorithm is to estimate how well a job offer matches a candidate profile.

Unlike a keyword search, the algorithm evaluates several independent criteria and combines their results into a single compatibility score.

The design of the algorithm follows three principles:

1. Each criterion is evaluated independently.
2. Only applicable criteria participate in the final score.
3. The scoring policy is independent from the matching logic.

This separation allows the algorithm to evolve without modifying the workflow or the application architecture.

---

# Matching Pipeline

The matching process consists of three distinct phases.

```
JobOffer
        +
CandidateProfile
        │
        ▼
JobMatchingService
        │
        ▼
CriterionMatch[]
        │
        ▼
MatchingScoreCalculator
        │
        ▼
MatchResult
```

Each component has a single responsibility.

---

# CriterionMatch

A `CriterionMatch` represents the evaluation of a single matching criterion.

It currently contains:

- criterion
- score
- applicable
- matched
- missing

A `CriterionMatch` answers five questions:

- Which criterion has been evaluated?
- Does this criterion apply?
- What score did it obtain?
- Which requirements were satisfied?
- Which requirements were not satisfied?

---

# Applicable Criteria

One of the most important design decisions is distinguishing between:

- a criterion that **fails**
- a criterion that **does not apply**

These situations are intentionally different.

A non-applicable criterion must not penalize the final score.

For example:

- a candidate without a salary expectation should not lose points because salary cannot be compared.
- a job offer without language requirements should not penalize candidates who speak several languages.
- a candidate without a remote preference should neither gain nor lose points because of the remote policy.

---

# Applicability Rules

## Skills

Applicable when the job specifies at least one required skill.

```
bool(job.requirements.skills)
```

---

## Languages

Applicable when the job specifies at least one language requirement.

```
bool(job.requirements.languages)
```

---

## Experience

Applicable when the job specifies a minimum number of years of experience.

```
job.requirements.years_experience is not None
```

---

## Salary

Applicable only when both sides provide salary information.

```
job.salary is not None
and
profile.salary is not None
```

---

## Remote

Applicable when the candidate has expressed a remote work preference.

```
profile.preferred_remote_type is not None
```

---

## Country

Applicable when the candidate specifies one or more preferred countries.

```
bool(profile.preferred_countries)
```

---

# Matching Policy

`MatchingPolicy` defines the importance of each criterion.

Its responsibility is configuration, not calculation.

Current weights are:

| Criterion | Weight |
|-----------|-------:|
| Skills | 4 |
| Experience | 3 |
| Languages | 2 |
| Salary | 1 |
| Remote | 1 |
| Country | 1 |

The policy should not contain matching logic.

---

# Matching Score Calculator

`MatchingScoreCalculator` combines all `CriterionMatch` objects into a final score.

The calculation algorithm is intentionally isolated from the rest of the application.

This allows new scoring strategies to be introduced without modifying `JobMatchingService`.

---

# Algorithm Evolution

## Initial implementation

The first implementation returned the highest individual score.

```
score = max(criteria_scores)
```

Although simple, this approach ignored most of the available information.

A job with one perfectly matching criterion obtained the maximum score even if all other criteria failed.

---

## Current Scoring Algorithm

The current implementation calculates a weighted average over all applicable criteria.

Only applicable criteria participate in the final score.

Each criterion contributes proportionally to its configured weight.

Pseudo-code:

```
weighted_sum = 0
total_weight = 0

for criterion_match in criterion_matches:

    if not criterion_match.applicable:
        continue

    weight = policy.weight_for(
        criterion_match.criterion,
    )

    weighted_sum += (
        criterion_match.score * weight
    )

    total_weight += weight

if total_weight == 0:
    return 0

return weighted_sum / total_weight
```

This approach has several advantages:

- criteria without sufficient information do not penalize the final result;
- more important criteria have greater influence on the score;
- the scoring policy is independent from the evaluation logic;
- new criteria can be introduced with minimal changes.

## Why a Weighted Average?

Earlier versions of the project selected the highest individual criterion score.

Although simple, this approach ignored the overall quality of the match and could overestimate compatibility.

For example, a candidate with one perfectly matching criterion and several poor matches could still receive the highest possible score.

The weighted-average approach evaluates the complete candidate profile while allowing more important criteria to contribute more strongly than others.

This produces a score that better reflects the overall compatibility between a candidate and a job offer.

The current implementation exposes a `weight_for()` method so that the score calculator remains independent from the internal representation of the policy.


# Design Goals

The matching algorithm should remain:

- deterministic;
- explainable;
- extensible;
- independently testable;
- independent from the workflow and CLI layers.

These goals guide future iterations of the project.

## Phase 15 – Match explanation

### Motivation

Up to Phase 14, the main objective of the matching engine was to calculate an accurate score representing how well a candidate matches a job offer.

Starting with Phase 15, the focus shifts from **calculation** to **explanation**.

A numerical score alone is not sufficient for users to understand why a recommendation was produced. The matching engine should also expose the evidence behind every criterion.

---

### MatchResultFormatter

A new service, `MatchResultFormatter`, is responsible for converting a `MatchResult` into a human-readable report.

This responsibility intentionally lives outside the domain model.

Responsibilities:

- Format the overall matching score.
- Interpret the score using qualitative labels (e.g. *Strong match*).
- Present every applicable matching criterion.
- Display matched and missing requirements.
- Keep presentation concerns separated from the matching algorithm.

The formatter contains no business logic and never recalculates scores.

---

### Formatter architecture

The formatter follows the same orchestration pattern used by `JobMatchingService`.

```text
format()
├── _format_score()
├── _format_criteria()
│
└── _format_criterion()
        │
        ├── _format_default()
        ├── _format_experience()
        └── ...
```

Each criterion can progressively evolve its own formatting without affecting the rest of the report.

---

### Current output

The formatter currently provides:

- Overall matching score.
- Qualitative score label.
- Applicable criteria ordered by importance.
- Individual criterion score.
- Matched requirements.
- Missing requirements.

Example:

```text
Overall match: 82% (Strong match)

Criteria

Skills: 75%
  ✓ Python
  ✗ Docker

Experience: 80%

Languages: 100%
  ✓ English
```

---

### Future evolution

Current `CriterionMatch` objects expose the result of each criterion:

- score
- matched requirements
- missing requirements

However, they do not expose the evidence used to compute that score.

Examples of missing contextual information include:

- Required vs. candidate years of experience.
- Required vs. offered salary.
- Required and candidate language levels.

Future iterations will enrich `CriterionMatch` with contextual details so that the formatter can explain *why* a score was assigned, rather than only displaying the score itself.

This evolution will preserve the separation of responsibilities:

- `JobMatchingService` computes.
- `MatchingScoreCalculator` scores.
- `CriterionMatch` stores evidence.
- `MatchResultFormatter` explains.

# Phase 15 – Explainable matching

## Motivation

The matching engine originally focused on producing a single numerical score representing how well a candidate matched a job offer.

Although accurate, a single score is not sufficient for users to understand the reasoning behind a recommendation.

Phase 15 introduces an explanation layer that makes every matching decision transparent without changing the underlying algorithm.

---

## Design goals

The explanation layer follows four principles:

- The matching algorithm remains deterministic.
- Business logic is never duplicated.
- The explanation is generated from the same data used to calculate the score.
- Presentation is separated from matching logic.

---

## CriterionMatch

`CriterionMatch` evolved from a simple intermediate result into the central representation of an evaluated matching criterion.

Each criterion now contains:

- criterion
- score
- applicable
- matched
- missing
- details

The `details` field stores contextual information used to explain the assigned score.

Examples:

Experience

```python
details = {
    "candidate": 4,
    "required": 5,
}
```

Salary

```python
details = {
    "candidate": 40000,
    "required": 45000,
    "currency": "EUR",
}
```

Languages

```python
details = {
    "candidate": "English B2",
    "required": "English C1",
}
```

Not every criterion requires contextual details.

For example, Remote and Country are already self-explanatory through their matched and missing values.

---

## MatchResultFormatter

Presentation responsibilities have been extracted into `MatchResultFormatter`.

The formatter is intentionally independent from the matching algorithm.

Responsibilities:

- Format the overall score.
- Add qualitative labels (Excellent match, Strong match, etc.).
- Order criteria according to their importance.
- Explain each applicable criterion.
- Present matched and missing requirements.
- Display contextual details when available.

The formatter never recalculates scores.

---

## Architecture

```text
                JobMatchingService
                        │
                        ▼
               list[CriterionMatch]
                        │
                        ▼
                 MatchResult
                        │
                        ▼
            MatchResultFormatter
                        │
                        ▼
            Human-readable explanation
```

---

## Separation of responsibilities

The matching pipeline is now divided into four distinct responsibilities.

### JobMatchingService

Coordinates the matching process and builds every `CriterionMatch`.

### MatchingScoreCalculator

Calculates the overall weighted score from individual criteria.

### CriterionMatch

Stores both the result and the evidence produced by every matching criterion.

### MatchResultFormatter

Transforms the matching result into a readable explanation.

---

## Future evolution

Phase 15 intentionally focuses only on explaining already available information.

The next architectural step will improve the quality of the information entering the matching engine rather than modifying the scoring algorithm itself.

Future work will introduce semantic profile extraction, allowing candidate profiles and job offers to be enriched before matching takes place.

## Architectural direction

The current matching engine operates on normalized `CandidateProfile` and `JobOffer` objects.

Future iterations will introduce an enrichment layer responsible for transforming raw documents (such as CVs and job descriptions) into normalized semantic profiles before matching.

This evolution preserves the existing matching engine while improving the quality and consistency of its inputs.