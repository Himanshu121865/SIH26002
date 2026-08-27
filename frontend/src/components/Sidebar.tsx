import { NavLink } from "react-router-dom";
import { useTranslation } from "react-i18next";

const NAV_ITEMS = [
  { to: "/", label: "nav.dashboard", icon: "M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-4 0a1 1 0 01-1-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 01-1 1h-2" },
  { to: "/tracking", label: "nav.tracking", icon: "M8 7h8m-8 4h8m-6 4h4M5 3h14a2 2 0 012 2v14a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2z" },
  { to: "/disruptions", label: "nav.disruptions", icon: "M12 9v2m0 4h.01M5.07 19H18.93a2 2 0 001.737-2.965L13.737 4.035a2 2 0 00-3.474 0L3.333 16.035A2 2 0 005.07 19z" },
  { to: "/districts", label: "nav.districts", icon: "M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z M15 11a3 3 0 11-6 0 3 3 0 016 0z" },
  { to: "/analytics", label: "nav.analytics", icon: "M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" },
  { to: "/emergency", label: "nav.emergency", icon: "M13 10V3L4 14h7v7l9-11h-7z" },
  { to: "/reports", label: "nav.reports", icon: "M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" },
];

const LANGUAGES = [
  { code: "en", label: "EN" },
  { code: "bn", label: "BN" },
  { code: "hi", label: "HI" },
  { code: "as", label: "AS" },
];

function Sidebar() {
  const { t, i18n } = useTranslation();

  return (
    <nav className="sidebar">
      <div className="sidebar-brand">
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
          <rect width="32" height="32" rx="8" fill="#3b82f6" fillOpacity="0.15" />
          <path d="M8 22L16 10L24 22H8Z" fill="#3b82f6" />
          <circle cx="16" cy="18" r="2" fill="white" />
        </svg>
        <div>
          <h1>NER Logistics</h1>
          <span>SIH 2026</span>
        </div>
      </div>

      <div className="sidebar-section">Navigation</div>

      {NAV_ITEMS.map((item) => (
        <NavLink
          key={item.to}
          to={item.to}
          end={item.to === "/"}
          className={({ isActive }) => isActive ? "active" : ""}
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d={item.icon} />
          </svg>
          <span>{t(item.label)}</span>
        </NavLink>
      ))}

      <div className="sidebar-footer">
        <div className="lang-label">Language</div>
        <div className="lang-buttons">
          {LANGUAGES.map((l) => (
            <button
              key={l.code}
              onClick={() => i18n.changeLanguage(l.code)}
              className={`lang-btn ${i18n.language === l.code ? "active" : ""}`}
            >
              {l.label}
            </button>
          ))}
        </div>
      </div>
    </nav>
  );
}

export default Sidebar;
