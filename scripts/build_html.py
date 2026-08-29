#!/usr/bin/env python3
import json
import re
import html
from pathlib import Path

SITE_DIR = Path(__file__).resolve().parent.parent


def get_valid_url(url, allow_relative=False):
    if not isinstance(url, str) or not url:
        return None
    if allow_relative and ':' not in url:
        return url
    return url if re.match(r'^https?://', url, re.IGNORECASE) else None


def esc(value):
    return html.escape(str(value or ''), quote=True)


def render_hero(personal):
    # Keep the content in reading order -- eyebrow, heading, subtitle, tagline,
    # supporting line, portrait, then contact actions -- so the mobile single-column grid needs
    # no order overrides. Desktop uses named grid areas on `.hero-content` to
    # move the complete profile module into a right-hand column.
    parts = []
    eyebrow_bits = [b for b in (personal.get("location", ""), personal.get("remote", "")) if b]
    parts.append(f'<p class="eyebrow">{esc(" | ".join(eyebrow_bits))}</p>')
    parts.append(f'<h1>{esc(personal.get("name", ""))}</h1>')
    parts.append(f'<h2 class="subtitle">{esc(personal.get("title", ""))}</h2>')
    parts.append(f'<p class="tagline terminal-type">{esc(personal.get("tagline", ""))}</p>')
    if personal.get('supporting'):
        parts.append(f'<p class="hero-supporting">{esc(personal.get("supporting"))}</p>')

    photo = get_valid_url(personal.get('photo'), allow_relative=True)
    photo_dark = get_valid_url(personal.get('photoDark'), allow_relative=True)
    photo_light = get_valid_url(personal.get('photoLight'), allow_relative=True)
    if photo and photo_dark and photo_light:
        parts.append(
            '<div class="profile-module">'
            '<div class="profile-frame">'
            f'<img class="profile-photo" src="{esc(photo_dark)}" '
            f'data-photo-dark="{esc(photo_dark)}" '
            f'data-photo-light="{esc(photo_light)}" '
            'width="512" height="512" decoding="async" fetchpriority="high" '
            'alt="Portrait of William Elias">'
            '</div>'
            '</div>'
        )

    parts.append('<div class="contact-info">')

    if personal.get('email'):
        parts.append(
            f'<a href="mailto:{esc(personal["email"])}" class="contact-pill">'
            '<i class="fas fa-envelope" aria-hidden="true"></i> Email</a>'
        )

    linkedin = get_valid_url(personal.get('linkedin'))
    if linkedin:
        parts.append(
            f'<a href="{esc(linkedin)}" target="_blank" rel="noopener noreferrer" class="contact-pill">'
            '<i class="fab fa-linkedin" aria-hidden="true"></i> LinkedIn</a>'
        )

    github = get_valid_url(personal.get('github'))
    if github:
        parts.append(
            f'<a href="{esc(github)}" target="_blank" rel="noopener noreferrer" class="contact-pill">'
            '<i class="fab fa-github" aria-hidden="true"></i> GitHub</a>'
        )

    resume_pdf = get_valid_url(personal.get('resumePdf'), allow_relative=True)
    if resume_pdf:
        parts.append(
            f'<a href="{esc(resume_pdf)}" target="_blank" rel="noopener noreferrer" class="contact-pill primary-action">'
            '<i class="fas fa-file-pdf" aria-hidden="true"></i> Resume PDF</a>'
        )

    parts.append('</div>')

    return ''.join(parts)


def render_summary(about_or_summary):
    paragraphs = [p.strip() for p in str(about_or_summary or '').split('\n\n') if p.strip()]
    return ''.join(f'<p>{esc(p)}</p>' for p in paragraphs)


def render_stats(stats):
    parts = []
    for stat in stats or []:
        parts.append(
            '<div class="stat-card">'
            f'<strong>{esc(stat.get("value", ""))}</strong>'
            f'<span>{esc(stat.get("label", ""))}</span>'
            '</div>'
        )
    return ''.join(parts)


def render_skills(skills):
    parts = []
    for skill in skills or []:
        tags = ''.join(f'<span>{esc(tag)}</span>' for tag in (skill.get('tags') or []))
        parts.append(
            '<div class="skill-category card">'
            f'<div class="skill-icon"><i class="fas {esc(skill.get("icon", ""))}"></i></div>'
            f'<h3>{esc(skill.get("category", ""))}</h3>'
            f'<div class="skill-tags">{tags}</div>'
            '</div>'
        )
    return ''.join(parts)


