import os

# Konfiguracja
ROOT_DIR = '.'
GLOBAL_CSS_LINK = '<link href="/css/global.css" rel="stylesheet">'
GLOBAL_CSS_PATH = os.path.join('css', 'global.css')

# Nowa zawartość global.css z wymuszeniem !important
GLOBAL_CSS_CONTENT = """
/* Global Font Setting (Enforced) */
body, h1, h2, h3, h4, h5, h6, p, span, a, li, button, input, textarea, select {
  font-family: 'Inter', sans-serif !important;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
"""

def add_global_css_link():
    print("--- Podpinanie css/global.css do plików HTML ---")
    for root, dirs, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Sprawdź czy plik już linkuje do global.css (różne warianty ścieżek)
                if "css/global.css" not in content:
                    # Szukamy miejsca, gdzie wstawić link (najlepiej przed końcem head)
                    if "</head>" in content:
                        new_content = content.replace("</head>", f"  {GLOBAL_CSS_LINK}\n</head>")
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Dodano global.css do: {file_path}")
                    else:
                        print(f"Pominięto (brak tagu head): {file_path}")
                else:
                    print(f"Już podpięty: {file_path}")

def update_global_css_rule():
    print("\n--- Aktualizacja reguły w css/global.css ---")
    if os.path.exists(GLOBAL_CSS_PATH):
        with open(GLOBAL_CSS_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Jeśli nie ma naszej wymuszonej reguły, dodajemy ją na samym początku
        if "font-family: 'Inter', sans-serif !important" not in content:
            new_content = GLOBAL_CSS_CONTENT + "\n" + content
            with open(GLOBAL_CSS_PATH, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("Zaktualizowano global.css o regułę z !important")
        else:
            print("global.css już ma silną regułę czcionki.")
    else:
        # Jeśli plik nie istnieje, tworzymy go
        with open(GLOBAL_CSS_PATH, 'w', encoding='utf-8') as f:
            f.write(GLOBAL_CSS_CONTENT)
        print("Utworzono nowy plik css/global.css")

if __name__ == "__main__":
    update_global_css_rule()
    add_global_css_link()
    print("\nGotowe! Wszystkie podstrony powinny teraz używać tej samej czcionki.")
