import { useState } from "react";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [relevantFrames, setRelevantFrames] = useState([]);
  const [visual, setVisual] = useState(null);
  const [summary, setSummary] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [processingStatus, setProcessingStatus] = useState("");
  const [video, setVideo] = useState(null);
  const [videoUrl, setVideoUrl] = useState("");
  const [youtubeUrl, setYoutubeUrl] = useState("");

  // =========================
  // REFRESH PAGE
  // =========================

  const refreshPage = () => {
    window.location.reload();
  };

  // =========================
  // BACK TO TOP
  // =========================

  const goToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  // =========================
  // START NEW VIDEO
  // =========================

  const resetProject = () => {
    setQuestion("");
    setAnswer("");
    setRelevantFrames([]);
    setVisual(null);
    setSummary("");
    setChatHistory([]);
    setLoading(false);
    setProcessingStatus("");
    setVideo(null);
    setVideoUrl("");
    setYoutubeUrl("");

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  // =========================
  // VIDEO UPLOAD
  // =========================

  const handleVideoChange = async (event) => {
    const selectedVideo = event.target.files[0];

    if (!selectedVideo) return;

    setVideo(selectedVideo);
    setVideoUrl(URL.createObjectURL(selectedVideo));

    setAnswer("");
    setRelevantFrames([]);
    setVisual(null);
    setSummary("");
    setChatHistory([]);

    setLoading(true);
    setProcessingStatus("🎬 Processing video...");

    const formData = new FormData();
    formData.append("video", selectedVideo);

    try {
      const response = await fetch(
        "http://127.0.0.1:5050/upload",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (response.ok) {
        setSummary(data.summary || "");
        setProcessingStatus("✅ Video ready!");
      } else {
        setProcessingStatus("");
        alert(data.error || "Upload failed.");
      }
    } catch (error) {
      console.error(error);

      setProcessingStatus("");
      alert("Could not connect to the backend.");
    }

    setLoading(false);
  };

  // =========================
  // YOUTUBE PROCESSING
  // =========================

  const processYouTubeVideo = async () => {
    if (!youtubeUrl.trim()) {
      alert("Please paste a YouTube URL.");
      return;
    }

    setLoading(true);
    setProcessingStatus("🎬 Processing YouTube video...");

    setAnswer("");
    setRelevantFrames([]);
    setVisual(null);
    setSummary("");
    setChatHistory([]);

    try {
      const response = await fetch(
        "http://127.0.0.1:5050/youtube",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            url: youtubeUrl,
          }),
        }
      );

      const data = await response.json();

      if (response.ok) {
        setSummary(data.summary || "");
        setProcessingStatus("✅ Video ready!");
      } else {
        setProcessingStatus("");
        alert(
          data.error ||
            "YouTube processing failed."
        );
      }
    } catch (error) {
      console.error(error);

      setProcessingStatus("");
      alert("Could not connect to the backend.");
    }

    setLoading(false);
  };

  // =========================
  // ASK QUESTION
  // =========================

  const askQuestion = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setAnswer("");
    setRelevantFrames([]);

    try {
      const response = await fetch(
        "http://127.0.0.1:5050/ask",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: question,
            history: chatHistory,
          }),
        }
      );

      const data = await response.json();

      if (response.ok) {
        const newAnswer =
          data.answer || "No answer received.";

        setAnswer(newAnswer);

        setRelevantFrames(
          data.relevant_frames || []
        );

        setVisual(
          data.visual || null
        );

        setChatHistory(
          (previousHistory) => [
            ...previousHistory,
            {
              role: "user",
              content: question,
            },
            {
              role: "assistant",
              content: newAnswer,
            },
          ]
        );

        setQuestion("");
      } else {
        setAnswer(
          data.error ||
            "Something went wrong."
        );
      }
    } catch (error) {
      console.error(error);

      setAnswer(
        "Could not connect to the backend."
      );
    }

    setLoading(false);
  };

  // =========================
  // FRONTEND
  // =========================

  return (
    <div className="app">

      {/* =========================
          FLOATING CONTROLS
      ========================= */}

      <div className="floating-controls">

        <button
          className="refresh-button"
          onClick={refreshPage}
          title="Refresh page"
        >
          ↻
          <span>Refresh</span>
        </button>

        <button
          className="top-button"
          onClick={goToTop}
          title="Back to top"
        >
          ↑
          <span>Top</span>
        </button>

      </div>

      {/* =========================
          HERO
      ========================= */}

      <header className="hero">

        <div className="hero-pipeline hero-pipeline-left">

          <span>VIDEO</span>
          <i></i>

          <span>AUDIO</span>
          <i></i>

          <span>TRANSCRIPT</span>

        </div>

        <div className="hero-pipeline hero-pipeline-right">

          <span>VISION</span>
          <i></i>

          <span>RETRIEVAL</span>
          <i></i>

          <span>AI ANSWER</span>

        </div>

        <div className="hero-overlay"></div>

        <div className="hero-content">

          <div className="hero-brand">
            MULTIMODAL AI
          </div>

          <div className="hero-top-right">
            VIDEO INTELLIGENCE
          </div>

          <div className="hero-main">

            <h1>
              Understand
              <br />
              <span>Every Frame.</span>
            </h1>

            <p>
              Upload a video and let AI understand what is
              <br />
              said, shown, and discussed.
            </p>

            <div className="hero-line"></div>

            <p className="hero-description">
              Multimodal Content Understanding &
              Conversational Retrieval
            </p>

          </div>

          <div className="hero-scroll">

            <span>
              SCROLL TO EXPLORE
            </span>

            <div className="scroll-line"></div>

          </div>

        </div>

      </header>

      {/* =========================
          MAIN CONTENT
      ========================= */}

      <main className="container">

        {/* =========================
            VIDEO UPLOAD
        ========================= */}

        <section className="video-card">

          <h2>
            🎥 Upload Your Video
          </h2>

          <label className="upload-box">

            <div className="upload-icon">
              🎥
            </div>

            <div className="upload-title">
              Upload a video
            </div>

            <div className="upload-subtitle">
              Click here to choose a video file
            </div>

            <input
              type="file"
              accept="video/*"
              onChange={handleVideoChange}
              className="hidden-file-input"
            />

          </label>

          {/* =========================
              YOUTUBE
          ========================= */}

          <div className="youtube-section">

            <div className="youtube-divider">
              <span>OR</span>
            </div>

            <h3 className="youtube-title">
              ▶️ Use a YouTube Video
            </h3>

            <div className="youtube-input">

              <input
                type="text"
                value={youtubeUrl}
                onChange={(e) =>
                  setYoutubeUrl(e.target.value)
                }
                placeholder="Paste YouTube URL..."
              />

              <button
                onClick={processYouTubeVideo}
                disabled={loading}
              >
                {loading
                  ? "Processing..."
                  : "Process YouTube Video"}
              </button>

            </div>

          </div>

          {/* =========================
              PROCESSING STATUS
          ========================= */}

          {processingStatus && (
            <div className="processing-status">

              <p>
                {processingStatus}
              </p>

            </div>
          )}

          {/* =========================
              VIDEO PREVIEW
          ========================= */}

          {videoUrl && (
            <video
              className="video-player"
              controls
            >

              <source
                src={videoUrl}
                type={video?.type}
              />

              Your browser does not support
              the video tag.

            </video>
          )}

        </section>

        {/* =========================
            SUMMARY
        ========================= */}

        {summary && (
          <section className="answer-card">

            <h2>
              📝 Video Summary
            </h2>

            <p>
              {summary}
            </p>

          </section>
        )}

        {/* =========================
            QUESTION
        ========================= */}

        <section className="question-card">

          <h2>
            Ask About the Video
          </h2>

          <div className="input-area">

            <input
              type="text"
              value={question}
              onChange={(e) =>
                setQuestion(e.target.value)
              }
              onKeyDown={(e) => {

                if (e.key === "Enter") {
                  askQuestion();
                }

              }}
              placeholder="Ask something about the video..."
            />

            <button
              onClick={askQuestion}
              disabled={loading}
            >
              {loading
                ? "Thinking..."
                : "Ask"}
            </button>

          </div>

        </section>

        {/* =========================
            AI ANSWER
        ========================= */}

        {answer && (

          <section className="answer-card">

            <h2>
              🤖 AI Answer
            </h2>

            <p>
              {answer}
            </p>

            {/* =========================
                RELATED CONCEPT VISUAL
            ========================= */}

            {visual &&
              visual.image_url && (

                <div className="visual-result">

                  <h3>
                    🌐 Related Concept Visual
                  </h3>

                  <img
                    src={visual.image_url}
                    alt={visual.query}
                    className="visual-result-image"
                  />

                  <p>
                    {visual.title}
                  </p>

                </div>

              )}

            {/* =========================
                RELEVANT VIDEO FRAMES
            ========================= */}

            {relevantFrames.length > 0 && (

              <div className="relevant-frames">

                <h3>
                  🎬 Relevant Video Frames
                </h3>

                <div className="frame-grid">

                  {relevantFrames.map(
                    (item, index) => (

                      <div
                        className="frame-card"
                        key={index}
                      >

                        <img
                          src={`http://127.0.0.1:5050/frames/${item.frame_path}`}
                          alt={`Relevant video frame ${
                            index + 1
                          }`}
                          className="relevant-frame-image"
                        />

                        <p>
                          <strong>
                            {item.frame}
                          </strong>
                        </p>

                        <p>
                          {item.description}
                        </p>

                      </div>

                    )
                  )}

                </div>

              </div>

            )}

            {/* =========================
                START NEW VIDEO
            ========================= */}

            <div className="answer-actions">

              <button
                className="new-video-button"
                onClick={resetProject}
              >
                + Start Another Video
              </button>

              <button
                className="top-action-button"
                onClick={goToTop}
              >
                ↑ Back to Top
              </button>

            </div>

          </section>

        )}

      </main>

    </div>
  );
}

export default App;