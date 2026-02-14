document.addEventListener("DOMContentLoaded", function() {
    const navbarHTML = `
    <nav class="navbar">
        <div class="nav-container">
            <a href="/index.html" class="logo">
                <img src="/assets/images/logo main transparent.png" alt="Collytics">
            </a>
            <button class="menu-trigger" id="menuTrigger">Menu</button>
        </div>
    </nav>
    
    <div class="dropdown-menu" id="dropdownMenu">
        <button class="dropdown-close" id="closeMenu">Close</button>
        <div class="dropdown-menu-inner">
            <div class="menu-section">
                <a href="/index.html">Home</a>
                <a href="/services.html">Serwis</a>
                <a href="/blog/index.html">Blog</a>
                <a href="https://www.collytics.io/audyt-widocznosci-ai.html">AI w firmie</a>
                <a href="/kontakt.html">Kontakt</a>
            </div>
            <div class="menu-divider"></div>
            <div class="social-links">
                <a href="https://www.facebook.com/collytics" title="Facebook">
                    <img src="/assets/images/facebook-white.png" alt="Facebook">
                </a>
                <a href="https://www.linkedin.com/company/collytics/" title="LinkedIn">
                    <img src="/assets/images/linkedin-white.png" alt="LinkedIn">
                </a>
                <a href="https://x.com/collytics" title="X">
                    <img src="/assets/images/x-white.png" alt="X">
                </a>
            </div>
        </div>
    </div>
    
    <div class="menu-overlay" id="menuOverlay"></div>`;

    // Wstaw navbar na początku <body>
    document.body.insertAdjacentHTML('afterbegin', navbarHTML);
    
    // Inicjalizuj funkcjonalność menu
    const menuTrigger = document.getElementById('menuTrigger');
    const closeMenu = document.getElementById('closeMenu');
    const dropdownMenu = document.getElementById('dropdownMenu');
    const menuOverlay = document.getElementById('menuOverlay');
    
    if (menuTrigger) {
        menuTrigger.addEventListener('click', function() {
            dropdownMenu.classList.add('active');
            menuOverlay.classList.add('active');
        });
    }
    
    if (closeMenu) {
        closeMenu.addEventListener('click', function() {
            dropdownMenu.classList.remove('active');
            menuOverlay.classList.remove('active');
        });
    }
    
    if (menuOverlay) {
        menuOverlay.addEventListener('click', function() {
            dropdownMenu.classList.remove('active');
            menuOverlay.classList.remove('active');
        });
    }
});
