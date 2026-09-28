from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import MODEL_NAME

load_dotenv()


def create_rewriter():
    return ChatGoogleGenerativeAI(model=MODEL_NAME)


def rewrite_query(question, documents):
    rewriter = create_rewriter()

    document_text = "\n\n".join(
        document.page_content for document in documents
    ) if documents else "(No useful documentation was retrieved.)"

    prompt = f"""
You are a technical documentation search query rewriter.

The original user question did not retrieve useful enough documentation.

Rewrite the question into a clearer and more specific search query that
preserves the user's original intent and improves retrieval.

Original question:
{question}

Previously retrieved documentation:
{document_text}

Return only the rewritten search query. Do not add explanations, quotes,
labels, or markdown.
"""

    response = rewriter.invoke(prompt)
    rewritten = response.content.strip()

    if not rewritten:
        return question

    return rewritten
