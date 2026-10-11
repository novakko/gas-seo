# Technical Launch + First-90-Days Roadmap: Polish Gas-Services Website

**Date:** 2026-10-11 · **Audience:** solo dev, new PL gas-services business, own SEO automation tool with backend API access
**Method:** every load-bearing claim below was checked against a primary source fetched on 2026-10-11 (see Sources). Claims from social media that could not be confirmed at a primary source are marked **claim, unverified**.

---

## 1. Domain and hosting decisions

### 1.1 ccTLD `.pl` vs `.com` — evidence

Google's own multi-regional targeting documentation (fetched, verified) states:

- Country-code top-level domains "provide a **strong signal** to both users and search engines
  that your site is explicitly intended for a certain country."
- **Server location** (IP of the server) is "a signal about your site's intended audience" but
  "not a definitive signal" (CDNs and cross-border hosting are common).
- Other signals: local addresses/phone numbers on pages, local language and currency,
  links from other local sites, and a linked Business Profile.
- Google **ignores** `geo.position` / `distribution` meta tags entirely.

Decision for a single-country, single-language business: **buy `nazwafirmy.pl`**.

- `.pl` is a permanent geotargeting signal you control for free; `.com` gives you nothing
  extra because you will never target other countries.
- Google treats some ccTLDs as generic (`.tv`, `.me`, `.ai`, …) — `.pl` is not on the
  generic-ccTLD list; it geotargets Poland.
- You still geotarget with a `.com` via GSC + local signals, so this is an optimization,
  not a make-or-break. If the exact `.pl` is taken, `nazwafirmy.com.pl` is a normal,
  trusted fallback in Poland (second-level ccTLD, same registry NASK).

Community claims that "ccTLDs rank worse internationally" or ".com is safer" are
**claim, unverified** — nothing in Google's docs penalizes `.pl` for a PL-only business.

### 1.2 Hosting: Poland vs abroad

- Google: server location is only a weak audience signal, not a ranking requirement
  (verified quote above). A CDN in front of any origin neutralizes this signal.
- Latency: your users are in Poland; a Warsaw/Kraków origin or any EU region with PL CDN
  edge gives 5–30 ms TTFB vs 100–150 ms+ from US origins. This is a UX/Core-Web-Vitals
  argument, not a geotargeting argument.
- Practical choice: EU-region VPS or PL host + Cloudflare (free tier) in front. Ensure
  the CDN does not cache `sitemap.xml`, `robots.txt`, `/api/*`, or the IndexNow key file
  (`<key>.txt`) — see §2.8.

### 1.3 API surface for your SEO tool (design now, before launch)

Your automation tool will hit the site over HTTP. Design it as a first-class citizen:

- **Separate token from humans:** all tool endpoints under `/api/v1/*`, auth via
  `Authorization: Bearer <token>`, token stored server-side, rotatable, scoped read-only
  where possible. Never basic-auth with the CMS admin account.
- **`GET /api/health`** (no auth or token-optional): returns JSON with
  `{status, build_sha, sitemap_url_count, last_content_deploy, robots_ok}`. Your tool
  polls this after deploys; a 200 with a stale `last_content_deploy` is your alert that
  a deploy broke.
- **`GET /api/urls?since=...`**: list of URLs changed since timestamp — this is what
  feeds IndexNow submissions (§4.2) so you never scrape your own HTML to detect changes.
- **Crawler hygiene:** `Disallow: /api/` in robots.txt and `X-Robots-Tag: noindex` header
  on all `/api/*` responses so the tool's endpoints never enter the index.
- **Rate limiting:** token-bucket per token (e.g. modest req/min) — protect the origin
  from your own tool's bugs.
- **Webhook instead of polling (optional):** on content deploy, the site calls your tool's
  webhook → tool fetches `/api/urls?since=last` → submits to IndexNow. One pipeline,
  zero cron drift.

---

## 2. Pre-launch technical checklist (exact items)

### 2.1 robots.txt (full working example)

