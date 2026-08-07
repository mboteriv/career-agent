# Phase 16 — ESCO Analysis

## Goal

Understand the ESCO dataset before implementing the import pipeline.

The objective is not to mirror ESCO.

The objective is to determine which parts of ESCO provide value for
Career Agent and how they map to the internal knowledge model.

## Principles

Career Agent owns its domain model.

ESCO is only one possible provider.

The import process transforms ESCO concepts into Career Agent
knowledge.

Unused ESCO concepts are intentionally ignored.

## Flow

ESCO Distribution
        │
        ▼
ESCOReader
        │
        ▼
ExternalKnowledge
        │
        ▼
KnowledgeCompiler
        │
        ▼
Knowledge
        │
        ▼
SQLite

## Expected information

| ESCO concept      | Career Agent    |
| ----------------- | --------------- |
| Skill             | Skill           |
| Occupation        | Occupation      |
| Alternative label | SkillAlias      |
| Relationship      | OccupationSkill |


The first implementation ignores:

- multilingual descriptions
- concept hierarchy
- broader concepts
- narrower concepts
- metadata
- publication information
- licensing metadata
- RDF relationships not used by Career Agent

## Expected transformations

| ESCO               | Career Agent       |
| ------------------ | ------------------ |
| UUID               | Internal id        |
| Preferred label    | preferred_label    |
| Alternative label  | alias              |
| Occupation → Skill | occupation_skill   |
| Provider id        | external_reference |

Career Agent may enrich imported knowledge with:

- manually curated aliases

- domain-specific mappings

- custom occupations

- additional relationships

- user corrections

## Future versions

Future versions may additionally import:

- technologies

- certifications

- industries

- educational qualifications

- tools

- software products

## Acceptance criteria

The first ESCO integration is considered complete when:

- skills can be imported

- occupations can be imported

- occupation-skill relationships exist

- aliases are searchable

- the application performs no runtime calls to ESCO

- all knowledge is available offline

## Dataset

Provider: ESCO

Version: 1.2.1

Language: English

Format: CSV

Downloaded: 2026-08-06