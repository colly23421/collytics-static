import os

# Dokładne nazwy z sitemap (bez .html na końcu w URL)
sitemap_articles = [
    'facebook-conversion-api-api-konwersji-bezpieczniejsze-i-bardziej-niezawodne-zrodlo-danych',
    'google-tag-manager-w-wordpress-jak-zainstalowac',
    'opcje-dopasowania-slow-kluczowych-w-google-ads'
]

# Template dla brakujących artykułów
template = """<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Collytics Blog</title>
    <link rel="stylesheet" href="../css/main.css">
    <style>
        body {{ background: #0a0a0a; color: #fff; font-family: Inter, sans-serif; }}
        .navbar {{ background: rgba(10, 10, 10, 0.95); padding: 20px; }}
        .content {{ max-width: 800px; margin: 100px auto; padding: 20px; }}
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <a href="../index.html" class="logo">
                <img src="../assets/images/logo main transparent.png" alt="Collytics">
            </a>
        </div>
    </nav>
    
    <div class="content">
        <h1>{title}</h1>
        <p>Artykuł w przygotowaniu...</p>
        <a href="index.html" style="color: #6366f1;">← Powrót do bloga</a>
    </div>
</body>
</html>"""

# Tytuły dla artykułów
titles = {
    'facebook-conversion-api-api-konwersji-bezpieczniejsze-i-bardziej-niezawodne-zrodlo-danych': 
        'Facebook Conversion API - Bezpieczniejsze źródło danych',
    'google-tag-manager-w-wordpress-jak-zainstalowac': 
        'Google Tag Manager w WordPress - Jak zainstalować',
    'opcje-dopasowania-slow-kluczowych-w-google-ads': 
        'Opcje dopasowania słów kluczowych w Google Ads'
}

# Utwórz brakujące pliki
for article in sitemap_articles:
    filepath = f'blog/{article}.html'
    
    if not os.path.exists(filepath):
        title = titles.get(article, article.replace('-', ' ').title())
        content = template.format(title=title)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Utworzono: {article}.html")
    else:
        print(f"→ Już istnieje: {article}.html")

# Sprawdź wszystkie pliki
print("\n" + "="*50)
print("Wszystkie pliki w blog/:")
for file in sorted(os.listdir('blog')):
    if file.endswith('.html') and 'backup' not in file:
        print(f"  ✓ {file}")
