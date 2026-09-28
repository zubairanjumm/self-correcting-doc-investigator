import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
    
import streamlit as st

from app.config import DEFAULT_DOCS_PATH, MAX_REWRITES
from app.main import investigate


st.set_page_config(
    page_title="Documentation Investigator",
    page_icon="🔎",
    layout="centered",
)


st.title("Documentation Investigator")

st.write(
    "Ask a question about your documentation. "
    "The system retrieves relevant documents and can rewrite "
    "the search query when the first retrieval is not useful."
)


st.divider()


question = st.text_area(
    "Your question",
    placeholder="How do I configure authentication?",
    height=120,
)


docs_path = st.text_input(
    "Documentation folder",
    value=str(DEFAULT_DOCS_PATH),
)


max_rewrites = st.slider(
    "Maximum query rewrites",
    min_value=0,
    max_value=5,
    value=MAX_REWRITES,
)


if st.button("Investigate", type="primary"):

    if not question.strip():
        st.warning("Please enter a question.")
        st.stop()

    try:
        with st.spinner("Investigating documentation..."):

            result = investigate(
                question=question.strip(),
                docs_path=Path(docs_path),
                max_rewrites=max_rewrites,
            )

        st.success("Investigation complete")

        st.subheader("Answer")

        st.write(result["answer"])

        st.divider()

        st.subheader("Investigation details")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Query rewrites",
                result.get("rewrite_count", 0),
            )

        with col2:
            relevant = result.get("relevant", False)

            st.metric(
                "Relevant documents",
                "Yes" if relevant else "No",
            )

        documents = result.get("documents", [])

        if documents:
            st.subheader("Retrieved documentation")

            for index, document in enumerate(documents, start=1):

                source = document.metadata.get(
                    "source",
                    "Unknown source",
                )

                with st.expander(f"Document {index}: {source}"):
                    st.write(document.page_content)

    except Exception as exc:
        st.error("The investigation failed.")
        st.exception(exc)