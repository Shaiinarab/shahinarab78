<!-- Cyberpunk Banner -->
<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:ff0080,100:00ffff&height=300&section=header&text=SHAHIN%20ARAB&fontSize=60&fontColor=ffffff&animation=twinkle&fontAlignY=35&font=Rubik+Glitch" alt="Cyberpunk Banner"/>
</div>

<h1 align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=20&duration=4000&pause=800&color=00ffff&center=true&vCenter=true&width=600&lines=🔮+Researcher+%7C+Open+Source+Enthusiast;⚡+Rust+%2B+Zig+%2B+Go+%2B+Python+%2B+Mojo;🐧+Linux+%7C+GPU+Computing+%7C+CUDA+%2F+OpenCL;🛡️+Cybersecurity+%7C+Hacking+Mindset;🎵+Music+Therapy+%7C+OS+Optimization" alt="Researcher and open source enthusiast. Rust, Zig, Go, Python and Mojo. Linux, GPU computing, CUDA and OpenCL. Cybersecurity with a hacking mindset. Music therapy and OS optimization."/>
</h1>

<p align="center">
  <a href="https://shaiinarab.github.io/shahinarab78/" target="_blank"><img src="https://img.shields.io/badge/%F0%9F%8C%90_ENTER_THE_HUB-shaiinarab.github.io%2Fshahinarab78-ff0080?style=for-the-badge&labelColor=0D1117" alt="Open the Repo Hub"/></a>
  <a href="https://github.com/Shaiinarab/shahinarab78/actions/workflows/deploy-pages.yml"><img src="https://img.shields.io/github/actions/workflow/status/Shaiinarab/shahinarab78/deploy-pages.yml?branch=main&style=flat-square&label=pages%20deploy" alt="Pages deploy status"/></a>
</p>

> 🗂️ **This repository is also my website** — a live repo hub that auto-syncs every public repository from the GitHub API: searchable, filterable, always current.

<details>
<summary><strong>⚙️ How this repo works</strong> — one page, one API, zero trackers</summary>
<br/>

<img src="assets/hub-flow.svg" alt="Data flow: the GitHub API feeds fetch and pagination, which feeds filter and sort, which renders repository cards with search and language chips. A local snapshot in the browser is the offline fallback."/>

- **`index.html` + `assets/`** — the hub itself. No build step, no framework, no cookies.
- **Live sync** — your browser calls the GitHub API on every visit; new repos appear without a redeploy. Rate-limited or offline? A cached snapshot from your last visit takes over.
- **Privacy by construction** — public data only, forks and this repo filtered out, nothing stored on a server.
- **Deploy** — every push to `main` ships the site files to GitHub Pages via `.github/workflows/deploy-pages.yml`.

</details>

---

## 🌑 **THE ARCHITECT** 

```rust
mod shahin_arab {
    pub struct Human {
        pub location: &'static str,        // "Shiraz, Iran 🇮🇷"
        pub archetype: &'static str,       // "INTP • AuDHD • Eternal Student"
        pub languages: Vec<&'static str>,  // ["Persian", "English"]
        pub passion_stack: Vec<&'static str>,
        pub mission: &'static str,
    }

    impl Human {
        pub fn new() -> Self {
            Self {
                location: "Shiraz, Iran 🇮🇷",
                archetype: "INTP • AuDHD • Eternal Student",
                languages: vec!["Persian 🔱", "English 🦅"],
                passion_stack: vec![
                    "Rust 🦀", "Zig ⚡", "Go 🐹", "Python 🐍", "Mojo 🔥",
                    "Linux 🐧", "GPU Computing 🎮", "CUDA/OpenCL",
                    "Cybersecurity 🛡️", "OS Optimization ⚙️"
                ],
                mission: "💰 Make money → Buy freedom → Transcend limits",
            }
        }

        pub fn mantra(&self) -> &'static str {
            "🌌 Even the sky is not a limit... YOU are the limit."
        }

        pub fn vibe(&self) -> &'static str {
            "🌃 Cyberpunk • Neon • Dark Symbolism • Occult Aesthetic"
        }
    }
}
```

> *"Let's not talk. Share music and feelings."* 🎧🖤

---

## 🔮 **CURRENT QUESTS**

