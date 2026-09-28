from langgraph.graph import END, START, StateGraph

from app.graph.nodes import (
    generate_node,
    grade_node,
    retrieve_node,
    rewrite_node,
)
from app.graph.state import InvestigatorState


def build_workflow():
    graph = StateGraph(InvestigatorState)

    graph.add_node("retrieve", retrieve_node)
    graph.add_node("grade", grade_node)
    graph.add_node("rewrite", rewrite_node)
    graph.add_node("generate", generate_node)

    graph.add_edge(START, "retrieve")
    graph.add_edge("retrieve", "grade")

    graph.add_conditional_edges(
        "grade",
        lambda state: "generate"
        if state.get("relevant", False)
        else (
            "generate"
            if state.get("rewrite_count", 0) >= state.get("max_rewrites", 2)
            else "rewrite"
        ),
        {
            "generate": "generate",
            "rewrite": "rewrite",
        },
    )

    graph.add_edge("rewrite", "retrieve")
    graph.add_edge("generate", END)

    return graph.compile()
