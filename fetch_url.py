#!/usr/bin/env python3
"""Fetch a URL to a file with UA header. Usage: fetch_url.py <url> <outfile> [--head]"""
import sys, urllib.request, ssl

url, outfile = sys.argv[1], sys.argv[2]
head = "--head" in sys.argv
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
      "Accept-Language": "pl-PL,pl;q=0.9,en;q=0.8"}
req = urllib.request.Request(url, headers=UA, method="HEAD" if head else "GET")
ctx = ssl.create_default_context()
try:
    with urllib.request.urlopen(req, timeout=25, context=ctx) as r:
        body = r.read() if not head else b""
        code = r.status
        final = r.geturl()
except urllib.error.HTTPError as e:
    code, final, body = e.code, url, e.read()[:2000]
except Exception as e:
    print(f"FAIL {url}: {type(e).__name__}: {e}")
    sys.exit(1)
if not head:
    pathlib = __import__("pathlib")
    pathlib.Path(outfile).write_bytes(body)
print(f"{code} {final} bytes={len(body)}")
