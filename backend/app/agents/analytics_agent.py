from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()


# Load API Key
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found")


# Updated Supported Model
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile"
)


# Analytics Agent
def analytics_agent(user_query):

    try:

        prompt = f"""
        You are a Retail Analytics Expert.

        You help businesses analyze:
        - Sales trends
        - Customer behavior
        - Profits
        - Product performance
        - Category insights

        Analyze the following retail query
        and provide business insights.

        User Query:
        {user_query}

        Give:
        - Sales trends
        - Customer behavior
        - Product insights
        - Recommendations

        Keep the explanation simple.
        """

        # Generate response
        response = llm.invoke(prompt)

        return response.content

    except Exception as e:

        return f"Analytics Agent Error: {str(e)}"