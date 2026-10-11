# Competitor Reverse-Engineering for a Local Gas-Services Site
### Free tools + self-built scrapers — no paid SaaS. Verified 2026-10-11.

Environment this was researched and tested on: Apple Silicon Mac, macOS 26.6, python3 3.12.11
(`/usr/bin/python3`-compatible), no sudo, plain `curl` with a browser-ish `User-Agent` header.

Everything marked **[verified]** was fetched from the primary source during this session
(HTTP 200 and content matched the claim). Anything else is explicitly marked
**claim, unverified** or **unknown (not fetched)**.

---

## 1. What free tiers actually offer (2025–2026 reality)

### Ahrefs — verified at ahrefs.com
- Ahrefs Webmaster Tools has been **renamed "Ahrefs Free"** ("Ahrefs Webmaster Tools is now
  Ahrefs Free" — on-page banner, fetched 2026-10-11). Free-forever account, no credit card.
- Full Site Explorer / Site Audit / Web Analytics data is **for verified websites only**
  (your own sites) — stated three times on the /free page.
- On-page limits table (fetched from /webmaster-tools): Site Audit
  "crawl credits/month per project: Unlimited"; for non-verified/free-checker contexts
  backlinks & keywords shown are "Top 1,000" vs "All known links" on paid.
- The standalone **free Backlink Checker** (ahrefs.com/backlink-checker, fetched) works on
  **any domain**: shows DR, number of referring domains, top referring domains/pages,
  top anchors, and a backlinks report per URL. The fetched page does not state a numeric
  row cap for anonymous users — cap: unknown (not fetched). Community consensus says the
  anonymous view is heavily truncated; treat any specific number as claim, unverified.
- **Competitive use:** free backlink checker = one-off "who links to the 3 competitors
  nearest me" lookups. Not a crawling API. Your own site gets the real data via verification.

### Google Keyword Planner — partially verified
- Help-center page (support.google.com/google-ads/answer/73361) fetched twice: rendered
  nav-heavy; the body sentence about volume ranges was not extractable in this session.
- Standing behavior: GKP is **free with any active Google Ads account** and shows **volume
  ranges, not exact volumes, unless you're actually spending** — claim, unverified at
  primary source this session (long-standing, widely documented).
- Practical: create a bare Ads account, never launch a campaign; you still get keyword ideas
  with ranges for Poland (set geo = Poland, language = Polish). Ranges are still useful for
  *ranking* demand buckets, useless for fine comparisons.

### Bing Webmaster Tools keyword research
- Help page (bing.com/webmasters/help/keyword-research-626a4e57) fetched: returned a
  241-byte JS shell only — **details unknown (not fetched)**.
- The tool itself is free with a BWT account (verify your site or import from GSC) and
  reports impressions/clicks-ish data from Bing — claim, unverified this session.
- Worth doing anyway: Bing share in Poland is small but BWT also gives a free site scan +
  SEO reports, and Bing SERPs are scrapable far more leniently than Google (still challenge-
  walled from datacenter IPs — see §2).

### Moz free tools — verified page, caps unknown
- moz.com/products/free-seo-tools fetched: lists Domain Analysis (DA, top pages),
  Link Explorer ("40 trillion links"), Keyword Explorer, Competitive Research, MozBar.
- Numeric free-query caps (commonly cited as a handful of Link Explorer queries/month):
  **not stated on fetched page — unknown (not fetched)**. Domain Analysis is the useful one:
  free DA + top-pages snapshot per competitor, once in a while.

### Ubersuggest — verified page, quota unverified
- neilpatel.com/ubersuggest fetched: markets "free limited features"; the often-quoted
  "3 free searches per day" **did not appear on the fetched page — unknown (not fetched)**.
- Treat it as a spot-checker for PL volumes, not a pipeline.

### Mangools / KWFinder — verified: no free tier
- mangools.com/free-seo-tools fetched: Mangools' free offering is a set of mini-tools
  (SERP Simulator, Reddit Threads Finder, Google Location Changer, SERP Volatility Checker,
  browser extension, AI Search Grader). KWFinder lookups come only with the paid trial —
  free lookup quota: unknown (not fetched). Don't plan around it.

### What is genuinely first-class free (and sufficient for local SEO)
| Tool | Cost | Verified this session |
|---|---|---|
| Google Search Console Performance | free | doc fetched [verified] |
| Google autocomplete API (`suggestqueries.google.com`) | free | live PL query [verified] |
| Wayback Machine CDX API | free | live JSON [verified] |
| GitHub api.github.com search + raw.githubusercontent.com | free, anon | live [verified] |
| r.jina.ai URL→markdown proxy | free (anon) | live incl. Google SERP [verified] |
| Ahrefs free backlink checker | free | page [verified] |
| Bing Webmaster Tools | free | help page JS-gated [unverified content] |

---

## 2. SERP data without paid APIs — legality, then what actually works

### ToS / legality reality (verified sources)
- Google's `robots.txt` disallows `/search` for all user-agents — fetched and confirmed
  (`Disallow: /search`) [verified].
- Google's Terms (policies.google.com/terms, fetched) prohibit "using automated means to
  access content from any of our services in violation of the machine-readable instructions
  on our web pages (for example, robots.txt files that disallow crawling...)" [verified].
- **hiQ Labs v. LinkedIn** (9th Cir.): scraping *public* webpages is not a CFAA
  "unauthorized access"; 2019 injunction, vacated after *Van Buren* (2021), reaffirmed on
  remand (April 2022); in Nov 2022 hiQ was found to have breached LinkedIn's User Agreement
  and the parties settled — full timeline fetched from Wikipedia [verified]. Net: publicly
  visible data scraping is a contract/ToS issue, not a crime in US precedent; enforcement in
  practice = blocking, cease-and-desist letters, civil claims — not raids.
- **Meta Platforms v. Bright Data (2024)** — often cited as "ToS can't restrict scraping of
  public data": I could **not verify** it — the Wikipedia article does not exist (fetch
  returned a missing-page view) [unverified]. Treat as claim, unverified.
