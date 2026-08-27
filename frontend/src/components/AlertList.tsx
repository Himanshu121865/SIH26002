import { useEffect, useState } from "react";
import { getAlerts, type Alert } from "../api";

function AlertList() {
  const [alerts, setAlerts] = useState<Alert[]>([]);

  useEffect(() => {
    getAlerts()
      .then((data) => setAlerts(data.alerts))
      .catch(console.error);
    const interval = setInterval(() =>
      getAlerts().then((d) => setAlerts(d.alerts)).catch(console.error), 60000);
    return () => clearInterval(interval);
  }, []);

  const severityColor = (s: string) => {
    if (s === "critical") return "var(--danger)";
    if (s === "high" || s === "warning") return "var(--warning)";
    return "var(--accent)";
  };

  return (
    <div className="card">
      <h3>Active Alerts ({alerts.length})</h3>
      {alerts.length === 0 ? (
        <p style={{ color: "var(--text-secondary)", padding: "1rem 0", fontSize: "0.82rem" }}>
          No active alerts
        </p>
      ) : (
        <div className="list-scroll" style={{ maxHeight: 220 }}>
          {alerts.map((a) => (
            <div key={a.id} className="alert-item">
              <div className="alert-item-header">
                <div className="alert-dot" style={{ background: severityColor(a.severity) }} />
                <span className="alert-title">{a.title}</span>
              </div>
              <div className="alert-message">{a.message}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default AlertList;
