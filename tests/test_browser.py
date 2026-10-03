import pytest
from playwright.sync_api import Page, expect
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
        pass  # silence HTTP logs


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


def wait_for_section(page: Page, section_id: str):
    """Wait for smooth scrolling to reach its target and the observer to catch up."""
    page.wait_for_function(
        """id => {
            const section = document.getElementById(id);
            const margin = parseFloat(getComputedStyle(section).scrollMarginTop) || 0;
            const desired = window.scrollY + section.getBoundingClientRect().top - margin;
            const maximum = document.documentElement.scrollHeight - innerHeight;
            const target = Math.max(0, Math.min(desired, maximum));
            return Math.abs(window.scrollY - target) <= 1;
        }""",
        arg=section_id, timeout=5000,
    )
    expect(page.locator(
        f'.nav-links a[href="#{section_id}"]'
    )).to_have_attribute("aria-current", "page", timeout=5000)


@pytest.mark.parametrize("width", [320, 390, 810, 1024, 1440])
@pytest.mark.parametrize("theme", ["dark", "light", "contrast-dark", "contrast-light"])
def test_responsive_layout_has_no_overflow(page: Page, test_url: str, width, theme):
    page.set_viewport_size({"width": width, "height": 900})
    page.emulate_media(color_scheme="light" if theme.endswith("light") else "dark")
    page.goto(test_url)
    if theme.startswith("contrast"):
        page.locator("#colorblind-toggle").click()
    page.evaluate("document.fonts.ready")
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    frame = page.locator('.hero-content').bounding_box()
    for box in page.locator('.hero-content > *').all():
        bounds = box.bounding_box()
        assert bounds['x'] >= frame['x']
        assert bounds['x'] + bounds['width'] <= frame['x'] + frame['width']


def test_mobile_resume_visible_without_opening_menu(page: Page, test_url: str):
    page.set_viewport_size({"width": 390, "height": 844})
    page.goto(test_url)
    button = page.locator('.nav-resume-btn')
    assert button.is_visible()
    box = button.bounding_box()
    assert box['y'] + box['height'] < 844


@pytest.mark.parametrize("theme", ["dark", "light", "contrast-dark", "contrast-light"])
def test_mobile_role_title_has_readable_contrast(page: Page, test_url: str, theme):
    page.set_viewport_size({"width": 390, "height": 900})
    page.emulate_media(color_scheme="light" if theme.endswith("light") else "dark")
    page.goto(test_url)
    if theme.startswith("contrast"):
        page.locator("#colorblind-toggle").click()
    colors = page.locator(".subtitle").evaluate("""el => {
        const rgb = value => value.match(/[\\d.]+/g).slice(0, 3).map(Number);
        return [rgb(getComputedStyle(el).color),
                rgb(getComputedStyle(el.closest('.hero-content')).backgroundColor)];
    }""")

    def luminance(rgb):
        channels = [value / 255 for value in rgb]
        linear = [
            value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4
            for value in channels
        ]
        return sum(value * weight for value, weight in zip(linear, [0.2126, 0.7152, 0.0722]))

    dark, light = sorted(luminance(color) for color in colors)
    assert (light + 0.05) / (dark + 0.05) >= 4.5


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
    page.evaluate("document.fonts.ready")

    build_link = page.locator('.nav-links a[href="#what-i-build"]')
    skills_link = page.locator('.nav-links a[href="#skills"]')

    # Force a scroll (scroll_into_view_if_needed is a no-op when the section is
    # already on screen at this viewport size) to exercise the observer band.
    page.evaluate("() => document.getElementById('what-i-build').scrollIntoView({block: 'start'})")
    wait_for_section(page, "what-i-build")
    assert build_link.get_attribute("aria-current") == "page"

    page.evaluate("() => document.getElementById('skills').scrollIntoView({block: 'start'})")
    wait_for_section(page, "skills")
    assert skills_link.get_attribute("aria-current") == "page"
    assert build_link.get_attribute("aria-current") is None
    # Active state is not conveyed by color alone: a non-color affordance must change too.
    border_color = skills_link.evaluate("el => getComputedStyle(el).borderBottomColor")
    assert border_color != "rgba(0, 0, 0, 0)"


