import os
import tempfile
from typing import List

import streamlit as st

import utils.logs as logs

# This import might not be strictly necessary if OPENAI_API_KEY is set elsewhere
# but keeping it for now based on original comment. Should be set via secrets ideally.
# os.environ["OPENAI_API_KEY"] = "sk-abc123" 

from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    # ServiceContext, # ServiceContext is deprecated, use Settings
    # set_global_service_context, # Use Settings instead
    Settings, # Import Settings
    StorageContext, # Needed for vector store persistence
    load_index_from_storage, # To load existing index
    Document # For type hinting
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb # Required by ChromaVectorStore

# Placeholder for where ChromaDB data will be stored
PERSIST_DIR = "./chroma_db" 

###################################
#
# Load Data from Uploaded Files
#
###################################
@st.cache_data(show_spinner="Loading files...")
def load_data(uploaded_files: List[st.runtime.uploaded_file_manager.UploadedFile]) -> List[Document]:
    """Loads data from Streamlit uploaded files into LlamaIndex Documents."""
    documents = []
    with tempfile.TemporaryDirectory() as temp_dir:
        for uploaded_file in uploaded_files:
            file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            logs.log.info(f"Loading document: {uploaded_file.name}")
        
        # Use SimpleDirectoryReader on the temporary directory
        reader = SimpleDirectoryReader(input_dir=temp_dir)
        try:
            documents = reader.load_data()
            logs.log.info(f"Loaded {len(documents)} documents successfully.")
        except Exception as e:
            logs.log.error(f"Error loading documents from temp directory: {e}")
            st.error(f"Failed to load documents: {e}")
            return [] # Return empty list on error
    return documents

###################################
#
# Chunk Data (Node Parsing)
#
###################################
@st.cache_data(show_spinner="Chunking documents...")
# Prefix 'documents' with an underscore to prevent hashing
def chunk_data(_documents: List[Document], chunk_size: int = None, chunk_overlap: int = None) -> List:
    """Chunks LlamaIndex Documents into Nodes using SentenceSplitter."""
    # Use chunk settings from session state or fallback to Settings defaults
    chunk_size = chunk_size or st.session_state.get("chunk_size", Settings.chunk_size)
    chunk_overlap = chunk_overlap or st.session_state.get("chunk_overlap", Settings.chunk_overlap)
    
    # Use the prefixed argument name here
    logs.log.info(f"Chunking {len(_documents)} documents with chunk_size={chunk_size}, chunk_overlap={chunk_overlap}")
    try:
        node_parser = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        # Use the prefixed argument name here
        nodes = node_parser.get_nodes_from_documents(_documents)
        logs.log.info(f"Created {len(nodes)} nodes.")
        return nodes
    except Exception as e:
        logs.log.error(f"Error chunking documents: {e}")
        st.error(f"Failed to chunk documents: {e}")
        return []

###################################
#
# Initialize Vector Store (Chroma)
#
###################################
@st.cache_resource(show_spinner="Initializing vector store...")
def index_data() -> ChromaVectorStore:
    """Initializes a ChromaDB vector store."""
    logs.log.info(f"Initializing ChromaDB vector store at: {PERSIST_DIR}")
    # Ensure the persistence directory exists
    os.makedirs(PERSIST_DIR, exist_ok=True)
    try:
        db = chromadb.PersistentClient(path=PERSIST_DIR)
        chroma_collection = db.get_or_create_collection("local_rag_collection") # Use a consistent collection name
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        logs.log.info("ChromaDB vector store initialized successfully.")
        return vector_store
    except Exception as e:
        logs.log.error(f"Error initializing ChromaDB: {e}")
        st.error(f"Failed to initialize vector database: {e}")
        st.stop() # Stop if DB connection fails

