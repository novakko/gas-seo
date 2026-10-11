# Local SEO + Technical Foundation: Gas-Services Website for Poland

**Prepared:** 2026-10-11 · **Market:** Poland (PL language, PL cities) · **Business type:** new
solo-run gas services company (instalacje gazowe, kotły/piece gazowe, serwis, przeglądy, ogrzewanie)

Evidence rules used below: every claim from a fetched primary source is marked [verified]; claims
I could not confirm at a source are marked **[inference]**, **[unverified]**, or **vendor survey,
unverified**. Reddit was unreachable during research (anonymous access blocked at the Reddit edge,
 AbuseAlleviationError on both www and old.reddit) — no community-evidence claims are included.

---

## 1. Google Business Profile (GBP) for a gas/heating trade

Why GBP first: for "serwis kotłów gazowych <miasto>"-type queries the map pack, not the organic
list, is the primary surface. Primary Category is repeatedly reported as the top local ranking
factor in the Whitespark Local Search Ranking Factors survey (vendor survey, unverified — the 2026
edition page was fetched and confirms the report exists and emphasizes Primary Category, but the
survey is self-reported panel data, not Google documentation).

### 1.1 Setup, field by field

- **Business name:** legal/trade name only. Google's "Guidelines for representing your business
  on Google" (support.google.com/business/answer/3038177) [verified page] prohibit keyword stuffing
  the name (e.g. "Jan Kowalski Serwis Kotłów Gazowych Taniej" is a takedown target; "Jan Kowalski
  Instalacje Gazowe" is fine if that's the registered name).
- **Primary category:** choose inside the GBP picker — the category list is not published as a
  document, so exact English/Polish strings are **unknown (not fetched)**. Candidates to look for
  in the picker [inference]: "Plumber" / "Hydraulik", "Heating contractor", "HVAC contractor"
  (schema.org separately defines Plumber and HVACBusiness — see §4). Rule: ONE primary category,
  matching the highest-revenue intent; add secondaries only for services you actually sell.
- **Service-area business (SAB):** set "Yes" for service-area mode, hide the address if customers
  don't visit you. Google's "Manage your service areas for service-area & hybrid businesses"
  (support.google.com/business/answer/3038163) [verified page] covers this mode. Cities/towns:
  enter the actual towns you serve (city-level, not voivodeship); Google documents a ~2-hour
  drivetime guideline for service areas in that page [verified page; exact wording not extracted].
- **Phone:** Polish landline or mobile in local format (+48 …), consistent with the site's
  `tel:` links and schema `telephone` — NAP consistency across GBP/site/directories (§2).
- **Hours + special hours:** set; holidays break "open now" trust signals.
- **Services:** enumerate each service (instalacja gazowa, wymiana kotła, przegląd, konserwacja,
  ogrzewanie podłogowe…) with short PL descriptions — this feeds map-pack "Services" tab and
  query matching [inference].
- **Photos:** real van/livery, meter/regulator work, boiler swaps (before/after), team photo.
  Stock photos are a spam signal competitors will report [inference].
- **Booking/appointment URL:** point at your own `/kontakt` or a booking endpoint on your domain —
  do NOT route through lead-gen marketplaces if avoidable (their numbers intercept calls)
  [inference].
- **Description:** 750-char field; front-load services + city + certification (see UDT note §7).

### 1.2 Fighting competitor spam in the map pack

- **Keyword-stuffed names:** suggest an edit directly in GBP ("Suggest an edit" → "Remove this
  name"), and/or file Google's business-name redressal form. The redressal form URL is **unknown
  (not fetched)**; the in-product flow is [inference]. Reported-and-removed stuffed names are the
  single most common map-pack win in trades, per vendor blogs (claim, unverified).
- **Fake addresses / P.O.-box storefronts:** "Suggest an edit" → location issues; repeat
  offenders get suspended through Google's business redressal forms [inference].
- **Review bombing:** Google's "Report inappropriate reviews on your Business Profile"
  (support.google.com/business/answer/4596773) [verified page] is the documented remediation path
  for policy-violating reviews.
- Track competitor GBP edits with a simple scraper against the Maps frontend of your automation
  tool (§5) — category/name changes are the actions spammers take most [inference].

## 2. Citations & directories — Poland (verified against live sites)

Fetched 2026-10-11 with a desktop UA; statuses below reflect what actually returned:

| Directory | Status | What it is today |
|---|---|---|
| panoramafirm.pl | 200 [verified] | Title: "Panorama Firm – największa wyszukiwarka firm w Polsce". Major PL business index; has "instalatorstwo" category taxonomy [verified]. Core citation. |
| pkt.pl | 200 [verified] | Title: "Baza firm pkt.pl – adresy, telefony, oferty, opinie, mapy". Classic PL citation source with reviews. Core citation. |
| oferteo.pl | 200 [verified] | Marketplace with a live "Hydraulik" category [verified]. Lead-gen marketplace + profile; tradesmen use it for leads. |
| fixly.pl | 200 via r.jina.ai [verified] | "Budowa domu, remont mieszkania… Fixly.pl"; home-services marketplace, "Hydraulik" present on homepage [verified]. Fixly is OLX-group's Fixly — used heavily by PL tradesmen [inference]. |
| aleo.pl | 403 / CAPTCHA via r.jina.ai [unverified] | Existed historically as a company directory; could not verify current state. Treat as secondary; verify manually. |
| zumi.pl | 200 [verified] | BUT the homepage now serves "Jakdojade – podróżuj wygodnie komunikacją miejską i PKP" — Zumi's directory is effectively dead/absorbed. Do NOT invest time here [verified redirect behavior]. |
| udt.gov.pl (UDT) | 200 [verified] | Not a citation — the Urząd Dozoru Technicznego site. See §7 for F-GAZ certification mention on their pages [verified]. |

**Practical citation sequence [inference]:** (1) Panorama Firm + pkt.pl as the two structural
citations; (2) Oferteo + Fixly as lead-gen profiles that also rank for "hydraulik/serwis kotłów"
queries; (3) verify Aleo manually; (4) skip Zumi. Always keep NAP byte-identical (street
abbreviation, phone format) across all of them; disputes in Polish directories are rarer than in
US ones but the data aggregator layer is thin — each directory is its own source of truth
[inference].

## 3. Site architecture

**Service pages vs city pages — the trades pattern [inference, standard local-SEO practice]:**

```
/                               home = brand + core services + service area
/uslugi/                        service hub
/uslugi/instalacje-gazowe/      one page per service
/uslugi/wymiana-kotla-gazowego/
/uslugi/serwis-kotlow-gazowych/
/uslugi/przeglady-gazowe/
/obszar-dzialania/              area hub
/serwis-kotlow-gazowe-krakow/   one page per service × top city (only where you truly serve)
/blog/                          occasional; FAQ content lives on service pages
```

- **URL language:** Polish slugs, no diacritics in URLs (`serwis-kotlow`, not `serwis-kotłów`),
  lowercase, hyphens. PL users and PL SERPs match Polish slugs [inference].
- **Service×city pages:** only where you have real jobs to reference; thin duplicates across 40
  towns is the classic doorway pattern (§7). A new solo business should launch with home + 3–6
  service pages + 2–4 city pages it actually works in, then grow by real expansion [inference].
- **Internal linking:** every service page links to sibling services and to its city page; city
  page links back to all services offered there; breadcrumbs on all pages (matches breadcrumb
  markup §4). Flat architecture — every target ≤3 clicks from home [inference].
- **Proof from real PL sites:** Oferteo's "Hydraulik" vertical is structured as
  category → city subcategories (observed in fetched HTML, [verified] for taxonomy existence).
  I could not fetch ranking data for individual tradesmen sites (no SERP access), so no
  ranking-verified site example is included — do not trust blog screenshots of such examples
  without re-verifying.

## 4. Structured data (JSON-LD), per schema.org + Search Central

Fetched and confirmed at schema.org (2026-10-11): `Plumber` and `HVACBusiness` are subtypes of
`HomeAndConstructionBusiness`, which is a subtype of `LocalBusiness` [verified]. `Service` defines
`serviceType`, `provider`, `areaServed`, `hasOfferCatalog` [verified]. Google's LocalBusiness doc
(developers.google.com/search/docs/appearance/structured-data/local-business) [verified] states:
"You must include the required properties for your content to be eligible for display as a rich
result."

**Home page — Plumber (LocalBusiness subtype), required + recommended props only:**

```json
{
  "@context": "https://schema.org",
  "@type": "Plumber",
  "@id": "https://example.pl/#business",
  "name": "Nazwa Firmy — Instalacje Gazowe",
  "url": "https://example.pl/",
  "telephone": "+48600100200",
  "image": "https://example.pl/img/van.jpg",
  "priceRange": "$$",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "ul. Przykładowa 12",
    "addressLocality": "Kraków",
    "postalCode": "30-001",
    "addressCountry": "PL"
  },
  "geo": { "@type": "GeoCoordinates", "latitude": 50.0647, "longitude": 19.9450 },
  "areaServed": [
    { "@type": "City", "name": "Kraków" },
    { "@type": "City", "name": "Wieliczka" }
  ],
  "openingHoursSpecification": [{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
    "opens": "07:00", "closes": "18:00"
  }],
  "sameAs": ["https://panoramafirm.pl/twoj-profil", "https://www.facebook.com/twojafirma"]
}
```

**Service page — Service referencing the business [verified props]:**

```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "Serwis kotłów gazowych",
  "provider": { "@id": "https://example.pl/#business" },
  "areaServed": { "@type": "City", "name": "Kraków" }
}
```

**FAQPage — do NOT build for rich results.** Google's FAQ rich-results doc
(developers.google.com/search/docs/appearance/structured-data/faqpage) [verified] now limits FAQ
rich-result *display* to "well-known, authoritative government and health websites". The old
"changes" blog post (developers.google.com/search/blog/2023/08/faq-changes) returns 404 today
[verified 404]. Markup is still harmless for machines, but expect zero FAQ stars.

**Review/aggregateRating on your own LocalBusiness — skip it.** Google's review-snippet doc
(developers.google.com/search/docs/appearance/structured-data/review-snippet) [verified] requires
compliance with its "guidelines about self-serving reviews" for local businesses; reviews you host
about yourself are self-serving and are not eligible for stars [inference from that guideline].
Put the effort into getting reviews *on the GBP* instead (§6).

Also validate everything with the Rich Results Test and Schema.org validator before/after deploy;
URLs are standard Google tooling [inference: not fetched this session].

## 5. Technical foundation

**Constraint recap:** solo dev, must expose a backend/API for his own SEO automation, Apple
Silicon Mac, broken brew, no sudo. Recommendation [inference, architecture guidance]:

1. **One small VPS runs everything** (e.g. any €4–8/mo tier — pricing unknown, not fetched):
   - Caddy or nginx serving the **static brochure site** (Astro/11ty static export) — no runtime
     needed for the public site, best CWV profile (§5.3);
   - the **API** (FastAPI/Node) on `api.example.pl` behind the same TLS terminator, systemd-managed;
   - Postgres/SQLite for the SEO automation data (rank tracking, GBP change scraping, lead log).
2. **Do not** put the public site on a JS-heavy SPA stack: crawl budget and CWV both suffer for a
   brochure site with zero interactivity needs [inference].
3. **Core Web Vitals targets** (Google's CWV doc, developers.google.com/search/docs/appearance/
   core-web-vitals) [verified]: **LCP < 2.5 s, INP < 200 ms, CLS < 0.1** at the 75th percentile.
   For a static brochure site these are trivially reachable: pre-sized image dimensions, no
   web-font FOUT layout shift, no third-party chat widgets on LCP path [inference].
4. **Sitemap:** XML sitemap per Google's "Build a sitemap" doc
   (developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap) [verified]:
   `<loc>`, lastmod, ≤50k URLs/file; submit via Search Console AND reference from robots.txt
   (`Sitemap: https://example.pl/sitemap.xml`).
5. **robots.txt:** allow all on the brochure site; disallow `/api/`; host the sitemap on the same
   host that serves it (Sitemap cross-host rules: sitemaps on a cross-host URL need that host's
   robots.txt ownership proof via Search Console — per the build-sitemap doc [verified page]).

**Search Console setup** (support.google.com/webmasters/answer/34592, "Add a website or platform
property") [verified page exists; steps summarized]:
1. Add **Domain property** `example.pl` (covers all subdomains+protocols) — verify via DNS TXT.
2. Add a second **URL-prefix property** `https://example.pl` — enables additional report types.
3. Submit `/sitemap.xml` in Sitemaps; request indexing for money pages after launch.
4. Bing Webmaster Tools (bing.com/webmasters/about) [verified page]: import sites/data from
   Search Console — import-from-GSC is a documented BWT onboarding feature [inference; not on the
   fetched page]. Bing share in PL is small but the import is one click [inference].

## 6. Reviews — compliant acquisition mechanics

- **The engine [inference]:** after a completed job, send one SMS with a **shortened g.page
  review link** (GBP → "Ask for reviews" link) + the customer's name. One ask, one reminder after
  3 days if no review. Polish customers complete SMS flows at far higher rates than email
  [inference].
- **No gating:** never route unhappy customers away from the review link — Google's guidelines
  page (support.google.com/business/answer/3038177) [verified page] prohibits review practices
  like discouraging/misselecting negative feedback. Ask *everyone*, same link.
- **No incentives for GBP reviews** (paying for reviews is prohibited on the guidelines page
  [verified page]); a discount for *feedback sent privately* is a different channel but keep it
  clearly separated from GBP [inference].
- **Schema risk:** see §4 — do not publish self-hosted review stars on the business's own site;
  they're self-serving and ineligible, and fabricated `aggregateRating` is a manual-action magnet
  [inference].
- **Dispute path:** for policy-violating reviews, use the documented report flow (§1.2).

## 7. What NOT to do — documented spam/penalty patterns in trades

1. **Do not keyword-stuff the GBP business name.** Guidelines page [verified] prohibits names
   that don't match real-world branding; competitors in PL trades DO file reports [inference].
2. **Do not mass-generate service×city pages** you don't serve — doorway pages are explicit
   Google spam policy territory (Google's spam policies doc; not fetched this session — policy
   existence is common knowledge, treat as unverified at source this session).
3. **Do not fake `aggregateRating`/`review` JSON-LD.** Schema spam on money pages is a classic
   manual-action trigger for local businesses [inference]; eligibility rules in §4/§6.
4. **Do not buy PL "500 katalogów" citation blasts.** Legacy PL SEO catalogs are largely dead
   (see Zumi's fate, §2); mass low-quality links are a link-spam pattern [inference].
5. **Do not operate without qualification.** Gas work in Poland requires qualification entries in
   the UDT-managed ewidencja (G-3 class for gas). The UDT site (udt.gov.pl) [verified] markets
   "Certyfikat dla personelu / dla przedsiębiorców" and references F-GAZ certification; the exact
   current legal instrument (Prawo gazowe / kompetencje rozporządzenie) was **not fetched** —
   verify before publishing any certification claim on the site or GBP, because fake certification
   claims are both illegal exposure and a reportable GBP violation [inference].
6. **Do not route the GBP phone through a call-tracking number** that swaps digits (dynamic
   number insertion) — inconsistent NAP confuses Google's matching [inference].

## Open questions / not verifiable this session

- Exact GBP category strings available in the PL picker (in-product only).
- Aleo's current status (Cloudflare-blocked even via r.jina.ai).
- All Reddit community evidence (platform-level anonymous block, AbuseAlleviationError).
- Whitespark/BrightLocal internal numbers (pages fetched; claims remain vendor-survey data).

## Sources

All fetched 2026-10-11, UA `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)`; JS-heavy pages
fetched via r.jina.ai.

- https://developers.google.com/search/docs/appearance/structured-data/local-business — [verified]
- https://developers.google.com/search/docs/appearance/structured-data/review-snippet — [verified]
- https://developers.google.com/search/docs/appearance/structured-data/faqpage — [verified]
  (FAQ rich results now limited to well-known authoritative government and health websites)
- https://developers.google.com/search/blog/2023/08/faq-changes — [verified 404]
- https://developers.google.com/search/docs/appearance/core-web-vitals — [verified]
  (LCP<2.5s, INP<200ms, CLS<0.1 at p75)
- https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap — [verified]
- https://support.google.com/webmasters/answer/34592 (Add a website or platform property) — [verified]
- https://support.google.com/business/answer/3038177 (Guidelines for representing your business
  on Google) — [verified page; JS-rendered body, policy wording quoted only where extracted]
- https://support.google.com/business/answer/3038163 (Manage service areas for service-area &
  hybrid businesses) — [verified]
- https://support.google.com/business/answer/4596773 (Report inappropriate reviews) — [verified]
- https://support.google.com/business/answer/2734035 — [verified 404] (GBP categories help URL
  has moved; category list not published as a doc)
- https://schema.org/Plumber — [verified] (subtype of HomeAndConstructionBusiness/LocalBusiness)
- https://schema.org/HVACBusiness — [verified] (same lineage)
- https://schema.org/HomeAndConstructionBusiness — [verified]
- https://schema.org/Service — [verified] (serviceType/provider/areaServed/hasOfferCatalog exist)
- https://panoramafirm.pl/ — [verified] (live PL firm index)
- https://www.pkt.pl/ — [verified] (live PL firm database with reviews)
- https://www.oferteo.pl/ — [verified] (marketplace, live Hydraulik category)
- https://fixly.pl/ — [verified via r.jina.ai] (live home-services marketplace)
- https://aleo.pl/ — [unverified] (403 / Cloudflare CAPTCHA, direct and via r.jina.ai)
- https://www.zumi.pl/ — [verified] (now serves Jakdojade content — directory effectively gone)
- https://www.udt.gov.pl/ — [verified] (UDT certifications incl. F-GAZ mention)
- https://whitespark.ca/local-search-ranking-factors/ — [verified page exists; 2026 report;
  content = vendor survey, unverified]
- https://www.brightlocal.com/research/local-consumer-review-survey/ — [verified page exists;
  content = vendor survey, unverified]
- https://www.bing.com/webmasters/about — [verified]
- https://www.reddit.com/r/SEO/search.json?… — [unverified] (AbuseAlleviationError 403, blocked
  at Reddit edge for anonymous access; retried via old.reddit and r.jina.ai, all 403)
- https://www.sterlingsky.xyz/local-seo-resources/faq-schema-generator/ — [unverified]
  (not fetched; local shell quoting error during fetch)
