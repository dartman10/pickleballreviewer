# Pickleball Review Hub — Project Reference

## What This Is

A JSON-driven static site that aggregates verified YouTube review videos, written review quotes, and cross-reviewer consensus for pickleball paddles. Modeled after the `golf-launch-monitors` project architecture.

**Project path:** `/Users/7p/myFiles/brainstormer/pickleball-review-hub/`

---

## Architecture

```
pickleball-review-hub/
├── data/paddles.json          # ← Single source of truth
├── build.py                   # Generates all HTML from JSON
├── css/style.css              # Shared styles
├── js/app.js                  # Client-side search/filter
├── index.html                 # Homepage template
├── output/                    # Generated site (deployable)
│   ├── index.html
│   ├── css/style.css
│   ├── js/app.js
│   ├── data/paddles.json
│   ├── pages/paddles/         # 16 paddle detail pages
│   ├── pages/categories/      # 9 category pages
│   ├── pages/guides/          # 3 guide pages
│   └── reviewers/             # 3 reviewer pages
├── plans/
│   ├── project-reference.md   # ← This file
│   └── approach.md            # Verified content methodology
└── verification-checklist.md  # Quality gates before each build
```

---

## How Data Flows

```
data/paddles.json  ──build.py──>  output/ (all HTML pages)
                                         │
                                    Local test
                             python3 -m http.server 8080
                                         │
                                    Deploy to Netlify
```

**To add a new paddle:**
1. Add entry to `data/paddles.json` (same fields, empty arrays for optional)
2. Run `python3 build.py`
3. All pages regenerate automatically

---

## JSON Schema Rules

### Required Fields (Every Paddle Entry)
```json
{
  "id": "unique-slug",           // URL-safe: lowercase, hyphens only
  "name": "Full Display Name",
  "brand": "Brand Name",
  "category": "power",           // or: budget, control, etc.
  "shape": "elongated",          // or: widebody, standard, classic
  "foam_type": "MPP",            // or: EPP, hybrid
  "price_range": "$99–$120",
  "price_min": 99,
  "price_max": 120,
  "description": "One-line summary",
  "specs_source": "https://...",  // Creator measurement page URL
  "measured_specs": {...},
  "youtube_videos": [],          // Empty array, NOT missing
  "written_reviews": [],
  "consensus_topics": [],
  "best_for": [],
  "tags": [],
  "retailers": []
}
```

### YouTube Video Entry
```json
{
  "title": "Video Title",
  "channel": "Creator Name",
  "date": "2026-03-09",
  "views": "43.9K",
  "duration": "12:13",
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```
**Rule:** `url` MUST be a real YouTube URL (`youtube.com/watch` or `youtu.be/`). No article pages, no blog posts, no written review URLs in this field.

### Written Review Entry
```json
{
  "author": "John Kew",           // Person or team name
  "site": "JohnKew Pickleball",   // Display name (used for reviewer page matching)
  "url": "https://...",           // Real URL to the written review
  "quotes": ["Direct quote 1", "Direct quote 2"],
  "pros": ["Pro 1", "Pro 2"],
  "cons": ["Con 1"],
  "disclosure": "Paddles sent free. No payment. No editorial input."
}
```

### Consensus Topic Entry
```json
{
  "topic": "Power level",
  "consensus": "Very high power, best in $100 category",
  "sources": ["Chris Olson", "John Kew", "The Kitchen"]
}
```
**Rule:** Every source name in `sources` MUST exist as an `author` value in `written_reviews` for that same paddle. If not, it's a hallucination — remove it.

### Retailer Entry
```json
{
  "name": "Enhance Pickleball",
  "url": "https://enhancepickleball.com/JOHNKEW",
  "price": "$99.99",
  "code": "JOHNKEW"
}
```

---

## Build Script Patterns

### 1. SEO Schema with Double Braces
```python
# f-string interpolation uses single {}
# JSON uses {}
# So JSON-LD needs {{ }} in f-strings:
page_html = f'''
<script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "{paddle['name']}"
}}</script>
'''
```

### 2. Conditional Rendering
```python
# Only render section if data exists
{video_cards or '<p>No videos yet.</p>'}
```

### 3. Deduplication for Reviewer Pages
```python
# Count unique paddles, not total reviews
reviewed_ids = set()
for p in paddles:
    for r in p.get('written_reviews', []):
        if r.get('site') == site:
            reviewed_ids.add(p['id'])
            break  # Only count each paddle once
```

