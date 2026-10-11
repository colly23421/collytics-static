# Collytics: zmiany treści SEO (październik 2026)

Instrukcja dla Claude Code. Źródło priorytetów: eksport Google Search Console (9.07–8.10.2026).

## Zasady ogólne

- Pracuj na nowym branchu `content/seo-2026-10`. Jeśli PR #2 (`fix/seo-audit-2026-10`) nie jest jeszcze scalony, utwórz branch od niego, żeby uniknąć konfliktów.
- Nie zmieniaj wyglądu ani układu. Używaj istniejących klas CSS i komponentów (sekcje, FAQ, karty).
- Nie dodawaj adresu pocztowego firmy nigdzie (ani w treści, ani w JSON-LD).
- Nie wymyślaj faktów, liczb ani nazw klientów. Jeśli tekst poniżej wymaga danych, których nie ma w repo, zostaw komentarz HTML `<!-- TODO: ... -->` i wypisz go w podsumowaniu.
- Każda zmiana FAQ na stronie musi być odzwierciedlona w JSON-LD `FAQPage` tej strony (te same pytania i odpowiedzi).
- Przy zmianie title/description zaktualizuj też `og:title`, `og:description`, `twitter:title`, `twitter:description`.
- Przy odświeżeniu wpisu ustaw `dateModified` w JSON-LD na `2026-10-11` i, jeśli wpis pokazuje datę, dodaj widoczną linię „Zaktualizowano: 11 października 2026”.
- Tego pliku (`seo-tresci-2026-10.md`) nie commituj.
- Zrób osobny commit dla każdej z części 1, 2 i 3. Przed każdym commitem pokaż diff do akceptacji.

---

## Część 1: strona Audytu Widoczności AI (`audyt-widocznosci-ai.html`)

Cel: z pozycji ok. 23 do pierwszej dziesiątki dla „audyt widoczności w AI” oraz zacząć łapać frazy „GEO” i „pozycjonowanie w ChatGPT”. GSC pokazuje popyt z całej Polski (zapytania z miastami: Warszawa, Bielsko-Biała, Chorzów, Konin, Radom, Częstochowa, Zabrze, Gliwice, Gdynia). Nie twórz osobnych podstron pod miasta.

### 1.1 Meta

- `<title>`: `Audyt widoczności w AI i GEO – pozycjonowanie w ChatGPT | Collytics`
- `meta description`: `Sprawdzamy, czy ChatGPT, Gemini i Perplexity polecają Twoją firmę. Audyt widoczności w AI i wdrożenie GEO dla firm z całej Polski. Raport w 48 h.`

### 1.2 H1 i lead

- H1: `Audyt widoczności w AI: czy ChatGPT poleca Twoją firmę, czy konkurencję?`
- Akapit pod H1 (zastępuje obecny):
  `Twoi klienci pytają ChatGPT, Gemini i Perplexity o polecenie firmy, produktu czy specjalisty. Audyt widoczności w AI pokazuje, co asystenci mówią o Twojej marce dziś, a wdrożenie GEO (Generative Engine Optimization) sprawia, że zaczynają Cię polecać. Pracujemy zdalnie z firmami z całej Polski.`

### 1.3 Nowa sekcja po sekcji „SEO to już za mało…” (H2)

H2: `Czym jest GEO i czym różni się od SEO?`

Treść:

`GEO (Generative Engine Optimization), nazywane też pozycjonowaniem w ChatGPT, to dostosowanie strony i informacji o firmie tak, żeby asystenci AI mogli je zrozumieć, uznać za wiarygodne i zacytować w odpowiedzi.`

`SEO walczy o miejsce na liście linków w Google. GEO walczy o miejsce w jednej odpowiedzi, którą dostaje użytkownik ChatGPT, Gemini, Perplexity czy Google AI Overviews. Obie dziedziny korzystają z tych samych fundamentów: szybkiej strony, jasnej struktury i danych strukturalnych. GEO dokłada do tego treści pisane tak, żeby dało się je przytoczyć, spójne dane o firmie w całej sieci oraz regularne sprawdzanie, co modele mówią o marce.`

