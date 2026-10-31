# Add Paddle Review — Repeatable Workflow

> **Use when:** User says "add [paddle name]" or "add paddle review for [paddle]"
> **Context:** Project lives at `/Users/7p/myFiles/brainstormer/pickleball-review-hub/`
> **Golden rule:** Never use auto-generated YouTube captions. Only verified sources: creator websites, YouTube API metadata, verified measurement databases.

## Step 1: Find the Brand

Look up the brand in `docs/brand-websites.md` for the official website. If not found:
```
web_search(query="[brand] pickleball official website")
```

Record: `brand_name`, `official_site_url`

## Step 2: Verify Product Name

Search the official brand site for the exact product name. Check:
- Exact spelling (including capitalization, spacing)
- Shape variants (Elongated, Widebody, Hybrid, Standard)
- Core thickness (14mm, 16mm)

**Common pitfalls:**
- "Lux Inferno" → "LUXX Control Air" (Selkirk, double X)
- "Luzz Inferno" → "Luzz Pro 4 Inferno" (full name)
- "Selkirk Lux Inferno" → Does not exist

## Step 3: Gather Verified Data

Check these 3 verified data sources:
1. **Pickleball Studio** — `https://pickleballstudio.com/paddles/[slug]`
2. **John Kew** — `https://johnkewpickleball.com/[slug]`
3. **The Kitchen** — `https://thekitchenpickle.com/paddle/[slug]`

For each source, extract:
- Measured specs: swing_weight, spin_rpm (or spin), twist_weight, balance, static_weight
- Written review quotes (direct quotes from creator website)
- YouTube videos (title, URL, channel, date)
- Retailer links (name, URL, price)

**If a paddle is NOT in Pickleball Studio:**
- Use John Kew measured specs (preferred)
- Use manufacturer listed specs as fallback
- Set `specs_source` with the verified URL

## Step 4: Create Paddle Entry

Use this JSON structure in `data/paddles.json`. **Critical format rules:**

```json
{
    "name": "Full Paddle Name (exact from brand site)",
    "brand": "Brand Name",
    "id": "lowercase-slug-with-dashes",
    "price_range": "$99-$120",
    "price_min": 99,
    "price_max": 120,
    "shape": "Elongated",
    "core_material": "MPP floating foam core",
    "surface_material": "Raw T700 carbon fiber grit",
    "core_thickness": "16mm",
    "handle_length": "5.5\"",
    "grip_circumference": "4.125\"",
    "certifications": "USAP",
    "year_released": 2026,
    "generation": "Gen 4",
    "category": "All-Court",
    "foam_type": "MPP",
    "description": "1-2 sentence description from verified data",
    "measured_specs": {
        "swing_weight": 118.44,
        "spin_rpm": 2022,
        "twist_weight": 6.23,
        "balance": "239 mm",
        "static_weight": "8.06 oz"
    },
    "spin_rpm": 2022,
    "swing_weight": 118.44,
    "twist_weight": 6.23,
    "spin_durability": 3,
    "specs_source": "https://johnkewpickleball.com/slug",
    "written_reviews": [
        {
            "author": "Name",
            "site": "Publisher Name",
            "url": "https://...",
            "quotes": ["Direct quote 1", "Direct quote 2"],
            "pros": ["Pro 1", "Pro 2"],
            "cons": ["Con 1", "Con 2"],
            "disclosure": "Testing methodology note"
        }
    ],
    "youtube_videos": [
        {
            "title": "Video Title",
            "url": "https://youtube.com/watch?v=ID",
            "channel": "Channel Name",
            "date": "YYYY-MM-DD"
        }
    ],
    "retailers": [
        {
            "name": "Store Name",
            "url": "https://...",
            "price": "$99.99"
        }
    ],
    "tags": ["tag1", "tag2", "tag3"]
}
```

**Critical format rules (build.py depends on these):**
- `measured_specs` keys must be plain numbers, NOT dicts: `"spin_rpm": 2022` ✅, `"spin": {"value": 2022}` ❌
- `foam_type` must be one of: `MPP`, `EPP`, `honeycomb`, `EVA`
- `spin_durability` is integer 1-4 (Tier 1 = most durable)
- `youtube_videos` URL must be real youtube.com/watch?v=ID URL (not placeholder)
- `written_reviews` uses `quotes` (plural array), NOT `quote` (singular string)

## Step 5: Build

```bash
cd /Users/7p/myFiles/brainstormer/pickleball-review-hub
python3 build.py
```

If build fails, check error:
- `KeyError: 'foam_type'` → Add `"foam_type": "MPP"` (or correct type)
- `KeyError: 'quotes'` → Change `"quote": "text"` to `"quotes": ["text"]`
- `TypeError: '<' not supported` → `measured_specs.spin_rpm` must be number, not dict

## Step 6: Verify

Test the live page:
```bash
curl -s https://pickleballreviewer.com/pages/paddles/[paddle-slug].html | \
    grep -c "paddle-name"
```

Or use browser to load:
```
goto_url("https://pickleballreviewer.com/pages/paddles/[paddle-slug].html")
```

Check:
- ✅ Status 200
- ✅ Title tag with paddle name
- ✅ OG title and description
- ✅ Price displayed
- ✅ Measured specs (spin_rpm, swing_weight, twist_weight)
- ✅ Written reviews (2+ sources)
- ✅ YouTube videos
- ✅ Retailers
- ✅ Tags rendered
- ✅ GA4 ID: G-6EL1LX9CG6

## Step 7: Commit and Push

```bash
git add -A
git commit -m "add [paddle name] — verified specs from [sources]"
git push
```

## Quick Checklist

- [ ] Brand website found and verified
- [ ] Product name matches official site exactly
- [ ] Measured specs from Pickleball Studio OR John Kew
- [ ] Written reviews: 2+ sources with direct quotes
- [ ] YouTube videos: real URLs (not placeholders)
- [ ] Retailers: 3+ links with prices
- [ ] `measured_specs` uses plain numbers (not dicts)
- [ ] `foam_type` is MPP, EPP, honeycomb, or EVA
- [ ] Build succeeds with `python3 build.py`
- [ ] Live page returns 200
- [ ] All content renders (specs, reviews, videos, retailers)
- [ ] Committed and pushed
