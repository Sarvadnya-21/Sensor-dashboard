import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export const api = axios.create({ baseURL: API_BASE });

export const fetchStats = () => api.get("/stats").then((r) => r.data);
export const fetchData = (params) => api.get("/data", { params }).then((r) => r.data);
export const fetchAlerts = (params) => api.get("/alerts", { params }).then((r) => r.data);
