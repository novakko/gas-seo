#!/usr/bin/python3
"""Extract keywords from one file. Usage: python3 one.py <file> <kw1,kw2> [ctx]"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract import text_of

fn, kws = sys.argv[1], sys.argv[2].split(",")
ctx = int(sys.argv[3]) if len(sys.argv) > 3 else 220
t = text_of(os.path.join(os.path.dirname(os.path.abspath(__file__)), fn))
low = t.lower()
for kw in kws:
    start, n = 0, 0
    while n < 6:
        i = low.find(kw.lower(), start)
        if i < 0:
            break
        print("[%s] %s …%s…" % (fn, kw, t[max(0, i - ctx):i + ctx].replace("\n", " ¶ ").strip()))
        start = i + len(kw); n += 1
