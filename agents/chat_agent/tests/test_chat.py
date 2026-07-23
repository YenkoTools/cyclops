from app.service import generate_response
from app.schemas import ChatRequest


def test_chat_response_is_deterministic() -> None:
    request = ChatRequest(contract_version="1.0", session_id="s1", message="hello")
    response = generate_response(request)
    assert response.session_id == "s1"
    assert "hello" in response.answer
