import os
import re

gtm_script = """
<!-- Google Tag Manager -->
<script>
(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-TZCR8FPZ');</script>
<!-- End Google Tag Manager -->"""

# Wzorzec noscript GTM do usunięcia
noscript_pattern = r'<noscript>.*?GTM-TZCR8FPZ.*?</noscript>'

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            
            # Usuń noscript GTM
            content = re.sub(noscript_pattern, '', content, flags=re.DOTALL)
            
            # Sprawdź czy GTM script już jest w head
            if 'GTM-TZCR8FPZ' not in content and '</head>' in content:
                # Dodaj GTM script przed </head>
                content = content.replace('</head>', gtm_script + '\n</head>')
                print(f"✓ Dodano GTM script do head: {filepath}")
            elif content != original:
                print(f"✓ Usunięto noscript GTM z: {filepath}")
            else:
                print(f"⊘ Bez zmian: {filepath}")
            
            if content != original:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)

print("\nGotowe!")
