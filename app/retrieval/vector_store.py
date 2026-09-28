from pathlib import Path

from langchain_chroma import Chroma

from app.config import VECTOR_STORE_PATH


def create_vector_store(embedding_model):
    VECTOR_STORE_PATH.mkdir(parents=True, exist_ok=True)

    return Chroma(
        collection_name="documentation",
        embedding_function=embedding_model,
        persist_directory=str(VECTOR_STORE_PATH),
    )


def add_documents(vector_store, chunks):
    if not chunks:
        return

    ids = [
        f"{document.metadata.get('source', 'document')}-{index}"
        for index, document in enumerate(chunks)
    ]

    vector_store.add_documents(chunks, ids=ids)


def retrieve_documents(vector_store, query, k=4):
    return vector_store.similarity_search(query, k=k)
