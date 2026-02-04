from datetime import datetime, timezone


def test_ingest_single(client):
    payload = {
        "latitude": 31.78,
        "longitude": 35.22,
        "signal_strength": -70.5,
        "timestamp": datetime(2026, 2, 4, 12, 0, tzinfo=timezone.utc).isoformat(),
    }
    r = client.post("/samples", json=payload)
    assert r.status_code == 201
    assert r.json()["inserted"] == 1
