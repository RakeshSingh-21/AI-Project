# AI-Project

# 🦙 Llama FastAPI Chat Application

A FastAPI-based chatbot application that integrates a locally hosted GGUF Large Language Model (LLM) using **llama.cpp**. The application provides a browser-based chat interface, supports streaming responses, and stores chat history in a MySQL database using SQLAlchemy.

---

# Features

- FastAPI backend
- Local GGUF model inference using llama.cpp
- Interactive web-based chat UI
- Streaming AI responses
- SQLAlchemy ORM integration
- MySQL database support
- Session-based conversation history
- Jinja2 template rendering
- Static CSS support

---

# Project Structure

```
llama_fastapi/
│
├── app.py                  # Main FastAPI application
├── database.py             # Database connection
├── models.py               # SQLAlchemy models
│
├── templates/
│   ├── index.html
│   ├── index1.html
│   └── index2.html
│
├── static/
│   ├── style.css
│   └── style1.css
│
└── __pycache__/
```

---

# Technologies Used

- Python
- FastAPI
- llama.cpp
- SQLAlchemy
- MySQL
- Jinja2
- HTML
- CSS

---

# Prerequisites

Install Python 3.10+ and the following packages:

```bash
pip install fastapi
pip install uvicorn
pip install sqlalchemy
pip install pymysql
pip install jinja2
pip install llama-cpp-python
```

---

# Database Configuration

The project uses MySQL.

Current database configuration:

```python
DATABASE_URL = "mysql+pymysql://root:root@localhost/chatdb"
```

Create the database before running:

```sql
CREATE DATABASE chatdb;
```

Tables are automatically created using:

```python
Base.metadata.create_all(bind=engine)
```

---

# Model Configuration

The application uses a local GGUF model through llama.cpp.

Example:

```python
llm = Llama(
    model_path="D:/Local_Models/meta-llama-3-8b-instruct.Q4_K_M.gguf",
    n_ctx=2048,
    n_threads=4
)
```

Update the `model_path` according to your local system.

---

# Running the Application

Start the server:

```bash
uvicorn app:app --reload
```

Default URL:

```
http://127.0.0.1:8000
```

---

# API Endpoints

## Home Page

```
GET /
```

Loads the chat interface.

---

## Create New Session

```
GET /new-session
```

Returns a new unique session ID.

Example:

```json
{
    "session_id":"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

---

## Chat

```
POST /chat
```

Example Request

```json
{
    "session_id":"abcd1234",
    "prompt":"Explain FastAPI"
}
```

The endpoint streams AI-generated responses from the local model.

---

## Chat History

```
GET /history/{session_id}
```

Returns all previous messages associated with the given session.

---

## Clear Chat

```
POST /clear
```

Clears the current session history.

---

# Database Schema

Table: `chats`

| Column | Type |
|----------|------|
| id | Integer |
| session_id | String |
| role | String |
| created_at | Timestamp |

> Note: The uploaded project currently comments out the `message` column in the model. It should be enabled if chat content needs to be stored.

Example:

```python
message = Column(Text)
```

---

# Chat Flow

```
Browser
    │
    ▼
FastAPI UI
    │
    ▼
POST /chat
    │
    ▼
llama.cpp
(Local GGUF Model)
    │
    ▼
Streaming Response
    │
    ▼
Save Conversation
(MySQL)
```

---

# Current Functionality

- Local LLM inference
- HTML chat interface
- Session generation
- Streaming responses
- Chat history retrieval
- Database integration

---

# Possible Improvements

- Authentication and user login
- Persistent conversation management
- Markdown rendering
- File upload support
- Multiple model selection
- Vector database integration (FAISS/ChromaDB)
- RAG implementation
- Docker deployment
- REST API documentation with Swagger
- Dark/Light theme toggle

---

# Future Enhancements

- LangChain integration
- Agentic AI workflow
- Memory-enabled conversations
- PDF document chat
- Voice input/output
- Multi-user support
- WebSocket-based real-time streaming
- GPU acceleration
- Conversation export

---

# Author

Developed as a FastAPI + llama.cpp local chatbot project for running GGUF language models with a lightweight web interface and MySQL-backed chat history.
