#!/usr/bin/env python3
"""
fix_canonical.py - usuwa .html z canonical i og:url w plikach HTML Collytics
Uruchom z głównego katalogu repo: python3 fix_canonical.py
"""

import os
import re

DOMAIN = "https://www.collytics.io"

def fix_meta_urls(content, filepath):
    changes = []

    # 1. canonical: <link rel="canonical" href="https://www.collytics.io/cokolwiek.html">
    def fix_canonical(m):
        old = m.group(0)
        new = old.replace('.html"', '"')
        if old != new:
            changes.append(f"  canonical: ...{m.group(1)}.html → bez .html")
        return new

    content = re.sub(
        r'<link\s+rel="canonical"\s+href="https://www\.collytics\.io([^"]+)\.html"',
        fix_canonical,
        content
    )

    # 2. og:url: <meta property="og:url" content="https://www.collytics.io/cokolwiek.html">
    def fix_og_url(m):
        old = m.group(0)
        new = old.replace('.html"', '"')
        if old != new:
            changes.append(f"  og:url: ...{m.group(1)}.html → bez .html")
        return new

    content = re.sub(
        r'(<meta\s+property="og:url"\s+content="https://www\.collytics\.io)([^"]+)\.html"',
        lambda m: m.group(1) + m.group(2) + '"',
        content
    )
    # Zlicz zmiany og:url osobno
    og_count = len(re.findall(r'og:url', content))

    # 3. JSON-LD url fields: "url": "https://www.collytics.io/cokolwiek.html"
    def fix_jsonld_url(m):
        old = m.group(0)
        new = old.replace('.html"', '"')
        if old != new:
            changes.append(f"  JSON-LD url: zmieniono")
        return new

    content = re.sub(
        r'("url"\s*:\s*"https://www\.collytics\.io[^"]+)\.html"',
        lambda m: m.group(1) + '"',
        content
    )

    return content, changes


def process_all_html(root_dir="."):
    total_files = 0
    modified_files = 0
    skip_dirs = {"node_modules", ".git", "__pycache__", "backups"}

    for dirpath, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in skip_dirs]

        for filename in files:
            if not filename.endswith(".html"):
                continue

            filepath = os.path.join(dirpath, filename)
            total_files += 1

            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                original = f.read()

            fixed, changes = fix_meta_urls(original, filepath)

            if fixed != original:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(fixed)
                modified_files += 1
                print(f"✅ {filepath}")
                for c in changes:
                    print(c)
            # else: plik bez zmian, pomijamy

    print(f"\n{'='*50}")
    print(f"Sprawdzono plików:  {total_files}")
    print(f"Zmodyfikowano:      {modified_files}")
    print(f"{'='*50}")


if __name__ == "__main__":
    print("🔧 Naprawianie canonical i og:url (usuwanie .html)...\n")
    process_all_html(".")
    print("\n✨ Gotowe!")
