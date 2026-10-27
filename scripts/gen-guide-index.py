#!/usr/bin/env python3
"""Guide index generator — called by build.py"""

def generate_guide_index():
    """Generate pages/guides/index.html listing all guides."""
    import os

    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Pickleball buying guides and foam core comparisons. Learn how to choose the right paddle for your game.">
    <title>Buying Guides — Pickleball Review Hub</title>
    <link rel="stylesheet" href="../../css/style.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
</head>
<body>
    <header class="site-header">
        <div class="container">
            <a href="../../index.html" class="logo">
                <span class="logo-icon">🏓</span>
                <span class="logo-text">Pickle<span class="highlight">Review</span>Hub</span>
            </a>
            <nav class="main-nav">
                <a href="../../index.html" class="nav-link">All Paddles</a>
                <a href="../../pages/categories/index.html" class="nav-link">Categories</a>
                <a href="index.html" class="nav-link active">Guides</a>
                <a href="../../pages/best-of/index.html" class="nav-link">Best Of</a>
                <a href="../../reviewers/index.html" class="nav-link">Reviewers</a>
                <a href="../../pages/compare.html" class="nav-link">Compare</a>
            </nav>
        </div>
    </header>

    <main>
        <div class="product-page-header">
            <div class="container">
                <h1>Buying Guides</h1>
                <p>Expert advice on choosing the right pickleball paddle — based on verified measured data, not marketing claims.</p>
            </div>
        </div>

        <section class="products-section">
            <div class="container">
                <div class="categories-grid">
                    <a href="how-to-choose.html" class="category-card">
                        <span class="category-icon">📋</span>
                        <h3>How to Choose a Pickleball Paddle</h3>
                        <p class="category-desc">Power vs control, foam types, shapes, and what to look for at every price point.</p>
                    </a>
                    <a href="mpp-vs-epp.html" class="category-card">
                        <span class="category-icon">🧊</span>
                        <h3>MPP vs EPP Foam</h3>
                        <p class="category-desc">Soft and springy or firm and connected. We break down the two foam core types.</p>
                    </a>
                    <a href="budget-under-120.html" class="category-card">
                        <span class="category-icon">💰</span>
                        <h3>Best Budget Paddles Under $120</h3>
                        <p class="category-desc">Premium performance without a premium price. Here are the best options.</p>
                    </a>
                </div>
            </div>
        </section>
    </main>

    <footer class="site-footer">
        <div class="container">
            <div class="footer-bottom">
                <p>&copy; 2026 Pickleball Review Hub. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <script src="../../js/app.js"></script>
</body>
</html>'''

    OUTPUT_DIR = 'output'
    os.makedirs(os.path.join(OUTPUT_DIR, 'pages', 'guides'), exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, 'pages', 'guides', 'index.html')
    with open(out_path, 'w') as f:
        f.write(html)
    print(f"   ✅ Guides index → pages/guides/index.html")


if __name__ == '__main__':
    generate_guide_index()
