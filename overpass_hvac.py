#!/usr/bin/env python3
"""Query Overpass API for Polish HVAC/gas craft businesses with websites. Usage: overpass_hvac.py"""
import json, urllib.request, urllib.parse, ssl, pathlib

q = '''[out:json][timeout:60];
area["ISO3166-1"="PL"][admin_level=2];
(
  node["craft"="hvac"](area);
  node["craft"="heating_engineer"](area);
  node["shop"="heating_supply"](area);
);
out center 200;'''
url = "https://overpass-api.de/api/interpreter"
data = urllib.parse.urlencode({"data": q}).encode()
req = urllib.request.Request(url, data=data, headers={"User-Agent": "Mozilla/5.0 research"})
ctx = ssl.create_default_context()
with urllib.request.urlopen(req, timeout=90, context=ctx) as r:
    data = json.loads(r.read().decode("utf-8", "replace"))
pathlib.Path("fetched/osm_hvac.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
els = data.get("elements", [])
print(f"total elements: {len(els)}")
n = 0
for e in els:
    t = e.get("tags", {})
    web = t.get("website") or t.get("contact:website")
    if web:
        n += 1
        print(f"- {t.get('name','?')} | {web} | {t.get('addr:city','')}")
print(f"with websites: {n}")
