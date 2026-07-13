document.addEventListener('DOMContentLoaded', () => {
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

    document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
    
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
    themeToggleBtn.addEventListener('click', () => {
        // If colorblind mode is active, we just toggle the dark/light variant of colorblind
        if (document.documentElement.getAttribute('data-theme') === 'colorblind' || 
            document.documentElement.classList.contains('dark-mode-colorblind')) {
            document.documentElement.classList.toggle('dark-mode-colorblind');
            const isDark = document.documentElement.classList.contains('dark-mode-colorblind');
            updateThemeIcon(isDark ? 'dark' : 'light');
            
            // Persist the underlying light/dark choice even in colorblind mode
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
            return;
        }

        let newTheme = 'light';
        if (document.documentElement.getAttribute('data-theme') === 'light') {
            newTheme = 'dark'; // Actually removes the attribute to fallback to root defaults
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

    // Colorblind Toggle Handler
    colorblindToggleBtn.addEventListener('click', () => {
        const currentlyColorblind = document.documentElement.getAttribute('data-theme') === 'colorblind';
        
        if (currentlyColorblind) {
            // Disable colorblind mode, restore previous theme
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
            // Enable colorblind mode
            enableColorblindMode();
        }
    });

    function enableColorblindMode() {
        document.documentElement.setAttribute('data-theme', 'colorblind');
        
        // Preserve dark mode preference within colorblind mode
        const isDark = localStorage.getItem('theme') !== 'light';
        if (isDark) {
            document.documentElement.classList.add('dark-mode-colorblind');
        } else {
            document.documentElement.classList.remove('dark-mode-colorblind');
        }
        
        localStorage.setItem('colorblind', 'true');
        colorblindToggleBtn.style.color = 'var(--primary)'; // highlight button
        updateThemeIcon(isDark ? 'dark' : 'light');
    }

    function updateThemeIcon(theme) {
        const icon = themeToggleBtn.querySelector('i');
        if (theme === 'light') {
            icon.classList.replace('fa-sun', 'fa-moon');
        } else {
            icon.classList.replace('fa-moon', 'fa-sun');
        }
    }
});
