# Phase 16 — SQLite Schema

## Goal

Define the persistent knowledge model used by Career Agent.

The schema is optimized for querying,
not for mirroring ESCO.

## Tables

# skill
- id
- preferred_label
- description

# skill_alias
- skill_id
- alias
- normalized_alias

# occupation
- id
- preferred_label
- description

# occupation_skill
- occupation_id
- skill_id

# external_reference
- entity_type
- entity_id
- provider
- external_id

## Indices
- skill.preferred_label
- skill_alias.alias
- occupation.preferred_label
- occupation_skill.skill_id
- occupation_skill.occupation_id

## Relationships
Occupation

↓

OccupationSkill

↓

Skill

↓

SkillAlias

## Target queries
- Find skill by label.
- Find skill by alias.
- Find occupation by label.
- Find all skills of an occupation.
- Find all occupations requiring a skill.

## Explicit decisions
- SQLite is read-only during normal application execution.
- Knowledge is rebuilt offline.
- The application never modifies imported ESCO data.
- Custom Career Agent knowledge will be stored separately from imported knowledge.