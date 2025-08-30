import React, { useState } from "react";
import GoogleIcon from "../assets/GoogleIcon";
import App from "../App";

const LoginPage = () => {
  const [email, setEmail] = useState("");

  return (
    <div
      style={{
        height: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: "400px",
          background: "transparent",
          padding: "32px 24px",
          boxSizing: "border-box",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <h1
          style={{
            textAlign: "center",
            fontSize: "2rem",
            fontWeight: 600,
            marginBottom: "12px",
            width: "100%",
            color: "black",
          }}
        >
          Log in
        </h1>
        <div
          style={{
            textAlign: "center",
            color: "#6b7280",
            fontSize: "1rem",
            marginBottom: "28px",
            width: "100%",
          }}
        >
          You’ll get smarter responses and can upload files, images, and more.
        </div>
        <input
          type="email"
          placeholder="Email Address"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={{
            width: "100%",
            padding: "16px",
            borderRadius: "28px",
            border: "1px solid #e5e7eb",
            fontSize: "1rem",
            marginBottom: "16px",
            outline: "none",
            boxSizing: "border-box",
            textAlign: "center",
            background: "#e5e7ebff",
            color: "black",
          }}
        />
        <button
          style={{
            width: "100%",
            padding: "16px",
            borderRadius: "28px",
            background: "#000000ff",
            color: "#ffffffff",
            fontWeight: 600,
            fontSize: "1rem",
            border: "none",
            marginBottom: "24px",
            cursor: "pointer",
          }}
        >
          Continue
        </button>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            margin: "24px 0",
            width: "100%",
          }}
        >
          <hr
            style={{ flex: 1, border: "none", borderTop: "1px solid #e5e7eb" }}
          />
          <span style={{ margin: "0 12px", color: "#6b7280", fontWeight: 500 }}>
            OR
          </span>
          <hr
            style={{ flex: 1, border: "none", borderTop: "1px solid #e5e7eb" }}
          />
        </div>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: "16px",
            width: "100%",
          }}
        >
          <button
            style={{
              width: "100%",
              height: "52px",
              padding: "14px",
              borderRadius: "28px",
              border: "1px solid #e5e7eb",
              background: "#fff",
              display: "flex",
              alignItems: "center",
              gap: "12px",
              fontSize: "1rem",
              cursor: "pointer",
              justifyContent: "center",
              color: "black",
            }}
          >
            <span
              style={{ display: "flex", alignItems: "center", lineHeight: 0 }}
            >
              <GoogleIcon size={24}></GoogleIcon>
            </span>
            Continue with Google
          </button>
        </div>
        <div
          style={{
            textAlign: "center",
            marginTop: "40px",
            color: "#6b7280",
            fontSize: "0.95rem",
            width: "100%",
          }}
        >
          <a
            href="#"
            style={{
              color: "#6b7280",
              textDecoration: "underline",
              marginRight: "12px",
            }}
          >
            Terms of Use
          </a>
          |
          <a
            href="#"
            style={{
              color: "#6b7280",
              textDecoration: "underline",
              marginLeft: "12px",
            }}
          >
            Privacy Policy
          </a>
        </div>
      </div>
    </div>
  );
};


export default LoginPage;
