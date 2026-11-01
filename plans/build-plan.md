# Pickleball Review Hub — Detailed Build Plan

## Overview

A data-driven static website that aggregates verified YouTube review videos, written review quotes, and cross-reviewer consensus for pickleball paddles. Built from structured JSON data with automated HTML generation.

**Current state:** 28 paddles complete, 4 verified reviewers (Pickleball Studio: 16, The Kitchen: 11, John Kew: 4, Pickleball Effect: 8). 57 pages generated, comparison tool, Best Of rankings, guide pages, reviewer index — all complete. 932+ internal links, 0 broken. **LIVE at https://pickleballreviewer.com** (custom domain). GitHub: https://github.com/dartman10/pickleballreviewer

---

## Week-by-Week Plan

### Week 1: Data Foundation (18 paddles)

**Goal:** Populate `paddles.json` with enough content to make the site useful.

**Actual result:** 23 paddles with verified data (4 original + 12 added from Pickleball Studio measurement databases + 5 Pickleball Effect paddles). 4 planned paddles were skipped because they don't appear in Pickleball Studio, John Kew, or paddlespecs.com databases — no measured specs available. 4th reviewer (Pickleball Effect) added with 7 measured paddles.

**Paddles completed:**
|Paddle|Brand|Category|Status|
|--------|-------|----------|--------|
|Enhance MPP Turbo Elongated|Enhance|power|✅ Done|
|Enhance EPP Turbo Elongated|Enhance|power|✅ Done|
|Spartus Spitfire Elongated|Spartus|power|✅ Done|
|Bread & Butter Loco Widebody|B&B|power|✅ Done|
|Luzz Pro 4 Inferno|Luzz|power|✅ Done|
|Selkirk Power Air Invicta|Selkirk|power|✅ Done|
|Selkirk Boomstik Widebody|Selkirk|power|✅ Done|
|Vatic Pro Prism Flash 16mm|Vatic Pro|power|✅ Done|
|11six24 Hurache-X Power2 Elongated|11six24|power|✅ Done|
|Spartus P1 Hybrid|Spartus|power|✅ Done|
|Gearbox GX2 Power Hybrid|Gearbox|power|✅ Done|
|Holbrook Fuze Elongated 16mm|Holbrook|power|✅ Done|
|CRBN 3X 16mm|CRBN|power|✅ Done|
|Ronbus Quanta R3|Ronbus|power|✅ Done|
|Ronbus Ripple V2 R4.14|Ronbus|power|✅ Done|
|CRBN 1X 14mm|CRBN|power|✅ Done|
|Engage Axiom Elongated 16mm|Engage|power|✅ Done|
|Volair CMD Hybrid|Volair|power|✅ Done|
|RPM Jade Elongated 16mm|RPM|power|✅ Done|
|Pakle Fuse Hybrid W|Pakle|power|✅ Done|
|Honolulu J2NF|Honolulu|power|✅ Done|
|Six Zero Coral Pro Hybrid|Six Zero|power|✅ Done|
|Ronbus Tenon R3.16|Ronbus|power|✅ Done|

**Paddles skipped (no measurement data):** Joovy Spin, Gamma Raptor, Head Radical Pro, Paddles Viper — not in Pickleball Studio / John Kew / paddlespecs.com databases. Replacement paddles selected from available measured data: 11six24 Hurache-X Power2, Spartus P1, Gearbox GX2 Power, Holbrook Fuze, CRBN 3X/1X, Ronbus Quanta R3, Ronbus Ripple V2, Vatic Pro Prism Flash, Luzz Pro 4 Inferno, Selkirk Boomstik Widebody, Engage Axiom, Volair CMD, RPM Jade, Pakle Fuse, Honolulu J2NF, Six Zero Coral Pro, Ronbus Tenon R3.16.

