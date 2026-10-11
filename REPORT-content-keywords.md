# Content & Keyword Strategy: Polish Gas-Services Domain (from live autocomplete data)

**Date:** 2026-10-11 · **Market:** Poland (PL) · **Business:** new one-person gas-services company, fresh domain, site not yet built
**Data basis:** `data/all_suggestions.tsv` — 752 rows, 18 seeds, 630 unique suggestions, live-fetched from Google autocomplete (client=firefox JSON endpoint) on 2026-10-11. 131 raw JSON responses kept in `data/q_*.json`.
**Evidence rules:** every dataset-derived statement is marked **[verified]** (it exists verbatim in the fetched TSV). Judgment calls are **[inference]** or **[assessment]**. External facts not fetched this session are **[claim, unverified]**. **No search volumes exist anywhere in this report** — no volume API was used; autocomplete rank is the only demand proxy (see §1.3).

Cross-references: `REPORT-local-seo-technical.md` (GBP, schema, NAP), `REPORT-launch-roadmap.md` (domain/hosting/90-day plan), `REPORT-seo-tool-architecture.md` (GSC quotas, stack).

---

## 0. TL;DR — decisions this data supports

1. **Build service pages around the four big money clusters that autocomplete actually returns:** serwis/przegląd kotła gazowego, montaż + wymiana kotła, przyłącze gazowe/gazu, projekt + instalacja gazowa (w domu). [verified — all are seed groups with dense suggestions in the TSV]
2. **Do NOT target the bare seed "instalacja gazowa".** Of its 250 suggestions, ~108 are automotive LPG (samochód, BRC, STAG, KME, Prins, diesle, specific car models) — the head term is intent-poisoned. Target "instalacja gazowa w domu" and "projekt instalacji gazowej" instead. [verified counts; assessment for the strategy]
3. **The deepest question vein is procedural/legal, not pricing:** 85 unique question-form suggestions (25× "czy…", 15× "jak…", 45× "ile…") dominate with "czy przyłącze gazowe wymaga pozwolenia na budowę", "czy kotłownia gazowa może być w piwnicy/garażu", "czy serwis kotła gazowego jest obowiązkowy". These are FAQ/HowTo fuel. [verified]
4. **Emergency intent ("gaz śmierdzi co robić"-type) is ABSENT from the dataset.** No smell-of-gas, leak, or panic query appears in any of the 630 unique suggestions. An emergency page is still recommended for service reasons, but it is **not** autocomplete-supported demand. [verified absence; inference for the recommendation]
5. **Price demand concentrates on przyłącze + kocioł, not on a generic "cennik usług gazowych"** — that seed returned exactly 1 suggestion (itself). Price content should live *inside* service pages, not on one price-list page. [verified; assessment]
6. **Brand modifiers are a real underserved layer:** 26 distinct brands appear in suggestions; boiler brands (Viessmann, Junkers, Immergas, Termet, Vaillant, De Dietrich, Buderus, Beretta, Saunier Duval, Ferroli, Wolf, Ariston, Bosch, Brötje) attach to serwis/przegląd/czyszczenie. [verified]

---

## 1. Method — what this dataset is and what it can and cannot tell you

### 1.1 How the data was collected [verified]

- Script: `fetch_suggest.py` in this repo. Endpoint: `https://suggestqueries.google.com/complete/search?client=firefox&hl=pl&q=<urlencoded-seed>` (plain JSON, no API key).
- Two passes per topic: (a) the bare seed (top-10 suggestions, roughly popularity-ordered), and (b) **alphabet expansion** — seed + " a"…"z" (and some seed + " <word>" prefixes like "serwis kotła gazowego cena") to surface the long tail. That's why e.g. `instalacja gazowa` has 250 rows and `cennik usług gazowych` has 1.
- 131 raw JSON responses in `data/q_*.json`; flattened, deduplicated into `data/all_suggestions.tsv` (columns: seed_group, queried, suggestion).

### 1.2 What autocomplete DOES tell you [verified methodology, assessment for weight]

