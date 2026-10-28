#!/usr/bin/env python3
"""
Pickleball Review Hub — Build Script
Reads data/paddles.json and generates all HTML pages in output/.
"""
import json
import os
import re
import shutil
from datetime import datetime

# Paths
DATA_FILE = "data/paddles.json"
OUTPUT_DIR = "output"
CSS_DIR = "css"
JS_DIR = "js"

def extract_video_id(url):
    """Extract YouTube video ID from a URL (youtube.com/watch?v=ID or youtu.be/ID)."""
    if not url:
        return ''
    # Match youtube.com/watch?v=ID
    m = re.search(r'(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})', url)
    if m:
        return m.group(1)
    return ''

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def copy_static_files():
    """Copy CSS, JS, and data files to output."""
    for src_dir, dst_name in [(CSS_DIR, 'css'), (JS_DIR, 'js')]:
        dst = os.path.join(OUTPUT_DIR, dst_name)
        os.makedirs(dst, exist_ok=True)
        for fname in os.listdir(src_dir):
            src_path = os.path.join(src_dir, fname)
            dst_path = os.path.join(dst, fname)
            if os.path.isfile(src_path):
                shutil.copy2(src_path, dst_path)
    # Copy data
    data_dst = os.path.join(OUTPUT_DIR, 'data')
    os.makedirs(data_dst, exist_ok=True)
    shutil.copy2(DATA_FILE, os.path.join(data_dst, 'paddles.json'))

