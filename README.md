# QuantMind — AI Quant Research Platform

> **Where Quantitative Finance Meets AI Engineering.**

**QuantMind** is an open-source **Financial AI research platform** combining financial econometrics, quantitative analysis, deep-learning forecasting, retrieval-augmented generation (RAG), multi-agent AI, and AWS cloud engineering in one evidence-grounded equity-research workflow.

The platform uses **LangGraph-based research orchestration**, **PyTorch LSTM and Transformer forecasting**, **SEC 10-K / 10-Q retrieval**, **Amazon Bedrock**, **Titan Text Embeddings V2**, and **Amazon S3 Vectors**, with reusable **CLI, FastAPI, and MCP** interfaces.

QuantMind is designed for **AI-assisted investment research, explainable financial intelligence, and decision support** rather than autonomous trading.

**Core stack:** Python · PyTorch · LangGraph · RAG · MCP · FastAPI · Amazon Bedrock · Titan Embeddings · S3 Vectors · ECS Fargate

**Created by Hsiang-Tai Lee, Ph.D. — AI / Quant Research Systems Developer**

---

## Current Milestone — v0.11 AWS Cloud Deployment

**v0.11 is the current completed platform baseline.**

It integrates the complete QuantMind research workflow with an AWS cloud deployment.

### AI Agents & Research Workflow

- LangGraph-based conditional research workflow
- LLM-driven `ResearchSupervisor`
- Structured `ResearchPlan`
- Technical, forecast, and fundamental specialist agents
- Evidence-grounded synthesis agent
- Controlled sequential multi-agent execution

### SEC RAG & Fundamental Research

- SEC 10-K / 10-Q research
- Amazon Titan Text Embeddings V2
- 1024-dimensional embeddings
- Amazon S3 Vectors semantic retrieval
- Evidence-first fundamental analysis
- Separation of offline ingestion and online research

### Quantitative & ML Research

- SMA, EMA, RSI, and MACD
- PyTorch LSTM forecasting
- PyTorch Transformer forecasting
- Chronological train / validation separation
- Leakage-controlled feature scaling
- RMSE / MAE evaluation
- Zero-return baseline comparison

### AWS Cloud Engineering

- Docker
- Amazon ECR
- Amazon ECS / Fargate
- Application Load Balancer
- VPC public / private subnet architecture
- IAM execution-role / task-role separation
- Amazon CloudWatch logging
- Amazon Bedrock
- Amazon S3 Vectors
- Demo-on-demand operation

---

## Demo

The v0.11 demo accepts a natural-language equity-research question and converts it into a structured research plan.

Example:

```json
{
  "ticker": "AAPL",
  "research_question": "What risks does Apple face from tariffs, international trade restrictions, and supply-chain concentration?"
}
```

For this question, the Research Supervisor selected a fundamental-only workflow:

```json
{
  "use_technical": false,
  "use_forecast": false,
  "use_fundamental": true,
  "filing_types": [
    "10-K",
    "10-Q"
  ]
}
```

The resulting execution path is:

```text
Natural-Language Question
        ↓
Research Supervisor
        ↓
ResearchPlan
        ↓
Fundamental Branch Selected
        ↓
Titan Text Embeddings V2
        ↓
Amazon S3 Vectors
        ↓
Relevant SEC Evidence
        ↓
Fundamental Research Agent
        ↓
Evidence-Grounded Synthesis
        ↓
Research Report
```

> **Live AWS demo available on request.**
>
> The public cloud endpoint is intentionally not kept active continuously. Screenshots and sample outputs are included so the system can be evaluated while the Fargate service is scaled down.

### v0.11 Architecture

![QuantMind v0.11 Architecture](docs/demo/05-v011-architecture.png)

### Public FastAPI Interface

![QuantMind FastAPI](docs/demo/01-fastapi-public-api.png)

### Natural-Language Research Request

![QuantMind Research Request](docs/demo/02a-research-request.png)

### Dynamic Research Routing

![QuantMind Research Routing](docs/demo/02b-research-routing-result.png)

