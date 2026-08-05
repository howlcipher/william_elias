function safeStorageGet(key) {
    try {
        return localStorage.getItem(key);
    } catch (e) {
        return null;
    }
}

function safeStorageSet(key, value) {
    try {
        localStorage.setItem(key, value);
    } catch (e) {
        // ignore: storage unavailable/blocked/quota-exceeded
    }
}

function getValidUrl(url, allowRelative = false) {
    if (typeof url !== 'string' || !url) return null;
    if (allowRelative && !url.includes(':')) return url;
    return /^https?:\/\//i.test(url) ? url : null;
}

document.addEventListener('DOMContentLoaded', () => {
    // --- Render Content from config.js ---
    if (typeof config !== 'undefined') {
        const heroTarget = document.getElementById('hero-content-target');
        if (heroTarget) {
            heroTarget.textContent = '';
            const heroCopy = document.createElement('div');
            heroCopy.className = 'hero-copy';
            
            const eyebrow = document.createElement('p');
            eyebrow.className = 'eyebrow';
            eyebrow.textContent = `${config.personal.location || ''} // AVAILABLE FOR REMOTE`;
            
            const h1 = document.createElement('h1');
            h1.textContent = config.personal.name || '';
            
            const h2 = document.createElement('h2');
            h2.className = 'subtitle';
            h2.textContent = config.personal.title || '';
            
            const tagline = document.createElement('p');
            tagline.className = 'tagline terminal-type';
            tagline.textContent = config.personal.tagline || '';
            
            const contactInfo = document.createElement('div');
            contactInfo.className = 'contact-info';
            
            if (config.personal.email) {
                const emailL = document.createElement('a');
                emailL.href = `mailto:${config.personal.email}`;
                emailL.className = 'contact-pill';
                const icon = document.createElement('i');
                icon.className = 'fas fa-envelope';
                icon.setAttribute('aria-hidden', 'true');
                emailL.appendChild(icon);
                emailL.appendChild(document.createTextNode(' Email'));
                contactInfo.appendChild(emailL);
            }
            
            const linkedInUrl = getValidUrl(config.personal.linkedin);
            if (linkedInUrl) {
                const link = document.createElement('a');
                link.href = linkedInUrl;
                link.target = '_blank';
                link.rel = 'noopener noreferrer';
                link.className = 'contact-pill';
                const icon = document.createElement('i');
                icon.className = 'fab fa-linkedin';
                icon.setAttribute('aria-hidden', 'true');
                link.appendChild(icon);
                link.appendChild(document.createTextNode(' LinkedIn'));
                contactInfo.appendChild(link);
            }
            
            const githubUrl = getValidUrl(config.personal.github);
            if (githubUrl) {
                const link = document.createElement('a');
                link.href = githubUrl;
                link.target = '_blank';
                link.rel = 'noopener noreferrer';
                link.className = 'contact-pill';
                const icon = document.createElement('i');
                icon.className = 'fab fa-github';
                icon.setAttribute('aria-hidden', 'true');
                link.appendChild(icon);
                link.appendChild(document.createTextNode(' GitHub'));
                contactInfo.appendChild(link);
            }
            
            const resumeUrl = getValidUrl(config.personal.resumePdf, true);
            if (resumeUrl) {
                const link = document.createElement('a');
                link.href = resumeUrl;
                link.target = '_blank';
                link.rel = 'noopener noreferrer';
                link.className = 'contact-pill primary-action';
                const icon = document.createElement('i');
                icon.className = 'fas fa-file-pdf';
                icon.setAttribute('aria-hidden', 'true');
                link.appendChild(icon);
                link.appendChild(document.createTextNode(' Resume PDF'));
                contactInfo.appendChild(link);
            }
            
            heroCopy.appendChild(eyebrow);
            heroCopy.appendChild(h1);
            heroCopy.appendChild(h2);
            heroCopy.appendChild(tagline);
            heroCopy.appendChild(contactInfo);
            heroTarget.appendChild(heroCopy);
            
            const photoUrl = getValidUrl(config.personal.photo, true);
            if (photoUrl) {
                const img = document.createElement('img');
                img.className = 'profile-photo';
                img.src = photoUrl;
                img.alt = `Professional headshot of ${config.personal.name || ''}`;
                heroTarget.appendChild(img);
            }
        }

        const summaryTarget = document.getElementById('summary-target');
        if (summaryTarget) {
            summaryTarget.textContent = '';
            const p = document.createElement('p');
            p.textContent = config.summary;
            summaryTarget.appendChild(p);
        }

        const skillsTarget = document.getElementById('skills-target');
        if (skillsTarget && config.skills) {
            skillsTarget.textContent = '';
            config.skills.forEach(skill => {
                const categoryCard = document.createElement('div');
                categoryCard.className = 'skill-category card';
                
                const skillIcon = document.createElement('div');
                skillIcon.className = 'skill-icon';
                const icon = document.createElement('i');
                icon.className = `fas ${skill.icon || ''}`;
                skillIcon.appendChild(icon);
                
                const h3 = document.createElement('h3');
                h3.textContent = skill.category || '';
                
                const tagsDiv = document.createElement('div');
                tagsDiv.className = 'skill-tags';
                (skill.tags || []).forEach(tag => {
                    const span = document.createElement('span');
                    span.textContent = tag;
                    tagsDiv.appendChild(span);
                });
                
                categoryCard.appendChild(skillIcon);
                categoryCard.appendChild(h3);
                categoryCard.appendChild(tagsDiv);
                skillsTarget.appendChild(categoryCard);
            });
        }

        const statsTarget = document.getElementById('stats-target');
        if (statsTarget && config.stats) {
            statsTarget.textContent = '';
            config.stats.forEach(stat => {
                const card = document.createElement('div');
                card.className = 'stat-card';
                
                const strong = document.createElement('strong');
                strong.textContent = stat.value || '';
                
                const span = document.createElement('span');
                span.textContent = stat.label || '';
                
                card.appendChild(strong);
                card.appendChild(span);
                statsTarget.appendChild(card);
            });
        }

        const experienceTarget = document.getElementById('experience-target');
        if (experienceTarget && config.experience) {
            experienceTarget.textContent = '';
            config.experience.forEach(job => {
                const item = document.createElement('div');
                item.className = 'timeline-item card';
                
                const dot = document.createElement('div');
                dot.className = 'timeline-dot';
                
                const date = document.createElement('div');
                date.className = 'timeline-date';
                date.textContent = job.date || '';
                
                const content = document.createElement('div');
                content.className = 'timeline-content';
                
                const h3 = document.createElement('h3');
                h3.textContent = job.title || '';
                
                const h4 = document.createElement('h4');
                h4.textContent = job.company + (job.location ? ` | ${job.location}` : '');
                
                const ul = document.createElement('ul');
                (job.achievements || []).forEach(ach => {
                    const li = document.createElement('li');
                    li.textContent = ach;
                    ul.appendChild(li);
                });
                
                content.appendChild(h3);
                content.appendChild(h4);
                content.appendChild(ul);
                
                item.appendChild(dot);
                item.appendChild(date);
                item.appendChild(content);
                experienceTarget.appendChild(item);
            });
        }

        const projectsTarget = document.getElementById('projects-target');
        if (projectsTarget && config.projects) {
            projectsTarget.textContent = '';
            config.projects.forEach(proj => {
                const card = document.createElement('div');
                card.className = 'project-card card';
                
                const h3 = document.createElement('h3');
                h3.textContent = proj.name || '';
                
                const sub = document.createElement('div');
                sub.className = 'project-subtitle';
                sub.textContent = proj.subtitle || '';
                
                const ul = document.createElement('ul');
                (proj.highlights || []).forEach(h => {
                    const li = document.createElement('li');
                    li.textContent = h;
                    ul.appendChild(li);
                });
                
                const tagsDiv = document.createElement('div');
                tagsDiv.className = 'skill-tags';
                (proj.tags || []).forEach(tag => {
                    const span = document.createElement('span');
                    span.textContent = tag;
                    tagsDiv.appendChild(span);
                });
                
                card.appendChild(h3);
                card.appendChild(sub);
                card.appendChild(ul);
                card.appendChild(tagsDiv);

                const projLink = getValidUrl(proj.link);
                if (projLink) {
                    const linkWrapper = document.createElement('div');
                    linkWrapper.style.marginTop = '1rem';
                    const linkEl = document.createElement('a');
                    linkEl.href = projLink;
                    linkEl.target = '_blank';
                    linkEl.rel = 'noopener noreferrer';
                    linkEl.className = 'contact-pill project-link';
                    const icon = document.createElement('i');
                    icon.className = 'fas fa-external-link-alt';
                    icon.setAttribute('aria-hidden', 'true');
                    linkEl.appendChild(icon);
                    linkEl.appendChild(document.createTextNode(' View Project'));
                    linkWrapper.appendChild(linkEl);
                    card.appendChild(linkWrapper);
                }

                projectsTarget.appendChild(card);
            });
        }

        const additionalExperienceTarget = document.getElementById('additional-experience-target');
        if (additionalExperienceTarget && config.additionalExperience) {
            additionalExperienceTarget.textContent = '';
            config.additionalExperience.forEach(job => {
                const article = document.createElement('article');
                article.className = 'additional-item';
                
                const div = document.createElement('div');
                const h3 = document.createElement('h3');
                h3.textContent = job.company || '';
                const pTitle = document.createElement('p');
                pTitle.textContent = job.title || '';
                div.appendChild(h3);
                div.appendChild(pTitle);
                
                const pDate = document.createElement('p');
                pDate.className = 'additional-date';
                pDate.textContent = job.date || '';
                
                const pSum = document.createElement('p');
                pSum.className = 'additional-summary';
                pSum.textContent = job.summary || '';
                
                article.appendChild(div);
                article.appendChild(pDate);
                article.appendChild(pSum);
                additionalExperienceTarget.appendChild(article);
            });
        }

        const educationTarget = document.getElementById('education-target');
        if (educationTarget && config.education) {
            educationTarget.textContent = '';
            config.education.forEach(edu => {
                const card = document.createElement('div');
                card.className = 'edu-card card';
                
                const iconDiv = document.createElement('div');
                iconDiv.className = 'edu-icon';
                const i = document.createElement('i');
                i.className = `fas ${edu.icon || ''}`;
                iconDiv.appendChild(i);
                
                const infoDiv = document.createElement('div');
                infoDiv.className = 'edu-info';
                
                const h3 = document.createElement('h3');
                h3.textContent = edu.degree || '';
                
                const p = document.createElement('p');
                p.textContent = edu.school + (edu.year ? ` (${edu.year})` : '');
                
                infoDiv.appendChild(h3);
                infoDiv.appendChild(p);
                
                card.appendChild(iconDiv);
                card.appendChild(infoDiv);
                educationTarget.appendChild(card);
            });
        }

        const footerTarget = document.getElementById('footer-target');
        if (footerTarget) {
            footerTarget.innerText = config.footerText;
        }
        
        initLastSynced();
        
        document.title = `${config.personal.name} | ${config.personal.title}`;
    }

    // 1. Intersection Observer for fade-in animations on scroll
    if (typeof IntersectionObserver === 'undefined') {
        // No IntersectionObserver support: skip the animation and show content immediately.
        document.querySelectorAll('.fade-in').forEach(el => el.classList.add('visible'));
    } else {
        const observerOptions = {
            root: null,
            rootMargin: '0px',
            threshold: 0.1
        };

        const observer = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target); // Only animate once
                }
            });
        }, observerOptions);

        // Wait a brief moment before observing so dynamic content renders
        setTimeout(() => {
            document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
        }, 50);
    }
    
    // 2. Mobile Menu Toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const mobileNav = document.querySelector('.mobile-nav');
    const mobileNavLinks = document.querySelectorAll('.mobile-nav-links a');

    const closeMobileMenu = () => {
        mobileNav.classList.remove('active');
        mobileMenuBtn.querySelector('i').classList.replace('fa-times', 'fa-bars');
        mobileMenuBtn.setAttribute('aria-expanded', 'false');
        mobileNav.setAttribute('aria-hidden', 'true');
    };

    if (mobileMenuBtn && mobileNav) {
        mobileMenuBtn.addEventListener('click', () => {
            mobileNav.classList.toggle('active');
            const icon = mobileMenuBtn.querySelector('i');
            const isOpen = mobileNav.classList.contains('active');
            if (isOpen) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
            mobileMenuBtn.setAttribute('aria-expanded', String(isOpen));
            mobileNav.setAttribute('aria-hidden', String(!isOpen));
        });

        // Close menu when a link is clicked
        mobileNavLinks.forEach(link => {
            link.addEventListener('click', () => {
                closeMobileMenu();
            });
        });

        // Close menu on Escape and return focus to the toggle button
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && mobileNav.classList.contains('active')) {
                closeMobileMenu();
                mobileMenuBtn.focus();
            }
        });
    }

    // 3. Theme Management
    const themeToggleBtn = document.getElementById('theme-toggle');
    const colorblindToggleBtn = document.getElementById('colorblind-toggle');
    
    // Check saved preferences
    const currentTheme = safeStorageGet('theme');
    const isColorblind = safeStorageGet('colorblind') === 'true';
    
    // Initialize theme based on preference or OS setting
    if (currentTheme) {
        document.documentElement.setAttribute('data-theme', currentTheme);
        updateThemeIcon(currentTheme);
    } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
        document.documentElement.setAttribute('data-theme', 'light');
        updateThemeIcon('light');
    }
    
    if (isColorblind) {
        enableColorblindMode();
    }

    // Theme Toggle Handler (Light/Dark)
    if(themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            if (document.documentElement.getAttribute('data-theme') === 'colorblind' || 
                document.documentElement.classList.contains('dark-mode-colorblind')) {
                document.documentElement.classList.toggle('dark-mode-colorblind');
                const isDark = document.documentElement.classList.contains('dark-mode-colorblind');
                updateThemeIcon(isDark ? 'dark' : 'light');
                
                safeStorageSet('theme', isDark ? 'dark' : 'light');
                return;
            }

            let newTheme = 'light';
            if (document.documentElement.getAttribute('data-theme') === 'light') {
                newTheme = 'dark'; 
            }
            
            if (newTheme === 'dark') {
                document.documentElement.removeAttribute('data-theme');
                safeStorageSet('theme', 'dark');
            } else {
                document.documentElement.setAttribute('data-theme', 'light');
                safeStorageSet('theme', 'light');
            }
            updateThemeIcon(newTheme);
        });
    }

    // Colorblind Toggle Handler
    if(colorblindToggleBtn) {
        colorblindToggleBtn.addEventListener('click', () => {
            const currentlyColorblind = document.documentElement.getAttribute('data-theme') === 'colorblind';
            
            if (currentlyColorblind) {
                // Derive light/dark from the live DOM state set when colorblind mode was
                // entered, not localStorage: the 'theme' key is only written on an explicit
                // theme-toggle click, so it's absent for an OS-auto-detected preference.
                const wasDark = document.documentElement.classList.contains('dark-mode-colorblind');
                if (wasDark) {
                    document.documentElement.removeAttribute('data-theme');
                } else {
                    document.documentElement.setAttribute('data-theme', 'light');
                }
                document.documentElement.classList.remove('dark-mode-colorblind');
                safeStorageSet('colorblind', 'false');
                colorblindToggleBtn.classList.remove('active');
                colorblindToggleBtn.setAttribute('aria-pressed', 'false');
                updateThemeIcon(wasDark ? 'dark' : 'light');
            } else {
                enableColorblindMode();
            }
        });
    }

    function enableColorblindMode() {
        // Read the current theme before overwriting data-theme to 'colorblind', and from the
        // live attribute (not localStorage) so an OS-auto-detected preference that was never
        // explicitly saved is still respected.
        const isDark = document.documentElement.getAttribute('data-theme') !== 'light';
        document.documentElement.setAttribute('data-theme', 'colorblind');

        if (isDark) {
            document.documentElement.classList.add('dark-mode-colorblind');
        } else {
            document.documentElement.classList.remove('dark-mode-colorblind');
        }
        
        safeStorageSet('colorblind', 'true');
        if(colorblindToggleBtn) {
            colorblindToggleBtn.classList.add('active');
            colorblindToggleBtn.setAttribute('aria-pressed', 'true');
        }
        updateThemeIcon(isDark ? 'dark' : 'light');
    }

    function updateThemeIcon(theme) {
        if(!themeToggleBtn) return;
        const icon = themeToggleBtn.querySelector('i');
        if (theme === 'light') {
            icon.classList.replace('fa-sun', 'fa-moon');
        } else {
            icon.classList.replace('fa-moon', 'fa-sun');
        }
        themeToggleBtn.setAttribute('aria-pressed', String(theme === 'dark'));
    }
});

