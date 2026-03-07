# ADR 0002: Engine vs Domain Pack

## Status
Accepted

## Context
Engineering knowledge differs by domain, but the transformation pipeline should remain reusable.

## Decision
The repository will separate:
- domain-agnostic engine logic
- domain-specific knowledge packs

HVAC will be implemented as the first domain pack.

## Consequences
- Better long-term extensibility
- Cleaner ownership boundaries
- Lower coupling between content and engine
