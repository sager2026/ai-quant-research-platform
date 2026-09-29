import chromadb
CHROMA_PATH = "data/chroma"
COLLECTION_NAME = "quantmind_filings"
client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_collection(
    name=COLLECTION_NAME
)

result = collection.get(
    limit=3,
    include=[
        "documents",
        "metadatas",
    ],
)
ids = result["ids"]
documents = result["documents"]
metadatas = result["metadatas"]
for i, (
    chunk_id,
    document,
    metadata,
) in enumerate(
    zip(
        ids,
        documents,
        metadatas,
    ),
    start=1,
):

    print("=" * 80)
    print("SAMPLE:", i)
    print("ID:", chunk_id)

    print()
    print("METADATA:")
    print(metadata)

    print()
    print("DOCUMENT:")
    print(document[:500])

    print()
