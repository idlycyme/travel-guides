#!/usr/bin/env python3
"""Download Wikipedia lead images for a mapping of keys → article titles.

usage: python3 tools/fetch_wiki.py mapping.json out_dir [--size 640]
mapping.json: {"colosseum": "Colosseum", "sansevero": "it:Cappella Sansevero", ...}
  Prefix "it:" / "ja:" etc. selects that language Wikipedia (default en).
Writes out_dir/<key>.jpg and out_dir/credits.json (source URL + title, for attribution).
Images are then downscaled with `sips -Z 480` (macOS) or any resizer.

Notes learned the hard way:
- Use prop=pageimages&pithumbsize=N; building thumb URLs by hand fails with HTTP 400.
- Batch ≤40 titles per request and sleep ~2 s between requests, or you get HTTP 429.
- Some articles have no lead image (returns nothing). Try an alternate title or skip.
- Check the results visually: logos, maps, and unrelated pictures (e.g. a flower named like a monument) slip in.
"""
import json, sys, os, time, urllib.request, urllib.parse
UA = {'User-Agent': 'TravelGuideBuilder/1.0 (personal offline travel guide)'}
mapping = json.load(open(sys.argv[1])); out = sys.argv[2]; size = 640
if '--size' in sys.argv: size = int(sys.argv[sys.argv.index('--size') + 1])
os.makedirs(out, exist_ok=True)
credits_path = os.path.join(out, 'credits.json')
credits = json.load(open(credits_path)) if os.path.exists(credits_path) else {}
by_lang = {}
for k, t in mapping.items():
    lang, title = (t.split(':', 1) if len(t) > 3 and t[2] == ':' else ('en', t))
    by_lang.setdefault(lang, {})[k] = title
for lang, items in by_lang.items():
    keys = list(items)
    for i in range(0, len(keys), 40):
        chunk = keys[i:i + 40]; titles = [items[k] for k in chunk]
        q = urllib.parse.urlencode({'action': 'query', 'prop': 'pageimages', 'piprop': 'thumbnail', 'pithumbsize': str(size), 'titles': '|'.join(titles), 'format': 'json', 'redirects': 1})
        d = json.load(urllib.request.urlopen(urllib.request.Request(f'https://{lang}.wikipedia.org/w/api.php?' + q, headers=UA), timeout=30))
        mp = {}
        for n in d['query'].get('normalized', []): mp[n['to']] = n['from']
        for r in d['query'].get('redirects', []): mp[r['to']] = mp.get(r['from'], r['from'])
        t2k = {items[k]: k for k in chunk}
        for pg in d['query']['pages'].values():
            k = t2k.get(mp.get(pg['title'], pg['title'])); th = pg.get('thumbnail', {}).get('source')
            if not k or not th: continue
            fn = os.path.join(out, k + '.jpg')
            if not os.path.exists(fn):
                try:
                    open(fn, 'wb').write(urllib.request.urlopen(urllib.request.Request(th, headers=UA), timeout=60).read())
                except Exception as e:
                    print('ERR', k, e); continue
                time.sleep(1.2)
            credits[k] = {'file': fn, 'src': th, 'title': pg['title'], 'lang': lang}
            print('ok', k, pg['title'])
        time.sleep(2)
json.dump(credits, open(credits_path, 'w'), ensure_ascii=False, indent=1)
missing = [k for k in mapping if k not in credits]
print('got', len(credits), 'missing', missing)
