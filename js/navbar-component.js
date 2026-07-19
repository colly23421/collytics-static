document.addEventListener("DOMContentLoaded", function() {
  // Nie dubluj, jeśli strona ma już navbar w HTML
  if (!document.querySelector('.navbar')) {
    const navbarHTML = `
    <nav class="navbar">
      <div class="nav-container">
        <a href="/kontakt" class="nav-kontakt">Kontakt</a>
        <a href="/" class="logo">
          <img src="/assets/images/Transparent Logo.png" alt="Collytics"
               onerror="this.onerror=null;this.src='/assets/images/logo main transparent.png';">
        </a>
        <button class="menu-trigger" id="menuTrigger">Menu</button>
      </div>
    </nav>
    <div class="dropdown-menu" id="dropdownMenu">
      <button class="dropdown-close" id="closeMenu">Zamknij</button>
      <div class="dropdown-menu-inner">
        <div class="menu-section">
          <a href="/">Home</a>
          <a href="/services">Oferta</a>
          <a href="/blog">Blog</a>
          <a href="/audyt-widocznosci-ai">AI w firmie</a>
          <a href="/kontakt">Kontakt</a>
        </div>
        <div class="menu-divider"></div>
        <div class="social-links">
          <a href="https://www.facebook.com/collytics" target="_blank" rel="noopener noreferrer" title="Facebook"><img src="/assets/images/facebook-white.png" alt="Facebook"></a>
          <a href="https://www.linkedin.com/company/collytics/" target="_blank" rel="noopener noreferrer" title="LinkedIn"><img src="/assets/images/linkedin-white.png" alt="LinkedIn"></a>
          <a href="https://x.com/collytics" target="_blank" rel="noopener noreferrer" title="X"><img src="/assets/images/x-white.png" alt="X"></a>
        </div>
      </div>
    </div>`;
    document.body.insertAdjacentHTML('afterbegin', navbarHTML);
  }
  const t = document.getElementById('menuTrigger'), c = document.getElementById('closeMenu'), m = document.getElementById('dropdownMenu');
  t && t.addEventListener('click', () => m.classList.add('active'));
  c && c.addEventListener('click', () => m.classList.remove('active'));
  m && m.querySelectorAll('a').forEach(a => a.addEventListener('click', () => m.classList.remove('active')));
});
