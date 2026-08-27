from sqlalchemy import Column, String, Float, DateTime, Text, Boolean, Integer
from datetime import datetime
import uuid

from models.database import Base


def gen_uuid():
    return str(uuid.uuid4())


class RoadSegment(Base):
    __tablename__ = "road_segments"

    id = Column(String, primary_key=True, default=gen_uuid)
    osm_id = Column(String, unique=True)
    name = Column(String)
    highway_type = Column(String)
    surface_type = Column(String)
    length_km = Column(Float)
    max_speed_kmh = Column(Float)
    start_lat = Column(Float)
    start_lon = Column(Float)
    end_lat = Column(Float)
    end_lon = Column(Float)
    is_vulnerable = Column(Boolean, default=False)
    vulnerability_score = Column(Float, default=0.0)
    last_updated = Column(DateTime, default=datetime.utcnow)


class VehiclePosition(Base):
    __tablename__ = "vehicle_positions"

    id = Column(String, primary_key=True, default=gen_uuid)
    vehicle_id = Column(String, index=True)
    driver_name = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    speed_kmh = Column(Float)
    heading = Column(Float)
    vehicle_type = Column(String, default="truck")
    cargo_type = Column(String)
    cargo_weight_kg = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.utcnow)


class DisruptionEvent(Base):
    __tablename__ = "disruption_events"

    id = Column(String, primary_key=True, default=gen_uuid)
    event_type = Column(String)
    severity = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    road_segment_id = Column(String)
    description = Column(Text)
    reported_by = Column(String)
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)


class FieldReport(Base):
    __tablename__ = "field_reports"

    id = Column(String, primary_key=True, default=gen_uuid)
    reporter_name = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    report_type = Column(String)
    title = Column(String, default="")
    description = Column(Text)
    severity = Column(String)
    status = Column(String, default="open")
    photo_url = Column(String, nullable=True)
    synced = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(String, primary_key=True, default=gen_uuid)
    alert_type = Column(String)
    severity = Column(String)
    title = Column(String)
    message = Column(Text)
    lat = Column(Float)
    lon = Column(Float)
    radius_km = Column(Float, default=10.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)


class District(Base):
    __tablename__ = "districts"

    id = Column(String, primary_key=True, default=gen_uuid)
    state_name = Column(String)
    district_name = Column(String)
    population = Column(Integer)
    road_density_km_per_sqkm = Column(Float)
    connectivity_score = Column(Float)
    resilience_score = Column(Float)


class SiliguriCorridor(Base):
    __tablename__ = "siliguri_corridor"

    id = Column(String, primary_key=True, default=gen_uuid)
    status = Column(String, default="operational")
    risk_level = Column(String, default="low")
    weather_impact = Column(String, default="none")
    blockage_reason = Column(Text, nullable=True)
    recorded_at = Column(DateTime, default=datetime.utcnow)
