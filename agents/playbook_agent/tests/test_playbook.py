from app.schemas import CaseContext, Observable, PlaybookRequest
from app.service import run_playbook


def test_playbook_response_is_deterministic() -> None:
    request = PlaybookRequest(
        contract_version="1.0",
        correlation_id="corr-1",
        source_system="google_secops_soar",
        playbook_name="triage-suspicious-login",
        requested_action="triage_suspicious_login",
        case=CaseContext(case_id="case-1"),
        observables=[
            Observable(type="ip", value="203.0.113.10"),
            Observable(type="user", value="Alice@example.com"),
        ],
        dry_run=True,
    )
    response = run_playbook(request)
    assert response.status == "success"
    assert response.recommended_next_step == "collect_more_context"
    assert response.artifacts[0].type == "normalized_ip"
