from pathlib import Path

from langchain_core.documents import Document


def load_documents(path: Path) -> list[Document]:
    documents = []

    found_files = path.glob("*.md")

    for file in found_files:
        text = file.read_text(encoding="utf-8")

        document = Document(
            page_content=text,
            metadata={"source": file.name},
        )

        documents.append(document)

    return documents
