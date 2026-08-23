#!/usr/bin/env node
// Repeatable verification battery for the static hub. Node built-ins only.
// Run: node scripts/verify.mjs   → exit 0 green / 1 red.
import { readFileSync } from "node:fs";

const CANON = "https://shaiinarab.github.io/shahinarab78/";
const failures = [];

function check(id, ok, detail = "") {
  const mark = ok ? "PASS" : "FAIL";
  console.log(`${mark}  ${id}${detail ? ` — ${detail}` : ""}`);
  if (!ok) failures.push(id);
}

const read = (p) => readFileSync(new URL(`../${p}`, import.meta.url), "utf8");

let index, notFound, robots, sitemap, workflow, appJs;
try {
  index = read("index.html");
  notFound = read("404.html");
  robots = read("robots.txt");
  sitemap = read("sitemap.xml");
  workflow = read(".github/workflows/deploy-pages.yml");
  appJs = read("assets/app.js");
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
check("404:absolute-stylesheet", notFound.includes('href="/shahinarab78/assets/style.css"'));
check("404:no-root-relative-links", !/\bhref="\/"(?!shahinarab78)/.test(notFound));
check("404:canonical-back-link", notFound.includes('href="/shahinarab78/"'));

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

console.log(failures.length ? `\nRED — ${failures.length} failing` : "\nGREEN — all checks passing");
process.exit(failures.length ? 1 : 0);
