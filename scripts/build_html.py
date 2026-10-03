#!/usr/bin/env python3
import json
import re
import html
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SITE_DIR = Path(__file__).resolve().parent.parent


def get_valid_url(url, allow_relative=False):
    if not isinstance(url, str) or not url:
        return None
    if allow_relative and ':' not in url:
        return url
    return url if re.match(r'^https?://', url, re.IGNORECASE) else None


def esc(value):
    return html.escape(str(value or ''), quote=True)


def load_resume_variants():
    """Targeted résumé downloads, in the order resume_variants.json defines them."""
    with open(SITE_DIR / 'resume_variants.json', 'r') as f:
        variants = json.load(f)['variants']
    return [
        {'key': key, 'label': v['label'], 'audience': v['audience'], 'file': v['file']}
        for key, v in variants.items()
    ]


def render_resume_links(resumes, link_class, with_audience=False):
    # Plain anchors, one per targeted résumé: no dropdown, hover, or nested
    # focus state, so touch, keyboard, and no-JS visitors get the same choice.
    parts = []
    for resume in resumes or []:
        href = get_valid_url(resume.get('file'), allow_relative=True)
        if not href:
            continue
        audience = (
            f'<span class="resume-audience">{esc(resume["audience"])}</span>'
            if with_audience and resume.get('audience') else ''
        )
        parts.append(
            f'<a href="{esc(href)}" target="_blank" rel="noopener noreferrer" class="{link_class}" '
            f'data-resume-variant="{esc(resume["key"])}">'
            '<i class="fas fa-file-arrow-down" aria-hidden="true"></i> '
            f'<span class="resume-text"><span class="resume-label">{esc(resume["label"])}</span>{audience}</span>'
            '<span class="visually-hidden"> (PDF)</span></a>'
        )
    return ''.join(parts)


