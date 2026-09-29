import json
import time
from pathlib import Path

import boto3
import chromadb
from botocore.exceptions import ClientError


# ============================================================
# Configuration
# ============================================================

AWS_PROFILE = "quantmind"
AWS_REGION = "us-east-2"

CHROMA_PATH = "data/chroma"
CHROMA_COLLECTION = "quantmind_filings"

VECTOR_BUCKET = "quantmind-sec-vectors"
VECTOR_INDEX = "sec-filings-titan-v2-1024"

TITAN_MODEL_ID = "amazon.titan-embed-text-v2:0"
EMBEDDING_DIMENSIONS = 1024

# Titan quota currently:
#   60 RPM
#
# 1.1 seconds between requests keeps us comfortably below it.
SECONDS_BETWEEN_EMBEDDINGS = 1.1

# S3 Vectors supports larger batches, but 25 gives us
# smaller restart units if something fails.
PUT_BATCH_SIZE = 25

CHECKPOINT_FILE = Path(
    "data/titan_s3vectors_migration_checkpoint.json"
)


# ============================================================
# Filtering
# ============================================================

XBRL_SIGNALS = (
    "http://fasb.org/",
    "us-gaap:",
    "xbrli:",
    "iso4217:",
    "dei:",
)

END_MATTER_SIGNALS = (
    "Pursuant to the requirements of the Securities Exchange Act of 1934",
    "Item 6.    Exhibits",
    "Rule 13a-14(a) / 15d-14(a) Certification",
)


def classify_chunk(document: str) -> str:

    text = document or ""

    xbrl_score = sum(
        text.count(signal)
        for signal in XBRL_SIGNALS
    )

    if xbrl_score >= 10:
        return "SKIP_XBRL"

    if any(
        signal in text
        for signal in END_MATTER_SIGNALS
    ):
        return "SKIP_END_MATTER"

    return "KEEP"


# ============================================================
# Checkpoint
# ============================================================

def load_checkpoint() -> set[str]:

    if not CHECKPOINT_FILE.exists():
        return set()

    with CHECKPOINT_FILE.open(
        "r",
        encoding="utf-8",
    ) as f:
        data = json.load(f)

    return set(
        data.get(
            "completed_ids",
            [],
        )
    )


def save_checkpoint(
    completed_ids: set[str],
) -> None:

    CHECKPOINT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    payload = {
        "completed_ids": sorted(
            completed_ids
        )
    }

    with CHECKPOINT_FILE.open(
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            payload,
            f,
            indent=2,
        )


# ============================================================
# Titan
# ============================================================

def embed_text(
    bedrock_client,
    text: str,
) -> list[float]:

    request_body = {
        "inputText": text,
        "dimensions": EMBEDDING_DIMENSIONS,
        "normalize": True,
    }

    while True:

        try:

            response = bedrock_client.invoke_model(
                modelId=TITAN_MODEL_ID,
                contentType="application/json",
                accept="application/json",
                body=json.dumps(
                    request_body
                ),
            )

            body = json.loads(
                response["body"].read()
            )

            embedding = body["embedding"]

            if (
                len(embedding)
                != EMBEDDING_DIMENSIONS
            ):
                raise RuntimeError(
                    "Unexpected Titan embedding "
                    f"dimension: {len(embedding)}"
                )

            return embedding

        except ClientError as exc:

            code = (
                exc.response
                .get("Error", {})
                .get("Code", "")
            )

            if code in {
                "ThrottlingException",
                "TooManyRequestsException",
            }:

                print(
                    "Titan throttled; retrying..."
                )

                time.sleep(5)
                continue

            raise


# ============================================================
# S3 Vectors
# ============================================================

def write_batch(
    s3vectors_client,
    batch: list[dict],
) -> None:

    if not batch:
        return

    s3vectors_client.put_vectors(
        vectorBucketName=VECTOR_BUCKET,
        indexName=VECTOR_INDEX,
        vectors=batch,
    )


# ============================================================
# Main migration
# ============================================================

