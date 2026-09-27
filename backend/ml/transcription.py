import os
import subprocess
import sys


def transcribe_audio(audio_path, output_path):
    """
    Transcribes audio using Whisper in a separate process.
    This prevents conflicts with the embedding model.
    """

    print("Starting Whisper transcription in separate process...")

    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)

    command = [
        sys.executable,
        "-m",
        "whisper",
        audio_path,
        "--model",
        "tiny",
        "--language",
        "English",
        "--output_dir",
        output_dir,
        "--output_format",
        "txt"
    ]

    subprocess.run(command, check=True)

    # Whisper creates a .txt file using the audio filename
    whisper_txt = os.path.join(
        output_dir,
        os.path.splitext(os.path.basename(audio_path))[0] + ".txt"
    )

    with open(whisper_txt, "r", encoding="utf-8") as file:
        transcript = file.read().strip()

    # Save/copy it to the requested output path
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(transcript)

    print("Transcription completed.")

    return transcript
