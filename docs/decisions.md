# Architecture Decisions

This document records the most important architectural decisions made during the evolution of Career Agent.

The goal is to preserve the reasoning behind each decision so that future changes can be evaluated in context.

---

# ADR-001

## JobMatchingService acts as an orchestrator

### Decision

`JobMatchingService` should coordinate the matching process but should not contain complex business logic.

### Motivation

Early versions concentrated most responsibilities in a single method.

As the matching algorithm evolved, responsibilities were extracted into dedicated components.

### Consequences

Responsibilities are now distributed between:

- JobMatchingService
- CriterionMatch
- MatchingScoreCalculator
- MatchingPolicy

---

# ADR-002

## CriterionMatch represents a complete criterion evaluation

### Decision

A `CriterionMatch` stores all information related to the evaluation of one criterion.

### Motivation

The project originally computed scores and explanations independently.

This duplicated logic and made future extensions difficult.

### Consequences

Each criterion now stores:

- score
- applicability
- matched requirements
- missing requirements

---

# ADR-003

## Non-applicable criteria do not affect the final score

### Decision

A criterion that cannot be evaluated does not participate in the score calculation.

### Motivation

Lack of information should not penalize either the candidate or the job offer.

### Example

A job offer without salary information should neither increase nor decrease compatibility based on salary expectations.

---

# ADR-004

## MatchingPolicy stores configuration only

### Decision

`MatchingPolicy` contains configuration values but no business logic.

### Motivation

Separating configuration from algorithms simplifies testing and allows multiple scoring strategies.

---

# ADR-005

## MatchingScoreCalculator owns the scoring algorithm

### Decision

The score calculation is isolated in a dedicated service.

### Motivation

Different scoring strategies should not require modifications to the matching workflow.

---

# ADR-006

## Criterion applicability is determined before scoring

### Decision

Each criterion determines whether it applies before the score is calculated.

### Motivation

The scoring algorithm should only combine already evaluated criteria.

It should not contain domain-specific rules.
