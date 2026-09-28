from pathlib import Path

from langchain_chroma import Chroma


VECTOR_STORE_PATH = Path("data/chroma")


def create_vector_store(embedding_model):
    vector_store = Chroma(
        collection_name="documentation",
        embedding_function=embedding_model,
        persist_directory=str(VECTOR_STORE_PATH),
    )

    return vector_store


def add_documents(vector_store, chunks):
    vector_store.add_documents(chunks)