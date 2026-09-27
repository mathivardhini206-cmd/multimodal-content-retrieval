import os
import subprocess


def extract_audio(video_path, audio_path):
    """
    Extracts audio from a video using FFmpeg.
    """

    os.makedirs(os.path.dirname(audio_path), exist_ok=True)

    command = [
        "ffmpeg",
        "-y",
        "-i",
        video_path,
        "-vn",
        "-acodec",
        "pcm_s16le",
        "-ar",
        "16000",
        "-ac",
        "1",
        audio_path
    ]

    subprocess.run(command, check=True)

    return audio_path
