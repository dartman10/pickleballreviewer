# Official Brand Websites — Cross-Verification Reference

> **Usage:** When adding a new paddle review, verify the paddle name and specs against the brand's official website BEFORE adding to `data/paddles.json`.

| Brand | Official Site | Paddle Line |
|-------|--------------|-------------|
| Enhance | https://enhancepickleball.com/collections/paddles | MPP Turbo, EPP Turbo, DUO, SweetSpot Pro, SweetSpot Team, The Banger |
| Luzz | https://luzzpickleball.com/collections/all | Pro 4 Inferno, Fog Original, and more |
| Selkirk | https://www.selkirk.com/collections/pickleball-paddles | Power Air, LUXX (Control Air), OMNI, Vanguard, AMPED, Project Boomstik |
| Spartus | https://gospartus.com/collections/paddles | Spitfire (Elongated/Widebody), P1 (Elongated/Hybrid/Standard), Olympus |
| Bread & Butter | https://www.bnbpickleball.com/collections | Loco, and more |
| Vatic Pro | https://vaticpro.com | Prism Flash, V-Sol Pro |
| 11six24 | https://11six24.com/collections/all | Hurache-X Power², Vapor Power, and 35+ more |
| Holbrook | https://holbrookpickleball.com/collections/all | Fuze (VantaGrit), and more |
| CRBN | https://crbnpickleball.com/collections/all | 3X, 1X, Barrage, TruFoam |
| Ronbus | https://ronbus.com/collections/all | Quanta, Ripple, Tenon |
| Engage | https://engagepickleball.com | Axiom, X2, and more |
| Volair | https://volair.com | Mach 2 Forza, CMD, and more |
| RPM | https://rpmpb.com | Jade, Q2, Friction Pro V2 |
| Pakle | https://paklepickleball.com/collections | Fuse, and more |
| Honolulu | https://808pickle.com | J2NF, and more |
| Six Zero | https://us.sixzeropickleball.com/collections/all | Coral Pro, Coral, Black Opal, Black Diamond, Quartz |
| Gearbox | https://gearboxsports.com/pickleball_en/ | GX2, GB1 balls |

## Verification Checklist for New Paddles

When adding a new paddle review, follow this process:

1. **Find the brand's official website** (listed above)
2. **Search their paddle lineup** for the exact product name
3. **Cross-check specs:**
   - Shape (elongated / widebody / hybrid)
   - Core thickness (14mm / 16mm)
   - Core material (MPP / EPP / honeycomb)
4. **Check the 3 verified data sources:**
   - [Pickleball Studio](https://pickleballstudio.com/paddles/) — measured specs
   - [John Kew](https://johnkewpickleball.com/) — measured specs + written review
   - [The Kitchen](https://thekitchenpickle.com/) — written review + analysis
5. **If a paddle is NOT in Pickleball Studio or paddlespecs.com:**
   - Use John Kew measured specs (preferred)
   - Use manufacturer listed specs as fallback
   - Mark `specs_source` with the verified URL
6. **Add to `data/paddles.json`** with verified data only

## Common Name Pitfalls

| Wrong Name | Correct Name | Notes |
|------------|--------------|-------|
| Lux Inferno | Luzz Pro 4 Inferno | "Lux" is a typo/autocorrect; the brand is **Luzz** (luzzpickleball.com), product is "Luzz Pro 4 Inferno" |
| Lux Pro 4 | Luzz Pro 4 | Same typo — "Lux" ≠ "Luzz" |
| Luzz Inferno | Luzz Pro 4 Inferno | Full product name is "Luzz Pro 4 Inferno" (also sold as "Luzz Inferno" informally) |
| Luxx Control Air | LUXX Control Air | Selkirk uses double X "LUXX" (not "Lux" or "Luxx") |
| Selkirk Lux Inferno | Does not exist | "Lux Inferno" is a typo for "Luzz Pro 4 Inferno"; Selkirk has "LUXX Control Air" |
