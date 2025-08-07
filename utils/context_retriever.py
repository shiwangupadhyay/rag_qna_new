from typing import List
from langchain_core.vectorstores import VectorStore
from langchain_core.documents import Document

def get_contexts_from_questions(
    questions: List[str],
    vector_store: VectorStore,
    k: int = 1
) -> List[str]:
    """
    Retrieves relevant context for each question from a vector store.

    For each question, it performs a similarity search and aggregates the
    text content of the retrieved documents into a single context string.

    Args:
        questions (List[str]): List of questions as strings.
        vector_store (VectorStore): Initialized vector store to perform similarity search.
        k (int): Number of similar documents to retrieve for each question.

    Returns:
        List[str]: A list where each element is a string of combined context
                   relevant to the corresponding question.
    """
    contexts = []

    for q in questions:
        try:
            docs: List[Document] = vector_store.similarity_search(q, k=k)

            if docs:
                context_string = " ".join([doc.page_content for doc in docs])
                contexts.append(context_string)
            else:
                contexts.append("No relevant context found.")
        except Exception as e:
            print(f"[Context Retrieval] Error retrieving context for question: '{q}': {e}")
            contexts.append("Error retrieving context.")

    return contexts