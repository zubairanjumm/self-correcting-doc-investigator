from langchain_core.documents import Document

from app.retrieval.vector_store import retrieve_documents


class FakeVectorStore:
    def similarity_search(self, query, k):
        return [
            Document(
                page_content=f"Result for {query}",
                metadata={"source": "test.md"},
            )
        ][:k]


def test_retrieve_documents():
    store = FakeVectorStore()

    documents = retrieve_documents(store, "How do I configure auth?", k=1)

    assert len(documents) == 1
    assert "configure auth" in documents[0].page_content
