from langchain_core.documents import Document

from app.ingestion.chunker import split_documents


def test_split_documents_creates_chunks():
    document = Document(page_content="word " * 1000, metadata={"source": "test.md"})

    chunks = split_documents([document])

    assert len(chunks) > 1
    assert all(chunk.page_content for chunk in chunks)
    assert all(chunk.metadata["source"] == "test.md" for chunk in chunks)
