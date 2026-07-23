from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from shared.bq.writer import BigQueryWriter
from shared.config import AppConfig

from .schemas import Artifact, Observable, PlaybookRequest, PlaybookResponse


def _normalize_observables(observables: list[Observable]) -> list[Observable]:
    return sorted(
        observables,
        key=lambda item: (item.type.lower(), item.value.lower()),
    )


def run_playbook(request: PlaybookRequest) -> PlaybookResponse:
    normalized = _normalize_observables(request.observables)
    artifacts = [
        Artifact(type=f"normalized_{item.type}", value=item.value.strip().lower())
        for item in normalized
    ]
    summary = "Deterministic suspicious-login triage completed."
    return PlaybookResponse(
        contract_version="1.0",
        correlation_id=request.correlation_id,
        status="success",
        summary=summary,
        recommended_severity="medium",
        recommended_next_step="collect_more_context",
        artifacts=artifacts,
        tool_results=[],
    )


def persist_playbook(
    writer: BigQueryWriter,
    config: AppConfig,
    request: PlaybookRequest,
    response: PlaybookResponse,
) -> None:
    writer.insert(
        "agent_runs",
        {
            "run_id": str(uuid4()),
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "agent_name": config.agent_name,
            "agent_version": config.agent_version,
            "correlation_id": request.correlation_id,
            "source_system": request.source_system,
            "case_id": request.case.case_id,
            "alert_id": request.case.alert_id,
            "status": response.status,
            "latency_ms": 0,
            "input_hash": None,
            "output_hash": None,
            "model_name": "deterministic_stub",
            "tool_count": len(response.tool_results),
            "trace_id": None,
        },
    )
    writer.insert(
        "playbook_invocations",
        {
            "invocation_id": str(uuid4()),
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "playbook_name": request.playbook_name,
            "correlation_id": request.correlation_id,
            "case_id": request.case.case_id,
            "alert_id": request.case.alert_id,
            "requested_action": request.requested_action,
            "status": response.status,
            "recommended_severity": response.recommended_severity,
            "recommended_next_step": response.recommended_next_step,
            "trace_id": None,
        },
    )
