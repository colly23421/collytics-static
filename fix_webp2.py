import os

files_to_fix = [
    ('assets/images/688e0ded690333d20e7aa5be_Code_Generated_Image.png', 'assets/images/688e0ded690333d20e7aa5be_Code_Generated_Image.webp'),
    ('assets/images/6876194656c6edf5453ea3b7_llms-txt-p-3200.jpeg', 'assets/images/6876194656c6edf5453ea3b7_llms-txt-p-3200.webp'),
    ('assets/images/blog/google ai.png', 'assets/images/blog/google_ai.webp'),
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
