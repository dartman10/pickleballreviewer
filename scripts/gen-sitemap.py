#!/usr/bin/env python3
"""
Generate sitemap.xml for Pickleball Reviewer.
All URLs are relative to https://pickleballreviewer.com/
"""
import json
import os

DATA_FILE = "data/paddles.json"
OUTPUT_DIR = "output"

def generate_sitemap():
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    paddles = data['paddles']

    urls = []

    # Homepage
    urls.append({
        "loc": "https://pickleballreviewer.com/",
        "priority": "1.0",
        "freq": "weekly"
    })

    # Paddle pages
    for p in paddles:
        urls.append({
            "loc": f"https://pickleballreviewer.com/pages/paddles/{p['id']}.html",
            "priority": "0.8",
            "freq": "monthly"
        })

    # Category index
    urls.append({
        "loc": "https://pickleballreviewer.com/pages/categories/index.html",
        "priority": "0.9",
        "freq": "weekly"
    })

    # Category pages
    categories = [
        ("power", "Power Paddles"),
        ("elongated", "Elongated"),
        ("MPP", "MPP Foam"),
        ("EPP", "EPP Foam"),
        ("budget", "Budget"),
        ("hybrid", "Hybrid"),
    ]
    for slug, _ in categories:
        urls.append({
            "loc": f"https://pickleballreviewer.com/pages/categories/{slug}.html",
            "priority": "0.8",
            "freq": "weekly"
        })

    # Guide index
    urls.append({
        "loc": "https://pickleballreviewer.com/pages/guides/index.html",
        "priority": "0.9",
        "freq": "weekly"
    })

    # Guide pages
    guides = [
        "how-to-choose",
        "mpp-vs-epp",
        "budget-under-120",
    ]
    for g in guides:
        urls.append({
            "loc": f"https://pickleballreviewer.com/pages/guides/{g}.html",
            "priority": "0.8",
            "freq": "monthly"
        })

    # Best Of index
    urls.append({
        "loc": "https://pickleballreviewer.com/pages/best-of/index.html",
        "priority": "0.9",
        "freq": "weekly"
    })

    # Best Of ranking pages
    best_of_slugs = [
        "best-power-pickleball-paddles",
        "best-budget-pickleball-paddles-under-100",
        "best-spin-pickleball-paddle",
        "best-value-pickleball-paddle",
    ]
    for slug in best_of_slugs:
        urls.append({
            "loc": f"https://pickleballreviewer.com/pages/best-of/{slug}.html",
            "priority": "0.8",
            "freq": "weekly"
        })

    # Reviewer index
    urls.append({
        "loc": "https://pickleballreviewer.com/reviewers/index.html",
        "priority": "0.9",
        "freq": "weekly"
    })

    # Reviewer detail pages
    reviewers = [
        "pickleball-studio",
        "john-kew",
        "the-kitchen",
        "pickleball-effect",
    ]
    for slug in reviewers:
        urls.append({
            "loc": f"https://pickleballreviewer.com/reviewers/{slug}.html",
            "priority": "0.8",
            "freq": "weekly"
        })

    # Compare page
    urls.append({
        "loc": "https://pickleballreviewer.com/pages/compare.html",
        "priority": "0.7",
        "freq": "weekly"
    })

    # Legal pages
    urls.append({
        "loc": "https://pickleballreviewer.com/privacy.html",
        "priority": "0.5",
        "freq": "yearly"
    })
    urls.append({
        "loc": "https://pickleballreviewer.com/affiliate-disclosure.html",
        "priority": "0.5",
        "freq": "yearly"
    })

    # Build XML
    xml_parts = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        xml_parts.append('  <url>')
        xml_parts.append(f'    <loc>{u["loc"]}</loc>')
        xml_parts.append(f'    <changefreq>{u["freq"]}</changefreq>')
        xml_parts.append(f'    <priority>{u["priority"]}</priority>')
        xml_parts.append('  </url>')
    xml_parts.append('</urlset>')

    sitemap = '\n'.join(xml_parts)

    # Write to output/
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, 'sitemap.xml')
    with open(out_path, 'w') as f:
        f.write(sitemap)

    print(f"🗺️  sitemap.xml → {out_path} ({len(urls)} URLs)")
    return len(urls)

if __name__ == '__main__':
    count = generate_sitemap()
    print(f"   Total sitemap entries: {count}")
