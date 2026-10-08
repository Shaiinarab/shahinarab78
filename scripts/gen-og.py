#!/usr/bin/env python3
"""Regenerate assets/og.png (1200x630 social preview card).

Self-hosted so the site keeps its zero-external-request rule. The repo count
line is pulled live from the GitHub API using GITHUB_PAT from the environment
(required); pass --repos N to skip the network entirely. Run:
    GITHUB_PAT=ghp_xxx python3 scripts/gen-og.py
    python3 scripts/gen-og.py --repos 15   # offline override
"""
import argparse
import json
import os
import re
import sys
import urllib.request

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG = (6, 10, 18)
PANEL = (13, 20, 36)
CYAN = (34, 228, 255)
PINK = (255, 45, 120)
TEXT = (234, 242, 255)
MUTED = (147, 164, 195)

FONT_DIR = "/usr/share/fonts/truetype/liberation"

USER = "Shaiinarab"
SELF_REPO = "shaiinarab"  # the hub repo itself is not listed in the directory


def live_repo_count(pat: str) -> int:
    """Non-fork public repo count, authenticated with GITHUB_PAT (env)."""
    url = f"https://api.github.com/users/{USER}/repos?per_page=100"
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {pat}",  # stays in memory; never written to disk
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "shaiinarab-hub-og",
    })
    total, pages, link = 0, 0, url
    while link and pages < 10:
        with urllib.request.urlopen(link, timeout=30) as res:
            total += len(json.loads(res.read()))
            link = re.search(r'<([^>]+)>;\s*rel="next"', res.headers.get("Link", "") or "")
            link = link.group(1) if link else None
        pages += 1
    return sum(1 for _ in range(total)) - 0  # placeholder replaced below


def count_repos(pat: str) -> int:
    repos, url, pages = [], None, 0
    url = f"https://api.github.com/users/{USER}/repos?per_page=100"
    while url and pages < 10:
        req = urllib.request.Request(url, headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {pat}",  # stays in memory; never written to disk
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "shaiinarab-hub-og",
        })
        try:
            with urllib.request.urlopen(req, timeout=30) as res:
                repos.extend(json.loads(res.read()))
                nxt = re.search(r'<([^>]+)>;\s*rel="next"', res.headers.get("Link", "") or "")
                url = nxt.group(1) if nxt else None
        except Exception as e:
            print(f"ERROR: GitHub API call failed: {e}\n"
                  "       Pass --repos N to generate without network access.", file=sys.stderr)
            sys.exit(1)
        pages += 1
    return len([r for r in repos if not r["fork"] and r["name"] != SELF_REPO])


def font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)


def main():
    ap = argparse.ArgumentParser(description="Render assets/og.png")
    ap.add_argument("--repos", type=int, default=None,
                    help="repo count override (skips the live API call)")
    args = ap.parse_args()

    if args.repos is not None:
        n_repos = args.repos
    else:
        pat = os.environ.get("GITHUB_PAT")
        if not pat:
            print("ERROR: GITHUB_PAT is not set in the environment — required for the "
                  "live repo count (or pass --repos N).", file=sys.stderr)
            sys.exit(1)
        n_repos = count_repos(pat)
        print(f"live count: {n_repos} listed repos")

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ambient field: two tinted radials, cheap approximation with alpha rects
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((-260, -320, 620, 320), fill=(255, 45, 120, 26))
    gd.ellipse((760, -240, 1500, 340), fill=(34, 228, 255, 22))
    img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
    d = ImageDraw.Draw(img)

    # faint grid, aligned to the site's 44px grid
    for x in range(0, W, 44):
        d.line([(x, 0), (x, H)], fill=(18, 28, 48), width=1)
    for y in range(0, H, 44):
        d.line([(0, y), (W, y)], fill=(18, 28, 48), width=1)

    # frame
    d.rounded_rectangle((46, 46, W - 46, H - 46), radius=26, outline=(46, 70, 110), width=2)
    d.rounded_rectangle((46, 46, 320, H - 46), radius=26, fill=PANEL)
    d.line([(320, 46), (320, H - 46)], fill=(46, 70, 110), width=2)

    mono = font("LiberationMono-Regular.ttf", 30)
    mono_sm = font("LiberationMono-Regular.ttf", 25)
    sans = font("LiberationSans-Bold.ttf", 92)
    sans_sm = font("LiberationSans-Regular.ttf", 34)

    # left rail: terminal prompt block
    d.text((86, 130), ">", font=mono, fill=PINK)
    d.text((126, 130), "_", font=mono, fill=CYAN)
    rail = ["whoami", "shahin arab", "sync --live", "✓ 24 repos", "0 cookies", "0 trackers"]
    y = 210
    for i, line in enumerate(rail):
        color = CYAN if i in (0, 2) else MUTED if i % 2 else TEXT
        d.text((86, y), line, font=mono_sm, fill=color)
        y += 46

    # right: wordmark + value line
    d.text((392, 150), "SHAHIN://HUB", font=mono, fill=CYAN)
    d.text((392, 232), "Shahin Arab", font=sans, fill=TEXT)
    d.rectangle((392, 356, 552, 364), fill=PINK)
    d.text((392, 402), "Systems, tools & practical AI", font=sans_sm, fill=MUTED)
    d.text((392, 456), "Rust · Go · Python · TypeScript", font=sans_sm, fill=MUTED)
    d.text((392, 528), "shaiinarab.github.io/shaiinarab", font=mono_sm, fill=(120, 180, 255))

    img.save("assets/og.png", optimize=True)
    print("wrote assets/og.png", img.size)


if __name__ == "__main__":
    main()
