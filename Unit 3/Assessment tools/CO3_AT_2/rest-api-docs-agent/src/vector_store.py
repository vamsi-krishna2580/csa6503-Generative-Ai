import os
import pickle

import faiss
import numpy as np

from .config import VECTORSTORE_PATH


class VectorStore:

    def __init__(self, embedding_model):

        self.embedding_model = embedding_model
        self.index = None
        self.documents = []

    def build(self, chunks):

        texts = [
            chunk["content"]
            for chunk in chunks
        ]

        print("Generating embeddings...")

        embeddings = (
            self.embedding_model
            .embed_documents(texts)
        )

        embeddings = np.asarray(
            embeddings,
            dtype="float32",
        )

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(
            dimension
        )

        self.index.add(embeddings)

        self.documents = chunks

        self.save()

        print(
            f"FAISS index created with "
            f"{self.index.ntotal} vectors."
        )

    def save(self):

        os.makedirs(
            os.path.dirname(VECTORSTORE_PATH),
            exist_ok=True,
        )

        faiss.write_index(
            self.index,
            VECTORSTORE_PATH + ".index",
        )

        with open(
            VECTORSTORE_PATH + ".pkl",
            "wb",
        ) as file:

            pickle.dump(
                self.documents,
                file,
            )

    def load(self):

        index_path = VECTORSTORE_PATH + ".index"
        data_path = VECTORSTORE_PATH + ".pkl"

        if not os.path.exists(index_path):
            raise FileNotFoundError(
                "Vector index not found. "
                "Run ingest.py first."
            )

        self.index = faiss.read_index(
            index_path
        )

        with open(
            data_path,
            "rb",
        ) as file:

            self.documents = pickle.load(file)

        print(
            f"Loaded FAISS index with "
            f"{self.index.ntotal} vectors."
        )

    def search(
        self,
        query,
        top_k=5,
    ):

        query_embedding = (
            self.embedding_model
            .embed_query(query)
        )

        query_embedding = np.asarray(
            [query_embedding],
            dtype="float32",
        )

        scores, indices = self.index.search(
            query_embedding,
            top_k,
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0],
        ):

            if index == -1:
                continue

            document = dict(
                self.documents[index]
            )

            document["score"] = float(score)

            results.append(document)

        return results