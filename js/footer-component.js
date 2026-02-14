document.addEventListener("DOMContentLoaded", function() {
    const footerHTML = `
<footer class="main-footer">
    <div class="footer-container">
        <div class="footer-grid">
            <div class="footer-col">
                <img src="/assets/images/logo-collytics-white.png" alt="Collytics" class="footer-logo-small">
                <p class="footer-bio">Zaawansowana analityka i marketing oparty na danych. Skalujemy biznes poprzez precyzyjne tagowanie i strategie AI.</p>
            </div>
            <div class="footer-col">
                <p class="footer-label">Nawigacja</p>
                <ul class="footer-links">
                    <li><a href="/index.html">Home</a></li>
                    <li><a href="/services.html">Serwis</a></li>
                    <li><a href="/blog/index.html">Blog</a></li>
                    <li><a href="https://www.collytics.io/audyt-widocznosci-ai.html">AI w firmie</a></li>
                    <li><a href="/legal/privacy-policy.html">Polityka Prywatności</a></li>
                </ul>
            </div>
            <div class="footer-col">
                <p class="footer-label">Kontakt</p>
                <p><a href="mailto:hello@collytics.io" class="email-link">hello@collytics.io</a></p>
                <p><strong>Warszawa:</strong> Marszałkowska Centre, 126/134</p>
                <p><strong>Estonia, Tallinn:</strong> Karamelli tn 2, 11317</p>
            </div>
            <div class="footer-col">
                <p class="footer-label">Social Media</p>
                <div class="footer-socials">
                    <a href="https://www.facebook.com/collytics" target="_blank">
                        <img src="/assets/images/facebook-white.png" alt="Facebook">
                    </a>
                    <a href="https://x.com/collytics" target="_blank">
                        <img src="/assets/images/x-white.png" alt="X">
                    </a>
                    <a href="https://www.linkedin.com/company/collytics/" target="_blank">
                        <img src="/assets/images/linkedin-white.png" alt="LinkedIn">
                    </a>
                </div>
                <div class="footer-tax-info">
                    <span>VAT: EE102761425</span>
                    <span>Reg: 17036315</span>
                </div>
            </div>
        </div>
        <div class="footer-bottom-bar">
            <div class="footer-copyright">&copy; 2026 COLLYTICS OÜ.</div>
        </div>
    </div>
</footer>`;

    const oldFooter = document.querySelector('footer');
    if (oldFooter) {
        oldFooter.outerHTML = footerHTML;
    } else {
        document.body.insertAdjacentHTML('beforeend', footerHTML);
    }
});
