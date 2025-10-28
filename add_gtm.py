import os
import re

gtm_code = """<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-TZCR8FPZ');</script>
<!-- End Google Tag Manager -->
"""

# Znajdź wszystkie pliki HTML
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Sprawdź czy GTM już nie jest dodany
            if 'GTM-TZCR8FPZ' not in content:
                # Dodaj GTM przed </head>
                new_content = content.replace('</head>', gtm_code + '</head>')
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"✓ Dodano GTM do: {filepath}")
            else:
                print(f"⊘ GTM już istnieje w: {filepath}")

print("\nGotowe!")
