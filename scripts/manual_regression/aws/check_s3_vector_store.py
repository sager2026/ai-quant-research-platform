from app.infrastructure.rag.s3_vector_store import (
    S3VectorStore,
)


class FakeS3VectorsClient:

    def __init__(self):
        self.put_requests = []
        self.query_request = None

    def put_vectors(self, **kwargs):

        self.put_requests.append(
            kwargs
        )

        return {}

    def query_vectors(self, **kwargs):

        self.query_request = kwargs

        return {
            "distanceMetric": "cosine",
            "vectors": [
                {
                    "key": "AAPL-10K-001",
                    "distance": 0.12,
                    "metadata": {
                        "document": (
                            "Apple faces supply-chain "
                            "and geopolitical risks."
                        ),
                        "ticker": "AAPL",
                        "filing_type": "10-K",
                        "filing_date": "2025-09-26",
                        "section": "Risk Factors",
                        "source": "SEC",
                    },
                }
            ],
        }


fake_client = FakeS3VectorsClient()

store = S3VectorStore(
    vector_bucket_name="quantmind-vectors",
    index_name="sec-filings-titan-v2",
    region="us-east-2",
    client=fake_client,
)


# =========================================================
# ADD
# =========================================================

store.add(
    ids=[
        "AAPL-10K-001"
    ],
    documents=[
        "Apple faces supply-chain "
        "and geopolitical risks."
    ],
    embeddings=[
        [0.1, 0.2, 0.3, 0.4]
    ],
    metadatas=[
        {
            "ticker": "AAPL",
            "filing_type": "10-K",
            "filing_date": "2025-09-26",
            "section": "Risk Factors",
            "source": "SEC",
        }
    ],
)

print(
    "Put requests:",
    len(fake_client.put_requests),
)

print(
    "Stored key:",
    fake_client
    .put_requests[0]["vectors"][0]["key"],
)

print(
    "Stored document:",
    fake_client
    .put_requests[0]["vectors"][0]
    ["metadata"]["document"],
)


# =========================================================
# SEARCH
# =========================================================

matches = store.search(
    query_embedding=[
        0.1,
        0.2,
        0.3,
        0.4,
    ],
    ticker="AAPL",
    filing_types=[
        "10-K",
        "10-Q",
    ],
    top_k=5,
)

print(
    "Match count:",
    len(matches),
)

print(
    "Document:",
    matches[0]["document"],
)

print(
    "Ticker:",
    matches[0]["metadata"]["ticker"],
)

print(
    "Distance:",
    matches[0]["distance"],
)

print(
    "Filter:",
    fake_client.query_request["filter"],
)