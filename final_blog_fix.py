import os
from bs4 import BeautifulSoup

print("--- Rozpoczynam OSTATECZNĄ naprawę wszystkich artykułów bloga ---")

BLOG_DIR = 'blog'
if not os.path.isdir(BLOG_DIR):
    print(f"BŁĄD KRYTYCZNY: Nie znaleziono folderu '{BLOG_DIR}'. Upewnij się, że skrypt jest w głównym folderze projektu.")
    exit()

# --- Idealny szablon HTML dla każdego artykułu ---
# Zawiera poprawne ścieżki (../), kompletną nawigację i działający skrypt.
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{TITLE}</title>
    <meta name="description" content="{DESCRIPTION}">

    <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','GT-5R3VKTJG');</script>

    <link rel="shortcut icon" type="image/png" href="../assets/images/Wordpress Transparent.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

    <link rel="stylesheet" href="../css/global.css">
    <link rel="stylesheet" href="../css/blog.css">
</head>
<body>
    <nav class="navbar" id="navbar">
        <div class="nav-container">
            <a class="logo" href="/index.html"><img alt="Collytics" src="../assets/images/logo main transparent.png"/></a>
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
                <a href="/about.html">O nas</a>
                <a href="/kontakt.html">Kontakt</a>
            </div>
            <div class="social-links">
                <a href="https://www.facebook.com/collytics" target="_blank" title="Facebook"><img alt="Facebook" src="../assets/images/facebook.png"/></a>
                <a href="https://www.linkedin.com/company/collytics/" target="_blank" title="LinkedIn"><img alt="LinkedIn" src="../assets/images/cons8-linkedin-500.svg"/></a>
                <a href="https://x.com/collytics" target="_blank" title="Twitter"><img alt="X" src="../assets/images/cons8-twitter-500.svg"/></a>
            </div>
        </div>
    </div>
    <div class="menu-overlay" id="menuOverlay"></div>

    <main class="blog-container article-content">
        {ARTICLE_CONTENT}
    </main>

    <footer>
        <div class="footer-container">
             <div class="footer-bottom">
                <p>© Collytics. All rights reserved. <a href="/legal/privacy-policy.html">Polityka Prywatności</a></p>
            </div>
        </div>
    </footer>

    <script>
        document.addEventListener("click", function(e) {{
            if(e.target.id === "menuTrigger") {{
                document.getElementById("dropdownMenu").classList.add("active");
                document.getElementById("menuOverlay").classList.add("active");
            }}
            if(e.target.id === "closeMenu" || e.target.id === "menuOverlay") {{
                document.getElementById("dropdownMenu").classList.remove("active");
                document.getElementById("menuOverlay").classList.remove("active");
            }}
        }});
    </script>
</body>
</html>
"""

# --- Przetwarzanie plików ---
for filename in os.listdir(BLOG_DIR):
    if filename.endswith('.html') and filename != 'index.html':
        filepath = os.path.join(BLOG_DIR, filename)
        print(f"-> Przebudowuję: {filepath}")

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')

            # 1. Wyciągnij kluczowe dane ze starego pliku
            title = soup.title.string if soup.title else "Bez tytułu"
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            description = meta_desc['content'] if meta_desc else "Brak opisu."

            # 2. Wyciągnij treść artykułu (szukamy po kilku możliwych kontenerach)
            article_body = soup.find('div', class_='post-body') or \
                           soup.find('div', class_='rich-text-block') or \
                           soup.find('main') or \
                           soup.find('article')

            # Jeśli nie znajdziemy specyficznego kontenera, bierzemy wszystko co sensowne z body
            if not article_body:
                article_body = soup.body
                # Usuwamy ze środka starą nawigację i stopkę, żeby się nie powieliły
                if article_body.nav: article_body.nav.decompose()
                if article_body.footer: article_body.footer.decompose()

            article_html = str(article_body) if article_body else "<p>Nie udało się odnaleźć treści artykułu.</p>"

            # 3. Wypełnij szablon wyciągniętymi danymi
            new_html_content = HTML_TEMPLATE.format(
                TITLE=title,
                DESCRIPTION=description.replace('"',"'"), # Prosta ochrona przed błędami
                ARTICLE_CONTENT=article_html
            )

            # 4. Zapisz całkowicie nowy, naprawiony plik
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_html_content)

            print(f"  OK: Plik został w pełni przebudowany.")

        except Exception as e:
            print(f"  BŁĄD: Nie udało się przetworzyć pliku. Powód: {e}")

print("\n--- Zakończono! Wszystkie artykuły zostały naprawione. ---")
