from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List
from constants.constant import CHUNK_OVERLAP,CHUNK_SIZE

def text_splitter(docs: List[Document]) -> List[Document]:
    """
    Splits a list of Document objects into smaller chunks using recursive character splitting.

    Uses LangChain's RecursiveCharacterTextSplitter to break each document into overlapping
    chunks of text for further processing such as embedding or retrieval.

    Args:
        docs (List[Document]): A list of LangChain Document objects to be split.

    Returns:
        List[Document]: A list of smaller Document chunks.

    Raises:
        None. Logs the exception and returns an empty list if an error occurs.
    """
    try:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        chunks = splitter.split_documents(docs)
        return chunks
    except Exception as e:
        print(f"[TextSplitter] Error splitting documents: {e}")
        return []
