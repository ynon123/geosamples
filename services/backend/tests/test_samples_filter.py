from datetime import datetime, timezone


def test_filter_samples_polygon(client):
    client.post("/samples", json={
        "latitude": 31.78,
        "longitude": 35.22,
        "signal_strength": -70.5,
        "timestamp": datetime(2026, 2, 4, 12, 0, tzinfo=timezone.utc).isoformat(),
    })

    polygon = {
        "type": "Polygon",
        "coordinates": [[
            [35.21, 31.77],
            [35.23, 31.77],
            [35.23, 31.79],
            [35.21, 31.79],
            [35.21, 31.77],
        ]]
    }

    r = client.post("/samples/filter", json={"polygon": polygon, "limit": 10, "offset": 0})
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
