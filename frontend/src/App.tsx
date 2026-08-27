import { Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Tracking from "./pages/Tracking";
import Disruptions from "./pages/Disruptions";
import Analytics from "./pages/Analytics";
import Districts from "./pages/Districts";
import Emergency from "./pages/Emergency";
import Reports from "./pages/Reports";
import Sidebar from "./components/Sidebar";
import "./App.css";

function App() {
  return (
    <div className="app">
      <Sidebar />
      <main className="main-content">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/tracking" element={<Tracking />} />
          <Route path="/disruptions" element={<Disruptions />} />
          <Route path="/districts" element={<Districts />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/emergency" element={<Emergency />} />
          <Route path="/reports" element={<Reports />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
