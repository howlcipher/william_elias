document.addEventListener('DOMContentLoaded', () => {
    // --- Render Content from config.js ---
    if (typeof config !== 'undefined') {
        const heroTarget = document.getElementById('hero-content-target');
        if (heroTarget) {
            heroTarget.innerHTML = `
                <h1>${config.personal.name}</h1>
                <h2 class="subtitle">${config.personal.title}</h2>
                <p class="tagline">${config.personal.tagline}</p>
                <div class="contact-info">
                    ${config.personal.email ? `<a href="mailto:${config.personal.email}" class="contact-pill"><i class="fas fa-envelope"></i> ${config.personal.email}</a>` : ''}
                    ${config.personal.phone ? `<a href="tel:${config.personal.phone.replace(/[^0-9+]/g,'')}" class="contact-pill"><i class="fas fa-phone"></i> ${config.personal.phone}</a>` : ''}
                    ${config.personal.linkedin ? `<a href="${config.personal.linkedin}" target="_blank" class="contact-pill"><i class="fab fa-linkedin"></i> LinkedIn</a>` : ''}
                    ${config.personal.github ? `<a href="${config.personal.github}" target="_blank" class="contact-pill"><i class="fab fa-github"></i> GitHub</a>` : ''}
                    ${config.personal.resumePdf ? `<a href="${config.personal.resumePdf}" target="_blank" class="contact-pill"><i class="fas fa-file-pdf"></i> Download Resume</a>` : ''}
                </div>
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
                    <h4>${skill.category}</h4>
                    <div class="skill-tags">
                        ${skill.tags.map(tag => `<span>${tag}</span>`).join('')}
                    </div>
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
                        <h4>${job.title}</h4>
                        <h5>${job.company}${job.location ? ` | ${job.location}` : ''}</h5>
                        <ul>
                            ${job.achievements.map(ach => `<li>${ach}</li>`).join('')}
                        </ul>
                    </div>
                </div>
            `).join('');
        }

        const educationTarget = document.getElementById('education-target');
        if (educationTarget) {
            educationTarget.innerHTML = config.education.map(edu => `
                <div class="edu-card card">
                    <div class="edu-icon"><i class="fas ${edu.icon}"></i></div>
                    <div class="edu-info">
                        <h4>${edu.degree}</h4>
                        <p>${edu.school}${edu.year ? ` (${edu.year})` : ''}</p>
                    </div>
                </div>
            `).join('');
        }

        const philosophyTarget = document.getElementById('philosophy-target');
        if (philosophyTarget && config.philosophyAndHobbies) {
            philosophyTarget.innerHTML = `
                <div class="card">
                    <h4 style="margin-bottom: 0.5rem; font-size: 1.25rem;">Core Philosophy</h4>
                    <p>${config.philosophyAndHobbies.philosophy}</p>
                    <h4 style="margin-top: 1.5rem; margin-bottom: 0.5rem; font-size: 1.25rem;">Hobbies</h4>
                    <p>${config.philosophyAndHobbies.hobbies}</p>
                </div>
            `;
        }

        const footerTarget = document.getElementById('footer-target');
        if (footerTarget) {
            footerTarget.innerText = config.footerText;
        }
        
        document.title = `${config.personal.name} | ${config.personal.title}`;
    }

    // 1. Intersection Observer for fade-in animations on scroll
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
    
    // 2. Mobile Menu Toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const mobileNav = document.querySelector('.mobile-nav');
    const mobileNavLinks = document.querySelectorAll('.mobile-nav-links a');

    if (mobileMenuBtn && mobileNav) {
        mobileMenuBtn.addEventListener('click', () => {
            mobileNav.classList.toggle('active');
            const icon = mobileMenuBtn.querySelector('i');
            if (mobileNav.classList.contains('active')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });

        // Close menu when a link is clicked
        mobileNavLinks.forEach(link => {
            link.addEventListener('click', () => {
                mobileNav.classList.remove('active');
                mobileMenuBtn.querySelector('i').classList.replace('fa-times', 'fa-bars');
            });
        });
    }

    // 3. Theme Management
    const themeToggleBtn = document.getElementById('theme-toggle');
    const colorblindToggleBtn = document.getElementById('colorblind-toggle');
    
    // Check saved preferences
    const currentTheme = localStorage.getItem('theme');
    const isColorblind = localStorage.getItem('colorblind') === 'true';
    
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
                
                localStorage.setItem('theme', isDark ? 'dark' : 'light');
                return;
            }

            let newTheme = 'light';
            if (document.documentElement.getAttribute('data-theme') === 'light') {
                newTheme = 'dark'; 
            }
            
            if (newTheme === 'dark') {
                document.documentElement.removeAttribute('data-theme');
                localStorage.setItem('theme', 'dark');
            } else {
                document.documentElement.setAttribute('data-theme', 'light');
                localStorage.setItem('theme', 'light');
            }
            updateThemeIcon(newTheme);
        });
    }

    // Colorblind Toggle Handler
    if(colorblindToggleBtn) {
        colorblindToggleBtn.addEventListener('click', () => {
            const currentlyColorblind = document.documentElement.getAttribute('data-theme') === 'colorblind';
            
            if (currentlyColorblind) {
                const savedTheme = localStorage.getItem('theme') || 'dark';
                if (savedTheme === 'light') {
                    document.documentElement.setAttribute('data-theme', 'light');
                } else {
                    document.documentElement.removeAttribute('data-theme');
                }
                document.documentElement.classList.remove('dark-mode-colorblind');
                localStorage.setItem('colorblind', 'false');
                colorblindToggleBtn.style.color = '';
                updateThemeIcon(savedTheme);
            } else {
                enableColorblindMode();
            }
        });
    }

    function enableColorblindMode() {
        document.documentElement.setAttribute('data-theme', 'colorblind');
        
        const isDark = localStorage.getItem('theme') !== 'light';
        if (isDark) {
            document.documentElement.classList.add('dark-mode-colorblind');
        } else {
            document.documentElement.classList.remove('dark-mode-colorblind');
        }
        
        localStorage.setItem('colorblind', 'true');
        if(colorblindToggleBtn) colorblindToggleBtn.style.color = 'var(--primary)';
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
    }
});
