// Import CSS styling for the navbar
import "../css_files/navbar.css";

// Import Link for client-side navigation

import React from "react";

function Navbar() {
  return (
    // Top-level header element styled as a navbar
    <header className="navbar">
      {/* Left side: Logo and navigation links */}
      <div className="navbar-text navbar-logo">
        Medilens
      </div>
      <div className="navbar-component">
        <a className="navbar-text" href="/">
          Home
        </a>
        {/* <a className="navbar-text" href="/pricing">
          Pricing
        </a> */}
        <a className="navbar-text" href="/">
          About
        </a>
      </div>

      {/* Right side: Log In and Sign Up buttons */}
      <div className="navbar-component">
        <a href="/" className="navbar-button navbar-login">
          Log In
        </a>
        <a href="/" className="navbar-button navbar-login">
          Sign Up
        </a>
      </div>
    </header>
  );
}

export default Navbar;
