from app.graph.state import InvestigatorState
from app.llm.generator import generate_answer
from app.llm.grader import grade_documents
from app.llm.rewriter import rewrite_query
from app.retrieval.vector_store import retrieve_documents


def retrieve_node(state: InvestigatorState) -> InvestigatorState:
    vector_store = state["vector_store"]
    question = state["question"]
    top_k = state.get("top_k", 4)

    documents = retrieve_documents(vector_store, question, k=top_k)

    return {
        "documents": documents,
    }


def grade_node(state: InvestigatorState) -> InvestigatorState:
    relevant = grade_documents(
        state["question"],
        state.get("documents", []),
    )

    return {
        "relevant": relevant,
    }


def rewrite_node(state: InvestigatorState) -> InvestigatorState:
    documents = state.get("documents", [])

    rewritten_question = rewrite_query(
        state["question"],
        documents,
    )

    return {
        "question": rewritten_question,
        "rewrite_count": state.get("rewrite_count", 0) + 1,
    }


def generate_node(state: InvestigatorState) -> InvestigatorState:
    answer = generate_answer(
        state["question"],
        state.get("documents", []),
    )

    return {
        "answer": answer,
    }


def route_after_grade(state: InvestigatorState) -> str:
    if state.get("relevant", False):
        return "generate"

    if state.get("rewrite_count", 0) >= state.get("max_rewrites", 2):
        return "generate"

    return "rewrite"
