import { useEffect, useState } from "react";
import MapContainer from "../components/MapContainer";
import { getDisruptions, getStats, type Disruption, type Stats } from "../api";

function EmergencyCorridors() {
  const [disruptions, setDisruptions] = useState<Disruption[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);

  useEffect(() => {
    getDisruptions().then((d) => setDisruptions(d.disruptions)).catch(console.error);
    getStats().then(setStats).catch(console.error);
  }, []);

  const critical = disruptions.filter((d) => d.severity === "critical" || d.severity === "high");
  const corridors = [
    { name: "Siliguri Corridor (Chicken Neck)", from: "Siliguri", to: "Gangtok", status: "congested", risk: "moderate" },
    { name: "NH-27 (Assam-Arunachal)", from: "Guwahati", to: "Itanagar", status: "operational", risk: "low" },
    { name: "NH-37 (Imphal-Jiribam)", from: "Imphal", to: "Jiribam", status: "disrupted", risk: "high" },
    { name: "NH-54 (Aizawl-Silchar)", from: "Aizawl", to: "Silchar", status: "operational", risk: "low" },
    { name: "NH-127A (Shillong-Dawki)", from: "Shillong", to: "Dawki", status: "operational", risk: "moderate" },
    { name: "NH-2 (Dimapur-Kohima)", from: "Dimapur", to: "Kohima", status: "operational", risk: "low" },
  ];

  const statusColor = (s: string) => {
    if (s === "disrupted") return "var(--danger)";
    if (s === "congested") return "var(--warning)";
    return "var(--success)";
  };

  const riskColor = (r: string) => {
    if (r === "high") return "var(--danger)";
    if (r === "moderate") return "var(--warning)";
    return "var(--success)";
  };

  return (
    <div>
      <div className="page-header">
        <h2>Emergency Corridors</h2>
        <p>Critical transport corridor status and disaster response routes</p>
      </div>

      <div className="dashboard-layout">
        <div className="dashboard-map-card">
          <div className="card-header">
            <h3>Disruption Map</h3>
            <span className="severity-badge critical">{critical.length} critical/high</span>
          </div>
          <div style={{ position: "relative" }}>
            <MapContainer showDisruptions showHeatmap />
          </div>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
          <div className="card">
            <h3>Corridor Status</h3>
            <div className="list-scroll" style={{ maxHeight: 300 }}>
              {corridors.map((c) => (
                <div key={c.name} className="alert-item">
                  <div className="alert-item-header">
                    <span style={{ fontWeight: 600, fontSize: "0.82rem" }}>{c.name}</span>
                  </div>
                  <div style={{ display: "flex", gap: "0.5rem", marginTop: "0.3rem" }}>
                    <span className="severity-badge" style={{
                      background: statusColor(c.status) + "20",
                      color: statusColor(c.status),
                    }}>
                      {c.status}
                    </span>
                    <span className="severity-badge" style={{
                      background: riskColor(c.risk) + "20",
                      color: riskColor(c.risk),
                    }}>
                      risk: {c.risk}
                    </span>
                  </div>
                  <div className="alert-time">{c.from} → {c.to}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="card">
            <h3>Active Disruptions ({critical.length})</h3>
            <div className="list-scroll" style={{ maxHeight: 200 }}>
              {critical.length === 0 ? (
                <p style={{ color: "var(--text-secondary)", fontSize: "0.82rem" }}>No critical disruptions</p>
              ) : (
                critical.map((d) => (
                  <div key={d.id} className="alert-item">
                    <div className="alert-item-header">
                      <span className={`severity-badge ${d.severity}`}>{d.severity}</span>
                      <span className="alert-title" style={{ marginLeft: "0.4rem" }}>
                        {d.type.replace(/_/g, " ")}
                      </span>
                    </div>
                    <div className="alert-message">{d.description}</div>
                    <div className="alert-time">
                      ({d.lat.toFixed(2)}, {d.lon.toFixed(2)})
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          {stats && (
            <div className="card">
              <h3>System Status</h3>
              <div style={{ fontSize: "0.82rem", lineHeight: 1.8 }}>
                <div>Monitored Roads: <strong>{stats.total_segments.toLocaleString()}</strong></div>
                <div>Active Disruptions: <strong style={{ color: "var(--danger)" }}>{stats.active_disruptions}</strong></div>
                <div>Active Alerts: <strong style={{ color: "var(--warning)" }}>{stats.active_alerts}</strong></div>
                <div>Fleet Vehicles: <strong>{stats.active_vehicles}</strong></div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default EmergencyCorridors;
