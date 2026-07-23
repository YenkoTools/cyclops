from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    agent_name: str
    agent_version: str
    google_cloud_project: str | None
    bq_dataset: str | None
    deployment_environment: str


def load_config(default_agent_name: str) -> AppConfig:
    return AppConfig(
        agent_name=os.getenv("AGENT_NAME", default_agent_name),
        agent_version=os.getenv("AGENT_VERSION", "0.1.0"),
        google_cloud_project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        bq_dataset=os.getenv("BQ_DATASET"),
        deployment_environment=os.getenv("DEPLOYMENT_ENVIRONMENT", "local"),
    )
