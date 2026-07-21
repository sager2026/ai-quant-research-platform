# Clean Architecture in QuantMind

---

# What is Clean Architecture?

Clean Architecture is a software design philosophy that organizes a system around its business rules rather than around frameworks or technologies.

Its primary goal is to ensure that the core business logic remains independent of external implementation details such as databases, APIs, machine learning frameworks, and user interfaces.

As technologies evolve, the business rules should remain stable.

---

# The Dependency Rule

The most important principle of Clean Architecture is:

> **Source code dependencies always point toward the business rules.**

Business logic never depends on implementation details.

In QuantMind, the Application and Domain layers never directly depend on Yahoo Finance, PyTorch, Ollama, or future technologies.

Instead, those technologies implement interfaces defined by the core system.

---

# Architectural Layers

## Presentation Layer

Responsible for user interaction.

Current implementation:

* `main.py`

Future implementations:

* FastAPI
* Web Dashboard
* REST API
* CLI

---

## Application Layer

Coordinates the research workflow.

Examples:

* `ResearchService`
* `IndicatorService`
* `PredictionService`
* `EquityPrompt`

The Application Layer defines **what the system does**, but not **how it is implemented**.

---

## Domain Layer

Contains the core business concepts of QuantMind.

Examples:

* `ResearchContext`
* `IndicatorResult`
* `PredictionResult`
* `PriceRepository`
* `MLModel`

The Domain Layer contains no framework-specific code.

---

## Infrastructure Layer

Implements the interfaces defined by the Domain.

Examples:

* `YahooRepository`
* `LSTMModel`
* `OllamaProvider`

Infrastructure components can be replaced without changing the business logic.

---

# Why QuantMind Uses Clean Architecture

QuantMind integrates multiple technologies including:

* Yahoo Finance
* PyTorch
* Ollama
* GitHub
* Future cloud services

These technologies will evolve over time.

However, the core concepts of quantitative research remain the same:

* Market Data
* Technical Indicators
* Forecasting
* Research
* Reporting

Clean Architecture isolates technological change from these business concepts.

---

# Benefits

## Maintainability

Business logic remains stable as technologies evolve.

---

## Replaceability

Components can be replaced independently.

Examples:

* Yahoo Finance → Polygon
* LSTM → Transformer
* Ollama → OpenAI

without redesigning the application workflow.

---

## Testability

Each layer can be tested independently.

Business logic can be validated without relying on external services.

---

## Scalability

New forecasting models, data providers, AI models, and research components can be added with minimal impact on the existing system.

---

# QuantMind Architectural Extension

QuantMind extends traditional Clean Architecture by separating three independent computational engines.

```text
Deterministic Mathematics
        │
        ▼
Statistical Forecasting
        │
        ▼
AI Reasoning
```

Each engine has a single responsibility:

* Deterministic mathematics computes indicators.
* Statistical forecasting predicts expected returns.
* AI reasoning explains quantitative evidence.

These engines communicate through a shared domain model (`ResearchContext`) while remaining loosely coupled.

---

# Summary

Clean Architecture enables QuantMind to evolve from a simple AI research prototype into a scalable AI Quant Research Platform.

By separating business concepts from implementation details, the platform can continuously incorporate new forecasting models, AI technologies, and research capabilities without redesigning its core architecture.
