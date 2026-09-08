# AGENTS.md — rules for AI assistants working in this repo

This repository is **public** and served by GitHub Pages. Anything committed is visible to everyone and stays in git history. Read this before editing or pushing.

## 1. Never commit
- Email addresses of any kind (work, personal, in User-Agent strings, in scripts, in commit author). Use `<user>@users.noreply.github.com` as the git author email.
- Local filesystem paths (`/Users/...`, `/home/...`, `/private/tmp/...`). Tools must use paths relative to the guide folder.
- Account or infrastructure details: SSH host aliases, GitHub usernames of other accounts, hostnames, IP addresses.
- Secrets: API keys, tokens, passwords, `.pat` files, cookies. Map-tile or geocoding keys go in environment variables, never in files.
- Booking identifiers: ticket codes (e.g. Vivaticket `TLITE…`), PNRs, insurance policy numbers, passport data, phone numbers, names of friends or third parties.
- Real-time location that is not already public by the owner's choice.

Hotels, addresses and flight numbers are the owner's call. Default to **asking** before adding them; in `italy/` the owner chose to keep them public.

## 2. Before every push
Run from the repo root and get an empty result:
```
grep -rIn -E "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}|/Users/|/private/tmp|ghp_|AKIA|api[_-]?key|TLITE[0-9]+" --exclude-dir=.git . | grep -v "users.noreply.github.com"
git log --all -p | grep -oE "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}" | sort -u   # only noreply addresses allowed
```
If something leaked and was already pushed, rewrite history (orphan branch → single commit → force push) and tell the owner; deleting the line in a new commit is not enough.

## 3. Content and build rules
- One guide per folder; `index.html` is shared logic and reads everything from `data.js`. Do not hard-code trip text in `index.html`.
- After changing any content, run `python3 tools/build_sw.py` inside the guide folder. The service-worker cache name carries a content hash; without it phones keep the old version.
- `eat_*` and `shop_*` entries go under the first day whose `city` matches, not the arrival evening.
- Every store item needs its own Google Maps link (`https://www.google.com/maps/search/?api=1&query=…`). Never link a whole shared list from a store item.
- Images: Wikipedia/Wikimedia only, keep `credits.json`, downscale (≤1600px hero, ≤480px thumbs), keep a guide under ~50 MB total (iOS cache limit).
- Map tiles: do not bulk-download from `tile.openstreetmap.org` (blocked, against policy). Use OSM France or a keyed provider; keep the attribution line on the rendered image.
- Keep the app dependency-free (no CDN scripts) so it works offline.

## 4. Verification before saying "done"
- `node -e` syntax check of the inline script in `index.html`.
- Headless Chrome screenshots at 500 px width: overview, one spot page, one day page.
- Live check after deploy: `curl` the guide's `sw.js` and compare the version line with the local file.

## 5. Workflow reference
`_template/README.md` is the canonical schema and build workflow. The project skill `.claude/skills/travel-guide/SKILL.md` wraps it for Claude Code (`/travel-guide`). Keep the three in sync when the schema changes.