Pod spodem krótka lista (użyj istniejącego stylu listy):
- `Audyt widoczności w AI: testujemy setki zapytań w ChatGPT, Gemini, Perplexity, Claude i Google AI Overviews.`
- `Wdrożenie GEO: dane strukturalne JSON-LD, treści gotowe do cytowania, plik llms.txt.`
- `Monitoring: co miesiąc sprawdzamy, czy i jak AI poleca Twoją firmę.`

Linki wewnętrzne w tej sekcji: „dane strukturalne JSON-LD” → wpis `/blog/jak-json-ld-zwieksza-widocznosc-w-wyszukiwarkach-ai`, „plik llms.txt” → wpis `/blog/czy-llms-txt-pomoze-ai-zrozumiec-twoja-strone-lepiej` (sprawdź canonicale i użyj dokładnych adresów).

### 1.4 Złagodzenie obietnic (przegląd marki)

Zamień sformułowania, których nie da się zagwarantować:

| Obecnie | Zamień na |
| --- | --- |
| `Zdominuj rekomendacje AI` | `Zwiększ szansę na rekomendację w AI` |
| `Kontroluj swój przekaz w 100%` | `Popraw to, co AI mówi o Twojej firmie` |
| `Pełna dominacja.` (pakiet Lider AI) | `Najpełniejszy pakiet.` |
| `…budujemy autorytet, który sprawia, że AI nie wyobraża sobie tej branży bez Twojej firmy.` | `…wzmacniamy sygnały, które zwiększają szansę, że następną rekomendacją będzie Twoja firma.` |
| `Chcę zdominować AI w swojej branży` | `Chcę wyprzedzić konkurencję w AI` |
| `Przejęcie pozycji konkurencji` | `Analiza pozycji konkurencji` |

Ceny pakietów zostają bez zmian.

### 1.5 Case BDental

Pod obecnym opisem dodaj jedno zdanie metodyki (jeśli w repo lub w artykule `/blog/jak-json-ld-zwieksza-widocznosc-w-wyszukiwarkach-ai` jest data testu i lista modeli, użyj ich; jeśli nie, zostaw TODO):

`Test objął 10 zapytań o stomatologię w regionie, sprawdzanych w [modele] w [miesiąc rok].`

### 1.6 Nowe pytania w FAQ (dodaj na początku listy FAQ)

1. **Co to jest GEO?**
   `GEO (Generative Engine Optimization) to optymalizacja strony i informacji o firmie pod asystentów AI, takich jak ChatGPT, Gemini czy Perplexity. Celem jest to, żeby AI rozumiało, czym się zajmujesz, i polecało Twoją firmę w odpowiedziach.`

2. **Ile kosztuje pozycjonowanie w ChatGPT?**
   `Audyt i wdrożenie podstaw zaczynają się od 490 PLN netto jednorazowo. Pakiet z treściami gotowymi do cytowania kosztuje 1 490 PLN netto, a pełny pakiet z analizą konkurencji 3 490 PLN netto. Monitoring miesięczny wyceniamy osobno.` (link „Zobacz pakiety” do sekcji pakietów na tej stronie, kotwica jak istnieje)

3. **Czy obsługujecie firmy z mojego miasta?**
   `Tak. Cały audyt i wdrożenie prowadzimy zdalnie, więc pracujemy z firmami z całej Polski, od małych gabinetów po sklepy internetowe. Przykładem jest klinika BDental z Gliwic, dla której asystenci AI zaczęli wskazywać ją jako pierwszą rekomendację w 7 na 10 testowanych zapytań.`

4. **Czy da się zmierzyć widoczność w AI?**
   `Tak. Testujemy stały zestaw zapytań, które zadają Twoi klienci, w każdym z asystentów osobno i zapisujemy, czy Twoja firma się pojawia, na którym miejscu i w jakim kontekście. Powtarzamy test co miesiąc, więc widać zmianę w czasie.`

Pytanie „Mam już SEO. Po co mi to?” zostaje, ale dopisz na końcu odpowiedzi: `SEO i GEO się uzupełniają: dobre SEO ułatwia wdrożenie GEO, ale go nie zastępuje.`

