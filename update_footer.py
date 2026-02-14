import os
import re

# Ten skrypt doda ładowanie wspólnego komponentu do każdego pliku HTML
FOOTER_SCRIPT_TAG = '<script src="/js/footer-component.js"></script>\n</body>'

def cleanup_and_inject():
    for root, dirs, files in os.walk("."):
        # Pomijamy foldery systemowe
        if '.git' in dirs: dirs.remove('.git')
        
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 1. Usuwamy wszystkie stare tagi <footer>...</footer>
                # To usunie też stary tekst "© Collytics. All rights reserved..."
                content = re.sub(r'<footer.*?>.*?</footer>', '', content, flags=re.DOTALL)

                # 2. Dodajemy skrypt ładujący nową stopkę przed </body>
                if '/js/footer-component.js' not in content:
                    if '</body>' in content:
                        content = content.replace('</body>', FOOTER_SCRIPT_TAG)
                    else:
                        content += FOOTER_SCRIPT_TAG

                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Zaktualizowano: {path}")

if __name__ == "__main__":
    cleanup_and_inject()
