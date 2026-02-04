from sqlalchemy import Column, DateTime, Float, text
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry
from .base import Base


class Sample(Base):
    __tablename__ = "samples"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    signal_strength = Column(Float, nullable=False)

    timestamp = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    geom = Column(
        Geometry(geometry_type="POINT", srid=4326),
        nullable=False,
    )
