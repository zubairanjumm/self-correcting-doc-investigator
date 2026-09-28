from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import MODEL_NAME

load_dotenv()


def create_generator():
    return ChatGoogleGenerativeAI(model=MODEL_NAME)


def generate_answer(question, documents):
    generator = create_generator()

    if documents:
        document_text = "\n\n".join(
            document.page_content for document in documents
        )
    else:
        document_text = "(No relevant documentation was retrieved.)"

    prompt = f"""
You are a technical documentation assistant.

Answer the user's question using only the provided documentation.

If the documentation does not contain enough information to answer the
question, say that the available documentation is insufficient. Do not
invent facts or fill gaps from general knowledge.

User question:
{question}

Documentation:
{document_text}

Give a concise, factual answer.
"""

    response = generator.invoke(prompt)
    return response.content.strip()
