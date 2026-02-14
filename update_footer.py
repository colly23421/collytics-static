import os
import re

# Używamy ścieżki absolutnej od roota strony, aby skrypt działał wszędzie tak samo
JS_TAG = '\n<script src="/js/footer-component.js"></script>\n</body>'

def cleanup_and_inject():
    count = 0
    # Pobieramy ścieżkę do folderu, w którym jest skrypt
    base_path = os.getcwd()
    print(f"Rozpoczynam pracę w: {base_path}")

    for root, dirs, files in os.walk(base_path):
        # Pomijamy foldery techniczne gita
        if '.git' in dirs:
            dirs.remove('.git')
        
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # 1. Usuwamy stare stopy - ignorujemy wielkość liter (re.IGNORECASE)
                    # Czyścimy też ewentualne białe znaki wokół tagu
                    new_content = re.sub(r'\s*<footer.*?>.*?</footer>\s*', '\n', content, flags=re.DOTALL | re.IGNORECASE)

                    # 2. Wstrzykujemy skrypt komponentu przed </body>
                    # Sprawdzamy czy skrypt już tam jest, żeby nie dublować
                    if 'footer-component.js' not in new_content:
                        if '</body>' in new_content.lower():
                            # replace z zachowaniem oryginalnej wielkości liter tagu body
                            new_content = re.sub(r'</body>', JS_TAG, new_content, flags=re.IGNORECASE)
                        else:
                            # Jeśli plik nie ma </body>, dodajemy na końcu
                            new_content += JS_TAG
                    
                    # Zapisujemy tylko jeśli faktycznie zaszła zmiana
                    if content != new_content:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"ZMIENIONO: {path}")
                        count += 1
                    else:
                        print(f"Pominięto (brak zmian): {path}")

                except Exception as e:
                    print(f"BŁĄD w pliku {path}: {e}")

    print(f"\n--- GOTOWE ---")
    print(f"Zaktualizowano łącznie: {count} plików HTML.")

if __name__ == "__main__":
    cleanup_and_inject()