### Evidence-Grounded SEC Research Report

![QuantMind SEC Grounded Report](docs/demo/03-sec-grounded-report.png)

### AWS ECS Deployment

![QuantMind AWS ECS Deployment](docs/demo/04-aws-ecs-deployment.png)

### Sample Artifacts

- [AAPL tariff and supply-chain risk report](docs/demo/aapl-tariff-risk-report.md)
- [Full API response JSON](docs/demo/aapl-tariff-risk-response.json)

### v0.11 Demo-Data Scope

The current AWS SEC corpus is intentionally small and controlled:

```text
AAPL
├── 10-K
└── 10-Q
```

The v0.11 S3 Vectors index contains a filtered set of Apple SEC filing chunks embedded with Titan Text Embeddings V2.

The research architecture itself is ticker-parameterized. Automated ingestion and expansion to additional issuers are planned for a future release.

---

## Architecture

QuantMind follows **Clean Architecture** principles.

```text
Presentation
     ↓
Application
     ↓
Domain

Infrastructure
     ↓
implements application / domain interfaces
```

The core research workflow does not belong to FastAPI, MCP, AWS, or any individual model provider.

```text
CLI
FastAPI
MCP
   ↓
ResearchApplicationService
   ↓
LangGraph Research Workflow
   ↓
ResearchResult
```

### Replaceable Infrastructure Providers

Interfaces and factories allow local and AWS environments to use different implementations without changing the core research workflow.

```text
LLMInterface
├── OllamaProvider
└── BedrockProvider

EmbeddingInterface
├── OllamaEmbeddingModel
└── BedrockEmbeddingModel

VectorStoreInterface
├── ChromaVectorStore
└── S3VectorStore

ForecastModel
├── LSTMModel
└── TransformerModel
```

The design goal is to keep **financial research logic independent from presentation, infrastructure, and deployment technologies**.

---

## Research Workflow

The QuantMind research workflow is **stateful, conditional, multi-agent, and intentionally sequential**.

```text
Natural-Language Research Question
        ↓
ResearchApplicationService
        ↓
ResearchState
        ↓
LangGraph
        ↓
ResearchSupervisor
        ↓
ResearchPlan
        ↓
Conditional Routing
        ↓
Selected Research Branches
        ↓
Technical / Forecast / Fundamental Evidence
        ↓
Specialist Research Agents
        ↓
ResearchContext
        ↓
Synthesis Research Agent
        ↓
ResearchResult
```

Conditional execution determines **which research branches run**.

Sequential execution determines **the order in which selected branches run**.

This keeps state transitions, evidence flow, model execution, and agent behavior easier to inspect, test, and debug.

---

## Research Supervisor

`ResearchSupervisor` converts a natural-language research objective into a structured `ResearchPlan`.

It determines whether a request requires:

```text
Technical analysis
Forecast analysis
Fundamental analysis
SEC 10-K evidence
SEC 10-Q evidence
```

Example:

```python
ResearchPlan(
    use_technical=False,
    use_forecast=False,
    use_fundamental=True,
    filing_types=[
        "10-K",
        "10-Q",
    ],
)
```

The planning architecture separates probabilistic LLM reasoning from deterministic workflow execution:

```text
Natural-Language Question
        ↓
LLM Planning
        ↓
ResearchPlan
        ↓
Deterministic LangGraph Routing
```

The supervisor decides **what research is required**.

The workflow decides **how that plan is executed**.

---

## Multi-Agent Research System

QuantMind uses specialist agents with explicit responsibilities rather than relying on unconstrained agent interaction.

### Technical Research Agent

```text
Market Data
    ↓
IndicatorService
    ↓
SMA / EMA / RSI / MACD
    ↓
Technical Evidence
    ↓
TechnicalResearchAgent
    ↓
Technical Interpretation
```

### Forecast Research Agent

```text
Market Data
    ↓
PredictionService
    ↓
ForecastModel
    ↓
LSTM / Transformer
    ↓
PredictionResult
    ↓
ForecastResearchAgent
    ↓
Forecast Interpretation
```

