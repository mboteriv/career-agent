# Career Agent

Career Agent is a personal project for collecting, normalizing, ranking and tracking software engineering job offers from multiple recruiting platforms.

The goal is to provide a single, normalized view of job offers regardless of their original source.

## Current architecture

```
                    Greenhouse API
                          │
                          ▼
                GreenhouseClient
                          │
                          ▼
               GreenhouseCollector
                          │
                          ▼
                 SourceJobOffer
                          │
                          ▼
                 GreenhouseParser
                          │
                          ▼
                 ParsedJobOffer
                          │
                          ▼
              JobOfferNormalizer
                          │
                          ▼
                     JobOffer
                          │
                          ▼
                 JobImportService
```

## Project structure

```
src/
└── career_agent/
    ├── clients/
    ├── collectors/
    ├── models/
    ├── normalizers/
    ├── parsers/
    └── services/
```

## Current features

- Greenhouse API integration
- HTTP client abstraction
- Job collection
- Parsing into provider-independent models
- Job normalization
- Application service for importing jobs
- Automated test suite

## Running the demo

```bash
uv run python scripts/greenhouse_demo.py
```

## Running the tests

```bash
uv run pytest
```

Current status:

- 27 passing tests
- Greenhouse integration working
- End-to-end import pipeline completed

## Roadmap

- [x] Greenhouse integration
- [x] Job import service
- [ ] Lever integration
- [ ] Ranking engine
- [ ] Filtering
- [ ] Notifications
- [ ] Persistence
- [ ] CLI