- That real Polish users type a phrase (or a prefix of it) — every suggestion line corresponds to actual query traffic Google deems worth suggesting.
- The **shape** of demand: which modifiers attach to a seed (cena/koszt, wymagania, przepisy, city, brand, question words).
- Relative salinity of topics: seeds that survive alphabet expansion with hundreds of variants (przyłącze gazowe: 191 rows) have far richer query ecosystems than seeds that don't (konserwacja kotła gazowego: 3 rows).
- Question language: the exact "czy/jak/ile" phrasings users type — free FAQ mining.
- Cross-seed confirmation: 91 suggestions were returned under more than one queried prefix (e.g. "kotłownia gazowa w bloku" appeared 3×). Duplicates across different prefixes are a stronger signal than one-off appearances. [verified]

### 1.3 What autocomplete does NOT tell you [verified — these limits are structural]

- **No volumes.** Autocomplete returns no counts. "Higher in the bare-seed list" is a *rough* popularity proxy only, and the list is personalized/localized/filtered by Google's systems (offensive and policy-sensitive suggestions are suppressed — [claim, unverified], Google doesn't document the filter in detail). Ranking within expanded lists is especially unreliable.
- **No seasonality, no trend, no conversion data.** A suggestion can be typed 50×/day or 5×/year.
- **Selection bias:** autocomplete surfaces *typable prefixes* — long, low-frequency phrasings never appear; niche-but-commercial queries with no prefix mass stay invisible.
- **It is not a keyword research tool.** Treat it as: (1) intent mapping, (2) FAQ harvesting, (3) URL-taxonomy scaffolding. Volume checks must come later from GSC's own data once the site has impressions (§7) — which is free and first-party.
- **Poland-wide, not city-level.** City modifiers visible in the data (§3.7) show where autocomplete mass exists nationally; they are not a substitute for local SERP checks.

### 1.4 Dataset stats [verified]

- 752 rows · 18 seed groups · 630 unique suggestions · 122 duplicate rows (same suggestion from multiple prefixes).
- Rows per seed group: instalacja gazowa 250 · przyłącze gazowe 191 · kotłownia gazowa 141 · serwis kotła gazowego 57 · 10 each for: serwis kotłów, montaż kotła gazowego, wymiana kotła gazowego, przegląd kotła gazowego, instalacja gazowa w domu, projekt instalacji gazowej, przyłącze gazu, czyszczenie kotła gazowego, ile kosztuje serwis kotła · ile kosztuje przyłącze gazu 9 · regulacja palnika gazowego 6 · ile kosztuje montaż kotła gazowego 4 · konserwacja kotła gazowego 3 · cennik usług gazowych 1.
- Question-form suggestions: 85 unique (45× "ile…", 25× "czy…", 15× "jak…").
- City-mentioning suggestions: 38 across 16 cities (Warszawa 6, Kraków 7, Poznań 3, Wrocław 3, Rzeszów 3, and 1–2 each elsewhere).
- Brand-mentioning suggestions: 111+ rows covering 26 distinct brands.

---

## 2. Seed → notable suggestions (top-20 table)

Notable = commercially or structurally most informative suggestions actually returned. Order ≈ frequency of appearance across prefix expansions in our data (rows), which is *our only* salinity proxy. [verified — all strings verbatim from the TSV]

