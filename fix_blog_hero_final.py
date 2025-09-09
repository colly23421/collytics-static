import os

filepath = 'blog/index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Dodaj kompletne style dla hero sekcji
hero_fix = """
<style>
/* NAPRAWA HERO SEKCJI BLOGA */
.blog-hero {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%) !important;
    padding: 160px 40px 80px !important;
    text-align: center !important;
    position: relative !important;
    min-height: 450px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin-bottom: 60px !important;
}

.blog-hero::before {
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    background: radial-gradient(circle at 50% 50%, rgba(99, 102, 241, 0.08) 0%, transparent 70%) !important;
    pointer-events: none !important;
}

.blog-hero-content {
    max-width: 800px !important;
    margin: 0 auto !important;
    position: relative !important;
    z-index: 1 !important;
}

.blog-hero .menu-label {
    display: none !important;
}

.blog-hero h1 {
    font-size: 3.5rem !important;
    color: #FFFFFF !important;
    margin-bottom: 24px !important;
    font-weight: 700 !important;
    line-height: 1.1 !important;
}

.blog-hero p {
    font-size: 1.25rem !important;
    color: #a1a1aa !important;
    line-height: 1.7 !important;
    max-width: 700px !important;
    margin: 0 auto !important;
}

/* Dekoracyjny element */
.blog-hero-content::after {
    content: '' !important;
    display: block !important;
    width: 60px !important;
    height: 4px !important;
    background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
    margin: 40px auto 0 !important;
    border-radius: 2px !important;
}

/* Container dla artykułów */
.container {
    max-width: 1200px !important;
    margin: 0 auto !important;
    padding: 0 20px 80px !important;
}

/* Responsive */
@media (max-width: 768px) {
    .blog-hero {
        padding: 120px 20px 60px !important;
        min-height: 350px !important;
    }
    
    .blog-hero h1 {
        font-size: 2rem !important;
    }
    
    .blog-hero p {
        font-size: 1rem !important;
    }
}
</style>
</head>"""

# Zamień </head>
content = content.replace('</head>', hero_fix)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Naprawiono hero sekcję:")
print("  - Dodano gradient tła")
print("  - Poprawiono widoczność tekstu")
print("  - Dodano dekoracyjny element")
print("  - Ustawiono właściwe odstępy")
