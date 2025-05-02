import streamlit as st

from components.tabs.local_files import tab_local_files
from components.tabs.github_repo import tab_github_repo
from components.tabs.website import website


def file_upload():
    st.title("Import your documents.")
    st.caption("Upload your documents to intelligently talk to them.")
    st.write("")

    with st.expander("💻 &nbsp; **Local Files**", expanded=True):
        tab_local_files()

  #  with st.expander("🗂️ &nbsp;**GitHub Repo**", expanded=False):
  #      tab_github_repo()

  #  with st.expander("🌐 &nbsp; **Website**", expanded=False):
  #      website()
