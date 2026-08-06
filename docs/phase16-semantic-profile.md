# Phase 16 – Semantic Profile Extraction

## Motivation

The current matching engine compares normalized `CandidateProfile` and `JobOffer` objects.

Although this architecture provides deterministic and explainable matching, the quality of the results depends entirely on how accurately those objects are populated.

Most professional knowledge already exists inside the candidate's CV and the job description, but is currently lost or manually entered through questionnaires.

The goal of Phase 16 is to transform raw professional documents into normalized semantic profiles before matching takes place.

The matching algorithm itself should remain unchanged.

---

# Design goals

Phase 16 follows five design principles.

## 1. The CV is the primary source of truth

Candidate profiles should be created automatically from the candidate's CV whenever possible.

The user should not manually reproduce information that already exists inside the document.

Questionnaires become complementary rather than mandatory.

They provide information that normally cannot be inferred from a CV, such as:

- preferred countries
- remote preferences
- salary expectations
- contract preferences
- availability

---

## 2. Job offers follow the same semantic pipeline

The same normalization process should be applied to job offers.

Both candidates and jobs should be transformed into a common semantic representation before matching.

Matching should never compare raw text.

---

## 3. Separate extraction from matching

The matching engine should never parse documents.

Likewise, document extraction should never calculate matching scores.

Both concerns remain completely independent.

---

## 4. Knowledge providers are replaceable

Career Agent must not depend directly on any external taxonomy.

Instead, it depends on an abstraction capable of providing semantic knowledge.

This allows different providers to be introduced without modifying the matching engine.

Examples:

- ESCO
- O*NET
- proprietary providers
- future AI-based providers

---

## 5. Preserve explainability

Semantic enrichment must improve matching quality without sacrificing explainability.

Every semantic capability used during matching should be traceable back to the original CV or job description.

---

# Current architecture

Current workflow:

CandidateProfile
        │
        ▼
Matching Engine
        ▲
        │
JobOffer

---

# Target architecture

Candidate CV
        │
        ▼
CV Extraction
        │
        ▼
Semantic Enrichment
        │
        ▼
CandidateProfile
        │
        ▼
Matching Engine
        ▲
        │
JobOffer
        ▲
        │
Semantic Enrichment
        ▲
        │
Raw Job Description

---

# New components

## CandidateCV

Represents the original candidate document.

Supported formats may include:

- PDF
- DOCX
- TXT

This object contains the raw source only.

---

## CVExtractor

Responsible for extracting structured textual information from a CV.

Responsibilities:

- document parsing
- section detection
- text normalization

It does not understand professional concepts.

---

## SemanticProvider

Converts extracted text into normalized professional knowledge.

The matching engine depends on this abstraction rather than on any concrete implementation.

Possible implementations include:

- ESCOProvider
- ONETProvider
- AIProvider

---

## CandidateProfileBuilder

Builds the final CandidateProfile from:

- extracted CV information
- semantic capabilities
- user preferences

---

# CandidateProfile

CandidateProfile becomes a semantic representation rather than a manually completed questionnaire.

The model should distinguish between factual information and user preferences.

Facts

- occupations
- capabilities
- technologies
- languages
- education
- certifications
- professional experience

Preferences

- salary expectations
- preferred countries
- remote preferences
- contract type
- availability

---

# Semantic enrichment

Semantic enrichment transforms professional language into normalized concepts.

Example

CV

    Accountant
    Auditing
    Budget planning

↓

Semantic Provider

↓

Accounting capability

The same process applies to job offers.

Matching therefore compares concepts instead of literal words.

---

# ESCO

The first implementation will use ESCO (European Skills, Competences, Qualifications and Occupations).

Reasons:

- official European taxonomy
- multilingual
- occupations
- skills
- competences
- knowledge
- alternative labels
- maintained and versioned

ESCO is treated as a knowledge provider rather than a dependency of the matching engine.

---

# Responsibilities

CVExtractor

Extract text.

SemanticProvider

Normalize professional knowledge.

CandidateProfileBuilder

Build semantic candidate profiles.

Job parsers

Extract job descriptions.

Matching Engine

Calculate matching scores.

MatchResultFormatter

Explain results.

---

# Future work

Phase 16 intentionally excludes:

- CV rewriting
- AI-generated recommendations
- cover letter generation
- conversational assistants

Those features may consume semantic profiles in later phases but are not part of semantic extraction itself.

---

# Expected benefits

- Less manual profile creation.
- Better matching quality.
- Support for non-technical professions.
- Multilingual normalization.
- Explainable semantic matching.
- Easier future integration with AI services.

# Semantic model

The matching engine should never compare raw text.

Instead, it compares normalized semantic entities extracted from both the candidate profile and the job offer.

These entities represent professional knowledge independently of how that knowledge is expressed in natural language.

---

## Occupation

Represents the candidate's current or previous professional roles.

Examples:

- Software Developer
- Accountant
- Translator
- Marketing Specialist

Occupations describe **what the candidate has done**.

