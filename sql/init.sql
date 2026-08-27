-- SIH26002 NER Logistics Platform — Database Schema

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS hstore;

-- Road segments with geometry
CREATE TABLE IF NOT EXISTS road_segments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    osm_id VARCHAR UNIQUE,
    name VARCHAR,
    highway_type VARCHAR,
    surface_type VARCHAR,
    length_km FLOAT,
    max_speed_kmh FLOAT,
    geometry GEOMETRY(LINESTRING, 4326),
    is_vulnerable BOOLEAN DEFAULT FALSE,
    vulnerability_score FLOAT DEFAULT 0.0,
    last_updated TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_road_segments_geom ON road_segments USING GIST (geometry);
CREATE INDEX IF NOT EXISTS idx_road_segments_osm ON road_segments (osm_id);

-- Vehicle positions
CREATE TABLE IF NOT EXISTS vehicle_positions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vehicle_id VARCHAR NOT NULL,
    lat FLOAT NOT NULL,
    lon FLOAT NOT NULL,
    speed_kmh FLOAT,
    heading FLOAT,
    cargo_type VARCHAR,
    driver_name VARCHAR,
    timestamp TIMESTAMP DEFAULT NOW(),
    geom GEOMETRY(POINT, 4326)
);

CREATE INDEX IF NOT EXISTS idx_vehicle_positions_geom ON vehicle_positions USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_vehicle_positions_vehicle ON vehicle_positions (vehicle_id);
CREATE INDEX IF NOT EXISTS idx_vehicle_positions_time ON vehicle_positions (timestamp DESC);

-- Disruption events
CREATE TABLE IF NOT EXISTS disruption_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type VARCHAR NOT NULL,
    severity VARCHAR NOT NULL,
    lat FLOAT NOT NULL,
    lon FLOAT NOT NULL,
    road_segment_id UUID REFERENCES road_segments(id),
    description TEXT,
    reported_by VARCHAR,
    verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    resolved_at TIMESTAMP,
    geom GEOMETRY(POINT, 4326)
);

CREATE INDEX IF NOT EXISTS idx_disruption_geom ON disruption_events USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_disruption_type ON disruption_events (event_type);
CREATE INDEX IF NOT EXISTS idx_disruption_active ON disruption_events (resolved_at) WHERE resolved_at IS NULL;

-- Field reports (mobile app)
CREATE TABLE IF NOT EXISTS field_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reporter_name VARCHAR NOT NULL,
    lat FLOAT NOT NULL,
    lon FLOAT NOT NULL,
    report_type VARCHAR NOT NULL,
    description TEXT,
    severity VARCHAR,
    photo_url VARCHAR,
    synced BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    geom GEOMETRY(POINT, 4326)
);

CREATE INDEX IF NOT EXISTS idx_field_reports_geom ON field_reports USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_field_reports_time ON field_reports (created_at DESC);

-- Alerts
CREATE TABLE IF NOT EXISTS alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    alert_type VARCHAR NOT NULL,
    severity VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    message TEXT,
    lat FLOAT,
    lon FLOAT,
    radius_km FLOAT,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_alerts_active ON alerts (active) WHERE active = TRUE;

-- Districts (NER 8 states)
CREATE TABLE IF NOT EXISTS districts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    state_name VARCHAR NOT NULL,
    district_name VARCHAR NOT NULL,
    population BIGINT,
    road_density_km_per_sqkm FLOAT,
    connectivity_score FLOAT,
    resilience_score FLOAT,
    geometry GEOMETRY(MULTIPOLYGON, 4326)
);

CREATE INDEX IF NOT EXISTS idx_districts_geom ON districts USING GIST (geometry);

-- Siliguri Corridor monitoring
CREATE TABLE IF NOT EXISTS siliguri_corridor (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    status VARCHAR DEFAULT 'operational',
    risk_level VARCHAR DEFAULT 'low',
    weather_impact VARCHAR DEFAULT 'none',
    blockage_reason TEXT,
    recorded_at TIMESTAMP DEFAULT NOW()
);
