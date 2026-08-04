import pytest
from playwright.sync_api import Page
import os
import json
import threading
import http.server
import socketserver

PORT = 8081
DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    def log_message(self, format, *args):
        pass # silence HTTP logs

socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(("", PORT), Handler)

def start_server():
    httpd.serve_forever()

@pytest.fixture(scope="session", autouse=True)
def test_server():
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    yield
    httpd.shutdown()
    httpd.server_close()

@pytest.fixture
def test_url():
    return f"http://localhost:{PORT}/index.html"

def test_format_relative_time(page: Page, test_url: str):
    page.goto(test_url)
    
    val_minutes = page.evaluate("""() => {
        const d = new Date(Date.now() - 5 * 60 * 1000).toISOString();
        return formatRelativeTime(d);
    }""")
    assert "minute" in val_minutes

    val_hours = page.evaluate("""() => {
        const d = new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString();
        return formatRelativeTime(d);
    }""")
    assert "hour" in val_hours

def test_validate_last_synced_data(page: Page, test_url: str):
    page.goto(test_url)
    valid_data = {
        "sha": "abcdef123",
        "commit": {"author": {"date": "2026-08-01T12:00:00Z"}},
        "html_url": "https://github.com/user/repo/commit/abcdef123"
    }
    invalid_data_1 = {"sha": ""}
    invalid_data_2 = {"sha": "abc", "commit": {}, "html_url": "http://github.com"}
    
    res1 = page.evaluate(f"() => validateLastSyncedData({json.dumps(valid_data)})")
    assert res1["sha"] == "abcdef123"
    assert res1["date"] == "2026-08-01T12:00:00Z"
    
    res2 = page.evaluate(f"() => validateLastSyncedData({json.dumps(invalid_data_1)})")
    assert res2 is None
    
    res3 = page.evaluate(f"() => validateLastSyncedData({json.dumps(invalid_data_2)})")
    assert res3 is None
    
def test_intersection_observer_fallback(page: Page, test_url: str):
    # Test behavior when IntersectionObserver is undefined.
    page.add_init_script("delete window.IntersectionObserver;")
    page.goto(test_url)
    
    # Wait for the setTimeout in script.js just in case
    page.wait_for_timeout(100)
    
    visible_count = page.locator('.fade-in.visible').count()
    total_count = page.locator('.fade-in').count()
    assert total_count > 0, "Should have .fade-in elements on the page"
    assert visible_count == total_count, "All .fade-in elements should be visible immediately"

def test_storage_failure_fallback(page: Page, test_url: str):
    errors = []
    page.on("pageerror", lambda err: errors.append(err))
    
    # Simulate storage failure
    page.add_init_script("""
        Object.defineProperty(window, 'localStorage', {
            value: {
                getItem: () => { throw new Error('Storage disabled'); },
                setItem: () => { throw new Error('Storage disabled'); }
            },
            configurable: true
        });
    """)
    page.goto(test_url)
    
    assert len(errors) == 0, f"Expected no uncaught errors on load, got: {errors}"
    
    theme_btn = page.locator('#theme-toggle')
    if theme_btn.count() > 0:
        initial_theme = page.evaluate("() => document.documentElement.getAttribute('data-theme')")
        theme_btn.click()
        new_theme = page.evaluate("() => document.documentElement.getAttribute('data-theme')")
        assert initial_theme != new_theme, "Theme should toggle even if localStorage fails"

def test_mobile_menu_behavior(page: Page, test_url: str):
    page.set_viewport_size({"width": 375, "height": 667})
    page.goto(test_url)
    
    btn = page.locator('.mobile-menu-btn')
    if btn.count() == 0:
        pytest.skip("Mobile menu button not found")
        
    nav = page.locator('.mobile-nav')
    
    assert btn.get_attribute('aria-expanded') == 'false'
    assert nav.get_attribute('aria-hidden') == 'true'
    assert not page.evaluate("() => document.querySelector('.mobile-nav').classList.contains('active')")
    
    btn.click()
    assert btn.get_attribute('aria-expanded') == 'true'
    assert nav.get_attribute('aria-hidden') == 'false'
    assert page.evaluate("() => document.querySelector('.mobile-nav').classList.contains('active')")
    
    page.keyboard.press('Escape')
    assert btn.get_attribute('aria-expanded') == 'false'
    assert nav.get_attribute('aria-hidden') == 'true'
    assert not page.evaluate("() => document.querySelector('.mobile-nav').classList.contains('active')")
    
    focused_class = page.evaluate("() => document.activeElement.className")
    assert 'mobile-menu-btn' in focused_class, "Focus should return to mobile menu button after closing"