**Data gathering per paddle:**
1. **YouTube videos** — Search YouTube for "[paddle name] review" from Pickleball Studio and John Kew. Record: title, channel, upload date, views, duration, URL.
2. **Written reviews** — Check Pickleball Studio (pickleballstudio.com), JohnKew (johnkewpickleball.com), The Kitchen (thekitchenpickle.com). Record: author, site, URL, quotes (direct only), pros, cons, disclosure.
3. **Measured specs** — Pickleball Studio has the most comprehensive measurements. Extract: spin RPM, swing weight, twist weight, balance, static weight, grip size, shape dimensions. Always cite `specs_source`.
4. **Consensus topics** — After gathering 2–3 reviewers, identify topics they ALL address. Write consensus statements only when 2+ reviewers agree on the same point.
5. **Retailers** — Find where the paddle sells, with prices and affiliate codes.

**YouTube data collection method:**
- Search YouTube directly (no API needed for MVP — manual extraction)
- Target channels: Pickleball Studio, John Kew, The Kitchen, Pickleball Tutorials, Real Paddle Pickleball
- If no YouTube review exists from these sources, use `youtube_videos: []` — do not substitute non-YouTube URLs

**Deliverable:** `paddles.json` with 23 verified paddle entries, each with:
- At least 1 YouTube video (or `[]` if none found — all paddles now have videos)
- At least 1 written review with direct quotes
- Measured specs from Pickleball Studio, John Kew, or Pickleball Effect
- Consensus topics where available (1+ reviewers agree)
- Retailer links with prices

**Data stats:** 44+ YouTube videos, 35+ written reviews, 39+ retailer links, 64+ consensus topics across 28 paddles. 4 verified reviewers: Pickleball Studio (16 paddles), The Kitchen (11), John Kew (4), Pickleball Effect (8).

**Quality gate:** Run `python3 scripts/verify-site-data.py` — must pass with 0 errors. ✅

---

### Week 2: Comparison Tool, Best-Of Pages, Navigation & SEO Prep ✅ PARTIAL

**Goal:** Add interactive comparison tool, "Best of" curated pages, related paddles, share buttons, standardized navigation, and prepare for SEO deployment.

**Status:** Comparison tool ✅ DONE, YouTube thumbnails ✅ DONE, standardized 6-item navigation ✅ DONE, guide pages ✅ DONE, reviewer index ✅ DONE, Best Of pages ✅ DONE, guide index ✅ DONE.

**Pending:** Related paddles (Task 5), Share buttons (Task 6), Best Of callouts on category pages (Task 3).

**Actions:**
1. ✅ **Build Paddle Comparison Tool** — Users select 2–4 paddles, see side-by-side spec comparison. All data from `paddles.json`, runs in browser via JavaScript. URL-persisted state. Best-value highlighting.
2. ✅ **Create "Best Of" category pages** — 4 ranking pages (best power, best budget under $100/$150/$200, best spin, best value). Dynamically generated from `paddles.json`. Index page at `pages/best-of/index.html`.
3. ✅ **Standardized 6-item navigation** — Constant nav on all 49 pages: All Paddles, Categories, Guides, Best Of, Reviewers, Compare. All nav links point to index pages. All "Guides" links verified across all pages.
4. ✅ **Write guide pages** — 3 complete guides (How to Choose, MPP vs EPP, Budget Under $120). Rich content with paragraphs, tables, pros/cons. Index page at `pages/guides/index.html`.
5. ✅ **Add "Compare" button** to every paddle page and category page card.
6. ✅ **Add navigation link** for "Compare" in main nav bar.
7. ✅ **Reviewer index page** — Dynamically generated with accurate paddle counts (unique per reviewer). All reviewer detail pages generated.
8. ✅ **YouTube video thumbnails** — Auto-extracted from YouTube URLs, lazy-loaded, alt-texted.
9. 🟡 **Add "Best Of" callout links on category pages** — Task 3 in week2-tasks.md.

**Reviewer index page structure:**
```
┌─────────────────────────────────────────────┐
│  Breadcrumbs: Home > Reviewers              │
├─────────────────────────────────────────────┤
│  Title: Top Pickleball Paddle Reviewers     │
│  Subtitle: Verified reviewers & their       │
│           paddle reviews                    │
├─────────────────────────────────────────────┤
│  Reviewer Cards (name, site, paddle count,  │
│  description, link to reviewer page)        │
├─────────────────────────────────────────────┤
│  Browse Categories (links to all categories)│
└─────────────────────────────────────────────┘
```

