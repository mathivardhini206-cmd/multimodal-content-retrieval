from sentence_transformers import SentenceTransformer


# Load the pretrained Sentence Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks):
    """
    Convert text chunks into numerical vectors.
    """
    embeddings = model.encode(chunks)

    return embeddings


if __name__ == "__main__":

    from preprocessing import clean_text, create_chunks

    # Read the transcript
    with open("data/transcripts/demo.txt", "r") as file:
        transcript = file.read()

    # Clean the transcript
    cleaned_text = clean_text(transcript)

    # Create chunks
    chunks = create_chunks(cleaned_text)

    # Create embeddings
    embeddings = create_embeddings(chunks)

    print("\nNumber of chunks:", len(chunks))

    print("Embedding shape:", embeddings.shape)

    print("\nFirst chunk:")
    print(chunks[0])

    print("\nFirst embedding:")
    print(embeddings[0])
    