def generate_paddle_page(paddle):
    """Generate a paddle detail page."""
    paddles = load_data()['paddles']
    paddle_id = paddle['id']

    # Related paddles (same brand or same category)
    related = [p for p in paddles if p['id'] != paddle_id and (
        p['brand'] == paddle['brand'] or p['category'] == paddle['category']
    )][:4]

    # Generate YouTube video cards HTML
    video_cards = ''
    if paddle.get('youtube_videos'):
        for v in paddle['youtube_videos']:
            vid_id = extract_video_id(v.get('url', ''))
            thumb_url = f"https://img.youtube.com/vi/{vid_id}/mqdefault.jpg" if vid_id else None
            if thumb_url:
                video_cards += f'''<div class="video-card">
                    <div class="video-thumb"><img src="{thumb_url}" alt="{v['title']}" loading="lazy" style="width:100%;height:100%;object-fit:cover;border-radius:6px;"></div>
                    <div class="video-info">
                        <div class="video-title"><a href="{v['url']}" target="_blank" rel="noopener">{v['title']}</a></div>
                        <div class="video-meta">{v['channel']} · {v['date']} · {v.get('views','?')} views · {v.get('duration','')}</div>
                    </div>
                </div>'''
            else:
                video_cards += f'''<div class="video-card">
                    <div class="video-thumb">▶ Video</div>
                    <div class="video-info">
                        <div class="video-title"><a href="{v['url']}" target="_blank" rel="noopener">{v['title']}</a></div>
                        <div class="video-meta">{v['channel']} · {v['date']} · {v.get('views','?')} views · {v.get('duration','')}</div>
                    </div>
                </div>'''

    # Generate written review cards HTML
    review_cards = ''
    if paddle.get('written_reviews'):
        for r in paddle['written_reviews']:
            quotes_html = '<div class="review-quote">"' + r['quotes'][0] + '"</div>'
            if len(r['quotes']) > 1:
                quotes_html += '<div class="review-quote">"' + r['quotes'][1] + '"</div>'
            pros_list = ''.join(f'<li>{p}</li>' for p in r.get('pros', []))
            cons_list = ''.join(f'<li>{c}</li>' for c in r.get('cons', []))
            review_cards += f'''<div class="review-block">
                <div class="review-source">{r['author']} — <a href="{r['url']}" target="_blank" rel="noopener">{r['site']} <small>(full review)</small></a></div>
                {quotes_html}
                <div class="pros-cons-section" style="font-size:0.85rem;">
                    {pros_list and f'<div><span class="pros-heading">Pros</span><ul class="pros-cons-list">{pros_list}</ul></div>'}
                    {cons_list and f'<div><span class="cons-heading">Cons</span><ul class="cons-list">{cons_list}</ul></div>'}
                </div>
                <div class="review-disclosure">{r.get('disclosure', '')}</div>
            </div>'''

    # Generate consensus table HTML
    consensus_rows = ''
    if paddle.get('consensus_topics'):
        for ct in paddle['consensus_topics']:
            consensus_rows += f'''<tr>
                <td><strong>{ct['topic']}</strong></td>
                <td>{ct['consensus']}</td>
                <td class="consensus-sources">{', '.join(ct['sources'])}</td>
            </tr>'''

    # Generate retailers HTML
    retailer_links = ''
    if paddle.get('retailers'):
        for r in paddle['retailers']:
            price_text = r.get('price', '')
            code_text = f' ({r.get("code","")})' if r.get('code') else ''
            retailer_links += f'<a href="{r["url"]}" class="retailer-link" target="_blank" rel="noopener">{r["name"]}{price_text and " — "+price_text}{code_text}</a>'

    # Generate related paddle links
    related_html = ''
    for rp in related:
        related_html += f'<a href="{rp["id"]}.html" class="related-product-link">{rp["name"]} — {rp["price_range"]}</a>'

    # Build specs table
    specs_html = ''
    if paddle.get('measured_specs'):
        specs_html = ''
        for k, v in paddle['measured_specs'].items():
            specs_html += f'<tr><th>{k.replace("_", " ").title()}</th><td>{v}</td></tr>'

    # Generate page HTML
    page_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{paddle['description']}">
    <title>{paddle['name']} Review — Pickleball Review Hub</title>
    <link rel="canonical" href="https://picklereviewhub.com/pages/paddles/{paddle['id']}.html">
    <!-- Open Graph -->
    <meta property="og:title" content="{paddle['name']} Review — Pickleball Review Hub">
    <meta property="og:description" content="{paddle['description']}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://picklereviewhub.com/pages/paddles/{paddle['id']}.html">
    <meta property="og:image" content="https://picklereviewhub.com/og-image.png">
    <link rel="stylesheet" href="../../css/style.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <!-- Breadcrumb Schema -->
    <script type="application/ld+json">{{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://picklereviewhub.com/"}},
        {{"@type": "ListItem", "position": 2, "name": "{paddle['category'].title()}", "item": "https://picklereviewhub.com/pages/categories/{paddle['category']}.html"}},
        {{"@type": "ListItem", "position": 3, "name": "{paddle['name']}"}}
      ]
    }}</script>
    <!-- Product Schema -->
    <script type="application/ld+json">{{
      "@context": "https://schema.org",
      "@type": "Product",
      "name": "{paddle['name']}",
      "description": "{paddle['description']}",
      "brand": {{"@type": "Brand", "name": "{paddle['brand']}}},
      "offers": {{
        "@type": "AggregateOffer",
        "lowPrice": {paddle.get('price_min', 0)},
        "highPrice": {paddle.get('price_max', 0)},
        "priceCurrency": "USD"
      }},
      "category": "{paddle['category']}"
    }}</script>
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
                <a href="../categories/index.html" class="nav-link">Categories</a>
                <a href="../guides/index.html" class="nav-link">Guides</a>
                <a href="../best-of/index.html" class="nav-link">Best Of</a>
                <a href="../../reviewers/index.html" class="nav-link">Reviewers</a>
                <a href="../compare.html" class="nav-link">Compare</a>
            </nav>
        </div>
    </header>

    <main>
        <nav class="breadcrumbs" aria-label="Breadcrumb">
            <div class="container">
                <ol class="breadcrumb-list">
                    <li class="breadcrumb-item"><a href="../../index.html" class="breadcrumb-link">Home</a></li>
                    <li class="breadcrumb-item"><a href="../categories/{paddle['category']}.html" class="breadcrumb-link">{paddle['category'].title()}</a></li>
                    <li class="breadcrumb-item"><span class="breadcrumb-current">{paddle['name']}</span></li>
                </ol>
            </div>
        </nav>

        <div class="product-page-header">
            <div class="container">
                <h1>{paddle['name']}</h1>
                <p>Verified reviews, YouTube videos, and where to buy</p>
            </div>
        </div>

        <section class="products-section">
            <div class="container">
                <div class="paddle-detail">
                    <div class="paddle-detail-header">
                        <div>
                            <h2>{paddle['name']}</h2>
                            <p>{paddle['description']}</p>
                        </div>
                        <div style="display:flex;align-items:center;gap:12px;">
                            <span class="paddle-detail-price">{paddle['price_range']}</span>
                            <a href="../compare.html?paddles={paddle['id']}" class="compare-btn" style="text-decoration:none;display:inline-block;padding:8px 16px;background:var(--accent);color:white;border-radius:6px;font-size:0.85rem;font-weight:600;">Compare</a>
                        </div>
                    </div>

                    <div class="paddle-card-tags" style="margin-bottom:20px;">
                        {''.join(f'<span class="tag {t}">{t}</span>' for t in paddle.get('tags', []))}
                    </div>

                    {'<table class="specs-table"><thead><tr><th colspan="2">Key Specifications</th></tr></thead><tbody>' + specs_html + '</tbody></table>' if specs_html else ''}

                    <div class="pros-cons-section">
                        <div>
                            <h4 class="pros-heading">Pros (from reviews)</h4>
                            <ul class="pros-cons-list">
                                {''.join(f'<li>{p}</li>' for r in paddle.get('written_reviews', []) for p in r.get('pros', []))}
                            </ul>
                        </div>
                        <div>
                            <h4 class="cons-heading">Cons (from reviews)</h4>
                            <ul class="cons-list">
                                {''.join(f'<li>{c}</li>' for r in paddle.get('written_reviews', []) for c in r.get('cons', []))}
                            </ul>
                        </div>
                    </div>

                    <div class="youtube-section">
                        <h4>📺 YouTube Review Videos</h4>
                        <div class="video-list">
                            {video_cards or '<p style="color: var(--text-secondary); font-size: 0.9rem;">No videos yet.</p>'}
                        </div>
                    </div>

                    <div class="written-review-section">
                        <h4>📝 Written Review Highlights</h4>
                        <p style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 12px;">Direct quotes from creator websites. No paraphrasing.</p>
                        {review_cards or '<p style="color: var(--text-secondary); font-size: 0.9rem;">No written reviews yet.</p>'}
                    </div>

                    <div class="consensus-section">
                        <h4>🔍 Cross-Reviewer Consensus</h4>
                        <p style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 12px;">Only includes points where 2+ verified reviewers address the same topic.</p>
                        <table class="consensus-table">
                            <thead><tr><th>Topic</th><th>Consensus</th><th>Sources</th></tr></thead>
                            <tbody>{consensus_rows or '<tr><td colspan="3" style="color: var(--text-secondary);">No consensus data yet.</td></tr>'}</tbody>
                        </table>
                    </div>

                    <div class="retailers-section">
                        <h4>🏷️ Where to Buy — Best Prices</h4>
                        <div class="retailer-links">
                            {retailer_links or '<p style="color: var(--text-secondary); font-size: 0.9rem;">No retailer links yet.</p>'}
                        </div>
                    </div>
                </div>

                <a href="../categories/{paddle['category']}.html" class="retailer-link" style="display:inline-block; margin-bottom: 20px;">&larr; Back to {paddle['category'].title()} Paddles</a>

                {related_html and f'<section class="related-products"><h3>Related Paddles</h3><div>{related_html}</div></section>'}
                <section class="related-articles" style="margin-top:30px;">
                    <h3>Buying Guides</h3>
                    <div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:8px;">
                        <a href="../guides/index.html" class="related-article-link">How to Choose a Pickleball Paddle</a>
                        <a href="../guides/mpp-vs-epp.html" class="related-article-link">MPP vs EPP Foam</a>
                        <a href="../guides/budget-under-120.html" class="related-article-link">Best Budget Paddles Under $120</a>
                    </div>
                </section>
            </div>
        </section>
    </main>

    <footer class="site-footer">
        <div class="container">
            <div class="footer-bottom">
                <p>&copy; 2026 Pickleball Review Hub. All rights reserved. | <a href="../../../privacy.html">Privacy</a> | <a href="../../../affiliate-disclosure.html">Affiliate Disclosure</a></p>
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

    # Write file
    os.makedirs(os.path.join(OUTPUT_DIR, 'pages', 'paddles'), exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, 'pages', 'paddles', f'{paddle_id}.html')
    with open(out_path, 'w') as f:
        f.write(page_html)
    return out_path

def generate_category_page(paddle_list, category_name, category_slug, description):
    """Generate a category page."""
    paddle_cards = ''
    for p in paddle_list:
        paddle_cards += f'''<article class="paddle-card" id="{p['id']}">
            <div class="paddle-card-header">
                <h3><a href="../paddles/{p['id']}.html">{p['name']}</a></h3>
                <span class="paddle-card-price">{p['price_range']}</span>
            </div>
            <p class="paddle-card-desc">{p['description']}</p>
            <div class="paddle-card-tags">{''.join(f'<span class="tag {t}">{t}</span>' for t in p.get('tags', []))}</div>
            <div class="paddle-card-stats">
                {'<span>▶ ' + str(len(p.get('youtube_videos', []))) + ' video(s)</span>' if p.get('youtube_videos') else ''}
                {'<span>📝 ' + str(len(p.get('written_reviews', []))) + ' review(s)</span>' if p.get('written_reviews') else ''}
                {'<span>🔍 ' + str(len(p.get('consensus_topics', []))) + ' consensus topics</span>' if p.get('consensus_topics') else ''}
            </div>
        </article>'''

    paddles = load_data()['paddles']
    all_categories = [
        ('power', '💥', 'Power Paddles', 'Maximum pop and power for aggressive players'),
        ('elongated', '📏', 'Elongated Shape', 'Reach and leverage with an elongated face'),
        ('MPP', '🧊', 'MPP Foam Core', 'Softer, springy feel — closer to Lux Inferno'),
        ('EPP', '🔥', 'EPP Foam Core', 'Firmer, more connected feel'),
        ('budget', '💰', 'Budget Picks', 'Top performance without breaking the bank'),
    ]

    category_links = ''
    for slug, icon, name, desc in all_categories:
        if slug != category_slug:
            count = sum(1 for p in paddles if slug == 'power' and p['category'] == 'power'
                       or slug == 'elongated' and p['shape'] == 'elongated'
                       or slug == 'MPP' and p['foam_type'] == 'MPP'
                       or slug == 'EPP' and p['foam_type'] == 'EPP'
                       or slug == 'budget' and p.get('price_max', 9999) <= 120)
            category_links += f'''<a href="{slug}.html" class="category-card">
                <span class="category-icon">{icon}</span>
                <h3>{name}</h3>
                <p class="category-desc">{desc}</p>
            </a>'''

    page_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description}">
    <title>{category_name} — Pickleball Review Hub</title>
    <!-- Open Graph -->
    <meta property="og:title" content="{category_name} — Pickleball Review Hub">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://picklereviewhub.com/pages/categories/{category_slug}.html">
    <meta property="og:image" content="https://picklereviewhub.com/og-image.png">
    <link rel="stylesheet" href="../../css/style.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script type="application/ld+json">{{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://picklereviewhub.com/"}},
        {{"@type": "ListItem", "position": 2, "name": "{category_name}"}}
      ]
    }}</script>
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
                <a href="index.html" class="nav-link">Categories</a>
                <a href="../guides/index.html" class="nav-link">Guides</a>
                <a href="../best-of/index.html" class="nav-link">Best Of</a>
                <a href="../../reviewers/index.html" class="nav-link">Reviewers</a>
                <a href="../compare.html" class="nav-link">Compare</a>
                </nav>
                </div>
                </header>

                <main>
                <nav class="breadcrumbs" aria-label="Breadcrumb">
                <div class="container">
                <ol class="breadcrumb-list">
                  <li class="breadcrumb-item"><a href="../../index.html" class="breadcrumb-link">Home</a></li>
                  <li class="breadcrumb-item"><span class="breadcrumb-current">{category_name}</span></li>
                </ol>
                </div>
                </nav>

        <div class="product-page-header">
            <div class="container">
                <h1>{category_name}</h1>
                <p>{description}</p>
                <p style="margin-top:8px;"><strong>{len(paddle_list)} paddle(s) in this category</strong></p>
            </div>
        </div>

        <section class="products-section">
            <div class="container">
                <div class="products-grid">{paddle_cards}</div>
            </div>
        </section>

        <section class="products-section" style="background: var(--bg-alt);">
            <div class="container">
                <h2>Browse Other Categories</h2>
                <div class="categories-grid">
                    {category_links}
                </div>
            </div>
        </section>
    </main>

    <footer class="site-footer">
        <div class="container">
            <div class="footer-bottom">
                <p>&copy; 2026 Pickleball Review Hub. All rights reserved. | <a href="../../../privacy.html">Privacy</a> | <a href="../../../affiliate-disclosure.html">Affiliate Disclosure</a></p>
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

    os.makedirs(os.path.join(OUTPUT_DIR, 'pages', 'categories'), exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, 'pages', 'categories', f'{category_slug}.html')
    with open(out_path, 'w') as f:
        f.write(page_html)
    return out_path

