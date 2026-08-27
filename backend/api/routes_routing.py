from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import text
import httpx

from config import settings
from models.database import SessionLocal

router = APIRouter()


class RouteRequest(BaseModel):
    origin_lat: float
    origin_lon: float
    dest_lat: float
    dest_lon: float
    vehicle_type: str = "truck"
    avoid_floods: bool = True


class RouteResponse(BaseModel):
    distance_km: float
    duration_minutes: float
    risk_score: float
    polyline: str
    waypoints: list[dict]


@router.get("/roads.geojson")
def get_roads_geojson():
    db = SessionLocal()
    try:
        rows = db.execute(
            text("SELECT osm_id, name, highway_type, start_lat, start_lon, end_lat, end_lon, vulnerability_score "
                 "FROM road_segments WHERE start_lat IS NOT NULL LIMIT 50000")
        ).fetchall()

        features = []
        for r in rows:
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [r[4], r[3]],
                        [r[6], r[5]],
                    ],
                },
                "properties": {
                    "osm_id": r[0],
                    "name": r[1],
                    "highway": r[2],
                    "vulnerability": r[7],
                },
            })

        return JSONResponse(content={
            "type": "FeatureCollection",
            "features": features,
        })
    finally:
        db.close()


@router.get("/stats")
def get_routing_stats():
    db = SessionLocal()
    try:
        total = db.execute(text("SELECT COUNT(*) FROM road_segments")).scalar()
        vulnerable = db.execute(text("SELECT COUNT(*) FROM road_segments WHERE is_vulnerable = 1")).scalar()
        highways = db.execute(
            text("SELECT highway_type, COUNT(*) FROM road_segments GROUP BY highway_type ORDER BY COUNT(*) DESC")
        ).fetchall()

        vehicles = db.execute(text("SELECT COUNT(*) FROM vehicle_positions")).scalar()
        disruptions = db.execute(text("SELECT COUNT(*) FROM disruption_events WHERE resolved_at IS NULL")).scalar()
        alerts = db.execute(text("SELECT COUNT(*) FROM alerts WHERE is_active = 1")).scalar()

        return {
            "total_segments": total,
            "vulnerable_segments": vulnerable,
            "by_type": {r[0]: r[1] for r in highways},
            "active_vehicles": vehicles,
            "active_disruptions": disruptions,
            "active_alerts": alerts,
        }
    finally:
        db.close()


@router.post("/optimize", response_model=RouteResponse)
async def optimize_route(req: RouteRequest):
    # Try Valhalla first
    try:
        import json as _json
        valhalla_body = _json.dumps({
            "locations": [
                {"lat": req.origin_lat, "lon": req.origin_lon},
                {"lat": req.dest_lat, "lon": req.dest_lon},
            ],
            "costing": "auto",
        })
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(
                f"{settings.VALHALLA_URL}/route",
                params={"json": valhalla_body},
            )
            if resp.status_code == 200:
                data = resp.json()
                return RouteResponse(
                    distance_km=data.get("trip", {}).get("summary", {}).get("length", 0) / 1000,
                    duration_minutes=data.get("trip", {}).get("summary", {}).get("time", 0) / 60,
                    risk_score=0.0,
                    polyline="",
                    waypoints=[],
                )
    except (httpx.ConnectError, httpx.TimeoutException):
        pass

    # Fallback: OSRM public API
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            url = (
                f"https://router.project-osrm.org/route/v1/driving/"
                f"{req.origin_lon},{req.origin_lat};{req.dest_lon},{req.dest_lat}"
                f"?overview=full&geometries=polyline&steps=true"
            )
            resp = await client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("code") == "Ok" and data.get("routes"):
                    route = data["routes"][0]
                    legs = route.get("legs", [])
                    instructions = []
                    waypoints = []
                    for leg in legs:
                        for step in leg.get("steps", []):
                            instructions.append(step.get("maneuver", {}).get("type", ""))
                            wp = step.get("intersections", [{}])
                            if wp:
                                waypoints.append({
                                    "lat": wp[0].get("lat", 0),
                                    "lon": wp[0].get("lon", 0),
                                    "name": step.get("name", ""),
                                })

                    # Calculate risk score based on disruption proximity
                    risk_score = 0.0
                    db = SessionLocal()
                    try:
                        mid_lat = (req.origin_lat + req.dest_lat) / 2
                        mid_lon = (req.origin_lon + req.dest_lon) / 2
                        nearby = db.execute(
                            text("SELECT COUNT(*) FROM disruption_events "
                                 "WHERE resolved_at IS NULL "
                                 "AND ABS(lat - :lat) < 0.5 AND ABS(lon - :lon) < 0.5"),
                            {"lat": mid_lat, "lon": mid_lon},
                        ).scalar()
                        risk_score = min(1.0, (nearby or 0) * 0.25)
                    finally:
                        db.close()

                    return RouteResponse(
                        distance_km=route.get("distance", 0) / 1000,
                        duration_minutes=route.get("duration", 0) / 60,
                        risk_score=risk_score,
                        polyline=route.get("geometry", ""),
                        waypoints=waypoints[:20],
                    )
    except (httpx.ConnectError, httpx.TimeoutException):
        pass

    # Final fallback: straight-line estimate
    import math
    R = 6371
    dlat = math.radians(req.dest_lat - req.origin_lat)
    dlon = math.radians(req.dest_lon - req.origin_lon)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(req.origin_lat)) * math.cos(math.radians(req.dest_lat)) * math.sin(dlon/2)**2
    dist = R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return RouteResponse(
        distance_km=round(dist, 1),
        duration_minutes=round(dist / 40 * 60, 0),
        risk_score=0.0,
        polyline="",
        waypoints=[],
    )


