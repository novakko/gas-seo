#!/usr/bin/python3
"""Parse saved Google SERP -> result URLs/titles. Usage: python3 parse_google.py <file>"""
import sys, os, re, html, urllib.parse

fn = sys.argv[1]
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), fn)
t = open(path, encoding="utf-8", errors="replace").read()

urls = []
# direct hrefs
for m in re.finditer(r'href="(/url\?q=[^"]+|https?://[^"]+)"[^>]*>', t):
    u = m.group(1)
    if u.startswith("/url?q="):
        q = urllib.parse.unquote(u[7:].split("&")[0])
        u = q
    if "google." in u or u.startswith("/"):
        continue
    if u not in [x[0] for x in urls]:
        urls.append((u, ""))
for u, _ in urls[:25]:
    print(u)
if not urls:
    print("(none)")
