#!/usr/bin/python3
"""Parse a saved Bing SERP HTML file -> result URLs/titles. Usage: python3 parse_bing.py <file>"""
import sys, os, re, html

fn = sys.argv[1]
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), fn)
t = open(path, encoding="utf-8", errors="replace").read()

# organic results live in <li class="b_algo"> blocks
blocks = re.split(r'class="b_algo"', t)[1:]
if not blocks:
    blocks = [t]
count = 0
for b in blocks:
    m = re.search(r'<a[^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a>', b)
    if not m:
        continue
    u = m.group(1)
    title = html.unescape(re.sub(r"<[^>]+>", "", m.group(2))).strip()
    print(u[:130], "|", title[:90])
    count += 1
    if count >= 10:
        break
if count == 0:
    print("(no results parsed)")
