import os
import re

# Konfiguracja
ROOT_DIR = '.'  # Szuka w obecnym folderze
FONT_LINKS = """
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
"""

GLOBAL_CSS_PATH = os.path.join('css', 'global.css')
GLOBAL_CSS_RULE = """
/* Global Font Setting (Added automatically) */
body {
  font-family: 'Inter', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
"""

def update_html_files():
    print("--- Aktualizacja plików HTML ---")
    for root, dirs, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Sprawdź czy plik ma <head> i czy nie ma już Intera
                if "</head>" in content and "family=Inter" not in content:
                    # Wstaw linki przed zamknięciem </head>
                    new_content = content.replace("</head>", FONT_LINKS + "\n</head>")
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Zaktualizowano: {file_path}")
                elif "family=Inter" in content:
                    print(f"Pominięto (już ma Inter): {file_path}")

def update_css_files():
    print("\n--- Aktualizacja plików CSS ---")
    
    # 1. Ustawienie globalne
    if os.path.exists(GLOBAL_CSS_PATH):
        with open(GLOBAL_CSS_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Dodajemy regułę body na górę pliku, jeśli jej nie ma
        if "font-family: 'Inter'" not in content:
            new_content = GLOBAL_CSS_RULE + "\n" + content
            with open(GLOBAL_CSS_PATH, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Dodano regułę globalną do: {GLOBAL_CSS_PATH}")
    else:
        print(f"Błąd: Nie znaleziono {GLOBAL_CSS_PATH}!")

    # 2. Czyszczenie innych plików CSS
    for root, dirs, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith(".css"):
                file_path = os.path.join(root, file)
                
                # Pomijamy global.css i biblioteki zewnętrzne jeśli są
                if file_path == GLOBAL_CSS_PATH or "bootstrap" in file:
                    continue

                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Szukamy starych font-family i komentujemy je
                # Wyrażenie regularne szuka: font-family: cos_tam;
                # i zamienia na: /* AUTO-REMOVED font-family: cos_tam; */
                
                # Pomiń, jeśli to już jest Inter
                if "font-family: 'Inter'" in content:
                    continue

                def replace_font(match):
                    return f"/* AUTO-REMOVED {match.group(0)} */"

                # Regex: znajdź font-family które NIE zawiera 'Inter'
                new_content = re.sub(r'font-family:\s*(?!.*?Inter)[^;]+;', replace_font, content)
                
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Wyczyszczono stare fonty w: {file_path}")

if __name__ == "__main__":
    update_html_files()
    update_css_files()
    print("\nGotowe! Wszystkie pliki zaktualizowane.")
