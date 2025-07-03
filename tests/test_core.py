# tests/test_core.py
from pathlib import Path


from app.core.config import Settings, FeatureFlags, get_app_version


def test_get_app_version(monkeypatch, tmp_path):
    version_content = "1.2.3"
    version_file = tmp_path / "VERSION"
    version_file.write_text(version_content)

    monkeypatch.setattr(Path, "resolve", lambda self: tmp_path / "app")
    monkeypatch.setattr(Path, "parent", tmp_path)

    version = get_app_version()
    assert version == version_content


def test_get_app_version_fallback(monkeypatch):
    monkeypatch.setattr(Path, "resolve", lambda self: Path("/nonexistent"))
    monkeypatch.setattr(
        Path, "read_text", lambda self: (_ for _ in ()).throw(FileNotFoundError())
    )
    assert get_app_version() == "0.0.0"


def test_settings_sqlalchemy_url(monkeypatch):
    monkeypatch.setenv("POSTGRES_USER", "user")
    monkeypatch.setenv("POSTGRES_PASSWORD", "pass")
    monkeypatch.setenv("POSTGRES_DB", "mydb")
    monkeypatch.setenv("POSTGRES_HOST", "localhost")
    monkeypatch.setenv("POSTGRES_PORT", "5432")
    monkeypatch.setenv("SECRET_KEY", "fake")

    settings = Settings()
    expected = "postgresql://user:pass@localhost:5432/mydb"
    assert settings.SQLALCHEMY_DATABASE_URL == expected


def test_feature_flags_default(monkeypatch):
    monkeypatch.delenv("FEATURE_SIMULATE_TASK_LATENCY", raising=False)
    monkeypatch.delenv("FEATURE_ENABLE_SUMMARY_ENDPOINT", raising=False)

    flags = FeatureFlags()
    assert flags.simulate_task_latency is False
    assert flags.enable_summary_endpoint is False