def main():

    print("=" * 70)
    print("QuantMind SEC → Titan V2 → S3 Vectors migration")
    print("=" * 70)

    # --------------------------------------------------------
    # AWS clients
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Chroma
    # --------------------------------------------------------

    chroma_client = (
        chromadb.PersistentClient(
            path=CHROMA_PATH
        )
    )

    collection = (
        chroma_client.get_collection(
            name=CHROMA_COLLECTION
        )
    )

    result = collection.get(
        include=[
            "documents",
            "metadatas",
        ]
    )

    ids = result["ids"]
    documents = result["documents"]
    metadatas = result["metadatas"]

    # --------------------------------------------------------
    # Prepare migration corpus
    # --------------------------------------------------------

    records = []

    skipped_xbrl = 0
    skipped_end = 0

    for (
        chunk_id,
        document,
        metadata,
    ) in zip(
        ids,
        documents,
        metadatas,
    ):

        classification = classify_chunk(
            document
        )

        if classification == "SKIP_XBRL":

            skipped_xbrl += 1
            continue

        if classification == "SKIP_END_MATTER":

            skipped_end += 1
            continue

        records.append(
            {
                "id": chunk_id,
                "document": document,
                "metadata": metadata,
            }
        )

    print()
    print(
        "Chroma chunks:",
        len(ids),
    )

    print(
        "Skipped XBRL:",
        skipped_xbrl,
    )

    print(
        "Skipped end matter:",
        skipped_end,
    )

    print(
        "Migration corpus:",
        len(records),
    )

    # --------------------------------------------------------
    # Resume support
    # --------------------------------------------------------

    completed_ids = load_checkpoint()

    if completed_ids:

        print(
            "Checkpoint entries:",
            len(completed_ids),
        )

    remaining = [
        record
        for record in records
        if record["id"]
        not in completed_ids
    ]

    print(
        "Remaining:",
        len(remaining),
    )

    if not remaining:

        print()
        print("Nothing to migrate.")
        return

    # --------------------------------------------------------
    # Embed + batch write
    # --------------------------------------------------------

    batch = []
    batch_ids = []

    total = len(records)

    for record in remaining:

        chunk_id = record["id"]
        document = record["document"]
        metadata = record["metadata"]

        original_position = (
            records.index(record) + 1
        )

        print(
            f"[{original_position:03}/{total}] "
            f"{metadata.get('ticker')} "
            f"{metadata.get('filing_type')} "
            f"chunk={metadata.get('chunk_index')} "
            "→ Titan",
            flush=True,
        )

        embedding = embed_text(
            bedrock,
            document,
        )

        vector_metadata = dict(
            metadata
        )

        # Store the actual SEC evidence with the vector.
        vector_metadata[
            "document"
        ] = document

        vector = {
            "key": chunk_id,
            "data": {
                "float32": embedding
            },
            "metadata": vector_metadata,
        }

        batch.append(vector)
        batch_ids.append(chunk_id)

        # Respect Titan RPM quota.
        time.sleep(
            SECONDS_BETWEEN_EMBEDDINGS
        )

        if (
            len(batch)
            >= PUT_BATCH_SIZE
        ):

            print(
                f"  → writing "
                f"{len(batch)} vectors "
                "to S3 Vectors..."
            )

            write_batch(
                s3vectors,
                batch,
            )

            completed_ids.update(
                batch_ids
            )

            save_checkpoint(
                completed_ids
            )

            print(
                f"  → committed "
                f"{len(completed_ids)}/{total}"
            )

            batch = []
            batch_ids = []

    # --------------------------------------------------------
    # Final partial batch
    # --------------------------------------------------------

    if batch:

        print(
            f"  → writing final "
            f"{len(batch)} vectors "
            "to S3 Vectors..."
        )

        write_batch(
            s3vectors,
            batch,
        )

        completed_ids.update(
            batch_ids
        )

        save_checkpoint(
            completed_ids
        )

    print()
    print("=" * 70)
    print("Migration complete")
    print("=" * 70)

    print(
        "Vectors migrated:",
        len(completed_ids),
    )

    print(
        "Vector bucket:",
        VECTOR_BUCKET,
    )

    print(
        "Vector index:",
        VECTOR_INDEX,
    )

    print(
        "Embedding model:",
        TITAN_MODEL_ID,
    )

    print(
        "Dimensions:",
        EMBEDDING_DIMENSIONS,
    )


if __name__ == "__main__":
    main()