### Fundamental Research Agent

```text
Research Question
    ↓
EvidenceRetriever
    ↓
Embedding Model
    ↓
Vector Store
    ↓
SEC Evidence
    ↓
FundamentalResearchAgent
    ↓
Fundamental Interpretation
```

### Synthesis Research Agent

```text
Selected Evidence
        +
Specialist Interpretations
        ↓
ResearchContext
        ↓
SynthesisResearchAgent
        ↓
Final Research Report
```

The architecture emphasizes **specialization and evidence flow**, not agent count.

---

## Fundamental Research & RAG

QuantMind includes an evidence-grounded fundamental-research pipeline using SEC filings.

Current supported filing types:

```text
SEC 10-K
SEC 10-Q
```

### AWS v0.11 Retrieval Path

```text
Research Question
        ↓
Titan Text Embeddings V2
        ↓
1024-Dimensional Query Embedding
        ↓
Amazon S3 Vectors
        ↓
Semantic Search
        ↓
Relevant SEC Filing Chunks
        ↓
VectorEvidenceRetriever
        ↓
FundamentalResearchAgent
        ↓
Amazon Nova Lite
        ↓
Evidence-Grounded Interpretation
```

The cloud SEC corpus was embedded using the same Titan embedding configuration used for query-time retrieval.

This keeps document and query vectors in the same embedding space.

### Offline vs. Online Processing

SEC ingestion is separated from normal research execution.

```text
Offline Ingestion

SEC Filing
    ↓
Chunking
    ↓
Embedding
    ↓
Vector Storage
```

```text
Online Research

Research Question
    ↓
Embedding
    ↓
Vector Retrieval
    ↓
Relevant Evidence
    ↓
Fundamental Agent
```

Normal research execution does **not** repeatedly download and re-embed SEC filings.

The design principle is:

> **Retrieve first, interpret second.**

---

## Technical Analysis

QuantMind produces deterministic technical evidence before any LLM interpretation occurs.

Current indicators:

```text
SMA(20)
EMA(20)
RSI(14)
MACD(12, 26, 9)
```

Pipeline:

```text
Market Data
    ↓
Price Series
    ↓
IndicatorService
    ↓
SMA / EMA / RSI / MACD
    ↓
IndicatorResult
    ↓
TechnicalResearchAgent
```

Technical analysis executes only when required by the `ResearchPlan`.

The Technical Research Agent interprets the supplied indicators rather than calculating them itself.

```text
Deterministic Calculation
        ↓
Technical Evidence
        ↓
LLM Interpretation
```

---

## Forecasting

QuantMind includes a PyTorch deep-learning forecasting pipeline for **next-day return prediction**.

Current models:

```text
LSTM
Transformer
```

There is currently no ARIMA model in the active forecasting architecture.

```text
PredictionService
    ↓
ForecastModel Interface
    ↓
ForecastModelFactory
    ↓
LSTMModel / TransformerModel
    ↓
PredictionResult
```

### Feature Engineering

Historical closing prices are converted into daily returns.

```text
return_t = price_t / price_(t-1) - 1
```

The models use the previous **30 daily returns** to predict the next return.

```text
30 Historical Returns
        ↓
Input Sequence
        ↓
LSTM / Transformer
        ↓
Next-Day Return
```

The default split is chronological:

```text
80% Training
20% Validation
```

The `StandardScaler` is fitted using training returns only, reducing validation leakage.

### LSTM

Default configuration:

```text
Sequence Length: 30
Hidden Size:     32
LSTM Layers:      1
Optimizer:       Adam
Learning Rate:   0.001
Epochs:          100
Random Seed:      42
Loss:            MSE
```

### Transformer

Default configuration:

```text
Sequence Length:    30
Model Dimension:    32
Attention Heads:     4
Encoder Layers:      2
Feedforward Size:   64
Dropout:           0.1
Optimizer:         AdamW
Learning Rate:   0.0005
Epochs:            100
Random Seed:        42
Loss:              MSE
```

