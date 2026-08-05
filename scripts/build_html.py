#!/usr/bin/env python3
import json
import re
import html
from pathlib import Path

SITE_DIR = Path(__file__).resolve().parent.parent

def build_html():
    with open(SITE_DIR / 'resume.json', 'r') as f:
        data = json.load(f)
    
    personal = data.get('personal', {})
    name = personal.get('name', '')
    title = personal.get('title', '')
    tagline = personal.get('tagline', '').replace(" // ", ", ")
    
    page_title = html.escape(f"{name} | {title}", quote=True)
    escaped_desc = html.escape(f"Resume of {name}, a {title}. {tagline}.", quote=True)
    escaped_og_desc = html.escape(f"{tagline.capitalize()}.", quote=True)
    
    with open(SITE_DIR / 'index.html', 'r') as f:
        html_content = f.read()

    # Update <title>
    html_content = re.sub(
        r'<title>.*?</title>',
        f'<title>{page_title}</title>',
        html_content
    )
    
    # Update <meta name="description">
    html_content = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{escaped_desc}">',
        html_content
    )
    
    # Update <meta property="og:title">
    html_content = re.sub(
        r'<meta property="og:title" content="[^"]*">',
        f'<meta property="og:title" content="{page_title}">',
        html_content
    )
    
    # Update <meta property="og:description">
    html_content = re.sub(
        r'<meta property="og:description" content="[^"]*">',
        f'<meta property="og:description" content="{escaped_og_desc}">',
        html_content
    )

    with open(SITE_DIR / 'index.html', 'w') as f:
        f.write(html_content)

if __name__ == "__main__":
    build_html()
