# Self-Correcting Document Investigator

A self-correcting RAG system that answers questions using technical documentation.

Instead of searching only once, the system checks whether the retrieved documents are relevant. If they are not useful enough, it rewrites the search query and searches again.

## How It Works

```text
User Question
      ↓
Retrieve Documents
      ↓
Grade Documents
      ↓
Relevant?
  ↓ Yes       ↓ No
Generate    Rewrite Query
Answer          ↓
             Retrieve Again
                  ↓
              Grade Again
```

The number of rewrites is limited so the system does not loop forever.

## Features

* Markdown document ingestion
* Document chunking
* Local embeddings with Sentence Transformers
* Chroma vector database
* Semantic document retrieval
* LLM-based document relevance grading
* Automatic query rewriting
* Bounded self-correction loop
* Gemini-powered answer generation
* Streamlit interface
* Pytest test suite

## Tech Stack

* Python
* LangChain
* LangGraph
* Google Gemini
* ChromaDB
* Sentence Transformers
* Pydantic
* Streamlit
* Pytest

## Project Structure

```text
self-correcting-doc-investigator/
│
├── app/
│   ├── graph/
│   │   ├── nodes.py
│   │   ├── state.py
│   │   └── workflow.py
│   │
│   ├── ingestion/
│   │   ├── loader.py
│   │   └── chunker.py
│   │
│   ├── llm/
│   │   ├── generator.py
│   │   ├── grader.py
│   │   └── rewriter.py
│   │
│   ├── retrieval/
│   │   ├── embeddings.py
│   │   └── vector_store.py
│   │
│   ├── config.py
│   ├── main.py
│   └── streamlit_app.py
│
├── data/
│   └── documents/
│
├── tests/
│
├── pyproject.toml
└── README.md
```

## Setup

Clone the repository and install the dependencies:

```bash
uv sync
```

Create a `.env` file and add your Gemini API key:

```env
GOOGLE_API_KEY=your_api_key_here
```

Put your Markdown documentation inside:

```text
data/documents/
```

## Run the Streamlit App

```bash
uv run streamlit run app/streamlit_app.py
```

Then ask a question about your documentation.

For example:

```text
How do I configure authentication?
```

## Run from the CLI

```bash
uv run python -m app.main "How do I configure authentication?"
```

## Run Tests

```bash
uv run pytest -v
```

## Example

Suppose the first search retrieves documentation about API rate limits instead of authentication.

The system can:

```text
Question
   ↓
Search
   ↓
Wrong / insufficient documents
   ↓
Rewrite query
   ↓
Search again
   ↓
Relevant authentication documentation
   ↓
Generate answer
```

This is the main idea behind the project: **the retrieval process can correct itself instead of relying on a single search attempt.**

## Purpose

This project was built to explore how self-correction can improve a basic RAG pipeline using retrieval, grading, query rewriting, and a graph-based workflow.
