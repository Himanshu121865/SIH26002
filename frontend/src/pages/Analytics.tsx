import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import {
  PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
} from "recharts";
import { getAnalytics, type Analytics } from "../api";

const COLORS = ["#3b82f6", "#ef4444", "#f59e0b", "#22c55e", "#8b5cf6", "#ec4899", "#06b6d4"];

const CustomTooltip = ({ active, payload }: any) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{
      background: "rgba(21, 29, 46, 0.95)",
      border: "1px solid #253049",
      borderRadius: 8,
      padding: "8px 12px",
      fontSize: "0.78rem",
    }}>
      <div style={{ fontWeight: 600 }}>{payload[0].name || payload[0].payload?.name}</div>
      <div style={{ color: "#94a3b8" }}>{payload[0].value}</div>
    </div>
  );
};

function AnalyticsPage() {
  const { t } = useTranslation();
  const [data, setData] = useState<Analytics | null>(null);

  useEffect(() => {
    getAnalytics().then(setData).catch(console.error);
  }, []);

  if (!data) return <div style={{ padding: "2rem", color: "var(--text-secondary)" }}>Loading analytics...</div>;

  const disruptionTypeData = Object.entries(data.disruptions_by_type).map(([name, value]) => ({
    name: name.replace(/_/g, " "),
    value,
  }));

  const disruptionSeverityData = Object.entries(data.disruptions_by_severity).map(([name, value]) => ({
    name,
    value,
  }));

  const roadsByStateData = Object.entries(data.roads_by_state)
    .slice(0, 8)
    .map(([name, value]) => ({ name, density: value ?? 0 }));

  const vulnerabilityData = [
    { name: t("analytics.vulnerable"), value: data.vulnerable_roads },
    { name: t("analytics.safe"), value: data.safe_roads },
  ];

  return (
    <div>
      <div className="page-header">
        <h2>{t("analytics.title")}</h2>
        <p>Road network analysis and disruption patterns</p>
      </div>
      <div className="analytics-grid">
        <div className="card">
          <h3>{t("analytics.vulnerabilityOverview")}</h3>
          <div className="analytics-stat-row">
            <div className="analytics-stat">
              <div className="num" style={{ color: "var(--accent)" }}>{data.total_roads.toLocaleString()}</div>
              <div className="lbl">{t("analytics.totalRoads")}</div>
            </div>
            <div className="analytics-stat">
              <div className="num" style={{ color: "var(--danger)" }}>{data.vulnerable_roads}</div>
              <div className="lbl">{t("analytics.vulnerable")}</div>
            </div>
            <div className="analytics-stat">
              <div className="num" style={{ color: "var(--success)" }}>{data.safe_roads.toLocaleString()}</div>
              <div className="lbl">{t("analytics.safe")}</div>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie data={vulnerabilityData} cx="50%" cy="50%" innerRadius={50} outerRadius={80} dataKey="value"
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                labelLine={false}
              >
                <Cell fill="var(--danger)" />
                <Cell fill="var(--success)" />
              </Pie>
              <Tooltip content={<CustomTooltip />} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <h3>{t("analytics.disruptionByType")}</h3>
          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie data={disruptionTypeData} cx="50%" cy="50%" outerRadius={100} dataKey="value"
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                labelLine={false}
              >
                {disruptionTypeData.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
              <Legend wrapperStyle={{ fontSize: "0.72rem", color: "var(--text-secondary)" }} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <h3>{t("analytics.disruptionBySeverity")}</h3>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={disruptionSeverityData}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
              <XAxis dataKey="name" stroke="var(--text-secondary)" tick={{ fontSize: 11 }} />
              <YAxis stroke="var(--text-secondary)" tick={{ fontSize: 11 }} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="value" radius={[6, 6, 0, 0]}>
                {disruptionSeverityData.map((entry, i) => (
                  <Cell key={i} fill={
                    entry.name === "critical" ? "#ef4444" :
                    entry.name === "high" ? "#f97316" :
                    entry.name === "moderate" ? "#f59e0b" : "#22c55e"
                  } />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <h3>{t("analytics.roadsByState")}</h3>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={roadsByStateData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
              <XAxis type="number" stroke="var(--text-secondary)" tick={{ fontSize: 11 }} />
              <YAxis type="category" dataKey="name" width={130} stroke="var(--text-secondary)" tick={{ fontSize: 11 }} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="density" name="Road Density (km/km²)" fill="var(--accent)" radius={[0, 6, 6, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

export default AnalyticsPage;
