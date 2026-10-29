#!/usr/bin/env python3
"""Reviewer index generator — to be pasted into build.py"""

def generate_reviewer_index():
    """Generate reviewers/index.html listing all reviewers."""
    import os
    
    # Load data
    import json
    with open('data/paddles.json') as f:
        data = json.load(f)
    paddles = data['paddles']
    
    reviewer_data_list = [
        ('Pickleball Studio', 'Pickleball Studio', 'Independent, thorough testing. Founder Chris Olson is a 4.75 DUPR player with 400+ paddles tested since 2021.', 'https://pickleballstudio.com/', 1),
        ('John Kew', 'JohnKew Pickleball', 'Data-driven lab testing. KewCOR firepower measurements, spin RPM, swing weight analysis.', 'https://johnkewpickleball.com/', 1),
        ('The Kitchen', 'The Kitchen Pickleball', 'Expert team. Scored ratings. Independent testing.', 'https://thekitchenpickle.com/', 1),
        ('Pickleball Effect', 'Pickleball Effect', 'Independent lab testing. 513+ paddles measured in-house with Stalker Pro S3 radar, Briffidi swing/twist weight. Braydon Unsicker is a 5.0 player.', 'https://pickleballeffect.com/', 1),
    ]
    
    # Count unique paddles per reviewer and update
    for i, rd in enumerate(reviewer_data_list):
        site = rd[1]
        reviewed_ids = set()
        for p in paddles:
            for r in p.get('written_reviews', []):
                if r.get('site') == site:
                    reviewed_ids.add(p['id'])
                    break
        # rd is a tuple (name, site, desc, url, placeholder_count)
        # Create new tuple with actual count as 6th element
        reviewer_data_list[i] = rd + (len(reviewed_ids),)
    
    # Build cards - now tuples are (name, site, desc, url, old_count, new_count)
    reviewer_cards = ''
    for name, site, desc, url, _old, count in reviewer_data_list:
        slug = name.lower().replace(' ', '-')
        icon = chr(0x1F3AC)  # camera
        reviewer_cards += f'''<a href="{slug}.html" class="category-card">
            <span class="category-icon">{icon}</span>
            <h3>{name}</h3>
            <p class="category-desc">{desc}</p>
            <p class="category-price">{count} paddle(s) reviewed</p>
        </a>'''
    
    # Build page
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Top pickleball paddle reviewers. Verified written reviews and measured data from trusted sources.">
    <title>Top Reviewers — Pickleball Review Hub</title>
    <!-- Open Graph -->
    <meta property="og:title" content="Top Pickleball Paddle Reviewers — Pickleball Review Hub">
    <meta property="og:description" content="Top pickleball paddle reviewers. Verified written reviews and measured data from trusted sources.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://pickleballreviewer.com/reviewers/index.html">
    <meta property="og:image" content="https://pickleballreviewer.com/og-image.png">
    <link rel="stylesheet" href="../css/style.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
</head>
<body>
    <header class="site-header">
        <div class="container">
            <a href="../index.html" class="logo">
                <span class="logo-icon">{chr(0x1F3D3)}</span>
                <span class="logo-text">Pickle<span class="highlight">Reviewer</span></span>
            </a>
            <nav class="main-nav">
                <a href="../index.html" class="nav-link">All Paddles</a>
                <a href="../pages/categories/index.html" class="nav-link">Categories</a>
                <a href="../pages/guides/index.html" class="nav-link">Guides</a>
                <a href="../pages/best-of/index.html" class="nav-link">Best Of</a>
                <a href="index.html" class="nav-link active">Reviewers</a>
                <a href="../pages/compare.html" class="nav-link">Compare</a>
            </nav>
        </div>
    </header>

    <main>
        <div class="product-page-header">
            <div class="container">
                <h1>Top Pickleball Paddle Reviewers</h1>
                <p>Verified written reviews and measured data from trusted creators.</p>
            </div>
        </div>

        <section class="products-section">
            <div class="container">
                <div class="categories-grid">
                    {reviewer_cards}
                </div>
            </div>
        </section>
    </main>

    <footer class="site-footer">
        <div class="container">
            <div class="footer-bottom">
                <p>&copy; 2026 Pickleball Review Hub. All rights reserved. | <a href="../privacy.html">Privacy</a> | <a href="../../affiliate-disclosure.html">Affiliate Disclosure</a></p>
            </div>
        </div>
    </footer>

    <!-- Google Analytics 4 — Replace G-XXXXXXXXXX with your GA4 measurement ID -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-XXXXXXXXXX');
    </script>
    <script src="../js/app.js"></script>
</body>
</html>'''
    
    OUTPUT_DIR = 'output'
    os.makedirs(os.path.join(OUTPUT_DIR, 'reviewers'), exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, 'reviewers', 'index.html')
    with open(out_path, 'w') as f:
        f.write(html)
    print(f"   ✅ Reviewers index → reviewers/index.html")


if __name__ == '__main__':
    generate_reviewer_index()
