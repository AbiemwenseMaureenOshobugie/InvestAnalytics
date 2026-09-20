# IA-1C Provider Evaluation

**Status:** Decision input for IA-1C  
**Research date:** 2026-09-20  
**Scope:** First concrete market-data adapters for Nigerian and global equities

## 1. Purpose

IA-1A and IA-1B deliberately defined provider-independent data and persistence contracts. IA-1C is the first milestone that crosses the system boundary into external market-data providers.

This document evaluates candidate providers before the IA-1C specification is drafted. It does **not** define provider-specific domain contracts and does not commit InvestAnalytics to an eventual production data vendor.

The evaluation is deliberately concerned with whether a provider can stress the adapter boundary, preserve provenance, support canonical normalization, and provide sufficient data for the first equity-intelligence workflows.

## 2. Decision context

The first adapter set should contain:

1. one Nigerian-market adapter; and
2. one global-market adapter.

The purpose of using two providers is not merely geographic coverage. The providers should expose materially different:

- identifier conventions;
- exchange/listing models;
- rate-limit behavior;
- historical-data access;
- corporate-action representations;
- adjustment semantics;
- authentication patterns; and
- licensing/usage constraints.

This gives IA-1C a meaningful test of provider abstraction rather than allowing one provider's API shape to become the de facto canonical model.

## 3. Evaluation criteria

| Criterion | Why it matters to IA-1C |
|---|---|
| Equity coverage | Establishes whether the adapter can populate the initial security/listing universe |
| Nigerian/global market coverage | Determines geographic suitability for the first adapter pair |
| Historical depth | Required for reproducible analytics and historical portfolio analysis |
| OHLCV quality | Core market-observation input |
| Corporate actions | Required for trustworthy historical interpretation and later adjusted-series handling |
| Identifier quality | Tests provider-independent security/listing identity and mapping |
| API availability | Required for automated ingestion |
| Authentication | Shapes credential handling without leaking provider concerns into domain code |
| Rate limits | Determines batching, throttling, retry, and scheduling requirements |
| Reliability/operability | Determines ingestion retry and data-quality behavior |
| Documentation/SDK support | Reduces adapter implementation risk while preserving the abstraction |
| Raw-response accessibility | Supports source-record retention and provenance |
| Licensing/usage rights | Important because InvestAnalytics is intended to mature into a professional platform |
| Cost/development accessibility | Determines feasibility of development and integration testing |
| Provider independence | Avoids accidentally coupling the canonical model to vendor-specific semantics |

## 4. Nigerian candidates

### 4.1 Kobo Terminal (formerly NGX Pulse)

The provider formerly surfaced as NGX Pulse was renamed **Kobo Terminal** in August 2026. The provider states that the product, developer API, accounts, and API keys continue through the transition.

Kobo Terminal provides Nigerian market intelligence including NGX and NASD OTC securities, indices, ETFs, corporate disclosures, and a developer API. Its public material explicitly directs developers to the API for programmatic access to market data.

**Architectural relevance:** this is a direct Nigerian-market source rather than a pan-African wrapper. That makes it preferable for the first Nigerian adapter if access, licensing, and API terms are confirmed during implementation preparation.

### 4.2 Mansa Markets

Mansa Markets provides a pan-African API covering multiple African exchanges, including NGX. Its public developer documentation exposes a common API shape and identifies NGX ETF/index data as coming from Kobo Terminal (formerly NGX Pulse).

Current public pricing shows a free developer tier and paid tiers with commercial rights. This makes Mansa attractive as a future African-market aggregation adapter, but it is less useful than a direct Kobo adapter for testing the boundary against the underlying Nigerian source.

### 4.3 NGX direct

The Nigerian Exchange remains the authoritative exchange-level source and a future licensing/data relationship may be important for production use. However, the direct historical-data process is not equivalent to a self-service API adapter.

It should therefore remain a **future authoritative-source/licensing track**, not the first automated IA-1C adapter.

## 5. Global candidates

### 5.1 EODHD

EODHD provides broad exchange coverage, historical market data, corporate actions, fundamentals, exchange/ticker metadata, and identifier mapping.

Its current documentation exposes:
- exchange and ticker lists;
- active and delisted securities;
- ISIN where available;
- corporate-action endpoints for dividends and splits;
- identifier mapping for CUSIP, ISIN, OpenFIGI, LEI and CIK;
- historical and intraday market-data endpoints.

Its current commercial pricing page lists an All World historical-data plan and an EOD+Intraday plan, making development access substantially more practical than relying on a highly restricted free tier.

