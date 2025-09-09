import os

filepath = 'blog/index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Znajdź i usuń konfliktujące style
# Usuń linię z "height: auto !important"
content = content.replace("""/* Zapobiegaj rozciąganiu */
img {
    max-width: 100% !important;
    height: auto !important;
}""", """/* Zapobiegaj rozciąganiu */
img {
    max-width: 100% !important;
}""")

# Dodaj bardziej specyficzne style z wyższym priorytetem
final_image_styles = """
<style>
/* FINALNA NAPRAWA OBRAZÓW - NAJWYŻSZY PRIORYTET */
.article-card .article-image {
    width: 100% !important;
    height: 200px !important;
    overflow: hidden !important;
}

.article-card .article-image img {
    width: 100% !important;
    height: 200px !important;
    min-height: 200px !important;
    max-height: 200px !important;
    object-fit: cover !important;
    object-position: center !important;
}

/* Usuń auto height dla obrazów w kartach */
.articles-grid img,
.article-card img {
    height: 200px !important;
    min-height: 200px !important;
    max-height: 200px !important;
}

/* Dla div z background-image */
.article-image[style*="background-image"] {
    height: 200px !important;
}

/* Override wszystkich innych stylów */
.container img {
    width: 100% !important;
    height: 200px !important;
    object-fit: cover !important;
}

/* Responsive */
@media (max-width: 768px) {
    .article-card .article-image,
    .article-card .article-image img,
    .articles-grid img {
        height: 180px !important;
        min-height: 180px !important;
        max-height: 180px !important;
    }
}
</style>
</head>"""

# Zamień </head> na nowe style
content = content.replace('</head>', final_image_styles)

# Zapisz
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Naprawiono obrazy - teraz powinny mieć dokładnie 200px wysokości")
