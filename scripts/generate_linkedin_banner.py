#!/usr/bin/env python3
"""
Generate the personal profile LinkedIn banner (1584 x 396) matching the
site's dark navy blueprint aesthetic, Space Grotesk / IBM Plex Mono typography,
and safe-area margin for the avatar overlay.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

SITE_DIR = Path(__file__).resolve().parent.parent

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    width: 1584px;
    height: 396px;
    background: #111e35;
    background-image: 
        linear-gradient(rgba(109, 174, 223, 0.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(109, 174, 223, 0.08) 1px, transparent 1px);
    background-size: 36px 36px;
    position: relative;
    overflow: hidden;
    font-family: 'Space Grotesk', sans-serif;
    color: #e9edf5;
}

/* Subtle corner technical label */
.corner-decor {
    position: absolute;
    top: 24px;
    left: 36px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    color: #6daedf;
    letter-spacing: 0.15em;
    opacity: 0.6;
}

/* Red WE. identity mark in upper-right */
.logo-mark {
    position: absolute;
    top: 24px;
    right: 48px;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 34px;
    font-weight: 700;
    color: #ef4444;
    letter-spacing: -0.06em;
}

/* Bottom accent bar matching the portfolio hero */
.accent-bar {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 6px;
    background: linear-gradient(to right, #ef4444 0 42%, #9fd3f4 42% 100%);
}

/* Main text container - positioned safely to the right of avatar overlay (left: 480px) */
.banner-content {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    left: 480px;
    right: 60px;
}

.headline {
    font-size: 46px;
    font-weight: 700;
    line-height: 1.1;
    letter-spacing: -0.035em;
    color: #e9edf5;
    text-transform: uppercase;
}

.tagline {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 20px;
    color: #a9b3c5;
    margin-top: 14px;
    line-height: 1.35;
}
.tagline-caret {
    color: #ef4444;
    font-weight: 700;
    margin-right: 6px;
}

.tech-stack {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 19px;
    font-weight: 600;
    color: #9fd3f4;
    margin-top: 16px;
    letter-spacing: 0.04em;
}

.ai-layer {
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 14px;
    font-weight: 600;
    color: #6daedf;
    margin-top: 12px;
    padding: 3px 10px;
    background: rgba(23, 41, 70, 0.8);
    border: 1px solid #6daedf;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
</style>
</head>
<body>
    <div class="corner-decor">SOFTWARE // DEVOPS // AUTOMATION</div>
    <div class="logo-mark">WE.</div>
    <div class="banner-content">
        <h1 class="headline">Software, DevOps &amp;<br>Automation Engineer</h1>
        <div class="tagline"><span class="tagline-caret">&gt;</span>Building Software, Automating Work &amp; Delivering Reliable Systems</div>
        <div class="tech-stack">Python &amp; FastAPI &nbsp;|&nbsp; CI/CD &nbsp;|&nbsp; Azure DevOps</div>
        <div class="ai-layer">AI-Enabled Engineering</div>
    </div>
    <div class="accent-bar"></div>
</body>
</html>
"""

def generate_banner(output_path: Path = None):
    if output_path is None:
        output_path = SITE_DIR / "assets" / "images" / "linkedin-banner.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1584, "height": 396}, device_scale_factor=1)
        page.set_content(HTML_TEMPLATE)
        page.wait_for_load_state("networkidle")
        page.screenshot(path=str(output_path))
        browser.close()

    print(f"Generated {output_path} ({output_path.stat().st_size} bytes)")


if __name__ == "__main__":
    generate_banner()
