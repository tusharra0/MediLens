import React, { useState, useRef } from 'react';
import "../css_files/landingpage.css";
import Navbar from "../components/navbar.jsx";

const LandingPage = () => {
  const [message, setMessage] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isAsking, setIsAsking] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);
  const fileInputRef = useRef(null);

  const handleSendMessage = async () => {
    if (!message.trim() && !selectedFile) return;

    // Handle file upload if there's a file
    if (selectedFile) {
      console.log('Uploading file:', selectedFile.name);
      setIsUploading(true);
      
      try {
        const formData = new FormData();
        formData.append('pdf', selectedFile);
        
        const response = await fetch('http://localhost:5000/api/upload-pdf', {
          method: 'POST',
          body: formData,
        });
        
        if (response.ok) {
          const result = await response.json();
          console.log('Upload successful:', result);
          
          // Add upload success message to chat
          setChatHistory(prev => [...prev, {
            type: 'system',
            message: `✅ Successfully uploaded "${selectedFile.name}" with ${result.chunks_created || 0} chunks processed.`
          }]);
        } else {
          console.error('Upload failed:', response.statusText);
          setChatHistory(prev => [...prev, {
            type: 'error',
            message: 'Failed to upload file. Please try again.'
          }]);
        }
      } catch (error) {
        console.error('Upload error:', error);
        setChatHistory(prev => [...prev, {
          type: 'error',
          message: 'Upload error: ' + error.message
        }]);
      } finally {
        setIsUploading(false);
      }
    }

    // Handle question asking if there's a message
    if (message.trim()) {
      console.log('Asking question:', message);
      
      // Add user message to chat
      setChatHistory(prev => [...prev, {
        type: 'user',
        message: message
      }]);
      
      setIsAsking(true);
      
      try {
        const response = await fetch('http://localhost:5000/api/ask', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ question: message }),
        });
        
        if (response.ok) {
          const result = await response.json();
          console.log('Question response:', result);
          
          // Add AI response to chat
          setChatHistory(prev => [...prev, {
            type: 'assistant',
            message: result.answer,
            sources: result.sources || []
          }]);
        } else {
          console.error('Question failed:', response.statusText);
          const errorData = await response.json();
          setChatHistory(prev => [...prev, {
            type: 'error',
            message: 'Failed to get answer: ' + (errorData.error || response.statusText)
          }]);
        }
      } catch (error) {
        console.error('Question error:', error);
        setChatHistory(prev => [...prev, {
          type: 'error',
          message: 'Error asking question: ' + error.message
        }]);
      } finally {
        setIsAsking(false);
      }
    }
    
    // Reset form
    setMessage('');
    setSelectedFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
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

  const clearChat = () => {
    setChatHistory([]);
  };

  return (
    <div className="landing-container">
      <Navbar />
      <div className="main-content">
        
        {/* Chat History Section */}
        <div className="chat-section">
          <div className="chat-header">
            <h3>Medical Assistant Chat</h3>
            {chatHistory.length > 0 && (
              <button className="clear-chat-btn" onClick={clearChat}>
                Clear Chat
              </button>
            )}
          </div>
          
          <div className="chat-history">
            {chatHistory.length === 0 ? (
              <div className="welcome-message">
                <p>👋 Welcome to MediLens! I can help you with medical questions.</p>
                <p>📄 Upload a PDF document and ask questions about it, or just ask me anything medical-related.</p>
              </div>
            ) : (
              chatHistory.map((chat, index) => (
                <div key={index} className={`chat-message ${chat.type}`}>
                  <div className="message-content">
                    {chat.type === 'user' && <strong>You:</strong>}
                    {chat.type === 'assistant' && <strong>🤖 Assistant:</strong>}
                    {chat.type === 'system' && <strong>💻 System:</strong>}
                    {chat.type === 'error' && <strong>❌ Error:</strong>}
                    <span>{chat.message}</span>
                  </div>
                  
                  {chat.sources && chat.sources.length > 0 && (
                    <div className="message-sources">
                      <details>
                        <summary>📚 Sources ({chat.sources.length})</summary>
                        {chat.sources.map((source, idx) => (
                          <div key={idx} className="source-item">
                            {source.substring(0, 200)}...
                          </div>
                        ))}
                      </details>
                    </div>
                  )}
                </div>
              ))
            )}
            
            {(isUploading || isAsking) && (
              <div className="chat-message loading">
                <div className="message-content">
                  <strong>🤖 Assistant:</strong>
                  <span>
                    {isUploading && "📤 Processing your PDF file..."}
                    {isAsking && "🤔 Thinking about your question..."}
                  </span>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Input Section */}
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
              disabled={isUploading || isAsking}
              title="Upload PDF document"
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
                placeholder={selectedFile ? "Ask a question about this document..." : "Ask me a medical question or upload a document..."}
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                className="message-input"
                disabled={isUploading || isAsking}
              />
            </div>
            
            <button className="mic-btn" disabled={isUploading || isAsking} title="Voice input (coming soon)">
              🎤
            </button>
            
            <button 
              className="send-btn"
              onClick={handleSendMessage}
              disabled={(!message.trim() && !selectedFile) || isUploading || isAsking}
              title="Send message"
            >
              {(isUploading || isAsking) ? '⏳' : '➤'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;