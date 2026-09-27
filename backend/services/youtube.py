import os
import yt_dlp


def download_youtube_video(url, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    output_template = os.path.join(
        output_folder,
        "%(title)s.%(ext)s"
    )

    options = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": output_template,
        "merge_output_format": "mp4",
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)

    title = info.get("title", "youtube_video")

    # Find the actual MP4 file created by yt-dlp.

    mp4_files = [
        file_name
        for file_name in os.listdir(output_folder)
        if file_name.lower().endswith(".mp4")
    ]

    if not mp4_files:
        raise FileNotFoundError(
            "YouTube video was downloaded, but the MP4 file could not be found."
        )

    mp4_files.sort(
        key=lambda file_name: os.path.getmtime(
            os.path.join(output_folder, file_name)
        ),
        reverse=True
    )

    video_path = os.path.join(
        output_folder,
        mp4_files[0]
    )
    
    return video_path