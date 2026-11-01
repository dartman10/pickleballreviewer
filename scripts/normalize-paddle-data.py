#!/usr/bin/env python3
"""
Normalize pickleball paddle data to enforce consistent casing and field values.

Fixes:
  - shape: Title-case → lowercase (e.g., "Elongated" → "elongated")
  - category: Invalid values → mapped to allowed values (power, control)
  - tags: Missing foam_type tag → appends the primary foam_type
  - duplicate IDs: Detects and warns about duplicate paddle IDs

Usage: python3 scripts/normalize-paddle-data.py
Runs from project root directory.
"""
import json
import os
import sys

# Shape: Title → lowercase
SHAPES_LOWER = {
    "Elongated": "elongated",
    "Hybrid": "hybrid",
    "Widebody": "widebody",
    "Standard": "standard",
}

# Category: invalid → allowed mapping
ALLOWED_CATEGORIES = {"power", "control"}
CATEGORY_MAP = {
    "All-Court": "power",
    "all-court": "power",
    "All Court": "power",
    "hybrid": "power",
    "elongated": "power",
    "elongated-control": "control",
    "Control": "control",
}

# Foam type mapping to canonical tags
FOAM_TAGS = {
    "MPP": "MPP",
    "EPP": "EPP",
    "EMA": "EMA",
    "honeycomb": "honeycomb",
    "EVA": "EVA",
    "Honeycomb": "honeycomb",
    "HONEYCOMB": "honeycomb",
}

def normalize(project_dir):
    data_path = os.path.join(project_dir, "data", "paddles.json")
    with open(data_path) as f:
        data = json.load(f)
    paddles = data.get("paddles", [])
    changes = 0
    seen_ids = set()

    for p in paddles:
        name = p.get("name", "?")
        id = p.get("id", "?")

        # Detect duplicate IDs
        if id in seen_ids:
            print(f"⚠️  Duplicate ID: {id} ({name})")
        seen_ids.add(id)

        # 1. Normalize shape casing
        shape = p.get("shape", "")
        if shape in SHAPES_LOWER:
            p["shape"] = SHAPES_LOWER[shape]
            print(f"  shape: '{shape}' → '{p['shape']}' ({name})")
            changes += 1

        # 2. Normalize category
        cat = p.get("category", "")
        if cat not in ALLOWED_CATEGORIES:
            new_cat = CATEGORY_MAP.get(cat, cat.lower())
            p["category"] = new_cat
            print(f"  category: '{cat}' → '{new_cat}' ({name})")
            changes += 1

        # 3. Add missing foam_type tag
        foam = p.get("foam_type", "")
        foam_tag = FOAM_TAGS.get(foam) if foam else None
        tags = p.get("tags", [])
        if foam_tag and foam_tag not in tags:
            tags.append(foam_tag)
            print(f"  tags: added '{foam_tag}' ({name})")
            changes += 1

    # Write back
    data["paddles"] = paddles
    with open(data_path, "w") as f:
        json.dump(data, f, indent=4)
        f.write("\n")

    print(f"\n{'='*50}")
    print(f"Normalization complete: {changes} change(s) applied to {len(paddles)} paddle(s)")
    print("Run `python3 build.py` to regenerate pages.")
    return 0

if __name__ == "__main__":
    project_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    sys.exit(normalize(project_dir))
