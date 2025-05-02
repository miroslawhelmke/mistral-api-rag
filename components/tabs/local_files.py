import os
import tempfile
import streamlit as st

import utils.logs as logs
# import utils.ollama as ollama # Remove ollama import
from utils.llama_index import (chunk_data, embed_data, index_data, load_data,
                           # read_data, save_data_to_session, update_data, # These seem less relevant now
                           upsert_data, view_data)


def tab_local_files():
    uploaded_file = st.file_uploader(
        "Upload a document",
        type=["pdf", "md", "txt"],  # Add supported file types
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    if uploaded_file:
        if st.button("Process Documents"):
            with st.spinner("Processing documents..."):
                # Initialize or load vector store
                if "vector_store" not in st.session_state or st.session_state["vector_store"] is None:
                    vector_store = index_data() # Initializes Chroma DB
                    st.session_state["vector_store"] = vector_store
                else:
                    vector_store = st.session_state["vector_store"]
                
                # Load data from uploaded files
                documents = load_data(uploaded_file)
                if not documents:
                    st.warning("No documents could be loaded. Please check file types and content.")
                    st.stop()
                
                # Chunk documents into nodes
                nodes = chunk_data(documents) # Uses chunk settings from session state/Settings
                if not nodes:
                    st.error("Failed to chunk documents.")
                    st.stop()

                # Embed and index or upsert data
                if "index" not in st.session_state or st.session_state["index"] is None:
                    # Create new index if it doesn't exist
                    index = embed_data(vector_store, nodes)
                    if index is None:
                        st.error("Failed to create index.")
                        st.stop()
                    st.session_state["index"] = index
                else:
                    # Upsert data into existing index
                    index = upsert_data(nodes)
                    if index is None:
                        st.error("Failed to update index.")
                        # Decide if we should stop or continue with the old index
                        index = st.session_state["index"] # Fallback to existing index
                    else:
                         st.session_state["index"] = index # Update session state with new index object

                # Create query engine from the index
                # This function now correctly takes the index object
                from utils.llama_index import create_query_engine 
                query_engine = create_query_engine(index)
                if query_engine:
                     st.session_state["query_engine"] = query_engine # This might be redundant if create_query_engine sets it
                     logs.log.info("Document Processing Completed")
                     st.toast(f"{len(uploaded_file)} documents processed successfully!", icon="✅")
                else:
                    st.error("Failed to create query engine after processing documents.")

    # Saved Documents View
    view_data() # Display status
