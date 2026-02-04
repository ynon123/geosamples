from datetime import datetime
from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict


class SampleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    latitude: float
    longitude: float
    signal_strength: float
    timestamp: datetime


class SampleCreateIn(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    signal_strength: float
    timestamp: datetime


SamplesIngestIn = Union[SampleCreateIn, List[SampleCreateIn]]


class SamplesIngestOut(BaseModel):
    inserted: int


class PolygonGeometry(BaseModel):
    type: Literal["Polygon"]
    coordinates: List[List[List[float]]]

    @field_validator("coordinates")
    def validate_coords(cls, coords: List[List[List[float]]]):
        if not coords or not isinstance(coords, list):
            raise ValueError("coordinates must be a non-empty list")

        ring = coords[0] if coords else None
        if not ring or len(ring) < 4:
            raise ValueError("polygon ring must have at least 4 points (including closing point)")

        for p in ring:
            if not isinstance(p, list) or len(p) != 2:
                raise ValueError("each polygon point must be [lon, lat]")
            lon, lat = p
            if not isinstance(lon, (int, float)) or not isinstance(lat, (int, float)):
                raise ValueError("polygon point values must be numbers")
            if lon < -180 or lon > 180:
                raise ValueError("polygon lon out of range (-180..180)")
            if lat < -90 or lat > 90:
                raise ValueError("polygon lat out of range (-90..90)")

        first = ring[0]
        last = ring[-1]
        if first[0] != last[0] or first[1] != last[1]:
            raise ValueError("polygon ring must be closed (first point must equal last point)")

        return coords


class SamplesFilterIn(BaseModel):
    polygon: Optional[PolygonGeometry] = None
    from_time: Optional[datetime] = None
    to_time: Optional[datetime] = None
    limit: int = Field(default=1000, ge=1, le=5000)
    offset: int = Field(default=0, ge=0)

    @model_validator(mode="after")
    def validate_time_range(self):
        if self.from_time and self.to_time and self.to_time < self.from_time:
            raise ValueError("to_time must be >= from_time")
        return self