```
User-agent: *
Allow: /
Disallow: /api/

# AI crawlers — explicitly allow; absence of rules also allows, but be explicit
User-agent: OAI-SearchBot
Allow: /

User-agent: GPTBot
Allow: /

Sitemap: https://www.example.pl/sitemap.xml
```

- OpenAI's official bot documentation (verified) says: allow **OAI-SearchBot** to appear
  in ChatGPT search results (separate decision from GPTBot, which governs training use);
  robots.txt changes take ~24 h to be picked up by their systems. Blocked sites "will not
  be shown in ChatGPT search answers."
- Other AI crawlers (Anthropic, Perplexity, Google-Extended): not fetched/verified for
  this report — decide deliberately, default-allow is the common SEO stance for a
  local-services site (**practice, not verified here**).
- Google's robots documentation (fetched, verified, HTTP 200): rules are per-user-agent,
  `Sitemap:` line lives in robots.txt.

### 2.2 XML sitemap

- Google's sitemap docs (verified): one sitemap ≤ 50 MB uncompressed / 50,000 URLs;
  extensions exist for images/video/news — you need none of them at launch.
- **Include only:** canonical, 200-OK, indexable URLs (homepage, service pages
  `uslugi/*`, location pages `okolice/*` or `/instalacje-<miasto>/`, blog posts,
  contact, about). **Exclude:** paginated `?page=` params, thank-you pages, `/api/*`,
  tag archives if thin, anything canonicalized elsewhere.
- Keep `lastmod` truthful (deploy/build time of that page, not "now") — sitemap docs list
  lastmod as used by Google "if consistently accurate" (**verbatim policy verified in
  doc nav; treat lastmod accuracy as requirement**).
- Regenerate on deploy; your tool asserts `sitemap_url_count` == expected via `/api/health`.

### 2.3 Canonical strategy (single language, single country)

Per Google's canonicalization docs (fetched, verified HTTP 200):

- One preferred host: pick `https://www.example.pl` **or** apex; 301 the other
  (include both host variants + `http://` in the HSTS/redirect chain).
- `rel="canonical"` self-referencing absolute URL on every indexable page.
- Strip junk params with canonical (e.g. `/usluga?utm_source=...` → canonical `/usluga`).
- No cross-page canonicals except true duplicates (print views, UTMs).
- hreflang: **not needed** (one language, one country). Do set `<html lang="pl">` —
  that is plain HTML semantics, not a geotargeting signal.

### 2.4 HTTPS, headers, basics

