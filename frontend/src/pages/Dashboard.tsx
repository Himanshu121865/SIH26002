import { useTranslation } from "react-i18next";
import MapContainer from "../components/MapContainer";
import StatsGrid from "../components/StatsGrid";
import SiliguriMonitor from "../components/SiliguriMonitor";
import AlertList from "../components/AlertList";
import WeatherPanel from "../components/WeatherPanel";

function Dashboard() {
  const { t } = useTranslation();
  return (
    <div>
      <div className="page-header">
        <h2>{t("dashboard.title")}</h2>
        <p>Real-time monitoring across North Eastern Region</p>
      </div>
      <StatsGrid />
      <div className="dashboard-layout">
        <div className="dashboard-map-card">
          <div className="card-header">
            <h3>{t("dashboard.map")}</h3>
            <div style={{ display: "flex", gap: "0.5rem" }}>
              <span className="severity-badge low">Live</span>
            </div>
          </div>
          <div style={{ position: "relative" }}>
            <MapContainer showVehicles showDisruptions showHeatmap />
            <div className="map-legend">
              <h4>Legend</h4>
              <div className="legend-item">
                <div className="legend-dot" style={{ background: "#3b82f6" }} />
                <span>Vehicle</span>
              </div>
              <div className="legend-item">
                <div className="legend-dot" style={{ background: "#ef4444" }} />
                <span>Critical</span>
              </div>
              <div className="legend-item">
                <div className="legend-dot" style={{ background: "#f97316" }} />
                <span>High</span>
              </div>
              <div className="legend-item">
                <div className="legend-dot" style={{ background: "#eab308" }} />
                <span>Moderate</span>
              </div>
              <div className="legend-item">
                <div className="legend-line" style={{ background: "#3b82f6" }} />
                <span>Road Network</span>
              </div>
            </div>
          </div>
        </div>
        <div className="dashboard-sidebar">
          <SiliguriMonitor />
          <WeatherPanel />
          <AlertList />
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
