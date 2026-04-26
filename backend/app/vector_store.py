from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import os
from dotenv import load_dotenv

load_dotenv()

VECTOR_DB_PATH = "faiss_index"

def process_pdf(file_path: str):
    """
    Loads a PDF, splits it into chunks, and adds it to the FAISS vector store.
    """
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(pages)
    
    embeddings = OpenAIEmbeddings()
    
    if os.path.exists(VECTOR_DB_PATH):
        vectorstore = FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)
        vectorstore.add_documents(docs)
    else:
        vectorstore = FAISS.from_documents(docs, embeddings)
    
    vectorstore.save_local(VECTOR_DB_PATH)
    return len(docs)

def get_retriever():
    """
    Returns a retriever for searching the vector store.
    """
    embeddings = OpenAIEmbeddings()
    if os.path.exists(VECTOR_DB_PATH):
        vectorstore = FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)
        return vectorstore.as_retriever(search_kwargs={"k": 3})
    return None

def search_vector_store(query: str):
    """
    Searches the vector store for relevant context.
    """
    retriever = get_retriever()
    if retriever:
        docs = retriever.get_relevant_documents(query)
        return "\n\n".join([doc.page_content for doc in docs])
    return "No relevant context found in uploaded documents."
