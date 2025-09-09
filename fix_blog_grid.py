import os

filepath = 'blog/index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Dodaj style dla grida 3 kolumn
grid_styles = """
<style>
/* GRID 3 KOLUMNY NA DESKTOP */
.articles-grid {
    display: grid !important;
    grid-template-columns: repeat(3, 1fr) !important;
    gap: 30px !important;
    max-width: 1200px !important;
    margin: 60px auto !important;
    padding: 0 20px !important;
}

.article-card {
    display: flex !important;
    flex-direction: column !important;
    background: #111111 !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    transition: transform 0.3s ease !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
}

.article-card:hover {
    transform: translateY(-5px) !important;
    border-color: rgba(255, 255, 255, 0.15) !important;
}

.article-card .article-image {
    width: 100% !important;
    height: 200px !important;
    overflow: hidden !important;
}

.article-card .article-image img {
    width: 100% !important;
    height: 200px !important;
    object-fit: cover !important;
}

.article-card .article-content {
    padding: 20px !important;
    flex: 1 !important;
    display: flex !important;
    flex-direction: column !important;
}

.article-category {
    background: rgba(99, 102, 241, 0.1) !important;
    border: 1px solid rgba(99, 102, 241, 0.3) !important;
    color: #fff !important;
    padding: 4px 12px !important;
    border-radius: 50px !important;
    font-size: 0.75rem !important;
    display: inline-block !important;
    margin-bottom: 12px !important;
}

.article-title {
    font-size: 1.1rem !important;
    color: #FFFFFF !important;
    margin-bottom: 10px !important;
    line-height: 1.3 !important;
}

.article-excerpt {
    font-size: 0.9rem !important;
    color: #a1a1aa !important;
    line-height: 1.5 !important;
    flex: 1 !important;
}

.article-meta {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    margin-top: 15px !important;
    padding-top: 15px !important;
    border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
}

.article-date {
    font-size: 0.8rem !important;
    color: #6b7280 !important;
}

.read-more {
    font-size: 0.85rem !important;
    color: #6366f1 !important;
}

/* Tablet - 2 kolumny */
@media (max-width: 992px) {
    .articles-grid {
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 25px !important;
    }
}

/* Mobile - 1 kolumna */
@media (max-width: 576px) {
    .articles-grid {
        grid-template-columns: 1fr !important;
        gap: 20px !important;
    }
    
    .article-title {
        font-size: 1.2rem !important;
    }
}

/* Usuń konflikty */
.container img {
    height: auto !important;
}

.articles-grid .article-image img {
    height: 200px !important;
}
</style>
</head>"""

# Zamień </head> na nowe style
content = content.replace('</head>', grid_styles)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Naprawiono grid - teraz 3 artykuły w rzędzie na desktopie")
print("✓ 2 artykuły w rzędzie na tablecie")
print("✓ 1 artykuł w rzędzie na mobile")