def test_logo_returns_to_top_and_clears_active_section(page: Page, test_url: str):
    page.set_viewport_size({"width": 1440, "height": 900})
    page.goto(test_url)
    page.evaluate("document.fonts.ready")

    page.evaluate("() => document.getElementById('experience').scrollIntoView({block: 'start'})")
    wait_for_section(page, "experience")
    exp_link = page.locator('.nav-links a[href="#experience"]')
    assert exp_link.get_attribute("aria-current") == "page"

    page.locator("a.logo").click()
    # Smooth-scroll (html { scroll-behavior: smooth }) animates the long
    # experience -> top jump, so poll for settling instead of a fixed sleep.
    page.wait_for_function("() => window.scrollY === 0", timeout=3000)

    expect(exp_link).not_to_have_attribute("aria-current", "page")
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
    page.evaluate("document.fonts.ready")
    page.evaluate("() => document.getElementById('education').scrollIntoView({block: 'start', behavior: 'instant'})")
    wait_for_section(page, "education")

    resume_btn = page.locator(".nav-resume-btn")
    assert resume_btn.count() == 1
    assert resume_btn.get_attribute("aria-current") is None


with open(os.path.join(DIRECTORY, "resume_variants.json")) as _source:
    RESUME_FILES = {name: v["file"] for name, v in json.load(_source)["variants"].items()}


@pytest.mark.parametrize("width", [390, 1440])
def test_nav_resume_cta_jumps_to_targeted_resume_choice(page: Page, test_url: str, width):
    page.set_viewport_size({"width": width, "height": 900})
    page.goto(test_url)
    page.evaluate("document.fonts.ready")

    resume_btn = page.locator(".nav-resume-btn")
    assert resume_btn.is_visible()
    assert resume_btn.get_attribute("href") == "#resume-downloads"
    resume_btn.click()
    choice = page.locator("#resume-downloads")
    expect(choice).to_be_in_viewport(timeout=5000)
    page.wait_for_function(
        "() => document.getElementById('resume-downloads').getBoundingClientRect().top >= 72",
        timeout=5000,
    )
    links = choice.locator("a.resume-action")
    assert [links.nth(i).get_attribute("href") for i in range(links.count())] == list(RESUME_FILES.values())
    for i in range(links.count()):
        expect(links.nth(i)).to_be_visible()


def test_mobile_nav_lists_both_targeted_resumes(page: Page, test_url: str):
    page.set_viewport_size({"width": 375, "height": 667})
    page.goto(test_url)

    page.locator(".mobile-menu-btn").click()
    links = page.locator(".mobile-resume-link")
    assert links.count() == len(RESUME_FILES)
    for i, (name, file) in enumerate(RESUME_FILES.items()):
        link = links.nth(i)
        assert link.is_visible()
        assert link.get_attribute("href") == file
        assert link.get_attribute("data-resume-variant") == name
        assert link.get_attribute("rel") == "noopener noreferrer"


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
    # Instant scrolling: the first disclosure sits at the bottom of a tall card,
    # and smooth scroll keeps the summary "unstable" long enough to miss the click.
    page.emulate_media(reduced_motion="reduce")
    page.goto(test_url)

    # Assert core resume content is visible
    name = page.locator("h1").inner_text()
    assert "William Elias" in name

    experience = page.locator(".timeline-content h3").first.inner_text()
    assert experience

    skill = page.locator(".skill-category h3").first.inner_text()
    assert skill

    detail = page.locator("#programs details").first
    detail.locator("summary").click()
    expect(detail).to_have_attribute("open", "")
    expect(detail.locator("li").first).to_be_visible()

    context.close()


@pytest.mark.parametrize("width", [390, 1440])
def test_navigation_links_reach_each_section(page: Page, test_url: str, width):
    page.set_viewport_size({"width": width, "height": 900})
    page.goto(test_url)
    page.evaluate("document.fonts.ready")
    for section in ("what-i-build", "programs", "experience", "projects", "education", "skills"):
        if width < 768:
            page.locator(".mobile-menu-btn").click()
            page.locator(f'.mobile-nav-links a[href="#{section}"]').click()
            expect(page.locator(".mobile-menu-btn")).to_have_attribute(
                "aria-expanded", "false"
            )
        else:
            page.locator(f'.nav-links a[href="#{section}"]').click()
        wait_for_section(page, section)