The Transformer uses sinusoidal positional encoding and gradient clipping.

Both models retain the model state with the lowest validation loss.

### Evaluation

Validation predictions are converted back into actual returns and price forecasts.

Current evaluation includes:

```text
Validation RMSE
Validation MAE
Zero-Return Baseline RMSE
```

The naive baseline assumes:

```text
Predicted Next Price = Current Price
```

equivalent to a predicted next-day return of zero.

This provides a simple reference for determining whether the deep-learning model improves on a naive forecast.

The forecasting pipeline returns a structured `PredictionResult` containing information such as:

```text
current price
predicted price
predicted return
forecast horizon
validation loss
validation RMSE
validation MAE
baseline RMSE
model name
```

The quantitative model produces the forecast evidence; the Forecast Research Agent interprets it afterward.

---

## Evidence-Grounded Synthesis

QuantMind distinguishes source evidence from LLM interpretation.

```text
Structured / Retrieved Evidence
            +
Specialist Interpretations
            ↓
ResearchContext
            ↓
SynthesisResearchAgent
            ↓
Final Research Report
```

Examples:

```text
Technical branch
Indicators → Technical Interpretation

Forecast branch
PredictionResult → Forecast Interpretation

Fundamental branch
SEC Evidence → Fundamental Interpretation
```

Only branches selected by the `ResearchPlan` contribute evidence to the synthesis stage.

The synthesis agent is intended to answer:

> **What conclusion is supported by the research evidence already produced?**

rather than create an independent body of unsupported facts.

LLM outputs remain probabilistic and should be independently verified.

---

## Application Interfaces

QuantMind exposes the same research system through three presentation interfaces.

```text
Human / Developer        Software Client        AI Host
      ↓                        ↓                   ↓
     CLI                    FastAPI              MCP
       \                      |                  /
        ───── ResearchApplicationService ──────
                         ↓
               Shared Research Workflow
```

### CLI

```text
main.py
    ↓
ResearchApplicationService
    ↓
ResearchResult
    ↓
Console
```

Useful for development, debugging, and direct local execution.

### FastAPI

```text
HTTP Client
    ↓
FastAPI
    ↓
ResearchApplicationService
    ↓
ResearchResult
    ↓
ResearchResponse
    ↓
HTTP / JSON
```

Health check:

```http
GET /health
```

Example:

```json
{
  "status": "ok",
  "service": "QuantMind"
}
```

Research request:

```http
POST /research
```

Example:

```json
{
  "ticker": "AAPL",
  "research_question": "What risks does Apple face from tariffs, international trade restrictions, and supply-chain concentration?"
}
```

FastAPI exposes stable public schemas rather than internal LangGraph state.

### MCP

QuantMind also exposes the research engine through a local **Model Context Protocol** server.

```text
AI Host / LLM
    ↓
MCP Client
    ↓
QuantMind MCP Server
    ↓
research_equity
    ↓
ResearchApplicationService
    ↓
Shared Research Workflow
```

Primary tool:

```text
research_equity(
    ticker: str,
    research_question: str
)
```

The current MCP implementation uses **stdio transport**.

MCP remains a thin presentation adapter and does not contain independent research logic.

---

## Application Contracts & State

QuantMind separates internal workflow state, synthesis context, application output, and public interface contracts.

```text
ResearchState
= complete internal workflow execution state

ResearchContext
= curated evidence and specialist interpretations
  required for synthesis

ResearchResult
= stable application-level result

ResearchResponse
= FastAPI / HTTP representation

ResearchToolResult
= MCP representation
```

### ResearchApplicationService

`ResearchApplicationService` is the stable application-level entry point shared by CLI, FastAPI, and MCP.

```text
Presentation Adapter
    ↓
ResearchApplicationService
    ↓
Initial ResearchState
    ↓
LangGraph
    ↓
Completed ResearchState
    ↓
ResearchResult
```

Presentation code therefore does not depend directly on LangGraph internals.

### ResearchState

`ResearchState` carries information through workflow execution.

