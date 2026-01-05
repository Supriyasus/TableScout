import { useState } from "react";

export default function SearchForm({ onSearch }) {
  const [query, setQuery] = useState("");

  return (
    <div className="bg-zinc-900 p-4 rounded-2xl space-y-3">
      <input
        className="w-full p-3 rounded-xl bg-zinc-800 outline-none focus:ring-2 focus:ring-indigo-500"
        placeholder="e.g. Quiet café to work under ₹300 at 5 PM"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button
        className="w-full bg-indigo-600 hover:bg-indigo-500 transition rounded-xl py-2"
        onClick={() => onSearch(query)}
      >
        Find Places
      </button>
    </div>
  );
}
