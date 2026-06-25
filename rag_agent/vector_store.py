from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_aws import BedrockEmbeddings
import config

# 1. Define the mock knowledge base containing facts and reference details
knowledge_base = [
    Document(
        page_content=(
            "Google Gemini is a family of highly capable multimodal AI models developed by Google. "
            "The latest generation includes gemini-3.1-flash, gemini-3.1-flash-lite, and gemini-3.1-pro. "
            "These models support text, image, audio, video, and code processing with a 1-million token context window."
        ),
        metadata={"source": "Gemini Fact Sheet"}
    ),
    Document(
        page_content=(
            "FAISS (Facebook AI Similarity Search) is a library for efficient similarity search and clustering "
            "of dense vectors. It contains algorithms that search in sets of vectors of any size, up to ones that "
            "possibly do not fit in RAM. It is widely used in vector databases and semantic search systems."
        ),
        metadata={"source": "FAISS Documentation"}
    ),
    Document(
        page_content=(
            "LangChain is an open-source framework designed to simplify the creation of applications "
            "using large language models (LLMs). It provides components like prompt templates, models, "
            "output parsers, vectorstores, and agents that can be composed to build complex applications."
        ),
        metadata={"source": "LangChain Overview"}
    ),
    Document(
        page_content=(
            "Retrieval-Augmented Generation (RAG) is a technique that enhances LLMs by retrieving relevant "
            "information from an external data source (like a vector database) and injecting it into the prompt. "
            "This helps reduce model hallucinations, provides up-to-date information, and leverages proprietary data."
        ),
        metadata={"source": "RAG Architecture Guide"}
    )
]

# 2. Lazy-loaded vector store instance
_vector_store = None

def get_vector_store():
    """Initializes and retrieves the shared in-memory FAISS vector database."""
    global _vector_store
    if _vector_store is None:
        # Initialize Bedrock Titan Embeddings in the configured region
        embeddings = BedrockEmbeddings(
            model_id=config.EMBEDDING_MODEL_ID,
            region_name=config.AWS_REGION
        )
        # Load the knowledge base into FAISS
        _vector_store = FAISS.from_documents(knowledge_base, embeddings)
    return _vector_store

def query_vector_store(query: str, k: int = 2):
    """Performs semantic similarity search against the vector database."""
    db = get_vector_store()
    return db.similarity_search(query, k=k)
