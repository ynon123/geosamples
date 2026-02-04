from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Iterable, Optional, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session, load_only
from sqlalchemy.sql import func

from app.api.schemas.samples import SampleCreateIn
from app.db.models.sample import Sample

log = logging.getLogger(__name__)


def _to_utc(dt: Optional[datetime]) -> Optional[datetime]:
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


class SamplesService:
    def list_samples(
        self,
        db: Session,
        *,
        limit: int,
        offset: int,
        from_time: Optional[datetime],
        to_time: Optional[datetime],
    ) -> Sequence[Sample]:
        q = (
            select(Sample)
            .options(load_only(Sample.id, Sample.latitude, Sample.longitude, Sample.signal_strength, Sample.timestamp))
            .order_by(Sample.timestamp.desc())
            .limit(limit)
            .offset(offset)
        )
        if from_time is not None:
            q = q.where(Sample.timestamp >= _to_utc(from_time))
        if to_time is not None:
            q = q.where(Sample.timestamp <= _to_utc(to_time))

        rows = db.execute(q).scalars().all()
        log.info("list_samples result=%d limit=%d offset=%d", len(rows), limit, offset)
        return rows

    def ingest_samples(self, db: Session, payloads: Iterable[SampleCreateIn]) -> int:
        count = 0
        for p in payloads:
            ts = _to_utc(p.timestamp)

            db.add(
                Sample(
                    latitude=p.latitude,
                    longitude=p.longitude,
                    signal_strength=p.signal_strength,
                    timestamp=ts,
                )
            )
            count += 1
        log.info("ingest_samples inserted=%d", count)
        return count

    def filter_samples(
        self,
        db: Session,
        *,
        polygon_geojson: Optional[dict],
        limit: int,
        offset: int,
        from_time: Optional[datetime],
        to_time: Optional[datetime],
    ) -> Sequence[Sample]:
        q = select(Sample).options(
            load_only(Sample.id, Sample.latitude, Sample.longitude, Sample.signal_strength, Sample.timestamp)
        )

        if polygon_geojson is not None:
            if not isinstance(polygon_geojson, dict):
                raise ValueError("polygon must be a dict/GeoJSON object")

            poly = func.ST_SetSRID(func.ST_GeomFromGeoJSON(json.dumps(polygon_geojson)), 4326)
            q = q.where(func.ST_Within(Sample.geom, poly))

        if from_time is not None:
            q = q.where(Sample.timestamp >= _to_utc(from_time))
        if to_time is not None:
            q = q.where(Sample.timestamp <= _to_utc(to_time))

        q = q.order_by(Sample.timestamp.desc()).limit(limit).offset(offset)

        rows = db.execute(q).scalars().all()
        log.info(
            "filter_samples result=%d limit=%d offset=%d polygon=%s",
            len(rows), limit, offset, polygon_geojson is not None
        )
        return rows
