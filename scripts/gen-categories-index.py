#!/usr/bin/env python3
"""Categories index generator — called by build.py"""

def generate_categories_index():
    """Generate categories/index.html listing all categories."""
    import os
    import json

    with open('data/paddles.json') as f:
        data = json.load(f)
    paddles = data['paddles']

    # Define all categories with icons, descriptions, and which field to filter on
    category_defs = [
        ('power', '💥', 'Power Paddles', 'Maximum pop and power for aggressive players'),
        ('elongated', '📏', 'Elongated Shape', 'Reach and leverage with an elongated face'),
        ('widebody', '🎯', 'Widebody Shape', 'Larger sweet spot and more stability'),
        ('hybrid', '⚖️', 'Hybrid Shape', 'Balance of power and control'),
        ('mpp', '🧊', 'MPP Foam Core', 'Softer, springy feel — closer to Luzz Pro 4 Inferno'),
        ('epp', '🔥', 'EPP Foam Core', 'Firmer, more connected feel'),
        ('honeycomb', '🐝', 'Honeycomb Core', 'Advanced honeycomb honeycomb technology'),
        ('eva', '🥚', 'EVA Foam Core', 'Traditional EVA foam construction'),
        ('budget', '💰', 'Budget Picks', 'Top performance under $120'),
    ]

    # Count paddles per category
    category_cards = ''
    for slug, icon, name, desc in category_defs:
        count = 0
        for p in paddles:
            if slug == 'power' and p['category'] == 'power':
                count += 1
            elif slug == 'elongated' and p['shape'] == 'elongated':
                count += 1
            elif slug == 'widebody' and p['shape'] == 'widebody':
                count += 1
            elif slug == 'hybrid' and p['shape'] == 'hybrid':
                count += 1
            elif slug == 'mpp' and p['foam_type'] == 'MPP':
                count += 1
            elif slug == 'epp' and p['foam_type'] == 'EPP':
                count += 1
            elif slug == 'honeycomb' and p['foam_type'] == 'honeycomb':
                count += 1
            elif slug == 'eva' and p['foam_type'] == 'EVA':
                count += 1
            elif slug == 'budget' and p.get('price_max', 9999) <= 120:
                count += 1
        category_cards += f'''<a href="{slug}.html" class="category-card">
            <span class="category-icon">{icon}</span>
            <h3>{name}</h3>
            <p class="category-desc">{desc}</p>
            <p class="category-price">{count} paddle(s)</p>
        </a>'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Browse all pickleball paddle categories. Power, control, budget, foam types, shapes, and more.">
    <title>All Categories — Pickleball Reviewer</title>
    <!-- Open Graph -->
    <meta property="og:title" content="All Paddle Categories — Pickleball Reviewer">
    <meta property="og:description" content="Browse all pickleball paddle categories. Power, control, budget, foam types, shapes, and more.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://pickleballreviewer.com/pages/categories/index.html">
    <meta property="og:image" content="https://pickleballreviewer.com/og-image.png">
    <link rel="stylesheet" href="../../css/style.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
</head>
<body>
    <header class="site-header">
        <div class="container">
            <a href="../../index.html" class="logo">
                <span class="logo-icon">{chr(0x1F3D3)}</span>
                <span class="logo-text">Pickleball<span class="highlight">Reviewer</span></span>
            </a>
            <nav class="main-nav">
                <a href="../../index.html" class="nav-link">All Paddles</a>
                <a href="index.html" class="nav-link active">Categories</a>
                <a href="../guides/index.html" class="nav-link">Guides</a>
                <a href="../best-of/index.html" class="nav-link">Best Of</a>
                <a href="../../reviewers/index.html" class="nav-link">Reviewers</a>
                <a href="../compare.html" class="nav-link">Compare</a>
            </nav>
        </div>
    </header>

    <main>
        <div class="product-page-header">
            <div class="container">
                <h1>All Paddle Categories</h1>
                <p>Browse {len(category_defs)} categories of verified, measured pickleball paddles. Sort by type, foam, shape, or budget.</p>
            </div>
        </div>

        <section class="products-section">
            <div class="container">
                <div class="categories-grid">
                    {category_cards}
                </div>
            </div>
        </section>
    </main>

    <footer class="site-footer">
        <div class="container">
            <div class="footer-bottom">
                <p>&copy; 2026 Pickleball Reviewer. All rights reserved. | <a href="../../privacy.html">Privacy</a> | <a href="../../../affiliate-disclosure.html">Affiliate Disclosure</a></p>
            </div>
        </div>
    </footer>

    <!-- Google Analytics 4 — Replace G-6EL1LX9CG6 with your GA4 measurement ID -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-6EL1LX9CG6"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-6EL1LX9CG6');
    </script>
    <script src="../../js/app.js"></script>
</body>
</html>'''

    OUTPUT_DIR = 'output'
    os.makedirs(os.path.join(OUTPUT_DIR, 'pages', 'categories'), exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, 'pages', 'categories', 'index.html')
    with open(out_path, 'w') as f:
        f.write(html)
    print(f"   ✅ Categories index → pages/categories/index.html")


if __name__ == '__main__':
    generate_categories_index()
