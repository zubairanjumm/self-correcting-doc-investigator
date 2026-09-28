from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def create_rewriter():
    return ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
    )


def rewrite_query(question, documents):
    rewriter = create_rewriter()

    document_text = "\n\n".join(
        document.page_content for document in documents
    )

    prompt = f"""
You are a technical documentation search query rewriter.

The original user question did not retrieve useful enough documentation.

Rewrite the question into a clearer and more specific search query that
would help retrieve documentation relevant to the user's actual intent.

Original question:
{question}

Previously retrieved documentation:
{document_text}

Return only the rewritten search query.
"""

    response = rewriter.invoke(prompt)

    return response.content