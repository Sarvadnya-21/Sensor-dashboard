import React, { useEffect, useState } from "react";
import { fetchData } from "../api/client";

const PAGE_SIZE = 25;

function RawDataView() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [page, setPage] = useState(0);

  useEffect(() => {
    setLoading(true);
    fetchData({ skip: page * PAGE_SIZE, limit: PAGE_SIZE })
      .then((d) => {
        setRows(d);
        setError("");
      })
      .catch((e) => {
        console.error(e);
        setError("Failed to load sensor data.");
      })
      .finally(() => setLoading(false));
  }, [page]);

  const showNext = rows.length === PAGE_SIZE;

  return (
    <div className="page">
      <h2>Raw Sensor Data</h2>
      {loading ? (
        <p>Loading data...</p>
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
                  <th>Temp (°C)</th>
                  <th>Humidity (%)</th>
                  <th>Voltage (V)</th>
                  <th>Current (A)</th>
                  <th>Pressure (hPa)</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((r) => (
                  <tr key={r.id}>
                    <td>{new Date(r.timestamp).toLocaleString()}</td>
                    <td>{r.topic}</td>
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
          {rows.length === 0 && <p>No sensor data yet.</p>}
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

export default RawDataView;
