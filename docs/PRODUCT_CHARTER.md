# InvestAnalytics Product Charter

**Version:** 0.1  
**Status:** Foundational  
**Product:** InvestAnalytics

## 1. Product identity

InvestAnalytics is an **Investment Intelligence & Portfolio Decision-Support Platform** for Nigerian and global equities, designed with professional investment workflows as the foundation while remaining usable by individual investors.

The platform is intended to turn fragmented investment information into a governed analytical workflow.

## 2. Vision

Help investors and investment professionals understand what they own, how it is performing, why performance changed, what risks and exposures exist, what assumptions support an investment thesis, what evidence supports or challenges it, what could happen under alternative scenarios, and what requires attention.

## 3. Users

The initial product serves:

- individual investors;
- professional investors and investment teams.

Professional workflows are the architectural foundation. Individual users should consume the same underlying analytical core rather than a disconnected simplified product.

## 4. Initial scope

### Asset class
Equities first.

### Geography
Nigerian and global equity markets.

### Future expansion
The architecture should permit later support for ETFs, fixed income, FX, commodities, funds, derivatives, and other asset classes without prematurely implementing them.

## 5. Core problem

Investment information is fragmented across portfolio systems, spreadsheets, market-data sources, financial statements, research documents, news, analyst notes, dashboards, and personal records.

InvestAnalytics should create a coherent system for:

- portfolio state;
- market and fundamental data;
- performance;
- risk and exposure;
- investment research;
- evidence and assumptions;
- scenario analysis;
- monitoring;
- decision history;
- governed AI assistance.

## 6. Core product loop

**Observe → Analyze → Explain → Investigate → Simulate → Decide → Monitor → Observe**

The loop is deliberately centered on human investment decisions rather than autonomous action.

## 7. Core domains

### Portfolio Management
Users, organizations, portfolios, accounts, securities, holdings, transactions, cash, benchmarks, mandates, and objectives.

### Market & Fundamental Data
Prices, OHLC, volume, adjusted prices, returns, indices, FX context, corporate actions, financial statements, revenue, earnings, EPS, margins, assets, liabilities, cash flow, dividends, valuation ratios, and related data.

### Performance Analytics
Absolute and relative returns, time-weighted return, money-weighted return, CAGR, contribution, attribution, and benchmark comparison.

### Risk Analytics
Volatility, covariance, correlation, beta, Sharpe, Sortino, drawdown, VaR, Expected Shortfall, concentration, liquidity, factor exposure, and stress testing.

### Investment Research
Business profile, fundamentals, valuation, competitive position, risks, catalysts, investment thesis, research documents, analyst notes, assumptions, evidence, and invalidation conditions.

A central research relationship is:

**Thesis → Assumptions → Evidence → Monitoring**

### Intelligence & Monitoring
Detect material changes in portfolio exposures, risk, market context, and thesis-relevant evidence. The initial goal is to create investigation opportunities rather than blind buy/sell signals.

### AI
Natural-language interaction, evidence retrieval, tool use, analytical reasoning, research assistance, and explanation over the underlying governed system.

### Governance
Data lineage, calculation lineage, model/version lineage, research provenance, AI traceability, decision history, auditability, and appropriate access controls.

## 8. AI operating principle

AI must sit above governed domain services and deterministic analytics.

For example, when asked:

> Why did my portfolio underperform yesterday?

the system should retrieve the relevant portfolio state, compute authoritative performance and attribution, identify contributors and detractors, retrieve relevant market/contextual evidence, and then allow the AI layer to explain the result.

The AI layer should not invent or independently substitute financial calculations when authoritative services can perform them.

## 9. What InvestAnalytics is not

The initial product is not:

- a stock-price prediction engine;
- an autonomous trading bot;
- a generic financial chatbot;
- a guaranteed-return system;
- a replacement for a portfolio manager;
- an unrestricted autonomous AI agent;
- a generic dashboard project.

## 10. Development model

The project may develop openly and should be architected from the beginning as a potential commercial product.

Potential open-source components include analytical libraries, portfolio calculations, data models, visualization, and documentation.

Potential commercial capabilities include hosted services, advanced data integrations, professional research workflows, enterprise permissions, collaboration, governance, managed infrastructure, and advanced AI capabilities.

## 11. Product quality attributes

The product should progressively demonstrate:

- analytical correctness;
- data quality;
- explainability;
- provenance;
- reproducibility;
- auditability;
- security;
- modularity;
- extensibility;
- operational reliability.

## 12. Strategic milestones

| Milestone | Purpose |
|---|---|
| IA-0 | Foundation |
| IA-1 | Equity Intelligence Core |
| IA-2 | Portfolio Analytics |
| IA-3 | Risk Intelligence |
| IA-4 | Investment Research |
| IA-5 | Monitoring |
| IA-6 | AI Analyst |
| IA-7 | Professional Platform |
| IA-8 | Multi-Asset Expansion |

The milestones are sequencing guidance, not permission to skip required contracts or governance work.
