import pytest
from playwright.sync_api import Page
import os
import json
import threading
import http.server
import socketserver

DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    def log_message(self, format, *args):
        pass # silence HTTP logs

socketserver.TCPServer.allow_reuse_address = True
# Port 0 lets the OS hand out a free port. A fixed port fails collection outright
# when anything else on the machine already holds it.
httpd = socketserver.TCPServer(("", 0), Handler)
PORT = httpd.server_address[1]

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


def test_profile_photo_tracks_theme_and_colorblind_mode(page: Page, test_url: str):
    page.add_init_script("localStorage.clear()")
    page.emulate_media(color_scheme="dark")
    page.goto(test_url)

    photo = page.locator('.profile-photo')
    theme_toggle = page.locator('#theme-toggle')
    colorblind_toggle = page.locator('#colorblind-toggle')
    dark_photo = 'assets/images/william-elias-profile-hoodie-dark.webp'
    light_photo = 'assets/images/william-elias-profile-hoodie-light.webp'

    def assert_photo_loaded(expected_source):
        page.wait_for_function(
            """expectedSource => {
                const image = document.querySelector('.profile-photo');
                return image.getAttribute('src') === expectedSource && image.complete && image.naturalWidth > 0;
            }""",
            arg=expected_source,
        )

    # Default/dark starts on the dark portrait.
    assert_photo_loaded(dark_photo)
    assert photo.get_attribute('alt') == 'Portrait of William Elias'
    assert photo.get_attribute('width') == '512'
    assert photo.get_attribute('height') == '512'

    module = page.locator('.profile-module')
    desktop_box = module.bounding_box()
    assert abs(desktop_box['width'] - desktop_box['height']) <= 1
    assert desktop_box['width'] <= 260
    assert page.locator('.hero-content').evaluate("el => getComputedStyle(el).overflow") == 'visible'

    # Light, including light colorblind mode, uses the light portrait.
    theme_toggle.click()
    assert_photo_loaded(light_photo)
    colorblind_toggle.click()
    assert_photo_loaded(light_photo)

    # Dark colorblind mode uses the dark portrait, and repeated switches stay in sync.
    theme_toggle.click()
    assert_photo_loaded(dark_photo)
    theme_toggle.click()
    assert_photo_loaded(light_photo)
    theme_toggle.click()
    assert_photo_loaded(dark_photo)


def test_profile_module_is_square_and_fits_mobile(page: Page, test_url: str):
    page.set_viewport_size({"width": 390, "height": 844})
    page.goto(test_url)

    module = page.locator('.profile-module')
    box = module.bounding_box()
    assert abs(box['width'] - box['height']) <= 1
    assert 150 <= box['width'] <= 180
    assert module.evaluate("el => getComputedStyle(el).gridArea") == 'photo'
    assert page.evaluate("() => document.documentElement.scrollWidth <= 390")
    assert page.locator('.profile-photo').get_attribute('alt') == 'Portrait of William Elias'

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

def test_terminal_caret_is_inline_pseudo_element_not_border(page: Page, test_url: str):
    page.goto(test_url)
    tagline = page.locator('.tagline.terminal-type')

    border_right_width = tagline.evaluate("el => getComputedStyle(el).borderRightWidth")
    assert border_right_width == "0px", (
        f"Caret should not be implemented as a border-right on the tagline box, got {border_right_width}"
    )

    after_style = tagline.evaluate("""el => {
        const cs = getComputedStyle(el, '::after');
        return {display: cs.display, width: cs.width, animationName: cs.animationName};
    }""")
    assert after_style["display"] == "inline-block"
    assert after_style["width"] not in ("0px", "auto", "")
    assert after_style["animationName"] == "terminal-caret"

def test_six_project_cards_render_with_correct_links(page: Page, test_url: str):
    page.goto(test_url)

    cards = page.locator("#projects-target .project-card")
    assert cards.count() == 6

    titles = cards.locator("h3").all_inner_texts()
    assert "RedrawUS" in titles
    assert "Password Arena" in titles

    redrawus_link = page.locator("#projects-target .project-card", has=page.locator("h3", has_text="RedrawUS")).locator("a.project-link")
    assert redrawus_link.get_attribute("href") == "https://github.com/howlcipher/redistricting-map"

    password_arena_link = page.locator("#projects-target .project-card", has=page.locator("h3", has_text="Password Arena")).locator("a.project-link")
    assert password_arena_link.get_attribute("href") == "https://github.com/howlcipher/password_arena"

