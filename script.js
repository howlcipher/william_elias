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

function syncProfilePhoto() {
    const photo = document.querySelector('.profile-photo');
    if (!photo) return;

    const isLight = document.documentElement.getAttribute('data-theme') === 'light' ||
        (document.documentElement.getAttribute('data-theme') === 'colorblind' &&
            !document.documentElement.classList.contains('dark-mode-colorblind'));
    const source = isLight ? photo.dataset.photoLight : photo.dataset.photoDark;

    if (source && photo.getAttribute('src') !== source) {
        photo.setAttribute('src', source);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Portfolio content (hero, summary, skills, experience, projects,
    // additional experience, education, footer) is pre-rendered into
    // index.html at build time by scripts/build_html.py from resume.json,
    // so crawlers and no-JS visitors see full content. This script only
    // handles interactivity and hydration from here on.
    initLastSynced();

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
    syncProfilePhoto();

    // Theme Toggle Handler (Light/Dark)
    if(themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            if (document.documentElement.getAttribute('data-theme') === 'colorblind' || 
                document.documentElement.classList.contains('dark-mode-colorblind')) {
                document.documentElement.classList.toggle('dark-mode-colorblind');
                const isDark = document.documentElement.classList.contains('dark-mode-colorblind');
                updateThemeIcon(isDark ? 'dark' : 'light');
                
                safeStorageSet('theme', isDark ? 'dark' : 'light');
                syncProfilePhoto();
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
            syncProfilePhoto();
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
            syncProfilePhoto();
        });
    }

    // 4. Scroll-aware navigation: highlight the nav link for the section currently in view.
    const sectionIds = ['about', 'skills', 'experience', 'programs', 'projects', 'education'];
    const navLinksById = new Map();
    document.querySelectorAll('.nav-links a[href^="#"], .mobile-nav-links a[href^="#"]').forEach(link => {
        const id = link.getAttribute('href').slice(1);
        if (!navLinksById.has(id)) navLinksById.set(id, []);
        navLinksById.get(id).push(link);
    });

    if (typeof IntersectionObserver !== 'undefined' && navLinksById.size) {
        let activeId = null;
        const setActiveSection = (id) => {
            if (id === activeId) return;
            activeId = id;
            navLinksById.forEach((links, linkId) => {
                links.forEach(link => {
                    if (linkId === id) {
                        link.classList.add('active');
                        link.setAttribute('aria-current', 'page');
                    } else {
                        link.classList.remove('active');
                        link.removeAttribute('aria-current');
                    }
                });
            });
        };

        const visibleSections = new Set();
        const sectionObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    visibleSections.add(entry.target.id);
                } else {
                    visibleSections.delete(entry.target.id);
                }
            });
            // sectionIds is already in document order, so the first match is the
            // topmost section currently inside the focus band.
            setActiveSection(sectionIds.find(id => visibleSections.has(id)) || null);
        }, {
            root: null,
            // Treat a thin horizontal band near the top of the viewport (below the
            // fixed navbar) as the "in view" zone, rather than the whole viewport.
            rootMargin: '-15% 0px -70% 0px',
            threshold: 0
        });

        sectionIds.forEach(id => {
            const el = document.getElementById(id);
            if (el) sectionObserver.observe(el);
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
