# 📄 Document-Aware Assistant (AutoRAG)

An AutoRAG (Retrieval-Augmented Generation) AI assistant that answers user questions using PDF documents, web search, and conversational memory.

---

##  Features
- PDF document ingestion
- Semantic search using pgvector
- Accurate answers using OpenAI GPT models
- Automatic web search fallback
- Persistent chat history using PostgreSQL
- Built with PhiData

---

##  Architecture
1. PDF → Text Extraction  
2. Text → Embeddings (OpenAI)  
3. Embeddings → PostgreSQL (pgvector)  
4. User Query → Knowledge Base Search  
5. If missing → Web Search (DuckDuckGo)  
6. Final Answer → LLM (GPT-4o)

---

##  Tech Stack
- LLM: OpenAI GPT-4o
- Framework: PhiData
- Vector DB: pgvector
- Database: PostgreSQL
- Embeddings: OpenAI
- Tools: DuckDuckGo Search

---
### How To Run
1️⃣ Clone the Repository
git clone https://github.com/sahilshore/Document-Aware-Assistant.git
cd Document-Aware-Assistant

2️⃣ Create a Virtual Environment
          python -m venv venv


Activate it:

Windows

venv\Scripts\activate


Mac / Linux

source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Setup Environment Variables

Create a .env file in the project root:
      
      OPENAI_API_KEY=your_openai_api_key
      OPENAI_MODEL_NAME=gpt-4o
      DATABASE_URL=postgresql+psycopg://ai:ai@localhost:5432/ai


!!!! Make sure PostgreSQL is running and pgvector extension is enabled.

5️⃣ Add a PDF Document

Place your PDF file in the project directory
(example: sample.pdf)

You can replace it with your own document if needed.

6️⃣ Run the Application
             python app.py

7️⃣ Example Query
Which team won IPL 2024?


The assistant will:

Search the PDF knowledge base

Fall back to web search if needed

Generate a grounded response using the LLM

Notes

Do not commit your .env file to GitHub

This project uses OpenAI embeddings and GPT models

Designed to demonstrate a production-ready AutoRAG workflow
