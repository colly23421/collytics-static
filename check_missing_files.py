import os
import glob

print("Sprawdzam pliki blogu...")
print("-" * 50)

expected_files = [
    'facebook-conversion-api-api-konwersji-bezpieczniejsze-i-bardziej-niezawodne-zrodlo-danych.html',
    'google-tag-manager-w-wordpress-jak-zainstalowac.html',
    'opcje-dopasowania-slow-kluczowych-w-google-ads.html'
]

for filename in expected_files:
    filepath = f'blog/{filename}'
    if os.path.exists(filepath):
        print(f"✓ Istnieje: {filename}")
    else:
        print(f"✗ BRAK: {filename}")

print("\nWszystkie pliki w blog/:")
for file in glob.glob('blog/*.html'):
    print(f"  - {os.path.basename(file)}")
