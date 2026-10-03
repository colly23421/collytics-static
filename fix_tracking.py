#!/usr/bin/env python3
"""
Collytics: naprawa Consent Mode / GA4 / GTM we wszystkich plikach HTML.
Uruchom z katalogu glownego repo:  python3 fix_tracking.py
Flaga --dry-run pokazuje tylko, co by sie zmienilo.
"""
import re, sys, pathlib

DRY = "--dry-run" in sys.argv
ROOT = pathlib.Path(".")
GTM_ID = "GTM-TZCR8FPZ"
SKIP_DIRS = {"node_modules", ".git"}
SKIP_FILES = {"blog-nav.html"}  # fragment, nie pelna strona

NEW_HEAD = f"""
  <!-- Consent Mode v2 + GTM (collytics fix) -->
  <script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('consent', 'default', {{
    analytics_storage: 'denied', ad_storage: 'denied',
    ad_user_data: 'denied', ad_personalization: 'denied',
    wait_for_update: 500
  }});
  try {{
    var s = JSON.parse(localStorage.getItem('cookie_consent'));
    var c = s && s.data && (!s.expiryDate || new Date(s.expiryDate) > new Date()) ? s.data : null;
    if (c) gtag('consent', 'update', {{
      analytics_storage: c.analytics ? 'granted' : 'denied',
      ad_storage: c.marketing ? 'granted' : 'denied',
      ad_user_data: c.marketing ? 'granted' : 'denied',
      ad_personalization: c.personalization ? 'granted' : 'denied'
    }});
  }} catch(e) {{}}
  </script>
  <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
  new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  }})(window,document,'script','dataLayer','{GTM_ID}');</script>
  <script src="/js/cookie-banner.js?v=4" defer></script>
  <!-- /Consent Mode v2 + GTM -->
"""

NOSCRIPT = (f'<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}" '
            'height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>')

SCRIPT_RE = re.compile(r"<script\b([^>]*)>(.*?)</script>\s*", re.S | re.I)
COMMENT_RE = re.compile(
    r"<!--\s*(Google Analytics[^>]*|Google Tag Manager[^>]*|End Google Tag Manager[^>]*|"
    r"GTM Consent Mode[^>]*|UWAGA: na stronie byly zaladowane DWA kontenery GTM.*?|"
    r"Consent Mode v2 \+ GTM.*?|/Consent Mode v2 \+ GTM)-->\s*", re.S | re.I)
NOSCRIPT_RE = re.compile(r"<noscript>\s*<iframe[^>]*googletagmanager\.com/ns\.html[^>]*>\s*</iframe>\s*</noscript>\s*", re.I)


def is_tracking_script(attrs, body):
    a, b = attrs.lower(), body
    if "cookie-banner.js" in a:
        return True
    if "googletagmanager.com/gtag/js" in a:
        return True
    if "gtm.js" in b and "googletagmanager" in b:
        return True
    if re.search(r"""gtag\(\s*['"]consent['"]\s*,\s*['"]default""", b):
        return True
    # inline: gtag('js') + gtag('config') bez innej logiki
    stripped = re.sub(r"window\.dataLayer\s*=\s*window\.dataLayer\s*\|\|\s*\[\];?|"
                      r"function gtag\(\)\{dataLayer\.push\(arguments\);\}|"
                      r"""gtag\(\s*['"]js['"]\s*,\s*new Date\(\)\);?|"""
                      r"""gtag\(\s*['"]config['"]\s*,\s*['"]G-[A-Z0-9]+['"]\s*\);?""", "", b)
    if "gtag(" in b and "config" in b and not stripped.strip():
        return True
    return False


def fix_html(path):
    src = path.read_text(encoding="utf-8")
    m = re.search(r"<head\b[^>]*>", src, re.I)
    if not m:
        return None
    head_end = src.lower().find("</head>")
    head = src[m.end():head_end]
    if "collytics fix" in src:
        return False  # juz naprawione
    if "googletagmanager" not in src and "cookie-banner.js" not in src:
        return None  # strona bez trackingu (np. polityka prywatnosci) - nie ruszamy

    head = SCRIPT_RE.sub(lambda s: "" if is_tracking_script(s.group(1), s.group(2)) else s.group(0), head)
    head = COMMENT_RE.sub("", head)
    rest = src[head_end:]
    # drugie ladowanie bannera w <body>
    rest = SCRIPT_RE.sub(lambda s: "" if "cookie-banner.js" in s.group(1).lower() else s.group(0), rest)
    # noscript GTM: zostaw dokladnie jeden, z wlasciwym ID, zaraz po <body>
    rest = NOSCRIPT_RE.sub("", rest)
    rest = re.sub(r"(<body\b[^>]*>)", r"\1\n  " + NOSCRIPT.replace("\\", "\\\\"), rest, count=1, flags=re.I)

    out = src[:m.end()] + NEW_HEAD + head.lstrip("\n") + rest
    if out == src:
        return False
    if not DRY:
        path.write_text(out, encoding="utf-8")
    return True


def fix_banner():
    p = ROOT / "js" / "cookie-banner.js"
    if not p.exists():
        print("!! brak js/cookie-banner.js"); return
    s = p.read_text(encoding="utf-8")
    o = s
    # 1) przy powrocie uzytkownika: consent update robi juz inline skrypt w <head>,
    #    banner wysyla tylko event do dataLayer
    s = s.replace(
        "console.log('[Cookie Banner] Znaleziono zgody:', consent);\n                this.updateGTMConsent(consent);",
        "console.log('[Cookie Banner] Znaleziono zgody:', consent);\n"
        "                window.dataLayer = window.dataLayer || [];\n"
        "                window.dataLayer.push({ 'event': 'cookie_consent_update', 'cookie_consent': consent });")
    # 2) ochrona przed podwojna inicjalizacja
    if "if (window.CookieBanner) return;" not in s:
      s = s.replace("(function() {\n    'use strict';",
                    "(function() {\n    'use strict';\n    if (window.CookieBanner) return;", 1)
    # 3) poprawny link do polityki prywatnosci
    s = s.replace('href="/polityka-prywatnosci.html"', 'href="/legal/privacy-policy"')
    # 4) mozliwosc ponownego otwarcia bannera: window.CookieBanner.open()
    if "CookieBanner.open" not in s:
      s = s.replace("    window.CookieBanner = CookieBanner;",
                  "    CookieBanner.open = function() {\n"
                  "        if (!document.getElementById('cookieBanner')) injectBannerHTML();\n"
                  "        CookieBanner.showBanner();\n    };\n"
                  "    window.CookieBanner = CookieBanner;", 1)
    if s != o:
        if not DRY:
            p.write_text(s, encoding="utf-8")
        print("zmieniono: js/cookie-banner.js")
    else:
        print("bez zmian: js/cookie-banner.js (sprawdz recznie)")


changed = 0
for f in sorted(ROOT.rglob("*.html")):
    if set(f.parts) & SKIP_DIRS or f.name in SKIP_FILES:
        continue
    r = fix_html(f)
    if r:
        changed += 1
        print("zmieniono:", f)
fix_banner()
print(f"\nGotowe. Plikow HTML zmienionych: {changed}" + ("  (DRY RUN - nic nie zapisano)" if DRY else ""))