def render_experience(experience):
    parts = []
    for job in experience or []:
        subtitle = esc(job.get('company', ''))
        if job.get('location'):
            subtitle += f' | {esc(job["location"])}'
        achievements = ''.join(f'<li>{esc(a)}</li>' for a in (job.get('achievements') or []))
        parts.append(
            '<div class="timeline-item card">'
            '<div class="timeline-dot"></div>'
            f'<div class="timeline-date">{esc(job.get("date", ""))}</div>'
            '<div class="timeline-content">'
            f'<h3>{esc(job.get("title", ""))}</h3>'
            f'<h4>{subtitle}</h4>'
            f'<ul>{achievements}</ul>'
            '</div>'
            '</div>'
        )
    return ''.join(parts)


def render_programs(programs):
    parts = []
    for prog in programs or []:
        bullets = ''.join(f'<li>{esc(b)}</li>' for b in (prog.get('bullets') or []))
        tech = ''.join(f'<span>{esc(t)}</span>' for t in (prog.get('technology') or []))
        parts.append(
            '<div class="program-card card">'
            f'<h3>{esc(prog.get("name", ""))}</h3>'
            f'<ul>{bullets}</ul>'
            f'<div class="skill-tags">{tech}</div>'
            '</div>'
        )
    return ''.join(parts)


def render_ai_capabilities(tiers):
    parts = []
    for tier in tiers or []:
        items = ''.join(f'<span>{esc(i)}</span>' for i in (tier.get('items') or []))
        parts.append(
            '<div class="capability-tier">'
            f'<h3>{esc(tier.get("tier", ""))}</h3>'
            f'<div class="skill-tags">{items}</div>'
            '</div>'
        )
    return '<div class="capability-arrow" aria-hidden="true"><i class="fas fa-arrow-down"></i></div>'.join(parts)


def render_projects(projects):
    parts = []
    for proj in projects or []:
        highlights = ''.join(f'<li>{esc(h)}</li>' for h in (proj.get('highlights') or []))
        tags = ''.join(f'<span>{esc(tag)}</span>' for tag in (proj.get('tags') or []))
        card = [
            '<div class="project-card card">',
            f'<h3>{esc(proj.get("name", ""))}</h3>',
            f'<div class="project-subtitle">{esc(proj.get("subtitle", ""))}</div>',
            f'<ul>{highlights}</ul>',
            f'<div class="skill-tags">{tags}</div>',
        ]
        link = get_valid_url(proj.get('link'))
        if link:
            card.append(
                '<div class="project-card-footer">'
                f'<a href="{esc(link)}" target="_blank" rel="noopener noreferrer" class="contact-pill project-link">'
                '<i class="fas fa-code-branch" aria-hidden="true"></i> View Repository '
                '<span aria-hidden="true">&rarr;</span></a>'
                '</div>'
            )
        card.append('</div>')
        parts.append(''.join(card))
    return ''.join(parts)


def render_nav_resume(personal):
    resume_pdf = get_valid_url(personal.get('resumePdf'), allow_relative=True)
    if not resume_pdf:
        return ''
    return (
        f'<a href="{esc(resume_pdf)}" target="_blank" rel="noopener noreferrer" class="nav-resume-btn">'
        '<i class="fas fa-file-pdf" aria-hidden="true"></i> Resume</a>'
    )


def render_mobile_nav_resume(personal):
    resume_pdf = get_valid_url(personal.get('resumePdf'), allow_relative=True)
    if not resume_pdf:
        return ''
    return (
        '<li>'
        f'<a href="{esc(resume_pdf)}" target="_blank" rel="noopener noreferrer" class="mobile-link mobile-resume-link">'
        '<i class="fas fa-file-pdf" aria-hidden="true"></i> Resume</a>'
        '</li>'
    )


def render_cta_copy(personal):
    return (
        '<p class="cta-copy">Software, DevOps, and automation engineer focused on building software, '
        'automating workflows, CI/CD delivery, production reliability, and AI-enabled tooling.</p>'
    )


def render_cta_actions(personal):
    parts = []

    if personal.get('email'):
        parts.append(
            f'<a href="mailto:{esc(personal["email"])}" class="contact-pill">'
            '<i class="fas fa-envelope" aria-hidden="true"></i> Email Me</a>'
        )

    linkedin = get_valid_url(personal.get('linkedin'))
    if linkedin:
        parts.append(
            f'<a href="{esc(linkedin)}" target="_blank" rel="noopener noreferrer" class="contact-pill">'
            '<i class="fab fa-linkedin" aria-hidden="true"></i> LinkedIn</a>'
        )

    resume_pdf = get_valid_url(personal.get('resumePdf'), allow_relative=True)
    if resume_pdf:
        parts.append(
            f'<a href="{esc(resume_pdf)}" target="_blank" rel="noopener noreferrer" class="contact-pill primary-action">'
            '<i class="fas fa-file-pdf" aria-hidden="true"></i> Resume PDF</a>'
        )

    github = get_valid_url(personal.get('github'))
    if github:
        parts.append(
            f'<a href="{esc(github)}" target="_blank" rel="noopener noreferrer" class="contact-pill">'
            '<i class="fab fa-github" aria-hidden="true"></i> GitHub</a>'
        )

    return ''.join(parts)


