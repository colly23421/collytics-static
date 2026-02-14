import os
import re

# Tag skryptu navbar
NAVBAR_SCRIPT = '<script src="/js/navbar-component.js"></script>'

def update_navbar():
    count = 0
    root_path = os.getcwd()
    print(f"Rozpoczynam aktualizację navbar w: {root_path}")

    for root, dirs, files in os.walk(root_path):
        # Ignoruj foldery
        if '.git' in dirs:
            dirs.remove('.git')
        if 'node_modules' in dirs:
            dirs.remove('node_modules')
        
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()

                original_content = content

                # Usuń stary navbar (wszystko od <nav> do </div> menu-overlay)
                content = re.sub(
                    r'<nav\s+class="navbar">.*?<div\s+class="menu-overlay"[^>]*></div>',
                    '',
                    content,
                    flags=re.DOTALL | re.IGNORECASE
                )

                # Dodaj skrypt navbar na początku <body> jeśli go nie ma
                if 'navbar-component.js' not in content:
                    # Znajdź <body> i dodaj skrypt zaraz po nim
                    content = re.sub(
                        r'(<body[^>]*>)',
                        r'\1\n' + NAVBAR_SCRIPT + '\n',
                        content,
                        flags=re.IGNORECASE
                    )

                # Zapisz jeśli są zmiany
                if content != original_content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(content)
                        f.flush()
                        os.fsync(f.fileno())
                    print(f"✅ Zaktualizowano: {path}")
                    count += 1

    print(f"\n🎉 Operacja zakończona. Zmieniono plików: {count}")

if __name__ == "__main__":
    update_navbar()
