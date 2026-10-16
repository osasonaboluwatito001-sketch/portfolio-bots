import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import create_app  # noqa: E402
from faq_engine import FAQEngine, normalize  # noqa: E402


@pytest.fixture
def engine():
    return FAQEngine.from_file(ROOT / "faq.json")


def test_normalize():
    assert normalize("  How LONG, does it take?? ") == "how long does it take"


def test_exact_match(engine):
    assert engine.ask("How do I get a refund?").answer.startswith("Contact support")


def test_fuzzy_match_with_typos(engine):
    m = engine.ask("how long dos delivry take")
    assert m and "24 hours" in m.answer


def test_no_match(engine):
    assert engine.ask("what is the airspeed of a swallow") is None


def test_empty_query(engine):
    assert engine.ask("   ") is None and engine.rank("") == []


def test_rank_sorted(engine):
    scores = [m.score for m in engine.rank("reset password", 4)]
    assert scores == sorted(scores, reverse=True)


def test_bad_threshold():
    with pytest.raises(ValueError):
        FAQEngine([], threshold=2)


@pytest.fixture
def client(engine):
    return create_app(engine).test_client()


def test_api_ask(client):
    r = client.post("/ask", json={"question": "which payment methods do you accept"})
    assert r.status_code == 200 and r.get_json()["matched"] is True


def test_api_no_match(client):
    body = client.post("/ask", json={"question": "zzz qqq"}).get_json()
    assert body["matched"] is False and "suggestions" in body


def test_api_bad_request(client):
    assert client.post("/ask", json={}).status_code == 400
    assert client.post("/ask", data="nope").status_code == 400