def render_json_ld(data):
    personal = data.get('personal', {})
    seo = data.get('seo', {})
    canonical_url = get_valid_url(seo.get('canonicalUrl')) or ''

    photo = get_valid_url(personal.get('photo'), allow_relative=True)
    image_url = None
    if photo and canonical_url:
        image_url = canonical_url.rstrip('/') + '/' + photo.lstrip('/')

    same_as = [u for u in (get_valid_url(personal.get('linkedin')), get_valid_url(personal.get('github'))) if u]

    person = {
        '@type': 'Person',
        'name': personal.get('name', ''),
        'jobTitle': personal.get('title', ''),
        'description': personal.get('tagline', ''),
    }
    if canonical_url:
        person['url'] = canonical_url
    if image_url:
        person['image'] = image_url
    if same_as:
        person['sameAs'] = same_as
    if seo.get('knowsAbout'):
        person['knowsAbout'] = seo['knowsAbout']

    profile_page = {
        '@context': 'https://schema.org',
        '@type': 'ProfilePage',
        'name': seo.get('siteName') or f"{personal.get('name', '')} | {personal.get('title', '')}",
        'mainEntity': person,
    }
    if canonical_url:
        profile_page['url'] = canonical_url

    return json.dumps(profile_page, indent=2)


def build_robots(canonical_url):
    canonical_url = canonical_url.rstrip('/') + '/' if canonical_url else ''
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        f"Sitemap: {canonical_url}sitemap.xml\n"
    )
    (SITE_DIR / 'robots.txt').write_text(content)


def build_sitemap(canonical_url):
    canonical_url = canonical_url.rstrip('/') + '/' if canonical_url else ''
    content = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        '  <url>\n'
        f'    <loc>{esc(canonical_url)}</loc>\n'
        '  </url>\n'
        '</urlset>\n'
    )
    (SITE_DIR / 'sitemap.xml').write_text(content)


def render_additional_experience(items):
    parts = []
    for job in items or []:
        parts.append(
            '<article class="additional-item">'
            f'<div><h3>{esc(job.get("company", ""))}</h3><p>{esc(job.get("title", ""))}</p></div>'
            f'<p class="additional-date">{esc(job.get("date", ""))}</p>'
            f'<p class="additional-summary">{esc(job.get("summary", ""))}</p>'
            '</article>'
        )
    return ''.join(parts)


def render_education(education):
    parts = []
    for edu in education or []:
        school = esc(edu.get('school', ''))
        if edu.get('year'):
            school += f' ({esc(edu["year"])})'
        parts.append(
            '<div class="edu-card card">'
            f'<div class="edu-icon"><i class="fas {esc(edu.get("icon", ""))}"></i></div>'
            f'<div class="edu-info"><h3>{esc(edu.get("degree", ""))}</h3><p>{school}</p></div>'
            '</div>'
        )
    return ''.join(parts)


def inject(html_content, marker, content):
    start = f'<!-- BUILD:{marker}:START -->'
    end = f'<!-- BUILD:{marker}:END -->'
    pattern = re.escape(start) + r'.*?' + re.escape(end)
    replacement = start + content + end
    new_html, count = re.subn(pattern, lambda m: replacement, html_content, flags=re.DOTALL)
    if count == 0:
        raise ValueError(f"Marker pair for {marker} not found in HTML content")
    return new_html


