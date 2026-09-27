import ollama


def generate_summary(transcript):
    """
    Generates a short summary of the uploaded video's transcript.
    """

    prompt = f"""
You are summarizing the transcript of a video.

Create a clear and concise summary of the video.

Focus on:
- The main topic
- Important events or ideas
- The main message or conclusion

Transcript:

{transcript}

Write the summary in 1–2 short paragraphs.
Do not add information that is not present in the transcript.
"""

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]
