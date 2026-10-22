# Stolen AI API key check (15 minutes)

What this is: the four things I did after the Railway breach (Oct 21, 2026), as a checklist you can run tonight.
Why: stolen Claude/OpenAI keys are being resold, and one OpenCode user saw $1,744.66 of charges in a single day
(Oct 18, 2026). A hard spend cap is what stopped it from being worse.

No accounts, keys or personal details of mine are in here. Check each provider's own docs (linked) before you
change anything; menus move.

## 1. Delete and replace your AI API keys (5 min)

Do this if a key ever lived in a hosted env var (Railway, Vercel, Netlify…), a repo, or a tool you logged into.

- **Claude (Anthropic):** Claude Console → **API keys** (`platform.claude.com/settings/keys`). Create a new key,
  put it where the old one was, then **Delete** the old one (Disable is reversible, Delete is permanent).
  New keys can get an expiration date.
- **OpenAI:** `platform.openai.com/api-keys`. Create the replacement, update your app, then revoke the old key.

Find where a key is used before you delete it:

```sh
# in each project folder: which files mention a key-shaped string (prints file names only)
git grep -lE 'sk-(ant|proj)-' || true
```

Then check your hosting provider's environment variables too (they are not in git).

## 2. Set a HARD spend cap (3 min)

- **Claude:** Settings → **Billing** → **Spend limits** → set limit. When usage hits it, requests stop (HTTP 400).
  Workspaces can have their own limit (not the Default workspace).
- **OpenAI:** Settings → Organization → **Limits** → Spend → *Edit spend limit* → turn on **"Enforce a hard limit"**.
  Without that toggle it is only an email alert and traffic continues.

Docs: `platform.claude.com/docs/en/api/rate-limits`, `developers.openai.com/api/docs/guides/spend-limits`.

## 3. Patch this week's bugs (5 min)

```sh
php -v     # update to 8.5.12, 8.4.27, 8.3.36 or 8.2.35 (PHP 8.1 and older: no official fix)
node -v    # update to 26.12.1, 24.22.1 or 22.23.4
```

Sources: php.net news (Oct 21, 2026), nodejs.org "October 2026 security releases" (Oct 21, 2026).

## 4. Security-check what runs without you (2 min to list)

Write down every bot, scraper, cron job or agent that runs on the web while you sleep, and for each one:
which key it uses, where that key is stored, and what it can spend. One key per app makes step 1 painless next time.

## My numbers (Oct 22, 2026)

- 8× H200 (enough for a full open-weight model like GLM-5.3) rents for $31.68–$42.32 an hour on GPU clouds,
  $63.30 on AWS → $22,810–$30,470 a month if it runs 24/7.
- Split across 10 small companies that is still $2,281–$3,047 each per month.

Sources for every number: the video description.
