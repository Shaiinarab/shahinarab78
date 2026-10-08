#!/usr/bin/env python3
"""Keep the hub's offline artifacts in sync with the live GitHub API.

Uses GITHUB_PAT from the environment (required) so requests run at the
authenticated 5000 req/hr rate limit instead of the unauthenticated 60/hr,
and never writes the token anywhere — it is only sent as a request header.

What it refreshes:
  1. FALLBACK_REPOS in assets/app.js — the built-in snapshot shown when the
     visitor's browser is offline or rate-limited. Regenerated from
     GET /users/<USER>/repos (forks and the hub repo itself excluded).
  2. <lastmod> in sitemap.xml — bumped to today when the site files change.

Run locally:   GITHUB_PAT=ghp_xxx python3 scripts/refresh-snapshot.py [--dry-run]
In CI:         called by .github/workflows/deploy-pages.yml before deploy.

Exit codes: 0 = done (changed or not), 1 = API/config failure.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP_JS = ROOT / "assets" / "app.js"
SITEMAP = ROOT / "sitemap.xml"

API_VERSION = "2022-11-28"  # stable GitHub REST API version


def die(msg: str) -> "NoReturn":  # noqa: F821
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def gh_get(url: str, pat: str) -> tuple[bytes, dict[str, str]]:
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {pat}",  # GITHUB_PAT stays in memory only
            "X-GitHub-Api-Version": API_VERSION,
            "User-Agent": "shaiinarab-hub-refresh",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            return res.read(), {k.lower(): v for k, v in res.headers.items()}
    except Exception as e:  # URLError, HTTPError, timeout
        die(f"GET {url} failed: {e}")


def fetch_repos(user: str, pat: str) -> list[dict]:
    """Walk Link-header pagination; same strategy as the site's own JS."""
    repos: list[dict] = []
    url: str | None = f"https://api.github.com/users/{user}/repos?per_page=100&sort=pushed"
    pages = 0
    while url and pages < 10:  # guard against pathological loops
        body, headers = gh_get(url, pat)
        repos.extend(json.loads(body))
        link = headers.get("link", "")
        m = re.search(r'<([^>]+)>;\s*rel="next"', link)
        url = m.group(1) if m else None
        pages += 1
    remaining = headers.get("x-ratelimit-remaining", "?")
    print(f"fetched {len(repos)} repos over {pages} page(s) · ratelimit remaining: {remaining}")
    return repos


def js_str(value: str | None) -> str:
    if value is None:
        return "null"
    return json.dumps(value, ensure_ascii=False)


def render_snapshot(repos: list[dict], user: str, self_repo: str) -> str:
    lines = [
        "  // Offline / rate-limited snapshot — regenerated from the live GitHub API by",
        f"  // `python3 scripts/refresh-snapshot.py` (uses GITHUB_PAT; CI keeps it fresh).",
        "  const FALLBACK_REPOS = [",
    ]
    kept = [r for r in repos if not r["fork"] and r["name"] != self_repo]
    for r in kept:
        fields = [
            f'name: {js_str(r["name"])}',
            f'description: {js_str(r.get("description"))}',
            f'language: {js_str(r.get("language"))}',
            f'html_url: {js_str(r["html_url"])}',
            f'stargazers_count: {int(r.get("stargazers_count", 0))}',
            f'forks_count: {int(r.get("forks_count", 0))}',
            f'archived: {"true" if r.get("archived") else "false"}',
        ]
        if r.get("homepage"):
            fields.append(f'homepage: {js_str(r["homepage"])}')
        lines.append("    { " + ", ".join(fields) + " },")
    lines.append("  ];")
    if not kept:
        die("API returned zero non-fork repos — refusing to blank the snapshot")
    return "\n".join(lines)


def patch_app_js(new_block: str) -> bool:
    src = APP_JS.read_text(encoding="utf-8")
    pattern = re.compile(r"  // Offline / rate-limited snapshot.*?\n  \];", re.S)
    if not pattern.search(src):
        die("could not locate the FALLBACK_REPOS block in assets/app.js")
    updated = pattern.sub(lambda _m: new_block, src, count=1)
    if updated == src:
        return False
    APP_JS.write_text(updated, encoding="utf-8")
    return True


def bump_sitemap() -> bool:
    xml = SITEMAP.read_text(encoding="utf-8")
    today = date.today().isoformat()
    updated = re.sub(r"<lastmod>\d{4}-\d{2}-\d{2}</lastmod>", f"<lastmod>{today}</lastmod>", xml)
    if updated == xml:
        return False
    SITEMAP.write_text(updated, encoding="utf-8")
    return True


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="print what would change, write nothing")
    args = ap.parse_args()

    pat = os.environ.get("GITHUB_PAT")
    if not pat:
        die("GITHUB_PAT is not set in the environment — this script requires it")

    src = APP_JS.read_text(encoding="utf-8")
    user = re.search(r'const USER = "([^"]+)"', src)
    self_repo = re.search(r'const SELF_REPO = "([^"]+)"', src)
    if not (user and self_repo):
        die(f"cannot read USER/SELF_REPO constants from {APP_JS}")

    repos = fetch_repos(user.group(1), pat)
    block = render_snapshot(repos, user.group(1), self_repo.group(1))

    if args.dry_run:
        changed = block not in src
        print(f"dry-run: snapshot {'WOULD CHANGE' if changed else 'already current'}")
        return

    if patch_app_js(block):
        print("updated: assets/app.js FALLBACK_REPOS")
    else:
        print("unchanged: assets/app.js")

    if bump_sitemap():
        print("updated: sitemap.xml lastmod")
    else:
        print("unchanged: sitemap.xml")


if __name__ == "__main__":
    main()
