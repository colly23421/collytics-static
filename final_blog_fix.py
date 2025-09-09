import os
import glob

# Kompletny styl naprawczy
style_fix = """<style>
/* Reset i podstawowe */
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    background: #0a0a0a !important;
    color: #ffffff !important;
    font-family: 'Inter', -apple-system, sans-serif !important;
    line-height: 1.6 !important;
}

/* Nawigacja */
nav, .navbar, header {
    background: rgba(10, 10, 10, 0.95) !important;
    backdrop-filter: blur(20px) !important;
}

/* Menu dropdown - poprawka kolorów */
.dropdown-menu {
    background: rgba(17, 17, 17, 0.98) !important;
}

.dropdown-menu a, .menu-section a {
    color: #FFFFFF !important;
    opacity: 0.9;
}

.dropdown-menu a:hover {
    color: #FFFFFF !important;
    opacity: 1;
}

.dropdown-close {
    background: rgba(255, 255, 255, 0.1) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    color: #FFFFFF !important;
}

/* Przyciski - lepsza widoczność tekstu */
.menu-trigger, button, .btn, .cta-button {
    background: transparent !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    color: #FFFFFF !important;
    opacity: 0.9;
}

.menu-trigger:hover, button:hover {
    background: rgba(255, 255, 255, 0.05) !important;
    border-color: rgba(255, 255, 255, 0.4) !important;
    color: #FFFFFF !important;
    opacity: 1;
}

/* Nagłówki - zmniejszone rozmiary */
h1 {
    color: #FFFFFF !important;
    font-size: 2.5rem !important;
    line-height: 1.2 !important;
    margin-bottom: 20px !important;
}

h2 {
    color: #FFFFFF !important;
    font-size: 1.75rem !important;
    margin: 30px 0 15px !important;
}

h3 {
    color: #FFFFFF !important;
    font-size: 1.35rem !important;
    margin: 25px 0 12px !important;
}

/* Tekst */
p, li, td, span {
    color: #a1a1aa !important;
    font-size: 1rem !important;
    line-height: 1.7 !important;
}

/* Tagi/kategorie */
.tag, .category, .badge {
    background: rgba(99, 102, 241, 0.1) !important;
    border: 1px solid rgba(99, 102, 241, 0.3) !important;
    color: #FFFFFF !important;
    padding: 6px 16px !important;
    border-radius: 50px !important;
    font-size: 0.875rem !important;
}

/* Linki */
a {
    color: #6366f1 !important;
    text-decoration: none !important;
}

a:hover {
    color: #818cf8 !important;
}

/* Footer - spójny z resztą */
footer {
    background: #111111 !important;
    border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
    padding: 60px 5% 40px !important;
}

.footer-container {
    text-align: center !important;
}

footer h2 {
    color: #FFFFFF !important;
    font-size: 2rem !important;
    margin-bottom: 20px !important;
}

footer p {
    color: #a1a1aa !important;
}

footer .logo img {
    height: 60px !important;
    max-height: 60px !important;
}

.footer-bottom {
    padding-top: 40px !important;
    border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
    color: #a1a1aa !important;
    font-size: 0.875rem !important;
}

/* Content area */
.article-content, article, main, .content {
    max-width: 800px !important;
    margin: 0 auto !important;
    padding: 60px 20px !important;
}

/* Responsive */
@media (max-width: 768px) {
    h1 { font-size: 1.8rem !important; }
    h2 { font-size: 1.4rem !important; }
    h3 { font-size: 1.2rem !important; }
    p, li { font-size: 0.95rem !important; }
}
</style>
"""

# Napraw wszystkie pliki HTML w blogu
for filepath in glob.glob('blog/*.html'):
    if 'backup' not in filepath:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Usuń stare style jeśli są
        if '<style>' in content and 'background: #0a0a0a' in content:
            # Znajdź i usuń stary styl
            start = content.find('<style>')
            end = content.find('</style>') + 8
            if start != -1 and end > start:
                content = content[:start] + content[end:]
        
        # Dodaj nowe style po <head>
        if '<head>' in content:
            content = content.replace('<head>', '<head>\n' + style_fix)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Naprawiono: {os.path.basename(filepath)}")

print("\n✅ Wszystkie pliki naprawione!")
