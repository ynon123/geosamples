CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS samples (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  latitude DOUBLE PRECISION NOT NULL CHECK (latitude >= -90 AND latitude <= 90),
  longitude DOUBLE PRECISION NOT NULL CHECK (longitude >= -180 AND longitude <= 180),

  signal_strength DOUBLE PRECISION NOT NULL,

  timestamp TIMESTAMPTZ NOT NULL DEFAULT now(),

  geom GEOMETRY(Point, 4326) NOT NULL
);

CREATE OR REPLACE FUNCTION samples_set_geom()
RETURNS TRIGGER AS $$
BEGIN
  NEW.geom := ST_SetSRID(ST_MakePoint(NEW.longitude, NEW.latitude), 4326);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_samples_set_geom ON samples;

CREATE TRIGGER trg_samples_set_geom
BEFORE INSERT OR UPDATE OF latitude, longitude
ON samples
FOR EACH ROW
EXECUTE FUNCTION samples_set_geom();


CREATE INDEX IF NOT EXISTS idx_samples_geom_gist ON samples USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_samples_timestamp ON samples (timestamp);
