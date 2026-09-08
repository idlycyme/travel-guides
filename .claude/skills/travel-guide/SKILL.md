---
name: travel-guide
description: Build an offline travel-guide PWA (day pages, trilingual sight highlights, souvenirs, restaurants, offline maps) from an itinerary, using the travel-guides template repo. Use when the user asks for a 旅遊導覽 / travel guide / 行程網頁 for a trip.
---

# Travel guide builder

Produces a static PWA in `<trip>/` of this repo from the template at `_template/`. Reference implementation: `italy/` (2026 Italy). Read `_template/README.md` first for the data schema and known pitfalls; do not re-derive them.

## Inputs to collect before starting
1. Itinerary: dates, cities, booked time slots, trains/flights, hotels with addresses (screenshot or sheet is fine).
2. Friends' recommendations: Google Maps short links with notes; shared Google Maps lists.
3. Souvenir wish list, if any.
4. Which items may be public. Default: emails, local paths, account names, ticket and policy numbers never go in; hotels and flights only if the user says so.

## Workflow (follow the README's 10 steps)
- Copy `_template/` to `<trip>/`, set `meta` (id, title, year, tz).
- Write `days` from the itinerary; `eat_*`/`shop_*` entries go under the first day whose city matches, not the arrival evening. Add a final `購物` day with `shop_general`.
- Write spots: intro, 6–10 highlights as `[中文, local language, English, 說明, thumb, map]`, history, tips. Local-language names are mandatory (on-site signs).
- Fetch images with `tools/fetch_wiki.py`; review a contact sheet; delete logos, maps and mismatches.
- Restaurants: resolve links with `tools/resolve_links.py`; shared lists with `tools/gmaps_list_dump.mjs` (headless Chrome via CDP; the public API returns only 10 items). Every store gets a per-store Google Maps search link, never the list link. Non-store food knowledge goes in `notes`.
- Coordinates: `tools/geocode.py`, then hand-check; fix wrong branches.
- Maps: `tools/mkmaps.py` (OSM France tiles; official OSM tiles block, CARTO needs a key). Merge `maps.json` into `days[].maps`.
- `tools/build_sw.py` after every content change, or phones keep the old cache.
- Verify: JS syntax check of index.html, headless Chrome screenshots at 500px width of overview, a spot page, a day page.
- Deploy: commit, push, add a link in the repo root `index.html`. Live at `https://<user>.github.io/travel-guides/<trip>/`. Read `AGENTS.md` before the first push.

## Quality bar (from the Italy build)
- Day page opens by default: Day 1 before the trip, the current day during it.
- Each restaurant item expands inline on the day page (name, photo, description, map button).
- Souvenir items say what it is, how to choose, price range, where to buy.
- Before the first public push, grep the tree and git history for emails, `/Users/`, account names, ticket ids; squash history if anything leaked.
