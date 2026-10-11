#!/usr/bin/env python3
"""Fetch a search engine results page and extract result URLs. Usage: serp.py <engine> <query>"""
import sys, re, urllib.parse, urllib.request, ssl

engine, query = sys.argv[1], sys.argv[2]
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
      "Accept-Language": "pl-PL,pl;q=0.9,en;q=0.8"}
ctx = ssl.create_default_context()

def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=25, context=ctx) as r:
        return r.read().decode("utf-8", "replace")

html = ""
if engine == "mojeek":
    html = get("https://www.mojeek.com/search?q=" + urllib.parse.quote(query))
    urls = re.findall(r'<a class="ob" href="(https?://[^"]+)"', html)
elif engine == "bing":
    html = get("https://www.bing.com/search?q=" + urllib.parse.quote(query) + "&setlang=pl&cc=PL")
    urls = re.findall(r'<h2><a href="(https?://[^"]+)"', html)
else:
    sys.exit("unknown engine")

seen = set()
for u in urls:
    u = urllib.parse.unquote(u.split("&")[0]) if "uddg=" in u else u
    host = urllib.parse.urlparse(u).netloc
    if host in seen:
        continue
    seen.add(host)
    print(u)
