from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from shared.bq.writer import BigQueryWriter
from shared.config import AppConfig

from .schemas import ChatRequest, ChatResponse


def generate_response(request: ChatRequest) -> ChatResponse:
    answer = (
        "This is a minimal deterministic chat response. "
        f"Received message: {request.message.strip()}"
    )
    return ChatResponse(
        contract_version="1.0",
        session_id=request.session_id,
        answer=answer,
        citations=[],
    )


def persist_chat(
    writer: BigQueryWriter,
    config: AppConfig,
    request: ChatRequest,
    response: ChatResponse,
) -> None:
    writer.insert(
        "agent_runs",
        {
            "run_id": str(uuid4()),
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "agent_name": config.agent_name,
            "agent_version": config.agent_version,
            "correlation_id": request.session_id,
            "source_system": "chat",
            "case_id": None,
            "alert_id": None,
            "status": "success",
            "latency_ms": 0,
            "input_hash": None,
            "output_hash": None,
            "model_name": "deterministic_stub",
            "tool_count": 0,
            "trace_id": None,
        },
    )
    writer.insert(
        "chat_messages",
        {
            "message_id": str(uuid4()),
            "session_id": request.session_id,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "role": "assistant",
            "content": response.answer,
            "trace_id": None,
        },
    )
