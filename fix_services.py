import os

# Otwórz services.html
filepath = 'services.html'

if os.path.exists(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Dodaj styl wymuszający białe nagłówki w footer
    footer_style = """
<style>
/* Naprawka dla services.html */
footer h2, .footer-cta h2 {
    color: #FFFFFF !important;
}
footer p, .footer-cta p {
    color: #a1a1aa !important;
}
.footer-container {
    background: #111111 !important;
}
/* Upewnij się że wszystkie h2 są białe */
h2 {
    color: #FFFFFF !important;
}
</style>
"""
    
    # Dodaj przed </head>
    if '</head>' in content:
        content = content.replace('</head>', footer_style + '\n</head>')
    
    # Zapisz
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ Naprawiono services.html")
else:
    print("❌ Nie znaleziono services.html")
