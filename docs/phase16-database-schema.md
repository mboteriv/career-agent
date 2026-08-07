# Phase 16 — Database Schema

## Goal

Career Agent does not use ESCO directly.

Instead, ESCO is treated as an external knowledge source that is imported
into a local SQLite database.

The SQLite database is the only knowledge source used by the application.

This allows Career Agent to:

- work completely offline;
- remain independent from ESCO;
- replace ESCO with another provider in the future;
- enrich the imported knowledge with Career Agent specific data.

## Design principles

The database models Career Agent's domain,
not ESCO's internal structure.

Every table exists because Career Agent needs it.

No table exists simply because ESCO contains it.

External identifiers are stored separately from the internal identifiers.

## Entities

| Entity            | Purpose                         |
| ----------------- | ------------------------------- |
| Skill             | Professional skill              |
| Occupation        | Professional occupation         |
| SkillAlias        | Alternative names               |
| OccupationSkill   | Occupation → Skill relationship |
| ExternalReference | Mapping to external providers   |

## Relationships

Occupation

↓

OccupationSkill

↓

Skill

↓

SkillAlias


## Internal identifiers

Career Agent owns every internal identifier.

Examples:

python

docker

accountant

translator

External identifiers (ESCO, O*NET...) are stored separately.

The application never depends on provider identifiers.

## Expected queries

The database is optimized for queries such as:

Find a skill by label.

Find a skill by alias.

Find all skills required by an occupation.

Find all occupations associated with a skill.

## Out of scope

The following ESCO concepts are intentionally ignored
during the first implementation.

- hierarchy

- broader concepts

- narrower concepts

- concept groups

- multilingual descriptions

- licensing metadata

- publication metadata

These concepts can be added later without affecting
the public domain model.

## Future extensions

Possible future entities include:

Knowledge

Capability

Certification

Tool

Technology

Language

Industry

Education

Company