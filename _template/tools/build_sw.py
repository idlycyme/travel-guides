#!/usr/bin/env python3
"""Regenerate sw.js asset list and cache version from current files.
Run inside the guide folder after any content change; the PWA only updates when the version hash changes."""
import os, hashlib, json, re
files = ['./', 'index.html', 'data.js', 'manifest.webmanifest']
for d in ['img', 'img/h', 'img/s', 'img/e', 'img/maps']:
    if os.path.isdir(d):
        files += sorted(d + '/' + f for f in os.listdir(d) if f.lower().endswith(('.jpg', '.png')))
if os.path.isdir('icons'):
    files += sorted('icons/' + f for f in os.listdir('icons') if f.endswith('.png'))
h = hashlib.sha1()
for f in files:
    if f != './':
        h.update(open(f, 'rb').read())
ver = h.hexdigest()[:10]
sw = open('sw.js').read()
guide = re.search(r"const CACHE = '([a-z0-9-]+?)-\w+';", sw).group(1)
sw = re.sub(r"// auto-generated\. version \w+", f"// auto-generated. version {ver}", sw, count=1)
sw = re.sub(r"const CACHE = '[a-z0-9-]+?-\w+';", f"const CACHE = '{guide}-{ver}';", sw, count=1)
sw = re.sub(r"const ASSETS = \[.*?\];", 'const ASSETS = ' + json.dumps(files, ensure_ascii=False) + ';', sw, count=1, flags=re.S)
open('sw.js', 'w').write(sw)
print('sw version', ver, 'assets', len(files))
