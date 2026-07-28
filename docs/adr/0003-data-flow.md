# ADR-0003: Data Flow

## Status

Accepted

## Context

Career Agent obtiene ofertas de múltiples fuentes con formatos heterogéneos (HTML, JSON, APIs, etc.).

Cada módulo del sistema debe tener una única responsabilidad y trabajar de forma independiente del resto.

## Decision

El flujo de datos seguirá una arquitectura por etapas.

Cada etapa recibirá un objeto de entrada y devolverá un objeto distinto, evitando modificar directamente los datos de la etapa anterior.

El flujo inicial será:

SourceJobOffer
↓

ParsedJobOffer
↓

JobOffer

Las responsabilidades serán:

- SourceJobOffer: representa exactamente la información obtenida de una fuente externa, sin modificaciones.
- ParsedJobOffer: representa la información extraída de la fuente y estructurada en campos conocidos.
- JobOffer: representa una oferta completamente normalizada dentro del dominio de Career Agent.

Los módulos se comunicarán exclusivamente mediante estos objetos.

Ningún módulo accederá directamente a otro ni modificará datos fuera de su responsabilidad.

## Consequences

### Advantages

- Bajo acoplamiento.
- Fácil incorporación de nuevas fuentes.
- Pruebas unitarias sencillas.
- Pipeline claramente definido.
- Cada etapa tiene una única responsabilidad.

### Disadvantages

- Existirán varios modelos que representan la misma oferta en distintos estados.
- Será necesario implementar transformaciones explícitas entre modelos.

## Future considerations

En el futuro podrán añadirse nuevas etapas al pipeline (por ejemplo, enriquecimiento de datos o análisis mediante IA) sin modificar las existentes.
