#!/usr/bin/env python3
"""Test all Week 1 pages for correctness."""

import os, json, sys

BASE = "/Users/7p/myFiles/brainstormer/pickleball-review-hub/output"
PAGES = os.path.join(BASE, "pages")
RESULTS = []

def check(name, path, checks):
    """Check a file against a list of (label, predicate) pairs."""
    if not os.path.exists(path):
        RESULTS.append(f"FAIL  {name}: FILE MISSING")
        return
    with open(path) as f:
        content = f.read()
    failed = [label for label, pred in checks if not pred(content)]
    status = "OK" if not failed else f"FAIL: {'; '.join(failed)}"
    RESULTS.append(f"{'✅' if not failed else '❌'} {name}: {status}")

# --- Homepage ---
check("homepage",
      os.path.join(PAGES, "index.html"),
      [
          ("has title", lambda c: "<title>" in c),
          ("has paddles", lambda c: "paddle" in c.lower()),
          ("has nav", lambda c: 'class="nav"' in c or 'class="navbar"' in c),
          ("has footer", lambda c: "<footer" in c.lower() or "footer" in c.lower()),
      ])

# --- Guide pages ---
for guide in ["best-pickleball-paddles", "how-to-choose-a-paddle", "paddle-terminology"]:
    check(f"guide {guide}",
          os.path.join(PAGES, "guides", f"{guide}.html"),
          [
              ("has title", lambda c: "<title>" in c),
              ("has h1", lambda c: "<h1" in c.lower()),
          ])

# --- Reviewer pages ---
reviewers = ["pickleball-studio", "johnkew-pickleball", "the-kitchen"]
for rev in reviewers:
    check(f"reviewer {rev}",
          os.path.join(PAGES, "reviewers", f"{rev}.html"),
          [
              ("has title", lambda c: "<title>" in c),
              ("has paddle links", lambda c: 'class="paddle-link"' in c or 'class="paddle-card"' in c),
          ])

# --- Category pages ---
categories = ["power", "control", "budget", "all-court", "spin", "foam-core", "elongated", "widebody", "hybrid"]
for cat in categories:
    check(f"category {cat}",
          os.path.join(PAGES, "categories", f"{cat}.html"),
          [
              ("has title", lambda c: "<title>" in c),
              ("has paddles", lambda c: "paddle" in c.lower()),
          ])

# --- All 16 paddle pages ---
with open("/Users/7p/myFiles/brainstormer/pickleball-review-hub/data/paddles.json") as f:
    data = json.load(f)

for i, paddle in enumerate(data['paddles']):
    slug = paddle['id']
    path = os.path.join(PAGES, "paddles", f"{slug}.html")
    videos = len(paddle.get('youtube_videos', []))
    reviews = len(paddle.get('written_reviews', []))
    consensus = len(paddle.get('consensus_topics', []))
    retailers = len(paddle.get('retailers', []))
    
    checks = [
        ("has Product schema", lambda c: '"@type": "Product"' in c),
        ("has BreadcrumbList schema", lambda c: '"@type": "BreadcrumbList"' in c),
        ("has canonical", lambda c: 'rel="canonical"' in c),
        ("has page title", lambda c: f'{paddle["name"]} Review' in c or paddle['name'] in c),
        (f"videos={videos} (found {videos})", lambda c, v=videos: c.count('class="video-card"') >= v),
        (f"reviews={reviews} (found {reviews})", lambda c, r=reviews: c.count('class="review-block"') >= r),
        (f"consensus={consensus} (found {consensus})", lambda c, n=consensus: c.count('class="consensus-sources"') >= n),
        (f"retailers={retailers} (found {retailers})", lambda c, r=retailers: c.count('class="retailer-link"') >= r),
        ("has specs table", lambda c: '<table' in c.lower() or 'measured_specs' in c.lower() or 'swing weight' in c.lower()),
    ]
    check(f"[{i:02d}] {paddle['name']}", path, checks)

# --- Print results ---
total = len(RESULTS)
ok = sum(1 for r in RESULTS if r.startswith('✅'))
fail = sum(1 for r in RESULTS if r.startswith('❌'))

print("=" * 60)
print(f"WEBSITE TEST — {total} pages | {ok} OK | {fail} FAIL")
print("=" * 60)
for r in RESULTS:
    print(r)

print("=" * 60)
if fail == 0:
    print("ALL CHECKS PASSED ✅")
else:
    print(f"FAILURES: {fail}")
