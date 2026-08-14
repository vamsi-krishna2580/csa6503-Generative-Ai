import google.generativeai as genai

from .config import (
    GOOGLE_API_KEY,
    GEMINI_MODEL,
    TOP_K,
)

from .prompts import build_prompt


class RestApiDocsAgent:

    def __init__(
        self,
        retriever,
    ):

        if not GOOGLE_API_KEY:
            raise ValueError(
                "GOOGLE_API_KEY is missing "
                "from .env"
            )

        genai.configure(
            api_key=GOOGLE_API_KEY
        )

        self.model = genai.GenerativeModel(
            GEMINI_MODEL
        )

        self.retriever = retriever

    def classify_query(self, query):

        query_lower = query.lower()

        endpoint_words = [
            "endpoint",
            "api",
            "request",
            "http",
            "get ",
            "post ",
            "put ",
            "patch ",
            "delete ",
            "repository",
            "issue",
            "pull request",
            "branch",
            "release",
        ]

        auth_words = [
            "auth",
            "authentication",
            "token",
            "permission",
            "permissions",
            "authorization",
            "bearer",
            "personal access token",
        ]

        error_words = [
            "error",
            "403",
            "404",
            "401",
            "429",
            "500",
            "rate limit",
            "forbidden",
            "unauthorized",
        ]

        categories = []

        if any(
            word in query_lower
            for word in endpoint_words
        ):
            categories.append("endpoint")

        if any(
            word in query_lower
            for word in auth_words
        ):
            categories.append("authentication")

        if any(
            word in query_lower
            for word in error_words
        ):
            categories.append("errors")

        if not categories:
            categories.append("general")

        return categories

    def retrieve(self, query):

        categories = self.classify_query(
            query
        )

        # Retrieve extra chunks when a query
        # combines multiple topics.
        top_k = TOP_K

        if len(categories) > 1:
            top_k = 7

        documents = self.retriever.retrieve(
            query,
            top_k,
        )

        return categories, documents

    def answer(self, query):

        categories, documents = (
            self.retrieve(query)
        )

        if not documents:

            return {
                "answer": (
                    "I cannot answer this from the "
                    "available GitHub REST API "
                    "documentation."
                ),
                "categories": categories,
                "sources": [],
                "retrieved": [],
            }

        prompt = build_prompt(
            query,
            documents,
        )

        response = self.model.generate_content(
            prompt
        )

        answer = response.text

        return {
            "answer": answer,
            "categories": categories,
            "sources": documents,
            "retrieved": documents,
        }