This folder is the local source of the `italy/` guide in a **public** GitHub Pages repo. Everything here gets published.
Rules: see `AGENTS.md` at the repo root (no emails, local paths, account details, secrets, ticket or policy numbers; hotels and flights are allowed by the owner's decision).
After content edits run `python3 tools/build_sw.py`. Before pushing run the pre-push grep from `AGENTS.md` §2 and make sure it returns nothing. Account and push details are in the assistant's memory, not in this file.
