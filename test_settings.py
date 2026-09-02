from app.config.settings import Settings


# =============================================================
# Test 1: Default configuration
# =============================================================


def test_default_settings():

    settings = Settings()

    assert (
        settings.forecast_model_name
        == "transformer"
    )

    assert (
        settings.llm_model
        == "qwen3:8b"
    )

    assert (
        settings.llm_num_ctx
        == 16384
    )

    assert (
        settings.embedding_model
        == "embeddinggemma"
    )

    assert (
        settings.chroma_path
        == "data/chroma"
    )

    assert (
        settings.chroma_collection_name
        == "quantmind_filings"
    )

    assert (
        settings.retrieval_top_k
        == 5
    )


# =============================================================
# Test 2: Environment variable override
# =============================================================


def test_environment_override(
    monkeypatch,
):

    monkeypatch.setenv(
        "QUANTMIND_LLM_MODEL",
        "test-model",
    )

    monkeypatch.setenv(
        "QUANTMIND_LLM_NUM_CTX",
        "8192",
    )

    settings = Settings()

    assert (
        settings.llm_model
        == "test-model"
    )

    assert (
        settings.llm_num_ctx
        == 8192
    )