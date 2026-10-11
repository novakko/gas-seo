#!/bin/bash
# Rebuild + validate + commit + push the report site.
# Prereq: gh auth login -h github.com (or a working git credential), remote origin set.
set -e
cd "$(dirname "$0")/.."
/usr/bin/python3 src/build_site.py
/usr/bin/python3 src/validate_html.py site/index.html
git add -A
git commit -m "rebuild site $(date +%Y-%m-%d %H:%M)" || echo "nothing to commit"
git push origin main
echo "deployed. Pages URL: https://novakko.github.io/gas-seo/"