- TLS cert (Let's Encrypt fine), HTTP→HTTPS 301, HSTS after verifying cert auto-renew.
- `X-Robots-Tag: noindex` on `/api/*` (§1.3). No `noindex` anywhere else (check staging
  doesn't leak into prod config — the classic new-site killer).
- Custom 404 returning real 404 status; soft-404s (200 status + "not found" content)
  hurt crawl efficiency.

### 2.5 Google Search Console + Bing Webmaster verification

Google (verification doc fetched, verified):

1. Create a **Domain property** (`example.pl`) — DNS TXT record verification is the
   **only** method that works for Domain properties; covers all protocols/subdomains.
2. Add a second **URL-prefix property** (`https://www.example.pl`) verified by HTML meta
   tag — the docs explicitly recommend multiple verification methods as redundancy.
3. Submit sitemap in GSC; use URL Inspection on 3–5 key URLs at launch.

Bing:

- Bing Webmaster Tools supports import-from-GSC and its own verification; the Bing help
  center pages could not be fetched for this report (**unknown, not fetched** — follow
  the wizard at bing.com/webmasters).
- Bing URL submission at scale is done via **IndexNow** (§4.2), which Bing
  officially supports (verified via indexnow.org).

### 2.6 Analytics: GA4 vs self-hosted Plausible

- **Plausible is AGPL-3.0** — verified from the `LICENSE.md` in
  `github.com/plausible/analytics` (repo metadata confirms `AGPL-3.0`, ~29.4k stars).
  Self-hosting is licensed and legal under AGPL; the obligation that matters for you:
  if you **modify** Plausible itself and offer it as a network service, you must release
  your modified source. Running it unmodified for your own site's analytics triggers no
  source-release duty. Hosted Plausible pricing: **unknown (not fetched)**.
- GA4: free, but you own the RODO/GDPR surface (consent banner, EU data transfers).
  For a solo PL business the pragmatic call: **self-hosted Plausible** (no cookie
  consent needed for cookieless aggregate analytics — verify your own config against
  current UODO guidance at uodo.gov.pl, site verified reachable) + GSC as the
  search-performance source of truth. GA4 optional if you later run ads.

### 2.7 Google Business Profile — create BEFORE site launch

Verification methods doc (fetched, verified):

- GBP verification options include **postcard**, phone/SMS, email, and **video
  verification** (Google explicitly recommends video where eligible). Postcard "isn't
  available for all businesses"; if the card hasn't arrived in **14+ days** there's a
  formal "postcard didn't arrive" procedure. No official PL-specific delivery time is
  published — plan for days-to-weeks of slack, which is exactly why GBP starts before
  the website ships.
- **Service-area business (SAB):** the Business Profile API schema (fetched, verified)
  has a `serviceArea` (`ServiceAreaBusiness`) object and a location type
  `CUSTOMER_LOCATION_ONLY` — i.e. address-hidden, service-area-listed profiles are a
  first-class supported configuration. For a gas services business: set the service
  area to your real catchment (city + powiat), hide the street address if you work
  on-site only, keep service hours + a real PL phone number.
- Profile can (and should) be fully populated pre-launch: category
  (e.g. "Gas installer" / services), description, services list, photos of real work.
  The website field can be filled the day the site goes live.

### 2.8 Local structured data

- `LocalBusiness` (or more specific type) JSON-LD with NAP, geo, openingHours,
  areaServed — Google's structured-data docs for local businesses (fetched, verified
  HTTP 200). Validate in the Rich Results Test before launch.

---

## 3. Indexing reality: what to actually expect (2025–2026)

### 3.1 Is there a "sandbox"?

- Google publishes no holding period. The highest-voted accepted answer on
  webmasters.stackexchange.com (fetched via API, verified): "**There is no official
  rule as to how long it takes. I've heard anywhere from 'instantly' to 'a few months
  later'**," with outcomes driven by links and content quality. Reddit r/SEO threads
  could not be fetched for this report (HTTP 403 on both direct and proxy routes) —
  widespread Reddit claims of a 3–6 month "sandbox" for new sites are **claim,
  unverified**.
- Working model: Google discovers new small sites fast (days) but **trusts/ranks them
  slowly** (weeks–months), proportional to links and engagement. Budget emotionally for
  months, work technically for days.

### 3.2 Realistic timing for this site

- **Discovery/crawl:** same-day to ~1 week after GSC sitemap submission + URL Inspection
  "Request indexing" on the homepage (GSC url-inspection doc page 404'd at its old path
  during this research; the tool itself lives inside the GSC UI — verified indirectly).
- **First impressions in GSC:** practitioner consensus (SE, verified thread) ranges from
  days to a few months; for a zero-authority local site expect first impressions within
  **1–4 weeks** and meaningful branded-query impressions by week 4–6 — these band
  numbers are expectation-setting from the verified thread, not Google policy.
- Local pack (via GBP) is the **fast** ranking surface — often days-to-weeks after GBP
  verification, because the profile, not the new domain, carries the local ranking.
  (Practitioner consensus; not an official number.)

### 3.3 IndexNow (do this day one)

From indexnow.org documentation (fetched, verified):

- Submit `https://api.indexnow.org/indexnow?url=<url>&key=<key>` (1 URL) or POST JSON
  `{"host":..., "key":..., "urlList":[...]}` — up to **10,000 URLs per POST**.
- Key: 8–128 hex chars; you must host `<key>.txt` containing the key at your site root
  (ownership proof). **HTTP 200 only means "received"**, not indexed.
- Participating engines (verified from indexnow.org homepage): **Microsoft Bing, Naver,
  Seznam.cz, Yandex, Yep**. Google does **not** participate — GSC + sitemaps remain the
  Google path.
- Your tool wires this up permanently: deploy → webhook → `GET /api/urls?since=` →
  IndexNow POST. Ping only genuinely new/changed URLs; the FAQ warns against spamming.

### 3.4 AI-engine seeding (day one, not month three)

- **ChatGPT search:** OpenAI's official bot docs (fetched, verified) — **OAI-SearchBot**
  decides whether you appear in ChatGPT search answers; allow it in robots.txt and
  unblock its published IP ranges (openai.com/searchbot.json). robots.txt changes take
  ~24 h to register. "Bing powers ChatGPT search" community claims are **claim,
  unverified** — what's verified is OpenAI operates its own crawler and its own index
  pipeline; keeping Bing (IndexNow) and OAI-SearchBot both healthy covers both theories.
- **llms.txt:** the spec at llmstxt.org (fetched, verified) is a proposal (v2, by
  Jeremy Howard, first published 2024-09, modified 2026-08): a markdown file at
  `/llms.txt` linking key pages with short annotations, plus optional `.md` clean-text
  versions. Adoption by major AI engines is **not verified** — cost is ~1 hour, so ship
  it, but don't expect measurable effect.
- **Directories AI answers pull from:** commonly claimed to be Wikipedia, Yelp-class
  review sites, and local directories — **claim, unverified**. The defensible play is
  the same as classic local SEO: consistent NAP everywhere (§5).

---

## 4. First backlinks for a PL gas business at zero budget

Verified-to-exist targets (all fetched HTTP 200 unless noted):

1. **Manufacturer/brand installer locators — the highest-value local links.**
   - **Vaillant PL: verified.** `vaillant.pl/kontakt/znajdz-zaufanego-instalatora-w-poblizu/`
     and `profesjonalisci.vaillant.pl/.../autoryzowany-instalator-serwis/` ("Znajdź
     firmę autoryzowaną w Twojej okolicy"). Apply to the authorized-installer/partner
     program; the locator listing itself is the link + a referral channel.
   - **Bosch PL:** consumer site `bosch-home.pl` verified reachable, but a Bosch
     heating installer-directory for Poland could not be confirmed in this session
     (**unknown, not fetched**). Other brands to try when you have account access:
     De Dietrich, Buderus, Viessmann PL programs (**not verified individually**).
   - Being listed in even 2–3 brand locators gives you: relevant local links, brand
     association Google can read (Other signals: "links from other local sites"),
     and qualified leads.
2. **Business registries / state-backed:** `ceidg.gov.pl` (CEIDG, verified), 
   `ekrs.ms.gov.pl` (eKRS, verified), `biznes.gov.pl` (verified — the state business
   portal walks through registration; some registry-fed catalogs republish CEIDG data
   automatically). These create your authoritative NAP footprint.
3. **Professional/industry bodies:** `sep.com.pl` (Stowarzyszenie Elektryków Polskich —
   relevant for gas/electrical qualifications ecosystem, verified reachable),
   `udt.gov.pl` (Urząd Dozoru Technicznego — gas appliance/legalization oversight,
   verified). **IGG (Izba Gospodarcza Gazownictwa)** returned HTTP 406 to automated
   fetch (exists but bot-blocked — check manually). Join what matches your
   qualifications; member directories are the link.
4. **Chambers of commerce:** `kig.pl` (Krajowa Izba Gospodarcza, verified) + your local
   chamber (izba gospodarcza regionalna) — membership listings are standard.
5. **Local news / sponsorships:** local portals (medium PL towns have them) cover
   "new business", sponsor kids' sports for a footer link; zero budget beyond the
   sponsorship itself. **Standard practice; individual outlets not verified.**
6. **Suppliers:** plumbing wholesalers (hurtownie) often have "find a contractor" or
   partner pages — ask your wholesaler rep in week 2. **Not verified individually.**

Avoid: paid link farms, generic "PL SEO catalogs" blast — unverified value, known risk.

---

## 5. Week-by-week: first 90 days

### Week 1 — ship + registers
1. Domain `.pl` bought; site live on final host; HTTPS + redirects verified (§2.4).
2. Pre-launch checklist §2.1–2.5 + 2.8 executed; `/api/health` and `<key>.txt` live.
3. GBP created + verification started (§2.7) — the long pole, start it now.
4. GSC Domain + URL-prefix properties; sitemap submitted; URL Inspection requested on
   homepage + top 3 service pages. Bing WT via GSC import; IndexNow homepage submit.
5. `<html lang="pl">`, JSON-LD LocalBusiness, Plausible live; 3–5 core pages:
   home, 3–4 service pages (e.g. instalacja gazu, przeglądy, wykrywanie ulatnień,
   kotły), contact with NAP + service area.

### Weeks 2–4 — content cadence + citations + monitoring
1. Publish 1 page/week minimum: city/location pages (`instalacje-gazowe-<miasto>`)
   and problem-solving posts mapped to real customer questions.
2. Citations: CEIDG-consistent NAP into registries, chamber, SEP/UDT-linked bodies
   where qualified (§4.2–4.4). Same NAP string everywhere.
3. Review engine starts: every completed job → GBP review link via SMS/email.
   Target modest + steady (e.g. 2–4/month beats 20 in month 1 — natural velocity;
   **practice, unverified**).
4. SEO tool monitoring on: daily `/api/health`, sitemap diff, GSC API pull for
   impressions/crawl stats, IndexNow on every deploy (§3.3).
5. Apply to Vaillant partner program (§4.1); contact Bosch/others as you confirm
   their PL programs.

### Month 2 — expansion + iteration on GSC data
1. Double down where GSC shows impressions-without-clicks (position 8–20 queries):
   expand those pages, add FAQ sections, improve internal links.
2. First "link-worthy" asset: e.g. a real cost/price guide for gas connections in
   your powiat (original local data = locally linkable).
3. Review velocity continues; add photos to GBP weekly (activity signals — practice).
4. Location pages for adjacent towns as capacity allows — one town, one page, unique
   content (jobs actually done there), no doorway spam.
5. Chase supplier/wholesaler listings; local news piece if there's a story.

### Month 3 — link building + consolidation
1. Convert any brand-locator acceptances; sponsorships land (seasonal — autumn heating
   season is your media hook in PL).
2. GSC crawl-stats review: fix crawl waste (params, thin pages), consolidate pages
   that cannibalize (same query, two URLs → merge + 301).
3. Prune/refresh weeks-1 content that got zero impressions in 8 weeks.
4. Set 90-day review: impressions trend, GBP insights calls/direction requests,
   review count/velocity, referring domains count (expect single-to-low-double
   digits — realistic; no official benchmark exists).
5. Tool iteration: add GSC position tracking per URL, auto-alert on index drops
   (`site:` counts + URL Inspection API where available).

---

## 6. KPI dashboard (all pullable by your tool)

- GSC API: impressions, clicks, avg position per URL (weekly delta).
- `/api/health`: deploy freshness, sitemap URL count drift.
- GBP: calls, direction requests, review count (manual/API).
- Referring domains (any free source you control); IndexNow POST success log.
- Target bands at day 90 (expectation-setting, practitioner-derived): branded queries
  ranking page 1; local pack presence for core service+city; 500–5,000 monthly
  impressions; 5–15 referring domains. If impressions are zero at week 6, debug:
  indexability → crawl stats → content depth → links, in that order.

## Sources

Fetched 2026-10-11. [verified] = HTTP 200 and content matched the claim.
[unverified] = fetched but content did not support the claim, or fetch failed.

- [verified] https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites — ccTLD strong signal; server location weak signal; geo meta tags ignored
- [verified] https://www.indexnow.org/documentation — protocol: 1-URL GET, 10k-URL POST, key-file ownership, 200 = received only
- [verified] https://www.indexnow.org/ — participating engines: Microsoft Bing, Naver, Seznam.cz, Yandex, Yep
- [verified] https://raw.githubusercontent.com/plausible/analytics/master/LICENSE.md — AGPL-3.0
- [verified] https://api.github.com/repos/plausible/analytics — license AGPL-3.0, ~29.4k stars (fetched via GitHub API)
- [verified] https://llmstxt.org/ — llms.txt v2 proposal, author/date confirmed
- [verified] https://r.jina.ai/https://support.google.com/business/answer/7107242 — GBP verification: video (recommended), phone/SMS, email, postcard; 14-day postcard procedure
- [verified] https://developers.google.com/my-business/reference/businessinformation/rest/v1/locations — ServiceAreaBusiness object; CUSTOMER_LOCATION_ONLY location type
- [verified] https://r.jina.ai/https://support.google.com/webmasters/answer/9008080 — GSC verification methods; Domain property = DNS only; multiple methods recommended
- [verified] https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap — 50MB/50k limits; extensions; index files
- [verified] https://developers.google.com/search/docs/crawling-indexing/robots/intro — robots.txt basics
- [verified] https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls — canonicalization
- [verified] https://developers.google.com/search/docs/appearance/structured-data/local-business — LocalBusiness structured data
- [verified] https://r.jina.ai/https://platform.openai.com/docs/bots — OAI-SearchBot = ChatGPT search inclusion; GPTBot = training; ~24h robots.txt pickup; IP range JSONs
- [verified] https://api.stackexchange.com/2.3/...questions/1574/answers — accepted answer: no official indexing time rule; "instantly to a few months"
- [verified] https://api.stackexchange.com/2.3/search/advanced (sandbox/new-site queries) — thread inventory on sandbox questions
- [verified] https://www.vaillant.pl/ — nav links to installer finder
- [verified] https://profesjonalisci.vaillant.pl/klienci-indywidualni/kontakt/sprzedaz-i-serwis/autoryzowany-instalator-serwis/ — authorized installer finder ("Znajdź firmę autoryzowaną w Twojej okolicy")
- [verified] https://www.vaillant.pl/kontakt/znajdz-zaufanego-instalatora-w-poblizu/ — consumer installer finder (linked from homepage nav)
- [verified] https://ceidg.gov.pl/ — CEIDG registry portal reachable
- [verified] https://ekrs.ms.gov.pl/ — eKRS reachable
- [verified] https://biznes.gov.pl/ — state business portal reachable
- [verified] https://www.udt.gov.pl/ — UDT reachable
- [verified] https://sep.com.pl/ — SEP reachable
- [verified] https://kig.pl/ — KIG reachable
- [verified] https://uodo.gov.pl/ — UODO (PL DPA) reachable
- [verified] https://www.bosch-home.pl/ — Bosch consumer PL site reachable (installer finder NOT confirmed)
- [unverified] https://igg.org.pl/ — HTTP 406 to automated fetch; exists, check manually
- [unverified] https://www.bing.com/webmasters/about — HTTP 200 but JS-only shell; content not extractable
- [unverified] Reddit r/SEO JSON search — HTTP 403 (direct and via proxy); community indexing-time threads not retrievable
- [unverified] Bing help-center URL (bing.com/webmasters/help/...) — fetch blocked/404 via proxy; Bing submission details taken from indexnow.org instead
- [unverified] https://bosch-thermotechnika.pl / bosch-climate.pl — DNS did not resolve; Bosch PL installer directory status unknown (not fetched)
- [unknown, not fetched] Plausible hosted pricing; GA4 current consent requirements detail; Anthropic/Perplexity crawler docs; Viessmann/De Dietrich PL programs
