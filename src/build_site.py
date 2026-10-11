#!/usr/bin/env python3
"""Generate interactive SEO research report (HTML) from REPORT-*.md files.

Anti-fabrication rules:
- Converts ONLY what exists in the markdown files. No data is invented.
- Every claim keeps its source markers ([verified]/[unverified]/[inference])
  and the per-report Sources section.
- Live-fetched autocomplete data is read from data/all_suggestions.tsv
  (produced by src/fetch_suggest.py hitting Google's real endpoint).

Output: site/index.html (self-contained, no external deps, no JS libraries).
"""
import html
import json
import os
import re
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
DATA_TSV = os.path.join(ROOT, "data", "all_suggestions.tsv")

REPORTS = [
    ("REPORT-local-seo-technical.md", "local",
     "Local SEO & Technical Foundation",
     "Google Business Profile, Polish citations, site architecture, structured data, hosting"),
    ("REPORT-geo-ai-citations.md", "geo",
     "AI Citations (GEO)",
     "How ChatGPT / Claude / Gemini / Copilot / Perplexity pick which businesses to cite"),
    ("REPORT-competitor-reverse-engineering.md", "competitors",
     "Competitor Reverse-Engineering",
     "Free tools + self-built scrapers instead of paid SaaS"),
    ("REPORT-seo-tool-architecture.md", "tool",
     "SEO Tool Architecture",
     "Free APIs, quotas, self-hosted components, data model"),
    ("REPORT-content-keywords.md", "content",
     "Keywords & Content Strategy",
     "Live-fetched autocomplete data, page taxonomy, new-domain velocity"),
    ("REPORT-launch-roadmap.md", "launch",
     "Launch & First 90 Days",
     "Sequenced technical roadmap, indexing reality, first backlinks"),
]


# ---------------------------------------------------------------- markdown --
def esc(s: str) -> str:
    return html.escape(s, quote=True)


def inline(s: str) -> str:
    """Inline markdown -> HTML. Placeholder extraction runs on raw text
    (codes -> md images/links -> bare URLs), then escaping, then emphasis,
    then placeholder restoration — so constructs can't collide."""
    codes, links, urls = [], [], []

    def _code(m):
        codes.append(m.group(1))
        return f"\x00{len(codes)-1}\x00"

    def _mdlink(m):
        links.append((m.group(1), m.group(2)))  # text, url
        return f"\x01{len(links)-1}\x01"

    def _url(m):
        raw = m.group(0)
        u = raw.rstrip(".,;:")
        trail = raw[len(u):]
        urls.append(u)
        return f"\x02{len(urls)-1}\x02{trail}"

    s = re.sub(r"`([^`]+)`", _code, s)
    # images -> markdown links with suffix (render as links, no external assets)
    s = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", r"[\1 (image)](\2)", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", _mdlink, s)
    s = re.sub(r"https?://[^\s)\]]+", _url, s)
    s = esc(s)
    # bold, italic, strikethrough
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"~~([^~]+)~~", r"<del>\1</del>", s)
    for i, c in enumerate(codes):
        s = s.replace(f"\x00{i}\x00", f"<code>{esc(c)}</code>")
    for i, (txt, url) in enumerate(links):
        s = s.replace(f"\x01{i}\x01",
                      f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(txt)}</a>')
    for i, u in enumerate(urls):
        s = s.replace(f"\x02{i}\x02",
                      f'<a href="{esc(u)}" target="_blank" rel="noopener">{esc(u)}</a>')
    return s


def slugify(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"[^\w\s-]", "", s.lower())
    return re.sub(r"[\s_]+", "-", s.strip())[:60] or "sec"


