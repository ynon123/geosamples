from datetime import datetime, timezone


def test_list_samples(client):
    client.post("/samples", json={
        "latitude": 31.78,
        "longitude": 35.22,
        "signal_strength": -70.5,
        "timestamp": datetime(2026, 2, 4, 12, 0, tzinfo=timezone.utc).isoformat(),
    })

    r = client.get("/samples?limit=10&offset=0")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["latitude"] == 31.78
    assert data[0]["longitude"] == 35.22