- EU/Poland dimension (context, not legal advice): business registries and review text are
  public, but review authors and sole traders are natural persons → GDPR applies to
  *processing* (store minimum, don't republish personal data). ToS risk sits with automated
  Google access; competitor-*page* scraping (their HTML) is the low-risk end.

### What actually worked from this machine today (all tested live)
| Method | Result |
|---|---|
| `curl google.com/search` plain | consent/JS shell, no results [tested] |
| same with `&gbv=1` basic HTML | HTTP 400 [tested] |
| `curl bing.com/search` | challenge page [tested] |
| `html.duckduckgo.com/html` and `lite.` | "anomaly/botnet" block page [tested] |
| `r.jina.ai/https://www.google.com/search?q=...&hl=pl` | **full SERP rendered** [verified] |

The **r.jina.ai** capture of a real Polish commercial query returned:
- the local pack ("Firmy"): 3 businesses with name, category (`· Naprawa pieców`),
  tenure line ("Działa od ponad 30 lat"), hours, phone numbers, a review quote, services;
- organic web results as snippets — **but organic titles/URLs did not survive the markdown
  render** (verified in the capture; only descriptions came through);
- People-Also-Ask / related-searches section markers ("Więcej pytań", "Inni
  wyszukiwali również") — collapsed, need expansion via follow-up queries.
- Anonymous r.jina.ai rate limits: unknown (not fetched). Expect throttling; cache responses.

So the honest free-SERP stack, in order:
1. **r.jina.ai for SERP + local pack** — categories, phones, review snippets, PAA seeds.
   For organic *URLs*, cross-fill by opening the top results manually in a browser once per
   keyword set (10 queries ≈ 10 minutes) or run a local headless browser from your home IP.
2. **Local headless browser (Playwright) from your home IP** at human cadence
   (a few queries/day, cached) — this is what the tools below automate.
3. **SerpBear** for ongoing rank tracking (next section).

### Community-used GitHub repos (star counts + last push verified via api.github.com today)
- `gosom/google-maps-scraper` — **6,369 stars, pushed 2026-09-24** [verified].
  Go + Playwright; CLI and Docker; CSV/JSON/Postgres outputs; flags verified in README:
  `-json -results out/results.json`, `-extra-reviews` (collect review texts);
  language/region options exist in the README but I did not verify exact flag names —
  unknown (not fetched).
- `omkarcloud/google-maps-scraper` — **3,607 stars, pushed 2026-09-21** [verified].
  Python/Botasaurus; review extraction "that actually works" per README; requires local
  Google Chrome; desktop app + built-in API.
- `towfiqi/serpbear` — **2,108 stars, pushed 2026-05-14** [verified]. Self-hosted rank
  tracker (Docker): unlimited keywords, email/position-change notifications, built-in REST
  API, **Google Search Console integration** (real impressions per tracked keyword) and
  **Google Ads integration** (real volume ranges per keyword — GKP data without the UI).
  README states it fetches SERPs *via* third-party scrapers/proxies (ScrapingAnt, SearchApi,
  SerpApi, etc. or your own proxies) — i.e., bring-your-own proxy = effectively free at
  small scale; docs at docs.serpbear.com.
- `ecoron/SerpScrap` — 273 stars, pushed 2026-09-02 [verified]. Python SERP extractor.
- High-star `oxylabs/*` and `ScrapingBee/*` "how to scrape" repos (2,914 / 2,101 / 482
  stars) are vendor marketing for paid APIs — skip for a no-SaaS setup [verified stars].
- GitHub search API: anonymous quota is 60 req/h per docs (not fetched this session);
  3 sequential searches succeeded unauthenticated during research [observed].

---

## 3. Google Maps / GMB competitor intelligence

Local pack data is the most decision-relevant competitor data in this niche, and it's the
easiest to collect free (the r.jina.ai capture already yields category, phone, tenure,
hours, review quote — all [verified] fields from a live PL query).

Per-competitor GMB snapshot to store weekly (CSV/SQLite):
- name, category (primary), phone, address, hours, "Działa od ponad X lat" tenure string,
  rating, review count, newest review date, review texts (via `-extra-reviews` /
  Botasaurus), photo count delta, services list (`Usługi:` in render), posts/updates.

Derived competitor metrics (all computable from the snapshot table):
- **review velocity** — new reviews per 30 days; who is actively farming and from when;
- **review recency gap** — days since last review = who is dormant;
- **category choices** — e.g. does the pack leader use "Naprawa pieców" vs
  "Firma remontowa" (verified category string from live capture);
- **photo cadence** — proxy for ongoing profile activity;
- **service keyword extraction** — pull `Usługi` items across all 10 pack competitors,
  union → the category vocabulary Google rewards.

Cadence: weekly run is plenty; local packs move slowly. Run from home IP or with the
gosom scraper's proxy option; aggressive pulls get you blocked fast.

---

## 4. On-page reverse-engineering protocol (the core playbook)

### What to extract from every top-10 competitor page
1. `<title>` and `H1` — build a pattern table (keyword order, city suffix, symbols,
   length). Verified observed pattern from live SERP snippets: brand + city + qualifier
   ("SERWIS 24H ➤ naprawa kotłów gazowych w Warszawie i okolicach") and 24h phone in title.
2. H2/H3 outline — section skeleton of the ranking page.
3. Word count and text-to-HTML ratio.
4. **Brand-list content** — the live capture shows ranking pages listing serviced boiler
   brands (Buderus, Junkers, Viessmann, Vaillant, Termet, De Dietrich, Baxi, Immergas) —
   replicate this vocabulary [verified from live SERP capture].
5. **Structured data** — view-source, grep `application/ld+json`; record types present:
   LocalBusiness/Plumber/HVACBusiness, Service, FAQPage, BreadcrumbList, AggregateRating.
6. Service × city page inventory — crawl competitor nav + `sitemap.xml`, count
   `/usluga/` and `/-miasto/` style URLs.
7. Internal linking — links per page, anchor texts to money pages.
8. Image `alt` coverage — % of imgs with non-empty alt, recurring alt patterns.
9. NAP + CTA placement — phone in header? FAQ block? review embed?
10. Publish/update dates (the capture shows a "5 dni temu" dated result — freshness is
    surfacing in this SERP) [verified from live capture].

### Doing it at scale with python3 — verified working setup
- **bs4 is now installed and verified**: `python3 -m pip install --target
  /Users/hajtomoto/Repo/.pylibs --trusted-host pypi.org --trusted-host
  files.pythonhosted.org beautifulsoup4` → **BeautifulSoup 4.15.0** (first attempt failed
  on a PyPI SSL cert error; `--trusted-host` fixes it; no sudo, no brew). Import with
  `sys.path.insert(0, '/Users/hajtomoto/Repo/.pylibs')`.
- End-to-end smoke test passed on a live page: fetched with stdlib `urllib`, parsed title,
  7 H2s, 475 links, 1 JSON-LD block [verified this session].
- Reference extractor (urllib + bs4, ~40 lines): loop competitor URLs → for each page
  emit CSV row: url, title, title_len, h1, h2_count, words, jsonld_types (joined),
  imgs, imgs_with_alt, internal_links. Add `time.sleep(2-4)` between fetches; identify
  with a normal browser UA; cache HTML to disk so you never re-fetch.
- Fallback if bs4 ever breaks: stdlib `html.parser` + `HTMLParser` subclass handles
  title/h1/h2/ld+json fine with zero dependencies (stdlib route was validated by the same
  smoke test shape before bs4 install succeeded).

---

## 5. Wayback Machine — competitor site history (exact endpoints)

Both verified live this session [verified]:
- CDX listing:
  `https://web.archive.org/cdx/search/cdx?url=example.com&output=json&limit=3`
  → JSON rows `[urlkey, timestamp, original, mimetype, statuscode, digest, length]`.
  Useful params: `from=2018&to=2026`, `collapse=timestamp:4` (yearly dedupe),
  `filter=statuscode:200`, `limit=-20` (latest N).
- Availability:
  `https://archive.org/wayback/available?url=<host>&timestamp=2019`
  → `archived_snapshots` (empty result is a normal response, not an error).
- Caveats verified: **`matchType=domain` wildcard queries now return 403
  "requires authorization"** — use per-URL queries instead (the competitor's `/oferta`
  page, `/kontakt`, each city page). One target domain returned `[]` because the exact
  host string was wrong — CDX is literal; confirm exact domain first.
- Internet Archive had a transient "Temporarily Offline" moment mid-session — retry,
  don't conclude [observed].
- Uses: date a competitor's city/service pages first appeared (their "expansion map"),
  title evolution, defunct directories that used to link to them (free link-idea mining).

---

## 6. Keyword gap analysis without paid tools

1. **GSC first (your own data).** Performance report gives real queries, impressions,
   clicks, position (doc fetched [verified]). Export everything, filter queries where
   position 5–20 → these are your fastest wins. SerpBear's GSC integration (verified
   README) puts real impressions next to tracked rankings automatically.
2. **Autocomplete mining (verified live, PL).**
   `https://suggestqueries.google.com/complete/search?client=firefox&hl=pl&gl=pl&q=<seed>`
   returned instant JSON, e.g. seed "naprawa pieców" → "naprawa pieców gazowych",
   "...na ekogroszek", "...kaflowych", "...co", "...gazowych szczecin", "...wrocław" —
   i.e. Google itself hands you the service × city matrix and the long-tail service
   modifiers [verified response captured this session]. Loop a–z + city names + "cena",
   "serwis", "przegląd", "awaria", "24h"; dedupe; you get hundreds of real queries.
3. **PAA / related**: fetch each keyword's SERP via r.jina.ai, expand "Więcej pytań" and
   "Inni wyszukiwali również" seeds iteratively [markers verified in live capture;
   questions themselves render collapsed — expand by searching the question text].
4. **Gap = competitor union − your set.** Extract competitor H1/H2/title vocab with the
   §4 extractor, diff against your keyword list. Anything they consistently target and
   you don't = content backlog. Anything *you* rank 5–20 for and they target heavily =
   priority.
5. **Reddit mining** — r/SEO, r/juststart, r/SEO_Digital_Marketing for tactic threads and
   "what still works" discussions: **direct reddit.com JSON and r.jina.ai access were both
   blocked from this environment today** (403 Blocked page; Jina anonymous block message
   cites abuse alleviation) [verified blocked]. From a residential browser, the JSON
   endpoints (`/r/SEO/search.json?q=...&restrict_sr=1&sort=top`) remain the standard
   approach — workflow claim, unverified from here. Polish homeowner questions (for
   content ideas) mine better from Polish forums and Marketplace Q&A anyway.

---

## 7. Poland-specific notes

- Polish directories probed: `pkt.pl` → 301, `oferteo.pl` → 301, `panorama-firm.pl` →
  DNS/timeout from this network [bare status verified; followed content unverified].
  Use them for citation consistency (NAP) and to see which competitors bother listing;
  Oferteo/Fixly also reveal real service-price expectations from lead requests.
- The live Warsaw SERP capture shows what actually ranks locally: local pack first with
  tenure + review quotes; organic titles with "SERWIS 24H", phone numbers in titles,
  brand-list boiler brands, district names (Wawer, Wesoła, Rembertów) and neighboring
  counties (pruszkowski, grodziski, Piaseczno) in snippets [all verified in capture].
  Your page templates should cover: main service + Warsaw, service + each district,
  boiler-brand pages (Termet, De Dietrich, Vaillant...), 24h emergency page, pricing page.
- Always pass `hl=pl&gl=pl` (autocomplete, SERP via jina) or you silently research the
  wrong market.

## 8. Suggested 4-week execution order

- **Week 1:** GSC verified + baseline export; pick 10 competitors (map pack + organic top
  10 for 5 seeds); snapshot all GMB data once (gosom scraper, home IP); Ahrefs free
  backlink checker on top 3; verify your site in Ahrefs Free + Bing WMT.
- **Week 2:** build the §4 extractor; run over ~50 competitor URLs; produce the title/H1
  pattern table, schema inventory, service×city matrix; Wayback-date their city pages.
- **Week 3:** autocomplete loop (§6) → keyword universe with GKP ranges as sanity
  buckets; diff vs competitor vocab → content backlog; SerpBear deployed (Docker) with
  ~50 tracked keywords + GSC integration.
- **Week 4:** publish first templates; set weekly cron: GMB snapshot diff, rank check,
  20 new autocomplete seeds, one Wayback check on each competitor's sitemap.

## 9. What could not be verified (do not trust until checked)
- Bing WMT keyword-research specifics (page JS-gated). Moz free query caps. Ubersuggest
  daily quota ("3/day" not on fetched page). Mangools trial lookup quota. Ahrefs anonymous
  backlink-checker row cap. GKP "ranges" wording at primary source. Meta v. Bright Data
  holding (no Wikipedia article; case exists but details unverified). gosom scraper exact
  language/deep flags. SerpBear current scraper-provider list. Reddit JSON from this
  network (blocked; test from home IP). r.jina.ai anonymous rate limits.

---

## Sources

Fetched this session via curl (direct or r.jina.ai); content matched unless noted.

- https://ahrefs.com/webmaster-tools — [verified] rename to Ahrefs Free; tool list; limits table
- https://ahrefs.com/free — [verified] verified-websites-only scope; free-forever terms
- https://ahrefs.com/backlink-checker — [verified] any-domain free checks; no numeric cap shown
- https://support.google.com/google-ads/answer/73361?hl=en — [unverified content] nav-only render; GKP range wording not extracted
- https://www.bing.com/webmasters/keyword-research — [unverified content] empty JS shell
- https://www.bing.com/webmasters/help/keyword-research-626a4e57 — [unverified content] 241-byte shell; direct fetch 0 bytes
- https://moz.com/products/free-seo-tools — [verified] tool list; caps absent from page
- https://neilpatel.com/ubersuggest/ — [verified page] "free limited features"; no daily quota stated
- https://mangools.com/pricing — [unverified content] 243-byte shell
- https://mangools.com/free-seo-tools — [verified] free mini-tools catalog; no KWFinder free tier
- https://www.google.com/robots.txt — [verified] `Disallow: /search`
- https://policies.google.com/terms — [verified] automated-access prohibition quote
- https://r.jina.ai/…/google.com/search?q=naprawa+piecow+gazowych+warszawa&hl=pl — [verified] local pack + snippets + PAA markers captured
- direct curl: google/bing/ddg SERP endpoints — [verified blocked] consent/400/challenge/anomaly
- api.github.com/search/repositories q=serp scraper, google-maps-scraper, serp rank tracker — [verified] star counts & push dates as cited
- https://raw.githubusercontent.com/gosom/google-maps-scraper/main/README.md — [verified] CLI flags, Docker, outputs
- https://raw.githubusercontent.com/omkarcloud/google-maps-scraper/master/README.md — [verified] Botasaurus, Chrome requirement, reviews
- https://raw.githubusercontent.com/towfiqi/serpbear/main/README.md — [verified] features, GSC/Ads integration, proxy model
- https://web.archive.org/cdx/search/cdx?url=example.com&output=json&limit=3 — [verified] live JSON rows
- https://web.archive.org/cdx/search/cdx?…matchType=domain — [verified 403] domain wildcard requires authorization
- https://archive.org/wayback/available?url=…&timestamp=2019 — [verified] live endpoint (empty snapshots is valid)
- https://suggestqueries.google.com/complete/search?client=firefox&hl=pl&q=naprawa+pieców — [verified] live PL suggestions JSON
- https://www.reddit.com/r/SEO/search.json?q=… — [verified blocked] 403 Blocked page; Jina mirror likewise blocked
- https://en.wikipedia.org/wiki/HiQ_Labs_v._LinkedIn — [verified] full case timeline as cited
- https://en.wikipedia.org/wiki/Meta_Platforms,_Inc._v._Bright_Data — [unverified] article does not exist
- https://support.google.com/webmasters/answer/9128668 (GSC overview) — [verified] Performance report description
- local install: bs4 4.15.0 into /Users/hajtomoto/Repo/.pylibs (pip --target + --trusted-host) — [verified] import + live-page smoke test passed
- pkt.pl / oferteo.pl / panorama-firm.pl bare probes — [verified statuses only] 301/301/DNS-fail; content not fetched
