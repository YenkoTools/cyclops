from __future__ import annotations

from typing import Any

try:
    from google.cloud import bigquery
except ImportError:  # pragma: no cover
    bigquery = None


class BigQueryWriter:
    def __init__(self, project_id: str | None, dataset: str | None) -> None:
        self.project_id = project_id
        self.dataset = dataset
        self._client = None
        if project_id and dataset and bigquery is not None:
            self._client = bigquery.Client(project=project_id)

    @property
    def enabled(self) -> bool:
        return self._client is not None and self.project_id is not None and self.dataset is not None

    def insert(self, table_name: str, row: dict[str, Any]) -> None:
        if not self.enabled:
            return
        table_id = f"{self.project_id}.{self.dataset}.{table_name}"
        errors = self._client.insert_rows_json(table_id, [row])
        if errors:
            raise RuntimeError(f"BigQuery insert failed for {table_id}: {errors}")
