import { useState } from "react";

export default function BookingModal({ place, onClose }) {
  const [people, setPeople] = useState(2);

  return (
    <div className="fixed inset-0 bg-black/60 flex justify-center items-center">
      <div className="bg-zinc-900 p-6 rounded-2xl w-80 space-y-4">
        <h3 className="text-lg font-semibold">Book {place.name}</h3>

        <label className="text-sm text-zinc-400">Party Size</label>
        <input
          type="number"
          min="1"
          value={people}
          onChange={(e) => setPeople(e.target.value)}
          className="w-full p-2 bg-zinc-800 rounded-xl"
        />

        <button className="w-full bg-green-600 hover:bg-green-500 rounded-xl py-2">
          Confirm Booking
        </button>

        <button
          onClick={onClose}
          className="w-full text-sm text-zinc-400 hover:text-zinc-200"
        >
          Cancel
        </button>
      </div>
    </div>
  );
}
