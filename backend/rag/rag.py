from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


DOCUMENTS_DIR = Path(__file__).parent / "Documents"
VECTOR_STORE_DIR = Path(__file__).parent / "Vector_store"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
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

    print(f"Total chunks: {len(chunks)}")

    embeddings = get_embeddings()

    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )

    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)

    vector_store.save_local(str(VECTOR_STORE_DIR))

    print("FAISS vector store created successfully.")

    return len(chunks)


def search_documents(query: str):
    embeddings = get_embeddings()

    vector_store = FAISS.load_local(
        str(VECTOR_STORE_DIR),
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vector_store.similarity_search(query, k=3)