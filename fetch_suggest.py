#!/usr/bin/env python3
"""Mine Google autocomplete (client=firefox JSON endpoint) for Polish gas-services seeds.
Saves raw JSON responses to data/ and a consolidated TSV. Real fetched data only."""
import json, time, urllib.parse, urllib.request, pathlib

OUT = pathlib.Path(__file__).parent / "data"
OUT.mkdir(exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
ENDPOINT = "https://suggestqueries.google.com/complete/search?client=firefox&hl=pl&q="

SEEDS = [
    # core service terms (building heating, NOT car LPG)
    "serwis kotłów", "kotłownia gazowa", "przyłącze gazowe",
    "montaż kotła gazowego", "wymiana kotła gazowego", "przegląd kotła gazowego",
    "konserwacja kotła gazowego", "instalacja gazowa w domu",
    "przyłącze gazu", "projekt instalacji gazowej", "odkurzanie kotłowni",
    "czyszczenie kotła gazowego", "regulacja palnika gazowego",
    # commercial-intent modifiers
    "ile kosztuje przyłącze gazu", "ile kosztuje serwis kotła",
    "ile kosztuje montaż kotła gazowego", "cennik usług gazowych",
    "awaria gazu co robić", "gaz śmierdzi co robić",
]
# question + alphabetical modifiers on the biggest commercial heads
MODIFIED = {}
for head in ["serwis kotła gazowego", "kotłownia gazowa", "przyłącze gazowe", "instalacja gazowa"]:
    MODIFIED[head] = [f"{head} {c}" for c in "abcdefghiklmnoprsuwz"]
    MODIFIED[head] += [f"czy {head}", f"jak {head}", f"ile kosztuje {head}",
                       f"{head} cena", f"{head} cennik", f"{head} warszawa",
                       f"{head} kraków", f"{head} co ile lat"]

def fetch(q):
    url = ENDPOINT + urllib.parse.quote(q)
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=15) as r:
        raw = r.read().decode("utf-8", "replace")
    try:
        data = json.loads(raw)
        return data[1], raw
    except json.JSONDecodeError:
        return [], raw

rows = []
all_queries = [(s, s) for s in SEEDS]
for head, variants in MODIFIED.items():
    all_queries += [(head, v) for v in variants]

seen = set()
for head, q in all_queries:
    if q in seen:
        continue
    seen.add(q)
    sugg, raw = fetch(q)
    slug = urllib.parse.quote(q, safe="")[:80]
    (OUT / f"q_{slug}.json").write_text(raw, encoding="utf-8")
    for s in sugg:
        rows.append((head, q, s))
    time.sleep(0.4)

tsv = OUT / "all_suggestions.tsv"
with tsv.open("w", encoding="utf-8") as f:
    f.write("seed_group\tqueried\tsuggestion\n")
    for r in rows:
        f.write("\t".join(r) + "\n")

# dedup suggestion frequency
from collections import Counter
c = Counter(s for _, _, s in rows)
print(f"queries={len(seen)} total_rows={len(rows)} unique_suggestions={len(c)}")
print("--- TOP 60 by cross-query frequency ---")
for s, n in c.most_common(60):
    print(f"{n}\t{s}")