| # | Seed / group | Rows | Notable suggestions (verbatim) |
|---|---|---|---|
| 1 | instalacja gazowa ⚠ | 250 | instalacja gazowa do domu · …do domu koszt · …na zgłoszenie · …z miedzi · …w mieszkaniu w bloku · ⚠ dominated by automotive: brc cena, stag 4, kme, prins, audi q5, golf 4 1.6, do diesla |
| 2 | przyłącze gazowe | 191 | …od skrzynki do domu koszt · …pozwolenie czy zgłoszenie · …cena za metr · …sąsiada na mojej działce · …a ulga termomodernizacyjna · …jak uzyskać · …odległość od granicy działki |
| 3 | kotłownia gazowa | 141 | …powyżej 60 kw wymagania · …wymagania ppoż · …w piwnicy · …w garażu · …musi mieć okno · …wentylacja mechaniczna · …w bloku hałas · …warunki techniczne |
| 4 | serwis kotła gazowego | 57 | …viessmann · …junkers · …immergas · …termet · …vaillant · …de dietrich · czy serwis kotła gazowego jest obowiązkowy · …na czym polega · …stawka vat · + 12 city variants (kraków, poznań, wrocław, rzeszów, szczecin, opole…) |
| 5 | serwis kotłów | 10 | serwis kotłów gazowych · …termet · …de dietrich · …immergas · …viessmann · …na pellet · …na ekogroszek |
| 6 | montaż kotła gazowego | 10 | …cena · …cena robocizny · …kondensacyjnego cena · …dwufunkcyjnego cena · …z zasobnikiem cena · …w łazience · …stawka vat |
| 7 | wymiana kotła gazowego | 10 | …cena · …dofinansowanie · …na kondensacyjny · …a ulga termomodernizacyjna · …na pompę ciepła · …na pompę ciepła dofinansowanie |
| 8 | przegląd kotła gazowego | 10 | …cena · …co ile · …protokół · …przepisy · …jaki paragraf · …viessmann · …junkers · …immergas |
| 9 | instalacja gazowa w domu | 10 | …cena · …schemat · …ze zbiornikiem · …jednorodzinnym koszt · …jakie rury · …przepisy |
| 10 | projekt instalacji gazowej | 10 | …cena · …w domu jednorodzinnym · …pdf · …po nowemu · …zewnętrznej · …na zgłoszenie · …wroclaw |
| 11 | przyłącze gazu | 10 | …od skrzynki do domu · …od skrzynki do domu cena · …do działki · …pgnig · …do domu jednorodzinnego |
| 12 | ile kosztuje serwis kotła | 10 | …kondensacyjnego · …na pellet · …olejowego · …viessmann · …junkers · …immergas · …vaillant |
| 13 | ile kosztuje przyłącze gazu | 9 | …do domu · …od skrzynki do domu · …od skrzynki do domu 2025 · …do działki · …ziemnego · …do mieszkania · …100m |
| 14 | czyszczenie kotła gazowego | 10 | …termet · …vaillant · …buderus · …junkers · …viessmann · …cena · …de dietrich · …ariston · …immergas |
| 15 | regulacja palnika gazowego | 6 | …amica · …beko · …riello · …grilla gazowego · …kotła gazowego |
| 16 | ile kosztuje montaż kotła gazowego | 4 | …dwufunkcyjnego · …z zasobnikiem · …kondensacyjnego |
| 17 | konserwacja kotła gazowego | 3 | …cena · …jaki vat |
| 18 | cennik usług gazowych | 1 | (only the seed itself — weakest ecosystem in the dataset) |
| 19 | (cross-cutting) "ile…" questions | 45 | ile kosztuje przyłącze gazu od skrzynki do domu 2025 · ile kosztuje instalacja gazowa w domu jednorodzinnym · ile trwa serwis kotła gazowego |
| 20 | (cross-cutting) "czy…/jak…" questions | 40 | czy przyłącze gazowe wymaga pozwolenia na budowę · czy kotłownia gazowa może być w piwnicy · jak sprawdzić czy instalacja gazowa jest szczelna · jak przyspieszyć przyłącze gazowe |

⚠ = intent-polluted head term, see §3.5.

---

## 3. Cluster analysis → money / service / informational / emergency

Cluster assignment is **[inference]** from the literal strings (a query containing "cena" is buying-intent; containing "czy wymaga pozwolenia" is pre-purchase informational); the underlying strings are **[verified]**.

### 3.1 Money cluster (buyer has or will have a project; page = service + price)

- **przyłącze gazowe / przyłącze gazu — the single biggest money cluster.** "ile kosztuje przyłącze gazu" ×9 variants (do domu, od skrzynki do domu +2025, do działki, ziemnego, do mieszkania, 100m), "przyłącze gazowe cena za metr", "przyłącze gazowe od skrzynki do domu koszt", "przyłącze gazowe cennik". [verified]
- **montaż/wymiana kotła gazowego — price-saturated.** "montaż kotła gazowego cena", "…cena robocizny", "…dwufunkcyjnego cena", "…kondensacyjnego cena", "…z zasobnikiem cena", "wymiana kotła gazowego cena", "…cena robocizny". Users are price-shopping *configurations* (dwufunkcyjny vs z zasobnikiem vs kondensacyjny) — the page must differentiate by config. [verified]
- **serwis/przegląd/konserwacja + cena:** "ile kosztuje serwis kotła gazowego" (+ per-brand: viessmann, junkers, immergas, termet, vaillant), "przegląd kotła gazowego cena", "konserwacja kotła gazowego cena". [verified]
- **projekt instalacji gazowej cena** — people buying the design step. [verified]

