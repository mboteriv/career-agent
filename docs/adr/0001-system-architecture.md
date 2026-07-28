# ADR-0001: System Architecture

## Status
Accepted

## Context

Career Agent debe crecer durante varios años y admitir múltiples fuentes de empleo, diferentes perfiles profesionales y distintos mecanismos de recomendación.

## Decision

Se adopta una arquitectura basada en pipelines, donde cada módulo tiene una única responsabilidad:

- Collector
- Parser
- Normalizer
- Database
- Decision Engine
- Ranking
- Notification

## Consequences

Ventajas:
- Fácil añadir nuevas fuentes.
- Fácil probar cada módulo.
- Bajo acoplamiento.
- Escalable.

Inconvenientes:
- Más archivos.
- Más interfaces.
- Algo más de código inicial.
