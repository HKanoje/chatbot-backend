# RAG Chatbot Backend

This is the backend for a RAG (Retrieval-Augmented Generation) chatbot. It uses Google Gemini for language modeling and Qdrant for the vector store. The application is built with FastAPI.

## Features

- **Chat with AI:** Engage in conversations with a powerful AI assistant.
- **Document Upload:** Upload various document types (PDF, Excel, Text, Images) to provide context for the chatbot.
- **RAG Pipeline:** The backend processes uploaded documents, chunks them, generates embeddings using Google Gemini, and stores them in a Qdrant vector database.
- **Contextual Responses:** When you chat, the backend searches for relevant information in the uploaded documents to provide more accurate and context-aware responses.
- **API Endpoints:** A comprehensive set of API endpoints for chat, document management, and health checks.
- **Easy Deployment:** Includes a `render.yaml` file for easy deployment on Render.

## Live Demo

- **Frontend:** [https://chatbot-frontend-one-ashy.vercel.app/](https://chatbot-frontend-one-ashy.vercel.app/)
- **Backend:** [https://chatbot-backend-l9sy.onrender.com/](https://chatbot-backend-l9sy.onrender.com/)

## Technologies Used

- **Backend Framework:** FastAPI
- **Language Model:** Google Gemini
- **Vector Store:** Qdrant
- **Document Processing:**
  - PyPDF2 (for PDFs)
  - openpyxl, pandas (for Excel)
  - Pillow, pytesseract (for Images/OCR)
- **Configuration:** pydantic-settings
- **Server:** Uvicorn

## Getting Started

### Prerequisites

- Python 3.11+
- An account with [Google AI Studio](https://aistudio.google.com/) to get a Gemini API key.
- An account with [Qdrant Cloud](https://qdrant.tech/cloud/) to get a Qdrant URL and API key.
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed on your system for image processing.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/chatbot-backend.git
    cd chatbot-backend
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create a `.env` file** in the root of the project and add the following environment variables:
    ```env
    GEMINI_API_KEY="your_gemini_api_key"
    QDRANT_URL="your_qdrant_url"
    QDRANT_API_KEY="your_qdrant_api_key"
    ```

### Running the Application

To run the application locally, use the following command:

```bash
python run.py
```

The application will be available at `http://localhost:8000`.

## API Endpoints

The API documentation is available at `http://localhost:8000/docs` when the application is running.

- `GET /`: Root endpoint with a welcome message.
- `GET /health`: Health check.
- `GET /info`: API information.
- `POST /api/v1/chat`: Send a chat message.
- `POST /api/v1/upload`: Upload a document.
- `POST /api/v1/chat-with-file`: Upload a file and ask a question about it in one request.
- `GET /api/v1/stats`: Get statistics about the vector store.

## Project Structure

The project is organized as follows:

```
├── app/                  # Main application folder
│   ├── api/              # API endpoints and routes
│   ├── core/             # Core logic (RAG engine, LLM client, etc.)
│   ├── models/           # Pydantic models
│   ├── services/         # Business logic
│   ├── utils/            # Utility functions
│   ├── config.py         # Application configuration
│   └── main.py           # FastAPI application entry point
├── data/                 # Data files
├── logs/                 # Log files
├── tests/                # Test files
├── uploads/              # Uploaded files
├── .env                  # Environment variables
├── requirements.txt      # Python dependencies
└── run.py                # Script to run the application
```

## Configuration

The application is configured using environment variables. The following variables can be set in the `.env` file:

| Variable                | Description                               | Default                  |
| ----------------------- | ----------------------------------------- | ------------------------ |
| `APP_NAME`              | The name of the application.              | "RAG Chatbot API"        |
| `APP_VERSION`           | The version of the application.           | "1.0.0"                  |
| `DEBUG`                 | Enable/disable debug mode.                | `True`                   |
| `HOST`                  | The host to bind to.                      | "0.0.0.0"                |
| `PORT`                  | The port to listen on.                    | 8000                     |
| `ALLOWED_ORIGINS`       | Comma-separated list of allowed origins.  | "http://localhost:5173"  |
| `GEMINI_API_KEY`        | Your Google Gemini API key.               |                          |
| `GEMINI_MODEL`          | The Gemini model to use.                  | "gemini-2.5-flash"       |
| `GEMINI_EMBEDDING_MODEL`| The Gemini embedding model to use.        | "models/gemini-embedding-001"   |
| `QDRANT_URL`            | The URL of your Qdrant instance.          |                          |
| `QDRANT_API_KEY`        | Your Qdrant API key.                      |                          |
| `QDRANT_COLLECTION_NAME`| The name of the Qdrant collection.        | "RAG-ChatBot"            |
| `MAX_FILE_SIZE_MB`      | The maximum file size for uploads in MB.  | 10                       |
| `ALLOWED_FILE_TYPES`    | Comma-separated list of allowed file types.| "pdf,xlsx,xls,txt,png,jpg,jpeg" |
| `UPLOAD_DIR`            | The directory to store uploaded files.    | "uploads"                |
| `EMBEDDING_DIMENSION`   | The dimension of the embeddings.          | 3072                     |
| `TOP_K_RESULTS`         | The number of results to return from search.| 5                        |
| `LOG_LEVEL`             | The log level.                            | "INFO"                   |
| `LOG_FILE`              | The path to the log file.                 | "logs/app.log"           |

## Deployment

This project is configured for deployment on Render. You can deploy it by creating a new Web Service on Render and pointing it to your fork of this repository. Render will automatically use the `render.yaml` file to configure the service.

## Testing

The `tests` directory contains basic tests for the API. To run the tests, you can use `pytest`:

```bash
pytest
```

You can also run the scripts individually:

```bash
python tests/test_api.py
python tests/test_chat.py
```
