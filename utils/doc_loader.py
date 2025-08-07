import os
import tempfile
import requests
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import PyMuPDFLoader
from urllib.parse import urlparse

def sanitize_filename_from_url(url: str) -> str:
    """Extract a safe filename from a URL (strip query params)."""
    parsed = urlparse(url)
    return os.path.basename(parsed.path)

def doc_loader(url: str) -> List[Document]:
    """
    Download a PDF from a URL and load it using PyMuPDFLoader.

    Args:
        url (str): PDF file URL.

    Returns:
        List[Document]: Pages of the PDF as Document objects.
    """
    try:
        # Download the file to a temporary directory
        response = requests.get(url)
        response.raise_for_status()

        filename = sanitize_filename_from_url(url)
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = os.path.join(temp_dir, filename)
            with open(temp_path, "wb") as f:
                f.write(response.content)

            # Load using PyMuPDF
            loader = PyMuPDFLoader(temp_path)
            docs = loader.load()
            return docs

    except Exception as e:
        print(f"[doc_loader] Failed to load document from URL: {url} | Error: {e}")
        return []