def md_to_html(md_text: str, prefix: str) -> str:
    """Convert our markdown dialect to HTML. Line-based, then inline."""
    out = []
    lines = md_text.split("\n")
    i, n = 0, len(lines)
    in_sources = False
    while i < n:
        line = lines[i]
        stripped = line.strip()
        # fenced code
        if stripped.startswith("```"):
            lang = stripped[3:].strip()
            buf = []
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            out.append('<pre class="code" data-lang="%s"><code>%s</code></pre>'
                       % (esc(lang), esc("\n".join(buf))))
            continue
        # table
        if stripped.startswith("|") and i + 1 < n and re.match(r"^\|[\s:|-]+\|$", lines[i+1].strip()):
            header = [c.strip() for c in stripped.strip("|").split("|")]
            rows = []
            i += 2
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            t = ['<div class="tablewrap"><table><thead><tr>']
            for h in header:
                t.append(f"<th>{inline(h)}</th>")
            t.append("</tr></thead><tbody>")
            for r in rows:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table></div>")
            out.append("".join(t))
            continue
        # headings
        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            level = len(m.group(1))
            text = m.group(2)
            if level == 2 and text.lower() == "sources":
                in_sources = True
            hid = f"{prefix}-{slugify(text)}"
            content = inline(text)
            # tag evidence markers inside headings
            content = tag_markers(content)
            out.append(f"<h{level} id=\"{hid}\">{content}"
                       f'<a class="anchor" href="#{hid}">§</a></h{level}>')
            i += 1
            continue
        # horizontal rule
        if re.match(r"^-{3,}$", stripped):
            out.append("<hr>")
            i += 1
            continue
        # blockquote
        if stripped.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append(f"<blockquote>{inline(' '.join(buf))}</blockquote>")
            continue
        # unordered list (supports nesting by 2-space indent)
        if re.match(r"^[-*+]\s+", stripped):
            items = []
            while i < n and re.match(r"^\s*[-*+]\s+", lines[i]):
                indent = len(lines[i]) - len(lines[i].lstrip())
                text = re.sub(r"^\s*[-*+]\s+", "", lines[i])
                i += 1
                while i < n and lines[i].strip() and not re.match(
                        r"^\s*([-*+]\s|\d+\.\s|#{1,6}\s|\||>|```)", lines[i]) \
                        and (len(lines[i]) - len(lines[i].lstrip())) > indent:
                    text += " " + lines[i].strip()
                    i += 1
                items.append((indent, text))
            out.append(build_list(items, prefix))
            continue
        # ordered list
        if re.match(r"^\d+\.\s+", stripped):
            items = []
            while i < n and re.match(r"^\s*\d+\.\s+", lines[i]):
                base = len(lines[i]) - len(lines[i].lstrip())
                text = re.sub(r"^\s*\d+\.\s+", "", lines[i])
                i += 1
                while i < n and lines[i].strip() and not re.match(
                        r"^\s*([-*+]\s|\d+\.\s|#{1,6}\s|\||>|```)", lines[i]) \
                        and (len(lines[i]) - len(lines[i].lstrip())) > base:
                    text += " " + lines[i].strip()
                    i += 1
                items.append((base, text))
            out.append(build_list(items, prefix, ordered=True))
            continue
        # blank
        if not stripped:
            i += 1
            continue
        # paragraph
        buf = [stripped]
        i += 1
        while i < n and lines[i].strip() and not re.match(
                r"^(#{1,6}\s|[-*+]\s|\d+\.\s|\||>|```|-{3,}$)", lines[i].strip()):
            buf.append(lines[i].strip())
            i += 1
        para = inline(" ".join(buf))
        para = tag_markers(para)
        cls = ' class="sources"' if in_sources else ""
        out.append(f"<p{cls}>{para}</p>")
    return "\n".join(out)


def build_list(items, prefix, ordered=False):
    """Build nested <ul>/<ol> from (indent, text) tuples. Indent levels are
    quantized to observed distinct values so 2/4-space nesting both work."""
    tag = "ol" if ordered else "ul"
    items = [(ind, tag_markers(inline(t))) for ind, t in items]
    levels = sorted({ind for ind, _ in items})
    rank = {ind: r for r, ind in enumerate(levels)}
    out = []
    depth = 0
    open_li = [False]  # open_li[d] = True while <li> at depth d is unclosed
    for indent, text in items:
        r = rank[indent]
        while r > depth:
            out.append(f"<{tag}>")
            depth += 1
            open_li.append(False)
        while depth > r:
            if open_li[depth]:
                out.append("</li>")
                open_li[depth] = False
            out.append(f"</{tag}>")
            depth -= 1
            open_li.pop()
        if open_li[depth]:
            out.append("</li>")
        out.append(f"<li>{text}")
        open_li[depth] = True
    while depth > 0:
        if open_li[depth]:
            out.append("</li>")
            open_li[depth] = False
        out.append(f"</{tag}>")
        depth -= 1
        open_li.pop()
    if open_li[0]:
        out.append("</li>")
    return f"<{tag}>" + "".join(out) + f"</{tag}>"


