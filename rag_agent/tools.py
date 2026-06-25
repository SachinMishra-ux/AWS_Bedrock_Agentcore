from langchain.tools import tool
from vector_store import query_vector_store

@tool
def query_knowledge_base(query: str) -> str:
    """Queries the vector database knowledge base for information matching the search query and returns relevant documents."""
    try:
        results = query_vector_store(query, k=2)
        if not results:
            return f"No matching information found in the knowledge base for: '{query}'"
        
        output_str = f"Matching Documents found for '{query}':\n\n"
        for i, doc in enumerate(results, 1):
            output_str += f"Document {i}:\n"
            output_str += f"Content: {doc.page_content}\n"
            output_str += f"Source Metadata: {doc.metadata.get('source', 'Unknown')}\n\n"
        return output_str
    except Exception as e:
        return f"Error querying knowledge base: {str(e)}"
