import pytest
from scripts.build_html import esc, get_valid_url, inject, render_summary

def test_esc():
    assert esc("hello") == "hello"
    assert esc("<script>") == "&lt;script&gt;"
    assert esc('"quotes"') == "&quot;quotes&quot;"
    assert esc(None) == ""

def test_get_valid_url():
    assert get_valid_url("https://example.com") == "https://example.com"
    assert get_valid_url("http://test.org") == "http://test.org"
    assert get_valid_url("ftp://bad.com") is None
    assert get_valid_url("javascript:alert(1)") is None
    assert get_valid_url("/assets/resume.pdf", allow_relative=True) == "/assets/resume.pdf"

def test_inject_success():
    html = "<div><!-- BUILD:TEST:START -->old<!-- BUILD:TEST:END --></div>"
    res = inject(html, "TEST", "new")
    assert res == "<div><!-- BUILD:TEST:START -->new<!-- BUILD:TEST:END --></div>"

def test_inject_missing_marker():
    html = "<div>No marker here</div>"
    with pytest.raises(ValueError, match="Marker pair for TEST not found in HTML content"):
        inject(html, "TEST", "new")

def test_render_summary():
    res = render_summary("A summary with <br> tag")
    assert res == "<p>A summary with &lt;br&gt; tag</p>"
