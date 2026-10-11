# How AI engines decide which local businesses to cite, and what measurably moves it

**Evidence-marked research dossier — /gas-seo project**
**Date: 2026-10-11 · Sources: primary docs + arXiv paper + live ToS checks (this session)**

## 0. Executive summary

- A local business can be cited by five AI surfaces: ChatGPT search, Perplexity,
  Claude web search, Gemini (AI Overviews + grounding), and Copilot. Each runs a
  named crawler with published docs; two of them (OAI-SearchBot, PerplexityBot)
  are explicitly documented as the *eligibility gate* for search answers.
- The single cheapest documented lever: make sure the site's robots.txt allows
  OAI-SearchBot, PerplexityBot, Googlebot, and Bingbot, and submit to Bing
  (Webmaster Tools + Places) with IndexNow pings on changes. Everything in this
  paragraph is quoted from primary docs listed in Sources.
- The only peer-reviewed effect-size data (GEO, arXiv 2311.09735, KDD '24)
  measured *academic/informational* queries, not local-business ones. Its
  concrete levers — citations, quotations, statistics — are directionally
  useful but must be caveated for a plumber's site [inference when applied
  to local queries].
- Measurement without ToS violations: manual prompt batteries, or API-based
  evals (OpenAI API, Anthropic API). Scripted polling of the ChatGPT UI is
  explicitly prohibited by OpenAI's Terms of Use [verified].
- llms.txt is a proposal with no documented answer-engine adoption commitment.
  Cheap to add, near-zero expected citation impact. Do not spend real time on
  it beyond a 15-minute file.

## 1. Which AI engines can cite a local business at all

Five surfaces matter for a Polish gas-services business:

1. **ChatGPT search** (OpenAI) — web-backed answers with inline citations.
   Documented stack [verified: openai.com/index/introducing-chatgpt-search]:
   "a fine-tuned version of GPT‑4o, post-trained" for search, drawing on
   "third-party search providers, as well as content provided directly by our
   partners." Bing is not named → the engine's exact index partner stays
   [claim, unverified].
2. **Perplexity** — search-first product; every answer is citation-bearing.
3. **Claude web search** (Anthropic) — launched 2025-03-20, global on all plans
   2025-05-27 [verified: anthropic.com/news/web-search].
4. **Gemini / Google AI Overviews** — grounded in Google's own index; for local
   queries this means ordinary local ranking signals (GBP, reviews, NAP) are
   the pipeline [inference from grounding docs, below].
5. **Copilot** (Microsoft) — no primary pipeline doc could be fetched this
   session (search engines bot-walled from this network). Pipeline
   description = [inference/claim, unverified].

Why this matters for a *new* business: answer engines are an additional
discovery surface that a brand-new domain can appear in faster than classic
"blue link" rankings, because eligibility is partially crawler-optics
(robots.txt + being in the crawled index) rather than accumulated authority.
The authority part still matters; this dossier only claims the eligibility
layer is documentable and cheap [inference].

## 2. What each engine's crawler can and cannot see

### OpenAI (ChatGPT)

From `platform.openai.com/docs/bots` [verified]:

- **OAI-SearchBot** — "Sites that are opted out of OAI-SearchBot will not be
  shown in ChatGPT search answers." This is the search-eligibility crawler.
- **GPTBot** — training crawl; blocking it does NOT remove a site from search
  answers (separate opt-out).
- **ChatGPT-User** — user-initiated fetches; "robots.txt rules may not apply";
  and explicitly "not used to determine whether content may appear in Search."
  Tuning robots.txt for ChatGPT-User therefore does nothing for visibility —
  a documented dead end.
- robots.txt changes propagate in ~24h. Published IP ranges:
  `openai.com/searchbot.json` and `gptbot.json` for allow-listing at the
  firewall level.
- The oft-repeated "ChatGPT search is powered by Bing" was **not** confirmed
  at any primary source this session (the search-launch post does not name
  Bing) → [claim, unverified].

### Perplexity

From `docs.perplexity.ai/guides/bots` [verified]:

- **PerplexityBot** — "designed to surface and link websites in search
  results… not used to crawl content for AI foundation models." Allowing it in
  robots.txt is the documented eligibility path; published IPs at
  `perplexity.com/perplexitybot.json`; ~24h robots.txt propagation.
- **Perplexity-User** — on-the-fly fetches when a user action triggers them;
  robots.txt is not consulted for these.

