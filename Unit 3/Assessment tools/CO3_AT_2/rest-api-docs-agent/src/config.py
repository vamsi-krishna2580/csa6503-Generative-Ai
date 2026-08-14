import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

TOP_K = 5

VECTORSTORE_PATH = "vectorstore/github_rest_docs"

RAW_DATA_PATH = "data/raw"
PROCESSED_DATA_PATH = "data/processed"

GEMINI_MODEL = "gemini-3.5-flash-lite"

SIMILARITY_THRESHOLD = 0.30