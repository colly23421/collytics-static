import os
import re

# Wzorzec do znalezienia starego kodu GTM
pattern = r'<noscript>\s*<iframe[^>]*googletagmanager\.com/ns\.html\?id=GT-5R3VKTJG[^>]*>.*?</iframe>\s*</noscript>'

# Znajdź wszystkie pliki HTML
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Sprawdź czy stary GTM istnieje
            if 'GT-5R3VKTJG' in content:
                # Usuń stary kod GTM
                new_content = re.sub(pattern, '', content, flags=re.DOTALL)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"✓ Usunięto stary GTM z: {filepath}")
            else:
                print(f"⊘ Brak starego GTM w: {filepath}")

print("\nGotowe!")