### Anthropic (Claude)

- `anthropic.com/news/web-search` [verified]: launch + rollout dates above.
  The announcement does **not** name the underlying index; "Claude search is
  Brave/Bing" stays [claim, unverified].
- `docs.anthropic.com/.../search-results` [verified]: developers get
  "search results content blocks" (source + title) that Claude cites like web
  results — that is the API-side citation mechanism, not a disclosure of the
  consumer index.
- Consumer ToS [verified]: automated access prohibited except via Anthropic
  API; scraping prohibited. Measurement must go through the API or by hand.

### Google (Gemini / AI Overviews)

- `ai.google.dev/gemini-api/docs/google-search` [verified]: the grounding
  pipeline is: prompt analysis → model generates search queries → executes
  them → synthesizes → returns inline `url_citation` annotations plus
  `google_search_call` / `google_search_result` steps. In other words:
  Gemini answers are built on **ordinary Google search results**.
- The crawlers overview page
  (`developers.google.com/search/docs/crawling-indexing/overview-google-crawlers`)
  [verified] documents common crawlers / special-case fetchers /
  user-triggered fetchers — but no longer contains a Google-Extended section;
  the familiar "block Google-Extended to opt out of AI training" description
  is [claim, unverified] at primary source.
- The old AI Overviews help URL is 404. Consequence [inference]: the
  documented lever for Gemini visibility is *classic* Google ranking — Googlebot
  access, sitemap, GBP, local pack presence.

### Microsoft Copilot

No primary doc fetched (all search engines bot-walled from this network).
Pipeline description [inference/claim, unverified]: Copilot is widely reported
to sit on Bing's index; the actionable, documented-adjacent lever is making
sure the site is in Bing Webmaster Tools and Bing Places.

## 3. Where AI engines get local-business facts

Documented pieces of the pipeline:

- **Their own crawl** (OAI-SearchBot, PerplexityBot — see §2) of the open web,
  which includes the site itself *and* the directories that list it.
- **Google's index** for Gemini/AI Overviews (documented grounding pipeline).
- **Bing's index** for Copilot [claim, unverified] and possibly ChatGPT search
  [claim, unverified]. Either way, Bing submission is cheap and is the
  documented input to IndexNow (below).
- **IndexNow** (`indexnow.org/documentation` [verified]): submitted URLs are
  "automatically shared with all other participating search engines."
  Participants: Bing, Naver, Seznam, Yandex, Yep. Google does not participate.
  Key-file ownership proves submitter controls the site; HTTP 429 = treated as
  spam signal. 10,000 URLs per POST is the documented cap.
- **OpenAI–Reddit partnership** [verified:
  openai.com/index/openai-and-reddit-partnership]: Reddit's Data API —
  "real-time, structured" content — feeds OpenAI products including ChatGPT.
  So Reddit threads are a *documented* ChatGPT input, not just community
  folklore; organically earning relevant thread presence (r/poland HVAC
  threads, local subs) is slow but real [inference]. (Fetching Reddit
  directly was still impossible this session — 403/429 on every route.)
- **Bing Places** (business listing): involvement of Bing Places data in
  Perplexity's local answers is [claim, unverified]; creating the listing is
  near-zero cost and is independently required for Bing maps presence.

What this means for the gas-services site [inference, grounded in §2]: the
facts an AI engine can cite about a business come from (a) the site's own
crawlable pages, (b) structured local listings (GBP for Google-grounded
answers; Bing Places for Bing-consuming answers), (c) directories that are
themselves crawlable — which is why the Poland directory work in
REPORT-local-seo-technical.md compounds here.

## 4. What measurably moves citations (GEO paper + corroboration)

**The GEO paper** — "GEO: Generative Engine Optimization," arXiv 2311.09735,
published at KDD '24 (DOI 10.1145/3637528.3671900) [verified: abstract page +
full text fetched].

- Method: GEO-bench — 10,000 queries (8K train / 1K val / 1K test; 80%
  informational, 10% each transactional/navigational), each query augmented
  with the text of the top-5 Google results. Domains are academic-flavored
  (science, history, …). **No local-business queries.**
