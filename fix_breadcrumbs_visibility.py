import os
import glob

# Bardziej widoczne style dla breadcrumbs
visible_breadcrumbs = """
<style>
/* BREADCRUMBS - WIDOCZNE */
.breadcrumbs {
    background: #1a1a1a !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
    padding: 25px 0 !important;
    margin-top: 80px !important;
    margin-bottom: 40px !important;
    position: relative !important;
    z-index: 10 !important;
}

.breadcrumbs-container {
    max-width: 1200px !important;
    margin: 0 auto !important;
    padding: 0 20px !important;
}

.breadcrumbs-list {
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
    font-size: 0.95rem !important;
}

.breadcrumbs-list a {
    color: #6366f1 !important;
    text-decoration: none !important;
    transition: all 0.3s ease !important;
    border-bottom: 1px solid transparent !important;
}

.breadcrumbs-list a:hover {
    color: #818cf8 !important;
    border-bottom: 1px solid #818cf8 !important;
}

.breadcrumbs-separator {
    color: #6b7280 !important;
    font-size: 1.1rem !important;
}

.breadcrumbs-current {
    color: #FFFFFF !important;
    font-weight: 500 !important;
}
</style>
"""

for filepath in glob.glob('blog/*.html'):
    filename = os.path.basename(filepath)
    if filename == 'index.html' or 'backup' in filename:
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Usuń stare style breadcrumbs jeśli są
    if '/* BREADCRUMBS */' in content:
        start = content.find('/* BREADCRUMBS */')
        end = content.find('</style>', start) 
        if start != -1 and end != -1:
            # Znajdź początek tego bloku <style>
            style_start = content.rfind('<style>', 0, start)
            content = content[:style_start] + content[end + 8:]
    
    # Dodaj nowe widoczne style
    content = content.replace('</head>', visible_breadcrumbs + '\n</head>')
    
    # Jeśli breadcrumbs HTML nie istnieją, dodaj je
    if '<div class="breadcrumbs">' not in content:
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
        # Dodaj po nawigacji
        nav_end = content.find('</nav>')
        if nav_end != -1:
            insert_pos = content.find('\n', nav_end) + 1
            content = content[:insert_pos] + breadcrumbs_html + content[insert_pos:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Naprawiono widoczność breadcrumbs: {filename}")

print("\n✅ Breadcrumbs powinny być teraz widoczne!")