---

## Capability

Represents professional capabilities independently of job titles.

Examples:

- Accounting
- Backend Development
- Localization
- Project Management

Capabilities describe **what the candidate is able to do**.

---

## Skill

Represents concrete operational skills.

Examples:

- Python
- Docker
- Google Ads
- SAP FI
- MemoQ

Skills are usually observable and trainable.

---

## Knowledge

Represents theoretical or domain knowledge.

Examples:

- IFRS
- GDPR
- Machine Learning
- Translation Theory

Knowledge differs from skills because it represents understanding rather than execution.

---

## Language

Represents spoken or written languages together with proficiency.

Examples:

- English C1
- Spanish Native

---

## Experience

Represents professional experience.

Examples:

- Years of experience
- Seniority
- Relevant projects

---

## Education

Represents academic qualifications.

Examples:

- Bachelor's degree
- Master's degree
- Professional certifications

---

These entities together form the semantic representation of a professional profile.

The matching engine operates on these entities rather than on raw CV text.

# Semantic relationships

Professional knowledge is not a flat collection of independent entities.

Instead, it forms a connected semantic graph.

Career Agent should preserve these relationships whenever possible.

---

## Occupation

Occupations are professional roles.

Examples:

- Accountant
- Translator
- Backend Developer

An occupation is associated with multiple capabilities.

Example

Translator

↓

Localization

Language Quality Assurance

Terminology Management

---

## Capability

Capabilities describe what a professional is able to accomplish.

They are broader than individual skills.

A capability may require several skills and pieces of knowledge.

Example

Backend Development

↓

Python

REST APIs

SQL

Testing

---

## Skill

Skills represent concrete abilities or technologies.

Skills may support multiple capabilities.

Example

Python

↓

Backend Development

Automation

Data Analysis

Machine Learning

---

## Knowledge

Knowledge represents theoretical understanding.

Knowledge supports one or more capabilities.

Example

GDPR

↓

Data Protection

Compliance

Privacy

---

## Technologies

Technologies are concrete tools used to apply skills.

Example

Docker

↓

Containerization

↓

DevOps

Cloud Engineering

---

A single entity may participate in multiple relationships.

Career Agent should therefore model professional knowledge as a graph rather than as isolated lists.

# Semantic processing pipeline

Career Agent transforms raw documents into semantic profiles through a sequence of independent processing stages.

Each stage has a single responsibility and produces an output consumed by the next stage.

This design keeps the architecture modular, testable and extensible.

---

## Stage 1 — Document extraction

Input

- Candidate CV
- Job description

Output

Raw structured text.

Responsibilities

- Parse documents.
- Extract sections.
- Normalize formatting.
- Preserve original wording.

No semantic interpretation occurs at this stage.

---

## Stage 2 — Semantic extraction

Input

Raw structured text.

Output

Detected semantic entities.

Examples

Occupation

Translator

Skills

Python

MemoQ

Docker

Languages

English C2

Spanish Native

This stage identifies concepts but does not normalize them.

---

## Stage 3 — Semantic normalization

Input

Detected entities.

Output

Normalized semantic entities.

Example

Input

"Software Engineer"

↓

Normalized occupation

ESCO Occupation #12345

Alternative labels

Software Developer

Backend Developer

Programmer

The same process applies to skills, knowledge and capabilities.

---

## Stage 4 — Semantic enrichment

Input

Normalized entities.

Output

Enriched semantic profile.

Example

Occupation

Translator

↓

Capabilities

Localization

Terminology Management

Quality Assurance

↓

Knowledge

CAT tools

Machine Translation

Professional Writing

The profile now contains inferred information rather than only explicitly written information.

---

## Stage 5 — Profile building

Input

Semantic entities

+

User preferences

Output

CandidateProfile

CandidateProfile becomes the canonical representation used by the matching engine.

---

## Stage 6 — Matching

The matching engine compares two semantic profiles.

It never accesses raw CVs or raw job descriptions.

---

## Stage 7 — Explanation

The existing explanation layer remains unchanged.

CriterionMatch

↓

MatchResult

↓

MatchResultFormatter

↓

Human-readable explanation

## Evidence provenance

Every detected or inferred professional concept should preserve the
evidence from which it originates.

Evidence must include its professional context.

Examples include:

- professional work experience
- personal projects
- academic projects
- education
- certifications
- publications

Career Agent must distinguish between the existence of a skill and the
context in which that skill has been demonstrated.

Evidence provenance should initially describe facts rather than assign
fixed importance weights.

The relevance of different evidence sources may depend on the job,
seniority level and matching policy.

Semantic inferences must remain traceable to the evidence that supports
them.

## Deferred decision

The semantic domain model intentionally postpones the decision of whether
professional concepts should be represented by a single `SemanticEntity`
class or by a hierarchy of specialized entities.

This decision will be taken after evaluating the structure, semantics and
relationships provided by ESCO.

Until then, the architecture depends only on the concept of semantic
entities rather than on their concrete implementation.