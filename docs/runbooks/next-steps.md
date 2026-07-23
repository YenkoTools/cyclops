# Next Steps

After the auth smoke test passes:

1. Run `chat_agent` locally.
2. Set `GOOGLE_CLOUD_PROJECT` and `BQ_DATASET` to test BigQuery writes.
3. Add OTLP env vars from Secret Manager when deploying to Cloud Run.
4. Deploy `chat_agent` first.
5. Deploy `playbook_agent` second.
6. Add Google SecOps ingestion and SOAR webhook integration after both services work.

## Local run examples

Run from `agents/chat_agent`:

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080
```

Run from `agents/playbook_agent`:

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8081
```
