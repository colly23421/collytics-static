import os
import re
from bs4 import BeautifulSoup

# --- GŁÓWNA KONFIGURACJA ---
BASE_FONT_SIZE_NEW = 15
HERO_H1_FONT_SIZE = "4.5rem"
HERO_P_FONT_SIZE = "1.25rem"
# -----------------------------

def update_css_file(filepath):
    """Modyfikuje plik global.css: zmienia bazowy font i konwertuje nagłówki na rem."""
    print(f"🔄 Przetwarzanie pliku CSS: {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # POPRAWKA 1: Szukaj font-size w 'html' LUB 'body'
        body_pattern = re.compile(r"((?:html|body)\s*\{[^}]*?font-size\s*:\s*)(\d+px)([^}]*?\})", re.DOTALL)

        def replace_body_font_size(match):
            original_size = match.group(2)
            new_size_css = f"{BASE_FONT_SIZE_NEW}px"
            print(f"    - Zmieniam bazowy font-size: z {original_size} na {new_size_css}.")
            return f"{match.group(1)}{new_size_css}{match.group(3)}"

        content, replacements = body_pattern.subn(replace_body_font_size, content)
        if replacements == 0:
            print("    - UWAGA: Nie znaleziono bazowego 'font-size' w 'html' ani 'body' do zmiany.")

        heading_pattern = re.compile(r"(h[1-6]\s*\{[^}]*?font-size\s*:\s*)(\d+)(px)([^}]*?\})", re.DOTALL)

        def convert_px_to_rem(match):
            original_px = int(match.group(2))
            rem_value = round(original_px / BASE_FONT_SIZE_NEW, 2)
            new_rem_size = f"{rem_value}rem"
            comment = f"/* {original_px}px / {BASE_FONT_SIZE_NEW}px */"
            print(f"    - Konwertuję nagłówek: z {original_px}px na {new_rem_size}.")
            return f"{match.group(1)}{new_rem_size} {comment}{match.group(4)}"

        content = heading_pattern.sub(convert_px_to_rem, content)

        hero_exception_css = f"""
/* === Wyjątek dla sekcji Hero na stronie głównej === */
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

        print(f"✅ Plik CSS został w pełni zaktualizowany.")

    except FileNotFoundError:
        print(f"    - BŁĄD: Nie znaleziono pliku {filepath}")
    except Exception as e:
        print(f"    - BŁĄD: Wystąpił nieoczekiwany problem: {e}")


def convert_headings_to_sentence_case(html_file):
    """Otwiera plik HTML i zamienia wszystkie nagłówki na Sentence case."""
    print(f"🔄 Przetwarzanie pliku HTML: {html_file}...")
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        changes_made = 0

        for tag in headings:
            # POPRAWKA 2: Użyj .get_text() aby pobrać tekst z zagnieżdżonych tagów
            original_text = tag.get_text(strip=True)
            if not original_text:
                continue

            sentence_case_text = original_text.lower().capitalize()

            if original_text != sentence_case_text:
                # Wyczyść zawartość taga (usuwa np. <strong>) i wstaw nowy tekst
                tag.clear()
                tag.append(sentence_case_text)
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
    print("🚀 Rozpoczynam automatyczną modyfikację całej strony (wersja 2.0)...")

    update_css_file('css/global.css')
    print("\n" + "="*50 + "\n")

    for root, _, files in os.walk('.'):
        if 'node_modules' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                full_path = os.path.join(root, file)
                convert_headings_to_sentence_case(full_path)

    print("\n" + "="*50)
    print("🎉 Wszystkie modyfikacje zostały zakończone!")


if __name__ == "__main__":
    main()
