import json
import re

from scripts.generate_resume_pdf import SITE_DIR, load_config


def _index_html():
    return (SITE_DIR / "index.html").read_text(encoding="utf-8")


class TestCanonicalAndOgMeta:
    def test_canonical_url_matches_seo_config(self):
        cfg = load_config()
        canonical = cfg["seo"]["canonicalUrl"]
        html_content = _index_html()
        assert f'<link rel="canonical" href="{canonical}">' in html_content

    def test_og_url_matches_canonical(self):
        cfg = load_config()
        canonical = cfg["seo"]["canonicalUrl"]
        html_content = _index_html()
        match = re.search(r'<meta property="og:url" content="(.*?)">', html_content)
        assert match
        assert match.group(1) == canonical

    def test_og_type_and_site_name_present(self):
        html_content = _index_html()
        assert '<meta property="og:type" content="website">' in html_content
        site_name_match = re.search(r'<meta property="og:site_name" content="(.*?)">', html_content)
        assert site_name_match
        assert site_name_match.group(1)

    def test_meta_description_fits_search_snippet(self):
        # Search results truncate around 160 characters; the description has to
        # land the name, the target title, and the core keywords before the cut.
        cfg = load_config()
        html_content = _index_html()
        match = re.search(r'<meta name="description" content="(.*?)">', html_content)
        assert match
        desc = match.group(1)
        assert len(desc) <= 160, f"meta description is {len(desc)} chars and will be truncated"
        assert cfg["personal"]["name"] in desc
        assert "DevOps" in desc
        assert "Platform" in desc

    def test_twitter_title_and_description_present(self):
        html_content = _index_html()
        assert re.search(r'<meta name="twitter:title" content=".+?">', html_content)
        assert re.search(r'<meta name="twitter:description" content=".+?">', html_content)


class TestJsonLd:
    def _extract_json_ld(self):
        html_content = _index_html()
        match = re.search(
            r'<!-- BUILD:JSONLD:START -->(.*?)<!-- BUILD:JSONLD:END -->', html_content, re.DOTALL
        )
        assert match, "JSON-LD script block not found"
        return json.loads(match.group(1))

    def test_json_ld_is_valid_json(self):
        self._extract_json_ld()

    def test_json_ld_is_profile_page_with_person(self):
        data = self._extract_json_ld()
        assert data["@context"] == "https://schema.org"
        assert data["@type"] == "ProfilePage"
        person = data["mainEntity"]
        assert person["@type"] == "Person"

    def test_json_ld_person_matches_canonical_data(self):
        cfg = load_config()
        data = self._extract_json_ld()
        person = data["mainEntity"]
        assert person["name"] == cfg["personal"]["name"]
        assert person["jobTitle"] == cfg["personal"]["title"]
        assert cfg["personal"]["linkedin"] in person["sameAs"]
        assert cfg["personal"]["github"] in person["sameAs"]

    def test_json_ld_uses_curated_knows_about_subset(self):
        cfg = load_config()
        data = self._extract_json_ld()
        person = data["mainEntity"]
        assert person["knowsAbout"] == cfg["seo"]["knowsAbout"]
        assert len(person["knowsAbout"]) < 30

    def test_json_ld_excludes_phone_and_address(self):
        cfg = load_config()
        data = self._extract_json_ld()
        blob = json.dumps(data)
        assert cfg["personal"]["phone"] not in blob
        assert "address" not in blob.lower()
        assert "streetAddress" not in blob


class TestRobotsAndSitemap:
    def test_robots_txt_exists_and_allows_crawling(self):
        content = (SITE_DIR / "robots.txt").read_text(encoding="utf-8")
        assert "User-agent: *" in content
        assert "Allow: /" in content

    def test_robots_txt_references_sitemap(self):
        cfg = load_config()
        content = (SITE_DIR / "robots.txt").read_text(encoding="utf-8")
        canonical = cfg["seo"]["canonicalUrl"].rstrip("/")
        assert f"Sitemap: {canonical}/sitemap.xml" in content

    def test_sitemap_contains_canonical_url_only(self):
        cfg = load_config()
        content = (SITE_DIR / "sitemap.xml").read_text(encoding="utf-8")
        assert cfg["seo"]["canonicalUrl"] in content
        assert "github.com" not in content

    def test_sitemap_is_well_formed_xml(self):
        import xml.etree.ElementTree as ET

        content = (SITE_DIR / "sitemap.xml").read_text(encoding="utf-8")
        root = ET.fromstring(content)
        urls = root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url")
        assert len(urls) == 1


