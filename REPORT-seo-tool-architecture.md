# Self-Built SEO + AI-Citation Monitor — Architecture Report

**Project:** gas-seo (gas-services website, Poland) · **Date:** 2026-10-11
**Constraints:** zero paid SaaS · Apple Silicon Mac (macOS 26) · `/usr/bin/python3` only, no pip global
(pure-python deps via `pip --target ~/Repo/.pylibs`) · VPS available (same host serves the site backend)
· Telegram delivery already works · GitHub account `novakko` (**gh CLI auth expired — run `gh auth login`
before any push**; repo data below was pulled via anonymous api.github.com).

Everything marked **[verified]** was fetched from the primary source on 2026-10-11 (see Sources).
Judgment calls are marked **[assessment]**. Missing numbers are marked **unknown (not fetched)**.

---

## 1. TL;DR architecture

```
                    ┌──────────────────────────────────────────────┐
  OFFICIAL APIs     │  GSC searchanalytics   CrUX API    PSI API   │   free, verified quotas
  (daily/weekly)    │  IndexNow ping         Safe Browsing         │
                    └───────────────┬──────────────────────────────┘
                                    │
  SELF-SCRAPED       SERP top-20 (low cadence) · map-pack grid · GMB reviews
  (weekly, sampled)  AI-engine citation battery (prompt sampling)
                                    │
                    ┌───────────────▼──────────────┐
  STATE             │  sqlite (single file)        │  snapshots + raw JSON kept
                    │  + JSONL append log          │  dedup by content hash
                    └───────────────┬──────────────┘
                                    │
  DELIVERY          Telegram bot (already working) — alerts + weekly digest
```

- **Scheduling:** VPS cron is primary (stable IP, no quota). GitHub Actions is a free secondary
  for API-only pulls (2,000 min/month on Free — verified §7).
- **Ground truth for positions:** Google Search Console API is the only free, legal, high-cadence
  source of real Google position data. Scraping is a sparse supplement, not the base.
- **AI citations:** run a fixed prompt battery through engine APIs (Gemini has a free tier;
  OpenAI Free tier has a $100/mo usage cap) and, optionally, browser-driven website checks
  (the OneGlanse approach — effective but ToS-tensioned).

## 2. Free official APIs — verified limits (2026-10-11)

### Google Search Console API — FREE, generous
- "All use of Google Search Console API is free of charge" — official Pricing page [verified].
- Usage Limits page (canonical URL moved to `developers.google.com/webmaster-tools/limits`;
  the old `/about/quotas` path 404s) [verified]:
  - Search Analytics: **per-site 1,200 QPM, per-user 1,200 QPM; per-project 40,000 QPM /
    30,000,000 QPD**. Plus *load* quotas in 10-minute and 1-day chunks — queries grouped or
    filtered by page and query together are the most expensive; wide date ranges cost more.
  - URL Inspection: **per-site 2,000 QPD / 600 QPM; per-project 15,000 QPM / 10,000,000 QPD**.
  - All other resources: per-user 20 QPS / 200 QPM; per-project 100,000,000 QPD.
- Practical read [assessment]: 200 keywords × 1 query/day ≈ 6 QPM — nowhere near the QPM caps;
  the real ceiling is the *load* quota. Cheap pattern: 1-day date range, group by `query` only
  (not page+query) for the daily pull; do page+query grouping in one weekly deep pull.
- Auth: OAuth refresh-token flow needs no third-party libs (plain HTTPS POST to
  `oauth2.googleapis.com/token`). Service-account route needs RS256 JWT signing — doable with
  pure-python `pyrsa`/`google-auth` installed into `~/Repo/.pylibs` [assessment].

### PageSpeed Insights API — free, no published cap on the doc page
- v5 About page live [verified]; it documents response shape and the monthly CrUX BigQuery
  alternative. Numeric request quota: **not stated on that page — unknown (not fetched)**.
  Community reports of ~25k/day per key are **claim, unverified**.
- Works without a key (low rate) or with a key; flag `category=performance` and
  `strategy=mobile` are what you want. Run weekly per template URL — that's enough for trends.

### Chrome UX Report (CrUX) API — free, explicit cap
- **"150 queries per minute per Google Cloud project, which is offered without charge"**
  [verified, API reference page]. Origin-level daily refresh is fine within 150 QPM.

