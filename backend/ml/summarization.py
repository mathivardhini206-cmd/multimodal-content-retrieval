import ollama


def generate_summary(transcript):

    prompt = f"""
    You are an intelligent video summarization assistant.

    The following transcript may be in any language.

    Your task is to:
    1. Understand the transcript in its original language.
    2. Summarize its main topic, important events, and key information.
    3. Write the entire summary in clear, natural English.
    4. Preserve the original meaning and important details.
    5. Do not invent information that is not present in the transcript.
    6. Keep the summary concise and easy to understand.

    IMPORTANT:
    Regardless of the language of the transcript,
    your final summary MUST be in English.

    Transcript:
    {transcript}
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
