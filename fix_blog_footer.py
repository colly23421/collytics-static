import os

filepath = 'blog/index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Znajdź i popraw ścieżkę do logo w footerze
content = content.replace(
    'src="assets/images/logo main transparent.png"',
    'src="../assets/images/logo main transparent.png"'
)

# Dodaj style naprawiające miganie i widoczność
footer_fix = """
<style>
/* NAPRAWA FOOTERA */
footer {
    background: #111111 !important;
    border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
    padding: 60px 5% 40px !important;
    position: relative !important;
    z-index: 1 !important;
}

footer .logo {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    margin-bottom: 24px !important;
}

footer .logo img {
    height: 60px !important;
    max-height: 60px !important;
    width: auto !important;
    display: block !important;
    opacity: 1 !important;
    visibility: visible !important;
}

/* Zapobieganie miganiu */
footer * {
    -webkit-backface-visibility: hidden !important;
    backface-visibility: hidden !important;
    transform: translateZ(0) !important;
}

/* Fix dla przycisków */
footer .cta-button {
    display: inline-block !important;
    background: transparent !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    color: #FFFFFF !important;
    padding: 14px 32px !important;
    border-radius: 50px !important;
    text-decoration: none !important;
    transition: all 0.3s ease !important;
}

footer .cta-button:hover {
    background: rgba(255, 255, 255, 0.05) !important;
    border-color: rgba(255, 255, 255, 0.4) !important;
}

/* Napraw tekst */
footer h2 {
    color: #FFFFFF !important;
    font-size: 2rem !important;
    margin-bottom: 20px !important;
}

footer p {
    color: #a1a1aa !important;
}

.footer-bottom {
    padding-top: 40px !important;
    border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
    color: #a1a1aa !important;
    font-size: 0.875rem !important;
}
</style>
</head>"""

# Dodaj style przed </head>
content = content.replace('</head>', footer_fix)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Naprawiono footer:")
print("  - Poprawiono ścieżkę do logo (../assets/)")
print("  - Naprawiono miganie elementów")
print("  - Ustawiono właściwą widoczność")
