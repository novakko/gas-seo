#!/usr/bin/env python3
"""Bing SERP via format=rss with proper percent-encoding. Usage: bing_rss.py <query> <outfile>"""
import sys, urllib.parse, urllib.request, ssl, re, html

query, outfile = sys.argv[1], sys.argv[2]
url = "https://www.bing.com/search?" + urllib.parse.urlencode({"q": query, "format": "rss", "count": "20"})
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
ctx = ssl.create_default_context()
with urllib.request.urlopen(req, timeout=25, context=ctx) as r:
    xml = r.read().decode("utf-8", "replace")
open(outfile, "w", encoding="utf-8").write(xml)
items = re.findall(r"<item><title>(.*?)</title><link>(.*?)</link><description>(.*?)</description>", xml, re.S)
if not items:
    print("NO RESULTS (empty channel)")
for t, l, d in items[:15]:
    t, l, d = html.unescape(t), html.unescape(l), html.unescape(d)
    d = re.sub(r"<[^>]+>", "", d)[:110]
    print(f"- {t}\n  {l}\n  {d}")
