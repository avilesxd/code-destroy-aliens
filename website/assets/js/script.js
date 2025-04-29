document.addEventListener('DOMContentLoaded', function () {
    // Mobile menu functionality
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const closeMenuButton = document.getElementById('close-menu');
    const mobileMenu = document.getElementById('mobile-menu');
    const mobileMenuLinks = mobileMenu.querySelectorAll('a');

    function toggleMenu() {
        const isExpanded = mobileMenuButton.getAttribute('aria-expanded') === 'true';
        mobileMenuButton.setAttribute('aria-expanded', !isExpanded);
        mobileMenu.classList.toggle('translate-x-full');

        // Update aria-hidden for the mobile menu
        mobileMenu.setAttribute('aria-hidden', isExpanded);
    }

    mobileMenuButton.addEventListener('click', toggleMenu);
    closeMenuButton.addEventListener('click', toggleMenu);

    // Close menu when clicking on a link
    mobileMenuLinks.forEach(link => {
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
    carousel.addEventListener('mouseenter', () => clearInterval(autoplayInterval));
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
});