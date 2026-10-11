#!/usr/bin/python3
"""Tiny helpers: ddg search + url fetcher. Usage:
   python3 tools.py search "query"           -> top result URLs
   python3 tools.py fetch name url [r.jina]  -> save to src/<name>.html
"""
import sys, os, re, html, urllib.parse, urllib.request

SRC = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "Mozilla/5.0", "Accept": "*/*"}

def get(url, timeout=45):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.getcode(), r.read()

def ddg(q):
    u = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(q)
    code, body = get(u)
    t = body.decode("utf-8", "replace")
    out = []
    for m in re.finditer(r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', t):
        href, title = m.group(1), m.group(2)
        if "uddg=" in href:
            href = urllib.parse.unquote(href.split("uddg=")[-1].split("&rut=")[0])
        if href.startswith("//"):
            href = "https:" + href
        title = html.unescape(re.sub(r"<[^>]+>", "", title))
        out.append((href, title[:90]))
    return code, out[:8]

def fetch(name, url, via_jina=False):
    target = ("https://r.jina.ai/" + url) if via_jina else url
    try:
        code, body = get(target)
    except urllib.error.HTTPError as e:
        code, body = e.code, e.read()
    path = os.path.join(SRC, name + ".html")
    with open(path, "wb") as f:
        f.write(body)
    print("%s  %dB  %s  %s" % (code, len(body), name, url))

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "search":
        code, res = ddg(sys.argv[2])
        print("HTTP", code)
        for u, t in res:
            print(u, "|", t)
    elif cmd == "fetch":
        fetch(sys.argv[2], sys.argv[3], len(sys.argv) > 4 and sys.argv[4] == "jina")
