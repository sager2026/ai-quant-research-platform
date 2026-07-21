# QuantMind

### Where Quantitative Finance Meets AI Engineering

An open-source **AI Quant Research Platform** that integrates **Financial Econometrics**, **Machine Learning**, **Large Language Models (LLMs)**, and **Clean Architecture** into a unified institutional-style investment research workflow.

QuantMind demonstrates how deterministic quantitative analysis, statistical forecasting, and AI reasoning can cooperate within a scalable software architecture to produce explainable investment research.

---

## Architecture

![QuantMind Architecture](docs/images/architecture_v0.3.png)


# Core Capabilities

| Capability                    | Status |
| ----------------------------- | :----: |
| Yahoo Finance Integration     |    ✅   |
| Technical Indicators          |    ✅   |
| Return-Based LSTM Forecasting |    ✅   |
| Feature Engineering           |    ✅   |
| Baseline Evaluation           |    ✅   |
| AI Research Report Generation |    ✅   |
| Clean Architecture            |    ✅   |
| Transformer Forecasting       |   🚧   |
| Financial RAG                 |   🚧   |
| Multi-Agent Research          |   🚧   |
| FastAPI Dashboard             |   🚧   |
| Cloud Deployment              |   🚧   |

---

# Design Philosophy

QuantMind is built upon one simple architectural principle:

> **Separate deterministic computation, statistical forecasting, and AI reasoning into independent, replaceable components.**

```text
Deterministic Mathematics
        │
        ▼
Statistical Forecasting
        │
        ▼
AI Reasoning
```

### Deterministic Mathematics

Technical indicators are computed directly from market data.

Examples

* SMA
* EMA
* RSI
* MACD

These calculations are deterministic and reproducible.

---

### Statistical Forecasting

Machine learning models forecast **expected returns**, not price levels.

The current implementation uses:

* Return-based LSTM

Future implementations include:

* Transformer
* XGBoost
* ARIMA
* Temporal Fusion Transformer (TFT)
* Informer

Forecasted returns are converted into **implied prices** for human interpretation.

---

### AI Reasoning

Large Language Models explain quantitative evidence.

LLMs **do not**

* calculate indicators
* train forecasting models
* estimate returns

Instead they synthesize structured quantitative evidence into professional research reports.

---

# System Workflow

```text
Yahoo Finance
        │
        ▼
Historical Market Data
        │
        ▼
Technical Indicators
        │
        ▼
Return-Based LSTM Forecast
        │
        ▼
Model Evaluation
        │
        ▼
ResearchContext
        │
        ▼
Evidence-Constrained Prompt
        │
        ▼
Ollama
        │
        ▼
Markdown Research Report
```

---

# Technology Stack

| Layer                 | Technology         |
| --------------------- | ------------------ |
| Programming Language  | Python             |
| Deep Learning         | PyTorch            |
| Market Data           | Yahoo Finance      |
| Data Analysis         | Pandas             |
| LLM                   | Ollama + Qwen3     |
| Software Architecture | Clean Architecture |
| Version Control       | Git & GitHub       |

---

# Project Structure

```text
ai-quant-research-platform
│
├── app
│   ├── application
│   ├── domain
│   ├── infrastructure
│   └── presentation
│
├── docs
│
├── reports
│
├── main.py
├── requirements.txt
└── README.md
```

---

# Current Status

| Item               | Status                     |
| ------------------ | -------------------------- |
| Current Version    | **v0.3**                   |
| Architecture       | **Forecast Engine (LSTM)** |
| Development Status | Active                     |
| License            | MIT                        |

---

# Architecture Evolution

| Version | Architecture Milestone                |
| ------- | ------------------------------------- |
| v0.1    | AI Research Pipeline MVP              |
| v0.2    | Quantitative Indicator Engine         |
| v0.3    | Forecast Engine (LSTM)                |
| v0.4    | Forecast Engine (Transformer)         |
| v0.5    | Knowledge Engine (RAG)                |
| v0.6    | Multi-Agent Research Engine           |
| v0.7    | FastAPI Service Platform              |
| v0.8    | Cloud Deployment                      |
| v1.0    | Production AI Quant Research Platform |

---

# Documentation

Project documentation is located in the **docs/** directory.

Current documentation includes:

* Project Overview
* Design Philosophy
* Clean Architecture
* Architecture v0.3
* Architecture Decision Records (ADR)
* Release Notes

---

# Quick Start

Clone the repository

```bash
git clone https://github.com/sager2026/ai-quant-research-platform.git
```

Enter the project

```bash
cd ai-quant-research-platform
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run QuantMind

```bash
python main.py
```

---

# Example Output

QuantMind automatically generates a Markdown equity research report including:

* Technical indicator analysis
* Return-based LSTM forecast
* Forecast evaluation
* Baseline comparison
* AI-generated research summary
* Overall investment outlook

---

# Why QuantMind?

Many AI finance projects focus on either:

* machine learning models,

or

* large language models.

QuantMind integrates:

* deterministic quantitative analysis,
* statistical forecasting,
* and AI reasoning

within a single scalable Clean Architecture.

The objective is not merely to predict financial markets, but to demonstrate how modern AI systems can support **explainable quantitative research**.

---

# Roadmap

## Forecast Engine

* Transformer
* XGBoost
* ARIMA
* Temporal Fusion Transformer
* Informer

## Knowledge Engine

* SEC 10-K Analysis
* SEC 10-Q Analysis
* Financial News
* Retrieval-Augmented Generation (RAG)

## Research Engine

* Multi-Agent Workflow
* LangGraph
* Portfolio Analyst
* Risk Analyst
* Fundamental Analyst

## Platform

* FastAPI
* Interactive Dashboard
* Docker
* Cloud Deployment
* CI/CD
* Monitoring

---

# License

This project is licensed under the MIT License.

---

# Acknowledgements

QuantMind is an educational and research-oriented project exploring the intersection of:

* Financial Econometrics
* Machine Learning
* Artificial Intelligence
* Modern Software Engineering

The project demonstrates how scalable, explainable AI systems can be engineered for quantitative investment research using Clean Architecture.
