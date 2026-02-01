import { useState } from "react";

export default function Login({ onAuthSuccess, switchToSignup }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async () => {
    setError("");

    try {
      const res = await fetch("http://localhost:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      if (!res.ok) {
        throw new Error("Invalid credentials");
      }

      const data = await res.json();

      // Save token
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("user_id", data.user_id);

      onAuthSuccess(data.user_id);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="auth-card">
      <h2>Welcome To TableScout</h2>

      <input
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      {error && <div className="auth-error">{error}</div>}

      <button onClick={handleLogin}>Login</button>

      <p className="auth-switch">
        Don’t have an account?{" "}
        <span onClick={switchToSignup}>Sign up</span>
      </p>
    </div>
  );
}
