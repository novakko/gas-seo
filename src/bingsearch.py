#!/usr/bin/python3
"""Bing HTML search -> result URLs. Usage: python3 bingsearch.py "query" [n]"""
import sys, os, re, html, urllib.parse, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
      "Accept-Language": "en-US,en;q=0.9"}

def search(q, n=10):
    url = "https://www.bing.com/search?q=" + urllib.parse.quote(q) + "&count=%d&setlang=en" % n
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        body = r.read().decode("utf-8", "replace")
    out = []
    for m in re.finditer(r'<h2[^>]*><a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', body):
        href, title = m.group(1), m.group(2)
        title = html.unescape(re.sub(r"<[^>]+>", "", title)).strip()
        if href.startswith("http") and "bing.com" not in href:
            out.append((href, title))
    return out

if __name__ == "__main__":
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    for u, t in search(sys.argv[1], n):
        print(u, "|", t[:100])
