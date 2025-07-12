# Conversational BI RAG Backend

A Python backend for a Conversational Business Intelligence (BI) system powered by Retrieval-Augmented Generation (RAG). This backend uses FastAPI, OpenAI, and ChromaDB to convert natural language questions into SQL queries and return insights as streaming text or graphs.

## 🧠 Key Features

- 🔍 **Natural Language to SQL**: Converts user questions into PostgreSQL queries using OpenAI.
- 📊 **Conversational BI**: Supports both textual and graph-based data responses.
- 🔁 **Streaming API (SSE)**: Delivers word-by-word responses in real-time.
- 📂 **RAG-Powered**: Uses schema, sample queries, filters, and metrics embedded via ChromaDB.
- 🧠 **Embeddings**: Generates and stores vector embeddings from documents for context-aware responses.



## 🚀 Tech Stack

- **FastAPI** – Lightweight, fast backend framework
- **PostgreSQL** – Data source for BI queries
- **ChromaDB** – Local vector store for embeddings
- **OpenAI API** – SQL generation, response synthesis
- **Docker Compose** – Containerized deployment
- **SSE/WebSocket** – Real-time data streaming (SSE implemented)



## 🛠️ Project Structure

    # Conversational BI RAG Backend

A Python backend for a Conversational Business Intelligence (BI) system powered by Retrieval-Augmented Generation (RAG). This backend uses FastAPI, OpenAI, and ChromaDB to convert natural language questions into SQL queries and return insights as streaming text or graphs.

## 🧠 Key Features

- 🔍 **Natural Language to SQL**: Converts user questions into PostgreSQL queries using OpenAI.
- 📊 **Conversational BI**: Supports both textual and graph-based data responses.
- 🔁 **Streaming API (SSE)**: Delivers word-by-word responses in real-time.
- 📂 **RAG-Powered**: Uses schema, sample queries, filters, and metrics embedded via ChromaDB.
- 🧠 **Embeddings**: Generates and stores vector embeddings from documents for context-aware responses.



## 🚀 Tech Stack

- **FastAPI** – Lightweight, fast backend framework
- **PostgreSQL** – Data source for BI queries
- **ChromaDB** – Local vector store for embeddings
- **OpenAI API** – SQL generation, response synthesis
- **Docker Compose** – Containerized deployment
- **SSE/WebSocket** – Real-time data streaming (SSE implemented)



## 🛠️ Project Structure

# Conversational BI RAG Backend

A Python backend for a Conversational Business Intelligence (BI) system powered by Retrieval-Augmented Generation (RAG). This backend uses FastAPI, OpenAI, and ChromaDB to convert natural language questions into SQL queries and return insights as streaming text or graphs.

## 🧠 Key Features

- 🔍 **Natural Language to SQL**: Converts user questions into PostgreSQL queries using OpenAI.
- 📊 **Conversational BI**: Supports both textual and graph-based data responses.
- 🔁 **Streaming API (SSE)**: Delivers word-by-word responses in real-time.
- 📂 **RAG-Powered**: Uses schema, sample queries, filters, and metrics embedded via ChromaDB.
- 🧠 **Embeddings**: Generates and stores vector embeddings from documents for context-aware responses.



## 🚀 Tech Stack

- **FastAPI** – Lightweight, fast backend framework
- **PostgreSQL** – Data source for BI queries
- **ChromaDB** – Local vector store for embeddings
- **OpenAI API** – SQL generation, response synthesis
- **Docker Compose** – Containerized deployment
- **SSE/WebSocket** – Real-time data streaming (SSE implemented)



## 🛠️ Project Structure

# Conversational BI RAG Backend

A Python backend for a Conversational Business Intelligence (BI) system powered by Retrieval-Augmented Generation (RAG). This backend uses FastAPI, OpenAI, and ChromaDB to convert natural language questions into SQL queries and return insights as streaming text or graphs.

## 🧠 Key Features

- 🔍 **Natural Language to SQL**: Converts user questions into PostgreSQL queries using OpenAI.
- 📊 **Conversational BI**: Supports both textual and graph-based data responses.
- 🔁 **Streaming API (SSE)**: Delivers word-by-word responses in real-time.
- 📂 **RAG-Powered**: Uses schema, sample queries, filters, and metrics embedded via ChromaDB.
- 🧠 **Embeddings**: Generates and stores vector embeddings from documents for context-aware responses.

## 🚀 Tech Stack

- **FastAPI** – Lightweight, fast backend framework
- **PostgreSQL** – Data source for BI queries
- **ChromaDB** – Local vector store for embeddings
- **OpenAI API** – SQL generation, response synthesis
- **Docker Compose** – Containerized deployment
- **SSE/WebSocket** – Real-time data streaming (SSE implemented)

## ⚙️ Setup Instructions

### 1. Clone the Repository
``` git clone https://github.com/haroonob/conversational-bi-rag-backend.git```
```cd conversational-bi-rag-backend```

## 2. Create .env File
```OPENAI_API_KEY=your-openai-key```

## 3. Run with Docker Compose
```docker compose up --build```

# Note 
wait for following message in logs before using
it will download , update and insert for data to database
https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx

### loader-1    | Data loaded and dates shifted into 'orders' table successfully!

# UI It is using following ui for demo purpose  
https://github.com/haroonob/react-ui-for-conversational-bi.git

![Preview](https://raw.githubusercontent.com/haroonob/react-ui-for-conversational-bi/main/src/assets/mainpage.png)

# API Endpoints
```markdown
    [POST /api/query]
    {
    "question": "Show total revenue by month"
    }
```

## 🛠️ Project Structure
```markdown
    conversational-bi-rag-backend/
    ├── app/
    │ ├── main.py # FastAPI entrypoint,SSE streaming responses,SQL generation and execution
    │ ├── rag_retriever.py # Embedding-based RAG
    │├── docs/ # RAG training documents
    ├── Dockerfile # Backend Dockerfile
    ├── data_loader.py # Loading open source order data to postgres
    ├── docker-compose.yml # Full stack orchestration
    └── requirements.txt