### 3.2 Service cluster (recurring / relationship work; page = service page + trust)

- **serwis kotła gazowego** — 57 rows, brand-split, 12 city variants, plus "…na czym polega", "ile trwa serwis kotła gazowego". This is the core annuity service for a one-person business. [verified]
- **przegląd kotła gazowego** — legal-obligation flavor: "co ile", "protokół", "przepisy", "jaki paragraf", "czy serwis kotła gazowego jest obowiązkowy". Buyers need the compliance story before they book. [verified]
- **czyszczenie kotła gazowego** — 10 brand variants; near-synonym of konserwacja for users. Fold as a section of serwis, or a thin subpage. [verified strings; assessment for folding]
- **regulacja palnika gazowego** — 6 rows, mostly kitchen-stove brands (amica, beko) + grilla. Off-target for a boiler business; ignore or one FAQ line. [verified; assessment]

### 3.3 Informational cluster (research / compliance; pages = pillar + FAQ)

- **kotłownia gazowa wymagania** — the richest informational vein: "powyżej 60 kw wymagania", "do 30 kw wymagania", "wymagania ppoż", "czy musi mieć okno", "czy może być w piwnicy / w garażu", "wentylacja mechaniczna", "warunki techniczne", "drzwi wymagania", "na poddaszu", "na piętrze", "komin", "minimalna powierzchnia", "ile m2". This is a pillar page. [verified]
- **Formalities:** "czy przyłącze gazowe wymaga pozwolenia na budowę", "…pozwolenie czy zgłoszenie", "przyłącze gazowe formalności", "…gdzie zgłosić", "…wniosek online", "instalacja gazowa na zgłoszenie", "projekt instalacji gazowej na zgłoszenie". [verified]
- **Money-tax intersections:** "czy przyłącze gazowe można odliczyć od podatku", "przyłącze gazowe a ulga termomodernizacyjna", "opłata za przyłącze gazowe a środek trwały", "wymiana kotła gazowego dofinansowanie", "…na pompę ciepła dofinansowanie", "montaż kotła gazowego stawka vat", "serwis kotła gazowego stawka vat", "przyłącze gazowe stawka vat". High pre-purchase value. [verified]
- **Tech how-to:** "instalacja gazowa w domu jakie rury", "…z czego", "przyłącze gazowe jaka rura", "…na jakiej głębokości", "przyłącze gazowe głębokość", "jak sprawdzić czy instalacja gazowa jest szczelna". [verified]

### 3.4 Emergency cluster — ABSENT [verified absence]

- Zero suggestions contain: śmierdzi, ulatuje, wyciek, awaria, gaz wyłączyć, zadymienie, alarm. The dataset was mined across 18 seeds + alphabet; emergency phrasings simply do not surface in this sampling.
- Interpretation: people in a gas-emergency either type very short queries autocomplete filters differently, or go straight to calling 998/112 or the pogotowie gazowe (992) — they don't browse. [assessment]
- **Decision:** ship ONE safety/emergency page (awaria, wyciek, śmierdzi → zakręcić, wietrzyć, nie włączać światła, zadzwonić 992, potem nasz numer) because it is a service duty and trust asset — but do NOT count it in SEO projections, and do not spend link equity on it. [inference]

### 3.5 The automotive-LPG pollution problem [verified counts / assessment for strategy]

- Bare seed "instalacja gazowa": 250 suggestions, of which ~108 are automotive (BRC, STAG, KME, Prins, Landi Renzo, Lovato, Elpigaz, Zenit, Zavoli, Europegas, Bormech, Stako; car models from Fiat Panda to Dodge Durango; "do diesla", "czy niszczy silnik", "w aucie jest bezpieczna"). Only ~29 are clearly home/installation queries.
- Consequence: the head term mixes two unrelated markets. A new domain ranking page for "instalacja gazowa" would fight LPG-installation shops and attract wrong-intent visitors.
- **Strategy:** never target bare "instalacja gazowa"; build on "instalacja gazowa w domu", "projekt instalacji gazowej", "przyłącze gazowe". Use "instalacja gazowa (LPG samochodowa)" only inside a one-paragraph disambiguation note if at all. [assessment]

