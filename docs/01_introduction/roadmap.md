# QuantMind Roadmap

## Overview

QuantMind evolves through a sequence of architectural milestones.

Each release adds a new subsystem or expands an existing one while preserving the core Clean Architecture.

The roadmap is designed to evolve QuantMind from a local AI-assisted research workflow into a modular, deployable AI Quant Research Platform.

---

## Architecture Evolution

| Version | Architecture Milestone        | Main Deliverable                                                      |
| ------- | ----------------------------- | --------------------------------------------------------------------- |
| v0.1    | AI Research Pipeline MVP      | Market data, Ollama integration, Markdown research report             |
| v0.2    | Quantitative Indicator Engine | SMA, EMA, RSI, MACD, structured technical analysis                    |
| v0.3    | Forecast Engine with LSTM     | Return-based LSTM forecasting, baseline evaluation, AI interpretation |
| v0.4    | Multi-Model Forecast Engine   | Transformer implementation and model comparison                       |
| v0.5    | Financial Knowledge Engine    | SEC filing retrieval and RAG                                          |
| v0.6    | Multi-Agent Research Engine   | LangGraph workflow and specialized research agents                    |
| v0.7    | Service Platform              | FastAPI backend and interactive dashboard                             |
| v0.8    | Deployment Platform           | Docker, cloud deployment, CI/CD, and monitoring                       |
| v0.9    | Integration Layer             | MCP tools and external research-system integration                    |
| v1.0    | Production QuantMind Platform | Integrated, documented, testable, and deployable research platform    |

---

## Current Release

### v0.3 — Forecast Engine with LSTM

Current capabilities include:

* Yahoo Finance market data
* Technical indicators
* Return-based LSTM forecasting
* Validation RMSE and MAE
* Naive baseline comparison
* Evidence-constrained Ollama reporting
* Clean Architecture
* Structured documentation

---

## Next Release

### v0.4 — Multi-Model Forecast Engine

Planned capabilities:

* Transformer forecasting model
* Shared forecasting interface
* LSTM and Transformer comparison
* Consistent model evaluation
* Model-selection configuration
* Forecasting framework documentation

The objective is not merely to add a Transformer, but to demonstrate that new forecasting models can be introduced without redesigning the research workflow.

---

## Future Subsystems

### Knowledge Engine

Planned for v0.5:

* SEC 10-K retrieval
* SEC 10-Q retrieval
* Financial-document parsing
* Vector storage
* Retrieval-Augmented Generation
* Evidence-grounded fundamental analysis

### Multi-Agent Research Engine

Planned for v0.6:

* Technical Analyst Agent
* Forecast Analyst Agent
* Fundamental Analyst Agent
* Risk Analyst Agent
* Portfolio Analyst Agent
* Chief Investment Officer synthesis
* LangGraph orchestration

### Service Platform

Planned for v0.7:

* FastAPI backend
* REST endpoints
* Research-job execution
* Report retrieval
* Interactive dashboard

### Deployment Platform

Planned for v0.8:

* Docker
* Cloud deployment
* CI/CD
* Automated testing
* Logging
* Monitoring
* Configuration management

### Integration Layer

Planned for v0.9:

* MCP-compatible tools
* External data connectors
* Research workflow interoperability
* Model and tool registry

---

## v1.0 Vision

QuantMind v1.0 will integrate:

```text
Market Data
    +
Indicator Engine
    +
Multi-Model Forecast Engine
    +
Financial Knowledge Engine
    +
Multi-Agent Research Engine
    +
FastAPI Service Platform
    +
Cloud Deployment
```

The long-term objective is to provide a modular AI Quant Research Platform in which data providers, forecasting models, knowledge sources, LLM providers, and research agents can evolve independently through stable interfaces.
