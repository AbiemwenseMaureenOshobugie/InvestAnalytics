# InvestAnalytics

**Investment Intelligence & Portfolio Decision-Support Platform for Nigerian and global equities.**

InvestAnalytics is a governed investment analytics platform designed for both individual investors and professional investment workflows.

Its purpose is to help users:

- understand portfolios and exposures;
- analyze performance and risk;
- research securities and investment theses;
- connect assumptions to evidence;
- investigate material changes;
- run scenarios;
- monitor investments and thesis conditions;
- use AI-assisted analysis grounded in deterministic analytics and evidence;
- preserve decision and analytical provenance.

## Current status

**Foundational specification phase — v0.1**

The repository is establishing the product constitution, product charter, master development context, and user/system workflow specification before the main implementation begins.

## Product loop

**Observe → Analyze → Explain → Investigate → Simulate → Decide → Monitor → Observe**

## Initial scope

- **Asset class:** Equities
- **Markets:** Nigeria + global
- **Users:** Individual investors + professional investment workflows

The architecture is intended to support future multi-asset expansion without prematurely implementing those asset classes.

## Foundational documents

- [Project Constitution](docs/PROJECT_CONSTITUTION.md)
- [Product Charter](docs/PRODUCT_CHARTER.md)
- [Master Context](docs/MASTER_CONTEXT.md)

The next major artifact is the **InvestAnalytics User & System Workflow Specification v0.1**.

## Architectural principle

AI is an assistant over governed domain services and deterministic analytics:

**User → AI interface → domain/tool service → deterministic analysis → evidence → AI interpretation → human decision**

InvestAnalytics is not initially an autonomous trading system, stock-price prediction engine, guaranteed-return system, or generic financial chatbot.