### 3.6 Brand modifiers [verified]

- Boiler brands attaching to serwis/przegląd/czyszczenie: Viessmann (6), Immergas (5), De Dietrich (4), Junkers (3), Termet (3), Vaillant (2), Buderus (2), Ariston (2), Saunier Duval, Ferroli, Wolf, Beretta, Bosch, Brötje (1 each). Termet's presence is a PL-market tell (domestic brand).
- Automotive brands (STAG 14, BRC 9, KME 8, Prins 7…) all belong to the polluted seed — ignore.
- Play: each service page gets a brand strip ("serwis: Viessmann · Vaillant · Junkers · Immergas · Termet · De Dietrich…") + per-brand H3 or FAQ line. These are long-tail, low-competition, high-conversion entries. [assessment]

### 3.7 City modifiers [verified]

- 38 city suggestions across 16 cities; densest for serwis kotła gazowego (kraków, poznań, wrocław, rzeszów, szczecin, opole, międzyrzecz, nowy sącz, zdunska wola) and przyłącze gazowe (warszawa, kraków, poznań, wrocław, radom, lublin, olsztyn, białystok, bydgoszcz, gdańsk + small towns: legionowo, grodzisk mazowiecki, zgierz, kutno, ostrołęka, stryków, garwolin, gniezno).
- These are national autocomplete patterns, NOT evidence about the user's city. Local pages follow the GBP/service-area strategy in `REPORT-local-seo-technical.md` §1–2; use this list only as inspiration for which `<miasto>` modifiers have proven autocomplete mass. [assessment]

---

## 4. URL map: page → target seed → supporting queries → schema

Slugs in Polish, ASCII-transliterated (schema.org types chosen per `REPORT-local-seo-technical.md` §4). All seeds/queries verbatim from dataset [verified]; page-to-keyword assignment is [assessment].

| URL | Target seed | Supporting queries (from data) | Schema |
|---|---|---|---|
| `/` (home) | brand + "instalacje gazowe <miasto>" | (brand seed absent from data — see §3.7 note) | LocalBusiness (+areaServed) |
| `/serwis-kotla-gazowego/` | serwis kotła gazowego | serwis kotła gazowego viessmann/junkers/immergas/termet/vaillant/de dietrich · ile kosztuje serwis kotła gazowego · co ile · na czym polega · ile trwa · stawka vat · czy serwis kotła gazowego jest obowiązkowy | Service + FAQPage |
| `/przeglad-kotla-gazowego/` | przegląd kotła gazowego | …cena · co ile · protokół · przepisy · jaki paragraf · czy obowiązkowy | Service + FAQPage |
| `/montaz-kotla-gazowego/` | montaż kotła gazowego | …cena · cena robocizny · dwufunkcyjnego cena · kondensacyjnego cena · z zasobnikiem cena · w łazience · stawka vat | Service + FAQPage |
| `/wymiana-kotla-gazowego/` | wymiana kotła gazowego | …cena · dofinansowanie · na kondensacyjny · a ulga termomodernizacyjna · na pompę ciepła (+ dofinansowanie) | Service + FAQPage |
| `/przylacze-gazowe/` | przyłącze gazowe (+ przyłącze gazu) | …od skrzynki do domu (cena) · pozwolenie czy zgłoszenie · krok po kroku · cena za metr · sąsiada na mojej działce · ile kosztuje przyłącze gazu do domu/działki/100m | Service + FAQPage + HowTo |
| `/projekt-instalacji-gazowej/` | projekt instalacji gazowej | …cena · w domu jednorodzinnym (cena) · na zgłoszenie · zewnętrznej · pdf | Service |
| `/instalacja-gazowa-w-domu/` | instalacja gazowa w domu | …cena · schemat · ze zbiornikiem · jakie rury · przepisy · jednorodzinnym koszt | Service + FAQPage |
| `/kotlownia-gazowa-wymagania/` | kotłownia gazowa (wymagania) | powyżej 60 kw wymagania · ppoż · okno · piwnica · garaż · wentylacja · warunki techniczne · minimalna powierzchnia · czy musi być wydzielona pożarowo | Article + FAQPage |
| `/cennik/` | (weak) cennik usług gazowych + ile-kosztuje cluster | konserwacja kotła gazowego cena · czyszczenie kotła gazowego cena · regulacja… cena | Service (offers/OfferCatalog) + FAQPage |
| `/awaria-gazowa/` | (none in data — §3.4) | — | Article |
| `/o-mnie/` `/kontakt/` | brand/trust | — | AboutPage / ContactPage |

