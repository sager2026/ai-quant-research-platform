# QuantMind Dependency Flow

> **Status:** Initial overview for v0.3.
> A more detailed dependency map will be completed in v0.4 when the Forecast Engine supports both LSTM and Transformer implementations.

## Dependency Rule

QuantMind follows the Clean Architecture dependency rule:

> Source-code dependencies point toward the core business rules.

```text
Presentation
      ↓
Application
      ↓
Domain
      ↑
Infrastructure
```

The Domain Layer does not depend on:

* Yahoo Finance
* PyTorch
* Ollama
* FastAPI
* databases
* cloud services

Infrastructure implementations depend on interfaces defined by the core layers.

## Current Dependency Examples

```text
YahooRepository
        implements
PriceRepository
```

```text
LSTMModel
        implements
MLModel
```

```text
OllamaProvider
        implements
LLMInterface
```

`ResearchService` coordinates these components through injected dependencies rather than constructing infrastructure implementations internally.

A complete file-level dependency diagram will be added when the multi-model Forecast Engine is completed in v0.4.
