# gas-seo

Research + tooling for a Polish gas-services business website
(instalacja gazowa / serwis kotłów), built to rank on Google **and** inside
AI answers (ChatGPT, Claude, Gemini, Copilot, Perplexity) — with a
self-built SEO monitoring tool instead of paid SaaS.

## Contents

| Path | What it is |
|---|---|
| `REPORT-*.md` | 6 deep-research dossiers. Every claim is marked `[verified]` (source fetched, HTTP 200, content matched), `[unverified]`, or `[inference]`. Sources listed per report. |
| `site/index.html` | The interactive single-page report (built by `src/build_site.py`, zero JS dependencies). Served via GitHub Pages. |
| `data/` | Real fetched datasets: Google autocomplete JSON per seed + `all_suggestions.tsv`. Nothing here is invented; re-fetch with `src/fetch_suggest.py`. |
| `research/` | Raw HTML/JSON evidence captured from primary sources during research (17 MB, not all deployed). |
| `src/build_site.py` | Markdown → interactive HTML generator (stdlib only). |
| `src/fetch_suggest.py` | Live Google autocomplete fetcher (Polish gas-services seeds). |
| `src/*.html, *.json` | Captured evidence pages fetched by research subagents (OpenAI/Anthropic/Gemini bot docs, arXiv GEO paper, GSC docs, GBP help pages, etc.). Left in place as captured; not deployed with the site. |

## Anti-fabrication policy

Numbers in the reports are either (a) fetched from a primary source on the
date shown and marked `[verified]`, or (b) explicitly marked
`unknown (not fetched)` / `claim, unverified`. Where the research could not
confirm a figure, it says so instead of inventing one.

## Build

```bash
/usr/bin/python3 src/build_site.py      # writes site/index.html
/usr/bin/python3 src/validate_html.py   # tag-balance check
```

## Live page

https://novakko.github.io/gas-seo/ (GitHub Pages, enabled per `docs/PAGES-SETUP.md`).

## Status

Research phase. Next: build the actual site + the SEO automation tool per
`REPORT-launch-roadmap.md`.
