import pytest
import json
from scripts.build_config import build_config

def test_build_config(tmp_path, monkeypatch):
    data = {"personal": {"name": "Test User"}}
    json_path = tmp_path / "resume.json"
    js_path = tmp_path / "config.js"
    json_path.write_text(json.dumps(data))
    
    monkeypatch.chdir(tmp_path)
    build_config()
    
    assert js_path.exists()
    content = js_path.read_text()
    assert content.startswith("const config = {")
    assert '"name": "Test User"' in content
