import { useEffect, useState } from "react";
import { getNerWeather, type WeatherCity } from "../api";

function WeatherPanel() {
  const [cities, setCities] = useState<WeatherCity[]>([]);

  useEffect(() => {
    getNerWeather()
      .then((data) => setCities(data.cities))
      .catch(console.error);
    const interval = setInterval(() =>
      getNerWeather().then((d) => setCities(d.cities)).catch(console.error), 300000);
    return () => clearInterval(interval);
  }, []);

  const weatherEmoji = (code: number) => {
    if (code >= 95) return "\u26C8";
    if (code >= 80) return "\uD83C\uDF27";
    if (code >= 71) return "\u2744";
    if (code >= 61) return "\uD83C\uDF27";
    if (code >= 51) return "\uD83C\uDF26";
    if (code >= 3) return "\u2601";
    if (code >= 1) return "\u26C5";
    return "\u2600";
  };

  return (
    <div className="card">
      <h3>NER Weather</h3>
      {cities.length === 0 ? (
        <p style={{ color: "var(--text-secondary)", padding: "0.5rem 0", fontSize: "0.82rem" }}>
          Loading...
        </p>
      ) : (
        <div className="weather-grid">
          {cities.map((c) => (
            <div key={c.city} className="weather-row">
              <span className="weather-city">{c.city}</span>
              <span className="weather-desc">
                {weatherEmoji(c.weather_code)} {c.description}
              </span>
              <span className="weather-temp">{c.temperature_c.toFixed(0)}°C</span>
              <span
                className="weather-rain"
                style={{ color: c.rainfall_24h_mm > 20 ? "var(--warning)" : "var(--text-secondary)" }}
              >
                {c.rainfall_24h_mm.toFixed(1)}mm
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default WeatherPanel;
