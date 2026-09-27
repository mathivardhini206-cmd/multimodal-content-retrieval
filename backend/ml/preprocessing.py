import re


def clean_text(text):
    """
    Cleans the raw transcript.
    """

    # Remove extra spaces and new lines
    text = re.sub(r"\s+", " ", text)

    # Remove unwanted characters
    text = re.sub(r"[^a-zA-Z0-9\s.,?'-]", "", text)

    return text.strip()


def create_chunks(text, chunk_size=80, overlap=20):
    """
    Splits the transcript into smaller overlapping chunks.
    """

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks

if __name__ == "__main__":

    # Read the Whisper transcript
    with open("data/transcripts/demo.txt", "r") as file:
        transcript = file.read()

    # Clean the transcript
    cleaned_text = clean_text(transcript)

    # Create chunks
    chunks = create_chunks(cleaned_text)

    print("\nCLEANED TRANSCRIPT:\n")
    print(cleaned_text)

    print("\n\nCHUNKS:\n")

    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i + 1}:")
        print(chunk) 
