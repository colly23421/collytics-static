// find-html-links.js
const fs = require('fs');
const path = require('path');

// Katalog główny projektu do przeszukania (kropka oznacza obecny katalog)
const DIRECTORY_TO_SCAN = './'; 
// Rozszerzenia plików, które chcemy sprawdzić pod kątem linków
const EXTENSIONS_TO_CHECK = ['.js', '.jsx', '.ts', '.tsx', '.html', '.md', '.astro'];

function scanDirectory(dir) {
    fs.readdir(dir, (err, files) => {
        if (err) {
            console.error('Błąd odczytu katalogu:', err);
            return;
        }

        files.forEach(file => {
            const filePath = path.join(dir, file);
            
            // Ignorujemy foldery, których nie musimy skanować
            if (filePath.includes('node_modules') || filePath.includes('.git') || filePath.includes('.next')) {
                return;
            }

            fs.stat(filePath, (err, stat) => {
                if (err) return;

                if (stat.isDirectory()) {
                    // Wywołanie rekursywne dla podkatalogów
                    scanDirectory(filePath);
                } else {
                    const ext = path.extname(file);
                    if (EXTENSIONS_TO_CHECK.includes(ext)) {
                        checkFileForHtmlLinks(filePath);
                    }
                }
            });
        });
    });
}

function checkFileForHtmlLinks(filePath) {
    fs.readFile(filePath, 'utf8', (err, content) => {
        if (err) return;
        
        // Proste wyrażenie regularne szukające atrybutów href="...html" lub href='...html'
        const regex = /href=["'][^"']*\.html["']/g;
        const matches = content.match(regex);
        
        if (matches) {
            console.log(`\n🔎 Znalazłem potencjalne linki .html w pliku: ${filePath}`);
            matches.forEach(match => console.log(`  - ${match}`));
        }
    });
}

// Uruchomienie skanowania
console.log('Rozpoczynam skanowanie plików...');
scanDirectory(DIRECTORY_TO_SCAN);