def build_html():
    with open(SITE_DIR / 'resume.json', 'r') as f:
        data = json.load(f)

    personal = data.get('personal', {})
    name = personal.get('name', '')
    title = personal.get('title', '')
    tagline = personal.get('tagline', '').replace(" // ", ", ")

    seo = data.get('seo', {})
    canonical_url = get_valid_url(seo.get('canonicalUrl')) or ''
    site_name = seo.get('siteName') or f"{name} | {title}"

    page_title = html.escape(f"{name} | {title}", quote=True)
    seo_suffix = "Python & FastAPI, C#/.NET, CI/CD, Azure DevOps, and AI-enabled engineering."
    # Search snippets cut off around 160 characters, so the meta description
    # carries name, title, and the core keywords and stops there. OG/Twitter
    # stay tagline-led, where the longer line still renders in full.
    description = (
        "Software, DevOps, and automation engineer: Python, FastAPI, C#/.NET, "
        "CI/CD, Azure DevOps, production reliability, and AI-enabled engineering."
    )
    escaped_desc = html.escape(description, quote=True)
    escaped_og_desc = html.escape(f"{tagline[:1].upper() + tagline[1:] if tagline else ''}. {seo_suffix}", quote=True)
    escaped_site_name = html.escape(site_name, quote=True)

    with open(SITE_DIR / 'index.html', 'r') as f:
        html_content = f.read()

    # Update <title>
    html_content = re.sub(
        r'<title>.*?</title>',
        lambda m: f'<title>{page_title}</title>',
        html_content
    )

    # Update <meta name="description">
    html_content = re.sub(
        r'<meta name="description" content=".*?">',
        lambda m: f'<meta name="description" content="{escaped_desc}">',
        html_content
    )

    # Update <meta property="og:title">
    html_content = re.sub(
        r'<meta property="og:title" content=".*?">',
        lambda m: f'<meta property="og:title" content="{page_title}">',
        html_content
    )

    # Update <meta property="og:description">
    html_content = re.sub(
        r'<meta property="og:description" content=".*?">',
        lambda m: f'<meta property="og:description" content="{escaped_og_desc}">',
        html_content
    )

    # Update <meta property="og:url">
    html_content = re.sub(
        r'<meta property="og:url" content=".*?">',
        lambda m: f'<meta property="og:url" content="{esc(canonical_url)}">',
        html_content
    )

    # Update <meta property="og:type">
    html_content = re.sub(
        r'<meta property="og:type" content=".*?">',
        lambda m: '<meta property="og:type" content="website">',
        html_content
    )

    # Update <meta property="og:site_name">
    html_content = re.sub(
        r'<meta property="og:site_name" content=".*?">',
        lambda m: f'<meta property="og:site_name" content="{escaped_site_name}">',
        html_content
    )

    # Update <meta name="twitter:title">
    html_content = re.sub(
        r'<meta name="twitter:title" content=".*?">',
        lambda m: f'<meta name="twitter:title" content="{page_title}">',
        html_content
    )

    # Update <meta name="twitter:description">
    html_content = re.sub(
        r'<meta name="twitter:description" content=".*?">',
        lambda m: f'<meta name="twitter:description" content="{escaped_og_desc}">',
        html_content
    )

    # Update <link rel="canonical">
    html_content = re.sub(
        r'<link rel="canonical" href=".*?">',
        lambda m: f'<link rel="canonical" href="{esc(canonical_url)}">',
        html_content
    )

    # Pre-render body content sections for SEO/no-JS visibility
    html_content = inject(html_content, 'HERO', render_hero(personal))
    html_content = inject(html_content, 'SUMMARY', render_summary(data.get('about') or data.get('summary', '')))
    html_content = inject(html_content, 'STATS', render_stats(data.get('stats')))
    html_content = inject(html_content, 'SKILLS', render_skills(data.get('skills')))
    exp_combined = data.get('experience', [])[:]
    for job in data.get('additionalExperience', []):
        job_copy = dict(job)
        if 'summary' in job_copy:
            job_copy['achievements'] = [job_copy['summary']]
        exp_combined.append(job_copy)
    html_content = inject(html_content, 'EXPERIENCE', render_experience(exp_combined))
    html_content = inject(html_content, 'PROGRAMS', render_programs(data.get('selectedEngineeringPrograms')))
    html_content = inject(html_content, 'AI_CAPABILITIES', render_ai_capabilities(data.get('aiEngineeringCapabilities')))
    html_content = inject(html_content, 'PROJECTS', render_projects(data.get('projects')))

    html_content = inject(html_content, 'EDUCATION', render_education(data.get('education')))
    html_content = inject(html_content, 'FOOTER', esc(data.get('footerText', '')))
    html_content = inject(html_content, 'NAV_RESUME', render_nav_resume(personal))
    html_content = inject(html_content, 'MOBILE_NAV_RESUME', render_mobile_nav_resume(personal))
    html_content = inject(html_content, 'CTA_COPY', render_cta_copy(personal))
    html_content = inject(html_content, 'CTA_ACTIONS', render_cta_actions(personal))
    html_content = inject(html_content, 'JSONLD', render_json_ld(data))

    with open(SITE_DIR / 'index.html', 'w') as f:
        f.write(html_content)

    build_robots(canonical_url)
    build_sitemap(canonical_url)


if __name__ == "__main__":
    build_html()
