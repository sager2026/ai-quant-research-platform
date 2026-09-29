from collections import Counter
import chromadb
CHROMA_PATH = "data/chroma"
COLLECTION_NAME = "quantmind_filings"
client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

print("Collections:")
for collection_info in client.list_collections():
    print(" -", collection_info)
collection = client.get_collection(
    name=COLLECTION_NAME
)

print()
print("Collection:", COLLECTION_NAME)
print("Total chunks:", collection.count())
result = collection.get(
    include=["metadatas"]
)

metadatas = result.get(
    "metadatas",
    [],
)
counts = Counter()

for metadata in metadatas:

    ticker = str(
        metadata.get(
            "ticker",
            "UNKNOWN",
        )
    ).upper()

    filing_type = str(
        metadata.get(
            "filing_type",
            "UNKNOWN",
        )
    ).upper()

    counts[
        (
            ticker,
            filing_type,
        )
    ] += 1

print()
print("Chunks by ticker / filing type:")
print()

for (
    ticker,
    filing_type,
), count in sorted(
    counts.items()
):

    print(
        f"{ticker:8} "
        f"{filing_type:8} "
        f"{count:6}"
    )

