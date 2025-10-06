#!/bin/bash

echo "Dodaję GTM Consent Mode..."

find . -name "*.html" -type f | while read file; do
  if grep -q "googletagmanager.com/gtm.js" "$file"; then
    echo "Przetwarzam: $file"
    cp "$file" "$file.backup"
    
    # Dodaj Consent Mode zaraz po <head>
    sed -i '' '/<head>/a\
  <!-- GTM Consent Mode -->\
  <script>\
  window.dataLayer = window.dataLayer || [];\
  function gtag(){dataLayer.push(arguments);}\
  gtag("consent", "default", {\
    "analytics_storage": "denied",\
    "ad_storage": "denied",\
    "ad_user_data": "denied",\
    "ad_personalization": "denied"\
  });\
  </script>
' "$file"
    
    # Usuń type="text/plain" i data-category z GTM
    sed -i '' \
      -e 's/ type="text\/plain" data-category="analytics"//g' \
      -e 's/ data-category="analytics"//g' \
      "$file"
  fi
done

echo "Gotowe!"
