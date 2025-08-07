from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional

from schema.schema import RunRequest
from constants.constant import EXPECTED_BEARER_TOKEN
from utils.doc_loader import doc_loader
from utils.text_splitter import text_splitter
from utils.embedding import get_google_embeddings
from utils.context_retriever import get_contexts_from_questions
from src.model import model
from src.prompt import prompt
from utils.faiss_utils import create_faiss_index

app = FastAPI()

@app.post("/hackrx/run")
async def run_hackrx(
    request: RunRequest,
    authorization: Optional[str] = Header(None)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = authorization.split(" ")[1]
    if token != EXPECTED_BEARER_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        docs = doc_loader(request.documents)

        chunks = text_splitter(docs)

        embedding_fn = get_google_embeddings()
        vector_store = create_faiss_index(chunks, embedding_fn)

        if not vector_store:
            raise HTTPException(status_code=500, detail="Failed to create in-memory vector store.")

        contexts = get_contexts_from_questions(request.questions, vector_store, k=3)

        model_pipe = prompt | model

        response = model_pipe.invoke({'retrieved_chunk': contexts,'questions_list': request.questions})

        
        return JSONResponse(content={'answers': response.answers},status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")