from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader
)
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

loader = DirectoryLoader(
    "rag/documents",
    glob="*.txt",
    loader_cls=TextLoader
)

documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

docs = text_splitter.split_documents(
    documents
)

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = FAISS.from_documents(
    docs,
    embedding_model
)

vectorstore.save_local(
    "rag/vectorstore"
)

prompt = PromptTemplate(
    template="""Answer the user question using the context below.
                Context:{context} Question:{question}""",
                input_variables=["context","question"]
)


llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-V4-Pro",
    task="text-generation"
)

model = ChatHuggingFace(
    llm=llm
)

output_parser = StrOutputParser()

chain = prompt | model | output_parser


def rag(question):

    results = vectorstore.similarity_search(
        question,
        k=2
    )

    context = "\n".join(
        [result.page_content for result in results]
    )

    response = chain.invoke({"context": context,"question": question})

    return response

# question= "what are business recommendation? "
# results = vectorstore.similarity_search(
#         question,
#         k=2
#     )

# context = "\n".join(
#         [result.page_content for result in results]
#     )

# response = chain.invoke({"context": context,"question": question})
# print(response)
