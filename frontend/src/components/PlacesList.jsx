export default function PlaceCard({ place, onClick, selected }) {
  return (
    <div
      className={`bg-zinc-900 p-4 rounded-2xl border cursor-pointer
      ${selected ? "border-green-500" : "border-zinc-800"}`}
      onClick={onClick}
    >
      <div className="flex justify-between">
        <h3 className="font-semibold">{place.name}</h3>
        <span className="text-sm text-zinc-400">⭐ {place.rating ?? "N/A"}</span>
      </div>

      <div className="text-sm text-zinc-400 mt-1">
        {place.distance ?? "?"} • {place.time ?? "?"} • Crowd: {place.crowd ?? "?"}
      </div>

      <p className="text-sm mt-2">{place.reason}</p>
    </div>
  );
}
