import os
import re
from bs4 import BeautifulSoup

# --- KONFIGURACJA ---
BASE_FONT_SIZE_NEW = "15px"  # Nowy, mniejszy rozmiar czcionki dla całej strony
HERO_H1_FONT_SIZE = "4.5rem"  # Oryginalny rozmiar dla H1 w sekcji Hero
HERO_P_FONT_SIZE = "1.25rem" # Oryginalny rozmiar dla P w sekcji Hero
# --------------------

def update_css_file(filepath):
    """Znajduje global.css, zmniejsza bazową czcionkę i dodaje wyjątek."""
    print(f"🔄 Przetwarzanie pliku CSS: {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Krok 1: Zmniejszenie bazowej czcionki w body
        # Używamy regex do znalezienia i podmiany font-size w selektorze body
        pattern = re.compile(r"(body\s*\{[^}]*?font-size\s*:\s*)(\d+px)([^}]*?\})", re.DOTALL)

        # Funkcja do podmiany, która pobiera oryginalny rozmiar i loguje go
        def replace_font_size(match):
            original_size = match.group(2)
            print(f"    - Znaleziono bazowy font-size: {original_size}. Zmieniam na {BASE_FONT_SIZE_NEW}.")
            return f"{match.group(1)}{BASE_FONT_SIZE_NEW}{match.group(3)}"

        content, replacements = pattern.subn(replace_font_size, content)

        if replacements == 0:
            print("    - UWAGA: Nie znaleziono reguły 'font-size' w selektorze 'body'.")
            return

        # Krok 2: Dodanie wyjątku dla sekcji .hero na końcu pliku
        hero_exception_css = f"""
/* === Wyjątek dla sekcji Hero na stronie głównej === */
/* Przywraca oryginalny rozmiar fontu dla h1 i p wewnątrz .hero */
.hero h1 {{
    font-size: {HERO_H1_FONT_SIZE};
}}
.hero p {{
    font-size: {HERO_P_FONT_SIZE};
}}
"""
        if hero_exception_css.strip() not in content:
            content += hero_exception_css
            print(f"    - Dodano wyjątek dla .hero na końcu pliku.")

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ Plik CSS został zaktualizowany.")

    except FileNotFoundError:
        print(f"    - BŁĄD: Nie znaleziono pliku {filepath}")
    except Exception as e:
        print(f"    - BŁĄD: Wystąpił nieoczekiwany problem: {e}")


def convert_to_sentence_case(html_file):
    """Otwiera plik HTML i zamienia wszystkie nagłówki na Sentence case."""
    print(f"🔄 Przetwarzanie pliku HTML: {html_file}...")
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        changes_made = 0

        for tag in headings:
            if tag.string: # Przetwarzaj tylko tagi, które mają prosty tekst w środku
                original_text = tag.string.strip()
                # Zamień na małe litery, a potem pierwszą na dużą.
                sentence_case_text = original_text.lower().capitalize()

                if original_text != sentence_case_text:
                    tag.string.replace_with(sentence_case_text)
                    changes_made += 1

        if changes_made > 0:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(str(soup.prettify(formatter="html5")))
            print(f"    - Zmieniono {changes_made} nagłówków na Sentence case.")
        else:
            print("    - Nie znaleziono nagłówków do zmiany.")

    except Exception as e:
        print(f"    - BŁĄD: Nie można było przetworzyć pliku {html_file}. Powód: {e}")


def main():
    """Główna funkcja skryptu."""
    print("🚀 Rozpoczynam automatyczną aktualizację strony...")

    # Aktualizacja pliku CSS
    update_css_file('css/global.css')

    print("\n" + "="*50 + "\n")

    # Wyszukiwanie i aktualizacja wszystkich plików HTML
    for root, _, files in os.walk('.'):
        # Ignoruj foldery, których nie chcesz przeszukiwać (np. zależności node)
        if 'node_modules' in root:
            continue

        for file in files:
            if file.endswith('.html'):
                full_path = os.path.join(root, file)
                convert_to_sentence_case(full_path)

    print("\n" + "="*50)
    print("🎉 Wszystkie zadania zostały zakończone!")


if __name__ == "__main__":
    main()
