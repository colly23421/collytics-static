import os
import glob

# Style dla breadcrumbs
breadcrumbs_style = """
<style>
/* BREADCRUMBS */
.breadcrumbs {
    background: rgba(255, 255, 255, 0.02);
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    padding: 20px 0;
    margin-bottom: 40px;
}

.breadcrumbs-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

.breadcrumbs-list {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.9rem;
}

.breadcrumbs-list a {
    color: #a1a1aa !important;
    text-decoration: none !important;
    transition: color 0.3s ease;
}

.breadcrumbs-list a:hover {
    color: #FFFFFF !important;
}

.breadcrumbs-separator {
    color: #4b5563;
    margin: 0 4px;
}

.breadcrumbs-current {
    color: #FFFFFF;
    font-weight: 500;
}

@media (max-width: 768px) {
    .breadcrumbs {
        padding: 15px 0;
    }
    
    .breadcrumbs-list {
        font-size: 0.85rem;
    }
}
</style>
"""

# HTML dla breadcrumbs (będzie dodany po <body>)
breadcrumbs_html = """
    <!-- Breadcrumbs -->
    <div class="breadcrumbs">
        <div class="breadcrumbs-container">
            <div class="breadcrumbs-list">
                <a href="../index.html">Strona główna</a>
                <span class="breadcrumbs-separator">→</span>
                <a href="index.html">Blog</a>
                <span class="breadcrumbs-separator">→</span>
                <span class="breadcrumbs-current">Artykuł</span>
            </div>
        </div>
    </div>
"""

# Zastosuj do wszystkich artykułów w blogu (pomijając index.html)
for filepath in glob.glob('blog/*.html'):
    filename = os.path.basename(filepath)
    
    # Pomiń index.html i pliki backup
    if filename == 'index.html' or 'backup' in filename:
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Sprawdź czy breadcrumbs już nie istnieją
    if 'breadcrumbs' not in content:
        # Dodaj style przed </head>
        if breadcrumbs_style not in content:
            content = content.replace('</head>', breadcrumbs_style + '\n</head>')
        
        # Znajdź koniec nawigacji i dodaj breadcrumbs
        # Szukamy końca menu overlay
        menu_end = content.find('<div class="menu-overlay" id="menuOverlay"></div>')
        if menu_end != -1:
            insert_pos = menu_end + len('<div class="menu-overlay" id="menuOverlay"></div>')
            content = content[:insert_pos] + '\n' + breadcrumbs_html + content[insert_pos:]
        else:
            # Alternatywnie po <body>
            body_tag = content.find('<body')
            body_end = content.find('>', body_tag) + 1
            content = content[:body_end] + '\n' + breadcrumbs_html + content[body_end:]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Dodano breadcrumbs do: {filename}")
    else:
        print(f"→ Breadcrumbs już istnieją w: {filename}")

print("\n✅ Breadcrumbs dodane do wszystkich artykułów!")
print("   Struktura: Strona główna → Blog → Artykuł")
