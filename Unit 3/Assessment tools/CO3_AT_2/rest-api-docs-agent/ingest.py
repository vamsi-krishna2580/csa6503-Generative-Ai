import json
import os

from src.loader import load_documents
from src.chunker import chunk_documents
from src.embeddings import EmbeddingModel
from src.vector_store import VectorStore

from src.config import PROCESSED_DATA_PATH


def main():

    print("=" * 60)
    print("REST API DOCUMENTATION RAG - INGESTION")
    print("=" * 60)

    print("\n[1/4] Loading documentation...\n")

    documents = load_documents()

    if not documents:
        raise RuntimeError(
            "No documents were downloaded."
        )

    print("\n[2/4] Chunking documentation...\n")

    chunks = chunk_documents(
        documents
    )

    os.makedirs(
        PROCESSED_DATA_PATH,
        exist_ok=True,
    )

    chunks_file = os.path.join(
        PROCESSED_DATA_PATH,
        "chunks.json",
    )

    with open(
        chunks_file,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            chunks,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"Saved chunks to {chunks_file}"
    )

    print("\n[3/4] Loading embedding model...\n")

    embedding_model = EmbeddingModel()

    print("\n[4/4] Building FAISS vector store...\n")

    vector_store = VectorStore(
        embedding_model
    )

    vector_store.build(
        chunks
    )

    print("\n" + "=" * 60)
    print("INGESTION COMPLETE")
    print("=" * 60)

    print(
        f"Documents : {len(documents)}"
    )

    print(
        f"Chunks    : {len(chunks)}"
    )

    print(
        f"Vector DB : FAISS"
    )

    print(
        f"Embedding : all-MiniLM-L6-v2"
    )


if __name__ == "__main__":
    main()