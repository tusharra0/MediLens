import React, { useState, useRef } from 'react';
import "../css_files/landingpage.css";
import Navbar from "../components/navbar.jsx";


const LandingPage = () => {
  const [message, setMessage] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const fileInputRef = useRef(null);

  const handleSendMessage = async () => {
    if (message.trim() || selectedFile) {
      console.log('Sending message:', message);
      
      if (selectedFile) {
        console.log('Uploading file:', selectedFile.name);
        setIsUploading(true);
        
        try {
          // Create FormData for file upload
          const formData = new FormData();
          formData.append('pdf', selectedFile);
          formData.append('message', message);
          
          // Replace with your actual API endpoint
          const response = await fetch('/api/upload-pdf', {
            method: 'POST',
            body: formData,
          });
          
          if (response.ok) {
            const result = await response.json();
            console.log('Upload successful:', result);
          } else {
            console.error('Upload failed:', response.statusText);
          }
        } catch (error) {
          console.error('Upload error:', error);
        } finally {
          setIsUploading(false);
        }
      }
      
      // Reset form
      setMessage('');
      setSelectedFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file);
      console.log('PDF selected:', file.name);
    } else {
      alert('Please select a PDF file only');
      e.target.value = '';
    }
  };

  const handleAttachmentClick = () => {
    fileInputRef.current?.click();
  };

  const removeSelectedFile = () => {
    setSelectedFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="landing-container">
      <Navbar />
      <div className="main-content">
        <div className="input-section">
          <div className="input-container">
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf"
              onChange={handleFileSelect}
              style={{ display: 'none' }}
            />
            
            <button 
              className="attachment-btn"
              onClick={handleAttachmentClick}
              disabled={isUploading}
            >
              📎
            </button>
            
            <div className="input-wrapper">
              {selectedFile && (
                <div className="selected-file">
                  <span className="file-name">📄 {selectedFile.name}</span>
                  <button className="remove-file" onClick={removeSelectedFile}>×</button>
                </div>
              )}
              
              <input
                type="text"
                placeholder={selectedFile ? "Add a message (optional)..." : "Describe your symptoms or upload a medical report..."}
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                className="message-input"
                disabled={isUploading}
              />
            </div>
            
            <button className="mic-btn" disabled={isUploading}>🎤</button>
            
            <button 
              className="send-btn"
              onClick={handleSendMessage}
              disabled={(!message.trim() && !selectedFile) || isUploading}
            >
              {isUploading ? '⏳' : '➤'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;