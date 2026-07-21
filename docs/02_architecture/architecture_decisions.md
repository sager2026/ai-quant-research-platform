# Architecture Decision Records (ADR)

This document records the major architectural decisions made during the development of QuantMind.

The purpose is not only to document **what** was implemented, but also **why** each decision was made.

Future contributors should understand the reasoning behind the architecture before modifying the system.

---

# ADR-001

## Use Clean Architecture

### Status

Accepted

### Decision

Organize QuantMind using Clean Architecture.

```
Presentation

↓

Application

↓

Domain

↑

Infrastructure
```

### Motivation

QuantMind integrates multiple technologies including

- Yahoo Finance
- PyTorch
- Ollama
- LangGraph (future)
- FastAPI (future)

These technologies are expected to evolve.

Business logic should remain independent of implementation details.

### Consequences

Benefits

- easier maintenance
- replaceable implementations
- lower coupling
- easier testing

Trade-offs

- additional abstraction
- more interfaces
- more files

---

# ADR-002

## Forecast Returns Instead of Prices

### Status

Accepted

### Decision

Forecast next-period returns rather than directly forecasting price levels.

### Motivation

Financial price series are generally nonstationary.

Return series are typically closer to stationary processes and are more appropriate forecasting targets in financial econometrics.

The platform derives an implied future price for presentation purposes.

### Alternatives Considered

Forecast future prices directly.

### Why Rejected

Price forecasting is common in deep learning literature but can produce misleading evaluation results because persistence alone often achieves low prediction error.

Forecasting returns aligns better with investment decision making.

### Consequences

Benefits

- stronger econometric foundation
- easier comparison with quantitative models
- better interpretation of forecast quality

Trade-offs

- requires converting returns into implied prices for reports

---

# ADR-003

## Separate Indicators from Forecasting Models

### Status

Accepted

### Decision

Technical indicators and forecasting models are implemented as separate subsystems.

```
IndicatorService

ForecastService
```

### Motivation

Indicators are deterministic calculations.

Forecasting models are statistical estimators.

They represent fundamentally different kinds of computation.

### Consequences

Benefits

- clear separation of responsibilities
- easier extension
- independent testing

---

# ADR-004

## LLMs Explain Rather Than Forecast

### Status

Accepted

### Decision

LLMs interpret quantitative evidence.

LLMs never calculate indicators or generate forecasts.

### Motivation

Numerical computation should remain deterministic and reproducible.

Language models are optimized for reasoning and communication rather than numerical estimation.

### Consequences

Benefits

- reproducible calculations
- explainable reports
- reduced hallucination risk

---

# ADR-005

## Require Baseline Comparison

### Status

Accepted

### Decision

Every forecasting model must be evaluated against an appropriate baseline.

Current implementation

```
Naive Zero-Return Forecast
```

### Motivation

Producing predictions alone does not demonstrate predictive value.

Forecast quality must be measured relative to a benchmark.

### Consequences

Benefits

- prevents misleading performance claims
- encourages rigorous evaluation
- aligns with quantitative research practice

---

# ADR-006

## Use Interfaces for Replaceable Components

### Status

Accepted

### Decision

External implementations communicate through interfaces.

Examples

```
PriceRepository

LLMInterface

MLModel
```

### Motivation

Application logic should not depend on concrete implementations.

### Consequences

The following replacements require no changes to ResearchService.

```
Yahoo Finance

↓

Polygon

↓

Bloomberg
```

```
Ollama

↓

OpenAI

↓

Claude
```

```
LSTM

↓

Transformer

↓

XGBoost
```

---

# ADR-007

## QuantMind Three-Engine Architecture

### Status

Accepted

### Decision

QuantMind separates the platform into three independent computational engines.

```
Deterministic Mathematics
        │
        ▼
Statistical Forecasting
        │
        ▼
AI Reasoning
```

### Motivation

Different computational paradigms should remain independent.

Each engine has one responsibility.

### Consequences

Future algorithms can evolve independently without affecting the rest of the platform.

This decision defines the long-term architectural philosophy of QuantMind.