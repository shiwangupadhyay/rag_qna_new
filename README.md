# ✨ Intelligent Document Q&A API

**Empowering your applications with secure, AI-driven document insights.**

This project provides a robust and scalable FastAPI service that leverages Retrieval Augmented Generation (RAG) to answer questions based on the content of provided documents, secured by a Bearer Token authentication mechanism.

---

## 🚀 Project Structure

```
.
├── app.py
├── Dockerfile
├── LICENSE
├── README.md
├── requirements.txt
├── test.py
├── constants/
│   ├── constant.py
│   └── __init__.py
├── schema/
│   ├── schema.py
│   └── __init__.py
├── src/
│   ├── model.py
│   └── prompt.py
└── utils/
    ├── context_retriever.py
    ├── doc_loader.py
    ├── embedding.py
    ├── faiss_utils.py
    └── text_splitter.py
```

---

## 🌟 Key Features

*   **Retrieval Augmented Generation (RAG):** Intelligently answers questions by retrieving and synthesizing information directly from the provided document context.
*   **Dynamic Document Ingestion:** Supports loading and processing PDF documents from external URLs on the fly.
*   **Efficient Text Processing:** Utilizes recursive character splitting to break down documents into manageable, overlapping chunks.
*   **Google Gemini Integration:** Leverages Google's powerful Gemini models for generating high-quality embeddings and crafting precise answers.
*   **In-Memory FAISS Vector Store:** Employs FAISS for rapid, in-memory similarity searches, ensuring quick context retrieval.
*   **Secure API Endpoint:** Protects sensitive operations with mandatory Bearer Token authentication.
*   **Structured API Responses:** Ensures consistent and easily parsable JSON output for answers.
*   **Containerized Deployment:** Includes a `Dockerfile` for seamless building and deployment via Docker.

---

## 🛠️ Technologies Used

*   **Python 3.11**: The core programming language.
*   **FastAPI**: A modern, fast (high-performance) web framework for building APIs.
*   **Uvicorn**: An ASGI server, powering the FastAPI application.
*   **LangChain**: A framework for developing applications powered by language models, used for:
    *   Document loading (`PyMuPDFLoader`)
    *   Text splitting (`RecursiveCharacterTextSplitter`)
    *   Vector store integration (`FAISS`)
    *   LLM orchestration (`ChatGoogleGenerativeAI`, `PromptTemplate`)
*   **Google Generative AI**: Specifically `GoogleGenerativeAIEmbeddings` for text embeddings and `ChatGoogleGenerativeAI` for the LLM (Gemini 2.5 Flash).
*   **PyMuPDF**: For robust PDF document parsing and loading.
*   **FAISS (Facebook AI Similarity Search)**: For efficient similarity search and clustering of dense vectors.
*   **Pydantic**: For data validation and serialization, ensuring robust API request and response schemas.
*   **python-dotenv**: For managing environment variables securely.
*   **Docker**: For containerizing the application, facilitating consistent deployment.

---

## ⚙️ Installation

### Prerequisites

*   Python 3.11+
*   `pip` (Python package installer)
*   Docker (optional, for containerized deployment)
*   A Google API Key for accessing Gemini models.

### 1. Clone the Repository

```bash
git clone <repository_url> # Replace <repository_url> with the actual URL
cd <repository_name>
```

### 2. Environment Variables

Create a `.env` file in the root directory of the project and add the following:

```dotenv
GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
# This token is used for API authentication.
# You can find the default value in constants/constant.py
EXPECTED_BEARER_TOKEN="5669aef1cb6e11718a9ea91c23074b21b9234233bec8da60d0b71a28eebcdc5e"
```

Replace `YOUR_GOOGLE_API_KEY` with your actual Google API Key. The `EXPECTED_BEARER_TOKEN` should match the one defined in `constants/constant.py`.

### 3. Local Setup (without Docker)

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Docker Setup (Recommended for Deployment)

Build the Docker image:

```bash
docker build -t rag-qna-api .
```

