# InvestAnalytics Master Context

**Version:** 0.1  
**Purpose:** Working context for development engines and future contributors.

## 1. Project

**InvestAnalytics** is an Investment Intelligence & Portfolio Decision-Support Platform for Nigerian and global equities.

The repository is:
**AbiemwenseMaureenOshobugie/InvestAnalytics**

## 2. Product objective

Build a serious, scalable, governable platform that helps users understand, analyze, research, monitor, simulate, and make human investment decisions using reliable data and quantitative analytics.

The product is not intended to predict prices or autonomously decide what users should buy or sell.

## 3. User model

Support both:

- individual investors;
- professional investors and investment teams.

Professional workflows are the foundation. Individual experiences should use the same underlying domain and analytical services.

## 4. Current asset and geography scope

Initial asset class:

**Equities**

Initial markets:

**Nigeria + global**

Future asset classes are deliberately deferred until the equity foundation is mature.

## 5. Core product loop

**Observe → Analyze → Explain → Investigate → Simulate → Decide → Monitor → Observe**

## 6. Primary domains

1. Portfolio Management
2. Market & Fundamental Data
3. Performance Analytics
4. Risk Analytics
5. Investment Research
6. Intelligence & Monitoring
7. AI
8. Governance

## 7. Research model

Investment research should make the relationship between a thesis and its supporting logic explicit:

**Thesis → Assumptions → Evidence → Monitoring**

Research objects should preserve provenance and make invalidation conditions possible to represent.

## 8. AI rule

The canonical architecture is:

**User → AI interface → domain/tool service → deterministic analysis → evidence → AI interpretation → human decision**

AI should orchestrate and explain governed analytical services, not replace authoritative financial calculations.

AI must not fabricate:

- market data;
- financial statements;
- calculations;
- evidence;
- citations;
- research conclusions.

## 9. Data architecture principle

External provider data should pass through:

**provider → raw data → validation → normalization → canonical data model → analytics**

Raw provider data must remain distinguishable from normalized and interpreted data, with provenance retained wherever practical.

Provider-specific logic should be isolated behind adapters.

## 10. Technology direction

The initial technology direction is:

- Python backend/quantitative layer;
- PostgreSQL;
- FastAPI;
- React + TypeScript;
- Power BI integration/reporting;
- GitHub + GitHub Actions.

These are architectural candidates until validated during IA-0.

## 11. Development sequence

### IA-0 — Foundation
Establish product architecture, domain model, security model, data architecture, development standards, and governance.

### IA-1 — Equity Intelligence Core
Build securities, markets, prices, corporate actions, fundamentals, portfolios, and transactions.

### IA-2 — Portfolio Analytics
Build valuation, performance, attribution, allocation, and benchmarking.

### IA-3 — Risk Intelligence
Build volatility, drawdown, correlation, concentration, VaR, Expected Shortfall, and stress testing.

### IA-4 — Investment Research
Build research objects, thesis, evidence, assumptions, and invalidation conditions.

### IA-5 — Monitoring
Build change detection, thesis monitoring, alerts, and risk monitoring.

### IA-6 — AI Analyst
Build natural-language interaction, tool use, evidence retrieval, reasoning, and explainability.

### IA-7 — Professional Platform
Build organizations, permissions, collaboration, committees, reporting, and audit.

### IA-8 — Multi-Asset Expansion
Expand beyond equities after the equity foundation is sufficiently mature.

## 12. Immediate workflow

The project should proceed in this order:

1. Establish foundational project documentation.
2. Define **InvestAnalytics User & System Workflow Specification v0.1**.
3. Derive the domain model from the approved workflows.
4. Derive the architecture from the domain model and system requirements.
5. Establish the Python/API/web project skeleton.
6. Implement IA-0 foundation capabilities.
7. Begin IA-1 only after the relevant contracts are stable.

## 13. Multi-engine collaboration rules

A secondary engine may inspect, research, propose, implement when authorized, test, and document.

It must not silently redefine:

- product scope;
- approved architecture;
- domain semantics;
- analytical definitions;
- AI governance;
- security boundaries.

Before making changes, inspect the current repository state and relevant specifications.

After making changes, verify the repository state, inspect the diff, run appropriate tests, and report the exact commit SHA and limitations.

Do not overwrite or undo another engine's work without first understanding the change and documenting the reason.

## 14. Source-of-truth rules

- The user has final product authority.
- Approved repository specifications define intended behavior.
- Git history defines actual implementation state.
- Tests define validated implementation behavior.
- Conversation context may guide development but should be converted into repository documentation when it becomes an approved project decision.

## 15. Immediate next artifact

The next major specification is:

**InvestAnalytics User & System Workflow Specification v0.1**

It should define, at minimum:

1. Create portfolio
2. Add/import holdings
3. Ingest market data
4. Analyze portfolio performance
5. Investigate a performance change
6. Research a security
7. Create an investment thesis
8. Monitor a thesis
9. Run a scenario
10. Produce an investment report
11. Ask the AI analyst a question
12. Record a human investment decision

The workflow specification must be derived from the product charter and constitution rather than introducing an unrelated product direction.
