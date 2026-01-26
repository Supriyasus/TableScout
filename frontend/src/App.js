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
  const [userId, setUserId] = useState(
    localStorage.getItem("user_id")
  );
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

  // const sendMessage = async () => {
  //   if (!input.trim()) return;

  //   setMessages((m) => [...m, { role: "user", text: input }]);
  //   const query = input;
  //   setInput("");

  //   setMessages((m) => [
  //     ...m,
  //     { role: "ai", text: "Checking nearby places considering traffic and crowd…" }
  //   ]);

  //   const places = await fetchPlaces(query);

  //   setMessages((m) => [
  //     ...m,
  //     { role: "ai", type: "places", data: places },
  //     { role: "ai", text: "Would you like me to book one of these?" }
  //   ]);
  // };



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
      const { latitude, longitude } = await getUserLocation(); // ✅ Get location
      const places = await fetchPlaces(query, latitude, longitude); // ✅ Pass it

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

  return (
    <div className="app-root">
      {/* Navbar */}
      <div className="navbar">
        <div className="nav-title">TableScout</div>
        <div className="nav-menu">
          <button
            className="menu-btn"
            onClick={() => setMenuOpen(!menuOpen)}
          >
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
                          <PlaceCard key={p.id} place={p} />
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
        <Route path="/about" element={<About />} /> {/* About Page Route */}
      </Routes>
      {showAbout && <About onClose={() => setShowAbout(false)} />}

    </div>
  );
}
