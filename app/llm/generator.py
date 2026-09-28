from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def create_generator():
    return ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
    )


def generate_answer(question, documents):
    generator = create_generator()

    document_text = "\n\n".join(
        document.page_content for document in documents
    )

    prompt = f"""
You are a technical documentation assistant.

Answer the user's question using only the provided documentation.

If the documentation does not contain enough information to answer the
question, clearly say that the available documentation is insufficient.

User question:
{question}

Documentation:
{document_text}

Give a concise, factual answer.
"""

    response = generator.invoke(prompt)

    return response.content