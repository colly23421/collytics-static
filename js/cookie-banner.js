// Cookie Consent Banner - Collytics.io
// Wersja: 3.2 (Fix: Meta Pixel + CAPI Deduplication)
// Data: 2025-10-06 (Updated)

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

            const consent = this.getConsent();

            if (!consent) {
                console.log('[Cookie Banner] Brak zgody - wyświetlam banner');
                injectBannerHTML();
                this.showBanner();
            } else {
                console.log('[Cookie Banner] Znaleziono zgody:', consent);
                this.updateGTMConsent(consent);
            }
        },

        showBanner: function() {
            const banner = document.getElementById('cookieBanner');
            if (banner) {
                banner.classList.add('show');
            }
        },

        hideBanner: function() {
            const banner = document.getElementById('cookieBanner');
            if (banner) {
                banner.classList.remove('show');
            }
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
            this.updateGTMConsent(consent);
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
            this.updateGTMConsent(consent);
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
            this.updateGTMConsent(consent);
            this.hideBanner();
        },

        saveConsent: function(consent) {
            const consentData = {
                version: '3.0',
                data: consent,
                expiryDate: new Date(Date.now() + CONSENT_EXPIRY_DAYS * 24 * 60 * 60 * 1000).toISOString()
            };

            try {
                localStorage.setItem(COOKIE_NAME, JSON.stringify(consentData));
                console.log('[Cookie Banner] ✅ Zgody zapisane:', consent);
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

        // KLUCZOWA FUNKCJA: Aktualizacja GTM Consent Mode + Meta Pixel + CAPI
        updateGTMConsent: function(consent) {
            console.log('[Cookie Banner] Aktualizacja GTM Consent Mode...');

            // 1. Aktualizacja zgód w Google (gtag)
            if (typeof gtag === 'undefined') {
                console.warn('[Cookie Banner] ⚠️ gtag nie znaleziony - GTM może nie być załadowany');
            } else {
                gtag('consent', 'update', {
                    'analytics_storage': consent.analytics ? 'granted' : 'denied',
                    'ad_storage': consent.marketing ? 'granted' : 'denied',
                    'ad_user_data': consent.marketing ? 'granted' : 'denied',
                    'ad_personalization': consent.personalization ? 'granted' : 'denied'
                });
            }

            // 2. Obsługa Meta Pixel (Facebook) + CAPI - Uruchamiamy TYLKO przy zgodzie marketingowej
            if (consent.marketing) {
                // Generujemy wspólne ID dla PageView (deduplikacja)
                const pageViewID = crypto.randomUUID();

                if (typeof fbq === 'function') {
                    console.log('[Cookie Banner] ✅ Zgoda marketingowa: Uruchamiam Meta Pixel');
                    fbq('init', '815513483687028');
                    // Przekazujemy EventID do Pixela przeglądarkowego
                    fbq('track', 'PageView', {}, { eventID: pageViewID });
                } else {
                    console.warn('[Cookie Banner] Zgoda jest, ale fbq nie załadowane (sprawdź <head>)');
                }

                // Uruchamiamy CAPI (funkcja zdefiniowana w HTML)
                if (typeof sendToFBCAPI === 'function') {
                    sendToFBCAPI('PageView', {}, {}, pageViewID);
                }

            } else {
                console.log('[Cookie Banner] ℹ️ Brak zgody marketingowej - Meta Pixel/CAPI wstrzymane');
            }

            console.log('[Cookie Banner] ✅ Statusy zaktualizowane:', {
                analytics: consent.analytics ? 'granted' : 'denied',
                marketing: consent.marketing ? 'granted' : 'denied',
                personalization: consent.personalization ? 'granted' : 'denied'
            });

            // Wyślij event do DataLayer
            window.dataLayer = window.dataLayer || [];
            window.dataLayer.push({
                'event': 'cookie_consent_update',
                'cookie_consent': consent
            });
        }
    };

    // Eksportuj do window
    window.CookieBanner = CookieBanner;

    // ===== FUNKCJE TESTOWE - DOSTĘPNE W KONSOLI =====
    window.cookieTest = {
        status: function() {
            console.log('=== STATUS COOKIE BANNER ===');
            const consent = CookieBanner.getConsent();
            console.log('Zgody:', consent || 'Brak');
            console.log('gtag:', typeof gtag !== 'undefined' ? '✅ Istnieje' : '❌ Brak');
            console.log('DataLayer:', window.dataLayer ? '✅ Istnieje (' + window.dataLayer.length + ' wpisów)' : '❌ Brak');

            if (window.dataLayer) {
                const consentEvents = window.dataLayer.filter(item =>
                    item[0] === 'consent' || item.event === 'cookie_consent_update'
                );
                console.log('Consent events w dataLayer:', consentEvents.length);
                if (consentEvents.length > 0) {
                    console.log('Ostatni consent:', consentEvents[consentEvents.length - 1]);
                }
            }
            console.log('==========================');
        },

        reset: function() {
            localStorage.removeItem(COOKIE_NAME);
            console.log('✅ Zgody wyczyszczone. Przeładuj stronę.');
            setTimeout(() => location.reload(), 1000);
        },

        show: function() {
            if (!document.getElementById('cookieBanner')) {
                injectBannerHTML();
            }
            CookieBanner.showBanner();
        },

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
