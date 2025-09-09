import os

# Specyficzne style dla strony głównej blogu
blog_index_styles = """
<style>
/* Naprawka dla strony głównej blogu */
.blog-grid .blog-image,
.blog-card .blog-image,
.blog-grid img,
.blog-card img {
    width: 100% !important;
    height: 200px !important;
    max-height: 200px !important;
    object-fit: cover !important;
    object-position: center !important;
}

/* Jeśli obrazy są jako background-image */
.blog-image[style*="background-image"] {
    height: 200px !important;
    max-height: 200px !important;
    background-size: cover !important;
    background-position: center !important;
}

/* Hero/Featured post */
.featured-post img,
.hero-post img {
    width: 100% !important;
    height: 300px !important;
    max-height: 300px !important;
    object-fit: cover !important;
}

/* Małe karty */
.small-card img {
    height: 150px !important;
    max-height: 150px !important;
}

/* Zapobiegaj rozciąganiu */
img {
    max-width: 100% !important;
    height: auto !important;
}

/* Override dla konkretnych obrazów */
.blog-section img,
article img {
    display: block !important;
    width: 100% !important;
    height: 200px !important;
    object-fit: cover !important;
}

/* Mobile */
@media (max-width: 768px) {
    .blog-image,
    .blog-card img {
        height: 180px !important;
    }
}
</style>
"""

# Zastosuj do blog/index.html
filepath = 'blog/index.html'
if os.path.exists(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Usuń stare style jeśli są
    if 'height: 200px !important' in content:
        print("Style już istnieją, aktualizuję...")
        # Znajdź i usuń stary blok
        start = content.find('<style>')
        while start != -1:
            end = content.find('</style>', start) + 8
            if 'blog-image' in content[start:end]:
                content = content[:start] + content[end:]
                break
            start = content.find('<style>', start + 1)
    
    # Dodaj nowe style
    content = content.replace('</head>', blog_index_styles + '\n</head>')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ Naprawiono blog/index.html")

# Zastosuj też do głównego index.html jeśli ma sekcję bloga
filepath = 'index.html'
if os.path.exists(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'blog-section' in content or 'blog-grid' in content:
        if 'blog-image' not in content or 'height: 200px' not in content:
            content = content.replace('</head>', blog_index_styles + '\n</head>')
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✓ Naprawiono index.html (sekcja bloga)")

print("\n✅ Gotowe! Obrazy na stronie bloga powinny mieć teraz 200px wysokości")