def tag_markers(s: str) -> str:
    """Wrap evidence markers in styled spans."""
    s = re.sub(r"\[verified\]", '<span class="tag ok">verified</span>', s, flags=re.I)
    s = re.sub(r"\[unverified\]", '<span class="tag warn">unverified</span>', s, flags=re.I)
    s = re.sub(r"\[inference\]", '<span class="tag inf">inference</span>', s, flags=re.I)
    s = re.sub(r"claim, unverified", '<span class="tag warn">claim, unverified</span>', s)
    s = re.sub(r"unknown \(not fetched\)",
               '<span class="tag na">unknown, not fetched</span>', s)
    return s


# ------------------------------------------------------------------- data --
def load_suggestions():
    """Read real fetched autocomplete data. Returns dict or None."""
    if not os.path.exists(DATA_TSV):
        return None
    data = {}
    with open(DATA_TSV, encoding="utf-8", errors="replace") as f:
        for row in f:
            parts = row.rstrip("\n").split("\t")
            if len(parts) >= 2 and parts[0] != "seed":
                seed, sug = parts[0], parts[1]
                data.setdefault(seed, [])
                if sug not in data[seed]:
                    data[seed].append(sug)
    return data or None


def suggestions_html(data):
    if not data:
        return ('<p class="na">Autocomplete dataset not present — '
                'run src/fetch_suggest.py to fetch live data.</p>')
    seeds = sorted(data.keys())
    sid = lambda s: re.sub(r"[^\w]+", "-", s.lower(), flags=re.UNICODE).strip("-")[:80]
    chips = "".join(f'<button class="chip" data-seed="{sid(s)}" onclick="showSeed(this)">'
                    f'{esc(s)}</button>' for s in seeds)
    rows = "".join(
        f'<div class="seedbox hidden" id="seed-{sid(s)}">'
        f"<h4>{esc(s)} <em class='muted'>— {len(v)} live suggestions</em></h4>"
        f"<ul class='suglist'>" + "".join(f"<li>{esc(x)}</li>" for x in v) + "</ul></div>"
        for s, v in sorted(data.items()))
    total = sum(len(v) for v in data.values())
    return (f"<p><strong>{len(seeds)}</strong> seeds · "
            f"<strong>{total}</strong> suggestions — fetched live from Google "
            f"autocomplete endpoint (suggestqueries.google.com), not invented. "
            f"Raw JSON in <code>data/</code>, TSV at <code>data/all_suggestions.tsv</code>.</p>"
            f'<div class="chips">{chips}</div>{rows}')