Not built: any automotive-LPG page; "regulacja palnika gazowego" (kitchen-stove intent) unless the business actually serves stoves. [assessment]

---

## 5. Content briefs — 5 highest-intent pages

Selection rationale [assessment]: (a) biggest autocomplete ecosystems that are home-domain, (b) money intent, (c) recurring-revenue services. Every H2/H3 below is a real suggestion or a question suggestion from the TSV [verified] — headings can be near-verbatim because they match typed queries.

### 5.1 `/serwis-kotla-gazowego/` — the annuity page

- **H1:** Serwis kotła gazowego — co obejmuje, ile kosztuje, jak często
- **Sections (from real queries):**
  - "Na czym polega serwis kotła gazowego" — step list of an actual visit (verified query: serwis kotła gazowego na czym polega)
  - "Ile kosztuje serwis kotła gazowego" — price table per scope; note stawka VAT (verified: serwis kotła gazowego stawka vat, konserwacja kotła gazowego jaki vat)
  - "Co ile lat / jak często" (verified: serwis kotła gazowego co ile, przegląd kotła gazowego co ile — cross-link to 5.2)
  - "Ile trwa serwis kotła gazowego" (verified)
  - "Czy serwis kotła gazowego jest obowiązkowy" + "Czy serwis gwarancyjny kotła gazowego jest płatny" (both verified — manufacturer-warranty angle)
  - Brand block, one short H3 each: Viessmann, Vaillant, Junkers, Immergas, Termet, De Dietrich (all verified modifiers)
  - CTA: phone + form ("umów termin serwisu")
- **FAQ schema:** the 4 question headings above.
- **Internal links:** → `/przeglad-kotla-gazowego/`, `/montaz-kotla-gazowego/`, `/awaria-gazowa/`.

### 5.2 `/przylacze-gazowe/` — the biggest, most question-dense money page

- **H1:** Przyłącze gazowe — koszt, formalności i wykonanie krok po kroku
- **Sections:**
  - "Ile kosztuje przyłącze gazu" — sub-breaks exactly as searched: do domu · od skrzynki do domu · do działki · cena za metr · (verified ×13 variants)
  - "Pozwolenie czy zgłoszenie" (verified: przyłącze gazowe pozwolenie czy zgłoszenie, czy przyłącze gazowe wymaga pozwolenia na budowę, czy przyłącze gazowe wymaga zgłoszenia)
  - "Krok po kroku" — wniosek → projekt → wykonawca → odbiór (verified: przyłącze gazowe krok po kroku, wniosek online, gdzie zgłosić, kto wykonuje, od czego zacząć, mam przyłącze gazowe co dalej)
  - "Odległości i warunki techniczne" (verified: odległości od innych instalacji, odległość od granicy działki, na jakiej głębokości, głębokość)
  - "Przyłącze gazowe sąsiada na mojej działce" + "zgoda sąsiada" (verified — standalone H2, zero competition likely)
  - "Podatki i ulgi" (verified: czy przyłącze gazowe można odliczyć od podatku, a ulga termomodernizacyjna, a środek trwały, a podatek od nieruchomości)
  - "Jak przyspieszyć przyłącze gazowe" (verified — golden differentiator)
- **Schema:** Service + FAQPage + HowTo (the krok-po-kroku section).
- **Internal links:** → `/projekt-instalacji-gazowej/`, `/instalacja-gazowa-w-domu/`, `/cennik/`.

