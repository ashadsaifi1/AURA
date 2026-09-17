import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

DOCUMENTS_DIR = Path(__file__).parent / "Documents"
VECTOR_STORE_DIR = Path(__file__).parent / "Vector_store"


def get_embeddings():
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )


def create_vector_store():
    documents = []

    for pdf_file in DOCUMENTS_DIR.glob("*.pdf"):
        loader = PyPDFLoader(str(pdf_file))
        documents.extend(loader.load())

    if not documents:
        raise ValueError("No PDF found in Documents folder.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    embeddings = get_embeddings()

    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )

    vector_store.save_local(str(VECTOR_STORE_DIR))

    return len(chunks)


def search_documents(query: str):
    embeddings = get_embeddings()

    vector_store = FAISS.load_local(
        str(VECTOR_STORE_DIR),
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vector_store.similarity_search(
        query,
        k=3
    )