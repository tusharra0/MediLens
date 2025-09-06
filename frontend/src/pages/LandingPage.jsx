import React, { useState, useRef, useEffect } from "react";
import "../css_files/landingpage.css";
import Navbar from "../components/Navbar.jsx";
import MicIcon from "../assets/MicIcon.jsx";
import PlusIcon from "../assets/PlusIcon.jsx";
import SendIcon from "../assets/SendIcon.jsx";
import Sidebar from "../components/Sidebar.jsx";

const LandingPage = () => {
  const [message, setMessage] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);
  const chatEndRef = useRef(null);

  // Auto-scroll to bottom when new messages are added
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatHistory]);

  const handleSendMessage = async () => {
    if (message.trim() || selectedFile) {
      // Add user message to chat history immediately
      const userMessage = {
        id: Date.now(),
        type: "user",
        content: message || "Uploaded medical document",
        file: selectedFile ? selectedFile.name : null,
        timestamp: new Date().toLocaleTimeString(),
      };

      setChatHistory((prev) => [...prev, userMessage]);
      setError(null);

      console.log("Sending message:", message);

      // Handle file upload or text-only message
      if (selectedFile) {
        console.log("Uploading file:", selectedFile.name);
        setIsUploading(true);

        try {
          const formData = new FormData();
          formData.append("pdf", selectedFile);
          formData.append("message", message);

          const response = await fetch("http://localhost:5000/api/upload-pdf", {
            method: "POST",
            body: formData,
          });

          const result = await response.json();

          if (response.ok && result.success) {
            console.log("Upload successful:", result);

            // Add AI response to chat history
            const aiMessage = {
              id: Date.now() + 1,
              type: "ai",
              content: result.ai_response,
              timestamp: new Date().toLocaleTimeString(),
              sessionId: result.session_id,
              filename: result.filename,
            };

            setChatHistory((prev) => [...prev, aiMessage]);
          } else {
            console.error(
              "Upload failed:",
              result.error || response.statusText
            );
            setError(result.error || "Upload failed. Please try again.");
          }
        } catch (error) {
          console.error("Upload error:", error);
          setError(
            "Network error. Please check your connection and try again."
          );
        } finally {
          setIsUploading(false);
        }
      } else if (message.trim()) {
        // Handle text-only message
        setIsUploading(true);

        try {
          const response = await fetch("http://localhost:5000/api/chat", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ message: message.trim() }),
          });

          const result = await response.json();

          if (response.ok && result.success) {
            console.log("Chat successful:", result);

            // Add AI response to chat history
            const aiMessage = {
              id: Date.now() + 1,
              type: "ai",
              content: result.ai_response,
              timestamp: new Date().toLocaleTimeString(),
              sessionId: result.session_id,
            };

            setChatHistory((prev) => [...prev, aiMessage]);
          } else {
            console.error("Chat failed:", result.error || response.statusText);
            setError(
              result.error || "Failed to get response. Please try again."
            );
          }
        } catch (error) {
          console.error("Chat error:", error);
          setError(
            "Network error. Please check your connection and try again."
          );
        } finally {
          setIsUploading(false);
        }
      }

      // Reset form
      setMessage("");
      setSelectedFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file && file.type === "application/pdf") {
      setSelectedFile(file);
      console.log("PDF selected:", file.name);
    } else {
      alert("Please select a PDF file only");
      e.target.value = "";
    }
  };

  const handleAttachmentClick = () => {
    fileInputRef.current?.click();
  };

  const removeSelectedFile = () => {
    setSelectedFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const clearChat = () => {
    setChatHistory([]);
    setError(null);
  };

  return (
    <div className="landing-root">
      <div className="app-sidebar">
        <Sidebar />
      </div>
      <div className="app-navbar">
        <Navbar />
      </div>

      <div className="main-content">
        {/* Show info when chat is empty */}
        {chatHistory.length === 0 && !message.trim() && !selectedFile && (
          <div className="center-hero">
            <div className="hero-text">
              Medilens
              <br />
              Your AI assistant for medical queries and reports.
            </div>
          </div>
        )}

        {/* Chat History */}
        {chatHistory.length > 0 && (
          <div className="chat-history">
            <div className="chat-messages">
              {chatHistory.map((msg) => (
                <div key={msg.id} className={`chat-message ${msg.type}`}>
                  <div className="message-header">
                    <span className="message-sender">
                      {msg.type === "user" ? "You" : "Dr. MediLens"}
                    </span>
                    <span className="message-time">{msg.timestamp}</span>
                  </div>

                  <div className="message-content">
                    {msg.file && (
                      <div className="message-file">📄 {msg.file}</div>
                    )}
                    {msg.filename && (
                      <div className="message-file">
                        📄 Analyzed: {msg.filename}
                      </div>
                    )}
                    <div className="message-text">
                      {msg.content.split("\n").map((line, index) => (
                        <p key={index}>{line}</p>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
              <div ref={chatEndRef} />
            </div>
          </div>
        )}

        {error && (
          <div className="error-message">
            <span>⚠️ {error}</span>
            <button onClick={() => setError(null)} className="error-close">
              ×
            </button>
          </div>
        )}

        {isUploading && (
          <div className="loading-indicator">
            <div className="loading-spinner"></div>
            <span>Dr. MediLens is analyzing...</span>
          </div>
        )}
      </div>

      {/* Input bar (fixed bottom) */}
      <div className="input-section">
        <div className="input-container">
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf"
            onChange={handleFileSelect}
            style={{ display: "none" }}
          />
          <button
            className="attachment-btn"
            onClick={handleAttachmentClick}
            disabled={isUploading}
          >
            <PlusIcon size={20} />
          </button>
          <div className="input-wrapper">
            {selectedFile && (
              <div className="selected-file">
                <span className="file-name">{selectedFile.name}</span>
                <button className="remove-file" onClick={removeSelectedFile}>
                  ×
                </button>
              </div>
            )}
            <input
              type="text"
              placeholder={
                selectedFile
                  ? "Add a message (optional)..."
                  : "Describe your symptoms or upload a medical report..."
              }
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              className="message-input"
              disabled={isUploading}
            />
          </div>
          <button className="mic-btn" disabled={isUploading}>
            <MicIcon size={20} />
          </button>
          <button
            className="mic-btn"
            onClick={handleSendMessage}
            disabled={(!message.trim() && !selectedFile) || isUploading}
          >
            {isUploading ? (
              <div className="button-spinner" />
            ) : (
              <SendIcon size={20} />
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;