### 5.3 `/montaz-kotla-gazowego/` — configuration-shopping page

- **H1:** Montaż kotła gazowego — ceny za każdy typ montażu
- **Sections (each price query = its own H2):**
  - "Ile kosztuje montaż kotła gazowego" (verified)
  - "Kocioł dwufunkcyjny vs z zasobnikiem vs kondensacyjny — cena" (verified: montaż kotła gazowego dwufunkcyjnego cena, z zasobnikiem cena, kondensacyjnego cena)
  - "Cena robocizny — co wchodzi w cenę" (verified: montaż kotła gazowego cena robocizny)
  - "Czy kocioł gazowy może stać w łazience" (verified: montaż kotła gazowego w łazience — legal answer + link to kotłownia page)
  - "Stawka VAT" (verified)
  - "Ile kosztuje serwis po montażu" — planting the annuity (cross-link 5.1)
- **Schema:** Service + FAQPage.
- **Internal links:** → `/wymiana-kotla-gazowego/`, `/serwis-kotla-gazowego/`, `/kotlownia-gazowa-wymagania/`.

### 5.4 `/wymiana-kotla-gazowego/` — the subsidy-flavored upgrade page

- **H1:** Wymiana kotła gazowego na nowy — ceny, dofinansowanie, ulga termomodernizacyjna
- **Sections:**
  - "Ile kosztuje wymiana kotła gazowego" (verified: cena, cena robocizny, na nowy)
  - "Wymiana starego kotła na kondensacyjny" (verified: wymiana kotła gazowego na kondensacyjny)
  - "Dofinansowanie i ulga termomodernizacyjna" (verified: wymiana kotła gazowego dofinansowanie, a ulga termomodernizacyjna)
  - "Wymiana kotła gazowego na pompę ciepła" + "dofinansowanie" (verified ×2 — capture exit-intent instead of losing the visitor)
  - "Kiedy wymiana = przegląd za dużo" — honest triage to serwis (trust play)
- **Schema:** Service + FAQPage.
- **Internal links:** → `/montaz-kotla-gazowego/`, `/serwis-kotla-gazowego/`.

### 5.5 `/przeglad-kotla-gazowego/` — compliance-driven recurring booking

- **H1:** Przegląd kotła gazowego — terminy, protokół i cena
- **Sections:**
  - "Co ile lat przegląd kotła gazowego" (verified: przegląd kotła gazowego co ile)
  - "Czy przegląd jest obowiązkowy — jaki paragraf" (verified: przegląd kotła gazowego jaki paragraf, przepisy) — cite the actual rozporządzenie; do NOT paraphrase from memory, verify text before publishing [assessment]
  - "Protokół z przeglądu — co powinien zawierać" (verified: przegląd kotła gazowego protokół)
  - "Ile kosztuje przegląd" (verified: cena)
  - Brand line: Viessmann / Junkers / Immergas (verified modifiers) → link serwis page
  - CTA: "przypomnienie o terminie" email/SMS — converts a one-off query into a yearly customer. [assessment]
- **Schema:** Service + FAQPage.
- **Internal links:** → `/serwis-kotla-gazowego/`, `/awaria-gazowa/`.

---

## 6. New-domain velocity guidance [assessment — no dataset evidence possible]

1. **Sequencing: money pages first, pillar second.** A fresh domain has no authority for "kotłownia gazowa" (141-row informational ecosystem = competitive). The service pages (5.1–5.5) target longer, transactional strings where the map pack + GSC long-tail can produce first contacts in weeks, not months.
2. **Ship order:** /serwis-kotla-gazowego → /przylacze-gazowe → /przeglad-kotla-gazowego → /montaz → /wymiana → /projekt → /instalacja-w-domu → /kotlownia pillar → /cennik → /awaria. One page per few days, not 10 at once — indexation and link drip stay natural.
3. **Question-first expansion.** After the core pages, each remaining "czy…/jak…/ile…" suggestion that doesn't fit an existing page becomes either an FAQ entry or a 400–800-word support post ("czy przyłącze gazowe jest środkiem trwałym" → tax post). 85 verified questions ≈ a year of light content.
4. **Internal linking = hub-spoke:** service pages ↔ pillar (kotłownia) ↔ formalities posts. Every page links up and sideways; no orphans (matches `REPORT-launch-roadmap.md` §3).
5. **Do not chase bare-head terms in month 1–6** ("instalacja gazowa" polluted, "kotłownia gazowa" informational mass). Re-evaluate at GSC-impression maturity (§7): if impressions for a head term grow organically, then upgrade the relevant page.
6. **Volume expectations: none to promise.** Autocomplete gives no numbers; the honest KPI for months 1–3 is *GSC impressions appearing at all* for target seeds, then position curves (§7). [assessment]