function formatRelativeTime(dateStr) {
    const diffMs = Date.now() - new Date(dateStr).getTime();
    const diffMin = Math.round(diffMs / 60000);
    const rtf = new Intl.RelativeTimeFormat('en', { numeric: 'auto' });
    if (Math.abs(diffMin) < 60) return rtf.format(-diffMin, 'minute');
    const diffHr = Math.round(diffMin / 60);
    if (Math.abs(diffHr) < 24) return rtf.format(-diffHr, 'hour');
    const diffDay = Math.round(diffHr / 24);
    return rtf.format(-diffDay, 'day');
}

function validateLastSyncedData(data) {
    if (!data || typeof data !== 'object') return null;
    const sha = data.sha;
    const date = data.commit && data.commit.author && data.commit.author.date;
    const url = data.html_url;
    if (typeof sha !== 'string' || sha.length === 0) return null;
    if (typeof date !== 'string' || isNaN(new Date(date).getTime())) return null;
    if (typeof url !== 'string' || !/^https:\/\/github\.com\//.test(url)) return null;
    return { sha, date, url };
}

function renderLastSynced(sha, date, url) {
    const target = document.getElementById('last-synced-target');
    if (!target) return;
    const shortSha = sha.slice(0, 7);

    target.textContent = '';

    const icon = document.createElement('i');
    icon.className = 'fas fa-code-commit';
    icon.setAttribute('aria-hidden', 'true');

    const link = document.createElement('a');
    link.textContent = `${formatRelativeTime(date)} (${shortSha})`;
    if (/^https:\/\//.test(url)) {
        link.href = url;
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
    }

    target.append(icon, document.createTextNode(' Last synced '), link);
}

function initLastSynced() {
    const sourceRepo = (typeof config !== 'undefined' && config.personal && config.personal.sourceRepo) || '';
    const branch = (typeof config !== 'undefined' && config.personal && config.personal.sourceBranch) || 'main';
    const ownerRepo = sourceRepo.replace('https://github.com/', '').replace(/\/$/, '');
    if (!/^[^/]+\/[^/]+$/.test(ownerRepo)) return;

    const CACHE_KEY = `we_last_synced:${ownerRepo}:${branch}`;
    const CACHE_TTL_MS = 10 * 60 * 1000;

    let cached = null;
    try {
        cached = JSON.parse(localStorage.getItem(CACHE_KEY));
    } catch (e) {
        cached = null;
    }

    if (cached && (Date.now() - cached.cachedAt) < CACHE_TTL_MS) {
        renderLastSynced(cached.sha, cached.date, cached.url);
        return;
    }

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000);

    fetch(`https://api.github.com/repos/${ownerRepo}/commits/${branch}`, {
        headers: { Accept: 'application/vnd.github+json' },
        signal: controller.signal
    })
        .then(res => {
            clearTimeout(timeoutId);
            if (!res.ok) throw new Error(`GitHub API returned ${res.status}`);
            return res.json();
        })
        .then(data => {
            const validated = validateLastSyncedData(data);
            if (!validated) throw new Error('Invalid last-synced API response shape');
            safeStorageSet(CACHE_KEY, JSON.stringify({ ...validated, cachedAt: Date.now() }));
            renderLastSynced(validated.sha, validated.date, validated.url);
        })
        .catch(() => {
            clearTimeout(timeoutId);
            if (cached) {
                renderLastSynced(cached.sha, cached.date, cached.url);
            }
        });
}
