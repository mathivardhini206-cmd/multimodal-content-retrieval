
import os
import subprocess
import sys


def transcribe_audio(audio_path, output_path, language=None):

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
        "--output_dir",
        output_dir,
        "--output_format",
        "txt"
    ]

    # Use the selected language.
    # If Auto Detect is selected, Whisper detects it automatically.
    if language and language != "auto":
        command.extend(["--language", language])

    subprocess.run(command, check=True)

    # Whisper creates a .txt file using the audio filename.
    whisper_txt = os.path.join(
        output_dir,
        os.path.splitext(os.path.basename(audio_path))[0] + ".txt"
    )

    # Read the generated transcript.
    with open(whisper_txt, "r", encoding="utf-8") as file:
        transcript = file.read().strip()

    # Save the transcript to the requested output path.
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(transcript)

    print("Transcription completed.")

    return transcript
