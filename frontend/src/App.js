import { useState } from "react";
import { fetchPlaces } from "./api";
import PlaceCard from "./components/PlaceCard";
import Login from "./components/Login";
import Signup from "./components/Signup";
import { Routes, Route, useNavigate } from "react-router-dom";
import About from "./components/About";

// --- Geolocation Helper ---
async function getUserLocation() {
  return new Promise((resolve) => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => resolve({ latitude: pos.coords.latitude, longitude: pos.coords.longitude }),
        async () => {
            try {
                const res = await fetch("https://ipapi.co/json/");
                const data = await res.json();
                resolve({ latitude: data.latitude, longitude: data.longitude });
            } catch { resolve({ latitude: 0, longitude: 0 }); }
        }
      );
    } else { resolve({ latitude: 0, longitude: 0 }); }
  });
}

export default function App() {
  const [userId, setUserId] = useState(localStorage.getItem("user_id"));
  const [authMode, setAuthMode] = useState("login");
  const [showAbout, setShowAbout] = useState(false);
  const [messages, setMessages] = useState([
    { role: "ai", text: "Hi! What are you looking for today?" }
  ]);
  const [input, setInput] = useState("");
  const [menuOpen, setMenuOpen] = useState(false);
  
  // Login/Signup Checks
  if (!userId) {
    return authMode === "login" ? (
      <Login onAuthSuccess={(id) => setUserId(id)} switchToSignup={() => setAuthMode("signup")} />
    ) : (
      <Signup onAuthSuccess={(id) => setUserId(id)} switchToLogin={() => setAuthMode("login")} />
    );
  }

  const sendMessage = async () => {
    if (!input.trim()) return;

    // 1. Add User Message
    const userMsg = { role: "user", text: input };
    setMessages((m) => [...m, userMsg]);
    
    const query = input;
    setInput("");

    // 2. Add Loading Message
    setMessages((m) => [...m, { role: "ai", text: "Checking nearby places considering traffic and crowd…" }]);

    try {
      const { latitude, longitude } = await getUserLocation();
      const places = await fetchPlaces(query, latitude, longitude);

      // 3. Add Results Message
      setMessages((m) => [
        ...m,
        { role: "ai", type: "places", data: places },
        { role: "ai", text: "Would you like me to book one of these?" }
      ]);
    } catch (err) {
      setMessages((m) => [...m, { role: "ai", text: "Sorry, I couldn't fetch recommendations right now." }]);
      console.error("Error fetching places:", err);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_id");
    setUserId(null);
    setAuthMode("login");
  };

  // --- AGENTIC BOOKING LOGIC ---
  async function handleBooking(place) {
    const token = localStorage.getItem("access_token");
    const time = new Date().toISOString();
    
    // 1. Data Extraction (Robust)
    // api.js flattens the object, so we prioritize place.website, fallback to properties
    const rawWebsite = place.website || place.properties?.metadata?.website;
    const rawPhone = place.phone || place.properties?.metadata?.phone;
    const name = place.name || place.properties?.name || "Unknown";
    const address = place.address || place.properties?.place_name || "";
    
    let bookingUrl = rawWebsite || null; 
    let actionType = "direct"; 

    // 2. Fallback Logic (Client Side Immediate Decision)
    if (!bookingUrl) {
        if (rawPhone) {
            actionType = "phone";
            bookingUrl = `tel:${rawPhone}`;
        } else {
            actionType = "fallback";
            // Pre-calculate a Google Search link in case backend fails or just for immediate open
            const query = encodeURIComponent(`Book table at ${name} ${address}`);
            bookingUrl = `https://www.google.com/search?q=${query}`;
        }
    }

    // 3. Immediate UI Action (Fixes Pop-up blockers)
    if (actionType === "phone") window.location.href = bookingUrl;
    else window.open(bookingUrl, "_blank");

    // 4. Agent Communication (Backend)
    try {
      fetch("http://localhost:8000/api/v1/booking", {
        method: "POST",
        headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
        body: JSON.stringify({ 
          place_id: place.id, // Normalized ID from api.js
          place_name: name,
          place_address: address, // Sent to Agent for context
          time: time,
          booking_url: actionType === "phone" ? null : bookingUrl 
        })
      }).then(res => res.json()).then(data => {
         // Show the Agent's reasoning message (e.g., "Redirecting to OpenTable...")
         if(data.message) alert(data.message); 
      });
    } catch (err) { console.error(err); }
  }

  return (
    <div className="app-root">
      {/* Navbar */}
      <div className="navbar">
        <div className="nav-title">TableScout</div>
        <div className="nav-menu">
          <button className="menu-btn" onClick={() => setMenuOpen(!menuOpen)}>☰</button>
          {menuOpen && (
            <div className="dropdown">
              <button className="dropdown-item" onClick={() => { setShowAbout(true); setMenuOpen(false); }}>About Us</button>
              <button className="dropdown-item danger" onClick={handleLogout}>Logout</button>
            </div>
          )}
        </div>
      </div>

      {/* Chat Area */}
      <div className="chat-container">
        {messages.map((msg, i) => (
          <div key={i}>
            {msg.role === "user" && <div className="message-user"><span>{msg.text}</span></div>}
            {msg.role === "ai" && msg.text && <div className="message-ai"><span>{msg.text}</span></div>}
            
            {msg.type === "places" && (
              <div className="places-wrapper">
                {msg.data.map((p) => (
                  // --- FIX: Added unique KEY here using 'p.id' ---
                  <div key={p.id} className="place-card">
                    <PlaceCard place={p} />
                    <button 
                        className="book-btn" 
                        onClick={() => handleBooking(p)}
                        style={{
                            marginTop: '10px',
                            padding: '8px 16px',
                            backgroundColor: p.website ? '#2ecc71' : '#3498db', 
                            color: 'white',
                            border: 'none',
                            borderRadius: '4px',
                            cursor: 'pointer'
                        }}
                    >
                      {p.website ? "Book on Website" : (p.phone ? "Call to Book" : "Find Table")}
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Input Area */}
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