| # | Project | Description | Stack |
|---|---------|-------------|-------|
| **01** | **[Oduverse → mashreghi_asil](https://github.com/Shaiinarab/mashreghi_asil)** | 🌸 E-commerce perfume online shop | Next.js + Rust + WASM |
| **02** | **NeuroSymphonia** | 🎵 Music-based therapeutic rhythmic mobile game | Healing through rhythm & code |
| **03** | **Nimrooz VPN** | 🛡️ Rust-based VPN client for all protocols | Freedom through encryption |
| **04** | **Music Sanctuary** | 🎼 Real Rap • EDM • Nu-Metal • Jazz • Iranian Folklore | The soundtrack of my soul |

---

## ⚗️ **ALCHEMY & SUBSTANCES**

<div align="center">

| ☕ | 🌿 | 🍄 |
|----|----|----|
| **Arabica Coffee** | **Sativa Cannabis** | **Psilocybin Mushrooms** |
| *Fuel for the mind* | *Creative expansion* | *Consciousness exploration* |

</div>

---

## 🛠️ **TECH ARSENAL**

<p align="center">
  <strong>⚔️ Languages of Power:</strong><br/>
  <img src="https://img.shields.io/badge/Rust-000000?style=for-the-badge&logo=rust&logoColor=white" alt="Rust"/>
  <img src="https://img.shields.io/badge/Zig-F7A41D?style=for-the-badge&logo=zig&logoColor=black" alt="Zig"/>
  <img src="https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white" alt="Go"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Mojo-EA832A?style=for-the-badge&logo=mojo&logoColor=white" alt="Mojo"/>
  
  <br/><br/>
  
  <strong>🐧 Operating Systems & Infrastructure:</strong><br/>
  <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" alt="Linux"/>
  <img src="https://img.shields.io/badge/CUDA-76B900?style=for-the-badge&logo=nvidia&logoColor=white" alt="CUDA"/>
  <img src="https://img.shields.io/badge/OpenCL-000000?style=for-the-badge&logo=opencl&logoColor=white" alt="OpenCL"/>
  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" alt="Git"/>
  
  <br/><br/>
  
  <strong>🛡️ Security & Research:</strong><br/>
  <img src="https://img.shields.io/badge/Cybersecurity-FF0080?style=for-the-badge&logo=cybersecurity&logoColor=white" alt="Cybersecurity"/>
  <img src="https://img.shields.io/badge/Research-00ffff?style=for-the-badge&logo=google-scholar&logoColor=black" alt="Research"/>
  <img src="https://img.shields.io/badge/Open%20Source-05A6F0?style=for-the-badge&logo=github&logoColor=white" alt="Open Source"/>
</p>

---

## 🎭 **THE PARADOX**

> 🧠 **Knows everything about computers**<br>
> 💻 **Never coded for money**<br>
> 🎓 **Eternal student, forever learning**<br>
> 🌊 **AuDHD • INTP • Persian/English Bilingual**

*I exist in the space between knowing and doing, between theory and practice, between the digital and the mystical.*

---

## 📊 **GITHUB STATISTICS**

<div align="center">
  <table>
    <tr>
      <td>
        <a href="https://github.com/Shaiinarab"><img src="https://github-readme-stats.vercel.app/api?username=Shaiinarab&show_icons=true&theme=radical&include_all_commits=true&count_private=true&hide_border=true&bg_color=0D1117&title_color=ff0080&icon_color=00ffff&text_color=C9D1D9" alt="GitHub statistics for Shaiinarab: stars, commits, pull requests and issues"/></a>
      </td>
      <td>
        <a href="https://github.com/Shaiinarab?tab=repositories"><img src="https://github-readme-stats.vercel.app/api/top-langs/?username=Shaiinarab&layout=compact&langs_count=6&theme=radical&hide_border=true&bg_color=0D1117&title_color=ff0080&icon_color=00ffff&text_color=C9D1D9" alt="Most used languages across Shaiinarab's repositories"/></a>
      </td>
    </tr>
  </table>
  
  <br/>
  
  <!-- Streak Stats -->
  <a href="https://github.com/Shaiinarab"><img src="https://streak-stats.demolab.com/?user=Shaiinarab&theme=radical&hide_border=true&background=0D1117&stroke=ff0080" alt="Contribution streak statistics for Shaiinarab"/></a>
  
  <br/><br/>
  
  <!-- Contribution Graph -->
  <a href="https://github.com/Shaiinarab"><img src="https://ghchart.rshah.org/ff0080/Shaiinarab" alt="Contribution calendar for Shaiinarab" style="width: 100%; max-width: 800px;"/></a>
</div>

---

## 🏆 **TROPHIES & ACHIEVEMENTS**

<p align="center">
  <a href="https://github.com/Shaiinarab"><img src="https://github-trophies.vercel.app/?username=Shaiinarab&theme=radical&no-frame=true&row=1&margin-w=10&column=4" alt="GitHub trophies earned by Shaiinarab"/></a>
</p>

---

## 🌐 **CONNECT IF YOU DARE**

<p align="center">
  <a href="https://www.linkedin.com/in/shaiinarab/" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/>
  </a>
  <a href="https://twitter.com/shaiinarab" target="_blank">
    <img src="https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white" alt="Twitter"/>
  </a>
  <a href="mailto:Shahinarab619@outlook.com">
    <img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"/>
  </a>
  <a href="https://github.com/shaiinarab" target="_blank">
    <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/>
  </a>
</p>

> 🎵 **Instead of talking, send me your favorite track.**<br>
> 🎧 *Music speaks what cannot be expressed.*

---

## 👁️ **YOU ARE WATCHER #**

<div align="center">
  <a href="https://github.com/Shaiinarab"><img src="https://komarev.com/ghpvc/?username=Shaiinarab&color=ff0080&style=flat-square" alt="Profile view counter for Shaiinarab"/></a>
</div>

---

<div align="center">

## 🌑 **FINAL TRANSMISSION**

<img src="https://media.giphy.com/media/v1.Y2xpdGlvbl9leHBsb3Npb24/XreJqONhNAmKVrXzDC/giphy.gif" width="200" alt="Cyberpunk GIF"/>

> **"Even the sky is not a limit. YOU are the limit."**<br>
> 🌃 Made with 🖤, ☕, 🎵, and ✨ by **Shahin Arab**<br>
> 🇮🇷 Shiraz, Iran • Eternal Student • Open Source Soul

</div>

---
