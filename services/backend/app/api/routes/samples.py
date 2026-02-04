import logging
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.schemas.samples import (
    SampleCreateIn,
    SampleOut,
    SamplesFilterIn,
    SamplesIngestIn,
    SamplesIngestOut,
)
from app.db.session import get_db
from app.service.samples_service import SamplesService

router = APIRouter()
svc = SamplesService()
log = logging.getLogger(__name__)


@router.get("/samples", response_model=List[SampleOut])
def get_samples(
    limit: int = Query(200, ge=1, le=5000),
    offset: int = Query(0, ge=0),
    from_time: Optional[datetime] = None,
    to_time: Optional[datetime] = None,
    db: Session = Depends(get_db),
):
    log.info("GET /samples limit=%d offset=%d from_time=%s to_time=%s", limit, offset, from_time, to_time)
    return svc.list_samples(db, limit=limit, offset=offset, from_time=from_time, to_time=to_time)


@router.post("/samples", status_code=201, response_model=SamplesIngestOut)
def post_samples(payload: SamplesIngestIn = Body(...), db: Session = Depends(get_db)):
    items = payload if isinstance(payload, list) else [payload]
    items_typed: List[SampleCreateIn] = items
    log.info("POST /samples count=%d", len(items_typed))
    inserted = svc.ingest_samples(db, items_typed)
    return SamplesIngestOut(inserted=inserted)


@router.post("/samples/filter", response_model=List[SampleOut])
def filter_samples(payload: SamplesFilterIn, db: Session = Depends(get_db)):
    polygon = payload.polygon.model_dump() if payload.polygon is not None else None
    log.info(
        "POST /samples/filter limit=%d offset=%d from_time=%s to_time=%s polygon=%s",
        payload.limit,
        payload.offset,
        payload.from_time,
        payload.to_time,
        "yes" if polygon else "no",
    )
    try:
        return svc.filter_samples(
            db,
            polygon_geojson=polygon,
            limit=payload.limit,
            offset=payload.offset,
            from_time=payload.from_time,
            to_time=payload.to_time,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
