import os

FAVICON = '  <link rel="icon" type="image/png" href="https://jfnewsom.github.io/is2053-assets/favicon.png">'
VIEWPORT = '  <meta name="viewport" content="width=device-width, initial-scale=1.0">'

support_dir = 'pages/support'
patched = []
skipped = []

for fname in sorted(os.listdir(support_dir)):
    if not fname.endswith('.html'):
        continue
    path = os.path.join(support_dir, fname)
    with open(path) as f:
        content = f.read()
    if 'favicon' in content:
        skipped.append(fname)
        continue
    if VIEWPORT in content:
        content = content.replace(VIEWPORT, VIEWPORT + '\n' + FAVICON, 1)
        with open(path, 'w') as f:
            f.write(content)
        patched.append(fname)

print(f"Patched {len(patched)} files:")
for f in patched: print(' ✓', f)
if skipped:
    print(f"\nSkipped {len(skipped)} (already had favicon):")
    for f in skipped: print(' –', f)
