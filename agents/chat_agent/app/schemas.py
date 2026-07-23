from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ChatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    contract_version: str
    session_id: str
    message: str
    context: dict | None = None


class ChatResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    contract_version: str
    session_id: str
    answer: str
    citations: list[str]
