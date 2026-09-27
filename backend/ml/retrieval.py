import faiss
import numpy as np

from .preprocessing import clean_text, create_chunks
from .embeddings import create_embeddings


def create_retriever(transcript):
    """
    Creates a FAISS index from the given transcript.
    """

    # Clean transcript
    cleaned_text = clean_text(transcript)

    # Create chunks
    chunks = create_chunks(cleaned_text)

    # Create embeddings
    embeddings = create_embeddings(chunks)

    # Convert embeddings to FAISS format
    embeddings = np.array(embeddings).astype("float32")

    # Create FAISS index
    index = faiss.IndexFlatL2(embeddings.shape[1])

    # Add embeddings to FAISS
    index.add(embeddings)

    return index, chunks


def search(query, index, chunks, top_k=2):
    """
    Finds the most relevant transcript chunks for a question.
    """

    # Convert question into an embedding
    query_embedding = create_embeddings([query])
    query_embedding = np.array(query_embedding).astype("float32")

    # Search FAISS
    distances, indices = index.search(query_embedding, top_k)

    results = []

    for i in indices[0]:
        if i < len(chunks):
            results.append(chunks[i])

    return results
