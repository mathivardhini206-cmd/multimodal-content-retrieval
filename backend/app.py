from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

from ml.rag import generate_answer
from services.visual_search import search_visual
from ml.transcription import transcribe_audio
from ml.summarization import generate_summary
from services.video import extract_audio
from ml.frames import extract_frames
from ml.vision import describe_frames
from services.youtube import download_youtube_video


app = Flask(__name__)
CORS(app)


# ============================================================
# GLOBAL DATA
# ============================================================

current_transcript = ""
current_visual_descriptions = []


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():
    return "Multimodal Content Retrieval API is running!"


# ============================================================
# SERVE VIDEO FRAME IMAGES
# ============================================================

@app.route("/frames/<path:frame_path>")
def serve_frame(frame_path):

    frame_directory = os.path.join(
        "data",
        "frames"
    )

    return send_from_directory(
        frame_directory,
        frame_path
    )


# ============================================================
# LOCAL VIDEO UPLOAD
# ============================================================

@app.route("/upload", methods=["POST"])
def upload_video():

    global current_transcript
    global current_visual_descriptions

    if "video" not in request.files:
        return jsonify({
            "error": "No video uploaded"
        }), 400

    video = request.files["video"]

    if video.filename == "":
        return jsonify({
            "error": "No video selected"
        }), 400

    upload_folder = "data/videos"
    audio_folder = "data/audio"
    transcript_folder = "data/transcripts"

    os.makedirs(upload_folder, exist_ok=True)
    os.makedirs(audio_folder, exist_ok=True)
    os.makedirs(transcript_folder, exist_ok=True)

    video_path = os.path.join(
        upload_folder,
        video.filename
    )

    video.save(video_path)

    audio_filename = (
        os.path.splitext(video.filename)[0]
        + ".wav"
    )

    audio_path = os.path.join(
        audio_folder,
        audio_filename
    )

    try:

        # ----------------------------------------------------
        # 1. Extract audio
        # ----------------------------------------------------

        extract_audio(
            video_path,
            audio_path
        )


        # ----------------------------------------------------
        # 2. Extract video frames
        # ----------------------------------------------------

        frame_folder = os.path.join(
            "data/frames",
            os.path.splitext(video.filename)[0]
        )

        extract_frames(
            video_path,
            frame_folder,
            interval=30
        )


        # ----------------------------------------------------
        # 3. Analyze frames with LLaVA
        # ----------------------------------------------------

        visual_descriptions = describe_frames(
            frame_folder
        )

        current_visual_descriptions = (
            visual_descriptions
        )


        # ----------------------------------------------------
        # 4. Transcribe audio
        # ----------------------------------------------------

        transcript_filename = (
            os.path.splitext(video.filename)[0]
            + ".txt"
        )

        transcript_path = os.path.join(
            transcript_folder,
            transcript_filename
        )

        transcript = transcribe_audio(
            audio_path,
            transcript_path
        )

        current_transcript = transcript


        # ----------------------------------------------------
        # 5. Generate automatic summary
        # ----------------------------------------------------

        summary = generate_summary(
            transcript
        )


        # ----------------------------------------------------
        # 6. Return result
        # ----------------------------------------------------

        return jsonify({
            "message": "Video processed successfully",
            "video": video.filename,
            "audio": audio_filename,
            "transcript": transcript,
            "summary": summary,
            "visual_descriptions": visual_descriptions
        })


    except Exception as e:

        print(
            "Video processing error:",
            e
        )

        return jsonify({
            "error": (
                "Video processing failed: "
                + str(e)
            )
        }), 500


# ============================================================
# YOUTUBE VIDEO PROCESSING
# ============================================================

