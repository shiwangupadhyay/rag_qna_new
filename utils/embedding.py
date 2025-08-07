import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

def get_google_embeddings():
    """
    Initializes and returns a MistralAIEmbeddings instance using the model and API key 
    from environment variables.

    Returns:
        MistralAIEmbeddings: Embedding model instance.
    """
    try:
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001"
        )
        return embeddings
    except Exception as e:
        print(f"[Embedding] Failed to initialize Mistral embeddings: {e}")
        raise
