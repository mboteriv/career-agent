# ADR-0004: Entity Identifiers

## Status

Accepted

## Context

Cada portal de empleo utiliza su propio sistema de identificación.

Los identificadores externos no son consistentes entre fuentes y no garantizan unicidad global.

Career Agent debe poder combinar ofertas procedentes de múltiples plataformas sin depender de identificadores ajenos.

## Decision

Cada JobOffer tendrá un identificador interno generado por Career Agent.

El identificador será independiente de la fuente de origen.

Los identificadores externos se conservarán únicamente como metadatos.

Siempre que sea posible, el identificador interno se generará a partir de información estable de la oferta (por ejemplo: empresa, título, ubicación y URL).

## Consequences

### Advantages

- Independencia respecto a cualquier portal.
- Deduplicación más sencilla.
- Posibilidad de combinar múltiples fuentes.
- Persistencia estable aunque cambie el sistema externo.

### Disadvantages

- Será necesario definir una estrategia robusta para generar el identificador.
- Algunos casos límite podrían requerir reglas adicionales de deduplicación.

## Future considerations

La estrategia de generación del identificador podrá evolucionar sin modificar el resto del sistema, siempre que se mantenga la unicidad de las entidades existentes.
