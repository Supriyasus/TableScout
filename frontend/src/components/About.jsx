import React from "react";
import "./About.css";

const About = ({ onClose }) => {
  const handleOverlayClick = (e) => {
    // Close if user clicks directly on the overlay (not inside modal-content)
    if (e.target.classList.contains("modal-overlay")) {
      onClose();
    }
  };

  return (
    <div className="modal-overlay" onClick={handleOverlayClick}>
      <div className="modal-content">
        <h1>About TableScout</h1>
        <p>
          We’re not just another “find‑a‑restaurant” app. TableScout is your wingman for nights out, lazy brunches, and spontaneous coffee runs.
        </p>
        <p>
          Instead of dumping endless lists, we actually <em>think</em> about what fits you right now. Traffic jam? We’ll steer you somewhere closer. Crowds too heavy? We’ll point you to a spot with breathing room. Looking for a vibe- chill café, buzzing bar, cozy bakery? We’ve got you.
        </p>
        <p>
          And when you’ve found the perfect place, you don’t have to switch apps or make awkward calls. With our built‑in Booking MCP (multi‑channel booking platform), you can reserve a table instantly- whether it’s a quick coffee catch‑up, a dinner for two, or a group hangout.
        </p>
        <p>
          Our mission is simple: make local discovery and booking feel less like work and more like serendipity. Every recommendation comes with context, and every booking comes with clarity. Because finding the right place - and securing it - should feel fun, not frustrating.
        </p>
        <button className="close-btn" onClick={onClose}>✕</button>
      </div>
    </div>
  );
};

export default About;
