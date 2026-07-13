from pathlib import Path

FRONTEND_SOURCE_DIRS = ("app", "components", "lib")
SERVER_ONLY_KEY_MARKERS = ("SUPABASE_SECRET_KEY", "SUPABASE_SERVICE_ROLE_KEY", "sb_secret_")


def test_frontend_source_does_not_reference_server_only_supabase_keys() -> None:
    frontend_root = Path("frontend")
    source_files = [
        path
        for directory in FRONTEND_SOURCE_DIRS
        for path in (frontend_root / directory).rglob("*.ts*")
    ]

    assert source_files
    for path in source_files:
        content = path.read_text(encoding="utf-8")
        assert not any(marker in content for marker in SERVER_ONLY_KEY_MARKERS), path