@router.get("/weather")
async def get_weather(lat: float = 26.14, lon: float = 91.73):
    from services.weather import get_weather as fetch_weather

    w = await fetch_weather(lat, lon)
    if w is None:
        return {"error": "Weather data unavailable", "lat": lat, "lon": lon}

    return {
        "lat": lat,
        "lon": lon,
        "temperature_c": w.temperature_c,
        "rainfall_1h_mm": w.rainfall_1h_mm,
        "rainfall_24h_mm": w.rainfall_24h_mm,
        "wind_speed_kmh": w.wind_speed_kmh,
        "humidity_pct": w.humidity_pct,
        "weather_code": w.weather_code,
        "description": w.description,
    }


@router.get("/predict-disruption")
async def predict_disruption(
    lat: float = 26.14,
    lon: float = 91.73,
    slope_deg: float = 20,
    elevation_m: float = 500,
):
    from services.weather import get_weather as fetch_weather
    from services.disruption_predictor import predict_disruption as predict

    rainfall_1h = 0.0
    rainfall_24h = 0.0

    w = await fetch_weather(lat, lon)
    if w:
        rainfall_1h = w.rainfall_1h_mm
        rainfall_24h = w.rainfall_24h_mm

    prediction = predict(
        rainfall_1h=rainfall_1h,
        rainfall_24h=rainfall_24h,
        slope_deg=slope_deg,
        elevation_m=elevation_m,
    )

    return {
        "lat": lat,
        "lon": lon,
        "risk_score": prediction.risk_score,
        "risk_level": prediction.risk_level,
        "contributing_factors": prediction.contributing_factors,
        "weather": {
            "rainfall_1h_mm": rainfall_1h,
            "rainfall_24h_mm": rainfall_24h,
        } if w else None,
    }


@router.get("/disruptions")
async def get_disruptions():
    db = SessionLocal()
    try:
        rows = db.execute(
            text("SELECT id, event_type, severity, lat, lon, description, created_at "
                 "FROM disruption_events WHERE resolved_at IS NULL ORDER BY created_at DESC LIMIT 50")
        ).fetchall()
        return {"disruptions": [
            {"id": r[0], "type": r[1], "severity": r[2], "lat": r[3], "lon": r[4], "description": r[5], "time": str(r[6])}
            for r in rows
        ]}
    finally:
        db.close()


@router.get("/ner-weather")
async def get_ner_weather():
    from services.weather import get_ner_weather_dashboard
    return {"cities": await get_ner_weather_dashboard()}


@router.get("/districts")
def get_districts():
    db = SessionLocal()
    try:
        rows = db.execute(
            text("SELECT id, state_name, district_name, population, road_density_km_per_sqkm, "
                 "connectivity_score, resilience_score FROM districts ORDER BY state_name")
        ).fetchall()

        # Count total active disruptions
        total_disruptions = db.execute(
            text("SELECT COUNT(*) FROM disruption_events WHERE resolved_at IS NULL")
        ).scalar() or 0

        result = []
        for r in rows:
            result.append({
                "id": r[0],
                "state": r[1],
                "district": r[2],
                "population": r[3],
                "road_density": r[4],
                "connectivity_score": r[5],
                "resilience_score": r[6],
                "active_disruptions": total_disruptions,
                "status": "good" if (r[5] or 0) > 0.6 else "moderate" if (r[5] or 0) > 0.3 else "poor",
            })
        return {"districts": result}
    finally:
        db.close()


@router.get("/analytics")
def get_analytics():
    db = SessionLocal()
    try:
        total = db.execute(text("SELECT COUNT(*) FROM road_segments")).scalar()
        vulnerable = db.execute(text("SELECT COUNT(*) FROM road_segments WHERE is_vulnerable = 1")).scalar()

        by_type = db.execute(
            text("SELECT highway_type, COUNT(*) FROM road_segments GROUP BY highway_type ORDER BY COUNT(*) DESC LIMIT 10")
        ).fetchall()

        disruptions_by_type = db.execute(
            text("SELECT event_type, COUNT(*) FROM disruption_events WHERE resolved_at IS NULL GROUP BY event_type")
        ).fetchall()

        disruptions_by_severity = db.execute(
            text("SELECT severity, COUNT(*) FROM disruption_events WHERE resolved_at IS NULL GROUP BY severity")
        ).fetchall()

        roads_by_state = db.execute(
            text("SELECT state_name, road_density_km_per_sqkm FROM districts ORDER BY road_density_km_per_sqkm DESC")
        ).fetchall()

        return {
            "total_roads": total,
            "vulnerable_roads": vulnerable,
            "safe_roads": total - vulnerable,
            "roads_by_type": {r[0]: r[1] for r in by_type},
            "disruptions_by_type": {r[0]: r[1] for r in disruptions_by_type},
            "disruptions_by_severity": {r[0]: r[1] for r in disruptions_by_severity},
            "roads_by_state": {r[0]: r[1] for r in roads_by_state},
        }
    finally:
        db.close()


@router.get("/siliguri-status")
async def siliguri_corridor_status():
    db = SessionLocal()
    try:
        row = db.execute(
            text("SELECT status, risk_level, weather_impact, recorded_at FROM siliguri_corridor ORDER BY recorded_at DESC LIMIT 1")
        ).first()
        if row:
            return {
                "corridor": "Siliguri",
                "width_km": 22,
                "status": row[0],
                "risk_level": row[1],
                "weather_impact": row[2],
                "last_updated": str(row[3]),
            }
    finally:
        db.close()
    return {"corridor": "Siliguri", "width_km": 22, "status": "operational", "risk_level": "low"}