Zaktualizuj JSON-LD `FAQPage`.

---

## Część 2: poprawa CTR wpisów z pierwszej dziesiątki

Oba wpisy są już na pozycjach 7–10, ale mało kto w nie klika. Zmieniamy tylko meta i pierwsze zdanie wpisu. Zanim zmienisz, przeczytaj wpis i sprawdź, czy nowy tytuł i opis są zgodne z treścią. Jeśli wpis czegoś nie omawia, dostosuj opis do faktycznej treści i napisz mi, co zmieniłeś.

### 2.1 `blog/jak-tworzy-sie-strony-internetowe-w-2026`

GSC: pozycja 9,4, 256 wyświetleń, 3 kliknięcia. Zapytania: „tworzenie stron internetowych 2026”, „word press 2026”.

- `<title>`: `Jak tworzy się strony internetowe w 2026? WordPress, AI czy kod`
- `meta description`: `Porównujemy trzy drogi do nowej strony: WordPress, kreatory AI i lekki kod. Koszt, szybkość, SEO i kiedy które rozwiązanie ma sens.`
- H1 zostaw, jeśli zawiera frazę „strony internetowe w 2026”. Pierwsze zdanie wpisu ma odpowiadać wprost na pytanie z tytułu w 1–2 zdaniach (definicja/odpowiedź na początku, potem rozwinięcie).

### 2.2 `blog/wyciek-danych-medycznych-piksel-meta-ga4-klinika`

GSC: pozycja 7,2, 146 wyświetleń, 3 kliknięcia. Zapytania związane z MyDr, wyciekiem i UODO.

- `<title>`: `Wyciek z MyDr nie był jedyny: piksel Meta i GA4 w klinice`
- `meta description`: `Piksel Meta i GA4 na stronie kliniki mogą przekazywać dane o zdrowiu pacjentów. Sprawdź, jak to wykryć, co mówi RODO i jak skonfigurować tracking bezpiecznie.`
- Na końcu wpisu dodaj CTA (w stylu istniejących przycisków): `Sprawdzimy, jakie dane wysyła Twoja strona` → `/kontakt`.
- Nie zmieniaj opisu faktów dotyczących MyDr.

---

## Część 3: odświeżenie dwóch wpisów z potencjałem

### 3.1 Wpis o llms.txt: `blog/czy-llms-txt-pomoze-ai-zrozumiec-twoja-strone-lepiej`

GSC: pozycja 22, 150 wyświetleń, 0 kliknięć. Zapytania: „llms.txt co to” (62 wyświetlenia), „co to jest llms.txt i jak go wdrożyć”, „llms txt”, „robots.txt llms”.

- `<title>`: `Co to jest llms.txt i jak go wdrożyć? Przykład i instrukcja`
- `meta description`: `llms.txt to plik, który podpowiada modelom AI, co jest najważniejsze na Twojej stronie. Wyjaśniamy, jak działa, czym różni się od robots.txt i jak go wdrożyć.`
- Tuż pod H1 dodaj akapit-definicję (2 zdania, pogrubione pierwsze zdanie):
  `**llms.txt to plik tekstowy w formacie Markdown umieszczany w głównym katalogu strony (np. twojadomena.pl/llms.txt), który w skrócie opisuje firmę i wskazuje najważniejsze podstrony dla modeli językowych.** To propozycja standardu, a nie oficjalny wymóg wyszukiwarek, więc traktuj go jako uzupełnienie danych strukturalnych, a nie ich zamiennik.`
