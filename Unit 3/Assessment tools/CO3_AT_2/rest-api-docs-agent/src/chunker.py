from langchain_text_splitters import RecursiveCharacterTextSplitter

from .config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )

    chunks = []

    for document in documents:

        text_chunks = splitter.split_text(
            document["content"]
        )

        for chunk_number, text in enumerate(
            text_chunks,
            start=1,
        ):

            chunks.append(
                {
                    "chunk_id": (
                        f"{document['id']}-{chunk_number}"
                    ),
                    "document_id": document["id"],
                    "title": document["title"],
                    "url": document["url"],
                    "category": document["category"],
                    "chunk_number": chunk_number,
                    "content": text,
                }
            )

    print(f"Created {len(chunks)} chunks.")

    return chunks