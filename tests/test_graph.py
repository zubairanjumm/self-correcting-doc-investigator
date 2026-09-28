from app.graph.nodes import route_after_grade
from app.graph.workflow import build_workflow


def test_route_to_generate_when_relevant():
    state = {
        "relevant": True,
        "rewrite_count": 0,
        "max_rewrites": 2,
    }

    assert route_after_grade(state) == "generate"


def test_route_to_rewrite_when_not_relevant_and_rewrites_remain():
    state = {
        "relevant": False,
        "rewrite_count": 0,
        "max_rewrites": 2,
    }

    assert route_after_grade(state) == "rewrite"


def test_route_to_generate_after_rewrite_limit():
    state = {
        "relevant": False,
        "rewrite_count": 2,
        "max_rewrites": 2,
    }

    assert route_after_grade(state) == "generate"


def test_workflow_compiles():
    workflow = build_workflow()

    assert workflow is not None