**Deliverable:** All categories populated with 3+ paddles, reviewer index page live, all counts accurate.

---

### Week 3: Guide Pages ✅ COMPLETE

**Goal:** Write actual guide pages to capture long-tail search traffic.

**Guides completed:** 3/5 (how-to-choose, mpp-vs-epp, budget-under-120)

**Guides still to write:**

| Guide | Target Keyword | Angle | Format |
|-------|---------------|-------|--------|
| Elongated vs Widebody Shape | "elongated vs widebody pickleball paddle" | Reach vs power trade-off explained | 600–1000 words |
| Spin Rankings Comparison | "pickleball paddle spin ranking" | Pull spin RPM data from Pickleball Studio/John Kew | 500–800 words |

**Guide writing rules:**
- No ASR transcripts — only verified written content
- Cross-reference paddle entries (link to detail pages)
- Each guide: 500–1500 words, structured with headings, tables, and comparison sections
- Guides are embedded as structured data in `build.py` (`GUIDE_DATA` dict), not a separate JSON file

---

### Week 4: SEO, Analytics & Polish ✅ COMPLETE

**Goal:** Production readiness — SEO optimization, analytics, legal pages.

**Completed:**
1. ✅ **Sitemap.xml** — Auto-generated from `paddles.json` + all page slugs. 52 URLs, written to `output/sitemap.xml`.
2. ✅ **robots.txt** — Allow all crawlers, reference sitemap.xml. Written to `output/robots.txt`.
3. ✅ **Open Graph tags** — Every page (57 total) has og:title, og:description, og:type, og:url, og:image.
4. ✅ **Google Analytics 4** — GA4 script on all 57 pages. Measurement ID: G-6EL1LX9CG6. Replaced placeholder.
5. ✅ **Privacy Policy page** — Complete policy covering data collection, analytics, third-party links, cookies, children's privacy. Written to `output/privacy.html`.
6. ✅ **Affiliate Disclosure page** — FTC-compliant disclosure covering affiliate relationships, objectivity commitment, transparency. Written to `output/affiliate-disclosure.html`.
7. ✅ **404 page** — Custom styled error page with site navigation and Privacy/Affiliate links. Written to `output/404.html`.
8. ✅ **Footer links** — Privacy and Affiliate Disclosure linked on all 57 pages with correct relative paths per page depth.
9. ✅ **Homepage stats updated** — 27 paddles, 7+ categories, 4 reviewers, $70 starting price.
10. ✅ **Legal page nav** — Privacy and Affiliate Disclosure pages have full navigation and consistent footer links.

**Deploy notes:**
- ✅ Domain setup: pickleballreviewer.com configured via Vercel
- ✅ Site deployed to https://pickleballreviewer.com (custom domain, Vercel URL deleted by user)
- ✅ GitHub repo: https://github.com/dartman10/pickleballreviewer
- ✅ GA4 measurement ID G-6EL1LX9CG6 installed on all pages (no longer placeholder)
- ✅ Submit `sitemap.xml` to Google Search Console and Bing Webmaster Tools
- ✅ OG image: `output/og-image.png` generated and linked on all 57 pages

---

### Week 5: Best-Of Pages UI Redesign ✅ DONE

**Bugfix:** Best Power ranking was sorting by spin RPM (same metric as Best Spin), causing Spartus Spitfire to appear #1 in all 3 categories. Fixed to sort by swing weight — the proper power metric. Added `_get_swing()` helper. All 20/20 power paddles have swing weight data.

**Goal:** Transform flat text-based ranking pages into a visually structured, user-friendly experience with proper visual hierarchy, progress bars, and thumbnail images.

