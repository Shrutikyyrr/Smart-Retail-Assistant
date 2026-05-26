from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

load_dotenv()

ENDPOINT = os.getenv("TEXT_ANALYTICS_ENDPOINT")

KEY = os.getenv("TEXT_ANALYTICS_KEY")


client = TextAnalyticsClient(
    endpoint=ENDPOINT,
    credential=AzureKeyCredential(KEY)
)


def analyze_sentiment(text: str):

    response = client.analyze_sentiment(
        documents=[text]
    )[0]

    result = {
        "sentiment": response.sentiment,
        "positive_score": response.confidence_scores.positive,
        "neutral_score": response.confidence_scores.neutral,
        "negative_score": response.confidence_scores.negative
    }

    return result