#!/usr/bin/env python3
import json

def build_config():
    with open('resume.json', 'r') as f:
        data = json.load(f)
    
    js_content = f"const config = {json.dumps(data, indent=4)};\n"
    
    with open('config.js', 'w') as f:
        f.write(js_content)

if __name__ == "__main__":
    build_config()
