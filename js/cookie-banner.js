// Cookie Consent Banner - Collytics.io
// Wersja: 2.0 (ulepszona)
// Data: 2025-10-06
// Poprawki: Prawdziwe blokowanie skryptów przed zgodą

(function() {
    'use strict';

    const COOKIE_NAME = 'cookie_consent';
    const CONSENT_EXPIRY_DAYS = 365;

    // ===== KROK 1: ZABLOKUJ WSZYSTKIE SKRYPTY PRZED INICJALIZACJĄ =====
    // To musi być PRZED wszystkim innym!
    function blockScripts() {
        // Znajdź wszystkie skrypty z data-category
        const scripts = document.querySelectorAll('script[data-category]');
        scripts.forEach(script => {
            if (script.type !== 'text/plain') {
                // Zablokuj skrypt zmieniając jego typ
                script.type = 'text/plain';
                script.setAttribute('data-original-type', 'text/javascript');
            }
        });
    }

    // Wywołaj natychmiast
    blockScripts();

    // Wstrzyknij HTML bannera do strony
    function injectBannerHTML() {
        const bannerHTML = `
            <div class="cookie-banner" id="cookieBanner">
                <div class="banner-content">
                    <div class="banner-header">
                        <h2>Używamy plików cookie</h2>
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
            console.log('[Cookie Banner] Inicjalizacja...');
            injectBannerHTML();

            const consent = this.getConsent();

            if (!consent) {
                console.log('[Cookie Banner] Brak zgody - wyświetlam banner');
                this.showBanner();
            } else {
                console.log('[Cookie Banner] Znaleziono zgody:', consent);
                this.loadScripts(consent);
            }

            // Dodaj obserwator dla nowych skryptów (dynamicznie dodawanych)
            this.observeNewScripts();
        },

        // Obserwuj nowe skrypty dodawane do strony
        observeNewScripts: function() {
            const observer = new MutationObserver((mutations) => {
                mutations.forEach((mutation) => {
                    mutation.addedNodes.forEach((node) => {
                        if (node.tagName === 'SCRIPT' && node.hasAttribute('data-category')) {
                            const consent = this.getConsent();
                            const category = node.getAttribute('data-category');

                            if (!consent || !consent[category]) {
                                // Brak zgody - zablokuj
                                node.type = 'text/plain';
                                node.setAttribute('data-original-type', 'text/javascript');
                                console.log(`[Cookie Banner] ❌ Zablokowano dynamiczny skrypt: ${category}`);
                            }
                        }
                    });
                });
            });

            observer.observe(document.documentElement, {
                childList: true,
                subtree: true
            });
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
                version: '2.0',
                data: consent,
                expiryDate: new Date(Date.now() + CONSENT_EXPIRY_DAYS * 24 * 60 * 60 * 1000).toISOString()
            };

            try {
                localStorage.setItem(COOKIE_NAME, JSON.stringify(consentData));
                console.log('[Cookie Banner] ✅ Zgody zapisane:', consent);

                // Wyślij event dla Google Tag Manager (jeśli używasz)
                window.dataLayer = window.dataLayer || [];
                window.dataLayer.push({
                    'event': 'cookie_consent_update',
                    'cookie_consent': consent
                });
            } catch (e) {
                console.error('[Cookie Banner] Błąd zapisu:', e);
                window.cookieConsent = consentData;
            }
        },

        getConsent: function() {
            try {
                const saved = localStorage.getItem(COOKIE_NAME);
                if (!saved) return null;

                const consentData = JSON.parse(saved);

                // Sprawdź czy nie wygasło
                if (consentData.expiryDate) {
                    const expiry = new Date(consentData.expiryDate);
                    if (expiry < new Date()) {
                        localStorage.removeItem(COOKIE_NAME);
                        return null;
                    }
                }

                return consentData.data;
            } catch (e) {
                return window.cookieConsent ? window.cookieConsent.data : null;
            }
        },

        // ===== KLUCZOWA FUNKCJA: ŁADOWANIE SKRYPTÓW =====
        loadScripts: function(consent) {
            console.log('[Cookie Banner] Ładowanie skryptów zgodnie ze zgodami...');

            // Aktywuj zablokowane skrypty według kategorii
            const scriptsByCategory = {
                analytics: document.querySelectorAll('script[data-category="analytics"]'),
                marketing: document.querySelectorAll('script[data-category="marketing"]'),
                personalization: document.querySelectorAll('script[data-category="personalization"]')
            };

            // Aktywuj skrypty analytics
            if (consent.analytics) {
                console.log('[Cookie Banner] ✅ Aktywuję skrypty analityczne');
                this.activateScripts(scriptsByCategory.analytics);
                this.loadGoogleAnalytics();
            } else {
                console.log('[Cookie Banner] ❌ Skrypty analityczne zablokowane');
            }

            // Aktywuj skrypty marketing
            if (consent.marketing) {
                console.log('[Cookie Banner] ✅ Aktywuję skrypty marketingowe');
                this.activateScripts(scriptsByCategory.marketing);
                this.loadFacebookPixel();
            } else {
                console.log('[Cookie Banner] ❌ Skrypty marketingowe zablokowane');
            }

            // Aktywuj skrypty personalizacji
            if (consent.personalization) {
                console.log('[Cookie Banner] ✅ Aktywuję skrypty personalizacji');
                this.activateScripts(scriptsByCategory.personalization);
            } else {
                console.log('[Cookie Banner] ❌ Skrypty personalizacji zablokowane');
            }
        },

        // Aktywuj zablokowane skrypty
        activateScripts: function(scripts) {
            scripts.forEach(script => {
                if (script.type === 'text/plain') {
                    // Utwórz nowy element script
                    const newScript = document.createElement('script');

                    // Skopiuj wszystkie atrybuty
                    Array.from(script.attributes).forEach(attr => {
                        if (attr.name !== 'type' && attr.name !== 'data-original-type') {
                            newScript.setAttribute(attr.name, attr.value);
                        }
                    });

                    // Ustaw właściwy typ
                    newScript.type = 'text/javascript';

                    // Skopiuj zawartość (dla inline scripts)
                    if (script.innerHTML) {
                        newScript.innerHTML = script.innerHTML;
                    }

                    // Zastąp stary skrypt nowym
                    script.parentNode.replaceChild(newScript, script);

                    console.log('[Cookie Banner] 🚀 Załadowano skrypt:', script.src || 'inline');
                }
            });
        },

        // Google Analytics
        loadGoogleAnalytics: function() {
            if (typeof gtag !== 'undefined') {
                console.log('[Cookie Banner] Google Analytics już załadowany');
                return;
            }

            // ZAMIEŃ 'GA_MEASUREMENT_ID' na swoje ID!
            const GA_ID = 'G-XXXXXXXXXX'; // <--- TUTAJ WPISZ SWOJE ID

            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            window.gtag = gtag;
            gtag('js', new Date());
            gtag('config', GA_ID);

            const script = document.createElement('script');
            script.async = true;
            script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_ID}`;
            document.head.appendChild(script);

            console.log('[Cookie Banner] 📊 Google Analytics załadowany');
        },

        // Facebook Pixel
        loadFacebookPixel: function() {
            if (typeof fbq !== 'undefined') {
                console.log('[Cookie Banner] Facebook Pixel już załadowany');
                return;
            }

            // ZAMIEŃ 'YOUR_PIXEL_ID' na swoje ID!
            const PIXEL_ID = 'YOUR_PIXEL_ID'; // <--- TUTAJ WPISZ SWOJE ID

            !function(f,b,e,v,n,t,s)
            {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
            n.callMethod.apply(n,arguments):n.queue.push(arguments)};
            if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
            n.queue=[];t=b.createElement(e);t.async=!0;
            t.src=v;s=b.getElementsByTagName(e)[0];
            s.parentNode.insertBefore(t,s)}(window, document,'script',
            'https://connect.facebook.net/en_US/fbevents.js');

            fbq('init', PIXEL_ID);
            fbq('track', 'PageView');

            console.log('[Cookie Banner] 📘 Facebook Pixel załadowany');
        }
    };

    // Eksportuj do window
    window.CookieBanner = CookieBanner;

    // ===== FUNKCJE TESTOWE - DOSTĘPNE W KONSOLI =====
    window.cookieTest = {
        // Sprawdź status
        status: function() {
            console.log('=== STATUS COOKIE BANNER ===');
            const consent = CookieBanner.getConsent();
            console.log('Zgody:', consent || 'Brak');
            console.log('Google Analytics:', typeof gtag !== 'undefined' ? '✅ Załadowany' : '❌ Zablokowany');
            console.log('Facebook Pixel:', typeof fbq !== 'undefined' ? '✅ Załadowany' : '❌ Zablokowany');
            console.log('DataLayer:', typeof dataLayer !== 'undefined' ? '✅ Istnieje' : '❌ Brak');

            // Sprawdź zablokowane skrypty
            const blockedScripts = document.querySelectorAll('script[type="text/plain"][data-category]');
            console.log('Zablokowane skrypty:', blockedScripts.length);
            blockedScripts.forEach(s => {
                console.log('  -', s.getAttribute('data-category'), s.src || 'inline');
            });
            console.log('==========================');
        },

        // Reset
        reset: function() {
            localStorage.removeItem(COOKIE_NAME);
            console.log('✅ Zgody wyczyszczone. Przeładuj stronę.');
            setTimeout(() => location.reload(), 1000);
        },

        // Pokaż banner ponownie
        show: function() {
            CookieBanner.showBanner();
        },

        // Sprawdź localStorage
        check: function() {
            const data = localStorage.getItem(COOKIE_NAME);
            console.log('LocalStorage:', data ? JSON.parse(data) : 'Brak danych');
        }
    };

    // Inicjalizuj po załadowaniu DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            CookieBanner.init();
            console.log('[Cookie Banner] 💡 Testuj w konsoli: cookieTest.status()');
        });
    } else {
        CookieBanner.init();
        console.log('[Cookie Banner] 💡 Testuj w konsoli: cookieTest.status()');
    }

})();
