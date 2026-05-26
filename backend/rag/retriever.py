from langchain_community.vectorstores import FAISS

from rag.embeddings import embeddings

vectorstore = FAISS.load_local(

    "rag/vectorstore/faiss_index",

    embeddings,

    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever(

    search_kwargs={"k": 3}
)