- Dodaj sekcje (pomiń te, które już są we wpisie; nie powtarzaj treści):
  - H2 `Przykład pliku llms.txt` z blokiem kodu z prostym przykładem (nagłówek H1 z nazwą firmy, cytat z opisem, sekcje z listą linków do kluczowych podstron). Jako przykład użyj fikcyjnej firmy, nie Collytics.
  - H2 `llms.txt a robots.txt: czym się różnią?` Krótko: robots.txt mówi robotom, czego nie wolno indeksować; llms.txt podpowiada modelom, co jest najważniejsze i jak to rozumieć. Jeden nie zastępuje drugiego.
  - H2 `Jak wdrożyć llms.txt krok po kroku` (numerowana lista: przygotuj opis firmy, wybierz 5–15 kluczowych podstron, zapisz plik jako llms.txt w katalogu głównym, sprawdź dostępność pod adresem, aktualizuj przy zmianach oferty).
  - H2 `Najczęstsze pytania` z 3 pytaniami (Czy Google korzysta z llms.txt? – odpowiedź ostrożna: brak potwierdzenia, że główne wyszukiwarki używają go do rankingu; Czy llms.txt zastępuje dane strukturalne? – nie; Czy mała firma potrzebuje llms.txt? – jako tani dodatek tak, ale ważniejsze są JSON-LD i spójne informacje o firmie). Dodaj JSON-LD `FAQPage` dla tych pytań.
- Na końcu CTA do `/audyt-widocznosci-ai`: `Chcesz sprawdzić, jak AI widzi Twoją stronę? Zobacz Audyt Widoczności AI.`
- Jeśli w katalogu głównym repo nie ma `llms.txt`, utwórz go dla Collytics (opis firmy z obecnej strony głównej, linki do: strony głównej, /services, /google-ads, /audyt-widocznosci-ai, /use-case-lab-wet, /blog/, /kontakt). Bez adresu pocztowego. We wpisie dodaj zdanie: `Nasz własny plik znajdziesz pod adresem collytics.io/llms.txt.`

### 3.2 Wpis o GTM w WordPress: `blog/google-tag-manager-w-wordpress-jak-zainstalowac`

GSC: pozycja 31, 215 wyświetleń, 6 kliknięć. Zapytania: „instalacja google tag manager”, „google tag manager wordpress”, „wordpress google tag manager”, „gtm4wp”, „tag manager wordpress”, „konsultacje google tag manager”, „wdrożenie google tag manager”.

- `<title>`: `Google Tag Manager w WordPress: 3 sposoby instalacji (2026)`
- `meta description`: `Jak zainstalować Google Tag Manager w WordPress? Wtyczka GTM4WP, Site Kit lub kod w functions.php. Instrukcja krok po kroku, test działania i najczęstsze błędy.`
- Upewnij się, że wpis zawiera (dodaj brakujące, nie powtarzaj istniejących):
  - Krótką odpowiedź na początku: trzy sposoby i który wybrać.
  - H2 `Sposób 1: wtyczka GTM4WP` (instalacja, wklejenie ID kontenera, gdzie w ustawieniach).
  - H2 `Sposób 2: Site Kit by Google`.
  - H2 `Sposób 3: kod w functions.php motywu potomnego` z blokiem kodu PHP, który dodaje skrypt GTM w `wp_head` i fragment noscript w `wp_body_open`, z `GTM-XXXXXXX` jako placeholderem. Dodaj uwagę, żeby edytować motyw potomny.
  - H2 `Jak sprawdzić, czy GTM działa` (tryb podglądu w GTM / Tag Assistant).
  - H2 `Najczęstsze błędy` (podwójny kod GA4: z wtyczki i z GTM; brak fragmentu w body; brak Consent Mode v2; kontener zainstalowany dwa razy).
  - H2 `Najczęstsze pytania` z 3 pytaniami i JSON-LD `FAQPage`.
- Link wewnętrzny do wpisu `/blog/google-tag-manager-kompleksowy-przewodnik` (dla czytelników, którzy chcą poznać GTM szerzej) i odwrotnie: z przewodnika dodaj link do tego wpisu przy wzmiance o instalacji. Dzięki temu wpisy nie będą ze sobą konkurować.
- Na końcu CTA: `Wolisz, żebyśmy wdrożyli GTM i GA4 za Ciebie? Napisz do nas.` → `/kontakt`.

---

## Na koniec

- Push brancha `content/seo-2026-10` i Pull Request z listą zmian w trzech częściach.
- Wypisz wszystkie TODO i miejsca, w których dostosowałeś tekst do faktycznej treści wpisu.
