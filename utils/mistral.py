import os
import streamlit as st
from llama_index.llms.mistralai import MistralAI
from llama_index.embeddings.mistralai import MistralAIEmbedding
from llama_index.core import Settings
import utils.logs as logs

# Define default models - check Mistral AI documentation for latest/recommended models
DEFAULT_MISTRAL_MODEL = "mistral-large-latest"
DEFAULT_MISTRAL_EMBEDDING = "mistral-embed"

def get_mistral_api_key():
    """Retrieves the Mistral API key from Streamlit secrets or environment variables."""
    api_key = st.secrets.get("MISTRAL_API_KEY", os.environ.get("MISTRAL_API_KEY"))
    if not api_key:
        logs.log.error("Mistral API key not found.")
        st.error("Mistral API key not found. Please set MISTRAL_API_KEY in your Streamlit secrets.")
        st.stop() # Stop execution if key is missing
    return api_key

@st.cache_resource(show_spinner=False)
def get_mistral_llm(model_name: str = DEFAULT_MISTRAL_MODEL) -> MistralAI:
    """Get a cached instance of the MistralAI LLM."""
    api_key = get_mistral_api_key()
    try:
        llm = MistralAI(model=model_name, api_key=api_key)
        logs.log.info(f"MistralAI LLM initialized with model: {model_name}")
        return llm
    except Exception as e:
        logs.log.error(f"Error creating Mistral LLM: {e}")
        st.error(f"Failed to initialize Mistral LLM: {e}")
        st.stop()

@st.cache_resource(show_spinner=False)
def get_mistral_embedding(model_name: str = DEFAULT_MISTRAL_EMBEDDING) -> MistralAIEmbedding:
    """Get a cached instance of the MistralAIEmbedding model."""
    api_key = get_mistral_api_key()
    try:
        embed_model = MistralAIEmbedding(model_name=model_name, api_key=api_key)
        logs.log.info(f"MistralAI Embedding model initialized with model: {model_name}")
        return embed_model
    except Exception as e:
        logs.log.error(f"Error creating Mistral Embedding model: {e}")
        st.error(f"Failed to initialize Mistral Embedding model: {e}")
        st.stop()

def configure_global_settings(llm_model: str = DEFAULT_MISTRAL_MODEL, embed_model: str = DEFAULT_MISTRAL_EMBEDDING):
    """Configures LlamaIndex global settings with Mistral models."""
    logs.log.info(f"Configuring global LlamaIndex settings with Mistral LLM: {llm_model} and Embedding: {embed_model}")
    try:
        Settings.llm = get_mistral_llm(model_name=llm_model)
        Settings.embed_model = get_mistral_embedding(model_name=embed_model)
        logs.log.info("LlamaIndex global settings configured successfully.")
        # Optional: Configure other settings like chunk size if needed
        # Settings.chunk_size = 512
        # Settings.chunk_overlap = 20
    except Exception as e:
        # Errors during initialization are already logged and handled in get_mistral_llm/get_mistral_embedding
        logs.log.error(f"Failed to configure global LlamaIndex settings: {e}")
        # No need to st.stop() here as it's already handled in the getter functions

# It's recommended to call configure_global_settings() early in your app initialization,
# e.g., at the beginning of main.py, after imports but before other components are loaded. 