import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import { submitReport, getRecentReports, type Report } from "../api";
import { saveReportOffline, getPendingReports, syncPendingReports, isOnline } from "../offline";

function Reports() {
  const { t } = useTranslation();
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [pendingCount, setPendingCount] = useState(0);
  const [syncing, setSyncing] = useState(false);
  const [online, setOnline] = useState(isOnline());
  const [form, setForm] = useState({
    report_type: "road_damage",
    title: "",
    description: "",
    severity: "moderate",
  });

  const loadReports = () => {
    getRecentReports().then((d) => setReports(d.reports)).catch(console.error);
    getPendingReports().then((p) => setPendingCount(p.length)).catch(console.error);
  };

  useEffect(() => {
    loadReports();
    const handleOnline = () => { setOnline(true); handleSync(); };
    const handleOffline = () => setOnline(false);
    window.addEventListener("online", handleOnline);
    window.addEventListener("offline", handleOffline);
    return () => {
      window.removeEventListener("online", handleOnline);
      window.removeEventListener("offline", handleOffline);
    };
  }, []);

  const handleSync = async () => {
    setSyncing(true);
    const count = await syncPendingReports();
    if (count > 0) loadReports();
    setSyncing(false);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setSuccess(false);

    const report = {
      ...form,
      lat: 26.14 + Math.random() * 2,
      lon: 91.73 + Math.random() * 3,
    };

    if (isOnline()) {
      try {
        await submitReport(report);
        setSuccess(true);
        setForm({ report_type: "road_damage", title: "", description: "", severity: "moderate" });
        loadReports();
        setTimeout(() => setSuccess(false), 3000);
      } catch {
        await saveReportOffline({ ...report, id: `offline-${Date.now()}` });
        setPendingCount((p) => p + 1);
        setSuccess(true);
        setTimeout(() => setSuccess(false), 3000);
      }
    } else {
      await saveReportOffline({ ...report, id: `offline-${Date.now()}` });
      setPendingCount((p) => p + 1);
      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000);
    }
    setLoading(false);
  };

  return (
    <div>
      <div className="page-header">
        <h2>{t("reports.title")}</h2>
        <p>{t("reports.description")}</p>
        <div style={{ display: "flex", gap: "0.75rem", marginTop: "0.5rem", alignItems: "center" }}>
          <span className={`severity-badge ${online ? "low" : "critical"}`}>
            {online ? "Online" : "Offline"}
          </span>
          {pendingCount > 0 && (
            <button
              onClick={handleSync}
              disabled={syncing || !online}
              className="btn-primary"
              style={{ fontSize: "0.75rem", padding: "0.3rem 0.8rem" }}
            >
              {syncing ? "Syncing..." : `Sync ${pendingCount} pending`}
            </button>
          )}
        </div>
      </div>
      <div className="dashboard-layout">
        <div className="card">
          <h3>{t("reports.submit")}</h3>
          {!online && (
            <div style={{
              background: "var(--warning-bg)", color: "var(--warning)", padding: "0.5rem 0.75rem",
              borderRadius: "var(--radius-sm)", fontSize: "0.78rem", marginBottom: "0.75rem",
            }}>
              You're offline. Reports will be saved locally and synced when you reconnect.
            </div>
          )}
          <form onSubmit={handleSubmit} className="report-form">
            <div className="form-row">
              <div className="form-group">
                <label>{t("reports.type")}</label>
                <select
                  value={form.report_type}
                  onChange={(e) => setForm({ ...form, report_type: e.target.value })}
                >
                  <option value="road_damage">{t("reports.types.road_damage")}</option>
                  <option value="landslide">{t("reports.types.landslide")}</option>
                  <option value="flooding">{t("reports.types.flooding")}</option>
                  <option value="accident">{t("reports.types.accident")}</option>
                  <option value="weather">{t("reports.types.weather")}</option>
                  <option value="other">{t("reports.types.other")}</option>
                </select>
              </div>
              <div className="form-group">
                <label>{t("reports.title_label")}</label>
                <input
                  type="text"
                  value={form.title}
                  onChange={(e) => setForm({ ...form, title: e.target.value })}
                  required
                  placeholder="Brief title..."
                />
              </div>
            </div>
            <div className="form-group">
              <label>{t("reports.description_label")}</label>
              <textarea
                value={form.description}
                onChange={(e) => setForm({ ...form, description: e.target.value })}
                required
                rows={3}
                placeholder="Describe the situation..."
              />
            </div>
            <div style={{ display: "flex", gap: "0.75rem", alignItems: "center" }}>
              <div className="form-group" style={{ marginBottom: 0 }}>
                <label>Severity</label>
                <select
                  value={form.severity}
                  onChange={(e) => setForm({ ...form, severity: e.target.value })}
                >
                  <option value="low">Low</option>
                  <option value="moderate">Moderate</option>
                  <option value="high">High</option>
                  <option value="critical">Critical</option>
                </select>
              </div>
              <button type="submit" disabled={loading} className="btn-primary">
                {loading ? t("reports.submitting") : t("reports.submit")}
              </button>
              {success && <span className="success-msg">{t("reports.success")}</span>}
            </div>
          </form>
        </div>

        <div className="card">
          <h3>Recent Reports ({reports.length})</h3>
          <div className="list-scroll">
            {reports.length === 0 ? (
              <p style={{ color: "var(--text-secondary)", padding: "1rem 0", fontSize: "0.82rem" }}>
                No reports yet
              </p>
            ) : (
              reports.map((r) => (
                <div key={r.id} className="alert-item">
                  <div className="alert-item-header">
                    <span className={`severity-badge ${r.severity}`}>{r.severity}</span>
                    <span className="alert-title" style={{ marginLeft: "0.4rem" }}>{r.title}</span>
                  </div>
                  <div className="alert-message">{r.description}</div>
                  <div className="alert-time">
                    {r.type.replace(/_/g, " ")} — {new Date(r.created_at).toLocaleString()}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Reports;
