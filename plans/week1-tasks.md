# Pickleball Review Hub — Week 1: Atomic Tasks Per Paddle

## Task Format

Each task is a self-contained unit of work for one paddle. Follow the same sequence for every paddle. When complete, the paddle entry is ready to be added to `paddles.json`.

---

## Task Template

For each paddle, execute these steps:

### Step 1: YouTube Video Search
- Search YouTube for `"[paddle name] review"`
- Find videos from: Pickleball Studio, John Kew, The Kitchen, Pickleball Tutorials, Real Paddle Pickleball
- For each video found, record:
  - Video ID (from URL)
  - Title
  - Channel name
  - Upload date
  - View count
  - Duration
- If no videos found → `youtube_videos: []`

### Step 2: Written Review Search
- Check these sources in order:
  1. `https://pickleballstudio.com/reviews/` — Full written reviews
  2. `https://johnkewpickleball.com/` — Lab-tested reviews
  3. `https://thekitchenpickle.com/` — Scored reviews
  4. Google: `"[paddle name] review" -site:youtube.com`
- For each review found, record:
  - Author name (person or team)
  - Site name (display name, used for reviewer page matching)
  - URL to the review
  - Direct quotes (copy verbatim — no paraphrasing)
  - Pros mentioned
  - Cons mentioned
  - Disclosure statement
- If no written review found → `written_reviews: []`

### Step 3: Measured Specs Extraction
- Primary source: `https://pickleballstudio.com/paddles/[paddle-slug]`
- Secondary source: `https://johnkewpickleball.com/[paddle-slug]`
- Tertiary: Brand website specs (last resort)
- Extract: spin RPM, swing weight, twist weight, balance point, static weight, grip size, shape dimensions
- Record `specs_source` URL
- Omit measurements not available — don't estimate

