document.addEventListener('DOMContentLoaded', function () {
    // Mobile menu functionality
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const closeMenuButton = document.getElementById('close-menu');
    const mobileMenu = document.getElementById('mobile-menu');
    const mobileMenuLinks = mobileMenu.querySelectorAll('a');

    function toggleMenu() {
        const isExpanded =
            mobileMenuButton.getAttribute('aria-expanded') === 'true';
        mobileMenuButton.setAttribute('aria-expanded', !isExpanded);
        mobileMenu.classList.toggle('translate-x-full');

        // Update aria-hidden for the mobile menu
        mobileMenu.setAttribute('aria-hidden', isExpanded);
    }

    mobileMenuButton.addEventListener('click', toggleMenu);
    closeMenuButton.addEventListener('click', toggleMenu);

    // Close menu when clicking on a link
    mobileMenuLinks.forEach((link) => {
        link.addEventListener('click', () => {
            mobileMenu.classList.add('translate-x-full');
            mobileMenuButton.setAttribute('aria-expanded', 'false');
            mobileMenu.setAttribute('aria-hidden', 'true');
        });
    });

    // Carousel functionality
    const carousel = document.getElementById('carousel-items');
    const items = carousel.querySelectorAll('.carousel-item');
    const indicators = document.querySelectorAll('.carousel-indicator');
    const prevButton = document.getElementById('prev-button');
    const nextButton = document.getElementById('next-button');

    let currentIndex = 0;
    const totalItems = items.length;

    // Function to update the carousel
    function updateCarousel() {
        // Update carousel position
        carousel.style.transform = `translateX(-${currentIndex * 100}%)`;

        // Update indicators
        indicators.forEach((indicator, index) => {
            const isSelected = index === currentIndex;
            indicator.classList.toggle('active', isSelected);
            indicator.setAttribute('aria-selected', isSelected);
            indicator.setAttribute('tabindex', isSelected ? '0' : '-1');

            // Update the corresponding item's visibility
            items[index].setAttribute('aria-hidden', !isSelected);
        });
    }

    // Events for buttons
    prevButton.addEventListener('click', function () {
        currentIndex = (currentIndex - 1 + totalItems) % totalItems;
        updateCarousel();
    });

    nextButton.addEventListener('click', function () {
        currentIndex = (currentIndex + 1) % totalItems;
        updateCarousel();
    });

    // Events for indicators
    indicators.forEach((indicator, index) => {
        indicator.addEventListener('click', function () {
            currentIndex = index;
            updateCarousel();
        });
    });

    // Keyboard navigation for carousel
    document.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowLeft') {
            currentIndex = (currentIndex - 1 + totalItems) % totalItems;
            updateCarousel();
        } else if (e.key === 'ArrowRight') {
            currentIndex = (currentIndex + 1) % totalItems;
            updateCarousel();
        }
    });

    // Automatic change every 5 seconds
    let autoplayInterval = setInterval(function () {
        currentIndex = (currentIndex + 1) % totalItems;
        updateCarousel();
    }, 5000);

    // Pause autoplay on hover and focus
    carousel.addEventListener('mouseenter', () =>
        clearInterval(autoplayInterval)
    );
    carousel.addEventListener('mouseleave', () => {
        autoplayInterval = setInterval(function () {
            currentIndex = (currentIndex + 1) % totalItems;
            updateCarousel();
        }, 5000);
    });

    // Pause autoplay when carousel is focused
    carousel.addEventListener('focusin', () => clearInterval(autoplayInterval));
    carousel.addEventListener('focusout', () => {
        autoplayInterval = setInterval(function () {
            currentIndex = (currentIndex + 1) % totalItems;
            updateCarousel();
        }, 5000);
    });

    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px',
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe all sections with fade-in class
    document.querySelectorAll('.fade-in').forEach((section) => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(30px)';
        section.style.transition =
            'opacity 0.8s ease-out, transform 0.8s ease-out';
        observer.observe(section);
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#' && href !== '') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start',
                    });
                }
            }
        });
    });

    // Add active class to nav links on scroll
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('nav a[href^="#"]');

    function highlightNavigation() {
        const scrollY = window.pageYOffset;

        sections.forEach((section) => {
            const sectionHeight = section.offsetHeight;
            const sectionTop = section.offsetTop - 150;
            const sectionId = section.getAttribute('id');

            if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
                navLinks.forEach((link) => {
                    link.classList.remove('text-green-400');
                    if (link.getAttribute('href') === `#${sectionId}`) {
                        link.classList.add('text-green-400');
                    }
                });
            }
        });
    }

    window.addEventListener('scroll', highlightNavigation);

    // Lazy load images
    const images = document.querySelectorAll('img[loading="lazy"]');
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.classList.add('loaded');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach((img) => imageObserver.observe(img));
});
