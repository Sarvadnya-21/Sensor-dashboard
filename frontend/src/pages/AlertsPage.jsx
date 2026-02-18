import React, { useEffect, useState } from "react";
import { fetchAlerts } from "../api/client";

const PAGE_SIZE = 25;

function AlertsPage() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [page, setPage] = useState(0);

  useEffect(() => {
    setLoading(true);
    fetchAlerts({ skip: page * PAGE_SIZE, limit: PAGE_SIZE })
      .then((d) => {
        setAlerts(d);
        setError("");
      })
      .catch((e) => {
        console.error(e);
        setError("Failed to load alerts.");
      })
      .finally(() => setLoading(false));
  }, [page]);

  const totalPages = Math.max(1, Math.ceil(alerts.length / PAGE_SIZE) || 1);
  const showNext = alerts.length === PAGE_SIZE;

  return (
    <div className="page">
      <h2>Alerts</h2>
      {loading ? (
        <p>Loading alerts...</p>
      ) : error ? (
        <p className="error">{error}</p>
      ) : (
        <>
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Time</th>
                  <th>Topic</th>
                  <th>Parameter</th>
                  <th>Threshold</th>
                  <th>Actual</th>
                  <th>Message</th>
                </tr>
              </thead>
              <tbody>
                {alerts.map((a) => (
                  <tr key={a.id} className="alert-row">
                    <td>{new Date(a.timestamp).toLocaleString()}</td>
                    <td>{a.topic}</td>
                    <td className="highlight-param">{a.violated_key}</td>
                    <td>{a.threshold_value}</td>
                    <td>{a.actual_value}</td>
                    <td>{a.message}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {alerts.length === 0 && <p>No alerts yet.</p>}
          <div className="pagination">
            <button
              onClick={() => setPage((p) => Math.max(p - 1, 0))}
              disabled={page === 0}
            >
              Previous
            </button>
            <span>Page {page + 1}</span>
            <button
              onClick={() => setPage((p) => p + 1)}
              disabled={!showNext}
            >
              Next
            </button>
          </div>
        </>
      )}
    </div>
  );
}

export default AlertsPage;
