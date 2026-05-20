import os
import re

files_to_fix = [
    ('assets/images/confident.jpeg', 'assets/images/confident.webp'),
    ('assets/images/stylish.jpeg', 'assets/images/stylish.webp'),
    ('assets/images/facebook.png', 'assets/images/facebook.webp'),
    ('assets/images/dentysta.png', 'assets/images/dentysta.webp'),
    ('assets/images/partners/bdental.png', 'assets/images/partners/bdental.webp'),
    ('assets/images/partners/chemiczna.png', 'assets/images/partners/chemiczna.webp'),
]

changed = []
html_files = []
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', '.vercel']]
    for fn in files:
        if fn.endswith('.html'):
            html_files.append(os.path.join(root, fn))

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    original = content
    for old, new in files_to_fix:
        content = content.replace(old, new)
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        changed.append(filepath)
        print(f"OK: {filepath}")

print(f"\nZmieniono: {len(changed)} plikow")
