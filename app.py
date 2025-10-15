import os
import sys
import traceback
import streamlit as st

# Ensure project root is on sys.path when running via Streamlit from nested dirs
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.graph.sqlgraph import sqlGraph
from src.sqlData.data import SQLData


@st.cache_resource(show_spinner=False)
def get_graph():
    """Build and cache the LangGraph once per app session."""
    builder = sqlGraph()
    return builder.workflow()


def init_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []  # list[tuple[user|assistant, text]]


def main():
    st.set_page_config(page_title="HR SQL Agent", page_icon="🧑‍💼", layout="centered")

    st.title("HR SQL Agent 🧑‍💼")
    st.caption("Ask questions about the resumes database. The agent will generate SQL, run it, and answer.")

    # API key hint (Groq)
    if not os.getenv("GROQ_API_KEY"):
        st.info(
            "Set environment variable GROQ_API_KEY before running for best results.\n"
            "Example (zsh): export GROQ_API_KEY=\"your_key\"",
            icon="🔑",
        )

    init_state()
    graph = get_graph()

    # Ensure the demo DB exists
    try:
        if not os.path.exists(os.path.join(ROOT_DIR, "resume.db")):
            SQLData().create_data()
    except Exception as db_e:
        st.warning(f"Could not verify/create database: {db_e}")

    with st.container():
        user_input = st.text_input(
            "Ask a question",
            placeholder="e.g., How many rows are there?",
            key="question_input",
        )
        col_send, col_clear = st.columns([1, 1])
        with col_send:
            send = st.button("Send", type="primary")
        with col_clear:
            clear = st.button("Clear")

    if clear:
        st.session_state.messages = []
        st.rerun()

    if send and user_input.strip():
        st.session_state.messages.append(("user", user_input.strip()))
        try:
            with st.spinner("Thinking..."):
                state = graph.invoke({"question": user_input.strip()})
            answer = state.get("answer") or "(No answer returned)"
            st.session_state.messages.append(("assistant", str(answer)))
        except Exception as e:
            st.error(f"Something went wrong: {e}")
            st.exception(e)
            traceback.print_exc()

    # Render history
    for role, text in st.session_state.messages:
        if role == "user":
            st.chat_message("user").write(text)
        else:
            st.chat_message("assistant").write(text)

    # Optional: show debug details for the last exchange
    if st.session_state.messages:
        if st.toggle("Show last run details (SQL + Result)"):
            try:
                # Re-run last question to show details without changing history
                last_q = next((m[1] for m in reversed(st.session_state.messages) if m[0] == "user"), None)
                if last_q:
                    state = graph.invoke({"question": last_q})
                    st.subheader("Generated SQL")
                    st.code(state.get("query", ""), language="sql")
                    st.subheader("Raw Result")
                    st.write(state.get("result", ""))
            except Exception as e:
                st.warning(f"Could not display details: {e}")


if __name__ == "__main__":
    main()
