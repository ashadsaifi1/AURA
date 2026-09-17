from pathlib import Path
import pickle

import numpy as np
import faiss

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from sklearn.feature_extraction.text import TfidfVectorizer


DOCUMENTS_DIR = Path(__file__).parent / "Documents"
VECTOR_STORE_DIR = Path(__file__).parent / "Vector_store"

INDEX_FILE = VECTOR_STORE_DIR / "index.faiss"
DATA_FILE = VECTOR_STORE_DIR / "rag_data.pkl"


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
    texts = [chunk.page_content for chunk in chunks]

    print(f"Total chunks: {len(texts)}")

    vectorizer = TfidfVectorizer(
        max_features=5000,
        stop_words="english",
        dtype=np.float32
    )

    vectors = vectorizer.fit_transform(texts)
    vectors = vectors.toarray().astype("float32")

    faiss.normalize_L2(vectors)

    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)

    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)

    faiss.write_index(index, str(INDEX_FILE))

    with open(DATA_FILE, "wb") as file:
        pickle.dump(
            {
                "texts": texts,
                "vectorizer": vectorizer
            },
            file
        )

    print("FAISS vector store created successfully.")
    return len(texts)


def search_documents(query: str, k: int = 3):

    if not INDEX_FILE.exists() or not DATA_FILE.exists():
        raise FileNotFoundError("RAG vector store not found.")

    index = faiss.read_index(str(INDEX_FILE))

    with open(DATA_FILE, "rb") as file:
        data = pickle.load(file)

    vectorizer = data["vectorizer"]
    texts = data["texts"]

    query_vector = vectorizer.transform([query])
    query_vector = query_vector.toarray().astype("float32")

    faiss.normalize_L2(query_vector)

    scores, indices = index.search(query_vector, k)

    results = []

    for idx in indices[0]:
        if idx != -1:
            results.append(
                Document(page_content=texts[idx])
            )

    return results