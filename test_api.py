import pytest

from fastapi.testclient import TestClient

from app.application.exceptions.research_execution_error import (
    ResearchExecutionError,
)
from app.domain.entities.research_plan import (
    ResearchPlan,
)
from app.domain.entities.research_result import (
    ResearchResult,
)
from app.presentation.api.app import app
from app.presentation.api.dependencies import (
    get_research_service,
)


# =============================================================
# Fake successful QuantMind research service
# =============================================================


class FakeResearchService:
    """
    Lightweight fake research service used by API tests.

    This avoids executing the real QuantMind research engine,
    including LangGraph, Ollama, Chroma, Yahoo Finance,
    forecasting, and SEC retrieval.
    """

    def research(
        self,
        ticker: str,
        research_question: str,
    ) -> ResearchResult:

        plan = ResearchPlan(
            use_technical=False,
            use_forecast=False,
            use_fundamental=True,
            filing_types=["10-Q"],
        )

        return ResearchResult(
            ticker=ticker,
            research_question=research_question,
            research_plan=plan,
            report=(
                "Test research report generated "
                "by the fake research service."
            ),
        )


# =============================================================
# Fake unexpected internal failure
# =============================================================


class FailingResearchService:
    """
    Simulates a completely unexpected internal failure.

    This should be handled by the generic Exception handler.
    """

    def research(
        self,
        ticker: str,
        research_question: str,
    ) -> ResearchResult:

        raise RuntimeError(
            "Simulated QuantMind internal failure."
        )


# =============================================================
# Fake known research execution failure
# =============================================================


class FailingResearchExecutionService:
    """
    Simulates a known QuantMind research execution failure.

    This should be handled by the
    ResearchExecutionError-specific API handler.
    """

    def research(
        self,
        ticker: str,
        research_question: str,
    ) -> ResearchResult:

        raise ResearchExecutionError(
            "Simulated research execution failure."
        )


# =============================================================
# FastAPI dependency providers
# =============================================================


def get_fake_research_service():
    return FakeResearchService()


def get_failing_research_service():
    return FailingResearchService()


def get_failing_research_execution_service():
    return FailingResearchExecutionService()


# =============================================================
# Default dependency override for every test
# =============================================================


@pytest.fixture(autouse=True)
def override_research_service():
    """
    By default, every API test uses the fast fake service.

    Individual failure tests may temporarily replace this
    override with a failing service.
    """

    app.dependency_overrides[
        get_research_service
    ] = get_fake_research_service

    yield

    app.dependency_overrides.clear()


# =============================================================
# Standard TestClient
# =============================================================


client = TestClient(app)


# =============================================================
# Test 1: Health endpoint
# =============================================================


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert response.json() == {
        "status": "ok",
        "service": "QuantMind",
    }


# =============================================================
# Test 2: Successful research request
# =============================================================


def test_research():

    response = client.post(
        "/research",
        json={
            "ticker": "AAPL",
            "research_question": (
                "What are Apple's recent business risks?"
            ),
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["ticker"] == "AAPL"

    assert (
        data["research_question"]
        == "What are Apple's recent business risks?"
    )

    assert (
        data["research_plan"]["use_technical"]
        is False
    )

    assert (
        data["research_plan"]["use_forecast"]
        is False
    )

    assert (
        data["research_plan"]["use_fundamental"]
        is True
    )

    assert (
        data["research_plan"]["filing_types"]
        == ["10-Q"]
    )

    assert (
        "Test research report"
        in data["report"]
    )


# =============================================================
# Test 3: Ticker normalization
# =============================================================


def test_research_ticker_is_uppercase():

    response = client.post(
        "/research",
        json={
            "ticker": "aapl",
            "research_question": (
                "What are Apple's recent business risks?"
            ),
        },
    )

    assert response.status_code == 200

    assert (
        response.json()["ticker"]
        == "AAPL"
    )


# =============================================================
# Test 4: Missing ticker validation
# =============================================================


def test_missing_ticker_returns_422():

    response = client.post(
        "/research",
        json={
            "research_question": (
                "What are Apple's recent business risks?"
            ),
        },
    )

    assert response.status_code == 422


# =============================================================
# Test 5: Invalid research question validation
# =============================================================


def test_invalid_research_question_returns_422():

    response = client.post(
        "/research",
        json={
            "ticker": "AAPL",
            "research_question": "",
        },
    )

    assert response.status_code == 422


# =============================================================
# Test 6: Unexpected internal failure
# =============================================================


def test_internal_failure_returns_500():

    app.dependency_overrides[
        get_research_service
    ] = get_failing_research_service

    error_client = TestClient(
        app,
        raise_server_exceptions=False,
    )

    response = error_client.post(
        "/research",
        json={
            "ticker": "AAPL",
            "research_question": (
                "What are Apple's recent business risks?"
            ),
        },
    )

    assert response.status_code == 500

    assert response.json() == {
        "detail": "Internal server error.",
    }


# =============================================================
# Test 7: Known research execution failure
# =============================================================


def test_research_execution_failure_returns_500():

    app.dependency_overrides[
        get_research_service
    ] = (
        get_failing_research_execution_service
    )

    error_client = TestClient(
        app,
        raise_server_exceptions=False,
    )

    response = error_client.post(
        "/research",
        json={
            "ticker": "AAPL",
            "research_question": (
                "What are Apple's recent business risks?"
            ),
        },
    )

    assert response.status_code == 500

    assert response.json() == {
        "detail": "Research execution failed.",
    }