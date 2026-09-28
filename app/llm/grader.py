from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

class GradeResult(BaseModel):
    relevant: bool = Field(
        description="Whether the retrieved documents are relevant to answering the question."
    )


def create_grader():
    return ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
    ).with_structured_output(GradeResult)


def grade_documents(question, documents):
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

Return relevant=true if the documentation is relevant to the question.
Return relevant=false if it is unrelated or does not contain useful information.
"""

    result = grader.invoke(prompt)

    return result.relevant