**Architectural relevance:** EODHD exercises exactly the kinds of provider differences IA-1C needs: exchange-coded symbols, multiple identifier systems, corporate-action endpoints, and explicit distinction between active/delisted instruments.

### 5.2 Tiingo

Tiingo provides broad global securities coverage and deep historical price data. Its current pricing documentation shows substantial request quotas and historical coverage, but its standard plans are explicitly limited to internal use. Fundamental data is also separately positioned as an add-on.

**Architectural relevance:** Tiingo's price-data workflow is attractive for local historical-price maintenance, but the licensing boundary is less suitable as the first provider for a platform intended eventually to display/share investment data.

### 5.3 Financial Modeling Prep (FMP)

FMP provides a broad financial-data API covering market prices, fundamentals, ratios, calendars, and additional asset classes. Current pricing includes global coverage at higher tiers.

However, FMP's current commercial terms explicitly state that displaying or redistributing sourced data requires a specific Data Display and Licensing Agreement.

**Architectural relevance:** FMP is a viable future provider, particularly if InvestAnalytics expands into broader asset classes and fundamental-data workflows, but its licensing model should not be assumed to fit the initial platform without a commercial agreement.

## 6. Comparative matrix

| Criterion | Kobo Terminal | Mansa Markets | EODHD | Tiingo | FMP |
|---|---|---|---|---|---|
| Primary scope | Nigerian | Pan-African | Global | Global | Global/multi-asset |
| NGX coverage | Native/direct | Yes, via Mansa/Kobo data layer | Not selected as Nigerian source | Not selected as Nigerian source | Broader coverage depends on plan |
| Historical price data | Yes; API access exists | Yes | Yes | Yes | Yes |
| Corporate actions | Yes, Nigerian disclosures/data domain | Yes, plan-dependent features | Strong dividends/splits coverage | Available in product ecosystem; exact first-adapter scope requires verification | Available on higher plans |
| Identifier facilities | Nigerian ticker/listing oriented | Common API + African market identity | Strong explicit ID-mapping API | Provider symbols | Provider symbols/reference data |
| Rate-limit model | Provider-specific; must be verified during adapter onboarding | Daily request quotas by tier | Plan/request quotas | Hourly/daily quotas | Minute-based quotas by plan |
| API/SDK maturity | Direct API | API + SDK ecosystem | API + SDKs | API | API + SDK ecosystem |
| Raw-response retention suitability | Yes, subject to API terms | Yes, subject to API terms | Yes, subject to API terms | Yes, subject to API terms | Yes, subject to API terms |
| Commercial/redistribution posture | Must be confirmed before production | Commercial rights on paid tiers | Commercial plans available | Standard plans marked internal-use | Display/redistribution requires agreement |
| Primary architectural value | Direct Nigerian-provider boundary | Future African aggregation boundary | Strong global-provider boundary | Price-data alternative | Future broader-data alternative |
| IA-1C role | **Recommended first Nigerian adapter** | Secondary/future adapter | **Recommended first global adapter** | Alternative candidate | Alternative/future provider |

## 7. Recommended first adapter pair

### Nigerian: Kobo Terminal

**Recommendation:** use **Kobo Terminal**, formerly NGX Pulse, as the first Nigerian adapter.

Rationale:

1. It is the direct continuation of the Nigerian provider identified during research.
2. It exposes a Nigerian-specific data model, which gives the provider abstraction a materially different boundary from the global adapter.
3. It provides programmatic access to Nigerian market data.
4. It avoids adding the additional aggregation layer introduced by Mansa.
5. Mansa can remain a useful future adapter for broader African-market coverage.

This recommendation is **provisional pending confirmation of current API documentation, access terms, rate limits, raw-response retention rights, and commercial licensing requirements during IA-1C implementation planning.**

### Global: EODHD

**Recommendation:** use **EODHD** as the first global adapter.

Rationale:

1. Broad exchange coverage supports the global-equity requirement.
2. Exchange/ticker metadata directly supports listing and identifier-resolution work.
3. Its explicit identifier-mapping API is unusually relevant to the IA-1A/IA-1B identity contracts.
4. Its corporate-action APIs allow IA-1C to test event ingestion separately from market observations.
5. Active/delisted ticker handling supports historical-universe requirements.
6. Its commercial plans provide a practical path for development and later evaluation of production licensing.

This is also **provisional**: the adapter must isolate EODHD-specific semantics and must not allow its symbol format, adjustment model, or response schema to become the canonical InvestAnalytics model.

