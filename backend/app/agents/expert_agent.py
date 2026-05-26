from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()


# API Key
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found")


# Updated Model
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile"
)


# ML Expert Agent
def expert_agent(user_query):

    try:

        prompt = f"""
        You are an ML Expert Agent.

        Analyze the ML outputs
        and generate business insights.

        Query:
        {user_query}

        Explain:
        - Forecast trends
        - Important factors
        - Risks
        - Recommendations
        - Business impact

        Keep explanation simple.
        """

        response = llm.invoke(prompt)

        return response.content

    except Exception as e:

        return f"Expert Agent Error: {str(e)}"