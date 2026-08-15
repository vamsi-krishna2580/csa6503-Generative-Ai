# CO3_AT_3 — Wildlife Observation Search

## Overview

This project implements a simple **semantic search system for wildlife observation reports** and benchmarks two vector-search technologies:

- **FAISS**
- **ChromaDB**

The same wildlife dataset, the same `all-MiniLM-L6-v2` embedding model, and the same embeddings are used for both systems to make the comparison fair.

## Student Details

| Field | Details |
|---|---|
| Name | N. Vamsi Krishna |
| Register Number | 192472011 |
| Course Code | CSA6503 |
| Course Name | Generative AI and Large Scale Models |
| Assessment | CO3 Assessment Tool 3 |
| Topic | Wildlife Observation Search |

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Implementation |
| Jupyter Notebook | Experiment and benchmarking |
| Sentence Transformers | Text embedding generation |
| `all-MiniLM-L6-v2` | Sentence embedding model |
| FAISS | Vector similarity search |
| ChromaDB | Vector database and semantic search |
| Pandas | Dataset and result processing |
| NumPy | Numerical operations |

## Dataset

The project uses a **synthetic citizen-science wildlife observation dataset** containing:

- **250 wildlife observation records**
- **25 species**
- Common name
- Scientific name
- Observation description

Dataset file:

`dataset/wildlife_observations.csv`

The observation descriptions are synthetic and were created for educational semantic-search benchmarking. The common-name/scientific-name pairs are based on publicly available wildlife taxonomy information.

## What We Did

The implementation follows the assignment requirements:

1. Loaded 250 wildlife observation descriptions.
2. Generated embeddings using `all-MiniLM-L6-v2`.
3. Obtained **250 embeddings with 384 dimensions**.
4. Used the same embeddings to create a FAISS index.
5. Used the same embeddings and metadata to create a ChromaDB collection.
6. Ran **10 semantic-search queries** on both systems.
7. Retrieved the **Top-5 results** from each system.
8. Measured FAISS and ChromaDB indexing time.
9. Measured average query latency.
10. Evaluated the number of relevant results in the Top-5.
11. Compared FAISS and ChromaDB results for multiple queries.
12. Tested the required scientific-name special case using:
   `Panthera tigris tigris`
13. Measured the storage footprint of both systems.
14. Saved the benchmark results as CSV files.

## FAISS vs ChromaDB — Benchmark Results

| Metric | FAISS | ChromaDB |
|---|---:|---:|
| Number of records | 250 | 250 |
| Embedding dimension | 384 | 384 |
| Indexing time | 0.000362 s | 0.276422 s |
| Average query latency | 0.000443 s | 0.004105 s |
| Average relevant results in Top-5 | 1.5 | 1.5 |
| Storage footprint | 375.04 KB | 1.78 MB |

## Comparison

| Feature | FAISS | ChromaDB |
|---|---|---|
| Main purpose | Fast vector similarity search | Vector database |
| Search speed in this experiment | Faster | Slower |
| Indexing time in this experiment | Lower | Higher |
| Query latency in this experiment | Lower | Higher |
| Metadata support | Basic / application-managed | Built-in metadata with documents |
| Persistence | Saved FAISS index | Persistent database |
| Storage in this experiment | Smaller | Larger |
| Best suited for | Fast, lightweight vector search | Applications needing database-style storage and metadata |

## Query Results

### Query 1

**Query:** `A large striped predator seen near a forest at dusk`

FAISS and ChromaDB returned the same Top-5 results in the displayed experiment.

![Query 1 FAISS and ChromaDB Results](Outputs/Screenshot%202026-08-15%20233930.png)

### Benchmark Results

The final benchmark confirms that both systems used the same 250 records and 384-dimensional embeddings.

![Final Benchmark Results](Outputs/Screenshot%202026-08-15%20233849.png)

### Average Query Latency

FAISS achieved an average query latency of **0.000443 seconds**, while ChromaDB achieved **0.004105 seconds**.

![Average Query Latency](Outputs/Screenshot%202026-08-15%20233842.png)

### Top-5 Relevance

The relevance evaluation was performed for all 10 semantic queries. Both systems achieved an average of **1.5 relevant results in the Top-5**.

![Top-5 Relevance Results](Outputs/Screenshot%202026-08-15%20233916.png)

### Special Case — Common Name vs Scientific Name

The special-case query was:

`Panthera tigris tigris observed near woodland`

In the displayed experiment, neither FAISS nor ChromaDB returned Bengal Tiger in the Top-5 for this query. Therefore, the experiment **does not demonstrate successful common-name/scientific-name matching for this particular query**.

![Scientific Name Special Case](Outputs/Screenshot%202026-08-15%20233902.png)

## Conclusion

For this 250-record wildlife semantic-search benchmark, **FAISS performed faster and used less storage** than ChromaDB.

FAISS recorded:

- Lower indexing time
- Lower average query latency
- Smaller storage footprint

Both systems produced the same average Top-5 relevance score of **1.5** in the implemented evaluation.

Therefore, **FAISS is suitable when fast and lightweight vector similarity search is the main requirement**. ChromaDB is preferable when an application benefits from a persistent vector database with document and metadata management.

The special scientific-name query did not successfully retrieve Bengal Tiger in the displayed Top-5 results, so this experiment should not claim that the embedding model solved the common-name/scientific-name case.

## Project Structure

```text
CO3_AT_3___Wildlife-Observation-Search/
│
├── requirements.txt
├── wildlife_search_final.ipynb
│
├── dataset/
│   └── wildlife_observations.csv
│
├── Outputs/
│   ├── Screenshot 2026-08-15 233842.png
│   ├── Screenshot 2026-08-15 233849.png
│   ├── Screenshot 2026-08-15 233902.png
│   ├── Screenshot 2026-08-15 233916.png
│   ├── Screenshot 2026-08-15 233930.png
│   └── Screenshot 2026-08-15 233938.png
│
└── results/
    ├── final_benchmark.csv
    ├── query_latency.csv
    ├── relevance_results.csv
    ├── wildlife_faiss.index
    └── chroma_db/
```

## Running the Project

Activate the Python environment and install the dependencies:

```bash
pip install -r requirements.txt
```

Open the notebook:

```bash
jupyter notebook wildlife_search_final.ipynb
```

Run the notebook cells to reproduce the embedding generation, FAISS and ChromaDB indexing, semantic searches, and benchmark results.

## Output Files

| File | Description |
|---|---|
| `results/final_benchmark.csv` | Final FAISS vs ChromaDB benchmark |
| `results/query_latency.csv` | Query latency for the 10 queries |
| `results/relevance_results.csv` | Top-5 relevance evaluation |
| `results/wildlife_faiss.index` | Saved FAISS index |
| `results/chroma_db/` | Persistent ChromaDB storage |