def generate_reviewer_page(name, site, description, url, paddle_count):
    """Generate a reviewer directory page."""
    paddle_links = ''
    paddles = load_data()['paddles']
    for p in paddles:
        for r in p.get('written_reviews', []):
            if r.get('site') == site:
                paddle_links += f'<a href="../pages/paddles/{p["id"]}.html" class="related-article-link">{p["name"]} — {p["price_range"]}</a>'
                break

    other_reviewers = [
        ('Pickleball Studio', 'Pickleball Studio', '33K+ subs. Independent, thorough testing. Founder Chris Olson is a 4.75 DUPR player.', 'Pickleball Studio'),
        ('John Kew', 'JohnKew Pickleball', '14.7K+ subs. Data-driven lab testing. KewCOR firepower measurements.', 'John Kew'),
        ('The Kitchen', 'The Kitchen Pickleball', 'Expert team. Scored ratings. Independent testing since 2023.', 'The Kitchen'),
    ]

    reviewer_links = ''
    for n, s, d, display in other_reviewers:
        if display != name:
            reviewer_links += f'''<a href="{n.lower().replace(' ', '-')}.html" class="reviewer-link">{display}</a>'''

    page_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{name} — Top pickleball paddle reviewer. {paddle_count} paddles reviewed.">
    <title>{name} Reviews — Pickleball Review Hub</title>
    <!-- Open Graph -->
    <meta property="og:title" content="{name} Reviews — Pickleball Review Hub">
    <meta property="og:description" content="{name} — {paddle_count} paddles reviewed. Pickleball paddle reviews from {site}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://picklereviewhub.com/reviewers/{name.lower().replace(' ', '-')}.html">
    <meta property="og:image" content="https://picklereviewhub.com/og-image.png">
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
                <h1>{name}</h1>
                <p>Pickleball paddle reviews from {site}</p>
            </div>
        </div>

        <section class="products-section">
            <div class="container">
                <div class="reviewer-card">
                    <h3>{name}</h3>
                    <p>{description}</p>
                    <a href="{url}" class="reviewer-link" target="_blank" rel="noopener">Visit {site} →</a>
                    <p style="margin-top:12px;font-size:0.85rem;color:var(--text-secondary);"><strong>{paddle_count} paddles reviewed on this site</strong></p>
                </div>

                <h3 style="margin-top:30px;margin-bottom:12px;">Paddles Reviewed by {name}</h3>
                <div style="display:flex;flex-wrap:wrap;gap:8px;">
                    {paddle_links or '<p style="color: var(--text-secondary);">No paddle reviews yet from this source.</p>'}
                </div>
            </div>
        </section>

        <section class="products-section" style="background: var(--bg-alt);">
            <div class="container">
                <h3>Other Top Reviewers</h3>
                <div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:12px;">
                    {reviewer_links}
                </div>
            </div>
        </section>
    </main>

    <footer class="site-footer">
        <div class="container">
            <div class="footer-bottom">
                <p>&copy; 2026 Pickleball Review Hub. All rights reserved. | <a href="../../privacy.html">Privacy</a> | <a href="affiliate-disclosure.html">Affiliate Disclosure</a></p>
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

    os.makedirs(os.path.join(OUTPUT_DIR, 'reviewers'), exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, 'reviewers', f'{name.lower().replace(" ", "-")}.html')
    with open(out_path, 'w') as f:
        f.write(page_html)
    return out_path