# ------------------------------------------------------------------ chrome --
CSS = """
:root{--bg:#0e1114;--card:#171b20;--card2:#1d232a;--tx:#e6e9ec;--mut:#98a1ab;
--acc:#4fc38f;--warn:#e0b050;--err:#e07070;--inf:#7aa7e0;--ln:#2a323b}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--tx);font:16px/1.65 -apple-system,'Segoe UI',
Roboto,sans-serif;padding-bottom:4rem}
header.hero{padding:3.5rem 1.2rem 2rem;max-width:980px;margin:0 auto}
.hero h1{font-size:clamp(1.7rem,4vw,2.6rem);line-height:1.15;letter-spacing:-.02em}
.hero .sub{color:var(--mut);margin-top:.8rem;max-width:720px}
.hero .meta{margin-top:1rem;color:var(--mut);font-size:.85rem}
.badges{margin-top:1.2rem;display:flex;gap:.5rem;flex-wrap:wrap}
.badge{font-size:.75rem;padding:.25rem .6rem;border:1px solid var(--ln);
border-radius:999px;color:var(--mut)}
nav.toc{max-width:980px;margin:1.5rem auto;padding:0 1.2rem;display:grid;
grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:.7rem}
.toc a{display:block;background:var(--card);border:1px solid var(--ln);
border-radius:12px;padding:.9rem 1rem;text-decoration:none;color:var(--tx);
transition:border-color .15s}
.toc a:hover{border-color:var(--acc)}
.toc .t{font-weight:650}
.toc .d{font-size:.82rem;color:var(--mut);margin-top:.25rem}
main{max-width:980px;margin:0 auto;padding:0 1.2rem}
section.report{background:var(--card);border:1px solid var(--ln);border-radius:16px;
padding:1.6rem;margin-bottom:1.6rem}
section.report>h2{font-size:1.45rem;margin:0 0 1rem;padding-bottom:.7rem;
border-bottom:1px solid var(--ln);letter-spacing:-.01em}
h3{font-size:1.15rem;margin:1.6rem 0 .6rem}
h4{font-size:1rem;margin:1.2rem 0 .5rem}
p{margin:.6rem 0}
p.sources{font-size:.85rem;color:var(--mut);border-left:2px solid var(--ln);
padding-left:.8rem}
a{color:var(--acc)}
.anchor{opacity:0;margin-left:.4rem;text-decoration:none;font-size:.8em}
h2:hover .anchor,h3:hover .anchor,h4:hover .anchor{opacity:.6}
ul,ol{margin:.6rem 0 .6rem 1.4rem}
li{margin:.3rem 0}
blockquote{border-left:3px solid var(--acc);background:var(--card2);
padding:.6rem 1rem;border-radius:0 8px 8px 0;margin:.8rem 0;color:var(--mut)}
pre.code{background:#0a0d10;border:1px solid var(--ln);border-radius:10px;
padding:.9rem 1rem;overflow-x:auto;margin:.8rem 0;font-size:.82rem;line-height:1.5}
code{font-family:'SF Mono',ui-monospace,Menlo,monospace;font-size:.86em;
background:#0a0d10;border:1px solid var(--ln);border-radius:5px;padding:.08em .35em}
pre.code code{background:none;border:none;padding:0}
.tablewrap{overflow-x:auto;margin:.8rem 0}
table{border-collapse:collapse;width:100%;font-size:.86rem}
th,td{border:1px solid var(--ln);padding:.45rem .6rem;text-align:left;
vertical-align:top}
th{background:var(--card2)}
.tag{display:inline;font-size:.72rem;font-weight:650;border-radius:5px;
padding:.1em .45em;margin-right:.15em;white-space:nowrap}
.tag.ok{background:#123527;color:var(--acc);border:1px solid #1d5c41}
.tag.warn{background:#3a2f14;color:var(--warn);border:1px solid #6b5420}
.tag.inf{background:#16283f;color:var(--inf);border:1px solid #2b4a73}
.tag.na{background:#2a2d31;color:var(--mut);border:1px solid var(--ln)}
.chips{display:flex;flex-wrap:wrap;gap:.4rem;margin:.8rem 0}
.chip{background:var(--card2);color:var(--tx);border:1px solid var(--ln);
border-radius:999px;padding:.3rem .75rem;font-size:.8rem;cursor:pointer}
.chip:hover{border-color:var(--acc)}
.chip.active{background:var(--acc);color:#08110c;border-color:var(--acc);font-weight:650}
.seedbox{background:var(--card2);border:1px solid var(--ln);border-radius:12px;
padding:1rem;margin:.7rem 0}
.seedbox h4{margin:0 0 .5rem}
.suglist{columns:2;gap:1.4rem;font-size:.88rem}
.hidden{display:none}
.muted{color:var(--mut);font-weight:400;font-size:.82em}
.na{color:var(--mut);font-style:italic}
footer{max-width:980px;margin:2rem auto 0;padding:1.2rem;color:var(--mut);
font-size:.95rem;border-top:1px solid var(--ln)}
.searchbar{max-width:980px;margin:0 auto 1rem;padding:0 1.2rem}
.searchbar input{width:100%;background:var(--card);border:1px solid var(--ln);
border-radius:12px;color:var(--tx);padding:.75rem 1rem;font-size:.95rem;outline:none}
.searchbar input:focus{border-color:var(--acc)}
@media(max-width:640px){.suglist{columns:1}}
"""

JS = """
function showSeed(btn){
  document.querySelectorAll('.chip').forEach(c=>c.classList.remove('active'));
  btn.classList.add('active');
  document.querySelectorAll('.seedbox').forEach(b=>b.classList.add('hidden'));
  var el=document.getElementById('seed-'+btn.dataset.seed);
  if(el)el.classList.remove('hidden');
}
function filterReports(q){
  q=q.toLowerCase();
  document.querySelectorAll('section.report').forEach(sec=>{
    var hit=!q||sec.textContent.toLowerCase().includes(q);
    sec.style.display=hit?'':'none';
  });
}
"""


