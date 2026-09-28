from typing import Any, TypedDict


class InvestigatorState(TypedDict, total=False):
    question: str
    documents: list[Any]
    answer: str
    relevant: bool
    rewrite_count: int
    max_rewrites: int
    vector_store: Any
    top_k: int
