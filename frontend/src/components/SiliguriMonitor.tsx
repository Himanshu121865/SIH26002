import { useEffect, useState } from "react";
import { getSiliguriStatus, type SiliguriStatus } from "../api";

function SiliguriMonitor() {
  const [status, setStatus] = useState<SiliguriStatus | null>(null);

  useEffect(() => {
    getSiliguriStatus().then(setStatus).catch(console.error);
    const interval = setInterval(() => getSiliguriStatus().then(setStatus).catch(console.error), 60000);
    return () => clearInterval(interval);
  }, []);

  const riskColor = (r: string) => {
    if (r === "critical" || r === "high") return "var(--danger)";
    if (r === "moderate") return "var(--warning)";
    return "var(--success)";
  };

  const statusColor = (s: string) => {
    if (s === "blocked") return "var(--danger)";
    if (s === "congested") return "var(--warning)";
    return "var(--success)";
  };

  return (
    <div className="card">
      <h3>Siliguri Corridor</h3>
      <div className="siliguri-status">
        <div
          className="siliguri-dot"
          style={{ background: status ? statusColor(status.status) : "var(--text-muted)" }}
        />
        <span style={{ fontSize: "1rem", fontWeight: 700 }}>
          {status ? status.status.toUpperCase() : "Loading..."}
        </span>
      </div>
      <p style={{ color: "var(--text-secondary)", fontSize: "0.78rem", marginTop: "0.35rem" }}>
        {status
          ? `${status.width_km}km corridor bottleneck`
          : "Fetching status..."}
      </p>
      <div className="siliguri-details">
        <div>
          Risk:{" "}
          <span style={{ color: status ? riskColor(status.risk_level) : "var(--text-secondary)", fontWeight: 600 }}>
            {status ? status.risk_level : "..."}
          </span>
        </div>
        <div>
          Weather: <span style={{ fontWeight: 600 }}>{status?.weather_impact || "..."}</span>
        </div>
        <div>
          Updated: <span style={{ fontWeight: 600 }}>{status ? new Date(status.last_updated).toLocaleTimeString() : "..."}</span>
        </div>
      </div>
    </div>
  );
}

export default SiliguriMonitor;
