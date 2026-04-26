from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
import os
from dotenv import load_dotenv

load_dotenv()

VECTOR_DB_PATH = "faiss_index"

def process_file(file_path: str):
    """
    Loads a PDF or Text file, splits it into chunks, and adds it to the FAISS vector store.
    """
    if file_path.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith('.txt'):
        loader = TextLoader(file_path)
    else:
        raise ValueError("Unsupported file format for Vector storage")
    
    pages = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(pages)
    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    
    # Process in batches to avoid rate limits
    batch_size = 50
    import time
    
    if os.path.exists(VECTOR_DB_PATH):
        vectorstore = FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)
        for i in range(0, len(docs), batch_size):
            batch = docs[i:i + batch_size]
            vectorstore.add_documents(batch)
            if i + batch_size < len(docs):
                time.sleep(2)  # Pause to avoid rate limits
    else:
        # First batch creates the index
        first_batch = docs[0:batch_size]
        vectorstore = FAISS.from_documents(first_batch, embeddings)
        
        # Subsequent batches add to it
        for i in range(batch_size, len(docs), batch_size):
            batch = docs[i:i + batch_size]
            vectorstore.add_documents(batch)
            time.sleep(2)  # Pause to avoid rate limits
    
    vectorstore.save_local(VECTOR_DB_PATH)
    return len(docs)

def get_retriever():
    """
    Returns a retriever for searching the vector store.
    """
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
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
