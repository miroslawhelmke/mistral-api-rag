import os
import shutil

import streamlit as st

import utils.helpers as func
import utils.llama_index as llama_index
import utils.logs as logs


def tab_github_repo():
    github_url = st.text_input(
        "Enter GitHub Repository URL",
        placeholder="https://github.com/jerryjliu/llama_index",
    )

    branch = st.text_input(
        "Enter Branch Name (optional, defaults to main/master)", placeholder="main"
    )

    if st.button("Load Repository"):
        if github_url:
            try:
                if github_url.startswith("https://github.com/"):
                    parts = github_url.strip('/').split('/')
                    owner = parts[-2]
                    repo = parts[-1]
                else:
                     raise ValueError("Invalid GitHub URL format")
            except Exception as e:
                st.error(f"Invalid GitHub URL format: {e}")
                owner, repo = None, None
            
            if owner and repo:
                with st.spinner("Loading repository content..."):
                    try:
                        st.warning("GitHub loading logic needs implementation (fetch_github_repo_content)")
                        documents = []

                        if documents:
                            st.session_state["documents"] = documents
                            st.toast(f"Repository '{repo}' loaded successfully!", icon="✅")

                            st.warning("GitHub indexing logic needs implementation (create_index_from_github)")
                            index = None

                            if index:
                                st.session_state["index"] = index
                                st.session_state["query_engine"] = llama_index.create_query_engine(index)
                                st.success("Repository indexed and ready for querying!")
                            else:
                                st.error("Failed to create index from GitHub repository.")
                        else:
                            st.warning("No documents found in the repository or failed to load.")
                    except Exception as e:
                        st.error(f"Failed to load or index repository: {e}")
                        logs.log.error(f"GitHub processing error: {e}")
        else:
            st.warning("Please enter a GitHub Repository URL.")

    if "documents" in st.session_state and st.session_state["documents"]:
        st.write(f"Loaded {len(st.session_state['documents'])} documents from the repository.")
    if "query_engine" in st.session_state:
        st.write("Query engine is ready.")
