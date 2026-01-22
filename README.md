# 📄 Document-Aware Assistant (AutoRAG)

An AutoRAG (Retrieval-Augmented Generation) AI assistant that answers user questions using PDF documents, web search, and conversational memory.

---

## 🚀 Features
- PDF document ingestion
- Semantic search using pgvector
- Accurate answers using OpenAI GPT models
- Automatic web search fallback
- Persistent chat history using PostgreSQL
- Built with PhiData

---

## 🧠 Architecture
1. PDF → Text Extraction  
2. Text → Embeddings (OpenAI)  
3. Embeddings → PostgreSQL (pgvector)  
4. User Query → Knowledge Base Search  
5. If missing → Web Search (DuckDuckGo)  
6. Final Answer → LLM (GPT-4o)

---

## 🛠️ Tech Stack
- LLM: OpenAI GPT-4o
- Framework: PhiData
- Vector DB: pgvector
- Database: PostgreSQL
- Embeddings: OpenAI
- Tools: DuckDuckGo Search

---

## ▶️ How to Run

### 1️⃣ Clone the repo
```bash
git clone https://github.com/sahilshore/Document-Aware-Assistant.git
cd Document-Aware-Assistant