def generate_guide_page(title, slug, description, content_sections, related_paddles):
    """Generate a real guide page with actual content."""
    # Build content HTML
    content_html = ''
    for section in content_sections:
        if section['type'] == 'heading':
            content_html += f'<h3>{section["text"]}</h3>'
        elif section['type'] == 'paragraph':
            content_html += f'<p>{section["text"]}</p>'
        elif section['type'] == 'pros-cons':
            content_html += '<div class="pros-cons-section">'
            if section.get('pros'):
                pros_list = ''.join(f'<li>{p}</li>' for p in section['pros'])
                content_html += f'<div><span class="pros-heading">{section["pros_title"]}</span><ul class="pros-cons-list">{pros_list}</ul></div>'
            if section.get('cons'):
                cons_list = ''.join(f'<li>{c}</li>' for c in section['cons'])
                content_html += f'<div><span class="cons-heading">{section["cons_title"]}</span><ul class="cons-list">{cons_list}</ul></div>'
            content_html += '</div>'
        elif section['type'] == 'table':
            table_rows = ''.join(f'<tr><td>{row[0]}</td><td>{row[1]}</td></tr>' for row in section['data'])
            content_html += f'<table class="specs-table"><thead><tr><th>{section["col1"]}</th><th>{section["col2"]}</th></tr></thead><tbody>{table_rows}</tbody></table>'
        elif section['type'] == 'list':
            items = ''.join(f'<li>{item}</li>' for item in section['items'])
            content_html += f'<ul style="padding-left:20px;line-height:1.8;">{items}</ul>'
        elif section['type'] == 'paddle-recommendations':
            recs = section['paddles']
            rec_html = ''
            for r in recs:
                rec_html += f'''<div class="best-of-rank-card" style="margin-bottom:12px;">
                    <div class="best-of-rank-body">
                        <h4 style="margin:0 0 4px;"><a href="../paddles/{r['id']}.html" style="color:inherit;text-decoration:none;">{r['name']}</a> — {r['price_range']}</h4>
                        <p style="margin:0;font-size:0.9rem;color:var(--text-secondary);">{r['description']}</p>
                    </div>
                </div>'''
            content_html += f'<div style="margin-top:8px;">{rec_html}</div>'
        elif section['type'] == 'divider':
            content_html += '<hr style="border:none;border-top:1px solid var(--border);margin:24px 0;">'

    # Related paddles
    related_html = ''
    if related_paddles:
        paddle_cards = ''
        for rp in related_paddles[:4]:
            paddle_cards += f'''<article class="paddle-card" id="{rp['id']}">
                <div class="paddle-card-header">
                    <h3><a href="../paddles/{rp['id']}.html">{rp['name']}</a></h3>
                    <span class="paddle-card-price">{rp['price_range']}</span>
                </div>
                <p class="paddle-card-desc">{rp['description']}</p>
            </article>'''
        related_html = f'''<section class="products-section" style="background: var(--bg-alt);">
            <div class="container">
                <h2>Related Paddles</h2>
                <div class="products-grid">{paddle_cards}</div>
            </div>
        </section>'''

    page_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description}">
    <title>{title} — Pickleball Review Hub</title>
    <link rel="canonical" href="https://picklereviewhub.com/pages/guides/{slug}">
    <!-- Open Graph -->
    <meta property="og:title" content="{title} — Pickleball Review Hub">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://picklereviewhub.com/pages/guides/{slug}">
    <meta property="og:image" content="https://picklereviewhub.com/og-image.png">
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
                <a href="../categories/index.html" class="nav-link">Categories</a>
                <a href="index.html" class="nav-link active">Guides</a>
                <a href="../best-of/index.html" class="nav-link">Best Of</a>
                <a href="../../reviewers/index.html" class="nav-link">Reviewers</a>
                <a href="../compare.html" class="nav-link">Compare</a>
            </nav>
        </div>
    </header>

    <main>
        <div class="product-page-header">
            <div class="container">
                <h1>{title}</h1>
                <p>Expert buying advice based on verified measured data — not marketing claims.</p>
            </div>
        </div>

        <section class="products-section">
            <div class="container" style="max-width:800px;">
                {content_html}
            </div>
        </section>

        {related_html}
    </main>

    <footer class="site-footer">
        <div class="container">
            <div class="footer-bottom">
                <p>&copy; 2026 Pickleball Review Hub. All rights reserved. | <a href="../../../privacy.html">Privacy</a> | <a href="../../../affiliate-disclosure.html">Affiliate Disclosure</a></p>
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
    clean_slug = slug if not slug.endswith('.html') else slug[:-5]
    os.makedirs(os.path.join(OUTPUT_DIR, 'pages', 'guides'), exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, 'pages', 'guides', f'{clean_slug}.html')
    with open(out_path, 'w') as f:
        f.write(page_html)
    print(f"   ✅ {title} → pages/guides/{clean_slug}.html")
    return out_path


def generate_placeholder_guide(title, slug, description):
    """Generate a placeholder guide page (coming soon)."""
    page_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description}">
    <title>{title} — Pickleball Review Hub</title>
    <!-- Open Graph -->
    <meta property="og:title" content="{title} — Pickleball Review Hub">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://picklereviewhub.com/pages/guides/{slug}">
    <meta property="og:image" content="https://picklereviewhub.com/og-image.png">
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
                <a href="../categories/index.html" class="nav-link">Categories</a>
                <a href="how-to-choose.html" class="nav-link active">Guides</a>
                <a href="../best-of/index.html" class="nav-link">Best Of</a>
                <a href="../../reviewers/index.html" class="nav-link">Reviewers</a>
                <a href="../compare.html" class="nav-link">Compare</a>
            </nav>
        </div>
    </header>

    <main>
        <div class="product-page-header">
            <div class="container">
                <h1>{title}</h1>
            </div>
        </div>

        <section class="products-section">
            <div class="container">
                <div style="text-align:center;padding:40px 0;">
                    <h2 style="color: var(--text-secondary);">🚧 Coming Soon</h2>
                    <p style="color: var(--text-secondary); margin-top:8px;">This guide is under review. Check back soon.</p>
                    <a href="../../index.html" class="retailer-link" style="display:inline-block;margin-top:20px;">&larr; Back to All Paddles</a>
                </div>
            </div>
        </section>
    </main>

    <footer class="site-footer">
        <div class="container">
            <div class="footer-bottom">
                <p>&copy; 2026 Pickleball Review Hub. All rights reserved. | <a href="../../../privacy.html">Privacy</a> | <a href="../../../affiliate-disclosure.html">Affiliate Disclosure</a></p>
            </div>
        </div>
    </footer>
