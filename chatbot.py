from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import uuid
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
import sqlite3

# Environment setup for GoogleGenerativeAI
os.environ["GOOGLE_API_KEY"] = "AIzaSyCGY4DhG9Eo3Lc9KUUjVZUCksIQXtflgO8"
os.environ["LANGCHAIN_PROJECT"] = "Langchain-Rag-Chatbot"

app = FastAPI()

# Model initialization
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

# Database functions
DB_NAME = "rag_app.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_application_logs():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS application_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            user_query TEXT,
            genai_response TEXT,
            model TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.close()

def insert_application_logs(session_id, user_query, genai_response, model):
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO application_logs (session_id, user_query, genai_response, model) VALUES (?, ?, ?, ?)
    ''', (session_id, user_query, genai_response, model))
    conn.commit()
    conn.close()

def get_chat_history(session_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT user_query, genai_response FROM application_logs WHERE session_id = ? ORDER BY created_at', (session_id,))
    messages = [{"role": "human", "content": row['user_query']} for row in cursor.fetchall()]
    conn.close()
    return messages

@app.post("/query/")
async def query_endpoint(request: Request):
    data = await request.json()
    session_id = data.get("session_id", str(uuid.uuid4()))
    user_query = data["user_query"]
    
    # Get chat history
    chat_history = get_chat_history(session_id)
    
    # Generate response with GoogleGenerativeAI
    response = llm.invoke(user_query)
    
    # Insert log into the database
    insert_application_logs(session_id, user_query, response, "GoogleGenerativeAI")
    
    return {"session_id": session_id, "user_query": user_query, "response": response}

# Initialize the database table
create_application_logs()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import uuid
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
import sqlite3

# Environment setup for GoogleGenerativeAI
os.environ["GOOGLE_API_KEY"] = "AIzaSyCGY4DhG9Eo3Lc9KUUjVZUCksIQXtflgO8"
os.environ["LANGCHAIN_PROJECT"] = "Langchain-Rag-Chatbot"

app = FastAPI()

# Model initialization
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

# Database functions
DB_NAME = "rag_app.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_application_logs():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS application_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            user_query TEXT,
            gpt_response TEXT,
            model TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.close()

def insert_application_logs(session_id, user_query, gpt_response, model):
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO application_logs (session_id, user_query, gpt_response, model) VALUES (?, ?, ?, ?)
    ''', (session_id, user_query, gpt_response, model))
    conn.commit()
    conn.close()

def get_chat_history(session_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT user_query, gpt_response FROM application_logs WHERE session_id = ? ORDER BY created_at', (session_id,))
    messages = [{"role": "human", "content": row['user_query']} for row in cursor.fetchall()]
    conn.close()
    return messages

@app.post("/query/")
async def query_endpoint(request: Request):
    data = await request.json()
    session_id = data.get("session_id", str(uuid.uuid4()))
    user_query = data["user_query"]
    
    # Get chat history
    chat_history = get_chat_history(session_id)
    
    # Generate response with GoogleGenerativeAI
    response = llm.invoke(user_query)
    
    # Insert log into the database
    insert_application_logs(session_id, user_query, response, "GoogleGenerativeAI")
    
    return {"session_id": session_id, "user_query": user_query, "response": response}

# Initialize the database table
create_application_logs()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