```text
ResearchState
├── ticker
├── research_question
├── research_plan
├── history
├── current_price
├── indicators
├── prediction
├── retrieval
├── technical_agent_result
├── forecast_agent_result
├── fundamental_agent_result
└── report
```

Not every field is populated for every request.

State population depends on the selected `ResearchPlan`.

### ResearchContext

The complete workflow state is not passed directly to synthesis.

Instead:

```text
Completed ResearchState
        ↓
Select Relevant Evidence
        +
Select Specialist Results
        ↓
ResearchContext
        ↓
SynthesisResearchAgent
```

The distinction is:

```text
ResearchState
= everything the workflow needs to execute

ResearchContext
= everything the synthesis agent needs to reason
```

### Public Models

The application-level result is converted into presentation-specific models:

```text
ResearchResult
├── CLI output
├── ResearchResponse
└── ResearchToolResult
```

This allows internal workflow structures to evolve without exposing them directly to external clients.

---

## AWS v0.11 Deployment

The verified AWS request path is:

```text
Internet
    ↓
Application Load Balancer
    ↓
Amazon ECS / Fargate
    ↓
FastAPI
    ↓
ResearchApplicationService
    ↓
LangGraph Research Workflow
    ↓
Research Agents
    ↓
Amazon Bedrock + Amazon S3 Vectors
    ↓
Research Report
```

### Container Deployment

```text
Docker Image
    ↓
Amazon ECR
    ↓
ECS Task Definition
    ↓
Amazon ECS / Fargate
```

### Network Architecture

```text
VPC
├── Public Subnets
│   └── Application Load Balancer
│
└── Private Subnets
    └── ECS / Fargate
```

The Application Load Balancer is internet-facing.

The Fargate application task runs in private subnets and receives application traffic through the load balancer.

### IAM Separation

```text
ecsTaskExecutionRole
    ↓
ECR image pull
CloudWatch log delivery
task startup infrastructure


quantmind-task-role
    ↓
application runtime permissions
Bedrock inference
S3 Vectors retrieval
```

Application code does not contain long-lived AWS credentials.

On Fargate, `boto3` obtains temporary credentials through the ECS Task Role.

### Managed AI Services

```text
Amazon Bedrock
├── Amazon Nova Lite
└── Titan Text Embeddings V2

Amazon S3 Vectors
└── SEC vector retrieval
```

### Observability

```text
QuantMind
    ↓
ECS awslogs Driver
    ↓
Amazon CloudWatch Logs
    ↓
/ecs/quantmind
```

### v0.11 Release Verification

The deployed runtime was validated through the public path:

```text
GET /health        → HTTP 200
POST /research     → HTTP 200
ALB target health  → healthy
CloudWatch logs    → checked for runtime errors
```

This tests more than container startup: it exercises the deployed research workflow through the AWS application path.

---

## Demo-on-Demand Operation

The AWS environment is intentionally operated as an **on-demand demo deployment**.

```text
Demo Required
    ↓
ECS desired count = 1
    ↓
Fargate task starts
    ↓
ALB routes traffic
    ↓
Live QuantMind Demo
    ↓
Demo Complete
    ↓
ECS desired count = 0
```

Start the service:

```powershell
aws ecs update-service `
    --cluster quantmind-cluster `
    --service quantmind-service `
    --desired-count 1 `
    --profile quantmind `
    --region us-east-2 `
    --no-cli-pager
```

Wait until stable:

```powershell
aws ecs wait services-stable `
    --cluster quantmind-cluster `
    --services quantmind-service `
    --profile quantmind `
    --region us-east-2
```

Scale back to zero:

```powershell
aws ecs update-service `
    --cluster quantmind-cluster `
    --service quantmind-service `
    --desired-count 0 `
    --profile quantmind `
    --region us-east-2 `
    --no-cli-pager
```

Scaling ECS to zero stops the Fargate application task, but persistent infrastructure such as the ALB, NAT Gateway, ECR, S3 Vectors, VPC resources, IAM roles, and CloudWatch resources may remain provisioned and may continue to incur cost.

