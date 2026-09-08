#!/usr/bin/env python3
"""Fill coords for spots, hotels and restaurants.

usage: python3 tools/geocode.py            (reads data.js, writes coords.json for review)
Strategy, in order:
 1. keep anything already in data.js coords
 2. Wikipedia prop=coordinates for spots whose img/credits.json title is known (landmarks)
 3. Nominatim (OpenStreetMap) for hotels (plan.hotel.addr) and restaurant items (query from the maps link)
Nominatim rules: 1 request/second, a real User-Agent, results are unreliable for shop names — always
review the printed list and hand-fix obviously wrong ones (compare with the Google Maps link) before
merging into data.js. Wrong branch of a chain is the common failure.
"""
import json, re, time, urllib.request, urllib.parse, os
UA = {'User-Agent': 'TravelGuideBuilder/1.0 (personal offline travel guide)'}
G = json.loads(re.search(r'window\.GUIDE = (.*);\s*$', open('data.js').read(), re.S).group(1))
S = G['spots']; C = dict(G.get('coords', {}))
def nominatim(q):
    u = 'https://nominatim.openstreetmap.org/search?' + urllib.parse.urlencode({'q': q, 'format': 'json', 'limit': 1})
    try:
        d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30))
        return [float(d[0]['lat']), float(d[0]['lon'])] if d else None
    except Exception:
        return None
    finally:
        time.sleep(1.1)
# landmarks via wikipedia
cred = json.load(open('img/credits.json')) if os.path.exists('img/credits.json') else {}
titles = {}
for sid, sp in S.items():
    if sp.get('kind') or sid in C: continue
    key = sp['imgs'][0]['f'].rsplit('.', 1)[0]
    if key in cred: titles[sid] = (cred[key].get('lang', 'en'), cred[key]['title'])
for lang in set(l for l, _ in titles.values()):
    ts = [t for l, t in titles.values() if l == lang]
    for i in range(0, len(ts), 40):
        q = urllib.parse.urlencode({'action': 'query', 'prop': 'coordinates', 'titles': '|'.join(ts[i:i+40]), 'format': 'json', 'redirects': 1})
        d = json.load(urllib.request.urlopen(urllib.request.Request(f'https://{lang}.wikipedia.org/w/api.php?' + q, headers=UA), timeout=30))
        mp = {}
        for n in d['query'].get('normalized', []): mp[n['to']] = n['from']
        for r in d['query'].get('redirects', []): mp[r['to']] = mp.get(r['from'], r['from'])
        got = {mp.get(pg['title'], pg['title']): pg['coordinates'][0] for pg in d['query']['pages'].values() if pg.get('coordinates')}
        for sid, (l, t) in titles.items():
            if l == lang and t in got: C[sid] = [got[t]['lat'], got[t]['lon']]
        time.sleep(1.5)
# hotels
for day in G['days']:
    h = (day.get('plan') or {}).get('hotel')
    if h and h.get('id') and h['id'] not in C:
        C[h['id']] = nominatim(h['addr']); print(h['id'], h['addr'], '->', C[h['id']])
# restaurants
for sid, sp in S.items():
    if sp.get('kind') != 'eat': continue
    for i, h in enumerate(sp['highlights']):
        key = f'{sid}_{i}'
        if key in C or len(h) < 6 or not h[5]: continue
        q = urllib.parse.unquote(h[5].split('query=')[1]) if 'query=' in h[5] else h[1]
        q = ', '.join(p for p in q.split(', ') if not re.search(r'[一-鿿]', p))
        C[key] = nominatim(q); print(key, '|', q, '->', C[key])
C = {k: v for k, v in C.items() if v}
json.dump(C, open('coords.json', 'w'), ensure_ascii=False, indent=1)
print('coords', len(C), '— review coords.json, then merge into data.js coords')
