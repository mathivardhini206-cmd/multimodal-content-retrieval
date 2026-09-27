import ollama
import base64
import os


def describe_frame(frame_path):

    with open(frame_path, "rb") as image_file:

        image_data = base64.b64encode(
            image_file.read()
        ).decode("utf-8")

    response = ollama.chat(
        model="llava:7b",
        options={
            "temperature": 0.2,
            "repeat_penalty": 1.2,
            "num_predict": 128
        },
        messages=[
            {
                "role": "user",
                "content": (
                    "Analyze this video frame carefully. "
                    "Describe exactly what is visible. "
                    "Identify people, their actions, objects, "
                    "the environment, screens, readable text, and "
                    "important activities. "
                    "If someone is using a computer, phone, book, "
                    "or other object, describe what they are doing "
                    "with it. "
                    "Do not guess details that cannot be seen."
                ),
                "images": [image_data],
            }
        ],
    )

    return response["message"]["content"].strip()


def describe_frames(frames_folder):

    descriptions = []

    frame_files = sorted(
        file_name
        for file_name in os.listdir(frames_folder)
        if file_name.lower().endswith(
            (".jpg", ".jpeg", ".png")
        )
    )

    for frame_file in frame_files:

        frame_path = os.path.join(
            frames_folder,
            frame_file
        )

        print(
            f"Analyzing {frame_file}..."
        )

        description = describe_frame(
            frame_path
        )

        # Create a path relative to data/frames
        relative_frame_path = os.path.relpath(
            frame_path,
            "data/frames"
        )

        # Make the path URL-friendly
        relative_frame_path = relative_frame_path.replace(
            os.sep,
            "/"
        )

        descriptions.append(
            {
                "frame": frame_file,
                "frame_path": relative_frame_path,
                "description": description
            }
        )

    return descriptions
