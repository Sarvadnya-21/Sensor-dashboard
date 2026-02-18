import React, { useEffect, useState } from "react";
import { fetchStats } from "../api/client";

function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    setLoading(true);
    fetchStats()
      .then((d) => {
        setData(d);
        setError("");
      })
      .catch((e) => {
        console.error(e);
        setError("Failed to load dashboard. Is the backend running on http://localhost:8000?");
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Loading dashboard...</p>;
  if (error) return <p className="error">{error}</p>;
  if (!data) return null;

  const latest = data.latest_readings;
  const latestList = latest && typeof latest === "object" && latest.topic
    ? [{ topic: latest.topic, timestamp: latest.timestamp, ...latest.values }]
    : [];

  return (
    <div className="page">
      <h2>Dashboard</h2>
      <div className="cards">
        <div className="card">
          <h3>Total Messages</h3>
          <p className="metric-value">{data.total_messages}</p>
        </div>
        <div className="card">
          <h3>Total Alerts</h3>
          <p className="metric-value">{data.active_alerts_count}</p>
        </div>
      </div>

      <section className="section">
        <h3>Latest Reading</h3>
        {latestList.length === 0 ? (
          <p>No sensor data yet. Start the sensor simulator to publish MQTT messages.</p>
        ) : (
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Topic</th>
                  <th>Time</th>
                  <th>Temp (°C)</th>
                  <th>Humidity (%)</th>
                  <th>Voltage (V)</th>
                  <th>Current (A)</th>
                  <th>Pressure (hPa)</th>
                </tr>
              </thead>
              <tbody>
                {latestList.map((r) => (
                  <tr key={r.topic}>
                    <td>{r.topic}</td>
                    <td>{new Date(r.timestamp).toLocaleString()}</td>
                    <td>{r.temperature ?? "-"}</td>
                    <td>{r.humidity ?? "-"}</td>
                    <td>{r.voltage ?? "-"}</td>
                    <td>{r.current ?? "-"}</td>
                    <td>{r.pressure ?? "-"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
}

export default Dashboard;
