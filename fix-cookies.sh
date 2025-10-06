#!/bin/bash

# Znajdź wszystkie pliki HTML
find . -name "*.html" -type f | while read file; do
  echo "Przetwarzam: $file"

  # Backup
  cp "$file" "$file.backup"

  # Zamień GTM i GA na zablokowane wersje
  sed -i '' \
    -e 's|<script async src="https://www.googletagmanager.com/gtag/js|<script type="text/plain" data-category="analytics" async src="https://www.googletagmanager.com/gtag/js|g' \
    -e 's|<!-- Google Tag Manager -->|<!-- Google Tag Manager - ZABLOKOWANY DO ZGODY -->|g' \
    -e 's|<!-- Google Analytics -->|<!-- Google Analytics - ZABLOKOWANY DO ZGODY -->|g' \
    "$file"

  # Dla inline GTM script
  perl -i -pe 's|<script>\s*\(function\(w,d,s,l,i\)|<script type="text/plain" data-category="analytics">\n(function(w,d,s,l,i)|g' "$file"

  # Dla inline GA script
  perl -i -pe 's|<script>\s*window\.dataLayer|<script type="text/plain" data-category="analytics">\nwindow.dataLayer|g' "$file"

done

echo "Gotowe! Sprawdź zmiany i usuń pliki .backup jeśli OK"
