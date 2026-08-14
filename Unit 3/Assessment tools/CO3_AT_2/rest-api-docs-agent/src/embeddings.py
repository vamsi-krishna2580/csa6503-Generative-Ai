from sentence_transformers import SentenceTransformer

from .config import EMBEDDING_MODEL


class EmbeddingModel:

    def __init__(self):
        print(
            f"Loading embedding model: "
            f"{EMBEDDING_MODEL}"
        )

        self.model = SentenceTransformer(
            EMBEDDING_MODEL
        )

    def embed_documents(self, texts):

        return self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True,
        )

    def embed_query(self, text):

        return self.model.encode(
            [text],
            normalize_embeddings=True,
        )[0]