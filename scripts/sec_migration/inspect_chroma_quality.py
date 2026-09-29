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
    include=[
        "documents",
        "metadatas",
    ]
)


ids = result["ids"]
documents = result["documents"]
metadatas = result["metadatas"]


samples = [
    0,
    10,
    25,
    50,
    75,
    100,
    125,
    129,
    130,
    150,
    175,
    185,
]


for index in samples:

    if index >= len(ids):
        continue

    print("=" * 80)

    print(
        f"CORPUS POSITION: "
        f"{index + 1}/{len(ids)}"
    )

    print(
        "ID:",
        ids[index],
    )

    print(
        "METADATA:",
        metadatas[index],
    )

    print()

    document = documents[index]

    print(
        "DOCUMENT:"
    )

    print(
        document[:1000]
    )

    print()