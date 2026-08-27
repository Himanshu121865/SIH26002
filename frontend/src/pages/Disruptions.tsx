import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import MapContainer from "../components/MapContainer";
import { getDisruptions, type Disruption } from "../api";

function Disruptions() {
  const { t } = useTranslation();
  const [disruptions, setDisruptions] = useState<Disruption[]>([]);

  useEffect(() => {
    getDisruptions()
      .then((d) => setDisruptions(d.disruptions))
      .catch(console.error);
    const interval = setInterval(() =>
      getDisruptions().then((d) => setDisruptions(d.disruptions)).catch(console.error), 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <div className="page-header">
        <h2>{t("disruptions.title")}</h2>
        <p>{t("disruptions.description")}</p>
      </div>
      <div className="dashboard-layout">
        <div className="dashboard-map-card">
          <div className="card-header">
            <h3>Disruption Map</h3>
            <span className="severity-badge critical">{disruptions.length} active</span>
          </div>
          <div style={{ position: "relative" }}>
            <MapContainer showDisruptions showHeatmap />
          </div>
        </div>
        <div className="card">
          <h3>{t("disruptions.count")} ({disruptions.length})</h3>
          <div className="list-scroll">
            {disruptions.map((d) => (
              <div key={d.id} className="disruption-item">
                <div className="alert-item-header">
                  <span className={`severity-badge ${d.severity}`}>{d.severity}</span>
                  <span style={{ fontWeight: 600, marginLeft: "0.4rem", fontSize: "0.82rem" }}>
                    {d.type.replace(/_/g, " ")}
                  </span>
                </div>
                <div className="alert-message">{d.description}</div>
                <div className="alert-time">
                  {new Date(d.time).toLocaleString()} — ({d.lat.toFixed(2)}, {d.lon.toFixed(2)})
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Disruptions;