The goal is **cost-aware demo operation**, not zero-cost infrastructure.

---

## Configuration & Bootstrap

Runtime configuration and dependency assembly are kept outside the core research logic.

Concrete dependencies are assembled in:

```text
app/bootstrap/research_factory.py
```

Runtime configuration is centralized in:

```text
app/config/settings.py
```

Conceptually:

```text
Configuration
    ↓
Provider Selection
    ↓
Concrete Dependencies
    ↓
Application Services
    ↓
ResearchApplicationService
```

The composition root determines **which concrete providers the runtime uses**.

The application layer determines **what research the system performs**.

This keeps local and AWS runtime choices separate from research behavior.

---

## Project Structure

```text
ai-quant-research-platform/
├── app/
│   ├── application/
│   │   ├── agents/
│   │   ├── embeddings/
│   │   ├── llm/
│   │   ├── prompts/
│   │   ├── retrieval/
│   │   ├── services/
│   │   ├── vectorstores/
│   │   └── workflow/
│   ├── bootstrap/
│   ├── config/
│   ├── domain/
│   │   ├── entities/
│   │   ├── forecast/
│   │   ├── indicators/
│   │   └── repositories/
│   ├── infrastructure/
│   │   ├── embeddings/
│   │   ├── llm/
│   │   ├── market_data/
│   │   ├── ml/
│   │   ├── rag/
│   │   └── vectorstores/
│   └── presentation/
│       ├── api/
│       └── mcp/
├── docs/
│   └── demo/
├── scripts/
├── tests/
├── main.py
├── Dockerfile
├── requirements.txt
├── requirements-docker.txt
└── README.md
```

Layer responsibilities:

```text
Domain
= core entities and abstractions

Application
= research use cases, agents, services, and orchestration

Infrastructure
= concrete LLM, embedding, vector, ML, and data providers

Presentation
= CLI, FastAPI, and MCP interfaces

Bootstrap
= dependency composition

Config
= runtime configuration
```

---

## Running QuantMind Locally

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

### CLI

```powershell
python main.py
```

### FastAPI

```powershell
python -m uvicorn app.presentation.api.app:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

### MCP

```powershell
python -m app.presentation.mcp.server
```

The current MCP server uses stdio transport.

All three entry points use the same `ResearchApplicationService`.

---

## Testing

QuantMind uses multiple levels of verification:

```text
Automated Tests
      +
Manual Real-System Checks
      +
AWS End-to-End Verification
```

### Automated Tests

Automated regression tests live under:

```text
tests/
```

Run:

```powershell
python -m pytest tests -v
```

Current automated coverage includes:

```text
FastAPI
MCP
MCP stdio transport
runtime configuration
```

### Manual Regression

Real-provider checks live under:

```text
scripts/manual_regression/
```

Current checks include:

```text
Research Supervisor
Technical Research Agent
Forecast Research Agent
Fundamental Research Agent
SEC 10-Q retrieval
```

### Cloud Verification

v0.11 was also verified through the deployed runtime:

```text
Docker
    ↓
Amazon ECR
    ↓
Amazon ECS / Fargate
    ↓
Application Load Balancer
    ↓
FastAPI
    ↓
LangGraph
    ↓
Amazon Bedrock
    ↓
Titan Text Embeddings V2
    ↓
Amazon S3 Vectors
    ↓
SEC Evidence
    ↓
