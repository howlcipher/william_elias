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
    parts = ['<div class="hero-copy">']
    parts.append(f'<p class="eyebrow">{esc(personal.get("location", ""))} // AVAILABLE FOR REMOTE</p>')
    parts.append(f'<h1>{esc(personal.get("name", ""))}</h1>')
    parts.append(f'<h2 class="subtitle">{esc(personal.get("title", ""))}</h2>')
    parts.append(f'<p class="tagline terminal-type">{esc(personal.get("tagline", ""))}</p>')
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
    parts.append('</div>')

    photo = get_valid_url(personal.get('photo'), allow_relative=True)
    if photo:
        parts.append(
            f'<img class="profile-photo" src="{esc(photo)}" '
            f'alt="Professional headshot of {esc(personal.get("name", ""))}">'
        )

    return ''.join(parts)


def render_summary(summary):
    return f'<p>{esc(summary)}</p>'


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
                '<div style="margin-top: 1rem;">'
                f'<a href="{esc(link)}" target="_blank" rel="noopener noreferrer" class="contact-pill project-link">'
                '<i class="fas fa-external-link-alt" aria-hidden="true"></i> View Project</a>'
                '</div>'
            )
        card.append('</div>')
        parts.append(''.join(card))
    return ''.join(parts)


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

    page_title = html.escape(f"{name} | {title}", quote=True)
    escaped_desc = html.escape(f"Resume of {name}, a {title}. {tagline}.", quote=True)
    escaped_og_desc = html.escape(f"{tagline[:1].upper() + tagline[1:] if tagline else ''}.", quote=True)

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

    # Pre-render body content sections for SEO/no-JS visibility
    html_content = inject(html_content, 'HERO', render_hero(personal))
    html_content = inject(html_content, 'SUMMARY', render_summary(data.get('summary', '')))
    html_content = inject(html_content, 'STATS', render_stats(data.get('stats')))
    html_content = inject(html_content, 'SKILLS', render_skills(data.get('skills')))
    html_content = inject(html_content, 'EXPERIENCE', render_experience(data.get('experience')))
    html_content = inject(html_content, 'PROJECTS', render_projects(data.get('projects')))
    html_content = inject(html_content, 'ADDITIONAL', render_additional_experience(data.get('additionalExperience')))
    html_content = inject(html_content, 'EDUCATION', render_education(data.get('education')))
    html_content = inject(html_content, 'FOOTER', esc(data.get('footerText', '')))

    with open(SITE_DIR / 'index.html', 'w') as f:
        f.write(html_content)


if __name__ == "__main__":
    build_html()
