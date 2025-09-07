// js/components.js
function loadHeader() {
    return `
    <nav>
        <div class="nav-container">
            <div class="logo">
                <a href="/">
                    <img src="/assets/images/logo-transparent.png" alt="Collytics" style="height: 56px;">
                </a>
            </div>
            <div class="nav-buttons">
                <a href="/blog/" class="btn btn-outline">Blog</a>
                <a href="/#kontakt" class="btn btn-outline">Kontakt</a>
            </div>
        </div>
    </nav>`;
}

function loadFooter() {
    return `
    <footer>
        <div class="footer-container">
            <img src="/assets/images/logo-transparent.png" alt="Collytics" style="height: 48px;">
            <p>© Collytics. All rights reserved.</p>
        </div>
    </footer>`;
}

// Automatyczne ładowanie
document.addEventListener('DOMContentLoaded', function() {
    // Wstaw header
    const headerEl = document.getElementById('header');
    if(headerEl) headerEl.innerHTML = loadHeader();
    
    // Wstaw footer
    const footerEl = document.getElementById('footer');
    if(footerEl) footerEl.innerHTML = loadFooter();
});
