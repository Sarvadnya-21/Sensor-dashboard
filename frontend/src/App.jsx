import React from "react";
import { Routes, Route, NavLink } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import AlertsPage from "./pages/AlertsPage";
import RawDataView from "./pages/RawDataView";

function App() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="sidebar-header">
          <h1>Sensor Monitor</h1>
        </div>
        <nav className="nav">
          <NavLink to="/" end className="nav-link">
            Dashboard
          </NavLink>
          <NavLink to="/alerts" className="nav-link">
            Alerts
          </NavLink>
          <NavLink to="/raw-data" className="nav-link">
            Raw Data
          </NavLink>
        </nav>
      </aside>
      <main className="main-content">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/alerts" element={<AlertsPage />} />
          <Route path="/raw-data" element={<RawDataView />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