### Google Business Profile API — free but gated
- Access "requires a valid Google account, a legitimate business purpose, a Google Cloud
  project, and a business website URL" [verified, GBP API overview]. The old
  `basic-availability` eligibility page is **gone (verified 404)** — approval is by
  application form per Google Cloud project; approval criteria beyond the overview text:
  unknown (not fetched).
- What it gives you once approved: locations, reviews (read/reply), performance data,
  media, notifications [verified, overview feature list].
- Reality check [assessment]: approval is not instant and is meant for the business owner /
  tooling on their behalf. Plan a **scrape fallback** for review count/rating/velocity (§3).

### Bing Webmaster + IndexNow
- Bing Webmaster JSON API is live: `GET https://www.bing.com/webmaster/api.svc/json/
  GetUserSites?apikey=test` returned `{"ErrorCode":3,"Message":"ERROR!!! InvalidApiKey"}`
  [verified — endpoint alive; bad key rejected]. Full API docs on learn.microsoft.com have
  moved (old URL 404); current doc location: unknown (not fetched). Get a key from
  bing.com/webmaster → Settings → API access.
- IndexNow protocol [verified, indexnow.org/documentation]: key = 8–128 hex chars, hosted at
  `https://example.com/<key>.txt`; submit `GET https://api.indexnow.org/indexnow?url=...&key=...`
  or POST JSON with up to **10,000 URLs per request**. Used by Bing, Yandex, Seznam, Naver
  and others. Zero cost. Wire this to your backend's "content changed" event.

### Google Safe Browsing API — free, non-commercial only
- "The Safe Browsing API is for non-commercial use only… If you need a solution for commercial
  purposes, please refer to Web Risk" + "There is no cost for use of this API"; default quota
  visible and raisable in the Developer Console [verified, Usage Restrictions page].
- For a business monitoring its own site this is effectively fine at tiny scale; if the tool
  is ever sold as a service, use Web Risk instead [assessment on the boundary].

### Google Autocomplete — unofficial
- `https://suggestqueries.google.com/complete/search?client=firefox&q=ogrzewanie` returned
  live JSON suggestions (Polish queries verified) [verified — endpoint works today].
- `google.com/robots.txt` disallows `/search` [verified]. Autocomplete itself isn't listed in
  robots.txt; automated harvesting sits in a ToS grey zone — Google's ToS text was not
  fetched; treat heavy autocomplete mining as **claim: unofficial, unverified legality**.
  Practical use: keyword-expansion suggestions in Polish, low cadence, cached forever
  (suggestions change slowly) [assessment].

### Wayback CDX API — free
- CDX Server API docs live on GitHub [verified]; the endpoint responded normally to queries
  during this research. Use for: "did this page exist before", competitor history, recovering
  removed pages. Availability API (`archive.org/wayback/available`) also live [verified by use].

## 3. What must be self-scraped (vs API)

| Data | API available? | Plan |
|---|---|---|
| Own positions, impressions, CTR | GSC API (free, verified) | daily pull, ground truth |
| SERP positions for any keyword | NO official API | scrape top-20, weekly, sampled |
| Map-pack / local grid position | NO API (GBP API ≠ rankings) | 3×3 or 5×5 grid scan, monthly |
| Competitor GMB reviews | GBP API only for OWN properties | scrape competitor listing pages |
| AI citations (ChatGPT/Claude/Gemini) | paid APIs (§5) | API battery + web check |
| CWV field data | CrUX + PSI APIs (free) | no scraping needed |

### Scraping-risk evidence (verified sources only)
- **hiQ Labs v. LinkedIn** (9th Cir., docket 17-16783): published opinions filed 2019-09-09
  and 2022-04-18; remand docket in D. Ariz. (2:22-mc-00025, opened 2022-05-25) [verified via
  CourtListener API]. The 2022 ruling's gist (scraping public pages isn't a CFAA "access"
  violation) is widely reported but the opinion PDF could not be fetched from ca9.uscourts.gov
  this session (404) — **holding text: unverified**. The parties settled afterwards
  (**claim, unverified**).
- **Van Buren v. United States** (SCOTUS 19-783): opinion PDF retrieved from supremecourt.gov
  [fetched; text not parsed this session]. It narrowed CFAA "exceeds authorized access" —
  US-law context only.
- **Meta Platforms v. Bright Data** (N.D. Cal., 3:23-cv-00077, filed 2023-01-06; mirror case
  Bright Data v. Meta, D. Del. 1:23-cv-00073) [verified via CourtListener]. The ruling on
  Meta's claims (reported: granted Bright Data's motion to dismiss — scraping public data
  ≠ breach of Facebook's terms for a non-subscriber) — **claim, unverified; ruling text not
  fetched**. Docket 745 PDF: not retrievable (403).
