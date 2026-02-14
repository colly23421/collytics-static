import os
import re

# Definicja skryptu komponentu
JS_TAG = '\n<script src="/js/footer-component.js"></script>\n</body>'

def hard_update():
    count = 0
    # Pobieramy pełną ścieżkę roboczą
    root_path = os.getcwd()
    print(f"Rozpoczynam skanowanie w: {root_path}")

    for root, dirs, files in os.walk(root_path):
        if '.git' in dirs:
            dirs.remove('.git')
        
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Usuwanie starej stopki (niezależnie od wielkości liter)
                new_content = re.sub(r'<footer.*?>.*?</footer>', '', content, flags=re.DOTALL | re.IGNORECASE)

                # Wstawianie skryptu przed </body>
                if 'footer-component.js' not in new_content:
                    if '</body>' in new_content.lower():
                        new_content = re.sub(r'</body>', JS_TAG, new_content, flags=re.IGNORECASE)
                    else:
                        new_content += JS_TAG

                # Zapisywanie zmian tylko jeśli treść się zmieniła
                if content != new_content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                        f.flush()
                        os.fsync(f.fileno()) # Wymuszenie zapisu na dysku
                    print(f"ZAPISANO: {path}")
                    count += 1

    print(f"\nOperacja zakończona. Zmieniono plików: {count}")

if __name__ == "__main__":
    hard_update()
