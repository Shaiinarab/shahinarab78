---
title: 'Hub Perfection Pass — harden the GitHub Pages repo hub'
type: 'feature'
created: '2026-08-23'
status: 'done'
review_loop_iteration: 0
baseline_commit: '537d817'
context:
  - '{project-root}/index.html'
  - '{project-root}/assets/app.js'
  - '{project-root}/assets/style.css'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The hub site from the previous run works, but it is not production-perfect: broken/missing 404 handling, no crawler files, avoidable API latency, an over-broadcasting ARIA live region, and several unhandled edge cases (stale language filter after resync, repos beyond page 1, links without `noreferrer`).

**Approach:** One cohesive hardening pass over the static site only — add GitHub Pages platform files (404, robots, sitemap), tighten SEO head tags, and patch real edge cases in the directory engine. No redesign, no new features, no build tooling.

## Boundaries & Constraints

**Always:** Keep the site zero-dependency (no frameworks, no external fonts); keep all user-visible copy in English; escape every string interpolated into HTML from the GitHub API; respect `prefers-reduced-motion`.

**Ask First:** Any change that alters the visual identity of the hub; any new third-party service or analytics.

**Never:** No commit or push (Freebuff Changes panel owns delivery). No changes to `.github/workflows/deploy-pages.yml` behavior. Do not add a package.json/build step to this repo.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| API success | `api.github.com` reachable | Live repo grid + chips render; stats filled; sync line shows ✓ time | N/A |
| Rate limited / network fail | fetch rejects or HTTP ≥ 400 | Fallback snapshot renders; amber notice + Retry visible; sync line shows ⚠ offline snapshot | Notice dismissible via successful retry |
| Forks & self repo | API returns fork entries + `shaiinarab` | Excluded from directory grid | N/A |
| Archived repo | `archived: true` in payload | Dimmed card with ARCHIVED badge | N/A |
| Search miss | Query matches nothing | Single empty-state message, no crash | N/A |
| Stale chip filter | Active language vanishes after resync | Filter resets to All so grid never stays empty from stale state | N/A |
| >100 public repos | Paginated API response | Directory follows pagination until exhausted (cap 3 pages as guard) | Stops at cap silently |
| Reduced motion | OS setting on | No typing loop, caret blink, pulse, shimmer; reveals instant | N/A |

</frozen-after-approval>

## Code Map

- `index.html` -- single-page hub markup; `<head>` holds SEO/meta; hero terminal pre carries `role="status"` (to be narrowed); search input lacks programmatic label.
- `assets/app.js` -- directory engine: `load()` fetches user+repos (single page), `renderChips()`/`renderGrid()`, fallback snapshot `FALLBACK_REPOS`, typing/reveal init.
- `assets/style.css` -- theme tokens + components; one malformed duplicate selector near `.feat-card h3 .arrow`; no sr-only utility needed.
- `.github/workflows/deploy-pages.yml` -- uploads repo root as Pages artifact (read-only constraint: leave behavior untouched).
- Missing entirely: `404.html`, `robots.txt`, `sitemap.xml` (Pages serves these automatically when present).

## Tasks & Acceptance

**Execution:**
- [x] `404.html` -- create themed not-found page reusing `assets/style.css` with its own compact layout block -- GitHub Pages serves this for unknown paths.
- [x] `robots.txt` -- allow all, point to sitemap -- crawler correctness.
- [x] `sitemap.xml` -- list canonical hub URL only -- correct lastmod/date.
- [x] `index.html` -- add `preconnect`+`dns-prefetch` for api.github.com, `og:site_name`, `og:locale`, `aria-label` on search input, drop `role="status"` from terminal pre -- perf + a11y + OG polish.
- [x] `assets/app.js` -- follow Link-header pagination (≤3 pages); reset `activeLang` if missing after resync; add `rel="noopener noreferrer"` to JS-built external link -- robustness.
- [x] `assets/style.css` -- fix duplicated arrow selector into one clean rule -- hygiene.

