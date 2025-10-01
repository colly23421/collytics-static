// Cookie Consent Banner - Collytics.io
// Wersja: 1.0
// Data: 2025-10-01

(function() {
    'use strict';

    const COOKIE_NAME = 'cookie_consent';
    const CONSENT_EXPIRY_DAYS = 365;

    // Wstrzyknij HTML bannera do strony
    function injectBannerHTML() {
        const bannerHTML = `
            <div class="cookie-banner" id="cookieBanner">
                <div class="banner-content">
                    <div class="banner-header">
                        <h2>🍪 Używamy plików cookie</h2>
                    </div>

                    <div class="banner-text">
                        Używamy plików cookie i podobnych technologii, aby zapewnić prawidłowe działanie strony, analizować ruch oraz personalizować treści i reklamy. Możesz zaakceptować wszystkie cookie lub dostosować swoje preferencje.
                        <a href="/legal/privacy-policy.html">Polityka prywatności</a>
                    </div>

                    <div class="consent-options" id="consentOptions">
                        <div class="consent-category">
                            <div class="category-info">
                                <h3>Niezbędne</h3>
                                <p>Wymagane do podstawowego działania strony. Nie można ich wyłączyć.</p>
                            </div>
                            <label class="toggle-switch">
                                <input type="checkbox" checked disabled>
                                <span class="slider"></span>
                            </label>
                        </div>

                        <div class="consent-category">
                            <div class="category-info">
                                <h3>Analityczne</h3>
                                <p>Pomagają nam zrozumieć, jak odwiedzający korzystają ze strony.</p>
                            </div>
                            <label class="toggle-switch">
                                <input type="checkbox" id="analyticsToggle">
                                <span class="slider"></span>
                            </label>
                        </div>

                        <div class="consent-category">
                            <div class="category-info">
                                <h3>Marketingowe</h3>
                                <p>Służą do wyświetlania spersonalizowanych reklam.</p>
                            </div>
                            <label class="toggle-switch">
                                <input type="checkbox" id="marketingToggle">
                                <span class="slider"></span>
                            </label>
                        </div>

                        <div class="consent-category">
                            <div class="category-info">
                                <h3>Personalizacja</h3>
                                <p>Pozwalają dostosować treści do Twoich preferencji.</p>
                            </div>
                            <label class="toggle-switch">
                                <input type="checkbox" id="personalizationToggle">
                                <span class="slider"></span>
                            </label>
                        </div>
                    </div>

                    <div class="banner-buttons" id="mainButtons">
                        <button class="btn btn-primary" onclick="window.CookieBanner.acceptAll()">Akceptuj wszystkie</button>
                        <button class="btn btn-secondary" onclick="window.CookieBanner.rejectAll()">Odrzuć wszystkie</button>
                        <button class="btn btn-text" onclick="window.CookieBanner.toggleOptions()">Dostosuj</button>
                    </div>

                    <div class="banner-buttons" id="customButtons" style="display: none;">
                        <button class="btn btn-primary" onclick="window.CookieBanner.savePreferences()">Zapisz preferencje</button>
                        <button class="btn btn-text" onclick="window.CookieBanner.toggleOptions()">Anuluj</button>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', bannerHTML);
    }

    // Główna klasa Cookie Banner
    const CookieBanner = {
        init: function() {
            injectBannerHTML();
            const consent = this.getConsent();
            if (!consent) {
                this.showBanner();
            } else {
                this.loadScripts(consent);
            }
        },

        showBanner: function() {
            document.getElementById('cookieBanner').classList.add('show');
        },

        hideBanner: function() {
            document.getElementById('cookieBanner').classList.remove('show');
        },

        toggleOptions: function() {
            const options = document.getElementById('consentOptions');
            const mainButtons = document.getElementById('mainButtons');
            const customButtons = document.getElementById('customButtons');

            const isShowing = options.classList.toggle('show');

            if (isShowing) {
                mainButtons.style.display = 'none';
                customButtons.style.display = 'flex';
            } else {
                mainButtons.style.display = 'flex';
                customButtons.style.display = 'none';
            }
        },

        acceptAll: function() {
            const consent = {
                necessary: true,
                analytics: true,
                marketing: true,
                personalization: true,
                timestamp: new Date().toISOString()
            };
            this.saveConsent(consent);
            this.loadScripts(consent);
            this.hideBanner();
        },

        rejectAll: function() {
            const consent = {
                necessary: true,
                analytics: false,
                marketing: false,
                personalization: false,
                timestamp: new Date().toISOString()
            };
            this.saveConsent(consent);
            this.hideBanner();
        },

        savePreferences: function() {
            const consent = {
                necessary: true,
                analytics: document.getElementById('analyticsToggle').checked,
                marketing: document.getElementById('marketingToggle').checked,
                personalization: document.getElementById('personalizationToggle').checked,
                timestamp: new Date().toISOString()
            };
            this.saveConsent(consent);
            this.loadScripts(consent);
            this.hideBanner();
        },

        saveConsent: function(consent) {
            const consentData = {
                version: '1.0',
                data: consent
            };

            // Zapisz w zmiennej JavaScript (zamiast localStorage)
            window.cookieConsent = consentData;

            console.log('Zgody zapisane:', consent);
        },

        getConsent: function() {
            // Odczytaj ze zmiennej JavaScript
            return window.cookieConsent ? window.cookieConsent.data : null;
        },

        loadScripts: function(consent) {
            // TUTAJ DODAJ SWOJE SKRYPTY ANALITYCZNE/MARKETINGOWE

            if (consent.analytics) {
                console.log('✅ Ładowanie Google Analytics');
                // Przykład Google Analytics:
                // this.loadGoogleAnalytics();
            }

            if (consent.marketing) {
                console.log('✅ Ładowanie skryptów marketingowych');
                // Przykład Facebook Pixel:
                // this.loadFacebookPixel();
            }

            if (consent.personalization) {
                console.log('✅ Ładowanie skryptów personalizacji');
            }
        },

        // Przykład integracji Google Analytics
        loadGoogleAnalytics: function() {
            // window.dataLayer = window.dataLayer || [];
            // function gtag(){dataLayer.push(arguments);}
            // gtag('js', new Date());
            // gtag('config', 'GA_MEASUREMENT_ID');

            // const script = document.createElement('script');
            // script.async = true;
            // script.src = 'https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID';
            // document.head.appendChild(script);
        }
    };

    // Eksportuj do window, żeby przyciski mogły używać
    window.CookieBanner = CookieBanner;

    // Inicjalizuj po załadowaniu DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            CookieBanner.init();
        });
    } else {
        CookieBanner.init();
    }

    // Funkcja resetowania dla testów
    window.resetCookieConsent = function() {
        window.cookieConsent = null;
        location.reload();
    };

})();
