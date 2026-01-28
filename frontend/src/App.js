import { useState } from "react";
import { fetchPlaces } from "./api";
import PlaceCard from "./components/PlaceCard";
import Login from "./components/Login";
import Signup from "./components/Signup";
import { Routes, Route, useNavigate } from "react-router-dom";
import About from "./components/About";

async function getUserLocation() {
  return new Promise((resolve) => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          resolve({
            latitude: pos.coords.latitude,
            longitude: pos.coords.longitude,
          });
        },
        async () => {
          try {
            const res = await fetch("https://ipapi.co/json/");
            const data = await res.json();
            resolve({ latitude: data.latitude, longitude: data.longitude });
          } catch {
            resolve({ latitude: 0, longitude: 0 });
          }
        }
      );
    } else {
      resolve({ latitude: 0, longitude: 0 });
    }
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
  const navigate = useNavigate();

  if (!userId) {
    return authMode === "login" ? (
      <Login
        onAuthSuccess={(id) => setUserId(id)}
        switchToSignup={() => setAuthMode("signup")}
      />
    ) : (
      <Signup
        onAuthSuccess={(id) => setUserId(id)}
        switchToLogin={() => setAuthMode("login")}
      />
    );
  }

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
      const { latitude, longitude } = await getUserLocation();
      const places = await fetchPlaces(query, latitude, longitude);

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
      console.error("Error fetching places:", err);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_id");
    setUserId(null);
    setAuthMode("login");
  };

  async function handleBooking(placeId) {
    const token = localStorage.getItem("access_token");
    const time = new Date().toISOString();

    try {
      const res = await fetch("http://localhost:8000/api/v1/booking", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ place_id: placeId, time })
      });

      const data = await res.json();
      alert(data.message || "Booking failed");
    } catch (err) {
      alert("Booking failed. Please try again.");
      console.error("Booking error:", err);
    }
  }

  return (
    <div className="app-root">
      {/* Navbar */}
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
              <button className="dropdown-item danger" onClick={handleLogout}>
                Logout
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Routes */}
      <Routes>
        <Route
          path="/"
          element={
            <>
              {/* Chat UI */}
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
                            <button onClick={() => handleBooking(p.id)}>
                              Book
                            </button>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>

              {/* Input */}
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
            </>
          }
        />
        <Route path="/about" element={<About />} />
      </Routes>
      {showAbout && <About onClose={() => setShowAbout(false)} />}
    </div>
  );
}
