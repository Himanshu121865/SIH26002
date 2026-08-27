import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import MapContainer from "../components/MapContainer";
import { getVehicles, type Vehicle } from "../api";

function Tracking() {
  const { t } = useTranslation();
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);

  useEffect(() => {
    getVehicles()
      .then((d) => setVehicles(d.vehicles))
      .catch(console.error);
    const interval = setInterval(() =>
      getVehicles().then((d) => setVehicles(d.vehicles)).catch(console.error), 15000);
    return () => clearInterval(interval);
  }, []);

  const typeColor = (type: string) => {
    if (type === "truck") return "#3b82f6";
    if (type === "van") return "#10b981";
    return "#f59e0b";
  };

  return (
    <div>
      <div className="page-header">
        <h2>{t("tracking.title")}</h2>
        <p>Real-time fleet positions across NER corridors</p>
      </div>
      <div className="dashboard-layout">
        <div className="dashboard-map-card">
          <div className="card-header">
            <h3>Fleet Map</h3>
            <span className="severity-badge low">{vehicles.length} vehicles</span>
          </div>
          <div style={{ position: "relative" }}>
            <MapContainer showVehicles />
          </div>
        </div>
        <div className="card">
          <h3>{t("tracking.fleet")} ({vehicles.length})</h3>
          <div className="list-scroll">
            {vehicles.map((v) => (
              <div key={v.vehicle_id} className="fleet-item">
                <div className="fleet-item-header">
                  <span style={{ fontWeight: 600 }}>{v.vehicle_id}</span>
                  <span style={{ color: "var(--text-secondary)", fontSize: "0.75rem" }}>
                    {v.speed_kmh} km/h
                  </span>
                </div>
                <div style={{ color: "var(--text-secondary)", fontSize: "0.78rem", marginTop: "0.2rem" }}>
                  {v.driver_name}
                </div>
                <div style={{ display: "flex", justifyContent: "space-between", marginTop: "0.3rem" }}>
                  <span
                    className="severity-badge"
                    style={{
                      background: `${typeColor(v.vehicle_type)}20`,
                      color: typeColor(v.vehicle_type),
                    }}
                  >
                    {v.vehicle_type}
                  </span>
                  <span style={{ color: "var(--text-muted)", fontSize: "0.7rem" }}>
                    {v.cargo_type}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Tracking;