### 4. Site Matching (Not Author Matching)
```python
# WRONG: match by author name (Chris Olson ≠ "Pickleball Studio")
if r.get('author') == name and r.get('site') == site:

# RIGHT: match by site name (consistent across all reviewers)
if r.get('site') == site:
```

---

## Verification Checklist

Run these checks before every `build.py` run:

### Pre-Build (in data/paddles.json)
- [ ] All source URLs are real (verified via tool call or web search)
- [ ] No ASR/auto-generated transcripts used — only creator websites
- [ ] YouTube URLs are actual YouTube links (youtube.com/watch or youtu.be/)
- [ ] Consensus source names match actual `author` values in `written_reviews`
- [ ] All required fields present (even empty arrays)
- [ ] `youtube_videos: []` instead of missing key
- [ ] No duplicate paddle entries (same id twice)
- [ ] Slugs are URL-safe (lowercase, hyphens, no special chars)

### Post-Build (check output/ pages)
- [ ] All expected files present (16 paddle + 9 category + 3 reviewer + 3 guide)
- [ ] No double `.html` extensions in filenames
- [ ] Each paddle page has SEO schema (Product + BreadcrumbList + canonical)
- [ ] Reviewer pages show correct unique paddle count (not review count)
- [ ] Consensus table sources match actual written review authors
- [ ] Written review links go to real creator websites (not auto-generated)
- [ ] Retailer links are real store URLs with affiliate codes
- [ ] Build script runs without errors

---

## Lessons Learned

### 1. Fake URLs Propagate Instantly
**Problem:** A non-YouTube URL in `youtube_videos` would appear on the generated paddle page as if it were a real video.
**Fix:** Always verify YouTube URLs contain `youtube.com/watch` or `youtu.be/`. For paddles without real YouTube reviews, use `youtube_videos: []`.

### 2. Author Names Don't Match Site Names
**Problem:** Pickleball Studio reviews use "Chris Olson" as author, but reviewer pages are named "Pickleball Studio." Matching by `author` failed.
**Fix:** Match reviewer pages by `site` field (always consistent), not by `author` field (varies by reviewer).

### 3. Count Unique Items, Not Entries
**Problem:** John Kew reviewed Spartus Spitfire twice (two different articles). Counting reviews inflated the count to 3 instead of 2 unique paddles.
**Fix:** Use `set()` of paddle IDs to count unique items.

### 4. Empty Arrays, Not Missing Keys
**Problem:** Paddles without YouTube reviews had no `youtube_videos` field. The build script crashed when trying to iterate over a missing key.
**Fix:** Always include `youtube_videos: []` even when empty.

### 5. Consensus Requires Source Verification
**Problem:** Consensus topic said "Chris Olson, John Kew, The Kitchen" but The Kitchen's review used "The Kitchen Team" as author. String mismatch.
**Fix:** Author name in `written_reviews` must EXACTLY match consensus `sources` array. Changed "The Kitchen Team" → "The Kitchen" for consistency.

### 6. Double-Brace JSON-LD
**Problem:** Python f-strings use `{}` for interpolation, but JSON-LD uses `{}` for objects. `{"@type": "Product"}` breaks the f-string.
**Fix:** Double all JSON-LD braces: `{{"@type": "Product"}}` → renders as `{"@type": "Product"}`.

### 7. Slug Consistency
**Problem:** Guide pages got `.html.html` extensions because slugs in build.py already ended in `.html` and then `.html` was appended again.
**Fix:** Strip trailing `.html` from slugs before appending `.html`: `clean_slug = slug[:-5] if slug.endswith('.html') else slug`.

---

### Current State (as of 2026-10-31)

### Data
- **27 paddles** with verified content
- **44+ YouTube videos** across all paddles (from Pickleball Studio, John Kew, The Kitchen, Pickleball Effect, PickleTip)
- **35+ written reviews** from 4 verified creators
- **39+ retailer links** (Affiliates: Pickleball Studio, Pickleball Warehouse, 11six24, 11six24, etc.)
- **64+ consensus topics** across 27 paddles (all sources verified)
- **5 guides** (How to Choose, MPP vs EPP, Budget Guide, Elongated vs Widebody, Spin Rankings)
- **7+ category pages** (Power, Elongated, Widebody, Hybrid, MPP Foam, EPP Foam, Honeycomb, EVA, Budget)
- **4 reviewer pages** (Pickleball Studio, John Kew, The Kitchen, Pickleball Effect)
- **Interactive Comparison Tool** (compare?with=... URL-based)
- **Constant nav** (All Paddles, Categories, Guides, Best Of, Reviewers, Compare) on all 6 page types
- **4 Best Of ranking pages** (Best Power, Best Budget Under $100, Best Spin, Best Value)
- **GA4 tracking**: G-6EL1LX9CG6 on all pages

