from langchain_groq import ChatGroq
from dotenv import load_dotenv
from rag.vectordb import rag

import os

load_dotenv()


# Load API Key
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found")


# Groq LLM
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile"
)


# Document Agent
def document_agent(user_query):

    try:

        # rag() already returns response text
        response = rag(user_query)

        return response

    except Exception as e:

        return f"Document Agent Error: {str(e)}"