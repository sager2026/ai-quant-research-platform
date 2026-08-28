from app.application.agents.fundamental_research_agent import (
    FundamentalResearchAgent,
)
from app.infrastructure.llm.ollama_provider import (
    OllamaProvider,
)
from app.infrastructure.rag.chroma_vector_store import (
    ChromaVectorStore,
)
from app.infrastructure.rag.ollama_embedding_model import (
    OllamaEmbeddingModel,
)
from app.infrastructure.rag.vector_evidence_retriever import (
    VectorEvidenceRetriever,
)

from knowledge_setup import prepare_knowledge


TICKER = "AAPL"

RESEARCH_QUESTION = (
    "What are Apple's recent business risks?"
)

FILING_TYPES = [
    "10-Q",
]


def main() -> None:

    # ---------------------------------------------------------
    # 1. Prepare SEC knowledge
    # ---------------------------------------------------------

    for filing_type in FILING_TYPES:

        prepare_knowledge(
            ticker=TICKER,
            filing_type=filing_type,
        )

    # ---------------------------------------------------------
    # 2. Create retrieval dependencies
    # ---------------------------------------------------------

    embedding_model = OllamaEmbeddingModel(
        model="embeddinggemma"
    )

    vector_store = ChromaVectorStore(
        path="data/chroma",
        collection_name="quantmind_filings",
    )

    evidence_retriever = VectorEvidenceRetriever(
        embedding_model=embedding_model,
        vector_store=vector_store,
        top_k=5,
    )

    # ---------------------------------------------------------
    # 3. Retrieve controlled SEC evidence
    # ---------------------------------------------------------

    retrieval = evidence_retriever.retrieve(
        ticker=TICKER,
        query=RESEARCH_QUESTION,
        filing_types=FILING_TYPES,
    )

    # ---------------------------------------------------------
    # 4. Create LLM
    # ---------------------------------------------------------

    llm = OllamaProvider(
        model="qwen3:8b"
    )

    # ---------------------------------------------------------
    # 5. Create Fundamental Research Agent
    # ---------------------------------------------------------

    fundamental_agent = FundamentalResearchAgent(
        llm=llm,
    )

    # ---------------------------------------------------------
    # 6. Interpret retrieved evidence
    # ---------------------------------------------------------

    result = fundamental_agent.analyze(
        ticker=TICKER,
        research_question=RESEARCH_QUESTION,
        retrieval=retrieval,
    )

    # ---------------------------------------------------------
    # 7. Display retrieved evidence
    # ---------------------------------------------------------

    print()
    print("FUNDAMENTAL RESEARCH AGENT")
    print("=" * 70)

    print(
        f"Ticker: {TICKER}"
    )

    print(
        f"Research question: {RESEARCH_QUESTION}"
    )

    print(
        f"Filing types: {FILING_TYPES}"
    )

    print()

    print("Retrieved SEC Evidence")
    print("-" * 70)

    for index, evidence in enumerate(
        retrieval.evidence,
        start=1,
    ):

        print()
        print(
            f"Evidence #{index}"
        )

        print(
            f"Filing type: {evidence.filing_type}"
        )

        print(
            f"Filing date: {evidence.filing_date}"
        )

        print(
            f"Relevance: {evidence.relevance_score:.4f}"
        )

        print(
            f"Source: {evidence.source}"
        )

    # ---------------------------------------------------------
    # 8. Display agent interpretation
    # ---------------------------------------------------------

    print()
    print("Agent Interpretation")
    print("-" * 70)

    print(
        f"Summary: {result.summary}"
    )

    print()
    print("Observations:")

    for observation in result.observations:
        print(
            f"- {observation}"
        )

    print()
    print("Risks / Limitations:")

    for risk in result.risks:
        print(
            f"- {risk}"
        )

    print()
    print(
        "Evidence references: "
        f"{result.evidence_references}"
    )


if __name__ == "__main__":
    main()