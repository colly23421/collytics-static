document.addEventListener("DOMContentLoaded", function() {
    const menuTrigger = document.getElementById("menuTrigger");
    const dropdownMenu = document.getElementById("dropdownMenu");
    const menuOverlay = document.getElementById("menuOverlay");
    const closeMenu = document.getElementById("closeMenu");
    const navbar = document.getElementById("navbar") || document.querySelector(".navbar");

    // Toggle menu
    function toggleMenu() {
        menuTrigger.classList.toggle("active");
        dropdownMenu.classList.toggle("active");
        menuOverlay.classList.toggle("active");
    }

    if(menuTrigger) menuTrigger.addEventListener("click", toggleMenu);
    if(closeMenu) closeMenu.addEventListener("click", toggleMenu);
    if(menuOverlay) menuOverlay.addEventListener("click", toggleMenu);

    // ESC key to close
    document.addEventListener("keydown", function(e) {
        if (e.key === "Escape" && dropdownMenu && dropdownMenu.classList.contains("active")) {
            toggleMenu();
        }
    });

    // ULEPSZONA WERSJA SCROLLOWANIA
    let lastScrollTop = 0;
    let scrollThreshold = 100;

    function handleScroll() {
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop;

        // Dodaj klasę 'scrolled' gdy strona jest przewinięta
        if (scrollTop > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        // Chowaj/pokazuj nawigację
        if (scrollTop > lastScrollTop && scrollTop > scrollThreshold) {
            // Scrollowanie w dół - schowaj
            navbar.classList.add('hidden');
        } else {
            // Scrollowanie w górę - pokaż
            navbar.classList.remove('hidden');
        }

        lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
    }

    // Nasłuchuj scrollowania z throttlingiem dla lepszej wydajności
    let isScrolling = false;
    window.addEventListener('scroll', function() {
        if (!isScrolling) {
            window.requestAnimationFrame(function() {
                handleScroll();
                isScrolling = false;
            });
            isScrolling = true;
        }
    });
});
