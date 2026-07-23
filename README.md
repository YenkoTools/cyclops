# cyclops

Starter scaffold for the Google SecOps thin-thread runbook.

## Included

- `chat_agent`: minimal structured chat service
- `playbook_agent`: deterministic playbook service
- shared config, tracing, and BigQuery helpers
- JSON schemas for request/response contracts
- sample payloads
- Azure DevOps auth-smoke pipeline

## Quick start

1. Create a Python 3.11 virtual environment and activate it.

    ```bash
       python -m venv .venv
       # windows
       .venv/Scripts/activate
       # linux
       source venv/bin/activate
    ```
2. Install the requirements from the agent you want to run.
   ```
      pip install -r .\requirements\chat-agent.txt
      pip install -r .\requirements\playbook-agent.txt
   ```
3. Start the chat agent:

If you run from the repo root cyclops, use:
```uvicorn agents.chat_agent.app.main:app --reload --port 8080```
or
```uvicorn agents.playbook_agent.app.main:app --reload --port 8081```
```bash
# cd into agents folder 
uvicorn app.main:app --reload --port 8080
uvicorn app.main:app --reload --port 8081
```

Run from:

- `agents/chat_agent`
- or `agents/playbook_agent`


4. Test agents:
```bash
Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:8081/playbook `
  -ContentType 'application/json' `
  -Body (Get-Content .\samples\playbook\triage-suspicious-login.json -Raw)
```
and
```bash
Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:8080/chat `
  -ContentType 'application/json' `
  -Body '{"contract_version":"1.0","session_id":"session-001","message":"What does this alert mean?","context":{}}'
```

## Notes

- The code is intentionally small and deterministic-first.
- BigQuery writes are skipped unless `GOOGLE_CLOUD_PROJECT` and `BQ_DATASET` are set.
- OTLP export is configured by env vars and can be added later during deployment.
- This scaffold is Python-first and does not require Docker.

## 