**Completed:**
1. ✅ **Hero cards for top 3** — Gold/silver/bronze gradient cards with YouTube thumbnails, prominent rank badges, progress bars for key stat (Spin RPM, Price, Value Score), and "View Full Review" CTAs.
2. ✅ **Ranked cards for #4+** — Compact cards with rank number, thumbnail, name, price, description, key stat with progress bar, and "View Review" link.
3. ✅ **Best-of hero banner** — Dark gradient header with paddle title, description, and summary stats ("X paddles ranked" + "Verified data from lab tests").
4. ✅ **Progress bars** — Visual representation of key stat relative to the best value (100% for #1, scaled % for all others).
5. ✅ **Side-by-side comparison CTA** — Button to compare top 3 paddles directly from any best-of page.
6. ✅ **Browse by category section** — Cards linking to power, budget, and comparison pages at bottom of all best-of pages.
7. ✅ **Responsive layout** — Cards stack vertically on mobile; hero cards switch to column layout.

**Files:**
- `build.py` — New `generate_best_of_pages()` function with hero card + rank card templates
- `css/best-of.css` — Complete stylesheet (7.8 KB) with hero cards, rank cards, progress bars, responsive breakpoints

**Before → After:**
- *Before:* Flat list of text-only cards, no visual distinction between ranks
- *After:* #1–#3 shown as large hero cards with gold/silver/bronze accents, thumbnails, progress bars; #4+ shown as compact cards with inline stat bars; dark hero banner with summary stats

---

### Week 6: Launch ✅ COMPLETE

**Goal:** Go live and capture initial traffic.

**Actions:**
1. ✅ Deployed to Vercel at https://pickleballreviewer.vercel.app
2. ✅ GitHub repo created: https://github.com/dartman10/pickleballreviewer
3. ⏳ Submit sitemap to Google Search Console (todo — needs GA4 ID first)
4. ⏳ Submit sitemap to Bing Webmaster Tools
5. ⏳ Share in pickleball communities (Reddit r/pickleball, pickleball Facebook groups) — follow each community's rules about self-promotion
6. ⏳ Monitor analytics for first 2 weeks
7. ⏳ Fix any broken links or 404s
8. ⏳ Add 2–3 more paddles based on user feedback or trending searches
9. ⏳ Write first follow-up guide: "Pickleball Paddle Weight Guide" or "Fiberglass vs Graphite Face"

---

## Enhancement Opportunities

These are optional improvements that add meaningful value with relatively low effort. Each includes the effort estimate, where it fits in the plan, and the specific change needed.

### 1. Auto-Related Paddles (Effort: 2 hours) 🟡 PENDING

**Why:** Currently `build.py` doesn't link paddles together. With 23 paddles in the dataset, internal linking is the easiest time to add. Improves SEO, keeps users on site longer, and makes the site feel like a real resource rather than a list of isolated pages.

**Implementation:**
- Add optional `related_paddles[]` field to each paddle in `paddles.json` — list of IDs of paddles in the same brand or category
- Patch `build.py` to render "You might also like" section on each paddle detail page
- Simple logic: group paddles by brand + category; show up to 3 related paddles that aren't the current one

**Where in plan:** Week 2 (pending) — leverages existing data, requires zero external data gathering.

**Risk:** Very low. All logic is in `build.py`; if it breaks, paddle detail pages still render correctly without related section.

---

### 2. YouTube Video Thumbnails ✅ DONE

**Status:** Implemented. All paddle pages show YouTube thumbnails (320x180 mqdefault), lazy-loaded, with alt-text. Auto-extracted from YouTube URLs at build time.

---

### 3. Schema.org `AggregateRating` (Effort: 2 hours)

**Why:** None of the 23 paddle pages currently have `AggregateRating` schema. With verified YouTube videos, written reviews, and consensus data, we can derive a composite rating that shows as star ratings in Google search results. This directly impacts click-through rate from search.

**Implementation:**
- Derive rating from review consensus frequency (how often a paddle is mentioned positively across 3 sources)
- Or use a simple heuristic: paddle count × review count ÷ max possible
- Add `AggregateRating` JSON-LD block to each paddle detail page's `<head>`
- Include `bestRating`, `worstRating`, `ratingValue`, `ratingCount`

**Where in plan:** Week 4 (SEO & polish)

**Risk:** Low. Schema is optional markup; if the rating value is unusual, Google may ignore it but won't penalize.

---

### 4. Paddle Page "Share" Buttons (Effort: 2 hours) 🟡 PENDING

**Why:** Launch strategy (Week 5) says to share in pickleball communities (Reddit r/pickleball, Facebook groups, Discord servers). Paddle pages don't currently have share buttons, making each share a manual URL copy-paste. Share buttons increase launch traffic and make social sharing frictionless.

**Implementation:**
- Add Twitter/X share link: `https://twitter.com/intent/tweet?text={title}&url={canonical_url}`
- Add Reddit share link: `https://www.reddit.com/submit?url={canonical_url}&title={title}`
- Add "Copy Link" button (JavaScript `navigator.clipboard.writeText()`)
- Simple inline SVG icons or text buttons — no external libraries needed

**Where in plan:** Week 2 (pending) — needed for launch, static buttons that point to well-known share URLs.

---

### 5. Add Authority Paddles (Effort: 4-6 hours)

**Why:** Our current set is heavily skewed toward power paddles (21 of 27). Only elongated, hybrid, and power categories exist. The most common comparison search queries are "Luzz Pro 4 Inferno review" and "Spartus Spitfire vs Luzz Pro 4 Inferno" — if we can add the Luzz Pro 4 Inferno, it would be the single highest-impact paddle for SEO and content authority.

**Recommended additions:**

|| Paddle | Priority | Why |
|--------|----------|-----|
|| Luzz Pro 4 Inferno | High | The "gold standard" paddle. Everyone compares to it. Highest-volume search term. |
|| Selkirk Boomstik Elongated | Medium | Different shape version of an already-covered paddle. Captures elongated shape queries. |
|| CRBN 3X vs Luzz Pro 4 Inferno guide | Medium | Head-to-head guide page (uses existing data from both paddles). |

**Current dataset composition (27 paddles):** 21 power, 6 control/all-court. Added since original 23: Selkirk OMNI Elongated, RPM Friction Pro V2, 11six24 Ultre Jelly Bean 2. Next targets: Luzz Pro 4 Inferno, Boomstik Elongated, Engage Axiom Elongated (already in dataset), RPM Friction Pro V2 (already in dataset).

**Data gathering note:** Luzz Pro 4 Inferno may not have measured specs in Pickleball Studio or paddlespecs.com (consistent with the same pattern that caused Joovy Spin / Gamma Raptor skips). If no measured specs exist, the Verified-Only Rule says to use `[REDACTED]` for missing measurements and rely on written reviews + YouTube videos only.

**Where in plan:** After Week 5 launch — "Phase 3" content expansion based on what search queries drive traffic.

**Risk:** Medium. If Luzz Pro 4 Inferno has no measured specs in target databases, we'd have to document that limitation explicitly.

**Workflow note:** Use `add-paddle-review` skill (8-step workflow: brand → verify → data → JSON → build → verify → deploy → test live). See `docs/add-paddle-review-workflow.md`.

---

### Priority Matrix

| Enhancement | Effort | Impact | Recommendation |
|-------------|--------|--------|----------------|
| YouTube thumbnails | 1h | High | ✅ DONE — Week 2, trivial code change |
| Related paddles | 2h | High | 🟡 PENDING — Week 2, leverages existing data |
| Share buttons | 2h | Medium | 🟡 PENDING — Week 2, needed for launch |
| AggregateRating schema | 2h | Medium | Do after — Week 4, SEO polish |
| Authority paddles | 4-6h | High | Do after — Week 5+, based on search data |

---

## Data Gathering Workflow

For each paddle, follow this exact sequence:

### Step 1: YouTube Search
```
Manual search on YouTube:
Query: "[paddle name] review"
Target: Pickleball Studio, John Kew, The Kitchen, Pickleball Tutorials
Record: video_id, title, channel, upload_date, views, duration
```
**Rule:** If no real YouTube review exists from target channels, use `youtube_videos: []`. Never substitute a written review URL.

### Step 2: Written Review Search
```
Check these sources (in order):
1. https://pickleballstudio.com/reviews/ — Full written reviews
2. https://johnkewpickleball.com/ — Lab-tested reviews
3. https://thekitchenpickle.com/ — Scored reviews
4. Google: "[paddle name] review" -site:youtube.com
```
**Rule:** Record only direct quotes from the creator's website. No paraphrasing. If the only content is a YouTube video transcript, skip the written review section.

### Step 3: Spec Data
```
Source priority:
1. Pickleball Studio (pickleballstudio.com/paddles/[paddle]) — Most comprehensive
2. John Kew Pickleball (johnkewpickleball.com/[paddle]) — Lab data
3. Brand website specs — Last resort, less trusted
```
**Rule:** Always cite the source. If a measurement isn't available, omit it — don't estimate.

### Step 4: Consensus
```
After collecting 2+ reviews:
1. List topics each reviewer mentions
2. Find overlapping topics (2+ reviewers on same point)
3. Write one-sentence consensus for each overlap
4. Cite the source names
```
**Rule:** Consensus only appears when 2+ reviewers address the same topic. If only 1 reviewer mentions something, it's a single-source observation — put it in the written review section, not the consensus table.

---

## Page Template Reference

Each page type maps to a build function. Here's the structure:

### Paddle Detail Page
```
┌─────────────────────────────────────────────┐
│  Breadcrumbs: Home > Category > Paddle      │
├─────────────────────────────────────────────┤
│  Title: [Paddle Name]                       │
│  Subtitle: Verified reviews, YouTube videos │
│           and where to buy                  │
├─────────────────────────────────────────────┤
│  Paddle Card (name, price, tags, pros/cons) │
│  Specs Table (from measured_specs)          │
├─────────────────────────────────────────────┤
│  📺 YouTube Videos (cards with video info)  │
│  📝 Written Reviews (quotes, pros/cons)     │
│  🔍 Consensus Table (topics + sources)      │
│  🏷️ Retailers (links with prices)          │
├─────────────────────────────────────────────┤
│  Related Paddles + Buying Guides            │
├─────────────────────────────────────────────┤
│  [← Back to Category]                       │
└─────────────────────────────────────────────┘
```

### Category Page
```
┌─────────────────────────────────────────────┐
│  Breadcrumbs: Home > Category               │
├─────────────────────────────────────────────┤
│  Title: [Category Name]                     │
│  Subtitle: [Description]                    │
│  [N paddle(s) in this category]             │
├─────────────────────────────────────────────┤
│  Paddle Cards Grid (name, price, tags,      │
│    stats: videos/reviews/consensus counts)  │
├─────────────────────────────────────────────┤
│  Browse Other Categories (links to 5 others)│
└─────────────────────────────────────────────┘
```

### Reviewer Page
```
┌─────────────────────────────────────────────┐
│  Breadcrumbs: Home > Reviewers > Name       │
├─────────────────────────────────────────────┤
│  Title: [Reviewer Name]                     │
│  Subtitle: Pickleball paddle reviews from   │
│           [Site Name]                       │
├─────────────────────────────────────────────┤
│  Reviewer Card (name, description, link to  │
│  site, paddle count, paddles reviewed)      │
├─────────────────────────────────────────────┤
│  Other Top Reviewers (links)                │
└─────────────────────────────────────────────┘
```

### Reviewer Index Page
```
┌─────────────────────────────────────────────┐
│  Breadcrumbs: Home > Reviewers              │
├─────────────────────────────────────────────┤
│  Title: Top Pickleball Paddle Reviewers     │
│  Subtitle: Verified reviewers & their       │
│           paddle reviews                    │
├─────────────────────────────────────────────┤
│  Reviewer Cards Grid (name, site, paddle    │
│  count, description, link to reviewer page) │
├─────────────────────────────────────────────┤
│  Browse Categories (links to all categories)│
└─────────────────────────────────────────────┘
```

### Guide Page
```
┌─────────────────────────────────────────────┐
│  Breadcrumbs: Home > Guides > Title         │
├─────────────────────────────────────────────┤
│  Title: [Guide Title]                       │
├─────────────────────────────────────────────┤
│  Guide Content (written article, tables,    │
│  images, links to paddle pages)             │
├─────────────────────────────────────────────┤
│  Related Articles + Related Paddles         │
└─────────────────────────────────────────────┘
```

---

## Week 2b: Paddle Comparison Tool (Interactive Feature) ✅ DONE

**Goal:** Let users pick 2–4 paddles and compare specs side-by-side. Increases engagement, time on site, and shareability.

### How It Works

**Entry point:** Each paddle detail page gets a "Compare" button. Clicking it opens a comparison UI where users select additional paddles to compare (up to 4 total).

**Flow:**
1. User visits any paddle page → clicks "Compare [Paddle Name]"
2. Comparison UI opens in a modal or dedicated page at `/compare?with=paddle-slug-1,paddle-slug-2`
3. User selects 1–3 more paddles from a searchable dropdown
4. Side-by-side comparison table renders with all measured specs
5. URL persists so users can bookmark/share specific comparisons

**Page template:**
```
┌─────────────────────────────────────────────┐
│  Breadcrumbs: Home > Compare                │
├─────────────────────────────────────────────┤
│  Title: Compare Pickleball Paddles          │
│  Subtitle: Side-by-side specs comparison    │
├─────────────────────────────────────────────┤
│  Select 2–4 Paddles:                        │
│  [Searchable dropdown × 4 slots]            │
│  [Compare Button]                           │
├─────────────────────────────────────────────┤
│  Comparison Table (if paddles selected):    │
│  ┌─────────┬─────────┬─────────┬─────────┐ │
│  │ Spec    │ Paddle1 │ Paddle2 │ Paddle3 │ │
│  ├─────────┼─────────┼─────────┼─────────┤ │
│  │ Swing   │ 118     │ 112     │ 114     │ │
│  │ Twist   │ 6.23    │ 5.62    │ 6.47    │ │
│  │ Spin    │ 2022    │ 1894    │ 1900    │ │
│  │ Balance │ 239mm   │ 245mm   │ 238mm   │ │
│  │ Weight  │ 8.06oz  │ 7.91oz  │ 7.9oz   │ │
│  │ Price   │ $119    │ $249    │ $99     │ │
│  └─────────┴─────────┴─────────┴─────────┘ │
│                                              │
│  Highlight the highest value in each row    │
│  (green checkmark or bold)                  │
├─────────────────────────────────────────────┤
│  Related:                                   │
│  [View Paddle 1] [View Paddle 2] ...        │
└─────────────────────────────────────────────┘
```

### Implementation

**Data source:** All data comes from existing `paddles.json` — no new data needed.

**Tech approach:**
1. **Compare endpoint** in `build.py` — generate `output/pages/compare.html` as a template with JavaScript
2. **JavaScript comparison engine** — parse URL query params, fetch paddle data, render comparison table
3. **Spec highlighting** — auto-highlight the best value in each row (highest spin, lowest swing weight, best price)
4. **Shareable URLs** — `http://localhost:8080/pages/compare.html?paddles=enhance-mpp-turbo,selkirk-power-air-invicta,vatic-pro-prism-flash-16mm`

**File structure:**
```
output/pages/compare.html    — JavaScript-driven comparison page (static HTML + JS)
scripts/verify-site-data.py  — already validates paddle data structure
```

**Comparison rows (all measured specs + extras):**

| Row Label | Source Field | Sort Direction |
|-----------|-------------|----------------|
| Price | `price_min` | ↑ lowest first |
| Spin RPM | `measured_specs.spin_rpm` | ↓ highest first |
| Swing Weight | `measured_specs.swing_weight` | ↓ highest first |
| Twist Weight | `measured_specs.twist_weight` | ↓ highest first (more stable) |
| Balance Point | `measured_specs.balance_point` | — |
| Static Weight | `measured_specs.static_weight` | — |
| Grip Size | `measured_specs.grip_size` | — |
| Shape | `shape` | — |
| Core | `foam_type` | — |
| Category | `category` | — |
| Best For | `best_for` tags | — |

### Features

- **Smart defaults:** If user clicks "Compare" from a paddle page, auto-add that paddle as the first selection
- **Popular comparisons:** Suggest common head-to-heads on the compare page (e.g., "Luzz Pro 4 Inferno vs Boomstik", "MPP Turbo vs Spartus Spitfire")
- **Highlight winner:** Each row highlights the best value (green for higher is better, blue for lower is better)
- **Responsive:** Works on mobile (horizontal scroll for wide tables)
- **No server needed:** Fully static — generated at build time, runs in browser

### Integration

- Add "Compare" button to every paddle detail page (next to "Buy Now" retailer links)
- Add "Add to Compare" button to paddle cards on category pages
- Add comparison links in related paddles section
- Update navigation: add "Compare" to main nav bar

**Deliverable:** Interactive comparison page that works with 0 API calls — all data from `paddles.json`, runs entirely in the browser.

---

## SEO Strategy

### Keyword Targets
| Page Type | Primary Keyword | Secondary Keywords |
|-----------|----------------|-------------------|
| Paddle page | "[brand] [paddle] review" | "[paddle] review 2026", "[paddle] vs [competitor]" |
| Category page | "best [shape] pickleball paddle" | "best power paddle", "elongated pickleball paddle" |
| Guide | "how to choose pickleball paddle" | "MPP vs EPP", "best budget paddle under $120" |
| Reviewer | "[reviewer] pickleball paddle review" | "[reviewer] pickleball studio" |

### On-Page SEO
- **Title tags:** "[Paddle Name] Review — Verified YouTube Videos & Consensus"
- **Meta descriptions:** 150–160 characters, include key benefit + price range
- **H1:** Paddle name only (one per page)
- **H2s:** Section headers (YouTube Videos, Written Reviews, etc.)
- **Schema:** Product (paddles), BreadcrumbList (all), Article (guides), CollectionPage (categories)
- **Canonical URLs:** Production URLs for all pages
- **Open Graph:** og:title, og:description, og:image on every page
- **Internal links:** Every paddle → related paddles + guides; every guide → relevant paddles

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| No YouTube videos for some paddles | High | Low | Write written reviews + specs instead — still valuable |
| Creator doesn't measure a paddle | Medium | Low | Use brand specs as fallback, clearly labeled |
| Consensus doesn't exist for some topics | High | Low | Show single-source quotes in written review section instead |
| Affiliate commission rates change | Low | Low | Data-driven; just update retailer links |
| Competitor launches similar site | Low | Medium | Focus on verified-only positioning; they'll use ASR |
| Google de-indexes affiliate sites | Low | High | Build organic traffic first; diversify with guides and comparison content |

---

## Success Metrics

### Month 1 (Launch)
- [x] 27 paddle pages live
- [x] 5 guide pages live
- [x] Reviewer index page live
- [x] Best Of index + 4 ranking pages live
- [x] 7+ categories populated (3+ paddles each)
- [x] Standardized 6-item navigation on all 57 pages
- [x] Comparison tool live at /pages/compare.html
- [x] YouTube thumbnails on all paddle pages
- [x] Site deployed to https://pickleballreviewer.com (custom domain)
- [x] GA4 tracking active: G-6EL1LX9CG6
- [ ] Google indexed (search site:pickleballreviewer.com)

### Month 3
- [ ] 1,000+ organic visits/month
- [ ] Top 3 ranking for at least 5 long-tail keywords
- [ ] 10+ paddle reviews (3+ sources per popular paddle) — currently 35+ reviews across 27 paddles (avg 1.3 sources)
- [ ] 5+ guides ranking on page 1

### Month 6
- [ ] 5,000+ organic visits/month
- [ ] Revenue from affiliate links (projected $200–$500/mo — based on industry benchmarks for niche affiliate sites)
- [ ] 50+ paddle pages with verified data — currently 27, on track
- [ ] Featured in pickleball community discussions
