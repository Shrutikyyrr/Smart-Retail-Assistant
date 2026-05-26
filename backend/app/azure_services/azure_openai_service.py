from openai import AzureOpenAI 
from dotenv import load_dotenv
import os

load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

client = AzureOpenAI(          
    api_key=api_key,
    azure_endpoint=endpoint,  
    api_version="2024-02-01"   
)

def generate_retail_insight(user_query):
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI Retail Assistant "
                    "that provides sales insights, "
                    "trend analysis, and recommendations."
                )
            },
            {
                "role": "user",
                "content": user_query
            }
        ],
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].message.content