from __future__ import annotations

from fastapi import FastAPI

from shared.bq.writer import BigQueryWriter
from shared.config import load_config
from shared.telemetry import configure_tracing, traced_span

from .schemas import ChatRequest, ChatResponse
from .service import generate_response, persist_chat

app = FastAPI(title="cyclops-chat-agent", version="0.1.0")
config = load_config("chat-agent")
configure_tracing(config.agent_name, config.deployment_environment)
writer = BigQueryWriter(config.google_cloud_project, config.bq_dataset)


@app.get("/healthz")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    with traced_span(
        "chat_request",
        agent_name=config.agent_name,
        session_id=request.session_id,
    ):
        response = generate_response(request)
        persist_chat(writer, config, request, response)
        return response
