#!/usr/bin/env python3
"""Resolve Google Maps short links (maps.app.goo.gl/...) to place name and coordinates.

usage: python3 tools/resolve_links.py links.txt
links.txt: one per line, optionally "key|url".
Prints key | name | lat,lng. Coordinates come from the @lat,lng in the redirected URL;
for a saved list (data=!4m2!11m1!2s<listId>) only the list id is printed — use gmaps_list_dump.mjs.
"""
import sys, re, urllib.request, urllib.parse, urllib.error
UA = {'User-Agent': 'Mozilla/5.0'}
for line in open(sys.argv[1]):
    line = line.strip()
    if not line: continue
    key, url = (line.split('|', 1) if '|' in line else (line, line))
    try:
        req = urllib.request.Request(url, headers=UA, method='HEAD')
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *a, **k): return None
        opener = urllib.request.build_opener(NoRedirect)
        try:
            opener.open(req, timeout=20); final = url
        except urllib.error.HTTPError as e:
            final = e.headers.get('Location', url)
    except Exception as e:
        print(key, '| ERR', e); continue
    final = urllib.parse.unquote(final)
    m = re.search(r'/place/([^/]+)/', final); ll = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', final); lst = re.search(r'11m1!2s([A-Za-z0-9_-]+)', final)
    name = m.group(1).replace('+', ' ') if m else ('LIST ' + lst.group(1) if lst else final[:100])
    print(key, '|', name, '|', f'{ll.group(1)},{ll.group(2)}' if ll else '')
