from __future__ import annotations

from fastapi import FastAPI, Header, HTTPException

from shared.bq.writer import BigQueryWriter
from shared.config import load_config
from shared.telemetry import configure_tracing, traced_span

from .schemas import PlaybookRequest, PlaybookResponse
from .service import persist_playbook, run_playbook

app = FastAPI(title="cyclops-playbook-agent", version="0.1.0")
config = load_config("playbook-agent")
configure_tracing(config.agent_name, config.deployment_environment)
writer = BigQueryWriter(config.google_cloud_project, config.bq_dataset)


@app.get("/healthz")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/playbook", response_model=PlaybookResponse)
def playbook(
    request: PlaybookRequest,
    x_shared_secret: str | None = Header(default=None),
) -> PlaybookResponse:
    expected = __import__("os").getenv("PLAYBOOK_SHARED_SECRET")
    if expected and x_shared_secret != expected:
        raise HTTPException(status_code=401, detail="Invalid shared secret")

    with traced_span(
        "playbook_request",
        agent_name=config.agent_name,
        correlation_id=request.correlation_id,
        case_id=request.case.case_id,
        playbook_name=request.playbook_name,
    ):
        response = run_playbook(request)
        persist_playbook(writer, config, request, response)
        return response
