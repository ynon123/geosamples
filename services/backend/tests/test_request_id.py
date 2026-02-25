import logging
import uuid


def test_request_id_generated_when_missing(client):
  r = client.get("/health")
  assert r.status_code == 200
  header = r.headers.get("X-Request-ID")
  assert header
  parsed = uuid.UUID(header)
  assert parsed.version == 4


def test_request_id_uses_incoming_header(client):
  rid = "test-correlation-id-123"
  r = client.get("/health", headers={"X-Request-ID": rid})
  assert r.status_code == 200
  assert r.headers.get("X-Request-ID") == rid


def test_request_id_available_in_logs(client):
  rid = "log-test-id-xyz"
  records = []

  logger = logging.getLogger()

  class ListHandler(logging.Handler):
    def emit(self, record):
      records.append(record)

  handler = ListHandler()
  logger.addHandler(handler)
  try:
    r = client.get("/samples?limit=10&offset=0", headers={"X-Request-ID": rid})
    assert r.status_code == 200

    relevant = [rec for rec in records if rec.name.startswith("app.")]
    assert relevant
    for rec in relevant:
      assert getattr(rec, "request_id", None) == rid
  finally:
    logger.removeHandler(handler)

