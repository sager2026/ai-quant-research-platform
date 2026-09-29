import chromadb


CHROMA_PATH = "data/chroma"
COLLECTION_NAME = "quantmind_filings"


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


counts = {
    "KEEP": 0,
    "SKIP_XBRL": 0,
    "SKIP_END_MATTER": 0,
}


for chunk_id, document, metadata in zip(
    ids,
    documents,
    metadatas,
):

    classification = classify_chunk(
        document
    )

    counts[classification] += 1

    if classification != "KEEP":

        print(
            f"{classification:16} "
            f"{metadata['filing_type']:4} "
            f"chunk={metadata['chunk_index']:3} "
            f"id={chunk_id[:12]}"
        )


print()
print("Migration preview")
print("-----------------")

for name, count in counts.items():
    print(
        f"{name:16}: {count}"
    )

print(
    f"{'TOTAL':16}: {len(ids)}"
)