## 8. Why Kobo Terminal + EODHD is a useful abstraction test

The selected pair intentionally creates different external representations:

```
Kobo Terminal
  Nigerian listing/security conventions
  Nigerian market/session semantics
  Provider-specific identifiers
        │
        ▼
   Provider Adapter
        │
        ├── raw source record
        ├── validation
        ├── normalization
        └── canonical observation
        ▲
        │
   Provider Adapter
        │
EODHD
  exchange-coded symbols
  global identifier mappings
  active/delisted universe
  explicit corporate-action endpoints
```

The canonical InvestAnalytics contracts must sit above both providers.

The system must never require the domain layer to know that one provider uses a particular ticker suffix, endpoint name, adjustment field, or authentication mechanism.

## 9. Provider-specific concerns that IA-1C must test

The first adapters should deliberately exercise:

### Identity

- provider symbol → canonical listing
- provider instrument ID → provider-independent security identity
- exchange/listing mapping
- identifier conflicts
- unresolved identifiers
- delisted securities

### Market observations

- date/time semantics
- exchange timezone
- session boundaries
- OHLCV field presence
- missing/null fields
- duplicate observations
- revised observations
- adjusted versus unadjusted values

### Corporate actions

- dividends
- splits
- effective/ex dates
- provider-specific event representations
- event corrections
- relationship between corporate actions and historical observations

### Ingestion

- pagination/batching
- daily versus request-rate quotas
- retryable failures
- non-retryable provider errors
- authentication failures
- partial responses
- provider outages
- idempotent replay

### Provenance

Every accepted canonical observation must remain traceable to:

```
provider
→ source request
→ raw record/artifact
→ validation result
→ normalization result
→ canonical observation
```

## 10. What this document does not decide

This document does **not** finalize:

- production provider licensing;
- exact API plan;
- exact endpoint set;
- exact provider request schedule;
- canonical database schema;
- raw-object storage technology;
- S3-compatible implementation;
- exact retry/backoff parameters;
- exact corporate-action normalization rules;
- provider-specific SDK dependency;
- production data redistribution rights.

Those decisions belong in IA-1C and its associated ADRs.

## 11. Related raw-storage decision

IA-1B identified raw-record storage as an ADR-worthy architectural decision.

The current direction remains:

**PostgreSQL metadata + object storage for immutable raw payloads.**

The storage abstraction should be provider- and storage-vendor-independent. The domain/application boundary should express operations such as:

```
store(raw_payload) → source_artifact_reference
retrieve(source_artifact_reference) → raw_payload
```

rather than exposing S3/MinIO-specific operations.

For local development and CI, an S3-compatible test implementation may be selected separately. The preferred direction for IA-1C is lightweight CI storage emulation and a fuller S3-compatible local service where needed for developer workflows.

## 12. CI gate observation

The live repository state was checked on 2026-09-20.

The current workflow at `.github/workflows/ci.yml` triggers on:

- push to `main`
- pull requests

It currently has **no `paths-ignore` or `paths` filter**.

Therefore, the current repository does **not** presently implement the proposed docs-only CI skip behavior.

The CI policy has now been resolved by ADR-IA-1C-003: CI will continue to run on every push to main, including documentation-only commits. No paths-ignore filter will be added. The IA-1C gate therefore does not distinguish CI applicability by file type; it distinguishes the documentation/decision review from the CI result attached to the resulting HEAD.

## 13. Decision summary

| Decision | Current recommendation | Status |
|---|---|---|
| First Nigerian adapter | **Kobo Terminal (formerly NGX Pulse)** | Provisional — confirm access/licensing during IA-1C |
| First global adapter | **EODHD** | Provisional — confirm plan/licensing during IA-1C |
| Provider strategy | **Dual-provider foundation** | Recommended |
| Raw-record architecture | PostgreSQL metadata + object storage payload | Direction from IA-1B; ADR required |
| Domain storage abstraction | Provider/storage-vendor independent | Required |
| CI docs filtering | `paths-ignore` is a possible future change | Not implemented yet |
| IA-1C spec | Draft only after decisions are approved | Next gate |

## 14. Next decision gate

Before IA-1C specification drafting:

1. Approve or change the proposed first-adapter pair.
2. Approve the raw-record storage direction and record it as an ADR.
3. Decide whether the current CI workflow should be changed to skip docs-only pushes.
4. Then draft the full IA-1C specification against the approved decisions.

**No provider SDK or provider-specific application code should be introduced until that gate is complete.**
