# Saved Reviewer Prompts (subagent-unavailable fallback)

This environment cannot spawn subagents. Per bmad-build step-04, the exact child
prompts are preserved here so each layer can be re-run externally in a fresh session.

To re-run: open a NEW session with an LLM of your choice, paste one block below plus
the CONTENT (the diff/files under docs/implementation-artifacts/review-content.md),
and paste the result back into the main session.

---

## Layer 1 — Blind Hunter

Conduct a review of CONTENT.
Look for what's missing, not only what's wrong.
Find at least ten issues to fix or improve.
Output a Markdown list of findings only — no severity, priority, or ranking.
If the content is empty, stop and say so.
If you have zero findings, re-check and keep thinking; do not stop with an empty list.

CONTENT:
The changed files in the current worktree since baseline 537d817:
index.html, assets/app.js, assets/style.css, README.md,
404.html, robots.txt, sitemap.xml, .github/workflows/deploy-pages.yml

Do not invoke any skill. Return only the review result.

---

## Layer 2 — Edge Case Hunter

Read `_bmad/render/bmad-build/**/review-prompts/edge-case-hunter.md` completely and
follow it as your review instructions (exhaustive path enumeration, JSON-array output).

Review content:
The changed files listed above.

Do not invoke any skill. Return only the review result.

---

## Layer 3 — Verification Gap Reviewer

Read `_bmad/render/bmad-build/**/review-prompts/verification-gap.md` completely and
follow it as your review instructions (changed-behavior vs verification tracing).

Review content:
The changed files listed above.

Do not invoke any skill. Return only the review result.