def test_scroll_spy_activates_correct_nav_link(page: Page, test_url: str):
    page.set_viewport_size({"width": 1440, "height": 900})
    page.goto(test_url)

    about_link = page.locator('.nav-links a[href="#about"]')
    skills_link = page.locator('.nav-links a[href="#skills"]')

    # Force a scroll (scroll_into_view_if_needed is a no-op when the section is
    # already on screen at this viewport size) to exercise the observer band.
    page.evaluate("() => document.getElementById('about').scrollIntoView({block: 'start'})")
    page.wait_for_timeout(300)
    assert about_link.get_attribute("aria-current") == "page"

    page.evaluate("() => document.getElementById('skills').scrollIntoView({block: 'start'})")
    page.wait_for_timeout(300)
    assert skills_link.get_attribute("aria-current") == "page"
    assert about_link.get_attribute("aria-current") is None
    # Active state is not conveyed by color alone: a non-color affordance must change too.
    border_color = skills_link.evaluate("el => getComputedStyle(el).borderBottomColor")
    assert border_color != "rgba(0, 0, 0, 0)"

def test_logo_returns_to_top_and_clears_active_section(page: Page, test_url: str):
    page.set_viewport_size({"width": 1440, "height": 900})
    page.goto(test_url)

    exp = page.locator("#experience")
    exp.scroll_into_view_if_needed()
    page.evaluate("window.scrollBy(0, 100)")
    page.wait_for_timeout(300)
    exp_link = page.locator('.nav-links a[href="#experience"]')
    assert exp_link.get_attribute("aria-current") == "page"

    page.locator("a.logo").click()
    # Smooth-scroll (html { scroll-behavior: smooth }) animates the long
    # skills -> top jump, so poll for settling instead of a fixed sleep.
    page.wait_for_function("() => window.scrollY === 0", timeout=3000)

    assert exp_link.get_attribute("aria-current") is None
    hero_box = page.locator("header.hero").bounding_box()
    assert hero_box["y"] >= 0


def test_logo_is_keyboard_focusable_with_accessible_label(page: Page, test_url: str):
    page.set_viewport_size({"width": 1440, "height": 900})
    page.goto(test_url)

    logo = page.locator("a.logo")
    assert logo.get_attribute("aria-label") == "Home — return to top"
    logo.focus()
    assert page.evaluate("() => document.activeElement.classList.contains('logo')")


def test_resume_action_never_marked_as_active_section(page: Page, test_url: str):
    page.set_viewport_size({"width": 1440, "height": 900})
    page.goto(test_url)
    page.evaluate("() => document.getElementById('education').scrollIntoView({block: 'start'})")
    page.wait_for_timeout(300)

    resume_btn = page.locator(".nav-resume-btn")
    assert resume_btn.count() == 1
    assert resume_btn.get_attribute("aria-current") is None

def test_desktop_nav_resume_cta_visible_and_safe_external_link(page: Page, test_url: str):
    page.set_viewport_size({"width": 1440, "height": 900})
    page.goto(test_url)

    resume_btn = page.locator(".nav-resume-btn")
    assert resume_btn.is_visible()
    assert resume_btn.get_attribute("href") == "William_Elias_Resume.pdf"
    assert resume_btn.get_attribute("rel") == "noopener noreferrer"

def test_mobile_nav_resume_cta_present_in_menu(page: Page, test_url: str):
    page.set_viewport_size({"width": 375, "height": 667})
    page.goto(test_url)

    page.locator(".mobile-menu-btn").click()
    resume_link = page.locator(".mobile-resume-link")
    assert resume_link.is_visible()
    assert resume_link.get_attribute("href") == "William_Elias_Resume.pdf"

def test_bottom_recruiter_cta_renders_with_actions(page: Page, test_url: str):
    page.goto(test_url)
    cta = page.locator("#contact-cta")
    cta.scroll_into_view_if_needed()

    assert cta.locator("h2.cta-title").inner_text() == "Open to U.S. Remote Opportunities"
    actions = cta.locator(".cta-actions a")
    assert actions.count() >= 3

def test_no_js_content(browser, test_url: str):
    context = browser.new_context(java_script_enabled=False)
    page = context.new_page()
    page.goto(test_url)
    
    # Assert core resume content is visible
    name = page.locator("h1").inner_text()
    assert "William Elias" in name
    
    experience = page.locator(".timeline-content h3").first.inner_text()
    assert experience
    
    skill = page.locator(".skill-category h3").first.inner_text()
    assert skill
    
    context.close()
