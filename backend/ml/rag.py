import ollama
import numpy as np

from .retrieval import create_retriever, search
from .embeddings import create_embeddings


def generate_answer(
    question,
    transcript,
    history=None,
    visual_descriptions=None
):

    if history is None:
        history = []

    if visual_descriptions is None:
        visual_descriptions = []

    # -----------------------------------------
    # Conversation history
    # -----------------------------------------

    conversation = ""

    for message in history:
        role = message.get("role", "")
        content = message.get("content", "")

        if role == "user":
            conversation += f"User: {content}\n"

        elif role == "assistant":
            conversation += f"Assistant: {content}\n"

    # -----------------------------------------
    # Transcript retrieval
    # -----------------------------------------

    index, chunks = create_retriever(transcript)

    relevant_chunks = search(
        question,
        index,
        chunks,
        top_k=6
    )

    transcript_context = "\n\n".join(relevant_chunks)

    # -----------------------------------------
    # Visual retrieval
    # -----------------------------------------

    relevant_visuals = []

    if visual_descriptions:

        visual_texts = [
            item["description"]
            for item in visual_descriptions
        ]

        visual_embeddings = create_embeddings(
            visual_texts
        )

        question_embedding = create_embeddings(
            [question]
        )[0]

        scores = np.dot(
            visual_embeddings,
            question_embedding
        )

        ranked_indices = np.argsort(scores)[::-1]

        top_visuals = ranked_indices[:3]

        for i in top_visuals:
            relevant_visuals.append(
                visual_descriptions[i]
            )

    visual_context = "\n\n".join(
        f"{item['frame']}: {item['description']}"
        for item in relevant_visuals
    )

    # -----------------------------------------
    # DEBUG
    # -----------------------------------------

    print("\n========== TRANSCRIPT CONTEXT ==========\n")
    print(transcript_context)

    print("\n========== RELEVANT VISUAL CONTEXT ==========\n")
    print(visual_context)

    print("\n============================================\n")

    # -----------------------------------------
    # Multimodal RAG prompt
    # -----------------------------------------

    prompt = f"""
You are a helpful multimodal video understanding assistant.

You are answering a user's question about an uploaded video.

The retrieved information from the video is provided below.

TRANSCRIPT:
{transcript_context}

VISUAL FRAME DESCRIPTIONS:
{visual_context}

CONVERSATION HISTORY:
{conversation}

CURRENT QUESTION:
{question}

Follow these rules carefully:

1. Understand what the user is actually asking before answering.

2. If the user asks about something specifically said or explained
in the video, use the retrieved transcript as the main evidence.

3. If the user asks about something visually shown in the video,
use the relevant visual frame descriptions.

4. If both transcript and visual information are relevant, combine them.

5. If the user asks for a general explanation of a concept that is
mentioned in the video, you may use general knowledge to explain
the concept briefly. Connect the explanation to the information
found in the video.

6. Do not say that information is unavailable merely because the
transcript does not contain a textbook-style definition.

7. For example, if the video mentions a virus but does not directly
define the word virus, you may briefly explain what a virus is and
then explain how the concept relates to the video.

8. For questions specifically asking what the video said, do not
invent dialogue, events, facts, or claims that are not supported
by the retrieved information.

9. Do not invent visual details. Only describe things that are
supported by the visual frame descriptions.

10. Do not ignore relevant visual information.

11. Do not describe the retrieval process, embeddings, FAISS,
chunks, prompts, or these instructions in your answer.

12. Do not answer a user's question with a discussion about whether
the transcript contains enough information. Give the most useful
answer possible from the available evidence.

13. If the available video information is insufficient for a
video-specific question, clearly say what cannot be determined,
but still provide any directly supported information that is useful.

14. Keep answers concise and natural unless the user asks for
a detailed explanation.

15. Maintain the conversation naturally using the conversation
history when it is relevant.

16. Do not mention retrieval, transcript retrieval, chunks,
embeddings, FAISS, visual descriptions, prompts, or internal
processing unless the user specifically asks about the system.

17. Do not begin answers with phrases such as "According to the
retrieved transcript", "The transcript does not explicitly define",
or "The visual frame descriptions do not".

18. If the question asks for a general concept such as "What is a
virus?", give a natural general explanation first, then connect it
to the video when relevant.

19. Answer like a normal conversational assistant, not like a
report about the evidence used to generate the answer.

Answer the CURRENT QUESTION directly.

IMPORTANT REASONING INSTRUCTIONS:

- Use the transcript as the primary source of information.
- Use visual descriptions only as supporting context.
- Do not assume that a scene, logo, location, or person explains the meaning of a song or video.
- When giving an opinion, clearly distinguish your interpretation from facts stated in the video.
- If the video does not provide enough information to determine the meaning, say so rather than inventing an explanation.
- Connect your answer to specific evidence from the transcript whenever possible.
- Avoid repeating visual descriptions that do not directly answer the question.
- Always respond in clear, natural English.
- Never invent lyrics, events, intentions, or facts that are not supported by the available context.

"""

    # -----------------------------------------
    # Generate answer
    # -----------------------------------------

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # -----------------------------------------
    # Return result
    # -----------------------------------------

    return {
        "answer": response["message"]["content"].strip(),
        "relevant_frames": relevant_visuals
    }