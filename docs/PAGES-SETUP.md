# GitHub Pages — setup (one-time, ~2 minutes)

The report page is `site/index.html`, published from this repo.

## If `gh` is authenticated (assistant can do this)

```bash
gh repo create gas-seo --public --source=. --push
gh api -X POST repos/novakko/gas-seo/pages -f "source[branch]=main" -f "source[path]=/site"
```

Live at: https://novakko.github.io/gas-seo/ (first deploy takes ~1 min).

## Manual (github.com UI)

1. Create public repo `gas-seo` (do NOT initialize with README).
2. `git remote add origin https://github.com/novakko/gas-seo.git && git push -u origin main`
3. Repo → **Settings → Pages** → Source: *Deploy from a branch* →
   Branch: `main`, Folder: **`/site`** → Save.

## Why /site folder

Keeps research sources (`REPORT-*.md`, `data/`, `research/`) out of the
deployed page while staying in one branch — no gh-pages branch juggling,
and Actions are not needed for a static page.
