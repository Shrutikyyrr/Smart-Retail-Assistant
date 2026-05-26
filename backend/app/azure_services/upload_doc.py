from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

from azure.storage.blob import BlobServiceClient

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from dotenv import load_dotenv

import os
import uuid

load_dotenv()



search_client = SearchClient(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    index_name=os.getenv("AZURE_SEARCH_INDEX"),
    credential=AzureKeyCredential(
        os.getenv("AZURE_SEARCH_KEY")
    )
)


blob_service_client = BlobServiceClient.from_connection_string(
    os.getenv("AZURE_STORAGE_CONNECTION_STRING")
)

container_client = blob_service_client.get_container_client(
    os.getenv("AZURE_BLOB_CONTAINER")
)


documents = []

blob_list = container_client.list_blobs()

for blob in blob_list:

    blob_client = container_client.get_blob_client(blob.name)

    blob_data = blob_client.download_blob().readall()

    text = blob_data.decode("utf-8")

    documents.append(text)

print("TOTAL DOCUMENTS:", len(documents))

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

split_docs = []

for doc in documents:

    chunks = text_splitter.split_text(doc)

    split_docs.extend(chunks)

print("TOTAL CHUNKS:", len(split_docs))


azure_docs = []

for chunk in split_docs:

    content = chunk.strip()

    if content:

        azure_docs.append({
            "id": str(uuid.uuid4()),
            "content": content
        })


result = search_client.upload_documents(
    documents=azure_docs
)

print("UPLOAD SUCCESS")
print(result)