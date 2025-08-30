import React, { useState } from "react";
import "../css_files/Sidebar.css";
import LogoutIcon from "../assets/LogoutIcon";
import ProfileIcon from "../assets/ProfileIcon";

const Sidebar = () => {
  const [chats, setChats] = useState([{ id: 1, title: "Chat 1" }]);
  const [activeChatId, setActiveChatId] = useState(1);

  const handleNewChat = () => {
    const newId = chats.length ? chats[chats.length - 1].id + 1 : 1;
    const newChat = { id: newId, title: `Chat ${newId}` };
    setChats([...chats, newChat]);
    setActiveChatId(newId);
  };

  const handleSelectChat = (id) => {
    setActiveChatId(id);
  };

  return (
    <div
      className="sidebar"
      style={{
        width: "220px",
        height: "100vh",
        color: "#fff",
        display: "flex",
        flexDirection: "column",
        padding: "20px 0",
      }}
    >
      <h2
        style={{
          color: "#000000ff",
          textAlign: "center",
          marginBottom: "30px",
        }}
      >
        MediLens
      </h2>
      <nav>
        <ul style={{ listStyle: "none", padding: 0 }}>
          <li style={{ margin: "20px 0" }}>
            <a
              href="#"
              onClick={(e) => {
                e.preventDefault();
                handleNewChat();
              }}
              style={{ color: "#000000ff", textDecoration: "none" }}
            >
              New Chat
            </a>
          </li>
          <li style={{ margin: "20px 0" }}>
            <a
              href="/settings"
              style={{ color: "#000000ff", textDecoration: "none" }}
            >
              Settings
            </a>
          </li>
        </ul>
      </nav>
      <div style={{ margin: "20px 0 0 0", padding: "0 20px" }}>
        <div
          style={{
            fontWeight: "bold",
            marginBottom: "10px",
            color: "#000000ff",
          }}
        >
          Chats
        </div>
        <div>
          {chats.map((chat) => (
            <button
              key={chat.id}
              onClick={() => handleSelectChat(chat.id)}
              style={{
                display: "block",
                width: "100%",
                background: activeChatId === chat.id ? "#e0e0e0" : "none",
                color: "#000000ff",
                border: "none",
                borderRadius: "6px",
                padding: "8px 10px",
                marginBottom: "6px",
                textAlign: "left",
                cursor: "pointer",
                fontWeight: activeChatId === chat.id ? "bold" : "normal",
              }}
            >
              {chat.title}
            </button>
          ))}
        </div>
      </div>
      <div style={{ marginTop: "auto", textAlign: "left" }}>
        <a
          href="/profile"
          style={{ color: "#000000ff", textDecoration: "none" }}
        >
          <ProfileIcon size={20}>Profile</ProfileIcon>
        </a>
      </div>
      <div
        style={{
          textAlign: "left",
          marginTop: "20px",
        }}
      >
        <a
          href="/logout"
          style={{
            color: "#000000ff",
            textDecoration: "none",
          }}
        >
          <LogoutIcon size={20}>Logout</LogoutIcon>
        </a>
      </div>
    </div>
  );
};


export default Sidebar;
