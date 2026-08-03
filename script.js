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

document.addEventListener('DOMContentLoaded', () => {
    // --- Render Content from config.js ---
    if (typeof config !== 'undefined') {
        const heroTarget = document.getElementById('hero-content-target');
        if (heroTarget) {
            heroTarget.innerHTML = `
                <div class="hero-copy">
                    <p class="eyebrow">${config.personal.location} // AVAILABLE FOR REMOTE</p>
                    <h1>${config.personal.name}</h1>
                    <h2 class="subtitle">${config.personal.title}</h2>
                    <p class="tagline terminal-type">${config.personal.tagline}</p>
                    <div class="contact-info">
                        ${config.personal.email ? `<a href="mailto:${config.personal.email}" class="contact-pill"><i class="fas fa-envelope" aria-hidden="true"></i> Email</a>` : ''}
                        ${config.personal.linkedin ? `<a href="${config.personal.linkedin}" target="_blank" rel="noopener noreferrer" class="contact-pill"><i class="fab fa-linkedin" aria-hidden="true"></i> LinkedIn</a>` : ''}
                        ${config.personal.github ? `<a href="${config.personal.github}" target="_blank" rel="noopener noreferrer" class="contact-pill"><i class="fab fa-github" aria-hidden="true"></i> GitHub</a>` : ''}
                        ${config.personal.resumePdf ? `<a href="${config.personal.resumePdf}" target="_blank" rel="noopener noreferrer" class="contact-pill primary-action"><i class="fas fa-file-pdf" aria-hidden="true"></i> Resume PDF</a>` : ''}
                    </div>
                </div>
                ${config.personal.photo ? `<img class="profile-photo" src="${config.personal.photo}" alt="Professional headshot of ${config.personal.name}">` : ''}
            `;
        }

        const summaryTarget = document.getElementById('summary-target');
        if (summaryTarget) {
            summaryTarget.innerHTML = `<p>${config.summary}</p>`;
        }

        const skillsTarget = document.getElementById('skills-target');
        if (skillsTarget) {
            skillsTarget.innerHTML = config.skills.map(skill => `
                <div class="skill-category card">
                    <div class="skill-icon"><i class="fas ${skill.icon}"></i></div>
                    <h3>${skill.category}</h3>
                    <div class="skill-tags">
                        ${skill.tags.map(tag => `<span>${tag}</span>`).join('')}
                    </div>
                </div>
            `).join('');
        }

        const statsTarget = document.getElementById('stats-target');
        if (statsTarget && config.stats) {
            statsTarget.innerHTML = config.stats.map(stat => `
                <div class="stat-card">
                    <strong>${stat.value}</strong>
                    <span>${stat.label}</span>
                </div>
            `).join('');
        }

        const experienceTarget = document.getElementById('experience-target');
        if (experienceTarget) {
            experienceTarget.innerHTML = config.experience.map(job => `
                <div class="timeline-item card">
                    <div class="timeline-dot"></div>
                    <div class="timeline-date">${job.date}</div>
                    <div class="timeline-content">
                        <h3>${job.title}</h3>
                        <h4>${job.company}${job.location ? ` | ${job.location}` : ''}</h4>
                        <ul>
                            ${job.achievements.map(ach => `<li>${ach}</li>`).join('')}
                        </ul>
                    </div>
                </div>
            `).join('');
        }

        const projectsTarget = document.getElementById('projects-target');
        if (projectsTarget && config.projects) {
            projectsTarget.innerHTML = config.projects.map(proj => `
                <div class="project-card card">
                    <h3>${proj.name}</h3>
                    <div class="project-subtitle">${proj.subtitle}</div>
                    <ul>
                        ${proj.highlights.map(h => `<li>${h}</li>`).join('')}
                    </ul>
                    <div class="skill-tags">
                        ${proj.tags.map(tag => `<span>${tag}</span>`).join('')}
                    </div>
                </div>
            `).join('');
        }

        const additionalExperienceTarget = document.getElementById('additional-experience-target');
        if (additionalExperienceTarget && config.additionalExperience) {
            additionalExperienceTarget.innerHTML = config.additionalExperience.map(job => `
                <article class="additional-item">
                    <div><h3>${job.company}</h3><p>${job.title}</p></div>
                    <p class="additional-date">${job.date}</p>
                    <p class="additional-summary">${job.summary}</p>
                </article>
            `).join('');
        }

        const educationTarget = document.getElementById('education-target');
        if (educationTarget) {
            educationTarget.innerHTML = config.education.map(edu => `
                <div class="edu-card card">
                    <div class="edu-icon"><i class="fas ${edu.icon}"></i></div>
                    <div class="edu-info">
                        <h3>${edu.degree}</h3>
                        <p>${edu.school}${edu.year ? ` (${edu.year})` : ''}</p>
                    </div>
                </div>
            `).join('');
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
                const savedTheme = safeStorageGet('theme') || 'dark';
                if (savedTheme === 'light') {
                    document.documentElement.setAttribute('data-theme', 'light');
                } else {
                    document.documentElement.removeAttribute('data-theme');
                }
                document.documentElement.classList.remove('dark-mode-colorblind');
                safeStorageSet('colorblind', 'false');
                colorblindToggleBtn.classList.remove('active');
                colorblindToggleBtn.setAttribute('aria-pressed', 'false');
                updateThemeIcon(savedTheme);
            } else {
                enableColorblindMode();
            }
        });
    }

    function enableColorblindMode() {
        document.documentElement.setAttribute('data-theme', 'colorblind');
        
        const isDark = safeStorageGet('theme') !== 'light';
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