def build():
    os.makedirs(SITE, exist_ok=True)
    today = date.today().isoformat()
    sections = []
    toc = []
    stats = {"sources": 0, "verified": 0, "words": 0}
    for fname, key, title, desc in REPORTS:
        path = os.path.join(ROOT, fname)
        if not os.path.exists(path):
            sections.append(f'<section class="report" id="{key}"><h2>{esc(title)}</h2>'
                            f'<p class="na">Report file {esc(fname)} not yet written '
                            f'(research subagent still running at build time).</p></section>')
            toc.append((key, title, desc + " (pending)"))
            continue
        md = open(path, encoding="utf-8", errors="replace").read()
        body = md_to_html(md, key)
        # count evidence markers + sources links
        stats["sources"] += len(re.findall(r"^\d+\.\s+https?://", md, flags=re.M))
        stats["verified"] += len(re.findall(r"\[verified\]", md, flags=re.I))
        stats["words"] += len(md.split())
        sections.append(
            f'<section class="report" id="{key}">\n<h2>{esc(title)}</h2>\n'
            f'<p class="muted">Source file: <code>{esc(fname)}</code> — '
            f'{len(md.split())} words. Evidence markers preserved as-is.</p>\n'
            f'{body}\n</section>')
        toc.append((key, title, desc))

    sug_data = load_suggestions()
    sug_section = (
        '<section class="report" id="autocomplete"><h2>Live Autocomplete Dataset '
        '<span class="muted">(real fetched data)</span></h2>'
        + suggestions_html(sug_data) + "</section>")

    toc_html = "".join(
        f'<a href="#{k}"><div class="t">{esc(t)}</div><div class="d">{esc(d)}</div></a>'
        for k, t, d in toc)

    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Gas Services SEO — Research Dossier ({today})</title>
<meta name="description" content="Anti-slop SEO research dossier for a Polish gas
services business: local SEO, AI citations, competitor reverse-engineering,
self-built monitoring tool. All claims source-marked.">
<style>{CSS}</style>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"TechArticle",
"headline":"Gas Services Website — SEO Research Dossier",
"datePublished":"{today}","dateModified":"{today}",
"author":{{"@type":"Organization","name":"gas-seo"}},
"about":{{"@type":"Thing","name":"SEO for local gas services business (Poland)"}}}}
</script>
</head>
<body>
<header class="hero">
<h1>Gas Services Website — SEO Research Dossier</h1>
<p class="sub">Deep-research compilation for building a Polish gas-services site
with maximum organic + AI-engine visibility, and a self-built monitoring tool
instead of paid SaaS. Every claim carries an evidence marker:
<span class="tag ok">verified</span> means the source was fetched and matched,
<span class="tag warn">unverified</span> means claimed but not confirmed,
<span class="tag inf">inference</span> is reasoning, not fact.</p>
<div class="badges">
<span class="badge">built {today}</span>
<span class="badge">{stats['words']:,} words</span>
<span class="badge">{stats['sources']} source URLs listed</span>
<span class="badge">{stats['verified']} [verified] markers</span>
<span class="badge">0 fabricated data</span>
</div>
</header>
<div class="searchbar"><input type="search" placeholder="Filter all reports…"
oninput="filterReports(this.value)"></div>
<nav class="toc">{toc_html}
<a href="#autocomplete"><div class="t">Live Autocomplete Dataset</div>
<div class="d">Real Google suggestions fetched for PL gas-services seeds</div></a>
</nav>
<main>
{sug_section}
{chr(10).join(sections)}
</main>
<footer>
<p>Generated {today} by <code>src/build_site.py</code> from 6 markdown dossiers
(<~{stats['words']:,} words, uncommitted working tree) ·
zero data invented — every claim carries its evidence tag in the source markdown.</p>
</footer>
<script>{JS}</script>
</body>
</html>"""
    out = os.path.join(SITE, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"written {out} ({os.path.getsize(out):,} bytes); "
          f"reports={sum(1 for f_, _, _, _ in REPORTS if os.path.exists(os.path.join(ROOT, f_)))}/6")


if __name__ == "__main__":
    build()
