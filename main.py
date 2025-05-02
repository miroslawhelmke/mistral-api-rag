import time

import streamlit as st

from components.chatbox import chatbox
from components.header import set_page_header
# Import the sidebar module directly
import components.sidebar 
# from components.sidebar import sidebar # Original import

from components.page_config import set_page_config
from components.page_state import set_initial_state
import utils.mistral as mistral

### Configure LlamaIndex Global Settings with Mistral
mistral.configure_global_settings()

def generate_welcome_message(msg):
    for char in msg:
        time.sleep(0.025)  # This is blocking :(
        yield char


### Page Setup
set_page_config()
set_page_header()

### Setup Initial State
set_initial_state()

# st.write("--- Debug: Displaying History ---") # Remove Debug
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])
    # st.chat_message(msg["role"]).write_stream(generate_welcome_message(msg['content']))
# st.write(f"--- Debug: Current Messages State ({len(st.session_state['messages'])} items) ---") # Remove Debug
# st.write(st.session_state["messages"]) # Remove Debug

### Sidebar
# Call the function using the module name
components.sidebar.sidebar()

### Chat Box
chatbox()
