from typing import List

import nest_asyncio    
### typically used to ensure that asynchronous code can run smoothly 
### in environments that may already have an event loop running.

import logging     
#### standard Python library used for tracking events that happen when some software runs.
#### It can be configured to display different levels of severity, 
#### such as DEBUG, INFO, WARNING, ERROR, and CRITICAL.

import os        
### commonly used for tasks like reading environment variables 
### or manipulating file paths.

from dotenv import load_dotenv
### used to load environment variables from a .env file (best practice)

# Load variables from .env
load_dotenv()

from phi.assistant import Assistant   
### instantiated and used to handle conversational interactions,
### potentially incorporating responses from various sources and knowledge bases.

from phi.document import Document    
### used to create, read, or manipulate documents that the assistant can reference or discuss.

from phi.document.reader.pdf import PDFReader   
### to read the pdf

from phi.document.reader.website import WebsiteReader 
### to read the url (not used now, but available)

from phi.llm.openai import OpenAIChat
### OpenAI LLM wrapper used by PhiData

from phi.knowledge import AssistantKnowledge  
### a component that manages the knowledge base or repository of information 
### that the assistant can use to answer questions or provide information.

from phi.tools.duckduckgo import DuckDuckGo   
### to search the web when knowledge base does not have the answer

from phi.embedder.openai import OpenAIEmbedder
### converts text into vector embeddings using OpenAI embedding models

from phi.vectordb.pgvector import PgVector2  
### used to store and retrieve embeddings in PostgreSQL using pgvector

from phi.storage.assistant.postgres import PgAssistantStorage  
### used to store chat history and assistant memory in PostgreSQL

import psycopg
### PostgreSQL driver used internally by PgVector and storage

# ---------------------------------------------------
# Environment variables (loaded from .env)
# ---------------------------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4o")
DB_URL = os.getenv("DATABASE_URL")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file")

logger = logging.getLogger(__name__)

# ---------------------------------------------------
# 1. Setup Assistant
# ---------------------------------------------------
def setup_assistant(llm: OpenAIChat) -> Assistant:
    return Assistant(
        name="auto_rag_assistant",

        llm=llm,
        ### LLM brain (OpenAI GPT model)

        storage=PgAssistantStorage(
            table_name="auto_rag_assistant_openai",
            db_url=DB_URL
        ),
        ### stores chat history and memory in PostgreSQL

        knowledge_base=AssistantKnowledge(
            vector_db=PgVector2(
                db_url=DB_URL,
                collection="auto_rag_documents_openai",
                embedder=OpenAIEmbedder(
                    model="text-embedding-3-small",
                    api_key=OPENAI_API_KEY,
                    dimensions=1536
                ),
            ),
            num_documents=3,
        ),
        ### knowledge base that stores and retrieves relevant documents

        description="You are a helpful Assistant called 'AutoRAG' and your goal is to assist the user in the best way possible.",

        instructions=[
            "Given a user query, first ALWAYS search your knowledge base using the `search_knowledge_base` tool to see if you have relevant information.",
            "If you don't find relevant information in your knowledge base, use the `duckduckgo_search` tool to search the internet.",
            "If you need to reference the chat history, use the `get_chat_history` tool.",
            "If the users question is unclear, ask clarifying questions to get more information.",
            "Carefully read the information you have gathered and provide a clear and concise answer to the user.",
            "Do not use phrases like 'based on my knowledge' or 'depending on the information'.",
        ],

        show_tool_calls=True,
        ### shows which tools are being used (KB search, web search)

        search_knowledge=True,
        ### enables searching the knowledge base

        read_chat_history=True,
        ### enables reading previous conversations

        tools=[DuckDuckGo()],
        ### external web search tool

        markdown=True,
        ### formats output in markdown

        add_chat_history_to_messages=True,
        ### adds previous messages to prompt

        add_datetime_to_instructions=True,
        ### adds current date and time to system instructions

        debug_mode=True,
        ### enables detailed logs
    )

# ---------------------------------------------------
# 2. Add Document to Knowledge Base
# ---------------------------------------------------
def add_document_to_kb(
    assistant: Assistant,
    file_path: str,
    file_type: str = "pdf"
):
    if file_type == "pdf":
        reader = PDFReader()
    else:
        raise ValueError("Unsupported file type")

    documents: List[Document] = reader.read(file_path)

    if documents:
        assistant.knowledge_base.load_documents(
            documents,
            upsert=True
        )
        logger.info(f"Document '{file_path}' added to the knowledge base.")
    else:
        logger.error("Could not read document")

# ---------------------------------------------------
# 3. Run Query
# ---------------------------------------------------
def query_assistant(
    assistant: Assistant,
    question: str
):
    response = ""
    for delta in assistant.run(question):
        response += delta  # streaming response
    return response

# ---------------------------------------------------
# MAIN
# ---------------------------------------------------
if __name__ == "__main__":

    nest_asyncio.apply()
    ### ensures async compatibility

    llm = OpenAIChat(
        model=OPENAI_MODEL_NAME,
        api_key=OPENAI_API_KEY
    )

    assistant = setup_assistant(llm)

    sample_pdf_path = "sample.pdf"
    add_document_to_kb(
        assistant,
        sample_pdf_path,
        file_type="pdf"
    )

    query = "Which team won IPL 2024?"
    response = query_assistant(assistant, query)

    print("Query:", query)
    print("Response:", response)
