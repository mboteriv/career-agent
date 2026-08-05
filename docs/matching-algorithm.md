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