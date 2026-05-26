from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

load_dotenv()

search_client = SearchClient(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    index_name=os.getenv("AZURE_SEARCH_INDEX"),
    credential=AzureKeyCredential(
        os.getenv("AZURE_SEARCH_KEY")
    )
)


def search_documents(query: str):

    results = search_client.search(
        search_text=query
    )

    documents = []

    for result in results:

        print(result)

        documents.append(
            result.get("content")
        )

    return documents[:3]