class TestNavigationCtas:
    def test_desktop_resume_nav_cta_exists(self):
        cfg = load_config()
        html_content = _index_html()
        nav_section = html_content.split('<div class="nav-right">')[1].split("</nav>")[0]
        assert "nav-resume-btn" in nav_section
        assert cfg["personal"]["resumePdf"] in nav_section

    def test_mobile_resume_nav_cta_exists(self):
        html_content = _index_html()
        assert "mobile-resume-link" in html_content

    def test_nav_resume_cta_not_marked_as_scroll_section(self):
        html_content = _index_html()
        nav_section = html_content.split('<div class="nav-right">')[1].split("</nav>")[0]
        assert 'href="#resume"' not in nav_section


class TestLogoHomeLink:
    def test_logo_is_accessible_home_anchor(self):
        html_content = _index_html()
        assert '<body id="top">' in html_content
        assert '<a href="#top" class="logo" aria-label="Home — return to top">WE.</a>' in html_content

    def test_no_duplicate_home_nav_item(self):
        html_content = _index_html()
        nav_section = html_content.split('<div class="nav-right">')[1].split("</nav>")[0]
        mobile_nav_section = html_content.split('<div class="mobile-nav"')[1].split("</div>")[0]
        assert ">Home<" not in nav_section
        assert ">Home<" not in mobile_nav_section

    def test_logo_not_marked_as_scroll_section(self):
        html_content = _index_html()
        assert html_content.count('class="logo"') == 1
        assert 'href="#top" class="logo"' in html_content


class TestBottomRecruiterCta:
    def test_recruiter_cta_section_exists(self):
        html_content = _index_html()
        assert 'id="contact-cta"' in html_content
        assert "Open to U.S. Remote Opportunities" in html_content

    def test_recruiter_cta_has_no_hype_language(self):
        html_content = _index_html()
        cta_section = html_content.split('id="contact-cta"')[1].split("</section>")[0]
        lowered = cta_section.lower()
        for phrase in ("hire me", "let's build the future", "10x engineer"):
            assert phrase not in lowered

    def test_recruiter_cta_exposes_email_linkedin_and_resume(self):
        cfg = load_config()
        html_content = _index_html()
        cta_section = html_content.split('id="contact-cta"')[1].split("</section>")[0]
        assert f'mailto:{cfg["personal"]["email"]}' in cta_section
        assert cfg["personal"]["linkedin"] in cta_section
        assert cfg["personal"]["resumePdf"] in cta_section

    def test_recruiter_cta_precedes_footer(self):
        html_content = _index_html()
        assert html_content.index('id="contact-cta"') < html_content.index("<footer>")


class TestProjectCardActions:
    def test_project_cards_expose_explicit_repository_action(self):
        html_content = _index_html()
        projects_section = html_content.split('id="projects-target"')[1].split('<!-- BUILD:PROJECTS:END -->')[0]
        assert projects_section.count("project-link") == 6
        assert "View Repository" in projects_section

    def test_project_links_use_safe_external_attributes(self):
        html_content = _index_html()
        projects_section = html_content.split('id="projects-target"')[1].split('<!-- BUILD:PROJECTS:END -->')[0]
        for link_html in re.findall(r'<a [^>]*class="contact-pill project-link"[^>]*>', projects_section):
            assert 'target="_blank"' in link_html
            assert 'rel="noopener noreferrer"' in link_html


class TestGeneratedAssetsFreshness:
    def test_robots_and_sitemap_match_seo_config(self):
        cfg = load_config()
        canonical = cfg["seo"]["canonicalUrl"]
        robots = (SITE_DIR / "robots.txt").read_text(encoding="utf-8")
        sitemap = (SITE_DIR / "sitemap.xml").read_text(encoding="utf-8")
        assert canonical.rstrip("/") in robots
        assert canonical in sitemap
