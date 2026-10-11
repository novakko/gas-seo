#!/bin/bash
# One-shot: create public repo, push, enable Pages. Requires: gh auth login -h github.com done.
set -e
cd "$(dirname "$0")/.."
gh auth status >/dev/null 2>&1 || { echo "FAIL: run 'gh auth login -h github.com' first"; exit 1; }
gh repo create gas-seo --public --source=. --push --description "SEO research dossier + self-built monitoring tool for a Polish gas-services business"
sleep 3
gh api -X POST repos/novakko/gas-seo/pages -f "source[branch]=main" -f "source[path]=/" >/dev/null && echo "Pages requested"
echo "waiting for first build..."
for i in $(seq 1 24); do
  status=$(gh api repos/novakko/gas-seo/pages --jq .status 2>/dev/null || echo "?")
  [ "$status" = "built" ] && break
  sleep 5
done
echo "status: $status"
curl -s -o /dev/null -w "HTTP %{http_code}\n" https://novakko.github.io/gas-seo/
echo "LIVE: https://novakko.github.io/gas-seo/"
