# Phase 17 — Business Logic

## Goal

Build the first business services on top of the ESCO knowledge base.

At the end of this phase, the application should be capable of reasoning about
candidate profiles and occupations using the semantic knowledge imported during
Phase 16.

Rather than expanding the database layer, this phase focuses on services that
answer business questions.

---

## Existing infrastructure

The project already provides:

- Semantic knowledge imported from ESCO
- SQLite knowledge database
- Semantic repository abstraction
- Skill lookup by label and alias
- Occupation lookup by related skills
- Skill lookup by occupation
- Relation type lookup (essential / optional)

These components become the foundation for higher-level reasoning.

---

## Iteration 17.1 — SkillGapAnalyzer

Goal:

Determine which skills are missing for a candidate to perform a given occupation.

Responsibilities:

- Compare candidate skills with occupation skills
- Distinguish between essential and optional missing skills
- Produce a structured SkillGap model

---

## Iteration 17.2 — OccupationMatcher

Goal:

Calculate how well a candidate matches one or more occupations.

Possible metrics:

- Essential skill coverage
- Optional skill coverage
- Overall matching percentage

---

## Iteration 17.3 — SkillRecommendationEngine

Goal:

Recommend the most valuable skills for improving a candidate profile.

Possible criteria:

- Missing essential skills
- Frequently requested skills
- Highest impact on occupation matching

---

## Iteration 17.4 — CareerPathExplorer

Goal:

Explore alternative occupations related to a candidate's current skills.

Examples:

- Similar occupations
- Occupations requiring only a few additional skills
- Progressive career paths

---

## Design principles

Business services should:

- depend on SemanticRepository
- remain independent from SQLite
- perform one business responsibility only
- expose immutable domain models
- remain easily testable using fake repositories