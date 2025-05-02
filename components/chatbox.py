import streamlit as st
from llama_index.core import Settings
import utils.logs as logs


def chatbox():
    # Check if a query engine exists (meaning data is loaded)
    query_engine = st.session_state.get("query_engine")
    is_disabled = query_engine is None
    placeholder_text = "Please upload and process documents first..." if is_disabled else "How can I help?"

    # Disable chat input if no query engine exists
    if prompt := st.chat_input(placeholder_text, disabled=is_disabled):
        
        # Double-check query engine just in case (though input should be disabled)
        if not query_engine:
            st.warning("Please process documents before chatting.")
            st.stop()

        # Add the user input to messages state
        st.session_state["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response stream
        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                # Always use query engine here since input is disabled otherwise
                try:
                    stream = query_engine.query(prompt) # Query engine uses global Settings
                    response = st.write_stream(stream.response_gen)
                except Exception as e:
                    logs.log.error(f"Error during context chat: {e}")
                    st.error(f"An error occurred: {e}")
                    response = "Sorry, I encountered an error processing your request with context."
                    st.write(response)
                # Removed the 'else' block for non-context chat as it's unreachable if input is disabled correctly

        # Add the final response to messages state
        st.session_state["messages"].append({"role": "assistant", "content": response})
