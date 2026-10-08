/* ============================================================
   SHAHIN://HUB — live GitHub directory
   Fetches public repos from api.github.com (unauthenticated),
   renders a searchable/filterable grid, falls back to a local
   snapshot when the API is unreachable or rate-limited.
   ============================================================ */
"use strict";

(() => {
  const USER = "Shaiinarab";
  const SELF_REPO = "shahinarab78"; // this site's own repo — not listed in the directory

  /* ---------- static data ---------- */

  const LANG_COLORS = {
    Rust: "#dea584", Zig: "#ec915c", Go: "#00ADD8", Python: "#3572A5",
    TypeScript: "#3178c6", JavaScript: "#f1e05a", HTML: "#e34c26",
    CSS: "#563d7c", Shell: "#89e051", C: "#555555", "C++": "#f34b7d",
    Java: "#b07219", Kotlin: "#A97BFF", Swift: "#F05138", Ruby: "#701516",
    PHP: "#4F5D95", Lua: "#000080", Dart: "#00B4AB", Nix: "#7ad3d4",
  };

  // Offline / rate-limited snapshot (kept roughly current with the account).
  const FALLBACK_REPOS = [
    { name: "portfolio-context", description: "Minimal public-safe portfolio context API on Cloudflare Workers.", language: "JavaScript", html_url: "https://github.com/Shaiinarab/portfolio-context", stargazers_count: 0, forks_count: 0, archived: false },
    { name: "repopulse", description: "Signed GitHub-webhook activity signal with a privacy-filtered public status feed.", language: "TypeScript", html_url: "https://github.com/Shaiinarab/repopulse", stargazers_count: 0, forks_count: 0, archived: false, homepage: "https://repopulse.shahino3ozone1353.workers.dev/status" },
    { name: "Simorgh-edge-gateway", description: "Agentic edge gateway for resilient AI-provider federation on Cloudflare Workers.", language: "TypeScript", html_url: "https://github.com/Shaiinarab/Simorgh-edge-gateway", stargazers_count: 0, forks_count: 0, archived: false },
    { name: "Data_Structure_And_Intro_To_Algorithms.CLRS", description: "Python mini-homework solutions for a Data Structures and Algorithms course.", language: "Python", html_url: "https://github.com/Shaiinarab/Data_Structure_And_Intro_To_Algorithms.CLRS", stargazers_count: 0, forks_count: 0, archived: false },
    { name: "Data-struct-and-intro-to-algo-final-project", description: "Queue and stack simulations in Python, with CLI and Tkinter interfaces.", language: "Python", html_url: "https://github.com/Shaiinarab/Data-struct-and-intro-to-algo-final-project", stargazers_count: 0, forks_count: 0, archived: false },
    { name: "mashreghi_asil", description: "Full-stack luxury perfume e-commerce platform built with Next.js, Rust, and WebAssembly.", language: "TypeScript", html_url: "https://github.com/Shaiinarab/mashreghi_asil", stargazers_count: 0, forks_count: 0, archived: false },
    { name: "Log-Sentinel", description: "Python command-line tool for ingesting and analyzing system and application log files.", language: "Python", html_url: "https://github.com/Shaiinarab/Log-Sentinel", stargazers_count: 0, forks_count: 0, archived: false },
    { name: "Falcons", description: "Resources and applications for the Falcon Persian-language project.", language: null, html_url: "https://github.com/Shaiinarab/Falcons", stargazers_count: 0, forks_count: 0, archived: false },
    { name: "Ararat-platform", description: "Unified management platform for FC Ararat Academy staff, players, and members in Shiraz, Iran.", language: "Go", html_url: "https://github.com/Shaiinarab/Ararat-platform", stargazers_count: 0, forks_count: 0, archived: false },
    { name: "shiraz-bazaar-telegram-bot", description: "Persian-first Telegram price bot with resilient tgju.org scraper, SQLite alerts, and automatic fallback — no cloud costs.", language: null, html_url: "https://github.com/Shaiinarab/shiraz-bazaar-telegram-bot", stargazers_count: 0, forks_count: 0, archived: false },
    { name: "Mashreghi-asil", description: "A website for a perfume online shop. (Superseded by mashreghi_asil.)", language: null, html_url: "https://github.com/Shaiinarab/Mashreghi-asil", stargazers_count: 0, forks_count: 0, archived: true },
    { name: "to-improve", description: "Notes and experiments for continuous improvement.", language: null, html_url: "https://github.com/Shaiinarab/to-improve", stargazers_count: 0, forks_count: 0, archived: true },
  ];

  const TYPED_PHRASES = [
    "Systems, tools & practical AI.",
    "Rust ⚙️ Go 🐹 Python 🐍 TypeScript ⚡",
    "Edge gateways · developer tooling · real users.",
    "Ship small. Verify everything. Repeat.",
  ];

  /* ---------- tiny helpers ---------- */

  const $ = (sel) => document.querySelector(sel);

  const esc = (s) =>
    String(s ?? "").replace(/[&<>"']/g, (c) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
    })[c]);

  const langColor = (lang) => LANG_COLORS[lang] || "#8b949e";

  function relTime(iso) {
    if (!iso) return "";
    const diff = Date.now() - new Date(iso).getTime();
    const units = [
      [31536000000, "year"], [2592000000, "month"], [604800000, "week"],
      [86400000, "day"], [3600000, "hour"], [60000, "minute"],
    ];
    for (const [ms, unit] of units) {
      if (Math.abs(diff) >= ms) {
        const v = Math.round(diff / ms);
        return `updated ${v} ${unit}${v !== 1 ? "s" : ""} ago`;
      }
    }
    return "updated just now";
  }

  const starIcon =
    '<svg viewBox="0 0 16 16" aria-hidden="true"><path fill="currentColor" d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.75.75 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Z"/></svg>';
  const forkIcon =
    '<svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="4" cy="3" r="1.7" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="12" cy="3" r="1.7" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="8" cy="13" r="1.7" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M4 4.9v.6c0 2 1.7 3 4 3s4-1 4-3v-.6" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>';

  /* ---------- state ---------- */

  const state = {
    user: null,
    repos: [],
    langs: ["All"],
    activeLang: "All",
    fromApi: false,
    cacheTime: null,
  };

  /* ---------- snapshot cache (offline fallback stays truthful) ---------- */

  const CACHE_KEY = "hub:snapshot:v1";

  function readCache() {
    try {
      const raw = localStorage.getItem(CACHE_KEY);
      if (!raw) return null;
      const parsed = JSON.parse(raw);
      return parsed && Array.isArray(parsed.repos) && parsed.repos.length ? parsed : null;
    } catch { return null; }
  }

  function writeCache(user, repos) {
    try {
      localStorage.setItem(CACHE_KEY, JSON.stringify({ t: Date.now(), user, repos }));
    } catch { /* private mode / quota — cache is optional */ }
  }

  /* ---------- DOM ---------- */

  const grid = $("#repo-grid");
  const chipsBox = $("#lang-chips");
  const searchInput = $("#repo-search");
  const resultLine = $("#result-line");
  const apiNote = $("#api-note");
  const retryBtn = $("#retry-btn");

  /* ---------- rendering ---------- */

  function showSkeletons() {
    grid.setAttribute("aria-busy", "true");
    grid.innerHTML = Array.from({ length: 8 }, () => '<div class="skel"></div>').join("");
    resultLine.textContent = "syncing with github…";
  }

  function repoCard(r) {
    const badges = [
      r.archived ? '<span class="badge-archived">ARCHIVED</span>' : "",
      r.homepage ? '<span class="badge-home">HAS LIVE DEMO</span>' : "",
    ].join(" ");
    return `
      <article class="repo-card${r.archived ? " is-archived" : ""}">
        <a href="${esc(r.html_url)}" target="_blank" rel="noopener noreferrer"
           aria-label="${esc(r.name)} on GitHub">
          <span class="repo-arrow" aria-hidden="true">↗</span>
          <h3 class="repo-name">${esc(r.name)} ${badges}</h3>
          <p class="repo-desc">${r.description ? esc(r.description) : '<span class="dim">No description yet.</span>'}</p>
          <div class="repo-meta">
            ${r.language ? `<span><span class="lang-dot" style="--lc:${langColor(r.language)}"></span>${esc(r.language)}</span>` : ""}
            <span class="mi">${starIcon}${r.stargazers_count}</span>
            <span class="mi">${forkIcon}${r.forks_count}</span>
            ${r.pushed_at ? `<span>${relTime(r.pushed_at)}</span>` : ""}
          </div>
        </a>
      </article>`;
  }

  function visibleRepos() {
    const q = searchInput.value.trim().toLowerCase();
    return state.repos.filter((r) => {
      if (state.activeLang !== "All" && r.language !== state.activeLang) return false;
      if (!q) return true;
      return `${r.name} ${r.description || ""}`.toLowerCase().includes(q);
    });
  }

  function renderGrid() {
    const items = visibleRepos();
    grid.setAttribute("aria-busy", "false");
    grid.innerHTML = items.length
      ? items.map(repoCard).join("")
      : `<p class="empty-state mono">⌁ no repositories match “${esc(searchInput.value)}” — try another signal.</p>`;
    resultLine.textContent = state.fromApi
      ? `${items.length} of ${state.repos.length} repositories shown`
      : state.cacheTime
        ? `${items.length} repositories · cached snapshot from ${new Date(state.cacheTime).toLocaleString()} — live sync unavailable`
        : `${items.length} repositories · built-in snapshot — live sync unavailable`;
    registerReveals(grid);
    writeUrlState();
  }

  function renderChips() {
    const counts = new Map();
    for (const r of state.repos) if (r.language) counts.set(r.language, (counts.get(r.language) || 0) + 1);
    state.langs = ["All", ...[...counts.entries()].sort((a, b) => b[1] - a[1]).map(([l]) => l)];
    chipsBox.innerHTML = state.langs
      .map((l) => `<button type="button" class="chip" data-lang="${esc(l)}" aria-pressed="${l === state.activeLang}">${esc(l)}${l === "All" ? "" : ` · ${counts.get(l)}`}</button>`)
      .join("");
  }

  /* ---------- stats + terminal slots ---------- */

  function fillStats(user, repos) {
    const set = (name, v) => { const el = document.querySelector(`[data-stat="${name}"]`); if (el) el.textContent = v; };
    const slot = (name, v) => { const el = document.querySelector(`[data-slot="${name}"]`); if (el) el.textContent = v; };
    const langs = new Set(repos.map((r) => r.language).filter(Boolean)).size;

    set("repos", user ? String(user.public_repos) : "—");
    set("listed", String(repos.length));
    set("langs", String(langs));
    set("followers", user ? String(user.followers) : "—");

    slot("repo-count", String(repos.length));
    const sync = document.querySelector('[data-slot="sync-status"]');
    if (sync) {
      sync.classList.remove("dim");
      sync.textContent = state.fromApi
        ? `✓ synced ${new Date().toLocaleTimeString()} · auto-refreshes on every visit`
        : state.cacheTime
          ? `⚠ cached snapshot · last live sync ${new Date(state.cacheTime).toLocaleString()}`
          : "⚠ offline snapshot · will retry next visit";
    }
  }

  /* ---------- data loading ---------- */

  async function getJson(res) {
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  }

  // Don't let a hanging connection pin the grid on skeletons forever.
  const reqSignal = () => (AbortSignal.timeout ? AbortSignal.timeout(12000) : undefined);

  // Follow the Link header so accounts with >100 public repos stay complete.
  function nextPageUrl(linkHeader) {
    if (!linkHeader) return null;
    const m = linkHeader.match(/<([^>]+)>;\s*rel="next"/);
    return m ? m[1] : null;
  }

  async function fetchAllRepos() {
    let url = `https://api.github.com/users/${USER}/repos?per_page=100&sort=pushed`;
    const all = [];
    for (let page = 0; page < 3 && url; page++) { // cap guards against pathological loops
      const res = await fetch(url, { headers: { Accept: "application/vnd.github+json" }, signal: reqSignal() });
      all.push(...(await getJson(res)));
      url = nextPageUrl(res.headers.get("Link"));
    }
    return all;
  }

  async function load() {
    showSkeletons();
    apiNote.hidden = true;
    try {
      const [userRes, repos] = await Promise.all([
        fetch(`https://api.github.com/users/${USER}`, { headers: { Accept: "application/vnd.github+json" }, signal: reqSignal() }),
        fetchAllRepos(),
      ]);
      const user = await getJson(userRes);
      state.user = user;
      state.repos = repos.filter((r) => !r.fork && r.name !== SELF_REPO);
      // A language chip that no longer exists would silently empty the grid.
      if (state.activeLang !== "All" && !state.repos.some((r) => r.language === state.activeLang)) {
        state.activeLang = "All";
      }
      state.fromApi = true;
      state.cacheTime = Date.now();
      writeCache(state.user, state.repos);
    } catch {
      const cache = readCache();
      state.user = cache?.user ?? null;
      state.repos = cache?.repos ?? FALLBACK_REPOS;
      state.fromApi = false;
      state.cacheTime = cache?.t ?? null;
      apiNote.hidden = false;
    }
    renderChips();
    renderGrid();
    fillStats(state.user, state.repos);
  }

  retryBtn.addEventListener("click", load);

  /* ---------- shareable filter state (?q=&lang=) ---------- */

  function readUrlState() {
    const p = new URLSearchParams(location.search);
    const q = p.get("q");
    const lang = p.get("lang");
    if (q) searchInput.value = q;
    if (lang) state.activeLang = lang;
  }

  function writeUrlState() {
    const p = new URLSearchParams(location.search);
    const q = searchInput.value.trim();
    if (q) p.set("q", q); else p.delete("q");
    if (state.activeLang && state.activeLang !== "All") p.set("lang", state.activeLang); else p.delete("lang");
    const qs = p.toString();
    history.replaceState(null, "", qs ? `?${qs}` : location.pathname);
  }

  /* ---------- filters ---------- */

  chipsBox.addEventListener("click", (e) => {
    const btn = e.target.closest(".chip");
    if (!btn) return;
    state.activeLang = btn.dataset.lang;
    for (const c of chipsBox.querySelectorAll(".chip")) c.setAttribute("aria-pressed", String(c === btn));
    renderGrid();
  });

  let searchTimer;
  searchInput.addEventListener("input", () => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(renderGrid, 120);
  });

  // Press "/" anywhere to jump to search.
  document.addEventListener("keydown", (e) => {
    if (e.key !== "/" || e.metaKey || e.ctrlKey || e.altKey) return;
    const t = e.target;
    if (t instanceof HTMLElement && (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.isContentEditable)) return;
    e.preventDefault();
    searchInput.focus();
  });

  /* ---------- hero typing effect ---------- */

  function initTyping() {
    const el = $("#typed");
    if (!el) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      el.textContent = TYPED_PHRASES[0];
      return;
    }
    let pi = 0, ci = 0, deleting = false;
    (function tick() {
      const phrase = TYPED_PHRASES[pi];
      ci += deleting ? -1 : 1;
      el.textContent = phrase.slice(0, ci);
      let delay = deleting ? 26 : 52;
      if (!deleting && ci === phrase.length) { delay = 2200; deleting = true; }
      else if (deleting && ci === 0) { deleting = false; pi = (pi + 1) % TYPED_PHRASES.length; delay = 420; }
      setTimeout(tick, delay);
    })();
  }

  /* ---------- reveal on scroll (staggered per group) ---------- */

  function registerReveals(root = document) {
    const els = [...root.querySelectorAll("[data-reveal]:not(.in)")];
    if (!els.length) return;
    if (!("IntersectionObserver" in window) ||
        window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      els.forEach((n) => n.classList.add("in"));
      return;
    }
    for (const n of els) {
      const group = [...(n.parentElement?.children || [n])].filter((c) => c.hasAttribute?.("data-reveal"));
      const idx = Math.max(0, group.indexOf(n));
      n.style.setProperty("--d", `${Math.min(idx, 7) * 80}ms`);
    }
    const io = new IntersectionObserver(
      (entries) => entries.forEach((en) => {
        if (!en.isIntersecting) return;
        en.target.classList.add("in");
        io.unobserve(en.target);
      }),
      { threshold: 0.05, rootMargin: "0px 0px 8% 0px" }
    );
    els.forEach((n) => io.observe(n));
  }

  /* ---------- nav: highlight the section being read ---------- */

  function initNavHighlight() {
    const links = [...document.querySelectorAll(".nav-links a")];
    const byId = new Map(links.map((a) => [a.getAttribute("href").slice(1), a]));
    const sections = [...byId.keys()].map((id) => document.getElementById(id)).filter(Boolean);
    if (!sections.length || !("IntersectionObserver" in window)) return;
    const io = new IntersectionObserver((entries) => {
      for (const en of entries) {
        if (!en.isIntersecting) continue;
        for (const a of links) a.removeAttribute("aria-current");
        byId.get(en.target.id)?.setAttribute("aria-current", "true");
      }
    }, { rootMargin: "-45% 0px -50% 0px" });
    sections.forEach((s) => io.observe(s));
  }

  /* ---------- boot ---------- */

  const yearEl = $("#year");
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());

  // "press /" is a keyboard affordance — hide it on touch devices
  if (window.matchMedia("(pointer: coarse)").matches) {
    searchInput.placeholder = "Search repositories…";
  }

  readUrlState();
  initTyping();
  registerReveals();
  initNavHighlight();
  load();
})();