**Acceptance Criteria:**
- Given a fresh visit with the API up, when the directory loads, then live repos render with chips and stats within one request pair (no waterfall).
- Given any fetch failure, when rendering completes, then the fallback snapshot is visible together with the retry notice.
- Given `/nonexistent-path` on the Pages origin, when requested, then the themed 404 page renders with working nav home.
- Given `node --check assets/app.js`, then exit code 0.

## Spec Change Log

- 2026-08-23 review loop (iteration 1): blind-hunter + edge-case-hunter surfaced two HIGH defects — relative stylesheet/nav hrefs on 404.html break because GitHub Pages serves the 404 document at every missing path depth, and "/" resolves to the account origin root rather than this project site. Amended to absolute /shaiinarab/ paths. Known-bad state avoided: unstyled, dead-end error page on deep links. KEEP: absolute-path strategy on any future 404/platform pages. Additional patches: fetch timeout guard (12s) prevents infinite skeleton state; decorative terminal cursor aria-hidden. Deferred: og:image external dependency; whether _bmad/.claude scaffolding should ship in the Pages artifact (human decision).
- 2026-08-23 process note: Checkpoint 1 approval delegated by user directive ("use them to continue this run to perfection"); proceeding [A]. VCS dirty-tree continuity accepted — the uncommitted hub IS the subject intent. KEEP: existing visual identity, zero-dependency constraint.

## Verification

**Commands:**
- `node --check assets/app.js` -- expected: silent success
- `python3 - <<'PY' ...` HTML parse of index.html + 404.html -- expected: no parse errors (well-formed)
- `grep -c 'data-stat' index.html` -- expected: 4 stat slots intact

**Manual checks (if no CLI):**
- 404 page visually consistent (dark bg, neon accents) and its "back to hub" link targets the canonical URL.

## Suggested Review Order

**Directory engine robustness**

- Pagination + timeout guard: Link-header walk with 3-page cap, 12s abort per request
  [`app.js:195`](../../assets/app.js#L195)

- Stale language chip can never silently empty the grid after a resync
  [`app.js:214`](../../assets/app.js#L214)

- Both fetch sites route through the same signal helper
  [`app.js:211`](../../assets/app.js#L211)

**Platform correctness (404 under project Pages)**

- Absolute asset path — the 404 document renders at *any* missing depth
  [`404.html:11`](../../404.html#L11)

- Hub-root links use /shaiinarab/, not "/", which is the account origin
  [`404.html:24`](../../404.html#L24)

**Perf + accessibility polish**

- API connection warmed before JS boots; no request waterfall
  [`index.html:26`](../../index.html#L26)

- Search input now has a programmatic accessible name
  [`index.html:163`](../../index.html#L163)

- Decorative terminal cursor hidden from assistive tech
  [`index.html:99`](../../index.html#L99)

**Crawler files & hygiene (peripherals)**

- [robots.txt](../../robots.txt) · [sitemap.xml](../../sitemap.xml) — canonical URLs only

- Generated BMAD render snapshots kept out of version control
  [.gitignore:2](../../.gitignore#L2)

## Spec Change Log

- 2026-08-23 dev pass 2 (Amelia): resolved defer "og:image external dependency" — switched to GitHub avatar CDN (`avatars.githubusercontent.com/u/211481146`) and added missing `twitter:image`; capsule-render dependency eliminated. Added `scripts/verify.mjs` (27 checks, node built-ins only) as repeatable red/green battery; live-API smoke test confirmed HTTP 200 + no Link header → pagination loop exits page 1 as designed. Two initial REDs were test defects (flow-style `branches: [main]`, arrow-const `esc`), not product defects — fixed the checks. Known-bad state avoided: editing product code to satisfy a wrong assertion. KEEP: verify.mjs must stay dependency-free and exit non-zero on any failure.
