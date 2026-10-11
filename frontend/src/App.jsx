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
  const [selectedLanguage, setSelectedLanguage] = useState("auto");

  // Build a thumbnail image URL from a YouTube link (no backend needed).
  const getYoutubeThumb = (url) => {
    if (!url) return "";
    const match = url.match(/(?:youtu\.be\/|v=|\/embed\/|\/shorts\/)([A-Za-z0-9_-]{11})/);
    return match ? `https://img.youtube.com/vi/${match[1]}/hqdefault.jpg` : "";
  };

  const refreshPage = () => {
    window.location.reload();
  };

  const goToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

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
    setSelectedLanguage("auto");
    window.scrollTo({ top: 0, behavior: "smooth" });
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
    formData.append("language", selectedLanguage);

    try {
      const response = await fetch("http://127.0.0.1:5050/upload", {
        method: "POST",
        body: formData,
      });

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
      const response = await fetch("http://127.0.0.1:5050/youtube", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: youtubeUrl, language: selectedLanguage }),
      });

      const data = await response.json();

      if (response.ok) {
        setSummary(data.summary || "");
        setProcessingStatus("✅ Video ready!");
      } else {
        setProcessingStatus("");
        alert(data.error || "YouTube processing failed.");
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

    const askedQuestion = question;

    setLoading(true);
    setAnswer("");
    setRelevantFrames([]);

    try {
      const response = await fetch("http://127.0.0.1:5050/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: askedQuestion, history: chatHistory }),
      });

      const data = await response.json();

      if (response.ok) {
        const newAnswer = data.answer || "No answer received.";
        setAnswer(newAnswer);
        setRelevantFrames(data.relevant_frames || []);
        setVisual(data.visual || null);
        setChatHistory((previousHistory) => [
          ...previousHistory,
          { role: "user", content: askedQuestion },
          { role: "assistant", content: newAnswer },
        ]);
        setQuestion("");
      } else {
        setAnswer(data.error || "Something went wrong.");
      }
    } catch (error) {
      console.error(error);
      setAnswer("Could not connect to the backend.");
    }

    setLoading(false);
  };

  const hasConversation = chatHistory.length > 0;
  const youtubeThumb = getYoutubeThumb(youtubeUrl);
  const hasResult = summary || videoUrl || youtubeThumb;

  return (
    <div className="app">

      {/* background */}
      <div className="mesh">
        <span className="m1"></span>
        <span className="m2"></span>
        <span className="m3"></span>
      </div>
      <div className="grid-bg"></div>

      {/* floating controls */}
      <div className="floating-controls">
        <button className="refresh-button" onClick={refreshPage} title="Refresh page">
          ↻<span>Refresh</span>
        </button>
        <button className="top-button" onClick={goToTop} title="Back to top">
          ↑<span>Top</span>
        </button>
      </div>

      {/* top nav */}
      <nav className="nav">
        <div className="brand">
          <span className="mark"><i className="t"></i><i className="a"></i></span>
          <b>Multimodal<span> / video intelligence</span></b>
        </div>
        <div className="nav-right">
          <span className="chip"><span className="d"></span>backend ready</span>
          <button className="ghost" onClick={resetProject}>New video</button>
        </div>
      </nav>

      <div className="wrap">

        {/* hero */}
        <section className="hero">
          <span className="eyebrow">speech · vision · retrieval</span>
          <h1>Understand <span className="g">every frame.</span></h1>
          <p>Drop a video or paste a link. The system listens, watches, and lets you have a real conversation about what was said and shown.</p>
        </section>

        {/* intake */}
        <div className="intake">
          <div className="pane">
            <label className="drop">
              <span className="ic">🎬</span>
              <b>Upload a video</b>
              <small>MP4, MOV, WEBM — click to choose a file</small>
              <input
                type="file"
                accept="video/*"
                onChange={handleVideoChange}
                className="hidden-file-input"
              />
            </label>
          </div>
          <div className="pane">
            <h3>or use a link</h3>
            <div className="yt">
              <div className="field">
                <input
                  type="text"
                  value={youtubeUrl}
                  onChange={(e) => setYoutubeUrl(e.target.value)}
                  placeholder="Paste a YouTube URL…"
                />
              </div>
              <button className="btn" onClick={processYouTubeVideo} disabled={loading}>
                {loading ? "Processing…" : "Process video"}
              </button>
              <div className="sel">Language
                <select
                  value={selectedLanguage}
                  onChange={(e) => setSelectedLanguage(e.target.value)}
                >
                  <option value="auto">Auto detect</option>
                  <option value="en">English</option>
                  <option value="ta">Tamil</option>
                  <option value="hi">Hindi</option>
                  <option value="te">Telugu</option>
                  <option value="ml">Malayalam</option>
                  <option value="kn">Kannada</option>
                  <option value="bn">Bengali</option>
                  <option value="es">Spanish</option>
                  <option value="fr">French</option>
                  <option value="de">German</option>
                  <option value="ja">Japanese</option>
                  <option value="ko">Korean</option>
                  <option value="zh">Chinese</option>
                  <option value="ar">Arabic</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        {/* processing status */}
        {processingStatus && (
          <div className="processing-status">
            <p>{processingStatus}</p>
          </div>
        )}

        {/* ---- SUMMARY (3/4) + VIDEO (1/4) row ---- */}
        {hasResult && (
          <div className="result-top">

            {summary && (
              <div className="card summary-card">
                <p className="label"><span className="bar teal"></span>Understanding</p>
                <div className="tags">
                  <span className="tag teal">summary in English</span>
                </div>
                <div className="summary">
                  <p>{summary}</p>
                </div>
              </div>
            )}

            {(videoUrl || youtubeThumb) && (
              <div className="card video-side">
                <p className="label"><span className="bar teal"></span>Video</p>
                {videoUrl ? (
                  <video className="video-player" controls>
                    <source src={videoUrl} type={video?.type} />
                    Your browser does not support the video tag.
                  </video>
                ) : (
                  <img className="yt-thumb" src={youtubeThumb} alt="Video thumbnail" />
                )}
              </div>
            )}

          </div>
        )}

        {/* ---- ASK BAR ---- */}
        <div className="asktop">
          <textarea
            rows="1"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                askQuestion();
              }
            }}
            placeholder="Ask about what was said or shown…"
          />
          <button className="send" onClick={askQuestion} disabled={loading}>
            {loading ? "Thinking…" : "Ask"}
          </button>
        </div>

        {/* ---- ANSWERS ---- */}
        {(hasConversation || loading) && (
          <section className="card convo">
            <div className="stream">

              {chatHistory.map((msg, index) =>
                msg.role === "user" ? (
                  <div className="q" key={index}>{msg.content}</div>
                ) : (
                  <div className="a" key={index}>
                    <div className="txt">{msg.content}</div>
                  </div>
                )
              )}

              {loading && (
                <div className="thinking"><span className="d"></span>Thinking…</div>
              )}

              {/* evidence for the latest answer */}
              {(relevantFrames.length > 0 || (visual && visual.image_url)) && (
                <div className="ev">

                  {relevantFrames.length > 0 && (
                    <>
                      <div className="cap">frames from the video</div>
                      <div className="frames">
                        {relevantFrames.map((item, index) => (
                          <div className="fr" key={index}>
                            <img
                              className="fr-im"
                              src={`http://127.0.0.1:5050/frames/${item.frame_path}`}
                              alt={`Relevant video frame ${index + 1}`}
                            />
                            <div className="fr-t">{item.frame}</div>
                            <div className="fr-c">{item.description}</div>
                          </div>
                        ))}
                      </div>
                    </>
                  )}

                  {visual && visual.image_url && (
                    <div className="concept">
                      <img className="concept-im" src={visual.image_url} alt={visual.query} />
                      <div className="ct">
                        <b>Related concept image</b>
                        {visual.title}
                        <div className="cx">EXTERNAL · WIKIMEDIA — NOT VIDEO EVIDENCE</div>
                      </div>
                    </div>
                  )}

                </div>
              )}

            </div>

            {hasConversation && (
              <div className="answer-actions">
                <button className="new-video-button" onClick={resetProject}>
                  + Start Another Video
                </button>
                <button className="top-action-button" onClick={goToTop}>
                  ↑ Back to Top
                </button>
              </div>
            )}
          </section>
        )}

      </div>
    </div>
  );
}

export default App;
