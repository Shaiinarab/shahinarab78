#!/usr/bin/env node
// Repeatable verification battery for the static hub. Node built-ins only.
// Run: node scripts/verify.mjs   → exit 0 green / 1 red.
import { readFileSync, statSync } from "node:fs";

const CANON = "https://shaiinarab.github.io/shaiinarab/";
const failures = [];

function check(id, ok, detail = "") {
  const mark = ok ? "PASS" : "FAIL";
  console.log(`${mark}  ${id}${detail ? ` — ${detail}` : ""}`);
  if (!ok) failures.push(id);
}

const read = (p) => readFileSync(new URL(`../${p}`, import.meta.url), "utf8");

let index, notFound, robots, sitemap, workflow, appJs, readme, css;
try {
  index = read("index.html");
  notFound = read("404.html");
  robots = read("robots.txt");
  sitemap = read("sitemap.xml");
  workflow = read(".github/workflows/deploy-pages.yml");
  appJs = read("assets/app.js");
  readme = read("README.md");
  css = read("assets/style.css");
} catch (e) {
  console.error("FAIL  fixture-load —", e.message);
  process.exit(1);
}

/* ---- index.html ---- */
for (const id of ["repo-grid", "lang-chips", "repo-search", "result-line", "api-note", "retry-btn", "typed", "year"]) {
  check(`index:#${id}`, index.includes(`id="${id}"`));
}
check("index:canonical", index.includes(`<link rel="canonical" href="${CANON}">`));
check("index:preconnect-api", index.includes('rel="preconnect" href="https://api.github.com"'));
check("index:search-aria-label", /id="repo-search"[^>]*aria-label=/.test(index));
check("index:no-status-on-terminal", !/<pre class="term-body mono" role="status"/.test(index));

let jsonldOk = false;
try {
  const m = index.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/);
  JSON.parse(m[1]);
  jsonldOk = true;
} catch { /* red */ }
check("index:jsonld-parses", jsonldOk);

/* ---- 404.html ---- */
check("404:absolute-stylesheet", notFound.includes('href="/shaiinarab/assets/style.css"'));
check("404:no-root-relative-links", !/\bhref="\/"(?!shaiinarab)/.test(notFound));
check("404:canonical-back-link", notFound.includes('href="/shaiinarab/"'));

/* ---- crawler files ---- */
check("robots:sitemap-matches-canon", robots.trim().endsWith(`Sitemap: ${CANON}sitemap.xml`));
check("sitemap:loc-is-canonical", sitemap.includes(`<loc>${CANON}</loc>`));
check("sitemap:lastmod-present", /<lastmod>\d{4}-\d{2}-\d{2}<\/lastmod>/.test(sitemap));

/* ---- consistency across surfaces ---- */
const canonInIndex = index.match(/<link rel="canonical" href="([^"]+)"/)?.[1];
const locInSitemap = sitemap.match(/<loc>([^<]+)<\/loc>/)?.[1];
check("consistency:canon-equals-sitemap", !!canonInIndex && canonInIndex === locInSitemap);

/* ---- deploy workflow ---- */
check("workflow:deploy-pages-v4", workflow.includes("actions/deploy-pages@v4"));
check("workflow:triggers-main", /branches:\s*(\n\s*-\s*|\[)\s*main/.test(workflow));
check("workflow:pages-write-perm", workflow.includes("pages: write"));

/* ---- directory engine hygiene ---- */
check("appjs:esc-used-for-html-injection", /(?:function esc\(|const esc = \()/u.test(appJs) && /\$\{esc\(r\.name\)\}/.test(appJs));
check("appjs:fallback-snapshot-exists", appJs.includes("FALLBACK_REPOS"));
check("appjs:timeout-guard", appJs.includes("AbortSignal.timeout"));
check("appjs:noreferrer-on-cards", appJs.includes('rel="noopener noreferrer"'));

/* ---- deploy hygiene: ship the site, not the workshop ---- */
check("workflow:verify-gate-before-deploy", workflow.includes("node scripts/verify.mjs"));
check("workflow:stages-site-dir", /path:\s*_site/.test(workflow));
check("workflow:no-whole-repo-upload", !/path:\s*\.\s*$/m.test(workflow));

/* ---- README widget correctness (the account is Shaiinarab) ---- */
const widgetUsers = [...readme.matchAll(/(?:username|user)=([A-Za-z0-9-]+)/g)].map((m) => m[1]);
const chartUsers = [...readme.matchAll(/ghchart\.rshah\.org\/[0-9a-f]+\/([A-Za-z0-9-]+)/g)].map((m) => m[1]);
const wrongUsers = [...widgetUsers, ...chartUsers].filter((u) => u.toLowerCase() !== "shaiinarab");
check(
  "readme:all-widgets-target-the-account",
  widgetUsers.length >= 4 && wrongUsers.length === 0,
  `${widgetUsers.length + chartUsers.length} widgets${wrongUsers.length ? ` — wrong: ${wrongUsers.join(",")}` : ""}`
);
check("readme:stats-use-real-account", readme.includes("username=Shaiinarab") && readme.includes("user=Shaiinarab") && readme.includes("ghchart.rshah.org/ff0080/Shaiinarab"));
check("readme:no-deprecated-hosts", !/readme-typing-svg\.herokuapp\.com|github-readme-streak-stats\.herokuapp\.com|github-profile-trophy\.vercel\.app/.test(readme));
check("readme:flow-diagram-linked", readme.includes("assets/hub-flow.svg"));
check("readme:widgets-have-alt-text", !/<img(?![^>]*\balt=)[^>]*>/i.test(readme));

/* ---- UI hardening ---- */
check("index:skip-link", index.includes('class="skip-link"'));
check("index:noscript-fallback", index.includes("<noscript>"));
check("index:token-hero-not-gradient-text", index.includes('class="tok"') && !index.includes('class="grad"'));
check("index:status-feed-not-card-grid", index.includes('class="feed"') && !index.includes("demo-card"));
check("index:colophon-diagram", index.includes('id="colophon"') && index.includes("assets/hub-flow.svg"));
check("index:og-self-hosted", index.includes("assets/og.png") && index.includes('property="og:image:width"'));
check("css:scroll-padding-for-sticky-nav", css.includes("scroll-padding-top"));
check("css:type-tokens", css.includes("--text-body") && css.includes("--text-display") && css.includes("--ease-out"));
check("css:no-unloaded-inter", !/--sans:\s*Inter,/.test(css));
check("css:tabular-numerals", css.includes("tabular-nums"));
check("css:prefers-contrast", css.includes("prefers-contrast: more"));
check("appjs:snapshot-cache", appJs.includes("hub:snapshot:v1") && appJs.includes("localStorage"));
check("appjs:shareable-filter-state", appJs.includes("history.replaceState"));

/* ---- shipped assets ---- */
for (const asset of ["assets/og.png", "assets/hub-flow.svg"]) {
  try {
    const st = statSync(new URL(`../${asset}`, import.meta.url));
    check(`asset:${asset}`, st.size > 500, `${st.size} bytes`);
  } catch {
    check(`asset:${asset}`, false, "missing");
  }
}

console.log(failures.length ? `\nRED — ${failures.length} failing` : "\nGREEN — all checks passing");
process.exit(failures.length ? 1 : 0);
