from .config import TOP_K, SIMILARITY_THRESHOLD


class Retriever:

    def __init__(self, vector_store):

        self.vector_store = vector_store

    def retrieve(
        self,
        query,
        top_k=TOP_K,
    ):

        results = self.vector_store.search(
            query,
            top_k,
        )

        if not results:
            return []

        filtered = [
            result
            for result in results
            if result["score"]
            >= SIMILARITY_THRESHOLD
        ]

        return filtered