export default function PlaceCard({ place }) {
  return (
    <div className="bg-zinc-900 p-4 rounded-2xl border border-zinc-800">
      <div className="flex justify-between">
        <h3 className="font-semibold">{place.name}</h3>
      </div>
      <div className="text-sm text-zinc-400 mt-1">
        {place.distance} • {place.time} • Crowd: {place.crowd}
      </div>
      <p className="text-sm mt-2">{place.reason}</p>
    </div>
  );
}