### Paddles
| Paddle | Brand | Category | YouTube | Written Reviews | Consensus |
|--------|-------|----------|---------|-----------------|-----------|
| Enhance MPP Turbo Elongated | Enhance | power | 2 | 3 | 6 |
| Enhance EPP Turbo | Enhance | power | 2 | 3 | 7 |
| Luzz Pro 4 Inferno | Luzz | power | 3 | 3 | 5 |
| Selkirk Power Air Invicta | Selkirk | power | 2 | 2 | 4 |
| Selkirk Boomstik Widebody | Selkirk | control | 2 | 2 | 5 |
| Spartus Spitfire Elongated | Spartus | power | 5 | 2 | 6 |
| B&B Loco Widebody | B&B | control | 4 | 1 | 4 |
| CRBN 3X 16mm | CRBN | control | 4 | 4 | 5 |
| CRBN 1X 14mm | CRBN | control | 4 | 3 | 4 |
| Vatic Pro Prism Flash 16mm | Vatic Pro | control | 2 | 2 | 5 |
| 11six24 Hurache-X Power2 | 11six24 | control | 2 | 3 | 6 |
| Spartus P1 | Spartus | control | 2 | 2 | 4 |
| Gearbox GX2 | Gearbox | control | 2 | 2 | 4 |
| Holbrook Fuze | Holbrook | control | 2 | 2 | 4 |
| Vatic Pro Quanta R3 | Vatic Pro | control | 3 | 3 | 5 |
| Ronbus Ripple R4.14 v2 | Ronbus | control | 5 | 2 | 5 |

### Reviewers
| Reviewer | Unique Paddles Reviewed | Site |
|----------|------------------------|------|
| Pickleball Studio | 10 | pickleballstudio.com |
| John Kew | 9 | johnkewpickleball.com |
| The Kitchen | 3 | thekitchenpickle.com |

---

## File Reference

| File | Purpose |
|------|---------|
| `data/paddles.json` | All paddle data — the single source of truth (27 paddles) |
| `data/guides.json` | Guide content (3 guides) |
| `build.py` | Generates all HTML pages from JSON (paddles, categories, reviewers, guides, compare) |
| `css/style.css` | Responsive styles (grid, cards, nav, comparison table) |
| `js/app.js` | Client-side search, filter, render |
| `index.html` | Homepage template |
| `templates/compare.html` | Paddle comparison tool template |
| `scripts/verify-site-data.py` | CLI data validation (8 automated checks) |
| `scripts/test-site.py` | Full page structure validator (32 pages) |
| `plans/build-plan.md` | 5-week execution plan |
| `plans/week1-tasks.md` | Week 1 atomic task tracker |
| `plans/week2-tasks.md` | Week 2 feature task tracker |
| `plans/project-reference.md` | This file — architecture, schema, state |
| `output/` | Generated site — deployable directory (57 pages: 27 paddle + 7 shape + 4 foam + 5 guide + 4 best-of + compare + homepage + 2 legal) |

---

## Next Steps

- [x] Deploy to Vercel at https://pickleballreviewer.com
- [x] Add Google Analytics 4 — G-6EL1LX9CG6 on all 57 pages
- [x] Add structured data (Organization, Website) for SEO
- [x] Expand paddle dataset — 27 paddles, on track for 50+
- [x] Add "Best Of" curated pages — 4 ranking pages live
- [x] Create affiliate disclosure page — live
- [x] Set up Sitemap.xml and robots.txt — 52 URLs
- [ ] Submit sitemap to Google Search Console
- [ ] Submit sitemap to Bing Webmaster Tools
- [ ] Add Google Analytics to Google Search Console
- [ ] Add 10+ more paddles (Lux Inferno, Boomstik Elongated, etc.)
- [ ] Auto-related paddles section on each paddle page (estimated 2h)
- [ ] Paddle share buttons (estimated 2h)
