import json

import streamlit as st

from datetime import datetime


def settings():
    st.header("Settings")
    st.caption("Configure Local RAG settings and integrations")

    st.subheader("LLM Configuration")
    st.info("The LLM (Mistral) and Embedding Model (Mistral) are configured globally using the `MISTRAL_API_KEY` from Streamlit secrets.")

    st.divider()

    st.subheader("Embedding Configuration")
    st.info("Using Mistral embedding model (`mistral-embed`) configured globally.")

    st.number_input(
        "Chunk Size",
        min_value=128,
        max_value=8192,
        value=512,
        step=128,
        key="chunk_size",
    )
    st.number_input(
        "Chunk Overlap",
        min_value=0,
        max_value=512,
        value=20,
        step=16,
        key="chunk_overlap",
    )

    st.divider()

    st.subheader("System Prompt")
    st.text_area(
        "System Prompt",
        key="system_prompt",
        value="You are a helpful AI assistant. Use the documents provided to answer questions. Provide citations to the source documents.",
        height=150,
    )

    st.subheader("Export Data")
    export_data_settings = st.container(border=True)
    with export_data_settings:
        st.write("Chat History")
        st.download_button(
            label="Download",
            data=json.dumps(st.session_state["messages"]),
            file_name=f"local-rag-chat-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.json",
            mime="application/json",
        )

    st.toggle("Advanced Settings", key="advanced")

    if st.session_state["advanced"] == True:
        with st.expander("Current Application State"):
            state = dict(sorted(st.session_state.items()))
            st.write(state)
