import hashlib

from app.application.knowledge.knowledge_store import KnowledgeStore
from app.domain.entities.filing import Filing

from app.infrastructure.rag.sec_document_extractor import (
    SECDocumentExtractor,
)
from app.infrastructure.rag.text_chunker import (
    TextChunker,
)
from app.infrastructure.rag.ollama_embedding_model import (
    OllamaEmbeddingModel,
)
from app.infrastructure.rag.chroma_vector_store import (
    ChromaVectorStore,
)


class VectorKnowledgeStore(KnowledgeStore):

    def __init__(
        self,
        extractor: SECDocumentExtractor,
        chunker: TextChunker,
        embedding_model: OllamaEmbeddingModel,
        vector_store: ChromaVectorStore,
    ):
        self.extractor = extractor
        self.chunker = chunker
        self.embedding_model = embedding_model
        self.vector_store = vector_store

    def store(
        self,
        filing: Filing,
    ) -> None:

        text = self.extractor.extract(
            filing.content
        )

        chunks = self.chunker.chunk(
            text
        )

        if not chunks:
            return

        embeddings = self.embedding_model.embed_many(
            chunks
        )

        ids = []
        metadatas = []

        for index, chunk in enumerate(chunks):

            chunk_id = self._create_chunk_id(
                filing=filing,
                index=index,
                chunk=chunk,
            )

            ids.append(chunk_id)

            metadatas.append(
                {
                    "ticker": filing.ticker,
                    "filing_type": filing.filing_type,
                    "filing_date": filing.filing_date,
                    "section": "Unknown",
                    "source": filing.source,
                    "chunk_index": index,
                }
            )

        self.vector_store.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def _create_chunk_id(
        self,
        filing: Filing,
        index: int,
        chunk: str,
    ) -> str:

        value = (
            f"{filing.ticker}|"
            f"{filing.filing_type}|"
            f"{filing.filing_date}|"
            f"{index}|"
            f"{chunk}"
        )

        return hashlib.sha256(
            value.encode("utf-8")
        ).hexdigest()