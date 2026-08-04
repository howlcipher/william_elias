#!/usr/bin/env python3
import json
import re
from pathlib import Path

SITE_DIR = Path(__file__).resolve().parent.parent

def build_html():
    with open(SITE_DIR / 'resume.json', 'r') as f:
        data = json.load(f)
    
    personal = data.get('personal', {})
    name = personal.get('name', '')
    title = personal.get('title', '')
    tagline = personal.get('tagline', '').replace(" // ", ", ")
    
    page_title = f"{name} | {title}".replace('&', '&amp;')
    
    with open(SITE_DIR / 'index.html', 'r') as f:
        html = f.read()

    # Update <title>
    html = re.sub(
        r'<title>.*?</title>',
        f'<title>{page_title}</title>',
        html
    )
    
    # Update <meta name="description">
    html = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="Resume of {name}, a {title}. {tagline}.">',
        html
    )
    
    # Update <meta property="og:title">
    html = re.sub(
        r'<meta property="og:title" content="[^"]*">',
        f'<meta property="og:title" content="{page_title}">',
        html
    )
    
    # Update <meta property="og:description">
    html = re.sub(
        r'<meta property="og:description" content="[^"]*">',
        f'<meta property="og:description" content="{tagline.capitalize()}.">',
        html
    )

    with open(SITE_DIR / 'index.html', 'w') as f:
        f.write(html)

if __name__ == "__main__":
    build_html()
