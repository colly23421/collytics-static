import os
import re

changed_files = []

SCRIPTS_TO_DEFER = [
    '/js/navbar-component.js',
    '/js/cookie-banner.js',
    '/js/footer-component.js',
    '../js/cookie-banner.js',
    'js/cookie-banner.js',
    'js/navbar-component.js',
    '../js/navbar-component.js',
    '../js/footer-component.js',
]

NEW_FONTS = '''<link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" media="print" onload="this.media='all'">
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"></noscript>'''

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    original = content
    changes = []

    for src in SCRIPTS_TO_DEFER:
        pattern = f'<script src="{src}"></script>'
        replacement = f'<script src="{src}" defer></script>'
        if pattern in content:
            content = content.replace(pattern, replacement)
            changes.append(f'  defer: {src}')

    font_pattern = r'<link[^>]*fonts\.googleapis\.com/css2\?family=Inter[^>]*>'
    if re.search(font_pattern, content):
        content = re.sub(font_pattern, '', content)
        content = content.replace('</head>', NEW_FONTS + '\n</head>', 1)
        changes.append('  async Google Fonts')

    def add_lazy(m):
        tag = m.group(0)
        if 'loading=' in tag or 'logo' in tag.lower() or 'favicon' in tag.lower():
            return tag
        return tag[:-1] + ' loading="lazy">'

    new_content = re.sub(r'<img\b[^>]*>', add_lazy, content)
    if new_content != content:
        content = new_content
        changes.append('  lazy images')

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return changes
    return []

html_files = []
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', '.vercel']]
    for fn in files:
        if fn.endswith('.html') and 'backup' not in fn:
            html_files.append(os.path.join(root, fn))

print(f"\nZnaleziono {len(html_files)} plikow HTML\n")
for fp in sorted(html_files):
    changes = process_file(fp)
    if changes:
        print(f"OK: {fp}")
        for c in changes:
            print(c)
        changed_files.append(fp)

print(f"\nZmieniono: {len(changed_files)} plikow")
