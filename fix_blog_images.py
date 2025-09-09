import os
import glob

# Style dla obrazów
image_styles = """
<style>
/* Kontrola rozmiaru obrazów głównych */
.hero-image, .article-hero img, .featured-image {
    width: 100% !important;
    max-width: 100% !important;
    height: 400px !important;
    object-fit: cover !important;
    object-position: center !important;
}

/* Obrazy w treści artykułu */
.article-content img, article img, .content img {
    max-width: 100% !important;
    height: auto !important;
    display: block !important;
    margin: 30px auto !important;
}

/* Małe obrazy/ikony */
img[width="100"], img[width="200"], .small-image {
    width: auto !important;
    max-width: 200px !important;
    height: auto !important;
}

/* Hero section na blogu */
.blog-hero, .article-header {
    max-height: 500px !important;
    overflow: hidden !important;
}

/* Obrazy w kartach bloga */
.blog-card img, .blog-image {
    width: 100% !important;
    height: 200px !important;
    object-fit: cover !important;
}

/* Responsive */
@media (max-width: 768px) {
    .hero-image, .article-hero img {
        height: 250px !important;
    }
}
</style>
"""

# Zastosuj do wszystkich plików blogu
for filepath in glob.glob('blog/*.html'):
    if 'backup' not in filepath:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Sprawdź czy nie ma już tych stylów
        if 'object-fit: cover' not in content:
            # Dodaj przed </head>
            content = content.replace('</head>', image_styles + '\n</head>')
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✓ Naprawiono obrazy w: {os.path.basename(filepath)}")

# Napraw też główną stronę blogu
if os.path.exists('blog/index.html'):
    with open('blog/index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'object-fit: cover' not in content:
        content = content.replace('</head>', image_styles + '\n</head>')
        
        with open('blog/index.html', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✓ Naprawiono blog/index.html")

print("\n✅ Obrazy naprawione!")
print("- Hero images: 400px wysokości")
print("- Obrazy w treści: auto wysokość")
print("- Karty bloga: 200px wysokości")
