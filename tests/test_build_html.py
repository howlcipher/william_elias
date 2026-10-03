import html

import pytest
from scripts.build_html import education_meta, esc, get_valid_url, inject, render_education, render_hero
from scripts.generate_linkedin_banner import banner_markup
from scripts.generate_resume_pdf import load_config

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

def test_render_hero_uses_theme_aware_portrait_with_intrinsic_dimensions():
    personal = {
        "name": "William Elias",
        "photo": "assets/images/william-elias-profile-hoodie-dark.webp",
        "photoDark": "assets/images/william-elias-profile-hoodie-dark.webp",
        "photoLight": "assets/images/william-elias-profile-hoodie-light.webp",
    }

    hero = render_hero(personal)

    assert 'class="profile-module"><div class="profile-frame">' in hero
    assert 'class="profile-photo"' in hero
    assert 'src="assets/images/william-elias-profile-hoodie-dark.webp"' in hero
    assert 'data-photo-dark="assets/images/william-elias-profile-hoodie-dark.webp"' in hero
    assert 'data-photo-light="assets/images/william-elias-profile-hoodie-light.webp"' in hero
    assert 'width="512" height="512"' in hero
    assert 'alt="Portrait of William Elias"' in hero


def test_in_progress_is_shown_once_and_blank_years_stay_blank():
    masters = {
        "icon": "fa-user-graduate",
        "degree": "M.S. Cyber Defense (In Progress)",
        "school": "Dakota State University",
        "year": "",
    }
    bachelor = {
        "icon": "fa-university",
        "degree": "B.S. Information Technology",
        "school": "Colorado State University Global Campus",
        "year": "",
    }
    business = {
        "icon": "fa-graduation-cap",
        "degree": "B.B.A. Business Administration",
        "school": "Rochester College",
        "year": "",
    }
    ccna = {
        "icon": "fa-certificate",
        "degree": "CCNA (Previously Held)",
        "school": "Cisco Networking Academy",
        "year": "2014 - 2017",
    }

    assert education_meta(masters) == "Dakota State University"
    assert education_meta(bachelor) == "Colorado State University Global Campus"
    assert education_meta(business) == "Rochester College"
    assert education_meta(ccna) == "Cisco Networking Academy (2014 - 2017)"

    card = render_education([masters, bachelor, business])
    assert card.count("In Progress") == 1
    assert "<h3>M.S. Cyber Defense (In Progress)</h3>" in card
    assert "<p>Dakota State University</p>" in card
    assert "<p>Colorado State University Global Campus</p>" in card
    assert "<p>Rochester College</p>" in card


def test_linkedin_banner_uses_the_current_title():
    personal = load_config()["personal"]
    markup = banner_markup(personal)
    assert html.escape(personal["title"]) in markup
    assert html.escape(personal["tagline"]) in markup
    assert "SOFTWARE // AUTOMATION" in markup
    assert "Software, DevOps" not in markup
    assert "DevOps &amp;" not in markup
