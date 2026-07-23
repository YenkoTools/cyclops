from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class CaseContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str
    alert_id: str | None = None
    severity: str | None = None
    title: str | None = None


class Observable(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: str
    value: str


class PlaybookRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    contract_version: str
    correlation_id: str
    source_system: str
    playbook_name: str
    requested_action: str
    case: CaseContext
    observables: list[Observable]
    dry_run: bool


class Artifact(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: str
    value: str


class ToolResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tool_name: str
    status: str
    result_ref: str | None = None


class PlaybookResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    contract_version: str
    correlation_id: str
    status: str
    summary: str
    recommended_severity: str
    recommended_next_step: str
    artifacts: list[Artifact]
    tool_results: list[ToolResult]