- **DOJ CFAA charging policy** (May 2022 statement: no prosecution of good-faith ToS
  violations): both live justice.gov URL and its archive redirect return a bot-wall (401) —
  **content unverified at source**.
- Google-specific: `google.com/robots.txt` disallows `/search` [verified]. Google's SERP ToS
  position (no automated querying) was **not fetched** — it is policy plus contract, not
  criminal law; the practical enforcement pattern is IP blocks and CAPTCHAs, not lawsuits
  against individuals tracking 200 keywords [assessment]. Poland/EU: the CFAA case law above
  is US law; no EU/Polish equivalent was researched in this session — **unknown (not fetched)**.

**Bottom line [assessment]:** scraping Google SERP is contractually prohibited and technically
hostile, but enforcement against small trackers is practically anti-bot, not legal. The
architecture therefore: (a) makes GSC the base truth, (b) scrapes rarely, small, and politely,
(c) never mixes scraping traffic with API traffic, (d) accepts that a scraped-positions feed
can break any week and degrades gracefully (gaps, not wrong data).

## 4. AI-engine citation monitoring

Provider facts (verified on official docs, 2026-10-11):

- **OpenAI**: tiers Free ($100/mo usage cap) / Build ($5 credit purchase → $500/mo) / Launch
  ($100 → $5k) / Grow ($500 → $200k); RPM+TPM per model; org- and project-level limits;
  responses carry `x-ratelimit-remaining-*` and sometimes `Retry-After` [verified].
- **Anthropic**: tiers Start/Build/Scale with monthly spend caps $500 / $1,000 / $200,000;
  new orgs start in an "Evaluation tier" below standard limits; token-bucket rate limiting;
  429 + `retry-after` on rate limits [verified]. No free tier listed on the page.
- **Gemini API**: free tier and paid tiers exist with per-model RPM/TPM; the free-tier numeric
  table renders client-side and could not be extracted — specific free RPM/TPM: **unknown
  (not fetched)** [tier existence verified].
- **Perplexity**: official API is paid (Orchestrator / Agent-with-citations / Search /
  Embeddings products; no free tier advertised on the overview page) [verified].
- **Copilot**: no public API for citation checking found — **unknown (not fetched)**.

