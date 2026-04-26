# DataPilot — AI-Powered Business Intelligence Assistant

DataPilot is an AI-driven data analysis platform that enables users to interact with both structured and unstructured data using natural language.

Built using a Hybrid RAG (Retrieval-Augmented Generation) architecture, DataPilot allows seamless querying of datasets (CSV, Excel, SQL) alongside deep contextual understanding from documents (PDF, TXT).

---

## Key Features

### Hybrid Intelligence (Structured + Unstructured)
- Query tabular data using natural language to SQL conversion
- Retrieve insights from large documents using vector search (RAG)

### SQL Agent (NL → SQL)
- Converts user queries into optimized SQL
- Supports CSV/Excel auto-ingested into a database
- Enables non-technical users to analyze data easily

### Document Intelligence (RAG)
- Processes large PDFs (100+ pages)
- Uses embeddings and FAISS for semantic search
- Provides context-aware answers from reports

### Conversational Interface
- Chat-based interaction with data
- Supports follow-up queries and contextual understanding

### Modern UI
- Clean, responsive interface
- Split layout: Data Upload and AI Chat
- Designed for a SaaS-like experience

---

## Architecture Overview

DataPilot follows a Hybrid RAG Architecture:

- Structured Pipeline  
  CSV/Excel → SQLite → SQL Agent → Query Execution  

- Unstructured Pipeline  
  PDF/TXT → Chunking → Embeddings → FAISS → Retrieval  

- LLM Layer  
  Combines SQL results and retrieved context to generate final responses  

---

## Tech Stack

### Backend
- FastAPI  
- SQLAlchemy  
- LangChain  

### AI Engine
- Google Gemini (Flash 1.5)

### Data Layer
- SQLite (Structured Data)  
- FAISS (Vector Database)

### Frontend
- React  
- Vite  
- Axios  

---

## Local Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
