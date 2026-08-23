# Deferred Work

- source_spec: docs/implementation-artifacts/spec-hub-perfection-pass.md
  summary: RESOLVED — og:image now uses the permanent GitHub avatar CDN instead of capsule-render.
  evidence: index.html og:image/twitter:image updated; verified by scripts/verify.mjs consistency checks.

- source_spec: docs/implementation-artifacts/spec-hub-perfection-pass.md
  summary: OPEN — decide whether _bmad/ and .claude/ scaffolding ships in the repo/Pages artifact.
  evidence: upload-pages-artifact path "." includes them; harmless publicly but adds deploy weight (~MBs).
