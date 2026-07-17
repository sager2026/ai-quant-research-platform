# QuantMind

## Where Quantitative Finance Meets AI Engineering

QuantMind is an open-source **AI Quant Research Platform** that combines quantitative finance, financial econometrics, deep learning, and modern AI engineering into a scalable investment research system.

Designed with **Clean Architecture**, QuantMind demonstrates how modern AI engineering can be combined with quantitative finance to produce explainable, institutional-grade investment research.

---

# Technology Stack

## Current

- Python
- Ollama
- Clean Architecture

## Planned

- FastAPI
- LangGraph
- Deep Learning
- RAG
- MCP

---

# Mission

QuantMind bridges quantitative finance and modern AI engineering through an open-source platform for AI-assisted investment research.

The platform combines:

- Market data
- Financial statements
- Macroeconomic information
- Technical indicators
- Deep learning models
- LLM-based reasoning

to support:

- AI-assisted equity research
- Portfolio analysis
- Investment decision support
- Explainable financial intelligence

Rather than focusing on algorithmic trading, QuantMind emphasizes transparent research, predictive analytics, and scalable software engineering.

---

# Architecture

```text
                    User
                     │
                     ▼
              Presentation
                     │
                     ▼
              Application
               /        \
              ▼          ▼
        Domain      Infrastructure
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
     Yahoo Finance    Ollama       SQLite / RAG
                      LLM