Run the Docker container:

```bash
docker run -d -p 80:80 --name rag-qna-service -e GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY" rag-qna-api
# Ensure you pass your GOOGLE_API_KEY as an environment variable to the container.
# The EXPECTED_BEARER_TOKEN is already baked into the image from constants/constant.py
# but you could also override it with -e EXPECTED_BEARER_TOKEN="..."
```

The API will be accessible on `http://localhost:80`.

---

## 🚀 Usage

### Running the API Locally

After installing dependencies, you can run the FastAPI application:

```bash
uvicorn app:app --host 0.0.0.0 --port 80
```

The API will now be running on `http://0.0.0.0:80`.

### API Endpoints

The service exposes a single, powerful endpoint for document querying:

#### `POST /hackrx/run`

This endpoint processes a given document URL and a list of questions, returning answers based on the document's content.

*   **Method:** `POST`
*   **URL:** `http://localhost:80/hackrx/run` (or your deployed URL)
*   **Authentication:** Requires a Bearer Token in the `Authorization` header.
    *   **Header:** `Authorization: Bearer <YOUR_BEARER_TOKEN>`
    *   **Default Token (from `constants/constant.py`):** `5669aef1cb6e11718a9ea91c23074b21b9234233bec8da60d0b71a28eebcdc5e`
*   **Request Body (`application/json`):**

    ```json
    {
        "documents": "string (URL to a PDF document, e.g., 'https://example.com/policy.pdf')",
        "questions": [
            "string (question 1)",
            "string (question 2)",
            "..."
        ]
    }
    ```

*   **Response Body (`application/json`):**

    ```json
    {
        "answers": [
            "string (answer to question 1)",
            "string (answer to question 2)",
            "..."
        ]
    }
    ```
    *   If an answer cannot be found in the provided context, the response for that question will be: `"Not mentioned in the provided context."`

*   **Error Responses:**
    *   `401 Unauthorized`: If the `Authorization` header is missing, invalid, or the token is incorrect.
    *   `500 Internal Server Error`: For issues during document loading, vector store creation, or LLM processing.

### Example Request (Python)

You can use the provided `test.py` script as an example, or copy the snippet below:

```python
import requests

# API URL (change if deployed elsewhere)
url = "http://localhost:80/hackrx/run"

# Bearer token from constants/constant.py or your .env file
bearer_token = "5669aef1cb6e11718a9ea91c23074b21b9234233bec8da60d0b71a28eebcdc5e"

# Sample payload with a public PDF URL and questions
payload = {
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": [
        "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
        "What is the waiting period for pre-existing diseases (PED) to be covered?",
        "Does this policy cover maternity expenses, and what are the conditions?",
        "What is the waiting period for cataract surgery?",
        "Are the medical expenses for an organ donor covered under this policy?",
        "What is the No Claim Discount (NCD) offered in this policy?",
        "Is there a benefit for preventive health check-ups?",
        "How does the policy define a 'Hospital'?",
        "What is the extent of coverage for AYUSH treatments?",
        "Are there any sub-limits on room rent and ICU charges for Plan A?"
    ]
}

# Headers for authentication and content type
headers = {
    "Authorization": f"Bearer {bearer_token}",
    "Content-Type": "application/json"
}

# Make the POST request
response = requests.post(url, json=payload, headers=headers)

# Print the response
print(f"Status Code: {response.status_code}")
try:
    print("Response JSON:", response.json())
except Exception as e:
    print("Failed to parse JSON. Raw response:")
    print(response.text)
```

### Example Request (cURL)

```bash
curl -X POST "http://localhost:80/hackrx/run" \
     -H "Authorization: Bearer 5669aef1cb6e11718a9ea91c23074b21b9234233bec8da60d0b71a28eebcdc5e" \
     -H "Content-Type: application/json" \
     -d '{
           "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
           "questions": [
               "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
               "What is the waiting period for pre-existing diseases (PED) to be covered?"
           ]
         }'
```

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)