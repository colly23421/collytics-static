import os
import re

# Nowy kod GTM do dodania
new_gtm = """<!-- Google Tag Manager -->
<script>
(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-TZCR8FPZ');</script>
<!-- End Google Tag Manager -->
"""

# Wzorce do usunięcia starego GTM
old_gtm_patterns = [
    r'<!-- Google Tag Manager - ZABLOKOWANY DO ZGODY -->.*?<!-- End Google Tag Manager -->',
    r'<!-- Google Tag Manager -->.*?GT-5R3VKTJG.*?<!-- End Google Tag Manager -->',
    r'<noscript>.*?GT-5R3VKTJG.*?</noscript>'
]

# Znajdź wszystkie pliki HTML
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Usuń wszystkie stare kody GTM
            for pattern in old_gtm_patterns:
                content = re.sub(pattern, '', content, flags=re.DOTALL)
            
            # Dodaj nowy GTM przed </head>, jeśli GTM-TZCR8FPZ jeszcze nie istnieje
            if 'GTM-TZCR8FPZ' not in content and '</head>' in content:
                content = content.replace('</head>', new_gtm + '\n</head>')
            
            # Zapisz tylko jeśli były zmiany
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✓ Zaktualizowano: {filepath}")
            else:
                print(f"⊘ Bez zmian: {filepath}")

print("\nGotowe!")