---

## 7. Tracking keyword → position over time with the GSC API (for the user's own SEO tool)

Ground rules from `REPORT-seo-tool-architecture.md` (fetched sources there): Search Console API is free of charge [verified there]; Search Analytics quota ≈ 1,200 requests/min per site [verified there].

### 7.1 The one query that matters

```
POST https://searchconsole.googleapis.com/webmasters/v3/sites/{siteUrl}/searchAnalytics/query
{
  "startDate": "2026-10-01", "endDate": "2026-10-07",
  "dimensions": ["query", "page"],
  "rowLimit": 25000,
  "dataState": "all"          // includes fresh, not-yet-finalized data
}
```

- Filter locally to your keyword universe: the seed list + the 630 unique suggestions from this dataset become the starting tracking set [verified set]. Match by normalization (lowercase, strip diacritics, collapse whitespace) because GSC returns variants.
- **Caveats [verified there / claim, unverified]:** GSC anonymizes/rare-query-filters some query rows (privacy threshold) — absence of a keyword in GSC ≠ zero searches. Position is the *average* top position of your URL for that query over the window, not a live SERP scrape.
- Autocomplete strings ≠ GSC query strings 1:1 — expect partial matches; keep a `keywords` table mapping autocomplete-phrase → tracked-variant.

### 7.2 Minimal tracker loop (fits the tool in `REPORT-seo-tool-architecture.md`)

1. `keywords` table: phrase, source=autocomplete|gsc|manual, cluster (money/service/info/emergency), target_url.
2. Weekly job (VPS cron): pull `query,page` for the last 7d and the same window 4/8/12 weeks back; store rows in sqlite with date (snapshots, append-only — same pattern as the rest of the tool).
3. Delta report → Telegram: for each cluster, top movers (`position` Δ and `impressions` Δ), new queries appearing (zero → N impressions = earliest demand signal a new domain gets), and pages whose queries are drifting to the *wrong* cluster (e.g. `/instalacja-gazowa-w-domu/` attracting LPG-car queries — would confirm §3.5 pollution).
4. Success gate for the velocity plan (§6): page is "working" when its target seed's impressions rise while position improves; only then consider scaling that cluster.
5. The site's `/api/v1/urls?since=...` endpoint (roadmap §1.3) feeds new pages into the keywords table automatically on publish.

---

## 8. Open items

- Autocomplete was fetched once (2026-10-11). Re-run quarterly with the same seeds to diff suggestion sets — new suggestions = new real queries; churn is itself signal. [assessment]
- Legal claims in 5.2/5.5 (pozwolenie/zgłoszenie, przegląd paragraphs) must be verified against current PL law text before publish — NOT covered by this dataset. [assessment]
- No volume, seasonality, or SERP-competition data was used anywhere in this report. First real demand numbers will come from GSC itself (§7). [verified limitation]

## Sources

- Google autocomplete (live fetch, 2026-10-11): `https://suggestqueries.google.com/complete/search?client=firefox&hl=pl&q=<seed>` — 131 raw responses in `data/q_*.json`, fetched by `fetch_suggest.py` (repo).
- Flattened dataset: `/Users/hajtomoto/Repo/gas-seo/data/all_suggestions.tsv` (752 rows; all quoted suggestions verbatim).
- Internal cross-references (this repo): `REPORT-local-seo-technical.md`, `REPORT-launch-roadmap.md`, `REPORT-seo-tool-architecture.md` (GSC quotas/limits were verified against primary sources in that report on 2026-10-11).
- No external volumes/APIs were used; no numbers beyond the dataset counts and internal-report cross-references appear in this document.