@pytest.mark.parametrize("width", [390, 1440])
def test_evidence_and_theme_controls_work_with_keyboard(page: Page, test_url: str, width):
    page.set_viewport_size({"width": width, "height": 900})
    page.emulate_media(color_scheme="dark")
    page.goto(test_url)
    page.locator("#theme-toggle").focus()
    page.keyboard.press("Enter")
    expect(page.locator("html")).to_have_attribute("data-theme", "light")
    page.locator("#colorblind-toggle").focus()
    page.keyboard.press("Space")
    expect(page.locator("html")).to_have_attribute("data-theme", "colorblind")
    expect(page.locator("#colorblind-toggle")).to_have_attribute("aria-pressed", "true")
    disclosures = page.locator("#programs details")
    assert disclosures.count() > 0
    for detail in disclosures.all():
        summary = detail.locator("summary")
        summary.focus()
        page.keyboard.press("Enter")
        expect(detail).to_have_attribute("open", "")
        expect(detail.locator("li").first).to_be_visible()
        page.keyboard.press("Space")
        expect(detail).not_to_have_attribute("open", "")


@pytest.mark.parametrize("variant", list(RESUME_FILES))
@pytest.mark.parametrize("scope", [".hero", "#resume-downloads", ".mobile-nav"])
def test_resume_actions_download_targeted_pdf(page: Page, test_url: str, scope, variant, tmp_path):
    page.set_viewport_size({"width": 390, "height": 900})
    page.goto(test_url)
    if scope == ".mobile-nav":
        page.locator(".mobile-menu-btn").click()
    with page.expect_download() as download_info:
        page.locator(f'{scope} a[data-resume-variant="{variant}"]').click()
    download = download_info.value
    assert download.suggested_filename == RESUME_FILES[variant]
    output = tmp_path / download.suggested_filename
    download.save_as(output)
    with open(os.path.join(DIRECTORY, RESUME_FILES[variant]), "rb") as source:
        assert output.read_bytes() == source.read()


def test_legacy_resume_url_still_serves_the_compatibility_pdf(page: Page, test_url: str):
    response = page.request.get(test_url.replace("index.html", "William_Elias_Resume.pdf"))
    assert response.ok
    with open(os.path.join(DIRECTORY, RESUME_FILES["production_devops"]), "rb") as source:
        assert response.body() == source.read()


@pytest.mark.parametrize("width", [320, 390, 810, 1024, 1440])
def test_resume_controls_are_touch_sized_and_need_no_hover(page: Page, test_url: str, width):
    page.set_viewport_size({"width": width, "height": 900})
    page.goto(test_url)
    page.evaluate("document.fonts.ready")
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    controls = page.locator("a.resume-action")
    assert controls.count() == 2 * len(RESUME_FILES)
    for i in range(controls.count()):
        control = controls.nth(i)
        control.scroll_into_view_if_needed()
        box = control.bounding_box()
        assert box["height"] >= 44 and box["width"] >= 44, box
        assert box["x"] >= 0 and box["x"] + box["width"] <= width
        # Visible without hovering: real text, not a hover-revealed menu.
        expect(control).to_be_visible()
        assert control.evaluate("el => el.tagName") == "A"
        assert control.get_attribute("href").endswith(".pdf")
    nav = page.locator(".nav-resume-btn").bounding_box()
    assert nav["height"] >= 44
    if width <= 620:
        # Stacked on narrow screens so each target spans the available width.
        hero = page.locator(".hero .resume-action")
        assert abs(hero.nth(0).bounding_box()["x"] - hero.nth(1).bounding_box()["x"]) <= 1


@pytest.mark.parametrize("width", [320, 1440])
def test_resume_controls_are_keyboard_reachable_with_visible_focus(page: Page, test_url: str, width):
    page.set_viewport_size({"width": width, "height": 900})
    page.goto(test_url)
    seen = []
    for _ in range(40):
        page.keyboard.press("Tab")
        info = page.evaluate("""() => {
            const el = document.activeElement;
            return {variant: el.dataset.resumeVariant || null,
                    inHero: !!el.closest('.hero'),
                    outline: getComputedStyle(el).outlineStyle,
                    width: getComputedStyle(el).outlineWidth};
        }""")
        if info["variant"] and info["inHero"]:
            assert info["outline"] == "solid" and info["width"] != "0px", info
            seen.append(info["variant"])
        if len(seen) == len(RESUME_FILES):
            break
    assert seen == list(RESUME_FILES)


def test_all_project_links_open_the_canonical_destination(page: Page, test_url: str):
    with open(os.path.join(DIRECTORY, "resume.json")) as source:
        projects = json.load(source)["projects"]
    # Check real click targets without making the regression suite depend on GitHub.
    for project in projects:
        page.context.route(project["link"], lambda route: route.fulfill(body="Repository"))
    page.goto(test_url)
    for project in projects:
        link = page.locator(f'#projects a[href="{project["link"]}"]')
        with page.expect_popup() as popup_info:
            link.click()
        popup = popup_info.value
        expect(popup).to_have_url(project["link"])
        popup.close()


