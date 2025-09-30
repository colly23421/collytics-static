import os
import re
from bs4 import BeautifulSoup

# Nazwa pliku, który będzie naszym wzorcem
template_file = 'index.html'

# Lista plików do zignorowania (oprócz samego wzorca)
ignore_list = ['test-menu.html', 'blog-nav.html', 'nav-template.html']

print(f"Używam '{template_file}' jako wzorca nawigacji i nagłówka.")

# --- Wczytanie wzorca ---
try:
    with open(template_file, 'r', encoding='utf-8') as f:
        template_content = f.read()
except FileNotFoundError:
    print(f"BŁĄD: Nie znaleziono pliku wzorca '{template_file}'. Upewnij się, że skrypt jest w głównym folderze projektu.")
    exit()

soup_template = BeautifulSoup(template_content, 'html.parser')

# Wyciągnięcie wzorcowej sekcji <head> i nawigacji
template_head = soup_template.head
template_nav = soup_template.find('nav', class_='navbar')
template_dropdown = soup_template.find('div', class_='dropdown-menu')
template_overlay = soup_template.find('div', class_='menu-overlay')

if not all([template_head, template_nav, template_dropdown, template_overlay]):
    print("BŁĄD: Nie udało się znaleźć wszystkich elementów menu lub sekcji <head> w pliku wzorca.")
    exit()

# --- Przetwarzanie plików HTML ---
for root, dirs, files in os.walk('.'):
    for filename in files:
        if filename.endswith('.html') and filename != template_file and filename not in ignore_list:
            filepath = os.path.join(root, filename)
            print(f"Aktualizuję: {filepath} ...")

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    target_content = f.read()

                soup_target = BeautifulSoup(target_content, 'html.parser')

                # Zachowanie oryginalnego tytułu strony
                original_title = soup_target.title
                if original_title:
                    template_head.title.replace_with(original_title)

                # Podmiana <head>
                if soup_target.head:
                    soup_target.head.replace_with(template_head)
                else:
                    # Jeśli nie ma head, dodaj go na początku
                    soup_target.html.insert(0, template_head)

                # Podmiana nawigacji
                old_nav = soup_target.find('nav', class_='navbar')
                old_dropdown = soup_target.find('div', class_='dropdown-menu')
                old_overlay = soup_target.find('div', class_='menu-overlay')

                if old_nav: old_nav.replace_with(template_nav)
                if old_dropdown: old_dropdown.replace_with(template_dropdown)
                if old_overlay: old_overlay.replace_with(template_overlay)

                # Zapisanie zmian
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(str(soup_target.prettify()))

            except Exception as e:
                print(f"  --> Wystąpił błąd podczas przetwarzania pliku {filepath}: {e}")

print("\nGotowe! Wszystkie pliki HTML zostały zaktualizowane.")
