import cv2
import os


def extract_frames(video_path, output_folder, interval=30):
    os.makedirs(output_folder, exist_ok=True)

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError("Could not open video.")

    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps <= 0:
        raise ValueError("Could not determine video FPS.")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps

    saved_count = 0
    current_time = 0

    while current_time < duration:

        cap.set(
            cv2.CAP_PROP_POS_MSEC,
            current_time * 1000
        )

        success, frame = cap.read()

        if not success:
            break

        frame_path = os.path.join(
            output_folder,
            f"frame_{saved_count:04d}.jpg"
        )

        cv2.imwrite(frame_path, frame)

        saved_count += 1
        current_time += interval

    cap.release()

    print(f"Extracted {saved_count} frames.")

    return saved_count