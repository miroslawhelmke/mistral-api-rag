import streamlit as st

import utils.logs as logs


def set_initial_state():
    """Sets the initial state variables for the application."""
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
        st.session_state["messages"].append(
            {"role": "assistant", "content": "How can I help you?"}
        )

    # Remove Ollama Endpoint State
    # if "ollama_endpoint" not in st.session_state:
    #     st.session_state["ollama_endpoint"] = "http://localhost:11434"

    # Initialize query engine
    if "query_engine" not in st.session_state:
        st.session_state["query_engine"] = None

    # Remove Ollama Models State
    # if "ollama_models" not in st.session_state:
    #     try:
    #         models = get_models()
    #         st.session_state["ollama_models"] = models
    #     except Exception as err:
    #         logs.log.warning(
    #             f"Warning: Initial loading of Ollama models failed. You might be hosting Ollama somewhere other than localhost. -- {err}"
    #         )
    #         st.session_state["ollama_models"] = []

    # Remove Selected Model State
    # if "selected_model" not in st.session_state:
    #     if st.session_state["ollama_models"]:
    #         st.session_state["selected_model"] = st.session_state["ollama_models"][0]
    #     else:
    #         st.session_state["selected_model"] = None # Or handle the case where no models are loaded

    # Initialize system prompt
    if "system_prompt" not in st.session_state:
        st.session_state["system_prompt"] = (
            "You are a helpful AI assistant. Use the documents provided to answer questions. Provide citations to the source documents."
        )

    # Initialize chunk size
    if "chunk_size" not in st.session_state:
        st.session_state["chunk_size"] = 512

    # Initialize chunk overlap
    if "chunk_overlap" not in st.session_state:
        st.session_state["chunk_overlap"] = 20

    # Initialize embedding model (removed specific selection, using global Mistral)
    if "embedding_model" not in st.session_state:
        st.session_state["embedding_model"] = "mistral-embed" # Indicate global default

    # Removed other_embedding_model state
    # if "other_embedding_model" not in st.session_state:
    #     st.session_state["other_embedding_model"] = "BAAI/bge-large-en-v1.5"

    # Initialize vector store
    if "vector_store" not in st.session_state:
        st.session_state["vector_store"] = None

    # Initialize index
    if "index" not in st.session_state:
        st.session_state["index"] = None

    # Initialize documents (optional, based on workflow)
    if "documents" not in st.session_state:
        st.session_state["documents"] = None

    # Add other initial state variables as needed
    # Example:
    # if "advanced" not in st.session_state:
    #     st.session_state["advanced"] = False
