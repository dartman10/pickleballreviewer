#!/usr/bin/env python3
"""Best Of index generator — called by build.py"""

def generate_best_of_index():
    """Generate pages/best-of/index.html listing all Best Of rankings."""
    import os

    # Define all Best Of rankings
    best_of_defs = [
        ('best-power-pickleball-paddles', '💥', 'Best Power',
         'Highest swing weight paddles — the heaviest faces deliver the most pop on contact'),
        ('best-budget-pickleball-paddles-under-100', '💰', 'Best Budget Under $100',
         'Premium performance without breaking the bank'),
        ('best-spin-pickleball-paddle', '🌀', 'Best Spin',
         'Maximum measured spin RPM for more bite and control'),
        ('best-value-pickleball-paddle', '📊', 'Best Value',
         'Best spin-to-price ratio — maximum performance per dollar'),
    ]

    best_of_cards = ''
    for slug, icon, name, desc in best_of_defs:
        best_of_cards += f'''<a href="{slug}.html" class="category-card">
            <span class="category-icon">{icon}</span>
            <h3>{name}</h3>
            <p class="category-desc">{desc}</p>
        </a>'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Curated Best Of rankings for pickleball paddles. Power, budget, spin, and value — sorted by verified measured data.">
    <title>Best Of Rankings — Pickleball Review Hub</title>
    <!-- Open Graph -->
    <meta property="og:title" content="Best Of Rankings — Pickleball Review Hub">
    <meta property="og:description" content="Curated Best Of rankings for pickleball paddles. Power, budget, spin, and value — sorted by verified measured data.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://picklereviewhub.com/pages/best-of/index.html">
    <meta property="og:image" content="https://picklereviewhub.com/og-image.png">
    <link rel="stylesheet" href="../../css/style.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
</head>
<body>
    <header class="site-header">
        <div class="container">
            <a href="../../index.html" class="logo">
                <span class="logo-icon">{chr(0x1F3D3)}</span>
                <span class="logo-text">Pickle<span class="highlight">Review</span>Hub</span>
            </a>
            <nav class="main-nav">
                <a href="../../index.html" class="nav-link">All Paddles</a>
                <a href="../../pages/categories/index.html" class="nav-link">Categories</a>
                <a href="../guides/index.html" class="nav-link">Guides</a>
                <a href="index.html" class="nav-link active">Best Of</a>
                <a href="../../reviewers/index.html" class="nav-link">Reviewers</a>
                <a href="../../pages/compare.html" class="nav-link">Compare</a>
            </nav>
        </div>
    </header>

    <main>
        <div class="product-page-header">
            <div class="container">
                <h1>🏆 Best Of Rankings</h1>
                <p>Curated rankings sorted by verified measured data — not marketing claims. Each ranking uses real lab measurements from trusted reviewers.</p>
            </div>
        </div>

        <section class="products-section">
            <div class="container">
                <div class="categories-grid">
                    {best_of_cards}
                </div>
            </div>
        </section>

        <section class="products-section" style="background: var(--bg-alt);">
            <div class="container">
                <h2>Compare Rankings</h2>
                <p style="color: var(--text-secondary); margin-bottom: 16px;">Compare top paddles across different rankings side by side.</p>
                <div style="display: flex; flex-wrap: wrap; gap: 12px; margin-top: 12px;">
                    <a href="best-power-pickleball-paddles.html" class="retailer-link">🔥 Best Power</a>
                    <a href="best-budget-pickleball-paddles-under-100.html" class="retailer-link">💰 Best Budget</a>
                    <a href="best-spin-pickleball-paddle.html" class="retailer-link">🌀 Best Spin</a>
                    <a href="best-value-pickleball-paddle.html" class="retailer-link">📊 Best Value</a>
                    <a href="../compare.html" class="retailer-link">🔍 Compare Paddles</a>
                </div>
            </div>
        </section>
    </main>

    <footer class="site-footer">
        <div class="container">
            <div class="footer-bottom">
                <p>&copy; 2026 Pickleball Review Hub. All rights reserved. | <a href="../../privacy.html">Privacy</a> | <a href="../../affiliate-disclosure.html">Affiliate Disclosure</a></p>
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
    <script src="../../js/app.js"></script>
</body>
</html>'''

    OUTPUT_DIR = 'output'
    os.makedirs(os.path.join(OUTPUT_DIR, 'pages', 'best-of'), exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, 'pages', 'best-of', 'index.html')
    with open(out_path, 'w') as f:
        f.write(html)
    print(f"   ✅ Best Of index → pages/best-of/index.html")


if __name__ == '__main__':
    generate_best_of_index()
