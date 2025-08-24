// Import the Munafah logo image
import logo from "../assets/munafah_logo.png";

// Import CSS styling for the navbar
import "../css_files/navbar.css";

// Import Link for client-side navigation

import React from "react";

function Navbar() {
  return (
    // Top-level header element styled as a navbar
    <header className="navbar">
      {/* Left side: Logo and navigation links */}
      <div className="navbar-component">
        <a className="navbar-logo">
          <img src={logo} alt="Munafah Logo" className="navbar-image" />
        </a>
        <a className="navbar-text" href="/landingpage">
          Home
        </a>
        {/* <a className="navbar-text" href="/pricing">
          Pricing
        </a> */}
        <a className="navbar-text" href="/about">
          About
        </a>
      </div>

      {/* Right side: Log In and Sign Up buttons */}
      <div className="navbar-component">
        <a href="/login" className="navbar-button navbar-login">
          Log In
        </a>
        <a href="/createaccount" className="navbar-button navbar-signup">
          Sign Up
        </a>
      </div>
    </header>
  );
}

export default Navbar;
