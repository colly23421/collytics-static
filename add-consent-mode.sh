#!/bin/bash

find . -name "*.html" -type f | while read file; do
  if grep -q "googletagmanager.com/gtm.js" "$file"; then
    echo "Przetwarzam: $file"
    cp "$file" "$file.backup"
    
    # Dodaj Consent Mode PRZED pierwszym <script> w <head>
    perl -0777 -i -pe 's/(<head>.*?)(<script>)/$1<!-- GTM Consent Mode - MUSI BYĆ PRZED GTM -->\n  <script>\n  window.dataLayer = window.dataLayer || [];\n  function gtag(){dataLayer.push(arguments);}\n  gtag("consent", "default", {\n    "analytics_storage": "denied",\n    "ad_storage": "denied",\n    "ad_user_data": "denied",\n    "ad_personalization": "denied"\n  });\n  <\/script>\n  $2/s' "$file"
  fi
done

echo "Gotowe!"
