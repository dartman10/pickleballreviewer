#!/usr/bin/env python3
"""
Pickleball Review Hub — Verification Script
Run this before every build.py run to catch data quality issues.

Usage: python3 scripts/verify-site-data.py
Runs from project root directory.
"""
import json
import os
import sys

def verify(project_dir):
    errors = 0
    warnings = 0

    data_path = os.path.join(project_dir, "data", "paddles.json")
    output_dir = os.path.join(project_dir, "output")

    # 1. JSON validity
    try:
        with open(data_path) as f:
            data = json.load(f)
        paddles = data.get("paddles", [])
        print(f"\n✅ JSON valid: {len(paddles)} paddle(s)")
    except json.JSONDecodeError as e:
        print(f"❌ JSON invalid: {e}")
        return 1
    except FileNotFoundError:
        print(f"❌ File not found: {data_path}")
        return 1

    required_fields = [
        "id", "name", "brand", "category", "price_range",
        "youtube_videos", "written_reviews", "consensus_topics", "retailers"
    ]

    # 2. Required fields check
    for p in paddles:
        missing = [f for f in required_fields if f not in p]
        if missing:
            print(f"❌ {p.get('name','?')}: missing fields {missing}")
            errors += 1
        # Check optional fields are arrays
        for arr_field in ["youtube_videos", "written_reviews", "consensus_topics", "tags", "retailers"]:
            if arr_field in p and not isinstance(p[arr_field], list):
                print(f"⚠️  {p['name']}: {arr_field} is not a list, found {type(p[arr_field]).__name__}")
                warnings += 1

    # 3. YouTube URL integrity
    for p in paddles:
        for v in p.get("youtube_videos", []):
            url = v.get("url", "")
            if url and "youtube.com" not in url and "youtu.be" not in url:
                print(f"❌ {p['name']}: '{url}' is NOT a YouTube URL")
                errors += 1

    # 4. Written review source URLs
    for p in paddles:
        for r in p.get("written_reviews", []):
            url = r.get("url", "")
            if url and not url.startswith("http"):
                print(f"❌ {p['name']}: '{url}' is not an http URL")
                errors += 1
            author = r.get("author", "")
            site = r.get("site", "")
            if not author:
                print(f"⚠️  {p['name']}: review missing 'author' field")
                warnings += 1
            if not site:
                print(f"⚠️  {p['name']}: review missing 'site' field")
                warnings += 1

    # 5. Consensus source integrity
    for p in paddles:
        review_authors = set(r.get("author", "") for r in p.get("written_reviews", []))
        for ct in p.get("consensus_topics", []):
            for src in ct.get("sources", []):
                if src not in review_authors:
                    print(f"❌ {p['name']}: consensus source '{src}' not in reviews: {review_authors}")
                    errors += 1

    # 6. Output file integrity
    expected_files = [
        "index.html", "css/style.css", "js/app.js", "data/paddles.json",
    ]
    for p in paddles:
        expected_files.append(f"pages/paddles/{p['id']}.html")

    if os.path.exists(output_dir):
        for ef in expected_files:
            fp = os.path.join(output_dir, ef)
            if not os.path.exists(fp):
                print(f"❌ Missing output file: {ef}")
                errors += 1

        # Check for double .html
        for root, dirs, files in os.walk(output_dir):
            for fname in files:
                if ".html.html" in fname:
                    print(f"❌ Double .html: {os.path.join(root, fname)}")
                    errors += 1

        # Check SEO schema
        for p in paddles:
            page_path = os.path.join(output_dir, "pages", "paddles", f"{p['id']}.html")
            if os.path.exists(page_path):
                with open(page_path) as f:
                    content = f.read()
                if '"@type": "Product"' not in content:
                    print(f"❌ {p['name']}: missing Product schema")
                    errors += 1
                if "rel=\"canonical\"" not in content:
                    print(f"❌ {p['name']}: missing canonical URL")
                    errors += 1
    else:
        print(f"⚠️  Output directory not found: {output_dir} (run build.py first)")
        warnings += 1

    # 7. Reviewer page unique paddle count
    if os.path.exists(output_dir):
        reviewer_dir = os.path.join(output_dir, "reviewers")
        if os.path.exists(reviewer_dir):
            import re
            for fname in os.listdir(reviewer_dir):
                if fname.endswith(".html"):
                    with open(os.path.join(reviewer_dir, fname)) as f:
                        content = f.read()
                    count_match = re.search(r'<strong>(\d+) paddles reviewed on this site</strong>', content)
                    link_count = len(re.findall(r'href="[^"]*pages/paddles/', content))
                    if count_match and int(count_match.group(1)) != link_count:
                        print(f"⚠️  {fname}: count says {count_match.group(1)} but links show {link_count}")
                        warnings += 1

    # Summary
    print(f"\n{'='*50}")
    print(f"Results: {errors} error(s), {warnings} warning(s)")
    if errors > 0:
        print("❌ FAIL — Fix errors before building")
        return 1
    elif warnings > 0:
        print("⚠️  WARNINGS — Review before deploying")
        return 0
    else:
        print("✅ PASS — Safe to build and deploy")
        return 0


if __name__ == "__main__":
    project_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    sys.exit(verify(project_dir))