def render_hero(personal, resumes=(), employer=""):
    # Keep the content in reading order -- eyebrow, heading, subtitle, tagline,
    # supporting line, portrait, then contact actions -- so the mobile single-column grid needs
    # no order overrides. Desktop uses named grid areas on `.hero-content` to
    # move the complete profile module into a right-hand column.
    parts = []
    eyebrow_bits = [b for b in (personal.get("location", ""), personal.get("remote", "")) if b]
    parts.append(f'<p class="eyebrow">{esc(" | ".join(eyebrow_bits))}</p>')
    parts.append(f'<h1>{esc(personal.get("name", ""))}</h1>')
    parts.append(f'<h2 class="subtitle">{esc(personal.get("title", ""))}</h2>')
    if employer:
        parts.append(f'<p class="hero-employer">{esc(employer)}</p>')
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

    resume_links = render_resume_links(resumes, 'contact-pill primary-action resume-action')
    if resume_links:
        parts.append(
            '<div class="resume-actions" role="group" aria-label="Download a targeted resume (PDF)">'
            f'{resume_links}</div>'
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

    parts.append('</div>')

    return ''.join(parts)


def render_skills(skills):
    parts = []
    for skill in skills or []:
        tags = ''.join(f'<span>{esc(tag)}</span>' for tag in (skill.get('tags') or []))
        parts.append(
            '<div class="skill-category card">'
            f'<div class="skill-icon"><i class="fas {esc(skill.get("icon", ""))}" aria-hidden="true"></i></div>'
            f'<h3>{esc(skill.get("category", ""))}</h3>'
            f'<p class="skill-context">{esc(skill.get("context", ""))}</p>'
            f'<div class="skill-tags">{tags}</div>'
            '</div>'
        )
    return ''.join(parts)


def render_experience(experience, summaries=None):
    # A role with a site summary links to Selected Work instead of repeating its
    # case studies; the PDFs still list every selected achievement.
    summaries = summaries or {}
    parts = []
    for job in experience or []:
        subtitle = esc(job.get('company', ''))
        if job.get('location'):
            subtitle += f' | {esc(job["location"])}'
        summary = summaries.get(job.get('id'))
        if summary:
            achievements = (
                f'<li>{esc(summary)}</li>'
                '<li><a href="#programs" class="inline-link">Selected Work</a> '
                'has the systems, scope, and verification behind this role.</li>'
            )
        else:
            achievements = ''.join(f'<li>{esc(a["text"])}</li>' for a in (job.get('achievements') or []))
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


def order_programs(programs, selected_work=None):
    """Programs in Selected Work order; any program not listed keeps its place at the end."""
    order = (selected_work or {}).get('order') or []
    by_id = {p.get('id'): p for p in programs or []}
    ordered = [by_id[i] for i in order if i in by_id]
    return ordered + [p for p in programs or [] if p.get('id') not in order]


def render_programs(programs, selected_work=None, stats=None):
    selected_work = selected_work or {}
    featured = set(selected_work.get('featured') or [])
    wide = set(selected_work.get('wide') or [])
    context = selected_work.get('context') or {}
    label = selected_work.get('provenanceLabel', '')
    metrics_by_program = {}
    for stat in stats or []:
        metrics_by_program.setdefault(stat.get('sourceProgram'), []).append(stat)
    parts = []
    for prog in order_programs(programs, selected_work):
        # Context lines restate some bullets as Scope / Implementation / Verification;
        # those bullets are not repeated on the site (the PDFs still use them).
        restated = set((selected_work.get('restatedBullets') or {}).get(prog.get('id'), []))
        bullets = ''.join(
            f'<li>{esc(b)}</li>' for i, b in enumerate(prog.get('bullets') or []) if i not in restated)
        bullets = f'<ul>{bullets}</ul>' if bullets else ''
        details = ''.join(f'<li>{esc(b)}</li>' for b in (prog.get('details') or []))
        tech = ''.join(f'<span>{esc(t)}</span>' for t in (prog.get('technology') or []))
        evidence = (
            '<details class="program-details"><summary>Implementation &amp; validation</summary>'
            f'<ul>{details}</ul></details>'
        ) if details else ''
        # Hero figures belong on the wide case-study card. A single figure on a
        # paired card (credential remediation) is a one-off layout; that count
        # stays in the program's normal bullets instead.
        metrics = ''
        if prog.get('id') in wide:
            metrics = ''.join(
                f'<li><strong>{esc(m.get("value", ""))}</strong> <span>{esc(m.get("label", ""))}</span></li>'
                for m in metrics_by_program.get(prog.get('name'), [])
            )
            metrics = f'<ul class="program-metrics" aria-label="Key figures">{metrics}</ul>' if metrics else ''
        lines = ''.join(
            f'<div><dt>{esc(line.get("label", ""))}</dt><dd>{esc(line.get("text", ""))}</dd></div>'
            for line in context.get(prog.get('id'), [])
        )
        lines = f'<dl class="program-context">{lines}</dl>' if lines else ''
        classes = 'program-card card' + (' program-featured' if prog.get('id') in featured else '')
        classes += ' program-wide' if prog.get('id') in wide else ''
        provenance = f'<p class="provenance-label">{esc(label)}</p>' if label else ''
        parts.append(
            f'<article class="{classes}" id="{esc(prog.get("id", ""))}">'
            f'{provenance}<h3>{esc(prog.get("name", ""))}</h3>'
            f'{metrics}{lines}{bullets}'
            f'<div class="skill-tags">{tech}</div>'
            f'{evidence}</article>'
        )
    return ''.join(parts)


def render_what_i_build(what_i_build):
    parts = []
    for item in (what_i_build or {}).get('items') or []:
        stack = ''.join(f'<span>{esc(t)}</span>' for t in (item.get('stack') or []))
        target = esc(item.get('programId', ''))
        parts.append(
            '<article class="build-card card">'
            f'<p class="provenance-label">{esc(item.get("provenance", ""))}</p>'
            f'<h3>{esc(item.get("name", ""))}</h3>'
            f'<div class="skill-tags build-stack">{stack}</div>'
            f'<p class="build-summary">{esc(item.get("summary", ""))}</p>'
            f'<a href="#{target}" class="inline-link build-link">How it was built '
            '<span aria-hidden="true">&rarr;</span></a>'
            '</article>'
        )
    return ''.join(parts)


def render_portfolio_note(personal, note):
    if not note:
        return ''
    source = get_valid_url(personal.get('sourceRepo'))
    link = (
        f' <a href="{esc(source)}" target="_blank" rel="noopener noreferrer" class="inline-link">'
        'View the source<span class="visually-hidden"> (opens in a new tab)</span></a>'
    ) if source else ''
    return f'<p>{esc(note)}{link}</p>'



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


def render_about(about):
    paragraphs = [part.strip() for part in (about or '').split('\n\n') if part.strip()]
    if not paragraphs:
        return ''
    body = ''.join(f'<p>{esc(paragraph)}</p>' for paragraph in paragraphs)
    return f'<div class="card about-copy">{body}</div>'


def render_projects(projects, provenance_label=''):
    parts = []
    for proj in projects or []:
        highlights = ''.join(f'<li>{esc(h)}</li>' for h in (proj.get('highlights') or []))
        tags = ''.join(f'<span>{esc(tag)}</span>' for tag in (proj.get('tags') or []))
        card = [
            '<div class="project-card card">',
            f'<p class="provenance-label provenance-independent">{esc(provenance_label)}</p>' if provenance_label else '',
            f'<h3>{esc(proj.get("name", ""))}</h3>',
            f'<div class="project-subtitle">{esc(proj.get("subtitle", ""))}</div>',
            f'<ul>{highlights}</ul>',
            f'<div class="skill-tags">{tags}</div>',
        ]
        actions = []
        link = get_valid_url(proj.get('link'))
        if link:
            actions.append(
                f'<a href="{esc(link)}" target="_blank" rel="noopener noreferrer" class="contact-pill project-link">'
                '<i class="fas fa-code-branch" aria-hidden="true"></i> View Repository '
                '<span aria-hidden="true">&rarr;</span></a>'
            )
        live = get_valid_url(proj.get('liveUrl'))
        if live:
            actions.append(
                f'<a href="{esc(live)}" target="_blank" rel="noopener noreferrer" class="contact-pill project-live-link">'
                '<i class="fas fa-globe" aria-hidden="true"></i> View Live Page '
                '<span aria-hidden="true">&rarr;</span></a>'
            )
        if actions:
            card.append(f'<div class="project-card-footer">{"".join(actions)}</div>')
        card.append('</div>')
        parts.append(''.join(card))
    return ''.join(parts)


def render_nav_resume(resumes):
    # The navbar has room for one compact control at every width, so it jumps
    # to the labelled two-résumé choice instead of picking a variant itself.
    if not resumes:
        return ''
    return (
        '<a href="#resume-downloads" class="nav-resume-btn">'
        '<i class="fas fa-file-pdf" aria-hidden="true"></i> Resumes</a>'
    )


def render_mobile_nav_resume(resumes):
    return ''.join(
        f'<li>{render_resume_links([resume], "mobile-link mobile-resume-link")}</li>'
        for resume in resumes or []
    )


def render_cta_resumes(resumes, intro=''):
    links = render_resume_links(resumes, 'contact-pill primary-action resume-action', with_audience=True)
    if not links:
        return ''
    intro_html = f'<p class="resume-choice-intro">{esc(intro)}</p>' if intro else ''
    return (
        f'{intro_html}<p class="resume-choice-label" id="resume-choice-label">Choose the resume that fits the role:</p>'
        f'<div class="resume-choice-actions" role="group" aria-labelledby="resume-choice-label">{links}</div>'
    )


def render_cta_copy(personal):
    return f'<p class="cta-copy">{esc(personal.get("contactCopy", ""))}</p>'


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

    # jobTitle is the official, employer-issued current title. Positioning
    # language (Software & Automation Engineer, platform, DevEx, ...) belongs in
    # description/knowsAbout, never in a title the person does not hold.
    current = next(iter(data.get('experience') or []), {})
    person = {
        '@type': 'Person',
        'name': personal.get('name', ''),
        'jobTitle': current.get('officialTitle') or current.get('title', ''),
        'description': seo.get('personDescription') or personal.get('tagline', ''),
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
        person['@id'] = canonical_url + '#person'
        profile_page['isPartOf'] = {
            '@type': 'WebSite',
            '@id': canonical_url + '#website',
            'url': canonical_url,
            'name': personal.get('name', ''),
            'about': {'@id': person['@id']},
        }

    return json.dumps(profile_page, indent=2).replace('<', '\\u003c')


def build_social_preview(data):
    personal = data['personal']
    image = Image.new('RGB', (1200, 630), '#111e35')
    draw = ImageDraw.Draw(image)
    for x in range(0, 1200, 30):
        draw.line((x, 0, x, 630), fill='#192e49')
    for y in range(0, 630, 30):
        draw.line((0, y, 1200, y), fill='#192e49')
    draw.rectangle((24, 24, 1175, 605), fill='#172946', outline='#6daedf', width=3)
    draw.rectangle((24, 596, 506, 605), fill='#ef4444')
    draw.rectangle((507, 596, 1175, 605), fill='#9fd3f4')

    def line(text, xy, size, color):
        draw.text(xy, text, font=ImageFont.load_default(size=size), fill=color)

    def wrapped(text, y, size, color, width=720):
        font = ImageFont.load_default(size=size)
        row = ''
        for word in text.split():
            candidate = f'{row} {word}'.strip()
            if row and draw.textlength(candidate, font=font) > width:
                line(row, (65, y), size, color)
                y += size + 12
                row = word
            else:
                row = candidate
        line(row, (65, y), size, color)
        return y + size + 12

    line(personal['name'], (65, 120), 76, '#e9edf5')
    y = wrapped(personal['title'], 224, 34, '#9fd3f4')
    wrapped(personal['tagline'], y + 24, 28, '#e9edf5')
    wrapped(personal['supporting'].replace('•', '|'), 447, 22, '#a9b3c5')
    line(personal['remote'], (65, 530), 22, '#9fd3f4')
    with Image.open(SITE_DIR / personal['photoDark']) as portrait:
        portrait = portrait.convert('RGB').resize((270, 270), Image.Resampling.LANCZOS)
        image.paste(portrait, (845, 175))
    draw.rectangle((840, 170, 1119, 449), outline='#6daedf', width=4)
    line('WE.', (1050, 65), 38, '#e9edf5')
    image.save(SITE_DIR / 'preview.jpg', quality=90, subsampling=0)


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


def education_meta(edu):
    """School line. A missing year is omitted; an in-progress degree keeps that status.

    Do not invent a start or end year. B.S. and B.B.A. have neither a year nor
    an in-progress status in the source, so those cards show the school only.
    """
    school = edu.get('school', '')
    year = (edu.get('year') or '').strip()
    if year:
        return f'{school} ({year})'
    if 'In Progress' in (edu.get('degree') or ''):
        return f'{school} (In Progress)'
    return school


def render_education(education):
    parts = []
    for edu in education or []:
        parts.append(
            '<div class="edu-card card">'
            f'<div class="edu-icon"><i class="fas {esc(edu.get("icon", ""))}" aria-hidden="true"></i></div>'
            f'<div class="edu-info"><h3>{esc(edu.get("degree", ""))}</h3>'
            f'<p>{esc(education_meta(edu))}</p></div>'
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

    page_title = html.escape(site_name, quote=True)
    # Search snippets cut off around 160 characters, so the meta description
    # carries name, title, and the core keywords and stops there. OG/Twitter
    # use their own canonical supporting copy for social sharing.
    escaped_desc = esc(seo.get('description', ''))
    escaped_og_desc = esc(seo.get('socialDescription') or tagline)
    escaped_site_name = html.escape(site_name, quote=True)

    with open(SITE_DIR / 'scripts' / 'site_template.html', 'r') as f:
        html_content = f.read()

    image_url = canonical_url.rstrip('/') + '/preview.jpg'
    for attribute in ('property="og:image"', 'name="twitter:image"'):
        html_content = re.sub(
            rf'<meta {attribute} content=".*?">',
            lambda m: f'<meta {attribute} content="{esc(image_url)}">',
            html_content,
        )

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
    resumes = load_resume_variants()
    site = data.get('site') or {}
    current_role = next(iter(data.get('experience') or []), {})
    html_content = inject(html_content, 'HERO', render_hero(personal, resumes, current_role.get('company', '')))
    html_content = inject(html_content, 'ABOUT', render_about(data.get('about')))
    html_content = inject(html_content, 'WHAT_I_BUILD', render_what_i_build(site.get('whatIBuild')))
    html_content = inject(html_content, 'SKILLS', render_skills(data.get('skills')))
    experience = '<div class="timeline">' + render_experience(
        data.get('experience'), site.get('experienceSummaries')) + '</div>'
    if data.get('additionalExperience'):
        experience += (
            '<div class="earlier-experience"><h3>Earlier Experience</h3>'
            '<div class="additional-experience">'
            + render_additional_experience(data['additionalExperience']) + '</div></div>'
        )
    html_content = inject(html_content, 'EXPERIENCE', experience)
    html_content = inject(html_content, 'PROGRAMS', render_programs(
        data.get('selectedEngineeringPrograms'), site.get('selectedWork'), data.get('stats')))
    html_content = inject(html_content, 'AI_CAPABILITIES', render_ai_capabilities(data.get('aiEngineeringCapabilities')))
    html_content = inject(html_content, 'PROJECTS_INTRO', esc(site.get('projectsIntro', '')))
    html_content = inject(html_content, 'PROJECTS', render_projects(
        data.get('projects'), site.get('projectsProvenanceLabel', '')))
    html_content = inject(html_content, 'PORTFOLIO_NOTE', render_portfolio_note(personal, site.get('portfolioNote')))

    html_content = inject(html_content, 'EDUCATION', render_education(data.get('education')))
    html_content = inject(html_content, 'FOOTER', esc(data.get('footerText', '')))
    html_content = inject(html_content, 'NAV_RESUME', render_nav_resume(resumes))
    html_content = inject(html_content, 'MOBILE_NAV_RESUME', render_mobile_nav_resume(resumes))
    html_content = inject(html_content, 'RESUME_CHOICE', render_cta_resumes(resumes, site.get('resumeChoiceIntro', '')))
    html_content = inject(html_content, 'CTA_COPY', render_cta_copy(personal))
    html_content = inject(html_content, 'CTA_ACTIONS', render_cta_actions(personal))
    html_content = inject(html_content, 'JSONLD', '<script type="application/ld+json">' + render_json_ld(data) + '</script>')

    with open(SITE_DIR / 'index.html', 'w') as f:
        f.write(html_content)

    build_robots(canonical_url)
    build_sitemap(canonical_url)
    build_social_preview(data)


if __name__ == "__main__":
    build_html()
