# 🚀 Deploy Tutorial — Shahin://HUB on GitHub Pages

Step-by-step: take this repository from local workspace → live website at
**https://shaiinarab.github.io/shaiinarab/**

Everything is already wired up — this repo ships with:

- `index.html` + `assets/` — the hub site (no build step needed)
- `404.html`, `robots.txt`, `sitemap.xml` — platform files
- `.github/workflows/deploy-pages.yml` — auto-deploys on every push to `main`
- `scripts/verify.mjs` — pre-flight checks you can run anytime

---

## Step 0 — Pre-flight (30 seconds)

Before shipping, run the verification battery:

```bash
node scripts/verify.mjs
```

Expected last line: `GREEN — all checks passing`. If it prints `RED`, fix the listed check IDs first.

---

## Step 1 — Commit your changes

**Option A — Freebuff Changes panel (recommended):**
Open the Changes panel → review the diff → **Save / Commit**.
Write a message like: `feat: repo hub site with auto-sync directory`

> ⚠️ Do not stage junk: `_bmad/render/` is already gitignored; everything else in the diff is meant to ship.

**Option B — terminal:**

```bash
git add -A
git status                 # sanity-check what's staged
git commit -m "feat: repo hub site with auto-sync directory"
```

*(If you use Option B inside Freebuff, only commit — pushes are handled next step.)*

---

## Step 2 — Push to `main`

```bash
git push origin main
```

Freebuff injects the GitHub credential automatically — no tokens, no SSH setup.
(If Freebuff reports it cannot mint the credential: reconnect the repository or update the Freebuff GitHub App permissions.)

The push triggers `.github/workflows/deploy-pages.yml`.

---

## Step 3 — Watch the deploy (first run matters!)

1. Open **https://github.com/Shaiinarab/shaiinarab/actions**
2. Click the run named **"Deploy to GitHub Pages"**
3. Wait ~30–60s for the `deploy` job to turn green ✅

### 🔴 First-run gotcha

If the job fails with something like *"Pages not enabled"* or a 404 from `deploy-pages`:

1. Go to **Settings → Pages** (sidebar of the repo)
2. Under **Build and deployment → Source**, select **GitHub Actions**
3. Back to the failed run → click **Re-run jobs**

That one-time flip is all it takes. Every later push deploys automatically.

---

## Step 4 — Verify it's live

Open **https://shaiinarab.github.io/shaiinarab/** and confirm:

| Check | Expected |
|---|---|
| Hero + neon theme loads | Terminal card shows `✓ synced <time>` |
| Repo grid fills | Your public repos appear with stars/forks |
| Search + `/` hotkey | Typing filters the grid |
| Language chips | Clicking one filters by language |
| Unknown URL e.g. `/shaiinarab/foo` | Themed 404 page with working "Back to the hub" |
| View counter in footer | Increments |

If the grid shows the amber *"Couldn't reach the GitHub API"* banner with a cached snapshot: that's the built-in fallback working — hit **Retry sync ⟳** or reload.

---

## Step 5 — Make it *usable*: point people at it

1. **Set the homepage** on this repo:
   `repo → ⚙️ About (top-right) → Website → https://shaiinarab.github.io/shaiinarab/`
2. **Profile README already links it** — the `🌐 ENTER THE HUB` badge in `README.md` now resolves once deployed.
3. Optional — pin the repo: profile page → **Customize your pins** → select `shaiinarab`.
4. Optional — custom domain (e.g. `hub.yourdomain.com`):
   - DNS: `CNAME` record → `Shaiinarab.github.io`
   - Settings → Pages → Custom domain → enter it → enable **Enforce HTTPS**
   - Add a `CNAME` file containing the domain to the repo root, and update the canonical/sitemap URLs in `index.html`, `robots.txt`, `sitemap.xml`, and `404.html` (they currently hard-code `shaiinarab.github.io/shaiinarab/`)
   - Re-run the workflow

---

## Day-to-day: how updates work

| You do | What happens |
|---|---|
| Push to `main` | Auto-redeploy (~60s) |
| Publish a new public repo on GitHub | Appears on the hub on next visitor load — no redeploy needed |
| Archive a repo | Card dims + gets ARCHIVED badge automatically |
| Run out of free API quota | Visitors see the offline snapshot until quota resets |

## Troubleshooting

| Symptom | Fix |
|---|---|
| Actions run fails first time | Settings → Pages → Source = **GitHub Actions** → re-run |
| Site 404s after green deploy | Wait 1–2 min for CDN propagation; hard-refresh (Ctrl+Shift+R) |
| Styles look broken on a deep link of the 404 page | Shouldn't happen — stylesheet is absolute (`/shaiinarab/assets/style.css`) |
| Workflow doesn't trigger | Confirm `.github/workflows/deploy-pages.yml` exists on `main` and Actions aren't disabled (Settings → Actions) |
| Old version cached | GitHub Pages CDN caches ~10 min max; browser cache: hard refresh |