### Step 4: Retailer Links
- Find where the paddle sells (brand website, Amazon, Dick's, etc.)
- Record: retailer name, URL, price, affiliate code
- Include 1–3 retailer options

### Step 5: Add to paddles.json
- Add entry following the JSON schema in `plans/project-reference.md`
- Ensure all required fields present
- Ensure `youtube_videos: []` if no videos
- Ensure all consensus source names match actual `author` values

---

## Tasks

### Task 1: Enhance MPP Turbo Elongated ✅ DONE
- **Brand:** Enhance
- **Category:** power
- **Shape:** elongated
- **Foam:** MPP
- **Price range:** $99–$120
- **Why:** Flagship power paddle, most searched in dataset
- **Key angle:** MPP foam provides springy, high-pop feel for aggressive players
- **Expected YouTube channels:** Pickleball Studio, John Kew, The Kitchen
- **Priority:** HIGH — anchors the power category
- **Actual result:** Built and verified. 3 YouTube videos, 3 written reviews, full measured specs, 6 retailer links, 4 consensus topics.

### Task 2: Enhance EPP Turbo Elongated ✅ DONE
- **Brand:** Enhance
- **Category:** power
- **Shape:** elongated
- **Foam:** EPP
- **Price range:** $99–$120
- **Why:** Same paddle as MPP Turbo but with firmer EPP foam — enables MPP vs EPP comparison
- **Key difference from MPP:** Firmer feel, less springy, more connected to the ball
- **Expected YouTube channels:** Pickleball Studio, John Kew, The Kitchen
- **Priority:** HIGH — completes the Enhance family
- **Actual result:** Built and verified. 2 YouTube videos, 2 written reviews (Pickleball Studio, The Kitchen), full measured specs, 4 retailer links, 3 consensus topics.

### Task 3: Spartus Spitfire Elongated ✅ DONE
- **Brand:** Spartus
- **Category:** power
- **Shape:** elongated
- **Foam:** MPP
- **Price range:** $149–$169
- **Why:** Premium power paddle, strong Pickleball Studio coverage
- **Key angle:** Sparta manufacturing pedigree — precision build quality
- **Expected YouTube channels:** Pickleball Studio, John Kew
- **Priority:** HIGH — fills power elongated gap
- **Actual result:** Built and verified. 5 YouTube videos, 2 written reviews, full measured specs, 4 retailer links, 3 consensus topics.

### Task 4: Bread & Butter Loco Widebody ✅ DONE
- **Brand:** B&B
- **Category:** power
- **Shape:** widebody
- **Foam:** MPP
- **Price range:** $119–$139
- **Why:** Affordable power option with widebody sweet spot
- **Key angle:** Budget-conscious power player — under $140 with measured spin
- **Expected YouTube channels:** Pickleball Studio, John Kew
- **Priority:** HIGH — fills power widebody gap
- **Actual result:** Built and verified. 4 YouTube videos, 2 written reviews, full measured specs, 3 retailer links, 2 consensus topics.

### Task 5: Luzz Pro 4 Inferno ✅ DONE
- **Brand:** Luzz
- **Category:** power
- **Shape:** elongated
- **Foam:** MPP
- **Price range:** $229–$249
- **Why:** Premium power paddle competing with Lux Inferno
- **Key angle:** Luzz's flagship — high-tech construction with measured performance data
- **Expected YouTube channels:** Pickleball Studio, John Kew
- **Priority:** HIGH — premium power comparison candidate
- **Actual result:** Built and verified. 2 YouTube videos, 2 written reviews, full measured specs, 3 retailer links, 2 consensus topics.

### Task 6: Selkirk Power Air Invicta ✅ DONE
- **Brand:** Selkirk
- **Category:** power
- **Shape:** elongated
- **Foam:** composite (carbon fiber face + MPP core)
- **Price range:** $199–$229
- **Why:** Carbon fiber face alternative to traditional fiberglass — instant power response
- **Key angle:** Selkirk's carbon fiber technology — feels different from fiberglass paddles
- **Expected YouTube channels:** Pickleball Studio, John Kew
- **Priority:** HIGH — popular power option
- **Actual result:** Built and verified. 2 YouTube videos, 2 written reviews, full measured specs, 3 retailer links, 2 consensus topics.

### Task 7: Selkirk Boomstik Widebody ✅ DONE
- **Brand:** Selkirk
- **Category:** power
- **Shape:** widebody
- **Foam:** MPP
- **Price range:** $159–$179
- **Why:** Widebody power option from the most recognized brand in pickleball
- **Key angle:** Selkirk's widebody power paddle — control-focused within the power category
- **Expected YouTube channels:** Pickleball Studio, John Kew
- **Priority:** HIGH — fills power widebody category
- **Actual result:** Built and verified. 2 YouTube videos, 2 written reviews, full measured specs, 3 retailer links, 2 consensus topics.

### Task 8: Vatic Pro Prism Flash 16mm ✅ DONE
- **Brand:** Vatic Pro
- **Category:** control
- **Shape:** standard
- **Foam:** MPP
- **Price range:** $139–$159
- **Why:** Leading control paddle — the go-to for control-oriented players
- **Key angle:** 16mm thick core — maximum control, maximum precision
- **Expected YouTube channels:** Pickleball Studio, John Kew
- **Priority:** HIGH — controls control category
- **Actual result:** Built and verified. 2 YouTube videos, 2 written reviews, full measured specs, 4 retailer links, 3 consensus topics.

### Task 9: 11six24 Hurache-X Power2 Elongated ✅ DONE
- **Brand:** 11six24
- **Category:** power
- **Shape:** elongated
- **Foam:** hybrid (H3 foam core)
- **Price range:** $139–$159
- **Why:** Innovative foam technology from a respected brand
- **Key angle:** H3 hybrid foam — different from standard MPP/EPP, unique feel
- **Expected YouTube channels:** Pickleball Studio, John Kew
- **Priority:** HIGH — adds 11six24 brand representation
- **Actual result:** Built and verified. 2 YouTube videos, 2 written reviews, full measured specs, 3 retailer links, 2 consensus topics.

### Task 10: Spartus P1 Hybrid ✅ DONE
- **Brand:** Spartus
- **Category:** power
- **Shape:** standard
- **Foam:** hybrid
- **Price range:** $149–$169
- **Why:** Hybrid foam option from a premium manufacturer
- **Key angle:** Spartus engineering — precision-controlled hybrid feel
- **Expected YouTube channels:** Pickleball Studio, John Kew
- **Priority:** MEDIUM — fills power standard category
- **Actual result:** Built and verified. 2 YouTube videos, 2 written reviews, full measured specs, 3 retailer links, 2 consensus topics.

### Task 11: Gearbox GX2 Power Hybrid ✅ DONE
- **Brand:** Gearbox
- **Category:** power
- **Shape:** standard
- **Foam:** hybrid
- **Price range:** $129–$149
- **Why:** Gearbox's power-focused hybrid paddle — adjustable weight system
- **Key angle:** Gearbox's modular design — customizable weight distribution
- **Expected YouTube channels:** Pickleball Studio, John Kew
- **Priority:** MEDIUM — adds Gearbox brand representation
- **Actual result:** Built and verified. 2 YouTube videos, 2 written reviews, full measured specs, 3 retailer links, 2 consensus topics.

### Task 12: Holbrook Fuze Elongated 16mm ✅ DONE
- **Brand:** Holbrook
- **Category:** power
- **Shape:** elongated
- **Foam:** MPP
- **Price range:** $129–$149
- **Why:** Popular elongated paddle from a rising brand
- **Key angle:** Holbrook's build quality — premium materials at mid-range price
- **Expected YouTube channels:** Pickleball Studio, John Kew
- **Priority:** MEDIUM — fills power elongated category
- **Actual result:** Built and verified. 2 YouTube videos, 2 written reviews, full measured specs, 3 retailer links, 2 consensus topics.

### Task 13: CRBN 3X 16mm ✅ DONE
- **Brand:** CRBN
- **Category:** all-court
- **Shape:** standard
- **Foam:** MPP
- **Price range:** $169–$189
- **Why:** CRBN's flagship all-court paddle — precision and versatility
- **Key angle:** "All-court" positioning — works for both power and control players
- **Expected YouTube channels:** Pickleball Studio, John Kew
- **Priority:** MEDIUM — adds CRBN brand, fills all-court category
- **Actual result:** Built and verified. 4 YouTube videos, 2 written reviews, full measured specs, 4 retailer links, 3 consensus topics.

### Task 14: Ronbus Quanta R3 ✅ DONE
- **Brand:** Ronbus
- **Category:** power
- **Shape:** standard
- **Foam:** MPP
- **Price range:** $149–$169
- **Why:** Ronbus's popular power paddle — strong measured performance
- **Key angle:** Ronbus's Quanta foam technology — proprietary core construction
- **Expected YouTube channels:** Pickleball Studio, John Kew
- **Priority:** MEDIUM — adds Ronbus brand
- **Actual result:** Built and verified. 3 YouTube videos, 2 written reviews, full measured specs, 3 retailer links, 2 consensus topics.

### Task 15: Ronbus Ripple V2 R4.14 ✅ DONE
- **Brand:** Ronbus
- **Category:** power
- **Shape:** standard
- **Foam:** MPP
- **Price range:** $139–$159
- **Why:** Ronbus's R4.14 generation — refined power paddle
- **Key angle:** Ripple surface pattern — enhanced spin generation
- **Expected YouTube channels:** Pickleball Studio, John Kew
- **Priority:** MEDIUM — fills power standard category
- **Actual result:** Built and verified. 5 YouTube videos, 2 written reviews, full measured specs, 3 retailer links, 2 consensus topics.

### Task 16: CRBN 1X 14mm ✅ DONE
- **Brand:** CRBN
- **Category:** control
- **Shape:** standard
- **Foam:** MPP
- **Price range:** $159–$179
- **Why:** CRBN's thinnest control paddle — maximum touch and precision
- **Key angle:** 14mm thick core — the thinnest in the dataset, maximum control
- **Expected YouTube channels:** Pickleball Studio, John Kew
- **Priority:** HIGH — only 2nd control paddle, thin-core alternative to Vatic Pro Prism
- **Actual result:** Built and verified. 4 YouTube videos, 2 written reviews, full measured specs, 4 retailer links, 3 consensus topics.

### Task 17: [Paddle Name TBD]
- **Brand:** TBD
- **Category:** [power/control/budget]
- **Shape:** [elongated/widebody/standard]
- **Foam:** [EPP/MPP/hybrid]
- **Price range:** [$XX–$YY]
- **Why:** [Reason for inclusion]
- **Key angle:** [Unique selling point or comparison angle]
- **Expected YouTube channels:** [Channels to search]
- **Priority:** [HIGH/MEDIUM/LOW]

### Task 18: [Paddle Name TBD]
- **Brand:** TBD
- **Category:** [power/control/budget]
- **Shape:** [elongated/widebody/standard]
- **Foam:** [EPP/MPP/hybrid]
- **Price range:** [$XX–$YY]
- **Why:** [Reason for inclusion]
- **Key angle:** [Unique selling point or comparison angle]
- **Expected YouTube channels:** [Channels to search]
- **Priority:** [HIGH/MEDIUM/LOW]

### Task 19: [Paddle Name TBD]
- **Brand:** TBD
- **Category:** [power/control/budget]
- **Shape:** [elongated/widebody/standard]
- **Foam:** [EPP/MPP/hybrid]
- **Price range:** [$XX–$YY]
- **Why:** [Reason for inclusion]
- **Key angle:** [Unique selling point or comparison angle]
- **Expected YouTube channels:** [Channels to search]
- **Priority:** [HIGH/MEDIUM/LOW]

### Task 20: [Paddle Name TBD]
- **Brand:** TBD
- **Category:** [power/control/budget]
- **Shape:** [elongated/widebody/standard]
- **Foam:** [EPP/MPP/hybrid]
- **Price range:** [$XX–$YY]
- **Why:** [Reason for inclusion]
- **Key angle:** [Unique selling point or comparison angle]
- **Expected YouTube channels:** [Channels to search]
- **Priority:** [HIGH/MEDIUM/LOW]

---

## Execution Order

**Status:** All 27 paddles completed. Original execution order was:

1. **Enhance MPP Turbo** — first paddle, established the data gathering workflow
2. **Enhance EPP Turbo** — same brand, validated cross-brand review matching
3. **Spartus Spitfire** — confirmed multi-source written review extraction
4. **Bread & Butter Loco** — verified B&B brand data availability
5. **Luzz Pro 4 Inferno** — corrected from "Selkirk Lux Inferno" based on search results
6. **Selkirk Power Air Invicta** — resolved naming ambiguity (Power Air vs Invicta)
7. **Selkirk Boomstik Widebody** — replacement for unmeasurable Joovy Spin
8. **Vatic Pro Prism Flash 16mm** — first control paddle added
9. **11six24 Hurache-X Power2** — batch #1 (double Week 1), added 4 more
10. **Spartus P1 Hybrid** — batch #1
11. **Gearbox GX2 Power Hybrid** — batch #1
12. **Holbrook Fuze Elongated 16mm** — batch #1
13. **CRBN 3X 16mm** — batch #2, added 4 more to reach 16
14. **Ronbus Quanta R3** — batch #2, brand corrected from "Vatic Pro" to "Ronbus"
15. **Ronbus Ripple V2 R4.14** — batch #2
16. **CRBN 1X 14mm** — batch #2

**Subsequent paddles added when found in Pickleball Studio / John Kew databases:**
- Selkirk Boomstik Widebody (replaced Joovy Spin — no measurement data)
- Vatic Pro Prism Flash 16mm (replaced Gamma Raptor — no measurement data)
- 11six24 Hurache-X Power2, Spartus P1, Gearbox GX2, Holbrook Fuze (replaced Head Radical Pro, Paddles Viper — no measurement data)
- CRBN 3X/1X, Ronbus Quanta R3, Ronbus Ripple V2 (replaced Kettler K1 Pro, Engage PX-3 — no measurement data)

**Post-launch additions (Week 7+):**
17. **Engage Axiom Elongated 16mm** — added from Pickleball Studio measurement database
18. **Volair CMD Hybrid** — added from Pickleball Studio measurement database
19. **RPM Jade Elongated 16mm** — added from Pickleball Studio measurement database
20. **Pakle Fuse Hybrid W** — added from Pickleball Studio measurement database
21. **Honolulu J2NF Hybrid** — added from Pickleball Studio measurement database
22. **Six Zero Coral Pro Hybrid** — added from Pickleball Studio measurement database
23. **Ronbus Tenon R3.16** — added from Pickleball Studio measurement database
24. **Selkirk LUXX Control Air Invikta** — added from John Kew measurement database
25. **Selkirk OMNI Elongated** — added Oct 2026, verified from John Kew, The Kitchen
26. **RPM Friction Pro V2** — added Oct 2026, verified from John Kew, The Kitchen, Pickleball Effect
27. **11six24 Ultre Jelly Bean 2** — added Oct 2026, verified from John Kew, The Kitchen, PickleTip

**Rationale for final set:** All 16 paddles have verified measured specs from Pickleball Studio or John Kew, at least 2 written reviews, and YouTube video coverage. The skipped paddles (Joovy Spin, Gamma Raptor, Head Radical Pro, Paddles Viper) were replaced with measurable alternatives that fill the same category/shape gaps.

---

## Completion Checklist (per paddle)

After completing a task, verify:

- [ ] YouTube videos found and recorded (or `[]`)
- [ ] At least 1 written review with direct quotes (or `[]`)
- [ ] Measured specs from Pickleball Studio or John Kew
- [ ] At least 1 retailer link with price
- [ ] JSON entry added to `paddles.json`
- [ ] `youtube_videos: []` if no videos (not missing key)
- [ ] All consensus source names match actual `author` values
- [ ] `build.py` runs without errors
- [ ] `python3 scripts/verify-site-data.py` passes with 0 errors
- [ ] Paddle page generated and renders correctly

---

## Data Quality Rules (always apply)

1. **No ASR transcripts** — Never use auto-generated YouTube captions for summaries. Only use creator websites for written content.
2. **Direct quotes only** — No paraphrasing in written reviews. Copy verbatim from the creator's website.
3. **Real URLs only** — Every link in the JSON must be a working URL. Verify before adding.
4. **YouTube URLs validated** — `youtube_videos` URLs must contain `youtube.com/watch` or `youtu.be/`. Never substitute a written review URL here.
5. **Consensus requires 2+ reviewers** — Only include consensus topics where 2+ reviewers address the same point.
6. **Source attribution** — Every consensus topic must cite source names that exactly match `author` values in `written_reviews`.
7. **Measured specs only** — Never include manufacturer specs. Only use measurements from Pickleball Studio, John Kew, or verified sources.
