from app.config.settings import (
    Settings,
    get_settings,
)


def test_default_settings(
    monkeypatch,
):
    monkeypatch.delenv(
        "QUANTMIND_FORECAST_MODEL",
        raising=False,
    )
    monkeypatch.delenv(
        "QUANTMIND_LLM_MODEL",
        raising=False,
    )
    monkeypatch.delenv(
        "QUANTMIND_LLM_NUM_CTX",
        raising=False,
    )
    monkeypatch.delenv(
        "QUANTMIND_OLLAMA_HOST",
        raising=False,
    )
    monkeypatch.delenv(
        "QUANTMIND_EMBEDDING_MODEL",
        raising=False,
    )
    monkeypatch.delenv(
        "QUANTMIND_CHROMA_PATH",
        raising=False,
    )
    monkeypatch.delenv(
        "QUANTMIND_CHROMA_COLLECTION",
        raising=False,
    )
    monkeypatch.delenv(
        "QUANTMIND_RETRIEVAL_TOP_K",
        raising=False,
    )

    settings = Settings()

    assert settings.forecast_model_name == "transformer"
    assert settings.llm_model == "qwen3:8b"
    assert settings.llm_num_ctx == 16384
    assert settings.ollama_host == "http://localhost:11434"
    assert settings.embedding_model == "embeddinggemma"
    assert settings.chroma_path == "data/chroma"
    assert (
        settings.chroma_collection_name
        == "quantmind_filings"
    )
    assert settings.retrieval_top_k == 5


def test_environment_override(
    monkeypatch,
):
    monkeypatch.setenv(
        "QUANTMIND_FORECAST_MODEL",
        "lstm",
    )
    monkeypatch.setenv(
        "QUANTMIND_LLM_MODEL",
        "test-model",
    )
    monkeypatch.setenv(
        "QUANTMIND_LLM_NUM_CTX",
        "8192",
    )
    monkeypatch.setenv(
        "QUANTMIND_OLLAMA_HOST",
        "http://test-ollama:11434",
    )
    monkeypatch.setenv(
        "QUANTMIND_EMBEDDING_MODEL",
        "test-embedding",
    )
    monkeypatch.setenv(
        "QUANTMIND_CHROMA_PATH",
        "test/chroma",
    )
    monkeypatch.setenv(
        "QUANTMIND_CHROMA_COLLECTION",
        "test_collection",
    )
    monkeypatch.setenv(
        "QUANTMIND_RETRIEVAL_TOP_K",
        "10",
    )

    settings = Settings()

    assert settings.forecast_model_name == "lstm"
    assert settings.llm_model == "test-model"
    assert settings.llm_num_ctx == 8192
    assert (
        settings.ollama_host
        == "http://test-ollama:11434"
    )
    assert settings.embedding_model == "test-embedding"
    assert settings.chroma_path == "test/chroma"
    assert (
        settings.chroma_collection_name
        == "test_collection"
    )
    assert settings.retrieval_top_k == 10