@pytest.mark.parametrize("width", [1024, 1440])
@pytest.mark.parametrize("theme", ["dark", "light", "contrast-dark", "contrast-light"])
def test_engineering_impact_cards_desktop_alignment_and_expansion(page: Page, test_url: str, width, theme):
    page.set_viewport_size({"width": width, "height": 900})
    page.emulate_media(color_scheme="light" if theme.endswith("light") else "dark")
    page.goto(test_url)
    if theme.startswith("contrast"):
        page.locator("#colorblind-toggle").click()
    page.evaluate("document.fonts.ready")

    cards = page.locator(".program-card").all()
    assert len(cards) == 8
    grid = page.locator(".programs-grid").bounding_box()
    classes = [card.get_attribute("class") for card in cards]

    # Featured software cards share one row of equal columns and equal height,
    # with skill tags and disclosures aligned along the bottom.
    featured = [c for c, cls in zip(cards, classes) if "program-featured" in cls]
    assert len(featured) == 3
    boxes = [c.bounding_box() for c in featured]
    assert max(b["y"] for b in boxes) - min(b["y"] for b in boxes) <= 1.5
    assert max(b["width"] for b in boxes) - min(b["width"] for b in boxes) <= 1.5
    assert max(b["height"] for b in boxes) - min(b["height"] for b in boxes) <= 1.5
    details = [c.locator(".program-details").bounding_box() for c in featured]
    assert max(d["y"] for d in details) - min(d["y"] for d in details) <= 1.5

    # The wide case study spans the whole grid.
    wide = [c for c, cls in zip(cards, classes) if "program-wide" in cls]
    assert len(wide) == 1
    assert abs(wide[0].bounding_box()["width"] - grid["width"]) <= 1.5

    # Remaining cards pair up with equal heights and aligned disclosure rows.
    paired = [c for c, cls in zip(cards, classes) if "program-featured" not in cls and "program-wide" not in cls]
    assert len(paired) == 4
    for i in range(0, len(paired), 2):
        box_a, box_b = paired[i].bounding_box(), paired[i + 1].bounding_box()
        assert abs(box_a["y"] - box_b["y"]) <= 1.5
        assert abs(box_a["height"] - box_b["height"]) <= 1.5, (
            f"Pair {i // 2 + 1} cards height mismatch: {box_a['height']} vs {box_b['height']}"
        )
        det_a = paired[i].locator(".program-details").bounding_box()
        det_b = paired[i + 1].locator(".program-details").bounding_box()
        assert abs(det_a["y"] - det_b["y"]) <= 1.5, (
            f"Pair {i // 2 + 1} details alignment mismatch: {det_a['y']} vs {det_b['y']}"
        )

    # Expanding one card of a pair does not stretch its sibling awkwardly.
    # Compare against each card's own natural height: a shorter card can open
    # without exceeding its taller neighbour.
    first, second = paired[0], paired[1]
    page.evaluate("document.querySelector('.programs-grid').style.alignItems = 'start'")
    page.wait_for_timeout(100)
    collapsed_first_height = first.bounding_box()["height"]
    collapsed_second_height = second.bounding_box()["height"]
    page.evaluate("document.querySelector('.programs-grid').style.alignItems = ''")
    first.locator("summary").click()
    expect(first.locator(".program-details")).to_have_attribute("open", "")

    assert first.bounding_box()["height"] > collapsed_first_height + 50
    assert abs(second.bounding_box()["height"] - collapsed_second_height) <= 2.0, (
        f"Sibling should retain natural collapsed height, got {second.bounding_box()['height']}"
    )

    # Re-collapse and verify equal-height returns
    first.locator("summary").click()
    expect(first.locator(".program-details")).not_to_have_attribute("open", "")
    assert abs(first.bounding_box()["height"] - second.bounding_box()["height"]) <= 1.5


def test_engineering_impact_cards_mobile_layout(page: Page, test_url: str):
    page.set_viewport_size({"width": 390, "height": 844})
    page.goto(test_url)
    page.evaluate("document.fonts.ready")

    cards = page.locator(".program-card").all()
    assert len(cards) == 8

    prev_bottom = 0
    grid_box = page.locator(".programs-grid").bounding_box()
    for card in cards:
        box = card.bounding_box()
        assert box["y"] >= prev_bottom - 1  # Stacking vertically
        assert box["x"] >= grid_box["x"] - 1  # No horizontal overflow
        assert box["x"] + box["width"] <= grid_box["x"] + grid_box["width"] + 1
        prev_bottom = box["y"] + box["height"]
