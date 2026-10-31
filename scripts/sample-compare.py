#!/usr/bin/env python3
"""Generate sample comparison page to preview the feature."""
import json

with open("data/paddles.json") as f:
    data = json.load(f)

compare_ids = ['enhance-mpp-turbo', 'spartus-spitfire', 'crbn-3x-16mm']
paddles = [p for p in data['paddles'] if p['id'] in compare_ids]

spec_rows = [
    ('Price', lambda p: p['price_range']),
    ('Spin RPM', lambda p: p['measured_specs'].get('spin_rpm', 'N/A')),
    ('Swing Weight (g·cm²)', lambda p: p['measured_specs'].get('swing_weight', 'N/A')),
    ('Twist Weight (kg·cm²)', lambda p: p['measured_specs'].get('twist_weight', 'N/A')),
    ('Balance Point', lambda p: p['measured_specs'].get('balance_point', 'N/A')),
    ('Static Weight', lambda p: p['measured_specs'].get('static_weight', 'N/A')),
    ('Grip Size', lambda p: p['measured_specs'].get('grip_size', 'N/A')),
    ('Shape', lambda p: p['shape']),
    ('Core', lambda p: p['foam_type']),
    ('Best For', lambda p: ', '.join(p['best_for']) if p.get('best_for') else '—'),
]

sort_direction = {
    'Spin RPM': True, 'Twist Weight': True, 'Swing Weight': False,
    'Balance Point': False, 'Static Weight': False, 'Price': False
}

def get_numeric(paddle, spec_name):
    spec_idx = [s[0] for s in spec_rows].index(spec_name)
    val = spec_rows[spec_idx][1](paddle)
    if val == 'N/A':
        return None
    if spec_name == 'Price':
        try: return int(val.replace('$', '').replace('+', ''))
        except: return None
    if spec_name == 'Spin RPM':
        try: return int(str(val).replace(',', '').split('/')[0])
        except: return None
    if spec_name == 'Swing Weight':
        try: return float(val.replace('g·cm²', '').replace('g·cm2', ''))
        except: return None
    if spec_name == 'Twist Weight':
        try: return float(val.split()[0])
        except: return None
    if spec_name == 'Static Weight':
        try: return float(val.replace('oz', ''))
        except: return None
    if spec_name == 'Balance Point':
        try: return int(val.replace('mm', ''))
        except: return None
    return None

best_values = {}
for spec_name, _ in spec_rows:
    if spec_name in ('Grip Size', 'Shape', 'Core', 'Best For'):
        continue
    vals = []
    for p in paddles:
        v = get_numeric(p, spec_name)
        if v is not None:
            vals.append((p, v))
    if vals:
        is_higher_better = sort_direction.get(spec_name, False)
        best = max(vals, key=lambda x: x[1]) if is_higher_better else min(vals, key=lambda x: x[1])
        for p, v in vals:
            if p == best[0]:
                best_values[(p['id'], spec_name)] = True

rows_html = ''
for spec_name, fn in spec_rows:
    cells = ''
    for p in paddles:
        val = fn(p)
        is_best = best_values.get((p['id'], spec_name), False)
        style = 'background: rgba(76, 209, 129, 0.15); font-weight: 700;' if is_best else ''
        badge = ' ✓' if is_best else ''
        cells += '<td style="' + style + '">' + str(val) + badge + '</td>'
    rows_html += '<tr><th>' + spec_name + '</th>' + cells + '</tr>'

headers_html = ''
for p in paddles:
    headers_html += '<th><div style="text-align:center;font-weight:700;font-size:0.95rem;margin-bottom:4px;">' + p['name'] + '</div><div style="text-align:center;font-size:0.8rem;color:#8888a0;">' + p['price_range'] + '</div></th>'

html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sample Comparison — Pickleball Reviewer</title>
<style>
:root {
    --bg: #0a0a0f; --bg-alt: #12121a; --text: #e8e8f0; --text-secondary: #8888a0;
    --accent: #6c5ce7; --green: #4cd181; --blue: #5b9bd5; --border: #2a2a3a;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Inter', system-ui, sans-serif; background: var(--bg); color: var(--text); padding: 24px; }
h1 { font-size: 1.4rem; margin-bottom: 8px; }
.subtitle { color: var(--text-secondary); margin-bottom: 24px; font-size: 0.9rem; }
.url-bar { background: var(--bg-alt); border: 1px solid var(--border); border-radius: 8px; padding: 10px 14px; font-family: monospace; font-size: 0.85rem; color: var(--accent); margin-bottom: 24px; word-break: break-all; }
.table-wrap { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; min-width: 600px; }
th, td { padding: 12px 16px; text-align: left; border-bottom: 1px solid var(--border); font-size: 0.9rem; }
th { background: var(--bg-alt); font-weight: 700; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-secondary); }
th[colspan="1"] { background: var(--bg-alt); }
tr:last-child th, tr:last-child td { border-bottom: none; }
td:first-child { font-weight: 600; color: var(--text-secondary); min-width: 120px; }
.highlight-best { color: var(--green); font-weight: 700; }
.legend { margin-top: 16px; font-size: 0.8rem; color: var(--text-secondary); }
.legend span { display: inline-block; margin-right: 24px; }
</style>
</head>
<body>

<h1>Paddle Comparison</h1>
<p class="subtitle">Side-by-side specs from verified measurements</p>

<div class="url-bar">
  Sample URL: /pages/compare.html?paddles=enhance-mpp-turbo,spartus-spitfire,crbn-3x-16mm
</div>

<div class="table-wrap">
<table>
  <thead>
    <tr><th>Spec</th>''' + headers_html + '''</tr>
  </thead>
  <tbody>
    ''' + rows_html + '''
  </tbody>
</table>
</div>

<div class="legend">
  <span>&#10003; = Best value in row</span>
  <span>Green = Higher is better</span>
  <span>Blue = Lower is better</span>
</div>

</body>
</html>'''

with open('output/pages/sample-compare.html', 'w') as f:
    f.write(html)

print("Sample comparison page: output/pages/sample-compare.html")
print("Open: http://localhost:8080/pages/sample-compare.html")

print("\n=== DATA SAMPLE ===")
for spec_name, fn in spec_rows:
    vals = [(p['name'], fn(p)) for p in paddles]
    print(f"\n{spec_name}:")
    for name, val in vals:
        print(f"  {name}: {val}")
