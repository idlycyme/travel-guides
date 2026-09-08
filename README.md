# travel-guides

Offline-first travel guide PWAs, one folder per trip, served with GitHub Pages. Plain HTML + one `data.js`, no build step, no framework.

- `italy/` — 2026 Italy (Rome, Naples, Tuscany, Cinque Terre, Florence, Venice, Milan). Live: https://idlycyme.github.io/travel-guides/italy/
- `_template/` — copy this to start a new guide. Its `README.md` documents the data schema, the tools and the 10-step build workflow.
- `AGENTS.md` — rules for AI assistants (and humans) editing this public repo: what must never be committed, pre-push checks, build rules.
- `.claude/skills/travel-guide/` — Claude Code project skill that automates the workflow.

## Make your own guide

### With Claude Code (recommended)
1. Fork or clone this repo and open it in Claude Code. The project skill is picked up automatically.
2. Type:
   ```
   /travel-guide 日本 2027/4/1–4/10
   ```
   then paste or attach: your itinerary (screenshot or sheet with dates, cities, booked slots, trains, hotels), friends' Google Maps links with their notes, any shared Google Maps list link, and your souvenir wish list.
3. Answer the two questions it will ask: which trip folder name to use, and whether hotels and flights may be public.
4. It writes `<trip>/data.js`, fetches images, builds maps, runs the checks in `AGENTS.md`, and pushes. Open `https://<you>.github.io/travel-guides/<trip>/` on your phone, Safari → Share → 加入主畫面.

Useful follow-up prompts once the guide exists:
- `把這份清單的餐廳加進去 <Google Maps 分享連結>`
- `每個看點加上當地語言與英文名稱`
- `伴手禮加入 <商品名>，放在對應城市`
- `重新產生 9/22 的地圖`
- `我改了 data.js，幫我更新 sw 版本並部署`

### Without an AI assistant
Copy `_template/` to a new folder, fill `data.js` following `_template/README.md`, run the scripts in `tools/`, push. Enable GitHub Pages on `main` / root and add a link in the root `index.html`.

## Credits
Images from Wikipedia / Wikimedia Commons (see each guide's `img/*/credits.json`). Map tiles © OpenStreetMap contributors. Content is personal travel notes; check official sites for hours and prices.
