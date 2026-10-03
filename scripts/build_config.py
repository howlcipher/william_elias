#!/usr/bin/env python3
"""Publish the small config.js the page script actually reads.

Portfolio content is pre-rendered into index.html. script.js uses config.js
only for the footer "last synced" widget: the source repository and branch.
"""
import json


def published_config(data: dict) -> dict:
    personal = data.get("personal") or {}
    return {
        "personal": {
            "sourceRepo": personal.get("sourceRepo") or "",
            "sourceBranch": personal.get("sourceBranch") or "main",
        }
    }


def build_config():
    with open('resume.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    js_content = f"const config = {json.dumps(published_config(data), indent=4)};\n"

    with open('config.js', 'w', encoding='utf-8') as f:
        f.write(js_content)

if __name__ == "__main__":
    build_config()
