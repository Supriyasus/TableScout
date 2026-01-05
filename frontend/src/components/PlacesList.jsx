import PlaceCard from "./PlaceCard";

export default function PlacesList({ places, onSelect, selected }) {
  if (!places.length) return null;

  return (
    <div className="space-y-4">
      {places.map((place) => (
        <PlaceCard
          key={place.id}
          place={place}
          onClick={() => onSelect(place)}
          selected={selected?.id === place.id}
        />
      ))}
    </div>
  );
}
