#!/usr/bin/env python3
"""Extract PL HVAC/gas businesses with websites from OSM Overpass JSON."""
import json
d = json.load(open("fetched/osm_kdk.json", encoding="utf-8"))
els = d.get("elements", [])
print(f"total craft=hvac nodes in PL: {len(els)}")
rows = []
for e in els:
    t = e.get("tags", {})
    web = t.get("website") or t.get("contact:website") or ""
    rows.append((t.get("name", "?"), web, t.get("addr:city", ""), t.get("phone", t.get("contact:phone", ""))))
webs = [r for r in rows if r[1]]
print(f"with website: {len(webs)}")
for w in sorted(webs, key=lambda x: x[2])[:40]:
    print(f"- {w[0]} | {w[1]} | {w[2]}")
print("--- sample of all names (first 30) ---")
for r in rows[:30]:
    print("*", r[0], "|", r[2])