### Battery design [assessment, mechanics; numbers are starting defaults]
- Fixed battery of 20–40 Polish prompts per service×city cell ("ile kosztuje wymiana kotła
  gazowego Warszawa", "naprawa pieców gazowych 24h", …) + brand-specific prompts.
- n=3–5 samples per prompt per engine, spread across hours/days — LLM answers are
  nondeterministic and time-varying; single-shot measurement is noise.
- Metrics per engine: `mention_rate` (runs naming the brand / total), `source_rate` (brand
  domain cited), `answer_position` (first mention index), `competitor_overlap`.
- Store raw answers (hash-deduped) — you will need to re-read them when scoring changes.
- Score with a cheap model where possible; OneGlanse's README honestly notes its scores are
  the analysis model's *reading* of saved answers, not scores returned by the sites [verified].
- Two access modes:
  1. **API mode** (default): Gemini free tier + OpenAI Free tier ≈ €0/mo for a small battery;
     deterministic to schedule, easy rate limiting via provider headers.
  2. **Website mode** (optional, cf. OneGlanse, MIT, drives the real ChatGPT/Gemini/Perplexity
     websites with your accounts): captures what customers actually see (web answers differ
     from raw-API answers), but automated website use sits against the engines' ToS — their
     ToS texts were not fetched this session; treat as **risk-accepted, unverified**.

## 5. Data model (sqlite — one file, WAL mode)

```sql
keywords(id, phrase, city, service, priority, active)
serp_snapshots(id, keyword_id, day, engine, position, url_found, raw_hash,
               fetched_at, src)             -- src: gsc|serp_scrape
gsc_daily(id, day, query, page, clicks, impressions, ctr, position)
grid_checks(id, day, point_lat, point_lng, keyword_id, pack_pos, own_present)
gbp_reviews(id, day, source, author, rating, text_hash, replied, scraped_at)
review_stats(id, day, location, count_total, rating_avg, velocity_30d)
ai_prompts(id, battery, prompt, engine, sample_no, run_day)
ai_answers(id, prompt_id, run_ts, answer_hash, mentions_brand, brand_pos,
           cited_domains, raw_path)
cwv(id, url, day, lcp_p75, inp_p75, cls_p75, source)   -- crux|psi
content_events(id, ts, url, kind)                       -- drives IndexNow pings
alerts(id, ts, rule_id, severity, payload, sent_tg)
meta(key, value)                                        -- cursors, etags, quotas
```

Dedup + storage rules: raw HTML/JSON answers to disk as `<hash>.json`, hash in sqlite;
never store the same fetched payload twice; JSONL append-only log for rebuildability.

## 6. Metrics + alerting for a local-services site

Daily automatics: GSC pull (queries+pages), IndexNow ping on `content_events`,
review-count check (own + 3 competitors), AI battery on its scheduled slice.
Weekly: SERP spot-check of money keywords, PSI per template URL, CrUX refresh.
Monthly: map-pack grid scan, full-battery AI run, Safe Browsing check of own domain.

Alert defaults [assessment — tuning is your judgment]:
- money-keyword position drop ≥ 3 slots day-over-day (confirm vs GSC before alerting);
- map-pack: own pin leaves top-3 at any grid point it previously held;
- review velocity goes negative or any new review ≤ 3★ (fast reply window);
- AI `mention_rate` drops ≥ 20% week-over-week on any engine (min sample 15 runs);
- CWV regression: LCP p75 > 2.5 s, INP > 200 ms, CLS > 0.1 [thresholds verified on
  web.dev/articles/vitals] — alert on CrUX p75 crossing, not PSI lab numbers;
- GSC impressions drop ≥ 30% w/w on a stable query set;
- dead-man switch: no successful GSC sync in 36 h → Telegram "monitor is down".

## 7. Scheduling: VPS cron vs GitHub Actions (verified numbers)

GitHub Actions current limits page (canonical URL moved to `/actions/reference/limits`;
old usage-limits URLs 404) [verified]: **Free plan: 500 MB storage, 2,000 min/month,
10 GB artifacts, 20 concurrent jobs**; `GITHUB_TOKEN` limited to **1,000 requests/hour/repo**.
- Fits easily: your whole workload ≈ 5–20 min/day of runner time.
- Weakness for scraping: runner egress IPs are datacenter ranges — anti-bot walls bite harder
  than from a VPS or home IP [assessment]. GHA is perfect for API pulls, IndexNow pings, PSI,
  GSC sync, Telegram digests; wrong place for Google scraping.
- VPS cron: no minute quota, static IP you control, shares the backend's network. Use
  lockfiles + jittered start minutes per job; one job = one process = one log file.
- Mac: dev only; don't schedule on a laptop that sleeps.
- Recommendation: GHA for the API layer (free-forever, quota verified), VPS cron for scraping
  + AI battery, both writing to the same sqlite file via the VPS (GHA jobs can SSH-push results
  or open a PR of JSONL — keep one writer for sqlite to avoid corruption) [assessment].

Fragility ranking (honest): GSC/PSI/CrUX/IndexNow/Wayback APIs — stable free-forever;
Gemini free tier — can change quarterly; OpenAI Free tier — promo-like, may tighten;
Google SERP scraping — breaks most often; GBP API approval — administrative risk;
Bing API docs location — already moved once (404 verified); gh CLI — re-auth needed now.

## 8. Anti-fragility playbook

- **Rate-limit respect:** on 429/403 read `Retry-After` (OpenAI/Anthropic verified to send
  it; Google returns plain 429) and back off exponentially with jitter. Never retry more
  than 3×. Log every 429 in `meta`.
- **Caching:** sqlite-backed HTTP cache with ETag/If-Modified-Since where servers send them;
  autocomplete + CDX results cached forever (append-only knowledge); PSI results cached 7 days.
- **Quota budget [assessment]:** GSC ≤ 100 queries/day (1 pull + re-runs), URL Inspection
  ≤ 200/day (cap is 2,000/site), PSI ≤ 50/day, CrUX ≤ 500/day, AI battery ≤ 300 runs/day.
  All ≪ verified caps — headroom is the reliability feature.
- **Anti-bot politeness (Google scraping):** ≤ 1 request / keyword / day, spread with jitter
  over 3 h windows; no two engines share cookies; real `Accept-Language: pl-PL`; full-stop
  abort on CAPTCHA (open gap in data, alert, wait 48 h). No proxy purchases — if a proxy
  becomes necessary, the design has already failed; fall back to GSC-only truth [assessment].
- **Dedup:** content-hash every payload before insert; keyword×day×engine unique index;
  AI answers deduped by hash so identical answers cost one row.
- **AI nondeterminism:** fixed seed/temp-0 where the API allows; still sample n=3 because
  engines A/B silently; majority-vote the mention label; keep per-run raw text.
- **Graceful degradation:** every collector writes `meta.last_ok`; Telegram digest prints a
  coverage matrix so silent failures are visible.

## 9. Open-source to borrow from (api.github.com search, 2026-10-11)

| Repo | Stars | License | Pushed | Note |
|---|---|---|---|---|
| towfiqi/serpbear | 2,108 | MIT | 2026-05-14 | rank tracker; scraper-APIs + GSC |
| serphacker/serposcope | 757 | MIT | 2024-01-22 | archived "legacy" — ideas only |
| crawlseo/crawlseo | 630 | MIT | 2026-10-06 | GSC + crawler + CWV dashboard |
| oneglanse/oneglanse | 211 | MIT | 2026-10-04 | AI-visibility tracker (websites) |
| joshcarty/google-searchconsole | 255 | MIT | 2025-11-15 | clean GSC API wrapper |
| databluedev/searchmirror | 111 | AGPL-3.0 | 2026-10-01 | needs paid SERP credits |
| jakob-bagterp/index-now-for-python | 8 | MIT | 2026-10-11 | tiny IndexNow client |

- serpbear: live rank checks ride third-party scraper APIs (ScrapingAnt/SerpApi/proxies) +
  GSC integration — self-hosted Next.js.
- oneglanse: drives the real ChatGPT/Gemini/Perplexity websites with BYO accounts; honestly
  labels its scores as the analysis model's *reading* of saved answers, not native scores.
- searchmirror: honest BYO-key caveats, but REQUIRES paid DataBlue SERP credits; legacy
  Django 3.2/Mongo 4.4 stack; AGPL — read, don't depend.
- index-now-for-python: v1.0.25, Python 3.11–3.14+, MIT.

Steal: SerpBear's GSC integration model + notification cadence; OneGlanse's answer-scoring
pipeline and honest "scores are our model's reading" labeling; searchmirror's BYO-key
security posture (encrypt provider keys at rest). Avoid dependency on anything AGPL unless
you accept copyleft on your tool [assessment].

## 10. Build order

1. **GSC sync** (OAuth refresh token, stdlib urllib; daily pull → `gsc_daily`) + Telegram
   heartbeat. Deliverable: weekly positions digest in Telegram.
2. **IndexNow + content_events** wired to the site backend (this is a day, not a week).
3. **PSI + CrUX weekly** for the 5–10 template pages; CWV table + regression alerts.
4. **AI battery v1**: Gemini free tier + OpenAI Free tier, 20 prompts × n=3, weekly;
   manual scoring first, model-scoring later.
5. **SERP spot-checker** on the VPS (money keywords only, weekly, polite).
6. **GBP**: apply for API access now (approval takes time); scrape fallback meanwhile.
7. **Grid scans + review velocity** last — highest scraping risk, moderate value at first.

## 11. Unknowns (explicit)

- PSI API numeric quota — unknown (not fetched); ~25k/day per key is community claim only.
- Gemini free-tier numeric RPM/TPM — unknown (not fetched; client-rendered table).
- Bing Webmaster API docs current URL + rate limits — unknown (not fetched; old docs 404,
  endpoint itself verified live).
- GBP API approval criteria beyond overview text — unknown (not fetched; eligibility page 404).
- Google ToS / Autocomplete harvesting legality — not fetched; treat as grey zone.
- EU/Polish-law treatment of SERP scraping — not researched this session.
- hiQ 2022 opinion text, Meta v Bright Data ruling text, DOJ CFAA policy text — sources
  404/bot-walled; holdings reported as claims, dockets verified.

## Sources

Fetched 2026-10-11 unless noted. [verified] = HTTP 200 + content matched expectation.

1. https://developers.google.com/webmaster-tools/pricing — GSC API free of charge [verified]
2. https://developers.google.com/webmaster-tools/limits — full GSC quota numbers [verified]
3. https://developers.google.com/webmaster-tools/about — GSC API overview [verified]
4. https://developers.google.com/webmaster-tools/search-console-api-original/v3/searchanalytics/query — searchanalytics reference [verified]
5. https://developers.google.com/webmaster-tools/about/quotas — [verified 404; page moved]
6. https://developers.google.com/speed/docs/insights/v5/about — PSI API [verified]
7. https://developers.google.com/web/tools/chrome-user-experience-report/api/reference — CrUX "150 queries/min, free" [verified]
8. https://developers.google.com/safe-browsing/v4/lookup-api — Lookup API doc [verified]
9. https://developers.google.com/safe-browsing/v4/usage-limits — non-commercial-only terms [verified]
10. https://developers.google.com/my-business/content/overview — GBP API eligibility/features [verified]
11. https://developers.google.com/my-business/content/basic-availability — [verified 404; page removed]
12. https://ai.google.dev/gemini-api/docs/rate-limits — tiers exist; numbers client-rendered [verified page; numbers unknown]
13. https://suggestqueries.google.com/complete/search?client=firefox&q=ogrzewanie — live JSON [verified]
14. https://www.google.com/robots.txt — Disallow /search [verified]
15. https://www.indexnow.org/documentation — key spec, 10,000 URLs/request [verified]
16. https://www.bing.com/webmaster/api.svc/json/GetUserSites?apikey=test — InvalidApiKey response [verified]
17. https://learn.microsoft.com/en-us/bing/webmaster/docs/sdks-samples-and-resources/apis — [verified 404; docs moved]
18. https://raw.githubusercontent.com/internetarchive/wayback/master/wayback-cdx-server/README.md — CDX API [verified]
19. https://web.archive.org/cdx/search/cdx?… (several queries) — CDX responds [verified by use]; note: no captures exist of the moved GSC/Bing/GH pages (empty results)
20. https://docs.github.com/en/actions/reference/limits — Free 500 MB / 2,000 min / 20 jobs; GITHUB_TOKEN 1,000 req/h [verified]
21. https://docs.github.com/en/actions/concepts/billing-and-usage — billing concepts [verified]
22. https://docs.github.com/en/actions/reference/usage-limits-billing-and-billing-faqs — [verified 404; URL moved]
23. https://core.telegram.org/bots/faq — 20 msg/min per group; ~30 msg/s bot cap; broadcast pacing [verified]
24. https://www.courtlistener.com/api/rest/v4/search/ (queries: hiQ Labs; Meta Bright Data) — dockets 17-16783, 2:22-mc-00025, 3:23-cv-00077, 1:23-cv-00073 [verified]
25. https://www.supremecourt.gov/opinions/20pdf/19-783_k53l.pdf — Van Buren PDF [fetched 200; text not parsed]
26. https://cdn.ca9.uscourts.gov/datastore/opinions/2022/04/18/21-5539.pdf — [verified 404]
27. https://www.justice.gov/opa/pr/department-justice-changes-original-computing-fraud-and-abuse-act-cfaa-policy — bot-wall 302→401 [unverified content]
28. https://www.justice.gov/archives/opa/pr/department-justice-changes-original-computing-fraud-and-abuse-act-cfaa-policy — bot-wall 401 via reader proxy [unverified content]
29. https://www.courtlistener.com/docket/67433248/meta-platforms-inc-v-bright-data-ltd/ — [verified 403 to curl]
30. https://platform.openai.com/docs/guides/rate-limits — tiers incl. Free $100/mo cap; header behavior [verified via reader proxy]
31. https://docs.anthropic.com/en/api/rate-limits — tiers/caps/token bucket/429 behavior [verified via reader proxy]
32. https://docs.perplexity.ai/getting-started/overview — paid product line [verified via reader proxy]
33. https://web.dev/articles/vitals — LCP 2.5 s / INP 200 ms / CLS 0.1 [verified]
34. https://api.github.com/search/repositories?q=… (serp rank tracker; seo monitoring self-hosted; indexnow python; google search console api python) — star/license/pushed data [verified 2026-10-11; counts drift daily]
35. https://raw.githubusercontent.com/towfiqi/serpbear/main/README.md — scraper-based architecture [verified]
36. https://raw.githubusercontent.com/databluedev/searchmirror/main/README.md — BYOK/credits caveats, AGPL [verified]
37. https://raw.githubusercontent.com/oneglanse/oneglanse/main/README.md — website-mode AI tracking rationale [verified]
38. https://raw.githubusercontent.com/jakob-bagterp/index-now-for-python/master/README.md — v1.0.25, MIT [verified]

Reader-proxy note: OpenAI/Anthropic/Perplexity/onegle-hub pages were fetched through
r.jina.ai (JS rendering); content attributed to the destination URLs.