- Results: adding **citations to sources, quotations, and statistics** yields
  +30–40% relative visibility (Position-Adjusted Word Count) and +15–30%
  (Subjective Impression); fluency improvements also +15–30%; headline "up to
  40%"; deployed Perplexity experiments "up to 37%". Two nuances from the
  full text [verified]: **Keyword Stuffing performed ~10% *worse*** than
  baseline ("Keyword Stuffing traditionally used in SEO don't perform well"),
  and gains were **largest for lower-ranked sources** (e.g. Statistics
  Addition scored +115.1 at rank 5 vs −20.6 at rank 1) — i.e. GEO levers
  help a *new* domain most, which is exactly this project's situation.
- **Caveat for this project** [inference]: the measured queries are not
  "best gas engineer near me" style. Directionally, the levers (specific
  numbers, quoted standards, cited regulations) map naturally onto a trades
  site's content (pressures, temperatures, UDT certification references,
  priced service tables) — but the effect size on local queries is unknown.

**Evidence tiers for commonly-cited local-AI factors:**

| Factor | Tier |
|---|---|
| OAI-SearchBot / PerplexityBot allowed in robots.txt | documented (§2 quotes) |
| IndexNow submission on content changes | documented (indexnow.org) |
| Bing Webmaster + Bing Places listing | documented inputs; downstream AI effect [claim, unverified] |
| GBP review volume/velocity → Gemini/AIO local answers | [inference] — grounding uses Google results; local pack ranking is GBP-driven per REPORT-local-seo-technical.md |
| Presence in crawlable PL directories | [inference] — directories are the crawlable entity records |
| Reddit/forum presence boosting AI citations | **documented for ChatGPT** (OpenAI–Reddit Data API partnership); organic presence itself is a long game. Fetching Reddit for research was impossible this session (403 at IP level on all routes; PullPush 429; redlib bot-walled). |
| llms.txt improving citations | no documented adoption commitment by any engine (§6) |

## 5. Recommended actions for the gas-services site

Ordered by (documented impact ÷ effort):

1. **robots.txt**: explicitly allow OAI-SearchBot, PerplexityBot, Googlebot,
   Bingbot (and don't block ChatGPT-User; it's irrelevant to search either
   way). Expect ~24h propagation per docs.
2. **Bing Webmaster Tools**: verify site, submit sitemap, enable IndexNow key
   + auto-submit on publish. This is the documented multi-engine URL pipe
   (Bing, Naver, Seznam, Yandex, Yep).
3. **Bing Places**: create the business listing with the same NAP/categories
   as GBP (categories research in REPORT-local-seo-technical.md).
4. **Crawlable citation footprint**: the PL directories verified live in
   REPORT-local-seo-technical.md (Panorama Firm, pkt.pl, Oferteo, Fixly —
   Zumi is dead) are themselves crawled by OAI-SearchBot/PerplexityBot; being
   on them with consistent NAP gives answer engines a second, older-domain
   record of the business [inference].
5. **Content levers with measured backing (caveated)**: per service page,
   include concrete numbers (typical price ranges, time-on-job, boiler
   models serviced), short quotes from applicable Polish regulations/UDT
   requirements, and explicit citations to the sources of those numbers —
   the three levers the GEO paper measured at +30–40% on its benchmark.
6. **Freshness pings**: IndexNow on every publish (the user's tool can fire
   this automatically — see §6).

## 6. How the user's SEO tool can measure AI citations

ToS reality first [verified]:

- OpenAI ToS (`openai.com/policies/terms-of-use/`): prohibits "Automatically
  or programmatically extract data or Output" and circumventing rate limits →
  scripted polling of the ChatGPT UI is a ToS violation. Do not build it.
- Anthropic consumer terms: same shape — automated access only via the API.
- Perplexity: same category of restriction on automated UI access.

Compliant measurement designs:

1. **Manual prompt battery** (zero cost, zero ToS risk): a fixed list of
   Polish buyer prompts ("jaki serwis kotłów gazowych w <miasto>",
   "najlepszy instalator gazowy <miasto>", "ile kosztuje przyłącze gazowe")
   run by hand weekly in each engine; log: cited? which sources? position of
   our domain? Keep results in the repo as TSV — same discipline as the
   autocomplete dataset in `data/`.