###################################
#
# Embed & Index Nodes
#
###################################
@st.cache_resource(show_spinner="Embedding and indexing data...")
# Prefix 'nodes' with an underscore to prevent hashing
def embed_data(_vector_store: ChromaVectorStore, _nodes: List) -> VectorStoreIndex:
    """Embeds nodes and creates a new VectorStoreIndex."""
    # Use the prefixed argument name here
    logs.log.info(f"Embedding {len(_nodes)} nodes and creating new index.")
    try:
        # Storage context to persist the index using the vector store
        storage_context = StorageContext.from_defaults(vector_store=_vector_store)
        
        # Create the index. Embedding model is taken from global Settings.embed_model
        index = VectorStoreIndex(
            _nodes, # Use the prefixed argument name here
            storage_context=storage_context,
            # embed_model=Settings.embed_model is used by default
            # service_context=Settings is used by default
            show_progress=True 
        )
        logs.log.info("Index created successfully.")
        return index
    except Exception as e:
        logs.log.error(f"Error embedding data and creating index: {e}")
        st.error(f"Failed to create index: {e}")
        return None # Return None on failure

###################################
#
# Upsert Data into Existing Index
#
###################################
# Note: Direct upsert might depend on the specific vector store implementation.
# For Chroma, we might need to load the index first or add nodes directly.
# This implementation assumes we reload the index and let LlamaIndex handle insertion.
# A more efficient approach might add nodes directly to the vector_store if supported well.
@st.cache_resource(show_spinner="Updating index...")
def upsert_data(nodes: List) -> VectorStoreIndex:
    """'Upserts' data by loading the existing index and inserting new nodes."""
    logs.log.info(f"Upserting {len(nodes)} new nodes into existing index.")
    try:
        # Load the vector store (assuming it was initialized and stored in session state)
        vector_store = st.session_state.get("vector_store")
        if not vector_store:
             logs.log.error("Vector store not found in session state for upsert.")
             st.error("Vector store not available. Please process initial documents first.")
             return None

        storage_context = StorageContext.from_defaults(vector_store=vector_store, persist_dir=PERSIST_DIR)
        
        # Load the index from storage. This ensures we use the existing embeddings.
        # Service context (including embed_model) is implicitly loaded via Settings
        index = load_index_from_storage(storage_context) 
                                        # service_context=Settings is used by default
        
        # Insert new nodes
        index.insert_nodes(nodes, show_progress=True)
        
        # Persist changes (optional depending on vector store auto-persistence)
        index.storage_context.persist(persist_dir=PERSIST_DIR) 
        logs.log.info("Index updated successfully.")
        return index
    except Exception as e:
        logs.log.error(f"Error upserting data: {e}")
        st.error(f"Failed to update index: {e}")
        return None

###################################
#
# View Data (Placeholder/Example)
#
###################################
# This function seems UI related, might belong in the tab itself or a UI helper
def view_data():
    """Placeholder function to potentially display info about indexed data."""
    if "index" in st.session_state and st.session_state["index"]:
        st.success("Data is indexed and ready.")
        # You could add more details here, like number of documents/nodes indexed.
        # Accessing underlying vector store info might be complex/store-specific.
    else:
        st.info("Upload and process documents or load a repository to start.")


###################################
#
# Create Service Context (DEPRECATED - Use Global Settings)
#
###################################
# Keeping the old function commented out for reference
# @st.cache_resource(show_spinner=False)
# def create_service_context(...):
#    ... (old implementation) ...

###################################
#
# Load Documents (Old version - replaced by load_data for UploadedFile)
#
###################################
# @st.cache_resource(show_spinner=False)
# def load_documents(data_dir: str):
#    ... (old implementation using SimpleDirectoryReader on a dir) ...

###################################
#
# Create Query Engine (Still potentially useful, but uses global Settings now)
#
###################################
@st.cache_resource(show_spinner=False)
def create_query_engine(_index: VectorStoreIndex): # Takes index as input
    """ Creates a query engine from the given index, using global Settings. """
    if not _index:
        logs.log.error("Cannot create query engine from None index.")
        st.error("Index is not available. Cannot create query engine.")
        return None
    logs.log.info("Creating query engine...")
    try:
        # LLM and Embed Model are picked from global Settings automatically
        query_engine = _index.as_query_engine(
            # similarity_top_k=st.session_state.get("top_k", 3), # Example if top_k is needed
            # service_context=Settings is used by default
            streaming=True, 
        )
        logs.log.info("Query engine created successfully.")
        st.session_state["query_engine"] = query_engine # Store in session state
        return query_engine
    except Exception as e:
        logs.log.error(f"Error when creating Query Engine: {e}")
        st.error(f"Failed to create query engine: {e}")
        return None
