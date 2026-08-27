import { useEffect, useState } from "react";
import { getDistricts, type District } from "../api";

function DistrictDashboard() {
  const [districts, setDistricts] = useState<District[]>([]);
  const [filter, setFilter] = useState<string>("all");

  useEffect(() => {
    getDistricts().then((d) => setDistricts(d.districts)).catch(console.error);
  }, []);

  const filtered = filter === "all" ? districts : districts.filter((d) => d.status === filter);

  const statusColor = (s: string) => {
    if (s === "good") return "var(--success)";
    if (s === "moderate") return "var(--warning)";
    return "var(--danger)";
  };

  const statusBg = (s: string) => {
    if (s === "good") return "var(--success-bg)";
    if (s === "moderate") return "var(--warning-bg)";
    return "var(--danger-bg)";
  };

  const grouped = filtered.reduce((acc, d) => {
    if (!acc[d.state]) acc[d.state] = [];
    acc[d.state].push(d);
    return acc;
  }, {} as Record<string, District[]>);

  const stats = {
    total: districts.length,
    good: districts.filter((d) => d.status === "good").length,
    moderate: districts.filter((d) => d.status === "moderate").length,
    poor: districts.filter((d) => d.status === "poor").length,
    totalPop: districts.reduce((s, d) => s + d.population, 0),
  };

  return (
    <div>
      <div className="page-header">
        <h2>District Connectivity</h2>
        <p>Road accessibility status across all 8 NER states</p>
      </div>

      <div className="stats-grid" style={{ marginBottom: "1.5rem" }}>
        <div className="stat-card success animate-in">
          <div className="stat-label">Total Districts</div>
          <div className="stat-value" style={{ color: "var(--accent)" }}>{stats.total}</div>
        </div>
        <div className="stat-card success animate-in" style={{ animationDelay: "0.05s" }}>
          <div className="stat-label">Good Connectivity</div>
          <div className="stat-value" style={{ color: "var(--success)" }}>{stats.good}</div>
        </div>
        <div className="stat-card warning animate-in" style={{ animationDelay: "0.1s" }}>
          <div className="stat-label">Moderate</div>
          <div className="stat-value" style={{ color: "var(--warning)" }}>{stats.moderate}</div>
        </div>
        <div className="stat-card danger animate-in" style={{ animationDelay: "0.15s" }}>
          <div className="stat-label">Poor Connectivity</div>
          <div className="stat-value" style={{ color: "var(--danger)" }}>{stats.poor}</div>
        </div>
      </div>

      <div style={{ display: "flex", gap: "0.5rem", marginBottom: "1.5rem" }}>
        {["all", "good", "moderate", "poor"].map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`lang-btn ${filter === f ? "active" : ""}`}
            style={{ textTransform: "capitalize" }}
          >
            {f}
          </button>
        ))}
      </div>

      {Object.entries(grouped).map(([state, dists]) => (
        <div key={state} style={{ marginBottom: "1.5rem" }}>
          <h3 style={{
            fontSize: "0.85rem", fontWeight: 600, color: "var(--text-primary)",
            marginBottom: "0.75rem", display: "flex", alignItems: "center", gap: "0.5rem",
          }}>
            {state}
            <span style={{ fontSize: "0.7rem", color: "var(--text-secondary)", fontWeight: 400 }}>
              ({dists.length} districts)
            </span>
          </h3>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))", gap: "0.75rem" }}>
            {dists.map((d) => (
              <div key={d.id} className="card" style={{ padding: "1rem" }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "0.5rem" }}>
                  <span style={{ fontWeight: 600, fontSize: "0.9rem" }}>{d.district}</span>
                  <span style={{
                    padding: "0.15rem 0.5rem", borderRadius: 4, fontSize: "0.65rem",
                    fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.03em",
                    background: statusBg(d.status), color: statusColor(d.status),
                  }}>
                    {d.status}
                  </span>
                </div>
                <div style={{ fontSize: "0.78rem", color: "var(--text-secondary)", lineHeight: 1.7 }}>
                  <div>Population: <strong>{d.population.toLocaleString()}</strong></div>
                  <div>Road Density: <strong>{d.road_density?.toFixed(2) || "N/A"} km/km²</strong></div>
                  <div>Connectivity: <strong style={{ color: statusColor(d.status) }}>
                    {d.connectivity_score ? (d.connectivity_score * 100).toFixed(0) : "N/A"}%
                  </strong></div>
                  <div>Resilience: <strong>{d.resilience_score ? (d.resilience_score * 100).toFixed(0) : "N/A"}%</strong></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

export default DistrictDashboard;
