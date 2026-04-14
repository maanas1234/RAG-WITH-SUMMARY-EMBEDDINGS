from langchain_classic.retrievers.multi_vector import MultiVectorRetriever
from langchain_classic.storage import InMemoryByteStore
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader,TextLoader

import os
import uuid

parent_splitter = RecursiveCharacterTextSplitter(chunk_size=300)

summaries_collection = Chroma(
    collection_name="Summaries",
    embedding_function=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"),
persist_directory="./chroma_db")

summaries_collection.reset_collection()

doc_byte_store = InMemoryByteStore()
doc_key = "doc_id"

multi_vector_retriever = MultiVectorRetriever(
    vectorstore=summaries_collection,
    byte_store=doc_byte_store
)

llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key =os.getenv("OPENROUTER_API_KEY"),
    model="openai/gpt-oss-120b:free"  # free tier model
)

chain = ({"document":lambda x:x.page_content} | ChatPromptTemplate.from_template("summarise the following document\n\n{document}") | llm | StrOutputParser())
x

loader = DirectoryLoader(
    path="./BOOKS AND PAPERS FOR AI",
    glob="*.pdf",
    loader_cls=PyPDFLoader
)

docs = loader.load()


chunks = parent_splitter.split_documents(docs)

doc_id = [str(uuid.uuid4() for _ in chunks)]

summaries = chain.batch(chunks, {"max_concurrency":2})

summary_docs = [
    Document(page_content=summaries[i], metadata={doc_key: doc_id[i]})
    for i in range(len(summaries))
]

summaries_collection.add_documents(summary_docs)

doc_byte_store.mset(list(zip(doc_id,chunks)))


                
result = multi_vector_retriever.invoke("Tell me about concept mapper?")
print(result[0])

print("THIS IS THE BREAK LINE BETWEEN MULTIVECTOR ND SIMILARITY")


result2 = summaries_collection.similarity_search("What is concept mapper?")
print(result2)