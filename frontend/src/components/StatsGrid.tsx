import { useEffect, useState } from "react";
import { getStats, type Stats } from "../api";

const ICONS = {
  vehicles: "M8 7h8m-8 4h8m-6 4h4M5 3h14a2 2 0 012 2v14a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2z",
  disruptions: "M12 9v2m0 4h.01M5.07 19H18.93a2 2 0 001.737-2.965L13.737 4.035a2 2 0 00-3.474 0L3.333 16.035A2 2 0 005.07 19z",
  roads: "M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l5.447 2.724A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7",
  alerts: "M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9",
};

function StatsGrid() {
  const [stats, setStats] = useState<Stats | null>(null);

  useEffect(() => {
    getStats().then(setStats).catch(console.error);
    const interval = setInterval(() => getStats().then(setStats).catch(console.error), 30000);
    return () => clearInterval(interval);
  }, []);

  const cards = stats
    ? [
        { key: "vehicles", label: "Active Vehicles", value: stats.active_vehicles, color: "accent" },
        { key: "disruptions", label: "Active Disruptions", value: stats.active_disruptions, color: "danger" },
        { key: "roads", label: "Roads Monitored", value: stats.total_segments, color: "success" },
        { key: "alerts", label: "Active Alerts", value: stats.active_alerts, color: "warning" },
      ]
    : [
        { key: "vehicles", label: "Active Vehicles", value: "...", color: "accent" },
        { key: "disruptions", label: "Active Disruptions", value: "...", color: "danger" },
        { key: "roads", label: "Roads Monitored", value: "...", color: "success" },
        { key: "alerts", label: "Active Alerts", value: "...", color: "warning" },
      ];

  return (
    <div className="stats-grid">
      {cards.map((s, i) => (
        <div key={s.key} className={`stat-card ${s.color} animate-in`} style={{ animationDelay: `${i * 0.05}s` }}>
          <div className="stat-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d={ICONS[s.key as keyof typeof ICONS]} />
            </svg>
          </div>
          <div className="stat-label">{s.label}</div>
          <div className="stat-value" style={{ color: `var(--${s.color})` }}>
            {typeof s.value === "number" ? s.value.toLocaleString() : s.value}
          </div>
        </div>
      ))}
    </div>
  );
}

export default StatsGrid;
