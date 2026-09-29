import json

import boto3


# ============================================================
# Configuration
# ============================================================

AWS_PROFILE = "quantmind"
AWS_REGION = "us-east-2"

TITAN_MODEL_ID = "amazon.titan-embed-text-v2:0"

VECTOR_BUCKET = "quantmind-sec-vectors"
VECTOR_INDEX = "sec-filings-titan-v2-1024"

QUERY = (
    "What risks does Apple face from tariffs, "
    "international trade restrictions, and "
    "supply-chain concentration?"
)

TOP_K = 5


# ============================================================
# AWS clients
# ============================================================

session = boto3.Session(
    profile_name=AWS_PROFILE,
    region_name=AWS_REGION,
)

bedrock = session.client(
    "bedrock-runtime"
)

s3vectors = session.client(
    "s3vectors"
)


# ============================================================
# Step 1: Embed the research question with Titan
# ============================================================

print("=" * 80)
print("QUERY")
print("=" * 80)
print(QUERY)

request_body = {
    "inputText": QUERY,
    "dimensions": 1024,
    "normalize": True,
}

response = bedrock.invoke_model(
    modelId=TITAN_MODEL_ID,
    contentType="application/json",
    accept="application/json",
    body=json.dumps(
        request_body
    ),
)

model_response = json.loads(
    response["body"].read()
)

query_embedding = model_response[
    "embedding"
]


print()
print(
    "Query embedding dimensions:",
    len(query_embedding),
)


# ============================================================
# Step 2: Query S3 Vectors
# ============================================================

response = s3vectors.query_vectors(
    vectorBucketName=VECTOR_BUCKET,
    indexName=VECTOR_INDEX,

    queryVector={
        "float32": query_embedding
    },

    topK=TOP_K,

    filter={
        "$and": [
            {
                "ticker": "AAPL"
            },
            {
                "filing_type": {
                    "$in": [
                        "10-K",
                        "10-Q",
                    ]
                }
            },
        ]
    },

    returnDistance=True,
    returnMetadata=True,
)


# ============================================================
# Step 3: Display retrieved SEC evidence
# ============================================================

vectors = response.get(
    "vectors",
    [],
)

print()
print("=" * 80)
print(
    f"TOP {len(vectors)} RESULTS"
)
print("=" * 80)


for rank, vector in enumerate(
    vectors,
    start=1,
):

    metadata = vector.get(
        "metadata",
        {},
    )

    document = metadata.get(
        "document",
        "",
    )

    print()
    print("-" * 80)

    print(
        f"RANK: {rank}"
    )

    print(
        "Distance:",
        vector.get("distance")
    )

    print(
        "Key:",
        vector.get("key")
    )

    print(
        "Ticker:",
        metadata.get("ticker")
    )

    print(
        "Filing type:",
        metadata.get("filing_type")
    )

    print(
        "Filing date:",
        metadata.get("filing_date")
    )

    print(
        "Chunk index:",
        metadata.get("chunk_index")
    )

    print(
        "Section:",
        metadata.get("section")
    )

    print(
        "Source:",
        metadata.get("source")
    )

    print()
    print("DOCUMENT:")
    print(
        document[:1500]
    )