from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

from app.config import MODEL_NAME

load_dotenv()


class GradeResult(BaseModel):
    relevant: bool = Field(
        description="Whether the retrieved documents contain enough information to answer the question."
    )


def create_grader():
    return ChatGoogleGenerativeAI(model=MODEL_NAME).with_structured_output(
        GradeResult
    )


def grade_documents(question, documents):
    if not documents:
        return False

    grader = create_grader()

    document_text = "\n\n".join(
        document.page_content for document in documents
    )

    prompt = f"""
You are a relevance grader for a technical documentation retrieval system.

Determine whether the retrieved documentation contains enough relevant
information to help answer the user's question.

User question:
{question}

Retrieved documentation:
{document_text}

Return relevant=true only when the documentation contains useful information
that directly helps answer the question.
Return relevant=false when it is unrelated or insufficient.
"""

    result = grader.invoke(prompt)
    return result.relevant
