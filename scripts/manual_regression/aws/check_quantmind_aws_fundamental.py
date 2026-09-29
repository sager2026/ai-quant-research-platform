import os
import json
from dataclasses import asdict, is_dataclass


# ============================================================
# Local test environment
# ============================================================

os.environ["AWS_PROFILE"] = "quantmind"

os.environ["QUANTMIND_LLM_PROVIDER"] = "bedrock"
os.environ["QUANTMIND_BEDROCK_MODEL_ID"] = "us.amazon.nova-lite-v1:0"
os.environ["QUANTMIND_BEDROCK_REGION"] = "us-east-2"

os.environ["QUANTMIND_EMBEDDING_PROVIDER"] = "bedrock"
os.environ["QUANTMIND_BEDROCK_EMBEDDING_MODEL_ID"] = (
    "amazon.titan-embed-text-v2:0"
)
os.environ["QUANTMIND_BEDROCK_EMBEDDING_REGION"] = "us-east-2"
os.environ["QUANTMIND_BEDROCK_EMBEDDING_DIMENSIONS"] = "1024"

os.environ["QUANTMIND_VECTOR_STORE_PROVIDER"] = "s3vectors"
os.environ["QUANTMIND_S3_VECTOR_BUCKET_NAME"] = "quantmind-sec-vectors"
os.environ["QUANTMIND_S3_VECTOR_INDEX_NAME"] = (
    "sec-filings-titan-v2-1024"
)
os.environ["QUANTMIND_S3_VECTOR_REGION"] = "us-east-2"

os.environ["QUANTMIND_RETRIEVAL_TOP_K"] = "5"


# ============================================================
# QuantMind production imports
# ============================================================

from app.config.settings import Settings

from app.bootstrap.embedding_factory import (
    create_embedding_model,
)

from app.bootstrap.vector_store_factory import (
    create_vector_store,
)

from app.bootstrap.llm_factory import (
    create_llm,
)

from app.infrastructure.rag.vector_evidence_retriever import (
    VectorEvidenceRetriever,
)

from app.application.agents.fundamental_research_agent import (
    FundamentalResearchAgent,
)


QUERY = (
    "What risks does Apple face from tariffs, "
    "international trade restrictions, and "
    "supply-chain concentration?"
)

TICKER = "AAPL"

FILING_TYPES = [
    "10-K",
    "10-Q",
]


def serialize(value):

    if is_dataclass(value):
        return asdict(value)

    if hasattr(value, "model_dump"):
        return value.model_dump()

    if hasattr(value, "dict"):
        return value.dict()

    if hasattr(value, "__dict__"):
        return value.__dict__

    return str(value)


def main():

    print("=" * 80)
    print("QUANTMIND AWS FUNDAMENTAL INTEGRATION TEST")
    print("=" * 80)

    settings = Settings()

    # ========================================================
    # Create real production providers
    # ========================================================

    embedding_model = create_embedding_model(
        settings=settings
    )

    vector_store = create_vector_store(
        settings=settings
    )

    llm = create_llm(
        settings=settings
    )

    print()
    print(
        "Embedding provider:",
        type(embedding_model).__name__,
    )

    print(
        "Vector store:",
        type(vector_store).__name__,
    )

    print(
        "LLM provider:",
        type(llm).__name__,
    )

    # ========================================================
    # Real production retriever
    # ========================================================

    retriever = VectorEvidenceRetriever(
        embedding_model=embedding_model,
        vector_store=vector_store,
        top_k=settings.retrieval_top_k,
    )

    print()
    print("=" * 80)
    print("RESEARCH QUESTION")
    print("=" * 80)
    print(QUERY)

    retrieval = retriever.retrieve(
        ticker=TICKER,
        query=QUERY,
        filing_types=FILING_TYPES,
    )

    print()
    print("=" * 80)
    print(
        "RETRIEVED EVIDENCE:",
        len(retrieval.evidence),
    )
    print("=" * 80)

    for index, evidence in enumerate(
        retrieval.evidence,
        start=1,
    ):

        print()
        print("-" * 80)

        print(
            f"Evidence #{index}"
        )

        print(
            "Ticker:",
            evidence.ticker,
        )

        print(
            "Filing:",
            evidence.filing_type,
        )

        print(
            "Date:",
            evidence.filing_date,
        )

        print(
            "Section:",
            evidence.section,
        )

        print(
            "Relevance:",
            round(
                evidence.relevance_score,
                4,
            ),
        )

        print(
            "Source:",
            evidence.source,
        )

        print()

        print(
            evidence.text[:800]
        )

    # ========================================================
    # Real Fundamental Research Agent
    # ========================================================

    print()
    print("=" * 80)
    print("FUNDAMENTAL AGENT ??NOVA LITE")
    print("=" * 80)

    agent = FundamentalResearchAgent(
        llm=llm
    )

    result = agent.analyze(
        ticker=TICKER,
        research_question=QUERY,
        retrieval=retrieval,
    )

    print()
    print("=" * 80)
    print("FUNDAMENTAL ANALYSIS RESULT")
    print("=" * 80)

    print(
        json.dumps(
            serialize(result),
            indent=2,
            ensure_ascii=False,
            default=str,
        )
    )

    print()
    print("=" * 80)
    print("INTEGRATION TEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
