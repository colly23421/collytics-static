#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skrypt automatycznie dodający Cookie Banner do wszystkich plików HTML
Autor: Claude dla Collytics.io
"""

import os
import re
from pathlib import Path

# Konfiguracja
CSS_LINK = '<link rel="stylesheet" href="/css/cookie-banner.css">'
JS_SCRIPT = '<script src="/js/cookie-banner.js"></script>'

# Linki dla plików w podfolderach (z ../)
CSS_LINK_SUBFOLDER = '<link rel="stylesheet" href="../css/cookie-banner.css">'
JS_SCRIPT_SUBFOLDER = '<script src="../js/cookie-banner.js"></script>'

def find_all_html_files(directory='.'):
    """Znajdź wszystkie pliki HTML w katalogu i podkatalogach"""
    html_files = []
    for root, dirs, files in os.walk(directory):
        # Pomijamy foldery: node_modules, .git, backups
        dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', '__pycache__', 'backups']]

        for file in files:
            if file.endswith('.html') and not file.startswith('.'):
                html_files.append(os.path.join(root, file))
    return html_files

def is_in_subfolder(filepath):
    """Sprawdź czy plik jest w podfolderze"""
    # Zlicz ilość '/' w ścieżce (więcej niż 0 = podfolder)
    return filepath.count(os.sep) > 0

def already_has_cookie_banner(content):
    """Sprawdź czy plik już ma cookie banner"""
    return 'cookie-banner.css' in content or 'cookie-banner.js' in content

def add_cookie_banner_to_file(filepath):
    """Dodaj linki do cookie bannera w pliku HTML"""

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Sprawdź czy już ma cookie banner
        if already_has_cookie_banner(content):
            print(f"⏭️  POMINIĘTO (już ma): {filepath}")
            return False

        # Określ czy to podfolder
        in_subfolder = is_in_subfolder(filepath)
        css_link = CSS_LINK_SUBFOLDER if in_subfolder else CSS_LINK
        js_script = JS_SCRIPT_SUBFOLDER if in_subfolder else JS_SCRIPT

        modified = False

        # 1. Dodaj CSS do <head>
        if '</head>' in content:
            # Dodaj CSS przed zamknięciem </head>
            css_with_comment = f'\n    <!-- Cookie Banner Styles -->\n    {css_link}\n'
            content = content.replace('</head>', f'{css_with_comment}</head>', 1)
            modified = True

        # 2. Dodaj JS przed </body>
        if '</body>' in content:
            # Dodaj JS przed zamknięciem </body>
            js_with_comment = f'\n    <!-- Cookie Banner Script -->\n    {js_script}\n'
            content = content.replace('</body>', f'{js_with_comment}</body>', 1)
            modified = True

        # Zapisz zmodyfikowany plik
        if modified:
            # Stwórz backup przed zapisaniem
            backup_path = f"{filepath}.backup"
            with open(backup_path, 'w', encoding='utf-8') as f:
                # Zapisz oryginalny content jako backup
                with open(filepath, 'r', encoding='utf-8') as orig:
                    f.write(orig.read())

            # Zapisz nową wersję
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"✅ ZMODYFIKOWANO: {filepath}")
            return True
        else:
            print(f"⚠️  PROBLEM: {filepath} - nie znaleziono </head> lub </body>")
            return False

    except Exception as e:
        print(f"❌ BŁĄD w {filepath}: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("🍪 COOKIE BANNER - Automatyczna instalacja")
    print("=" * 60)
    print()

    # Znajdź wszystkie pliki HTML
    html_files = find_all_html_files('.')

    print(f"Znaleziono {len(html_files)} plików HTML\n")

    if not html_files:
        print("❌ Nie znaleziono żadnych plików HTML!")
        return

    # Pokaż listę plików
    print("Pliki do przetworzenia:")
    for f in html_files:
        print(f"  - {f}")
    print()

    # Zapytaj o zgodę
    response = input("Czy chcesz kontynuować? (tak/nie): ").lower()
    if response not in ['tak', 't', 'yes', 'y']:
        print("Anulowano.")
        return

    print("\nRozpoczynam modyfikację plików...\n")

    # Modyfikuj pliki
    modified_count = 0
    skipped_count = 0
    error_count = 0

    for filepath in html_files:
        result = add_cookie_banner_to_file(filepath)
        if result:
            modified_count += 1
        elif result is False:
            skipped_count += 1
        else:
            error_count += 1

    # Podsumowanie
    print()
    print("=" * 60)
    print("📊 PODSUMOWANIE")
    print("=" * 60)
    print(f"✅ Zmodyfikowano:    {modified_count} plików")
    print(f"⏭️  Pominięto:        {skipped_count} plików")
    print(f"❌ Błędy:            {error_count} plików")
    print(f"📁 Razem:            {len(html_files)} plików")
    print()
    print("💾 Backup plików zapisany z rozszerzeniem .backup")
    print()
    print("✨ Gotowe! Sprawdź stronę w przeglądarce.")
    print("=" * 60)

if __name__ == "__main__":
    main()
