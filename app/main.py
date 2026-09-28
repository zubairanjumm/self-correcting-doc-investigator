import argparse
from pathlib import Path

from app.config import (
    DEFAULT_DOCS_PATH,
    MAX_REWRITES,
    TOP_K,
)
from app.graph.workflow import build_workflow
from app.ingestion.chunker import split_documents
from app.ingestion.loader import load_documents
from app.retrieval.embeddings import create_embedding_model
from app.retrieval.vector_store import add_documents, create_vector_store


def build_index(docs_path: Path):
    documents = load_documents(docs_path)

    if not documents:
        raise ValueError(f"No Markdown documents found in {docs_path}")

    chunks = split_documents(documents)
    embedding_model = create_embedding_model()
    vector_store = create_vector_store(embedding_model)
    add_documents(vector_store, chunks)

    return vector_store


def investigate(
    question: str,
    docs_path: Path = DEFAULT_DOCS_PATH,
    max_rewrites: int = MAX_REWRITES,
):
    vector_store = build_index(docs_path)
    workflow = build_workflow()

    return workflow.invoke(
        {
            "question": question,
            "documents": [],
            "answer": "",
            "relevant": False,
            "rewrite_count": 0,
            "max_rewrites": max_rewrites,
            "vector_store": vector_store,
            "top_k": TOP_K,
        }
    )


def main():
    parser = argparse.ArgumentParser(
        description="Self-correcting technical documentation investigator."
    )
    parser.add_argument("question", help="Question to investigate.")
    parser.add_argument(
        "--docs",
        type=Path,
        default=DEFAULT_DOCS_PATH,
        help="Directory containing Markdown documentation.",
    )
    parser.add_argument(
        "--max-rewrites",
        type=int,
        default=MAX_REWRITES,
        help="Maximum number of query rewrites.",
    )

    args = parser.parse_args()

    result = investigate(
        question=args.question,
        docs_path=args.docs,
        max_rewrites=args.max_rewrites,
    )

    print(result["answer"])


if __name__ == "__main__":
    main()
