import os

# Popraw linki w blog/index.html
filepath = 'blog/index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Zamień linki na właściwe nazwy
replacements = [
    # Facebook Conversion API - różne warianty
    ('facebook-conversion-api.html', 
     'facebook-conversion-api-api-konwersji-bezpieczniejsze-i-bardziej-niezawodne-zrodlo-danych.html'),
    ('facebook-conversion-api-api-konwersji.html', 
     'facebook-conversion-api-api-konwersji-bezpieczniejsze-i-bardziej-niezawodne-zrodlo-danych.html'),
    
    # Google Tag Manager
    ('google-tag-manager-wordpress.html', 
     'google-tag-manager-w-wordpress-jak-zainstalowac.html'),
    ('gtm-wordpress.html', 
     'google-tag-manager-w-wordpress-jak-zainstalowac.html'),
    
    # Opcje dopasowania
    ('opcje-dopasowania-google-ads.html', 
     'opcje-dopasowania-slow-kluczowych-w-google-ads.html'),
    ('slowa-kluczowe-google-ads.html', 
     'opcje-dopasowania-slow-kluczowych-w-google-ads.html'),
]

# Zastosuj zamienniki
for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f"✓ Zamieniono: {old} → {new}")

# Zapisz
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ Linki w blog/index.html zostały naprawione!")
