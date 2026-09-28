from langchain_core.documents import Document

from app.graph import nodes


class FakeVectorStore:
    def __init__(self):
        self.queries = []

    def similarity_search(self, query, k):
        self.queries.append(query)

        if len(self.queries) == 1:
            return [
                Document(
                    page_content="This document explains API rate limits.",
                    metadata={"source": "api.md"},
                )
            ]

        return [
            Document(
                page_content=(
                    "Authentication is configured using the API_KEY "
                    "environment variable."
                ),
                metadata={"source": "authentication.md"},
            )
        ]


def test_self_correction_loop(monkeypatch):
    store = FakeVectorStore()

    def fake_grade_documents(question, documents):
        return "authentication" in documents[0].page_content.lower()

    def fake_rewrite_query(question, documents):
        return "API authentication configuration"

    def fake_generate_answer(question, documents):
        return "Authentication uses the API_KEY environment variable."

    monkeypatch.setattr(
        nodes,
        "grade_documents",
        fake_grade_documents,
    )

    monkeypatch.setattr(
        nodes,
        "rewrite_query",
        fake_rewrite_query,
    )

    monkeypatch.setattr(
        nodes,
        "generate_answer",
        fake_generate_answer,
    )

    from app.graph.workflow import build_workflow

    workflow = build_workflow()

    result = workflow.invoke(
        {
            "question": "How do I configure authentication?",
            "documents": [],
            "answer": "",
            "relevant": False,
            "rewrite_count": 0,
            "max_rewrites": 1,
            "vector_store": store,
            "top_k": 1,
        }
    )

    assert store.queries == [
        "How do I configure authentication?",
        "API authentication configuration",
    ]

    assert result["rewrite_count"] == 1
    assert result["relevant"] is True
    assert result["answer"] == (
        "Authentication uses the API_KEY environment variable."
    )