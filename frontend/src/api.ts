const API_BASE = "/api/v1";

export interface Stats {
  total_segments: number;
  vulnerable_segments: number;
  active_vehicles: number;
  active_disruptions: number;
  active_alerts: number;
  by_type: Record<string, number>;
}

export interface Vehicle {
  vehicle_id: string;
  driver_name: string;
  lat: number;
  lon: number;
  speed_kmh: number;
  heading: number;
  vehicle_type: string;
  cargo_type: string;
  last_updated: string;
}

export interface Disruption {
  id: string;
  type: string;
  severity: string;
  lat: number;
  lon: number;
  description: string;
  time: string;
}

export interface Alert {
  id: string;
  type: string;
  severity: string;
  title: string;
  message: string;
  lat: number;
  lon: number;
  created_at: string;
}

export interface WeatherCity {
  city: string;
  lat: number;
  lon: number;
  temperature_c: number;
  rainfall_1h_mm: number;
  rainfall_24h_mm: number;
  wind_speed_kmh: number;
  humidity_pct: number;
  weather_code: number;
  description: string;
}

export interface SiliguriStatus {
  corridor: string;
  width_km: number;
  status: string;
  risk_level: string;
  weather_impact: string;
  last_updated: string;
}

export interface DisruptionPrediction {
  lat: number;
  lon: number;
  risk_score: number;
  risk_level: string;
  contributing_factors: string[];
}

async function fetchJSON<T>(path: string): Promise<T> {
  const resp = await fetch(`${API_BASE}${path}`);
  if (!resp.ok) throw new Error(`API error: ${resp.status}`);
  return resp.json();
}

export async function getStats(): Promise<Stats> {
  return fetchJSON<Stats>("/routing/stats");
}

export async function getVehicles(): Promise<{ vehicles: Vehicle[]; count: number }> {
  return fetchJSON("/tracking/vehicles");
}

export async function getDisruptions(): Promise<{ disruptions: Disruption[] }> {
  return fetchJSON("/routing/disruptions");
}

export async function getAlerts(): Promise<{ alerts: Alert[]; count: number }> {
  return fetchJSON("/alerts/active");
}

export async function getSiliguriStatus(): Promise<SiliguriStatus> {
  return fetchJSON("/routing/siliguri-status");
}

export async function getNerWeather(): Promise<{ cities: WeatherCity[] }> {
  return fetchJSON("/routing/ner-weather");
}

export async function getWeather(lat: number, lon: number): Promise<WeatherCity> {
  return fetchJSON(`/routing/weather?lat=${lat}&lon=${lon}`);
}

export async function predictDisruption(
  lat: number,
  lon: number,
  slopeDeg: number = 20,
  elevationM: number = 500
): Promise<DisruptionPrediction> {
  return fetchJSON(
    `/routing/predict-disruption?lat=${lat}&lon=${lon}&slope_deg=${slopeDeg}&elevation_m=${elevationM}`
  );
}

export async function getRoadsGeoJSON(): Promise<GeoJSON.FeatureCollection> {
  return fetchJSON("/routing/roads.geojson");
}

export interface Analytics {
  total_roads: number;
  vulnerable_roads: number;
  safe_roads: number;
  roads_by_type: Record<string, number>;
  disruptions_by_type: Record<string, number>;
  disruptions_by_severity: Record<string, number>;
  roads_by_state: Record<string, number>;
}

export async function getAnalytics(): Promise<Analytics> {
  return fetchJSON("/routing/analytics");
}

export interface FieldReport {
  report_type: string;
  title: string;
  description: string;
  lat: number;
  lon: number;
  severity: string;
}

export async function submitReport(report: FieldReport): Promise<{ status: string; report_id: string }> {
  const resp = await fetch(`${API_BASE}/reports/submit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(report),
  });
  if (!resp.ok) throw new Error(`API error: ${resp.status}`);
  return resp.json();
}

export interface Report {
  id: string;
  type: string;
  title: string;
  description: string;
  lat: number;
  lon: number;
  severity: string;
  status: string;
  created_at: string;
}

export async function getRecentReports(): Promise<{ reports: Report[]; count: number }> {
  return fetchJSON("/reports/recent");
}

export interface District {
  id: string;
  state: string;
  district: string;
  population: number;
  road_density: number;
  connectivity_score: number;
  resilience_score: number;
  active_disruptions: number;
  status: string;
}

export async function getDistricts(): Promise<{ districts: District[] }> {
  return fetchJSON("/routing/districts");
}

export interface RouteResult {
  distance_km: number;
  duration_minutes: number;
  risk_score: number;
  polyline: string;
  waypoints: { lat: number; lon: number; name: string }[];
  instructions: string[];
}

export async function optimizeRoute(
  originLat: number, originLon: number,
  destLat: number, destLon: number,
  vehicleType: string = "truck"
): Promise<RouteResult> {
  const resp = await fetch(`${API_BASE}/routing/optimize`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      origin_lat: originLat, origin_lon: originLon,
      dest_lat: destLat, dest_lon: destLon,
      vehicle_type: vehicleType, avoid_floods: true,
    }),
  });
  if (!resp.ok) throw new Error(`Routing error: ${resp.status}`);
  return resp.json();
}