2. **API-based eval**: OpenAI API and Anthropic API are the sanctioned
   automated channels. A nightly script sends the same prompt battery via API
   (search-enabled model for OpenAI), records cited URLs, and diffs week over
   week. Cost is the only downside; prompt batteries of ~20 prompts × 5
   engines weekly are trivially cheap. Documented API surfaces [verified]:
   - **Gemini grounding**: `google_search` tool; model picks queries; inline
     URL + cited-text annotations come back programmatically. Pricing:
     **5,000 grounded searches/month free**, then $14 per 1,000 (Gemini 3+
     models) — the cheapest documented automated measurement of the five.
   - **Perplexity**: Agent API (built-in citations; base URL
     `perplexity.ai/v1/agent`) and a Search API exist [verified:
     docs.perplexity.ai]; exact pricing unknown (not fetched).
   - **Anthropic** `web_search` tool: returns "cited sources" with each
     response [verified: docs.anthropic.com web-search-tool docs].
   - **OpenAI**: search-enabled responses through the API; retrieval of cited
     URLs is possible but annotation shape was not verified this session
     [unverified].
   - **Copilot**: no sanctioned programmatic channel documented → manual
     battery only.
3. **Crawler-access canary**: the site's access log answers "are the AI
   crawlers actually coming?" — grep for OAI-SearchBot/PerplexityBot/GPTBot
   user-agents by published IP ranges (`openai.com/searchbot.json`,
   `perplexity.com/perplexitybot.json`). Zero-cost, documented, and it
   validates that robots.txt is not accidentally blocking them.
4. **Reverse-engineering a competitor's citation** [inference]: when an AI
   answer cites a competitor, the cited URLs reveal which directories/forums
   the engine pulled from; get listed in the same ones (ties back to the
   directory checklist).

## 7. Open questions / unknowns

- ChatGPT search's index partner: unresolved at primary sources this session
  [claim, unverified that it is Bing].
- Copilot's pipeline: no primary doc fetched; everything in §2/Copilot is
  inference.
- Local-query GEO effect sizes: the paper's benchmark contains no
  local-business queries; treat its percentages as informational-query
  measurements.
- Reddit's role: documented as a ChatGPT input via the OpenAI partnership
  [verified]; its weight in answers, and any equivalent Perplexity/Claude
  deal mechanics, remain unquantified (fetch routes all blocked this
  session).
- llms.txt: no engine has documented that it consults the file (§6 of
  llmstxt.org's own text lists publisher-side adoption only).

## Sources

All fetched 2026-10-11 from this project's sessions; raw copies in `src/`.

- https://platform.openai.com/docs/bots — OAI-SearchBot/GPTBot/ChatGPT-User
  roles, 24h propagation, IP lists [verified]
- https://openai.com/policies/terms-of-use/ — automated-extraction prohibition
  [verified]
- https://docs.perplexity.ai/guides/bots — PerplexityBot/Perplexity-User,
  robots.txt handling, IP list [verified]
- https://www.anthropic.com/news/web-search — Claude web search launch dates
  [verified]
- https://docs.anthropic.com/en/docs/build-with-claude/search-results —
  search-result content blocks (API citation mechanism) [verified]
- https://ai.google.dev/gemini-api/docs/google-search — grounding pipeline +
  `url_citation` output shape [verified]
- https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers
  — current crawler taxonomy; no Google-Extended section remains [verified]
- https://openai.com/index/introducing-chatgpt-search/ — search stack:
  fine-tuned GPT-4o, third-party search providers/partner content [verified]
- https://openai.com/index/openai-and-reddit-partnership/ — Reddit Data API
  feeds ChatGPT ("real-time, structured" content) [verified]
- https://docs.perplexity.ai/docs/getting-started/overview — Agent API +
  Search API existence [verified; pricing unknown (not fetched)]
- https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/web-search-tool
  — `web_search` returns cited sources [verified]
- https://arxiv.org/abs/2311.09735 — GEO paper abstract [verified]
- https://arxiv.org/html/2311.09735 (full text) — GEO-bench composition and
  effect sizes [verified]
- https://llmstxt.org — self-described "a proposal"; adoption claims are the
  site's own words [verified as fetched]
- https://indexnow.org/documentation — shared-submission protocol, key-file,
  429 spam signal, 10k URL cap, participant engines [verified]
- https://openai.com/searchbot.json , https://openai.com/gptbot.json ,
  https://www.perplexity.com/perplexitybot.json — published crawler IPs
  [verified]
- Reddit JSON (r/SEO et al.), old.reddit, PullPush, redlib instances — 403/429
  on every route from this network [blocked, unverified]