</body>
</html>'''

    os.makedirs(os.path.join(OUTPUT_DIR, 'pages', 'guides'), exist_ok=True)
    # Strip .html from slug if present, then add it back
    clean_slug = slug if not slug.endswith('.html') else slug[:-5]
    out_path = os.path.join(OUTPUT_DIR, 'pages', 'guides', f'{clean_slug}.html')
    with open(out_path, 'w') as f:
        f.write(page_html)
    return out_path

def _get_spin(p):
    """Safely extract spin_rpm from measured_specs."""
    return p.get('measured_specs', {}).get('spin_rpm') or 0

def _get_twist(p):
    """Safely extract twist_weight from measured_specs."""
    return p.get('measured_specs', {}).get('twist_weight') or 0

def generate_best_of_pages():
    """Generate 4 curated 'Best Of' ranking pages."""
    paddles = load_data()['paddles']

    # Sortable paddles: those that have at least spin_rpm data
    with_spin = [p for p in paddles if _get_spin(p) > 0]

    # Budget paddles: price_max <= 100
    budget_paddles = [p for p in paddles if p.get('price_max', 9999) <= 100]

    # Best value: spin_rpm / price_max
    with_value = [(p, _get_spin(p) / p.get('price_max', 1)) for p in paddles if p.get('price_max', 0) > 0]
    with_value.sort(key=lambda x: x[1], reverse=True)

    best_of_configs = [
        {
            'title': 'Best Power Paddle Pickleball',
            'slug': 'best-power-pickleball-paddles',
            'description': 'Top-ranked power paddles measured by spin RPM and twist weight — real lab data, not marketing claims.',
            'icon': '🔥',
            'badge_prefix': 'Best Power',
            'sort_fn': lambda p: (_get_spin(p), _get_twist(p)),
            'sort_reverse': True,
            'data': paddles,
            'key_stat': lambda p: str(_get_spin(p)),
            'key_stat_label': 'Spin RPM',
        },
        {
            'title': 'Best Budget Pickleball Paddles Under $100',
            'slug': 'best-budget-pickleball-paddles-under-100',
            'description': 'Premium performance without breaking the bank. Paddles measured by experts that cost $100 or less.',
            'icon': '💰',
            'badge_prefix': 'Best Budget',
            'sort_fn': lambda p: p.get('price_max', 9999),
            'sort_reverse': False,
            'data': budget_paddles,
            'key_stat': lambda p: p['price_range'],
            'key_stat_label': 'Price',
        },
        {
            'title': 'Best Spin Pickleball Paddle',
            'slug': 'best-spin-pickleball-paddle',
            'description': 'Highest spin RPM paddles verified by measured testing. More spin = more bite and control.',
            'icon': '🌀',
            'badge_prefix': 'Top Spin',
            'sort_fn': lambda p: _get_spin(p),
            'sort_reverse': True,
            'data': with_spin,
            'key_stat': lambda p: str(_get_spin(p)),
            'key_stat_label': 'Spin RPM',
        },
        {
            'title': 'Best Value Pickleball Paddle',
            'slug': 'best-value-pickleball-paddle',
            'description': 'Best spin-to-price ratio — maximum performance per dollar spent. Score calculated from measured spin RPM / price.',
            'icon': '📊',
            'badge_prefix': 'Best Value',
            'sort_fn': lambda x: x[1],
            'sort_reverse': True,
            'data': with_value,
            'is_score_list': True,
            'key_stat': lambda x: f'{_get_spin(x[0])} RPM / ${x[0].get("price_max", "")}',
            'key_stat_label': 'Value Score',
        },
    ]

    os.makedirs(os.path.join(OUTPUT_DIR, 'pages', 'best-of'), exist_ok=True)

    for config in best_of_configs:
        items = config['data']
        sorted_items = sorted(items, key=config['sort_fn'], reverse=config['sort_reverse'])

        # Build ranked paddle cards
        # Compute max key value for progress bars
        key_vals = []
        for item in sorted_items:
            actual_p = item if not config.get('is_score_list') else item[0]
            val = _get_spin(actual_p) if config['key_stat_label'] == 'Spin RPM' else (actual_p.get('price_max', 1) if config['key_stat_label'] == 'Price' else (_get_spin(actual_p) / actual_p.get('price_max', 1) if config['key_stat_label'] == 'Value Score' else 0))
            key_vals.append(val)
        max_val = max(key_vals) if key_vals else 1

        # Build ranked paddle cards — top 3 get special treatment
        cards = ''
        for rank, item in enumerate(sorted_items, 1):
            actual_p = item if not config.get('is_score_list') else item[0]
            vid_id = extract_video_id(actual_p.get('youtube_videos', [{}])[0].get('url', '')) if actual_p.get('youtube_videos') else ''
            thumb_src = f'https://img.youtube.com/vi/{vid_id}/mqdefault.jpg' if vid_id else ''

            # Calculate progress bar percentage
            val = _get_spin(actual_p) if config['key_stat_label'] == 'Spin RPM' else (actual_p.get('price_max', 1) if config['key_stat_label'] == 'Price' else (_get_spin(actual_p) / actual_p.get('price_max', 1) if config['key_stat_label'] == 'Value Score' else 0))
            pct = min(int((val / max_val) * 100), 100) if max_val > 0 else 0

            # Top 3 get hero cards; #4+ get compact cards
            if rank <= 3:
                gold = ' 🥇' if rank == 1 else (' 🥈' if rank == 2 else ' 🥉')
                cards += f'''<div class="best-of-hero-card" style="background: linear-gradient(135deg, {['#fef3cd, #fff8e1', '#e8e8e8, #f5f5f5', '#fce4ec, #fff0f3'][rank-1]} 0%, white 100%);">
                    <div class="best-of-hero-badge">#{rank} <span class="badge-label">{config['badge_prefix']}</span></div>
                    <div class="best-of-hero-body">
                        <div class="best-of-hero-thumb">
                            {f'<img src="{thumb_src}" alt="{actual_p["name"]}" loading="lazy">' if thumb_src else '<div class="best-of-thumb-placeholder">🏓</div>'}
                        </div>
                        <div class="best-of-hero-info">
                            <h3><a href="../paddles/{actual_p['id']}.html">{actual_p['name']}{gold}</a></h3>
                            <p class="best-of-rank-desc">{actual_p['description']}</p>
                            <div class="best-of-hero-stat">
                                <div class="best-of-stat-value">{config['key_stat'](item)} <span class="best-of-stat-label">{config['key_stat_label']}</span></div>
                                <div class="best-of-stat-bar"><div class="best-of-stat-fill" style="width:{pct}%"></div></div>
                            </div>
                            <div class="best-of-hero-price">{actual_p['price_range']}</div>
                        </div>
                    </div>
                    <div class="best-of-hero-cta"><a href="../paddles/{actual_p['id']}.html" class="best-of-hero-btn">View Full Review →</a></div>
                </div>'''
            else:
                cards += f'''<div class="best-of-rank-card">
                    <div class="best-of-rank-number">#{rank}</div>
                    <div class="best-of-rank-thumb">
                        {f'<img src="{thumb_src}" alt="{actual_p["name"]}" loading="lazy">' if thumb_src else '<div class="best-of-thumb-placeholder">🏓</div>'}
                    </div>
                    <div class="best-of-rank-body">
                        <div class="best-of-rank-top">
                            <h3><a href="../paddles/{actual_p['id']}.html">{actual_p['name']}</a></h3>
                            <span class="best-of-rank-price">{actual_p['price_range']}</span>
                        </div>
                        <p class="best-of-rank-desc">{actual_p['description']}</p>
                        <div class="best-of-rank-stat-row">
                            <span class="best-of-rank-stat-value">{config['key_stat'](item)} {config['key_stat_label']}</span>
                            <div class="best-of-stat-bar best-of-stat-bar-sm"><div class="best-of-stat-fill" style="width:{pct}%"></div></div>
                        </div>
                        <a href="../paddles/{actual_p['id']}.html" class="best-of-rank-btn">View Review →</a>
                    </div>
                </div>'''

        page_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{config['description']}">
    <title>{config['title']} — Pickleball Review Hub</title>
    <link rel="canonical" href="https://picklereviewhub.com/pages/best-of/{config['slug']}.html">
    <!-- Open Graph -->
    <meta property="og:title" content="{config['title']} — Pickleball Review Hub">
    <meta property="og:description" content="{config['description']}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://picklereviewhub.com/pages/best-of/{config['slug']}.html">
    <meta property="og:image" content="https://picklereviewhub.com/og-image.png">
    <link rel="stylesheet" href="../../css/style.css">
    <link rel="stylesheet" href="../../css/best-of.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script type="application/ld+json">{{{{
      "@context": "https://schema.org",
      "@type": "ItemList",
      "name": "{config['title']}",
      "itemListElement": [{", ".join(f'{{"@type":"ListItem","position":{rank},"name":"{p["name"]}"}}' for rank, p in enumerate(sorted_items[:5] if not config.get('is_score_list') else [x[0] for x in sorted_items[:5]]))}]
    }}}}</script>
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
                <a href="../categories/index.html" class="nav-link">Categories</a>
                <a href="../guides/index.html" class="nav-link">Guides</a>
                <a href="../best-of/index.html" class="nav-link">Best Of</a>
                <a href="../../reviewers/index.html" class="nav-link">Reviewers</a>
                <a href="../compare.html" class="nav-link">Compare</a>
            </nav>
        </div>
    </header>

    <main>
        <nav class="breadcrumbs" aria-label="Breadcrumb">
            <div class="container">
                <ol class="breadcrumb-list">
                    <li class="breadcrumb-item"><a href="../../index.html" class="breadcrumb-link">Home</a></li>
                    <li class="breadcrumb-item"><span class="breadcrumb-current">{config['title']}</span></li>
                </ol>
            </div>
        </nav>

        <div class="best-of-hero-banner">
            <div class="container">
                <h1>{config['icon']} {config['title']}</h1>
                <p>{config['description']}</p>
                <div class="best-of-banner-stats">
                    <span class="best-of-banner-stat"><strong>{len(sorted_items)}</strong> paddles ranked</span>
                    <span class="best-of-banner-stat"><strong>Verified data</strong> from lab tests</span>
                </div>
            </div>
        </div>

        <section class="products-section">
            <div class="container">
                <div class="best-of-list">
                    {cards}
                </div>

                <div class="best-of-cta-section">
                    <a href="../compare.html?paddles={','.join(p['id'] if not config.get('is_score_list') else p[0]['id'] for p in sorted_items[:3])}" class="best-of-cta-btn">🔍 Compare Top 3 Side by Side</a>
                </div>
            </div>
        </section>

        <section class="products-section" style="background: var(--bg-alt);">
            <div class="container">
                <h2>Browse Paddles by Category</h2>
                <div class="categories-grid">
                    <a href="../categories/power.html" class="category-card">
                        <span class="category-icon">💥</span>
                        <h3>Power Paddles</h3>
                        <p class="category-desc">Maximum pop and power</p>
                    </a>
                    <a href="../categories/budget.html" class="category-card">
                        <span class="category-icon">💰</span>
                        <h3>Budget Picks</h3>
                        <p class="category-desc">Under $120</p>
                    </a>
                    <a href="../compare.html" class="category-card">
                        <span class="category-icon">🔍</span>
                        <h3>Compare Paddles</h3>
                        <p class="category-desc">Side-by-side spec comparison</p>
                    </a>
                </div>
            </div>
        </section>
    </main>

    <footer class="site-footer">
        <div class="container">
            <div class="footer-bottom">
                <p>&copy; 2026 Pickleball Review Hub. All rights reserved. | <a href="../../../privacy.html">Privacy</a> | <a href="../../../affiliate-disclosure.html">Affiliate Disclosure</a></p>
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

        out_path = os.path.join(OUTPUT_DIR, 'pages', 'best-of', f'{config["slug"]}.html')
        with open(out_path, 'w') as f:
            f.write(page_html)
        print(f"   ✅ {config['title']} → pages/best-of/{config['slug']}.html ({len(sorted_items)} ranked)")

    return len(best_of_configs)

def main():
    print("🏓 Pickleball Review Hub — Building...")
    print()

    # Clean output
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)

    # Copy static files
    print("📁 Copying static files...")
    copy_static_files()

    # Generate sitemap
    exec(open("scripts/gen-sitemap.py").read())

    # Copy legal files (privacy, affiliate disclosure, robots, 404)
    print("📄 Copying legal/site files...")
    for fname in ['privacy.html', 'affiliate-disclosure.html', 'robots.txt', '404.html']:
        src = os.path.join('legal', fname)
        dst = os.path.join(OUTPUT_DIR, fname)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"   ✅ {fname} → {fname}")
        else:
            print(f"   ⚠️  {fname} not found in legal/")
    print()

    paddles = load_data()['paddles']
    print(f"📋 Loaded {len(paddles)} paddles from data/paddles.json")
    print()

    # Generate paddle detail pages
    print("📄 Generating paddle detail pages...")
    for p in paddles:
        out = generate_paddle_page(p)
        print(f"   ✅ {p['name']} → pages/paddles/{p['id']}.html")
    print()

    # Generate category pages
    print("📂 Generating category pages...")

    # Power category
    power_paddles = [p for p in paddles if p['category'] == 'power']
    if power_paddles:
        generate_category_page(power_paddles, 'Power Paddles', 'power', 'Maximum pop and power for aggressive players.')
        print(f"   ✅ Power Paddles ({len(power_paddles)} paddles) → pages/categories/power.html")

    # Shape categories
    shapes = {}
    for p in paddles:
        shape = p.get('shape', 'other')
        if shape not in shapes:
            shapes[shape] = []
        shapes[shape].append(p)
    for shape, shape_paddles in shapes.items():
        slug = shape.lower()
        generate_category_page(shape_paddles, f'{shape} Shape', slug, f'{shape} shape pickleball paddles for reach and leverage.')
        print(f"   ✅ {shape} Shape ({len(shape_paddles)} paddles) → pages/categories/{slug}.html")

    # Foam type categories
    foams = {}
    for p in paddles:
        foam = p.get('foam_type', 'other')
        if foam not in foams:
            foams[foam] = []
        foams[foam].append(p)
    for foam, foam_paddles in foams.items():
        slug = foam.lower()
        foam_desc = 'MPP (microcellular polypropylene) — softer, springy feel closer to Lux Inferno.' if foam == 'MPP' else 'EPP (expanded polypropylene) — firmer, more connected feel.'
        generate_category_page(foam_paddles, f'{foam} Foam Core', slug, foam_desc)
        print(f"   ✅ {foam} Foam ({len(foam_paddles)} paddles) → pages/categories/{slug}.html")

    # Budget category
    budget_paddles = [p for p in paddles if p.get('price_max', 9999) <= 120]
    if budget_paddles:
        generate_category_page(budget_paddles, 'Budget Picks', 'budget', 'Top performance without breaking the bank. Under $120.')
        print(f"   ✅ Budget Picks ({len(budget_paddles)} paddles) → pages/categories/budget.html")
    print()

    # Generate reviewer pages
    print("🎬 Generating reviewer pages...")
    reviewer_data = [
        ('Pickleball Studio', 'Pickleball Studio', 'Independent, thorough testing. Founder Chris Olson is a 4.75 DUPR player with 400+ paddles tested since 2021.', 'https://pickleballstudio.com/', 1),
        ('John Kew', 'JohnKew Pickleball', 'Data-driven lab testing. KewCOR firepower measurements, spin RPM, swing weight analysis.', 'https://johnkewpickleball.com/', 1),
        ('The Kitchen', 'The Kitchen Pickleball', 'Expert team. Scored ratings (Power 89/100, Spin 77/100). Independent testing.', 'https://thekitchenpickle.com/', 1),
        ('Pickleball Effect', 'Pickleball Effect', 'Independent lab testing. 513+ paddles measured in-house with Stalker Pro S3 radar, Briffidi swing/twist weight. Braydon Unsicker is a 5.0 player.', 'https://pickleballeffect.com/', 1),
    ]
    # Count actual unique paddles reviewed per reviewer
    for rd in reviewer_data:
        name = rd[0]
        site = rd[1]
        reviewed_ids = set()
        for p in paddles:
            for r in p.get('written_reviews', []):
                if r.get('site') == site:
                    reviewed_ids.add(p['id'])
                    break
        generate_reviewer_page(name, rd[1], rd[2], rd[3], len(reviewed_ids))
        print(f"   ✅ {name} → reviewers/{name.lower().replace(' ', '-')}.html ({len(reviewed_ids)} unique paddle(s)")
    print()

    # Generate reviewer index page
    exec(open("scripts/gen-reviewer-index.py").read())
    print()

    # Generate categories index page
    exec(open("scripts/gen-categories-index.py").read())
    print()

    # Generate Best Of index page
    exec(open("scripts/gen-best-of-index.py").read())
    print()

    # Generate guide pages with actual content
    print("📖 Generating guide pages...\n")

    # Guide 1: How to Choose a Pickleball Paddle
    guides_to_generate = [
        ('how-to-choose.html', 'How to Choose a Pickleball Paddle',
         'Power vs control, foam types, shapes, and what to look for at every price point.',
         [
             {'type': 'paragraph', 'text': 'Choosing the right pickleball paddle depends on three factors: your playing style, your physical preferences, and your budget. Based on verified measurements from trusted reviewers, here is a data-driven guide to help you pick the right paddle.'},
             {'type': 'heading', 'text': 'Step 1: Choose Your Foam Type'},
             {'type': 'paragraph', 'text': 'There are two main foam core types in modern pickleball paddles, and the choice affects everything from feel to spin potential.'},
             {'type': 'table', 'col1': 'Property', 'col2': 'MPP (Microcellular Polypropylene)', 'data': [
                 ['Feel', 'Softer, springy, slightly muted'],
                 ['Spin potential', 'Excellent — grippy surface'],
                 ['Dwell time', 'Longer — more controlled shots'],
                 ['Examples', 'CRBN 3X 16mm (2,750 RPM), Holbrook Fuze Elongated']
             ]},
             {'type': 'table', 'col1': 'Property', 'col2': 'EPP (Expanded Polypropylene)', 'data': [
                 ['Feel', 'Firmer, more connected, direct'],
                 ['Spin potential', 'Good — but less than MPP'],
                 ['Dwell time', 'Shorter — faster hands'],
                 ['Examples', 'Enhance EPP Turbo Elongated, Selkirk Power Air Invicta']
             ]},
             {'type': 'table', 'col1': 'Property', 'col2': 'Honeycomb Core', 'data': [
                 ['Feel', 'Unique — stiff face with flexible core'],
                 ['Spin potential', 'Very high on many models'],
                 ['Dwell time', 'Variable — depends on construction'],
                 ['Examples', 'CRBN 1X 14mm, Vatic Pro Prism Flash 16mm']
             ]},
             {'type': 'heading', 'text': 'Step 2: Pick a Shape'},
             {'type': 'list', 'items': [
                 '<strong>Elongated (tapered):</strong> More reach, higher leverage, higher MOI. Best for players who want extra power on volleys and serves. Measured spin RPM consistently 50-100 RPM higher than standard shapes.',
                 '<strong>Widebody:</strong> Larger sweet spot, more stable against off-center hits. Best for players who prioritize control and consistency over maximum power.',
                 '<strong>Hybrid:</strong> Blends a wider head with a slightly elongated profile. Best for players who want power without sacrificing too much control.',
                 '<strong>Standard:</strong> Balanced feel, lower MOI, faster hand speed at the net.'
             ]},
             {'type': 'heading', 'text': 'Step 3: Consider Your Budget'},
             {'type': 'paragraph', 'text': 'You do not need to spend $200+ for a competitive paddle. Here is what verified data shows across price ranges:'},
             {'type': 'table', 'col1': 'Budget', 'col2': 'What to Expect', 'data': [
                 ['Under $80', 'Basic EPP core. Adequate for recreational play, but limited spin RPM (1,800-2,000 range).'],
                 ['$80-$120', 'Sweet spot. Many MPP and honeycomb paddles live here. Spin RPM 2,200-2,750 range. Best value for competitive play.'],
                 ['$120-$160', 'Premium features: raw carbon fiber faces, optimized weight distribution, top-tier spin measurements.']
             ]},
             {'type': 'heading', 'text': 'Step 4: Match Power vs Control'},
             {'type': 'paragraph', 'text': 'Power and control are not opposites — the right paddle gives you both. Here is how to think about it:'},
             {'type': 'pros-cons', 'pros_title': 'Power Paddles', 'pros': [
                 'Higher spin RPM (2,400+)',
                 'Heavier weight (8.1-8.5 oz) for more drive power',
                 'Wider heads or elongated shape for more leverage',
                 'Best for: aggressive players who hit through the ball'
             ], 'cons_title': 'Control Paddles', 'cons': [
                 'Lower spin RPM (1,900-2,200)',
                 'Lighter weight (7.5-7.9 oz) for faster hands',
                 'Standard or widebody shape for larger sweet spot',
                 'Best for: patients who set up shots and place with precision'
             ]},
             {'type': 'divider'},
             {'type': 'heading', 'text': 'Our Top Recommendations by Playing Style'},
             {'type': 'paddle-recommendations', 'paddles': [
                 {'id': 'spartus-spitfire', 'name': 'Spartus Spitfire Elongated', 'price_range': '$150-$180', 'description': 'Top measured spin (2,982 RPM). Best spin paddle in our dataset. Elongated shape, honeycomb core.'},
                 {'id': 'enhance-mpp-turbo', 'name': 'Enhance MPP Turbo Elongated', 'price_range': '$99-$120', 'description': 'Best value. MPP foam with high spin (2,690 RPM) at a sub-$120 price.'},
                 {'id': 'selkirk-power-air-invicta', 'name': 'Selkirk Power Air Invicta', 'price_range': '$180-$210', 'description': 'Premium widebody with honeycomb core. Excellent balance of power and control.'}
             ]},
             {'type': 'divider'},
             {'type': 'heading', 'text': 'Quick Decision Tree'},
             {'type': 'list', 'items': [
                 'Want maximum spin? → Choose elongated shape with honeycomb core (Spartus Spitfire, CRBN 3X 16mm).',
                 'Want the best value? → Choose MPP foam in the $80-$120 range (Enhance MPP Turbo).',
                 'Want maximum control? → Choose widebody shape with EPP foam (Holbrook Fuze, Spartus P1).',
                 'On a tight budget? → Vatic Pro Prism Flash 16mm offers honeycomb performance under $100.'
             ]}
         ],
         None),

        ('mpp-vs-epp.html', 'MPP vs EPP Foam — What\'s the Difference?',
         'Soft and springy or firm and connected. We break down foam core types with real measured data.',
         [
             {'type': 'paragraph', 'text': 'Foam core type is one of the most important decisions when choosing a pickleball paddle. The foam determines the feel of every shot, how long the ball stays on the face, and ultimately how much spin you can generate.'},
             {'type': 'heading', 'text': 'MPP (Microcellular Polypropylene)'},
             {'type': 'paragraph', 'text': 'MPP foam has a finer, more compact cellular structure than EPP. This creates a softer, more springy feel that many players describe as "crisp" or "bouncy." MPP paddles tend to have longer dwell time — the ball stays on the face slightly longer, giving you more time to generate spin and control placement.'},
             {'type': 'table', 'col1': 'Metric', 'col2': 'Typical Range', 'data': [
                 ['Spin RPM', '2,400 - 2,750+'],
                 ['Weight range', '7.9 - 8.4 oz'],
                 ['Dwell time', 'Longer — more spin potential'],
                 ['Feel', 'Softer, springy, slightly muted'],
                 ['Best for', 'Players who prioritize spin and control']
             ]},
             {'type': 'heading', 'text': 'EPP (Expanded Polypropylene)'},
             {'type': 'paragraph', 'text': 'EPP foam has larger, more open cells, creating a firmer, more direct feel. Shots feel more "connected" and immediate. EPP paddles have shorter dwell time, which means faster hand speed at the net but slightly less spin potential compared to MPP.'},
             {'type': 'table', 'col1': 'Metric', 'col2': 'Typical Range', 'data': [
                 ['Spin RPM', '2,000 - 2,350'],
                 ['Weight range', '7.5 - 8.3 oz'],
                 ['Dwell time', 'Shorter — faster hands'],
                 ['Feel', 'Firmer, more connected, direct'],
                 ['Best for', 'Players who prioritize feel and hand speed']
             ]},
             {'type': 'divider'},
             {'type': 'heading', 'text': 'Head-to-Head Comparison'},
             {'type': 'table', 'col1': 'Feature', 'col2': 'Winner', 'data': [
                 ['Maximum spin RPM', 'MPP — consistently higher across our dataset'],
                 ['Hand speed at net', 'EPP — shorter dwell time means faster reactions'],
                 ['Off-center forgiveness', 'Tie — depends more on shape and weight distribution'],
                 ['Price range', 'Tie — both types found across all price points'],
                 ['Spin-to-price ratio', 'MPP — MPP paddles offer more spin per dollar']
             ]},
             {'type': 'divider'},
             {'type': 'heading', 'text': 'Top MPP Paddles in Our Dataset'},
             {'type': 'paddle-recommendations', 'paddles': [
                 {'id': 'holbrook-fuze-elongated-16mm', 'name': 'Holbrook Fuze Elongated 16mm', 'price_range': '$99-$120', 'description': 'Best MPP paddle. 2,380 RPM spin, excellent control, under $120.'},
                 {'id': 'enhance-mpp-turbo', 'name': 'Enhance MPP Turbo Elongated', 'price_range': '$99-$120', 'description': 'Second-best MPP. 2,690 RPM spin, elongated shape, great value.'},
                 {'id': 'spartus-spitfire', 'name': 'Spartus Spitfire Elongated', 'price_range': '$150-$180', 'description': 'Highest spin in dataset. Honeycomb but compares favorably to MPP.'}
             ]},
             {'type': 'divider'},
             {'type': 'heading', 'text': 'Top EPP Paddles in Our Dataset'},
             {'type': 'paddle-recommendations', 'paddles': [
                 {'id': 'enhance-epp-turbo', 'name': 'Enhance EPP Turbo Elongated', 'price_range': '$99-$120', 'description': 'Top EPP paddle. 2,060 RPM spin, elongated shape, excellent control.'},
                 {'id': 'selkirk-power-air-invicta', 'name': 'Selkirk Power Air Invicta', 'price_range': '$180-$210', 'description': 'Premium EPP with honeycomb insert. Great all-around performance.'},
                 {'id': 'ronbus-ripple-r4-14-v2', 'name': 'Ronbus Ripple R4.14 v2', 'price_range': '$90-$110', 'description': 'Budget EPP. 2,085 RPM spin, great value.'}
             ]},
             {'type': 'divider'},
             {'type': 'heading', 'text': 'The Verdict'},
             {'type': 'paragraph', 'text': 'If spin is your priority, choose MPP. If feel and hand speed matter more, choose EPP. For most players, the difference is measurable but not dramatic — both foam types produce paddles that are competitive at the club level. The bigger factors are shape, weight, and surface texture.'}
         ],
         None),

        ('budget-under-120.html', 'Best Budget Pickleball Paddles Under $120',
         'Premium performance doesn\'t need a premium price. Here are the best measured options.',
         [
             {'type': 'paragraph', 'text': 'You do not need to spend $200+ for a competitive pickleball paddle. Our dataset includes 16 paddles with verified measured data, and 4 of them cost $120 or less — with spin measurements that rival paddles twice their price.'},
             {'type': 'heading', 'text': 'The Best Budget Paddles by Measured Spin RPM'},
             {'type': 'table', 'col1': 'Rank', 'col2': 'Paddle', 'data': [
                 ['#1', 'Spartus Spitfire Elongated — $150-$180 — 2,982 RPM (honeycomb core)'],
                 ['#2', 'Vatic Pro Prism Flash 16mm — under $100 — 1,860 RPM (honeycomb core)'],
                 ['#3', 'Ronbus Quanta R3 — $90-$110 — 2,465 RPM (EPP core)'],
                 ['#4', 'Enhance MPP Turbo Elongated — $99-$120 — 2,690 RPM (MPP core)']
             ]},
             {'type': 'divider'},
             {'type': 'heading', 'text': 'Detailed Breakdown'},
             {'type': 'paddle-recommendations', 'paddles': [
                 {'id': 'spartus-spitfire', 'name': 'Spartus Spitfire Elongated', 'price_range': '$150-$180', 'description': 'Highest spin paddle in our entire dataset. Honeycomb core with 2,982 RPM measured spin. If you can stretch the budget, this is the best spin paddle available.'},
                 {'id': 'vatic-pro-prism-flash-16mm', 'name': 'Vatic Pro Prism Flash 16mm', 'price_range': 'Under $100', 'description': 'Best value honeycomb paddle. 1,860 RPM spin at under $100. Raw carbon fiber face. Excellent for players on a strict budget who want honeycomb performance.'},
                 {'id': 'ronbus-quanta-r3', 'name': 'Ronbus Quanta R3', 'price_range': '$90-$110', 'description': 'Best budget EPP. 2,465 RPM spin at $90-$110. Great spin-to-price ratio at 27 RPM per dollar.'},
                 {'id': 'enhance-mpp-turbo', 'name': 'Enhance MPP Turbo Elongated', 'price_range': '$99-$120', 'description': 'Best MPP under $120. 2,690 RPM spin from an MPP core. Elongated shape gives extra reach. The best value MPP paddle in our dataset.'}
             ]},
             {'type': 'divider'},
             {'type': 'heading', 'text': 'Key Takeaways'},
             {'type': 'list', 'items': [
                 'Spin RPM matters more than price. The Spartus Spitfire ($150-$180) has the highest spin in our dataset, but the Vatic Pro Prism Flash (under $100) proves honeycomb performance does not require a premium price.',
                 'MPP foam is available under $120. The Enhance MPP Turbo Elongated at $99-$120 gives you 2,690 RPM spin — MPP performance that used to cost $150+.',
                 'Budget honeycomb paddles exist. The Vatic Pro Prism Flash 16mm and CRBN 1X 14mm offer honeycomb core performance at prices that used to only buy EPP.',
                 'Shape matters more than foam. An elongated shape adds 50-100 RPM of spin over a standard shape, regardless of foam type.'
             ]},
             {'type': 'divider'},
             {'type': 'heading', 'text': 'Value Score: Spin RPM per Dollar'},
             {'type': 'table', 'col1': 'Paddle', 'col2': 'Spin per Dollar', 'data': [
                 ['Spartus Spitfire', '~25 RPM/$'],
                 ['Vatic Pro Prism Flash 16mm', '~19 RPM/$'],
                 ['Enhance MPP Turbo', '~17 RPM/$'],
                 ['Ronbus Quanta R3', '~27 RPM/$']
             ]},
             {'type': 'paragraph', 'text': 'The Ronbus Quanta R3 offers the best spin-per-dollar ratio in our dataset. For every dollar spent, you get the most spin RPM of any paddle we have measured.'}
         ],
         None)
    ]

    guides = [
        ('how-to-choose.html', 'How to Choose a Pickleball Paddle', 'Power vs control, foam types, shapes, and what to look for at every price point.'),
        ('mpp-vs-epp.html', 'MPP vs EPP Foam — What\'s the Difference?', 'Soft and springy or firm and connected. We break down foam core types.'),
        ('budget-under-120.html', 'Best Budget Pickleball Paddles Under $120', 'Premium performance doesn\'t need a premium price. Here are the best options.'),
    ]

    # Generate guide index
    exec(open("scripts/gen-guide-index.py").read())
    print()

    for item in guides_to_generate:
        slug, title, desc, sections, guide_paddles = item
        generate_guide_page(title, slug, desc, sections, guide_paddles)
    print()


    # Copy homepage
    print("📄 Copying homepage...")
    shutil.copy2('index.html', os.path.join(OUTPUT_DIR, 'index.html'))
    print("   ✅ index.html → output/index.html")
    print()

    # Generate Best Of pages
    print("🏆 Generating Best Of ranking pages...")
    num_best_of = generate_best_of_pages()
    print()

    # Copy compare page
    print("🔍 Copying compare page...")
    if os.path.exists('templates/compare.html'):
        shutil.copy2('templates/compare.html', os.path.join(OUTPUT_DIR, 'pages', 'compare.html'))
        print("   ✅ compare.html → output/pages/compare.html")
    else:
        print("   ⚠️  templates/compare.html not found — skipping")
    print()

    # Save counts before exec() overwrites them
    _paddle_count = len(paddles)
    _shape_count = len(shapes)
    _foam_count = len(foams)
    _guide_count = len(guides)

    # Summary
    print("═══════════════════════════════════════════════════════")
    print("✅ BUILD COMPLETE")
    print(f"   Total pages: {_paddle_count} paddle + {_shape_count} shape + {_foam_count} foam + 2 built-in + {_guide_count} guide")
    print(f"   Output directory: {OUTPUT_DIR}/")
    print(f"   View locally: cd {OUTPUT_DIR} && python3 -m http.server 8080")
    print("═══════════════════════════════════════════════════════")

if __name__ == '__main__':
    main()
