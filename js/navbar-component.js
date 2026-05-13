document.addEventListener("DOMContentLoaded", function() {
    const navbarHTML = `
    <nav class="navbar">
        <div class="nav-container">
            <a href="/" class="logo">
                <img src="/assets/images/logo main transparent.png" alt="Collytics">
            </a>
            <button class="menu-trigger" id="menuTrigger">Menu</button>
        </div>
    </nav>
    
    <div class="dropdown-menu" id="dropdownMenu">
        <button class="dropdown-close" id="closeMenu">Close</button>
        <div class="dropdown-menu-inner">
            <div class="menu-section">
                <a href="/">Home</a>
                <a href="/services">Serwis</a>
                <a href="/blog">Blog</a>
                <a href="https://www.collytics.io/audyt-widocznosci-ai">AI w firmie</a>
                <a href="/kontakt">Kontakt</a>
            </div>
            <div class="menu-divider"></div>
            <div class="social-links">
                <a href="https://www.facebook.com/collytics" target="_blank" rel="noopener noreferrer" title="Facebook">
                    <img src="/assets/images/facebook-white.png" alt="Facebook">
                </a>
                <a href="https://www.linkedin.com/company/collytics/" target="_blank" rel="noopener noreferrer" title="LinkedIn">
                    <img src="/assets/images/linkedin-white.png" alt="LinkedIn">
                </a>
                <a href="https://x.com/collytics" target="_blank" rel="noopener noreferrer" title="X">
                    <img src="/assets/images/x-white.png" alt="X">
                </a>
            </div>
        </div>
    </div>
    
    <div class="menu-overlay" id="menuOverlay"></div>`;

    document.body.insertAdjacentHTML('afterbegin', navbarHTML);
    
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