Research Output
```

The layered testing strategy separates fast automated regression from real-provider and full-cloud verification.

---

## Design Principles

QuantMind follows these architectural principles:

- **Clean Architecture** — presentation, application, domain, and infrastructure responsibilities remain separated.
- **Single application boundary** — CLI, FastAPI, and MCP reuse `ResearchApplicationService`.
- **Evidence before interpretation** — deterministic computation and retrieval produce evidence before LLM reasoning.
- **Typed state and contracts** — workflow state, synthesis context, application results, and public models have distinct responsibilities.
- **Conditional orchestration** — only research branches required by the `ResearchPlan` execute.
- **Controlled multi-agent execution** — specialized agents operate within an explicit LangGraph workflow.
- **Replaceable infrastructure** — LLMs, embeddings, vector stores, forecasting models, and market-data providers remain swappable.
- **Offline / online separation** — document ingestion is separated from normal research execution.
- **Explainable research** — interpretations are grounded in observable quantitative or documentary evidence.
- **Multi-interface reuse** — one research system serves humans, software clients, and AI hosts.
- **Cloud credential isolation** — AWS authorization uses IAM roles rather than credentials stored in source code.
- **Cost-aware operation** — cloud compute can be scaled down when the demo is not required.

---

## Roadmap

### Completed

```text
v0.1   Initial AI market-research MVP
v0.2   Technical indicators
v0.3   Forecasting foundation
v0.4   PyTorch deep-learning forecasting
v0.5   SEC filings + RAG
v0.6   LangGraph research workflow
v0.7   Agentic research planning
v0.8   Multi-agent research system
v0.9   FastAPI interface
v0.10  MCP integration
v0.11  AWS deployment + Bedrock + S3 Vectors
```

### v0.12 — ML Engineering & MLOps

Planned areas:

- Amazon SageMaker training and deployment workflows
- model lifecycle and registry
- CI/CD and automated evaluation
- monitoring and drift detection
- retraining workflows
- automated SEC ingestion
- multi-company SEC expansion
- infrastructure and cost optimization

### v0.13 — Research Data & AI Evaluation

Planned areas:

- earnings-call ingestion
- financial-news ingestion
- grounding evaluation
- AI-output evaluation
- evidence provenance

### v0.14 — Portfolio Intelligence

Planned areas:

- multi-company comparison
- portfolio analytics
- portfolio-level risk
- web research dashboard

### v1.0

Long-term goal:

```text
Financial Econometrics
        +
Machine Learning
        +
Retrieval-Augmented Generation
        +
Agentic AI
        +
Cloud / MLOps Engineering
        ↓
Production-Oriented Financial AI Research Platform
```

Future roadmap items are planned extensions and are not part of the current v0.11 implementation.

---

## Technology Stack

### Quantitative & Machine Learning

```text
Python
pandas
NumPy
scikit-learn
PyTorch
LSTM
Transformer
```

### Agentic AI

```text
LangGraph
Multi-Agent Research
Amazon Bedrock
Amazon Nova Lite
Ollama
```

### RAG & Data

```text
Amazon Titan Text Embeddings V2
Amazon S3 Vectors
ChromaDB
SEC EDGAR
Yahoo Finance
```

### Application Interfaces

```text
FastAPI
Uvicorn
Pydantic
Model Context Protocol (MCP)
CLI
```

### AWS & Infrastructure

```text
Docker
Amazon ECR
Amazon ECS / Fargate
Application Load Balancer
Amazon VPC
AWS IAM
Amazon CloudWatch
```

### Testing

```text
pytest
Manual Regression Scripts
AWS End-to-End Verification
```

---

## Project Goal

QuantMind is intended to demonstrate how **financial econometrics, quantitative analysis, machine learning, RAG, multi-agent AI, application engineering, and cloud infrastructure** can be integrated into one coherent Financial AI research system.

The goal is not to automate trading decisions.

The platform currently supports research workflows involving:

```text
Equity Research
Quantitative Analysis
Technical Analysis
Deep-Learning Forecasting
Fundamental Research
SEC Filing Analysis
AI-Assisted Investment Decision Support
External AI Agent Integration
```

The research philosophy is:

```text
Data
    ↓
Quantitative / Retrieval Systems
    ↓
Structured Evidence
    ↓
Specialized AI Reasoning
    ↓
Research Synthesis
    ↓
Human Decision
```

AI is intended to complement quantitative and documentary evidence rather than replace it.

---

## Disclaimer

QuantMind is an educational and research project.

It does not provide investment advice, brokerage services, or autonomous trading recommendations.

Financial forecasts, retrieved evidence, LLM outputs, and research conclusions should be independently verified before use in real-world investment decisions.
