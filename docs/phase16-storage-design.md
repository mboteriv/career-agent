# Phase 16 – Storage Design

## Motivation

Career Agent uses ESCO as a semantic knowledge provider.

However, ESCO is not the application's domain model.

The application owns its own persistence layer and imports only the
information required by the matching engine.

This document defines the persistent storage used by Career Agent.

---

# Design principles

## 1. Career Agent owns the database

ESCO is an external data source.

Career Agent never queries ESCO directly during normal execution.

Instead:

ESCO

↓

Importer

↓

Career Agent database

↓

SemanticProvider

---

## 2. Offline first

All semantic information is available locally.

No Internet connection is required during matching.

Benefits

- deterministic behaviour
- reproducible results
- low latency
- no external dependency
- versioned knowledge

---

## 3. Import once

ESCO data is imported during a dedicated import process.

Normal application execution never reads ESCO CSV files.

---

## 4. Separate entities from relationships

Professional concepts remain independent from the semantic relationships
connecting them.

This simplifies maintenance and future extensions.

---

# Architecture

ESCO CSV

↓

Importer

↓

Career Agent Database

↓

Repositories

↓

SemanticProvider

↓

ProfessionalProfile

---

# Persistent entities

The persistence layer stores professional concepts independently.

## Occupation

Stores occupations imported from ESCO.

Fields

- id
- external_id
- preferred_label
- description
- status

---

## Skill

Stores professional skills.

Fields

- id
- external_id
- preferred_label
- description
- category

Possible categories include

- skill
- knowledge
- language
- competence

---

## Certification

Stores recognised certifications.

Initially optional.

---

# Relationship tables

Relationships are stored independently.

## OccupationSkillRelation

Represents the relationship between occupations and skills.

Fields

- occupation_id
- skill_id
- relation_type

Relation types

- essential
- optional

---

## SkillHierarchyRelation

Represents broader and narrower skills.

Fields

- parent_skill_id
- child_skill_id

---

## AlternativeLabel

Stores multilingual alternative labels.

Fields

- entity_id
- language
- label

This enables multilingual lookup while preserving a single semantic entity.

---

# Candidate data

Candidate data is intentionally separated from ESCO.

ProfessionalProfile references semantic entities but never duplicates them.

Example

ProfessionalProfile

↓

SkillReference

↓

Skill

---

# Job data

Job offers follow the same approach.

JobOffer

↓

ProfessionalProfile

↓

SkillReference

↓

Skill

Both candidate and job reference the same semantic concepts.

---

# Repository layer

The persistence layer is accessed only through repositories.

Examples

OccupationRepository

SkillRepository

SemanticRelationRepository

The matching engine never performs direct database queries.

---

# Import process

The importer is responsible for

- reading ESCO CSV files
- validating data
- transforming records
- storing normalized entities
- storing semantic relationships

The importer never contains matching logic.

---

# Versioning

The database records the ESCO version used during import.

This guarantees reproducible matching behaviour across application updates.

---

# Future extensions

The persistence layer should allow additional providers.

Examples

- O*NET
- Proprietary taxonomies
- Internal company knowledge

The database schema should remain stable regardless of the provider used.

---

# Non-goals

The persistence layer does not store

- CV files
- generated recommendations
- AI prompts
- embeddings
- chat history

These belong to higher application layers.

---

# Architectural summary

Career Agent owns the semantic persistence layer.

ESCO provides knowledge.

Repositories expose domain objects.

SemanticProvider builds semantic profiles.

The matching engine consumes semantic profiles without knowing their origin.