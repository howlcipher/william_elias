import pytest
import json
from scripts.build_config import build_config

def test_build_config_publishes_only_the_last_synced_source(tmp_path, monkeypatch):
    data = {
        "personal": {
            "name": "Test User",
            "sourceRepo": "https://github.com/example/repo",
            "sourceBranch": "dev",
        },
        "about": "This bio stays in resume.json and must not be copied into config.js.",
    }
    json_path = tmp_path / "resume.json"
    js_path = tmp_path / "config.js"
    json_path.write_text(json.dumps(data))

    monkeypatch.chdir(tmp_path)
    build_config()

    assert js_path.exists()
    content = js_path.read_text()
    assert content.startswith("const config = {")
    embedded = json.loads(content.removeprefix("const config = ").removesuffix(";\n"))
    assert embedded == {
        "personal": {
            "sourceRepo": "https://github.com/example/repo",
            "sourceBranch": "dev",
        }
    }
    assert "Test User" not in content
    assert "about" not in content