@app.route("/youtube", methods=["POST"])
def youtube():

    global current_transcript
    global current_visual_descriptions

    current_transcript = ""
    current_visual_descriptions = []

    data = request.get_json()

    if not data or not data.get("url"):
        return jsonify({
            "error": "YouTube URL is required"
        }), 400

    youtube_url = data["url"]

    video_folder = "data/videos/youtube"
    audio_folder = "data/audio/youtube"
    transcript_folder = "data/transcripts"
    frame_base_folder = "data/frames/youtube"

    os.makedirs(
        video_folder,
        exist_ok=True
    )

    os.makedirs(
        audio_folder,
        exist_ok=True
    )

    os.makedirs(
        transcript_folder,
        exist_ok=True
    )

    os.makedirs(
        frame_base_folder,
        exist_ok=True
    )

    try:

        # ----------------------------------------------------
        # 1. Download YouTube video
        # ----------------------------------------------------

        video_path = download_youtube_video(
            youtube_url,
            video_folder
        )

        print(
            "YouTube video downloaded:",
            video_path
        )


        # ----------------------------------------------------
        # 2. Extract audio
        # ----------------------------------------------------

        video_name = os.path.splitext(
            os.path.basename(video_path)
        )[0]

        audio_filename = (
            video_name
            + ".wav"
        )

        audio_path = os.path.join(
            audio_folder,
            audio_filename
        )

        extract_audio(
            video_path,
            audio_path
        )


        # ----------------------------------------------------
        # 3. Transcribe audio
        # ----------------------------------------------------

        transcript_filename = (
            video_name
            + ".txt"
        )

        transcript_path = os.path.join(
            transcript_folder,
            transcript_filename
        )

        transcript = transcribe_audio(
            audio_path,
            transcript_path
        )

        current_transcript = transcript


        # ----------------------------------------------------
        # 4. Extract video frames
        # ----------------------------------------------------

        frame_folder = os.path.join(
            frame_base_folder,
            video_name
        )

        extract_frames(
            video_path,
            frame_folder,
            interval=30
        )


        # ----------------------------------------------------
        # 5. Analyze frames with LLaVA
        # ----------------------------------------------------

        visual_descriptions = describe_frames(
            frame_folder
        )

        current_visual_descriptions = (
            visual_descriptions
        )


        # ----------------------------------------------------
        # 6. Generate summary
        # ----------------------------------------------------

        summary = generate_summary(
            transcript
        )


        # ----------------------------------------------------
        # 7. Return result
        # ----------------------------------------------------

        return jsonify({
            "message": (
                "YouTube video processed successfully"
            ),
            "video": os.path.basename(video_path),
            "audio": audio_filename,
            "transcript": transcript,
            "summary": summary,
            "visual_descriptions": visual_descriptions
        })


    except Exception as e:

        print(
            "YouTube processing error:",
            e
        )

        return jsonify({
            "error": (
                "YouTube processing failed: "
                + str(e)
            )
        }), 500


# ============================================================
# ASK QUESTIONS ABOUT CURRENT VIDEO
# ============================================================

@app.route("/ask", methods=["POST"])
def ask_question():

    global current_transcript
    global current_visual_descriptions

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No question provided"
        }), 400

    question = data.get(
        "question",
        ""
    ).strip()

    history = data.get(
        "history",
        []
    )

    if not question:
        return jsonify({
            "error": "Question cannot be empty"
        }), 400

    if not current_transcript:
        return jsonify({
            "error": "Please upload or process a video first"
        }), 400

    try:

        print(
            "Visual descriptions available:",
            len(current_visual_descriptions)
        )

        result = generate_answer(
            question,
            current_transcript,
            history,
            current_visual_descriptions
        )

        visual_result = search_visual(question)

        return jsonify({
            "answer": result["answer"],
            "relevant_frames": result["relevant_frames"],
            "visual": visual_result
        })


    except Exception as e:

        print(
            "Question answering error:",
            e
        )

        return jsonify({
            "error": (
                "Question answering failed: "
                + str(e)
            )
        }), 500


# ============================================================
# START FLASK SERVER
# ============================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5050,
        debug=False
    )
