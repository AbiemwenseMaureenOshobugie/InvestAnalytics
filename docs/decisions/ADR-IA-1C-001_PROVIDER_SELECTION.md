# ADR-IA-1C-001: First Market-Data Provider Adapters

- Status: Accepted
- Date: 2026-09-20
- Scope: IA-1C Market Data Ingestion Foundation

## Context

IA-1A and IA-1B require provider-independent canonical identities, observations, provenance, validation, and persistence. IA-1C is the first milestone that connects InvestAnalytics to external market-data providers.

The first provider pair must test the adapter boundary against materially different external representations rather than allow one vendor's API model to become the canonical model.

The selected Nigerian provider, formerly known as NGX Pulse, is now marketed as Kobo Terminal. Provider marketing names are not stable architectural identifiers.

## Decision

The first IA-1C adapter pair is:

- Nigerian market: Kobo Terminal, formerly NGX Pulse.
- Global market: EODHD.

The selections are provisional with respect to eventual production/vendor licensing. Before production use, current API access, rate limits, historical coverage, corporate-action coverage, retention rights, display/redistribution rights, pricing, and commercial terms must be verified against the intended use.

### Stable internal adapter identifiers

Provider marketing names must not be used as domain identifiers, persistence identifiers, configuration keys, or business rules.

IA-1C will use stable internal adapter identifiers:

- ng_primary — first Nigerian-market adapter.
- global_primary — first global-market adapter.

The mapping from internal identifier to external provider is configuration/infrastructure metadata.

If the external provider changes its marketing name, is acquired, or is replaced while the adapter contract remains suitable, the canonical domain contracts do not change. A provider replacement is a deliberate infrastructure/ADR change, not a domain-model rename.

The codebase must not contain business logic that branches on strings such as NGX Pulse, Kobo Terminal, or other provider marketing names. Provider-specific names may appear only in infrastructure metadata, documentation, provenance/source metadata, and operational configuration where needed for human identification.

## Rationale

Kobo Terminal provides a direct Nigerian-market boundary and therefore avoids adding Mansa's aggregation layer to the first Nigerian adapter. It also exposes Nigerian-specific identifiers and market semantics.

EODHD provides broad global exchange coverage, explicit identifier mapping, historical market data, corporate-action endpoints, and active/delisted instrument information. This creates a materially different provider boundary from the Nigerian adapter.

The pair therefore tests:

- provider-specific identifiers;
- listing/exchange conventions;
- rate limiting;
- historical retrieval;
- corporate actions;
- adjustment semantics;
- validation and normalization;
- provenance;
- partial failures and retries.

## Alternatives considered

### Mansa Markets + EODHD

Rejected for the first Nigerian adapter because Mansa introduces an additional aggregation layer over Nigerian data. It remains a candidate for a future African-market adapter.

### NGX direct + EODHD

Deferred because the direct NGX historical-data path is licensing/manual-data oriented rather than a self-service API adapter suitable for the first automated ingestion foundation.

### Tiingo + EODHD

Not selected because the first global adapter benefits more from EODHD's explicit identifier mapping, corporate-action coverage, and broad exchange/reference-data capabilities. Tiingo remains a viable future price-data provider.

### FMP + EODHD

Not selected because FMP's broader multi-asset scope is not required to prove the IA-1C equity ingestion boundary, while its display/redistribution licensing requires separate commercial agreement.

## Consequences

Positive:
- Two genuinely different provider representations exercise the abstraction.
- Provider identity is separated from provider marketing names.
- Provider changes do not require canonical-domain renaming.
- Future providers can be added without changing domain contracts.

Tradeoffs:
- Two adapters increase implementation and test surface.
- Provider-specific licensing and access terms must be tracked separately.
- Adapter tests must prove both adapters map into the same canonical contracts.

## Follow-up

IA-1C must define the provider adapter contract before SDK-specific code is introduced. Provider SDKs, if used, remain inside infrastructure adapters.
