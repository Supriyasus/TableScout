// components/Home.jsx
import { useState } from "react";
import PlaceCard from "./PlaceCard";
import About from "./About";
import { fetchPlaces } from "../api";

export default function Home({ userId, onLogout }) {
  const [messages, setMessages] = useState([
    { role: "ai", text: "Hi! What are you looking for today?" }
  ]);
  const [input, setInput] = useState("");
  const [menuOpen, setMenuOpen] = useState(false);
  const [showAbout, setShowAbout] = useState(false);
  const API_BASE = process.env.REACT_APP_API_URL ? `${process.env.REACT_APP_API_URL}/v1` : "http://127.0.0.1:8000/api/v1";

  const sendMessage = async () => {
    if (!input.trim()) return;

    setMessages((m) => [...m, { role: "user", text: input }]);
    const query = input;
    setInput("");

    setMessages((m) => [
      ...m,
      { role: "ai", text: "Checking nearby places considering traffic and crowd…" }
    ]);

    try {
      const res = await fetch("https://ipapi.co/json/");
      const loc = await res.json();
      const places = await fetchPlaces(query, loc.latitude, loc.longitude);

      setMessages((m) => [
        ...m,
        { role: "ai", type: "places", data: places },
        { role: "ai", text: "Would you like me to book one of these?" }
      ]);
    } catch (err) {
      setMessages((m) => [
        ...m,
        { role: "ai", text: "Sorry, I couldn't fetch recommendations right now." }
      ]);
    }
  };

  const handleBooking = async (placeId) => {
    const token = localStorage.getItem("access_token");
    const time = new Date().toISOString();

    const res = await fetch(`${API_BASE}/booking`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({ place_id: placeId, time })
    });

    const data = await res.json();
    alert(data.message || "Booking failed");
  };

  return (
    <div className="app-root">
      <div className="navbar">
        <div className="nav-title">TableScout</div>
        <div className="nav-menu">
          <button className="menu-btn" onClick={() => setMenuOpen(!menuOpen)}>
            ☰
          </button>
          {menuOpen && (
            <div className="dropdown">
              <button
                className="dropdown-item"
                onClick={() => {
                  setShowAbout(true);
                  setMenuOpen(false);
                }}
              >
                About Us
              </button>
              <button className="dropdown-item danger" onClick={onLogout}>
                Logout
              </button>
            </div>
          )}
        </div>
      </div>

      <div className="chat-container">
        {messages.map((msg, i) => (
          <div key={i}>
            {msg.role === "user" && (
              <div className="message-user">
                <span>{msg.text}</span>
              </div>
            )}
            {msg.role === "ai" && msg.text && (
              <div className="message-ai">
                <span>{msg.text}</span>
              </div>
            )}
            {msg.type === "places" && (
              <div className="places-wrapper">
                {msg.data.map((p) => (
                  <div key={p.id} className="place-card">
                    <PlaceCard place={p} />
                    <button onClick={() => handleBooking(p.id)}>Book</button>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="input-wrapper">
        <div className="input-bar">
          <input
            placeholder="Ask for nearby places…"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />
          <button onClick={sendMessage}>Send</button>
        </div>
      </div>

      {showAbout && <About onClose={() => setShowAbout(false)} />}
    </div>
  );
}
