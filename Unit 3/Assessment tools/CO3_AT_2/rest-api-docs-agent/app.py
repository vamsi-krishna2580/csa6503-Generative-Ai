import streamlit as st

from src.embeddings import EmbeddingModel
from src.vector_store import VectorStore
from src.retriever import Retriever
from src.agent import RestApiDocsAgent

from src.config import (
    TOP_K,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    EMBEDDING_MODEL,
    GEMINI_MODEL,
)


st.set_page_config(
    page_title="REST API Docs Agent",
    page_icon="🔎",
    layout="wide",
)


@st.cache_resource
def initialize_agent():

    embedding_model = EmbeddingModel()

    vector_store = VectorStore(
        embedding_model
    )

    vector_store.load()

    retriever = Retriever(
        vector_store
    )

    agent = RestApiDocsAgent(
        retriever
    )

    return agent


st.title("🔎 REST API Documentation Agent")

st.markdown(
    """
### GitHub REST API Documentation QA

Ask questions about GitHub REST API:

- Endpoints
- Authentication
- Permissions
- Parameters
- Errors
- Rate limits
- Request examples
"""
)

with st.sidebar:

    st.header("RAG Configuration")

    st.write(
        f"**Embedding:** `{EMBEDDING_MODEL}`"
    )

    st.write(
        f"**Chunk size:** `{CHUNK_SIZE}`"
    )

    st.write(
        f"**Chunk overlap:** `{CHUNK_OVERLAP}`"
    )

    st.write(
        f"**Top-K:** `{TOP_K}`"
    )

    st.write(
        f"**LLM:** `{GEMINI_MODEL}`"
    )

    st.divider()

    st.info(
        """
This system answers only from the
indexed GitHub REST API documentation.

Retrieved chunks are displayed below
each answer to demonstrate grounding.
"""
    )


try:

    agent = initialize_agent()

except Exception as error:

    st.error(
        f"Failed to initialize RAG system: {error}"
    )

    st.stop()


query = st.text_area(
    "Ask a REST API documentation question",
    placeholder=(
        "Example: How do I create an issue "
        "using the GitHub REST API and what "
        "authentication is required?"
    ),
    height=100,
)


if st.button(
    "Ask Documentation Agent",
    type="primary",
):

    if not query.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "Retrieving documentation and generating answer..."
        ):

            result = agent.answer(
                query
            )

        st.subheader("Answer")

        st.markdown(
            result["answer"]
        )

        st.divider()

        st.subheader(
            "🤖 Agent Routing"
        )

        st.write(
            "Detected topics:"
        )

        for category in result[
            "categories"
        ]:

            st.badge(category)

        st.divider()

        st.subheader(
            "📚 Retrieved Documentation"
        )

        if not result["retrieved"]:

            st.warning(
                "No sufficiently relevant "
                "documentation was retrieved."
            )

        for index, document in enumerate(
            result["retrieved"],
            start=1,
        ):

            score = document[
                "score"
            ]

            with st.expander(
                f"Source {index}: "
                f"{document['title']} "
                f"(similarity: {score:.3f})"
            ):

                st.markdown(
                    f"**Category:** "
                    f"{document['category']}"
                )

                st.markdown(
                    f"**Chunk:** "
                    f"{document['chunk_id']}"
                )

                st.markdown(
                    f"**Source:** "
                    f"[Official GitHub Documentation]"
                    f"({document['url']})"
                )

                st.markdown(
                    "**Retrieved chunk:**"
                )

                st.code(
                    document["content"],
                    language="text",
                )