#!/usr/bin/env python3
"""Dump SERP html to file for inspection. Usage: serp_dump.py <engine> <query> <outfile>"""
import sys, urllib.parse, urllib.request, ssl
engine, query, outfile = sys.argv[1], sys.argv[2], sys.argv[3]
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
      "Accept-Language": "pl-PL,pl;q=0.9,en;q=0.8",
      "Accept": "text/html,application/xhtml+xml"}
ctx = ssl.create_default_context()
if engine == "mojeek":
    url = "https://www.mojeek.com/search?q=" + urllib.parse.quote(query)
elif engine == "bing":
    url = "https://www.bing.com/search?q=" + urllib.parse.quote(query) + "&setlang=pl&cc=PL"
else:
    sys.exit("unknown")
req = urllib.request.Request(url, headers=UA)
with urllib.request.urlopen(req, timeout=25, context=ctx) as r:
    html = r.read().decode("utf-8", "replace")
open(outfile, "w", encoding="utf-8").write(html)
print(f"saved {len(html)} bytes to {outfile}")
