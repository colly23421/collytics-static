import os
from bs4 import BeautifulSoup, Comment

# --- Konfiguracja ---
BLOG_DIR = 'blog'
TEMPLATE_FILE = 'index.html' # Plik wzorcowy dla nawigacji

print("--- Rozpoczynam automatyczną naprawę artykułów bloga ---")

# --- Wczytanie wzorca nawigacji ---
try:
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        soup_template = BeautifulSoup(f.read(), 'html.parser')
except FileNotFoundError:
    print(f"BŁĄD: Nie znaleziono pliku wzorca '{TEMPLATE_FILE}'. Upewnij się, że skrypt jest w głównym folderze projektu.")
    exit()

# Wyciągnięcie wzorcowej nawigacji
template_nav = soup_template.find('nav', class_='navbar')
template_dropdown = soup_template.find('div', class_='dropdown-menu')
template_overlay = soup_template.find('div', class_='menu-overlay')

if not all([template_nav, template_dropdown, template_overlay]):
    print("BŁĄD: Nie udało się znaleźć kompletnej nawigacji w pliku wzorca index.html.")
    exit()

# Popraw ścieżki w skopiowanej nawigacji, aby działały z podfolderu
for img in template_nav.find_all('img'):
    if img['src'].startswith('/assets'):
        img['src'] = '..' + img['src']
for img in template_dropdown.find_all('img'):
    if img['src'].startswith('/assets'):
        img['src'] = '..' + img['src']

# --- Przetwarzanie plików w folderze /blog/ ---
if not os.path.isdir(BLOG_DIR):
    print(f"BŁĄD: Nie znaleziono folderu '{BLOG_DIR}'.")
    exit()

for filename in os.listdir(BLOG_DIR):
    if filename.endswith('.html') and filename != 'index.html':
        filepath = os.path.join(BLOG_DIR, filename)
        print(f"-> Naprawiam: {filepath}")

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')

            # --- 1. NAPRAWA SEKCI <HEAD> ---
            if soup.head:
                original_title = soup.title or soup.new_tag('title')
                original_description = soup.find('meta', attrs={'name': 'description'})

                # Usuń całą zawartość head
                soup.head.clear()

                # Dodaj nową, czystą strukturę
                soup.head.append(BeautifulSoup(f"""
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    {original_title}
                    {original_description or ''}
                    <link rel="shortcut icon" type="image/png" href="../assets/images/Wordpress Transparent.png">
                    <link rel="preconnect" href="https://fonts.googleapis.com">
                    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
                    <link rel="stylesheet" href="../css/global.css">
                    <link rel="stylesheet" href="../css/blog.css">
                """, 'html.parser'))

            # --- 2. NAPRAWA NAWIGACJI W <BODY> ---
            old_nav = soup.find('nav')
            old_dropdown = soup.find('div', class_='dropdown-menu')
            old_overlay = soup.find('div', class_='menu-overlay')

            if old_nav: old_nav.replace_with(template_nav)
            if old_dropdown: old_dropdown.replace_with(template_dropdown)
            if old_overlay: old_overlay.replace_with(template_overlay)

            # --- 3. NAPRAWA SKRYPTU ---
            # Usuń stare skrypty
            for script_tag in soup.body.find_all('script'):
                script_tag.decompose()

            # Dodaj nowy skrypt
            script_content = """
            document.addEventListener("click", function(e) {
                if(e.target.id === "menuTrigger") {
                    document.getElementById("dropdownMenu").classList.add("active");
                    document.getElementById("menuOverlay").classList.add("active");
                }
                if(e.target.id === "closeMenu" || e.target.id === "menuOverlay") {
                    document.getElementById("dropdownMenu").classList.remove("active");
                    document.getElementById("menuOverlay").classList.remove("active");
                }
            });
            """
            new_script_tag = soup.new_tag('script')
            new_script_tag.string = script_content
            soup.body.append(new_script_tag)


            # Zapisz zmiany
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(soup))

        except Exception as e:
            print(f"  --> Wystąpił błąd: {e}")

print("\nGotowe! Wszystkie artykuły w folderze /blog/ zostały zaktualizowane.")
