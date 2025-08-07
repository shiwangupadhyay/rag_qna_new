from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.embeddings.base import Embeddings
from typing import List

def create_faiss_index(chunks: List[Document], embedding_fn: Embeddings):
    """
    Creates a temporary, in-memory FAISS index from document chunks.

    This function takes a list of document chunks and an embedding function,
    and creates a FAISS vector store directly in memory. This index is
    temporary and will be discarded after the request is complete.

    Args:
        chunks (List[Document]): The list of document chunks to be indexed.
        embedding_fn (Embeddings): The embedding function to use for creating vectors.

    Returns:
        FAISS | None: A FAISS vector store instance, or None if an error occurs.
    """
    try:
        print("Creating in-memory FAISS index...")
        # FAISS.from_documents handles embedding the chunks and building the index
        vector_store = FAISS.from_documents(chunks, embedding_fn)
        print("FAISS index created successfully.")
        return vector_store
    except Exception as e:
        print(f"[FAISS] Error occurred while creating the index: {e}")
        return None