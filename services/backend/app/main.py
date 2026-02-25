from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4

from app.core.settings import get_settings
from app.core.logging import configure_logging, request_id_var
from app.api.router import api_router


def create_app() -> FastAPI:
    configure_logging()
    settings = get_settings()
    app = FastAPI(title="Geo Samples API", version="1.0.0")

    @app.middleware("http")
    async def request_id_middleware(request: Request, call_next):
        incoming = request.headers.get("X-Request-ID")
        request_id = incoming or str(uuid4())

        token = request_id_var.set(request_id)
        try:
            response = await call_next(request)
        finally:
            request_id_var.reset(token)

        response.headers["X-Request-ID"] = request_id
        return response

    origins = [o.strip() for o in (settings.cors_origins or "").split(",") if o.strip()]
    if origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(api_router)

    @app.get("/health", tags=["system"])
    def health():
        return {"status": "ok"}

    return app


app = create_app()
