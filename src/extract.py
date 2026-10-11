#!/usr/bin/python3
"""Extractor: turn fetched HTML into greppable text snippets around keywords."""
import re, sys, html, os, json

SRC = os.path.dirname(os.path.abspath(__file__))

def text_of(path):
    t = open(path, encoding="utf-8", errors="replace").read()
    t = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", t)
    t = re.sub(r"(?s)<!--.*?-->", " ", t)
    t = re.sub(r"(?i)<br\s*/?>|</p>|</li>|</h[1-6]>|</div>|</tr>", "\n", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    t = re.sub(r"[ \t\r\xa0]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n", t)
    return t

def find_hits(keywords, ctx=200, limit=40):
    kws = [k.lower() for k in keywords]
    for fn in sorted(os.listdir(SRC)):
        if not fn.endswith(".html"):
            continue
        t = text_of(os.path.join(SRC, fn))
        low = t.lower()
        hits = 0
        for kw in kws:
            start = 0
            while hits < limit:
                i = low.find(kw, start)
                if i < 0:
                    break
                snippet = t[max(0, i - ctx):i + ctx].replace("\n", " ¶ ")
                print("[%s] %s …%s…" % (fn, kw, snippet.strip()))
                hits += 1
                start = i + len(kw)
        if hits:
            print("-" * 60)

if __name__ == "__main__":
    find_hits(sys.argv[1].split(","))
