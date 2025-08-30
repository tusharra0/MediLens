import React, { useState, useRef } from "react";
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
  const fileInputRef = useRef(null);

  const handleSendMessage = async () => {
    if (message.trim() || selectedFile) {
      console.log("Sending message:", message);

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

          if (response.ok) {
            const result = await response.json();
            console.log("Upload successful:", result);
          } else {
            console.error("Upload failed:", response.statusText);
          }
        } catch (error) {
          console.error("Upload error:", error);
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

  return (
    <div className="landing-container">
      <Navbar />
      <div className="main-content" style={{ marginLeft: "220px" }}>
        {/* Show info when chat is empty */}
        {!message.trim() && !selectedFile && (
          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              height: "calc(100vh - 120px)", // adjust for input section height
              width: "100%",
              position: "absolute",
              left: 0,
              top: 0,
              zIndex: 1,
            }}
          >
            <div
              style={{
                textAlign: "center",
                fontSize: "1.3rem",
                color: "#6b7280",
                fontWeight: "500",
              }}
            >
              Medilens
              <br />
              Your AI assistant for medical queries and reports.
            </div>
          </div>
        )}
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
              <PlusIcon size={20}></PlusIcon>
            </button>

            <div className="input-wrapper">
              {selectedFile && (
                <div className="selected-file">
                  <span className="file-name"> {selectedFile.name}</span>
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
              <MicIcon size={20}></MicIcon>
            </button>

            <button
              className="mic-btn"
              onClick={handleSendMessage}
              disabled={(!message.trim() && !selectedFile) || isUploading}
            >
              {isUploading ? (
                <SendIcon size={20}></SendIcon>
              ) : (
                <SendIcon size={20}></SendIcon>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;
