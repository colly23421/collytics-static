#!/bin/bash

echo "Konwersja obrazow do WebP..."

# Obrazy do konwersji
IMAGES=(
    "assets/images/confident.jpeg"
    "assets/images/stylish.jpeg"
    "assets/images/facebook.png"
    "assets/images/dentysta.png"
    "assets/images/partners/bdental.png"
    "assets/images/partners/chemiczna.png"
)

for img in "${IMAGES[@]}"; do
    if [ -f "$img" ]; then
        # Nazwa bez rozszerzenia
        base="${img%.*}"
        webp_file="${base}.webp"
        
        # Konwertuj z quality 75
        cwebp -q 75 "$img" -o "$webp_file"
        
        # Rozmiary
        orig=$(du -h "$img" | cut -f1)
        new=$(du -h "$webp_file" | cut -f1)
        echo "  $img: $orig -> $new"
    else
        echo "  BRAK: $img"
    fi
done

echo ""
echo "Gotowe! Sprawdz rozmiary powyzej."
