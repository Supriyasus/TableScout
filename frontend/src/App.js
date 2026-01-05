import { useState } from "react";
import { fetchPlaces } from "./api";
import PlaceCard from "./components/PlaceCard";

export default function App() {
  const [messages, setMessages] = useState([
    { role: "ai", text: "Hi! What are you looking for today?" }
  ]);
  const [input, setInput] = useState("");
  const [menuOpen, setMenuOpen] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    setMessages((m) => [...m, { role: "user", text: input }]);
    const query = input;
    setInput("");

    setMessages((m) => [
      ...m,
      { role: "ai", text: "Checking nearby places considering traffic and crowd…" }
    ]);

    const places = await fetchPlaces(query);

    setMessages((m) => [
      ...m,
      { role: "ai", type: "places", data: places },
      { role: "ai", text: "Would you like me to book one of these?" }
    ]);
  };

  return (
    <div className="app-root">
      {/* Top Navbar */}
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
              <div className="dropdown-item">About Us</div>
              <div className="dropdown-item">Logout</div>
            </div>
          )}
        </div>
      </div>

      {/* Chat */}
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
    </div>
  );
}
