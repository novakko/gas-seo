#!/usr/bin/env python3
"""Batch-fetch a list of URL->outfile pairs from a manifest file. Usage: batch_fetch.py manifest.txt
Manifest lines: <url> <tab> <outfile-relative-to-fetched/>"""
import sys, time, urllib.request, urllib.error, ssl, pathlib

BASE = pathlib.Path(__file__).parent
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
      "Accept-Language": "pl-PL,pl;q=0.9,en;q=0.8",
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
ctx = ssl.create_default_context()

for line in open(BASE / sys.argv[1], encoding="utf-8"):
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    url, out = line.split("\t")
    outp = BASE / "fetched" / out
    outp.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
            body = r.read()
            print(f"{r.status} {len(body)}B {r.geturl()} -> fetched/{out}")
            outp.write_bytes(body)
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code} {url} -> fetched/{out}")
        outp.write_bytes(e.read()[:5000])
    except Exception as e:
        print(f"FAIL {type(e).__name__} {url} -> fetched/{out}")
    time.sleep(1.2)
