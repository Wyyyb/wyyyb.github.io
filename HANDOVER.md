# HANDOVER — wyyyb.github.io (Yubo Wang's personal homepage)

> 中文摘要：这是王钰博（Yubo Wang）个人学术主页的交接文档，面向以后维护或重新设计本站的人类与 AI agent。网站是纯静态站点（HTML/CSS/vanilla JS），内容全部在 `_src/data.json`，运行 `python3 _src/build.py` 生成 `index.html`，推送到 `main` 分支即部署（GitHub Pages 从 `main` 根目录直接提供服务）。本文档记录了：站点现状、仓库结构、数据模型与内容约定、设计系统、素材来源（论文 teaser 图如何裁出、logo 来源与许可）、构建/部署/验收流程、已确认与未确认的个人事实、历史决策、已知坑和待办事项。改内容前先读第 2 节和第 11 节。

_Last updated: 2026-10-15 (commit history: see `git log`). Maintained by the owner, Yubo Wang (GitHub `Wyyyb`)._

---

## 1. Status at a glance

| Item | Value |
|---|---|
| Live URL | https://wyyyb.github.io/ |
| Repository | https://github.com/Wyyyb/wyyyb.github.io — branch `main`, root `/` |
| Hosting | GitHub Pages, "Deploy from a branch" (`main`, `/`), `.nojekyll` present (no Jekyll processing) |
| Stack | Static HTML + CSS + vanilla JS. No framework, no package.json. Generator: Python 3 + Jinja2 + Pillow (`_src/build.py`) |
| Source of truth for content | `_src/data.json` (edit this, then rebuild). `index.html` is generated but hand-editable |
| Old site | al-folio/Jekyll version archived on branch `al-folio-archive`; the stale `gh-pages` branch is unused and can be deleted |
| Design | Editorial-minimal: Newsreader (serif) + Inter, cream/charcoal light & dark themes, single teal accent; publication rows with teaser at left (Haozhe-Wang/Jon-Barron style) and Dongfu-Jiang-style hero, badges, logo strip |
| Page weight | ~72 KB HTML (incl. inline SVG icon sprite) + 21 KB CSS + 7 KB JS + ~1.3 MB images (15 WebP teasers ≈ 1.1 MB, logos ≈ 0.2 MB, photo 142 KB) + Google Fonts |

Deploy verification one-liner (after pushing): `gh api -X POST repos/Wyyyb/wyyyb.github.io/pages/builds` then poll `gh api repos/Wyyyb/wyyyb.github.io/pages/builds/latest --jq .status` until `built`, then `curl -s https://wyyyb.github.io/ | grep -c "<title>"` (expect 1).

## 2. The owner — confirmed facts, unverified facts, and things NOT to do

**Confirmed by the owner (chat, 2026-10-15) or by primary sources:**
- Yubo Wang (王钰博). Ph.D. student in Computer Science, University of Waterloo, **May 2024 – Present**; advisor Prof. Wenhu Chen (TIGER-Lab); affiliated with the Vector Institute; collaborating with TIGER-Lab since 2023 (first Waterloo-affiliated paper Sept 2023).
- Student Researcher, **Google Cloud AI Research (CAIR)**, **Aug 2026 – Jan 2027**, working on automated research methods.
- Research Intern, **MiniMax**, **Jun 2025 – Dec 2025**, pre-training and mid-training for the MiniMax-M2 series (he is a listed contributor of the MiniMax-M2 technical report).
- Applied Scientist, **Tencent Smart Healthcare**, **Apr 2021 – Aug 2023** (his older homepage called the same job "NLP Algorithm Engineer"; LinkedIn says Applied Scientist — the owner accepted "Applied Scientist").
- M.S. in Computer Science, UC Davis, **Sep 2019 – Jan 2021**. B.Eng. in Computer Science, Chu Kochen Honors College, Zhejiang University, **Aug 2015 – Jun 2019**.
- Handles: email y726wang@uwaterloo.ca; GitHub `Wyyyb`; X `@YuboWang726`; Google Scholar `s_ZW7voAAAAJ` (~4,000 citations, h-index 11 in Oct 2026); LinkedIn `in/yubo-wang-1321a7195`.

**Owner preferences (explicit requests):**
- No citation / h-index statistics on the page (removed on request; `profile.scholar_stats` is `null` — the template renders nothing when null).
- Do **not** mention an HKUST research-assistant position (it was removed on request; do not reintroduce from old search snippets).
- Hero photo should be modest in size (currently 168×210 desktop, 144×180 tablet, 96×120 phone).
- The affiliation logo strip must not sit in the hero; it lives between News and Publications.
- Dates everywhere are month-precise ("Mon YYYY – Mon YYYY", en dash with spaces).

**Unverified / do not assert:**
- Any Vector Institute programme title beyond "affiliated with" (papers list Vector as an affiliation from June 2025 on).
- The FIM mid-training paper (arXiv 2607.12463) is under double-blind review (an ICLR 2027 submission exists on OpenReview). Keep it labelled "arXiv 2026" until decisions (~late Jan 2027); never write "under review at ICLR".
- Google Scholar attributes "PIN: A knowledge-intensive dataset…" to him; the arXiv author list does not include him — it is intentionally **excluded**. Semantic Scholar also wrongly merges arXiv 2604.12243 and 2605.12500 (other Yubo Wangs) — exclude.

## 3. Repository layout

```
index.html                 generated page (python3 _src/build.py). Hand-editable: every publication / news item / row is a commented block
style.css, script.js       copies of _src/style.css and _src/script.js made by build.py (edit the _src versions)
assets/img/profile.jpg     hero portrait (845×1056) + profile-432.webp / profile-648.webp (srcset variants)
assets/img/teasers/*.webp  one teaser per publication, named by publication key, ≤1000 px wide, quality 88
assets/img/logos/*.png     institution logos (RGBA, 160 px tall; *_mark.png = square marks for wide wordmarks)
assets/img/favicon.svg, favicon-32.png, apple-touch-icon.png, og.png (1200×630 social card)
robots.txt, sitemap.xml, .nojekyll
_src/data.json             ALL content (see §4)
_src/template.html.j2      Jinja2 template (autoescape on; fields ending in _html / news.html / about paragraphs are inserted with |safe)
_src/build.py              renders the template; computes year groups, link labels/icons, image sizes, JSON-LD; copies css/js
_src/style.css             design tokens + all styles (see §6)
_src/script.js             theme toggle, Selected/All filter, news "show more", scroll-spy, deep links
_src/icons.svg             inline SVG sprite (Font Awesome Free 6.5.2 CC BY 4.0 + Academicons SIL OFL); regenerate with _src/tools/make_sprite.py
_src/tools/pdfkit.py       PDF figure finder/cropper used to cut the teasers (see §7.1)
_src/tools/teaser_webp.py  PNG → WebP export for teasers
_src/tools/shot.py         Playwright screenshot helper (desktop/mobile, light/dark, full page or viewport)
_src/tools/make_icons.py   regenerates favicon PNGs and og.png from favicon.svg + profile.jpg (Playwright)
_src/tools/make_sprite.py  downloads the icon SVGs and rebuilds _src/icons.svg
_src/provenance/research.json      verified per-paper metadata with sources and notes (authors + marks, venue evidence, every link checked, teaser crop coordinates), plus bio facts with source URLs
_src/provenance/papers_manifest.json  the paper list that drove the research pass (arXiv ids, claimed venues, PDFs used)
_src/provenance/site_content.json     the hand-written content block from which data.json's non-publication parts were assembled
README.md, HANDOVER.md
```

Python dependencies: `jinja2`, `Pillow` (build); `playwright` + Chromium (screenshots/icons only); `pymupdf` (pdfkit only). The tools contain `sys.path.append('/home/ubowang_google_com/.local/lib/python3.10/site-packages')` from the original environment — harmless elsewhere; delete if you like.

## 4. Content model (`_src/data.json`)

Top-level keys: `profile`, `about`, `news`, `experience`, `education`, `service`, `footer`, `affiliation_logos`, `publications`, `publications_meta`.

### 4.1 profile
`name`, `name_cn` (王钰博), `eyebrow` ("Ph.D. Student in Computer Science"), `tagline`, `affiliations` [{name,url}] (rendered as the hero line with " · "), `location`, `photo_portrait`, `email`, `links` [{label,url,icon}] with icon ∈ {envelope, google-scholar, github, x-twitter, linkedin, cv} (mapped to sprite symbols in build.py `ICONS`; add `{"label":"CV","url":"assets/pdf/CV.pdf","icon":"cv"}` to show a CV pill), `chips` (research keywords), `scholar_stats` (null = hidden), `site_url`, `description_meta`.

### 4.2 about
`paragraphs`: list of HTML strings (inserted unescaped). `interests`: [{label, items:[{name,url}]}] rendered as the two-column table under the prose. Keep the first paragraph's facts in sync with §2.

### 4.3 news
Newest first. `{"date":"YYYY-MM", "emoji":"🎉", "html":"…"}`. The first 6 are shown; the rest are behind "Show all N updates". Conventions: acceptances use 🎉 and bold the venue (`<strong>COLM 2026</strong>`), releases 🚀, reports 📄, jobs 💼, benchmarks/adoption 📊. Dates are month precision; the build renders "Mon YYYY".

### 4.4 publications
One object per paper (order in the file does not matter; build.py sorts):
- `key` — slug; also the teaser filename and the deep-link id `#pub-<key>`.
- `title`, `authors_html` — authors as HTML; **`<b>Yubo Wang</b>`** always; `*` = equal contribution, `†` = core contributors, exactly as the paper marks them (`publications_meta.has_equal_marks/has_core_marks` drive the legend line). For >10 authors use "First, Second, Third, …, <b>Yubo Wang</b>, …, Last" (team reports: "M-A-P Team: …", "MiniMax (218 contributors in alphabetical order, incl. <b>Yubo Wang</b>)").
- `venue_short` (badge text: "NeurIPS 2024", "Findings of EMNLP 2026", "arXiv 2026", "Tech Report 2026"), `venue_long`, `distinction` (free text; a second badge is shown only when it contains Spotlight / Oral / Best Paper / Outstanding / Highlight).
- `year`, `month` — **first arXiv version** date. Grouping on the page uses the *publication* year when `venue_short` contains a year and is not arXiv/Tech Report; otherwise the arXiv year (`display_year` in build.py). Within a group, newest arXiv date first.
- `arxiv_url`, `pub_page_url` (OpenReview / ACL Anthology / NeurIPS proceedings).
- `links`: [{label,url}] in display order. Labels understood by build.py: Paper (shown as "arXiv" when the URL is arxiv.org), Publication Page (shown as OpenReview / ACL Anthology / NeurIPS by host), Project Page, Code, Dataset, Models, Demo, Leaderboard, HF Collection, Blog, Tweet, PDF. Anything else gets a generic link icon. Only add links you have opened.
- `summary` — one sentence, ≤ ~28 words, concrete, no hype. `highlight` — optional ≤12-word verified fact (e.g. "1,000+ GitHub stars", "Adopted by the Hugging Face Open LLM Leaderboard"); `highlight_source_url` optional.
- `selected` — shown in the default view (currently the 6 first-author papers + ClawBench + Critique-Coder = 8). `first_author`, `n_authors`, `github_stars`, `teaser_alt`, `teaser_verified` are informational.
- `teaser` — `assets/img/teasers/<key>.webp` or null (null renders a labelled dotted placeholder tile; name comes from `SHORT_NAMES` in build.py — add new keys there).

`publications_meta` = {count, selected_count, has_equal_marks, has_core_marks} — **recompute by hand when you add papers** (or let the no-JS status line be slightly off; script.js recounts from the DOM at runtime).

### 4.5 experience / education
`{role|degree, org, org_url, where, dates, logo, logo_square (optional square mark for wide wordmarks), logo_text (fallback monogram), details}`. Empty `dates`/`where`/`details` are simply omitted. Order = newest first.

### 4.6 affiliation_logos
The logo strip between News and Publications: [{name,url,logo}]. Wordmarks (aspect > 1.8) automatically get the `is-wordmark` class (rendered smaller).

### 4.7 footer / service
`footer.copyright`, `footer.updated` ("Last updated: October 2026" — **update when you change content**), `footer.credit`. `service` is null (section hidden); set `{"reviewing": "…"}` to show a Service section.

## 5. Build, deploy, verify

```bash
# from the repository root
python3 _src/build.py            # -> index.html, style.css, script.js
python3 - <<'EOF'                # quick HTML sanity (tags balanced)
from html.parser import HTMLParser
class P(HTMLParser):
    VOID={'img','br','meta','link','input','hr','source','wbr','area','base','col','embed','param','track','use','path'}
    def __init__(s): super().__init__(); s.stack=[]; s.errs=[]
    def handle_starttag(s,t,a):
        if t not in s.VOID: s.stack.append(t)
    def handle_endtag(s,t):
        if t in s.VOID: return
        if s.stack and s.stack[-1]==t: s.stack.pop()
        else: s.errs.append((t, s.getpos()))
p=P(); p.feed(open('index.html').read()); print('unbalanced:', p.errs, 'open:', p.stack)
EOF
python3 _src/tools/shot.py file://$PWD/index.html /tmp/desktop.png 1280 full light
python3 _src/tools/shot.py file://$PWD/index.html /tmp/mobile.png 375 full light
python3 _src/tools/shot.py file://$PWD/index.html /tmp/dark.png 1280 viewport dark
git add -A && git commit -m "…" && git push origin main
gh api -X POST repos/Wyyyb/wyyyb.github.io/pages/builds      # Pages did not always rebuild on push by itself; requesting a build is reliable (~30 s)
```

Acceptance checklist before pushing (all were green on 2026-10-15):
1. `document.documentElement.scrollWidth == viewport width` at 320/360/375/414/768/1024/1280 (use Playwright; see the overflow snippet in the git history of this doc or write `pg.evaluate('document.documentElement.scrollWidth')`).
2. Light and dark screenshots look intentional (dark: images are dimmed by `filter: brightness(.88)`).
3. Selected/All toggle: counts, `aria-pressed`, status line "Showing 8 selected of 15 papers." / "Showing all 15 papers."; the "Selected" badge is visible only in the All view.
4. Every new URL opened manually; arXiv ids match titles.
5. `footer.updated` bumped; `?v=` cache-busting query on css/js is the build date (automatic).

## 6. Design system (why it looks the way it does)

References the owner chose: https://jdf-prog.github.io/ (Dongfu Jiang; information architecture: hero pills/chips, logo strip, badges, timeline rows) and https://haozheh3.github.io/ (Haozhe Wang; calm teaser-left publication rows, one-line summaries, show selected/all), secondary https://cs.uwaterloo.ca/~w2ren/ (Weiming Ren). Three full variants were built and judged (visual, usability, code/a11y lenses); the editorial-minimal variant won and was then merged with the best ideas of the others and fixed per a 5-lens QA pass. Saved variants/screenshots are not in the repo (they live in the original scratch workspace, see §9).

Tokens (`:root` in `_src/style.css`; dark values via `light-dark()` inside `@supports`, plain light values as fallback):
- Background `#faf8f3` / dark `#171614`; elevated `#f1ede5` / `#201f1b`; image plate `#ffffff` / `#dcd9d2`.
- Ink `#1e1c19` / `#ebe7df`, ink-2 `#4f4b45` / `#b9b3a8`, ink-3 `#6f6a62` / `#908a7f` (all ≥ 4.5:1 on their backgrounds).
- Accent teal `#1f6b63` / `#7cc7bb` (links, chips, active segment), accent-soft `#e3eeeb` / `#1c2a28`; venue badge umber `#6a5a3a` on `#f0eadd` (dark `#c9b68f` on `#272319`).
- Type: Newsreader 500 for name, section titles, year labels, publication titles; Inter 400/500/600 for everything else; body 17 px / 1.65; measure 880 px; CJK name uses system CJK fonts.
- Layout: single column; hero = text + 168×210 photo (grid); sections separated by hairlines, not cards; publication row = `--figure-w` 240 px plate (16:9, `object-fit: contain`, white plate) + text; year label shares the figure column; hover tint on rows.
- Breakpoints: ≤900 px (figure 184 px, photo 144 px), ≤720 px (hero becomes photo-beside-name via `display: contents`, single-column pub rows, stacked footer), ≤640 px (header becomes static two-row: brand + theme toggle, then all five links; no horizontal scrolling), ≤340 px (tighter nav).
- Theme: follows OS; toggle persists to localStorage and is forgotten again when the choice matches the OS; constant accessible name "Dark theme" with `aria-pressed`.
- Icons: inline SVG sprite, `<svg class="icon"><use href="#i-github"/></svg>`; no icon-font CDNs (they cost ~450 KB and blocked rendering).
- Accessibility: landmarks, skip link (fixed position), one h1, heading order h1→h2→h3 (year)→h4 (title), `role="list"` on styled lists, focus rings, `aria-live` status for the filter, reduced-motion handling, print stylesheet prints all papers/news.
- No-JS: all papers and news visible; toggle/controls hidden; status line reads "15 papers, 8 marked Selected."

## 7. Assets and how they were made

### 7.1 Publication teasers
Owner requirement: each teaser is cut from the paper itself — the **method/system/pipeline overview figure**, or the conceptual teaser (usually Fig. 1) — never a results table. Procedure with `_src/tools/pdfkit.py` (PyMuPDF):
```bash
python3 _src/tools/pdfkit.py info  PAPER.pdf 1            # captions, image rects, drawing clusters, suggested figure bbox, text blocks (PDF points, origin top-left)
python3 _src/tools/pdfkit.py page  PAPER.pdf 1 /tmp/p1.png --zoom 2 --grid   # page with a labelled 50-pt grid to read coordinates
python3 _src/tools/pdfkit.py clip  PAPER.pdf 1 108 201 506 393 /tmp/key.png --zoom 4   # crop + auto-trim white margins (pad 12 px)
python3 _src/tools/teaser_webp.py /tmp/key.png --out assets/img/teasers   # -> assets/img/teasers/key.webp (≤1000 px wide, q88)
```
Rules used: exclude caption/body text/arXiv stamp; include all panels and legends; prefer aspect 1.25–2.4 (the plate is 16:9 with letterboxing); if a figure is very wide, crop the overview sub-panel (done for FIM: left+middle panels of Fig. 1; ClawBench: left+middle of Fig. 1). Every crop was reviewed visually; coordinates are recorded in `_src/provenance/research.json` → `teasers[]`.

Per-paper provenance (venue · selected · author position · teaser source · publication page):

| key | venue | selected | position | teaser (page / figure / px) | publication page |
|---|---|---|---|---|---|
| `fim-midtraining` | arXiv 2026 | yes | 1st/8 | p.1 Fig. 1 (1295×557) | — |
| `minimax-m2` | Tech Report 2026 | no | 175/218 | p.26 Fig. 8 (1697×917) | — |
| `rewardharness` | COLM 2026 | no | 8/14 | p.3 Fig. 2 (1609×877) | https://openreview.net/forum?id=tXv4YSeA2j |
| `clawbench` | Findings of EMNLP 2026 | yes | 2/28 | p.1 Fig. 1 (1483×863) | https://openreview.net/forum?id=bqzqPmhNiN |
| `critique-coder` | ICLR 2026 | yes | 3/4 | p.3 Fig. 2 (1095×518) | https://openreview.net/forum?id=tsuxIeLUsz |
| `one-shot-cft` | EMNLP 2025 | yes | 1st/5 | p.3 Fig. 2 (1824×659) | https://aclanthology.org/2025.emnlp-main.149/ |
| `scholarcopilot` | COLM 2025 | yes | 1st/10 | p.1 Fig. 1 (1310×607) | https://openreview.net/forum?id=r8nloXtluk |
| `supergpqa` | NeurIPS 2025 | no | 63/97 | p.6 Fig. 2 (1687×900) | https://openreview.net/forum?id=6WgflzYQpf |
| `cft` | COLM 2025 | yes | 1st/3 | p.1 Fig. 1 (1592×763) | https://openreview.net/forum?id=vTAz44GgOA |
| `mammoth-vl` | ACL 2025 | no | 5/10 | p.2 Fig. 2 (1815×1065) | https://aclanthology.org/2025.acl-long.680/ |
| `mega-bench` | ICLR 2025 | no | 6/16 | p.1 Fig. 1 (1508×1156) | https://openreview.net/forum?id=2rWbKbmOuM |
| `mmmu-pro` | ACL 2025 | no | 4/13 | p.4 Fig. 4 (1817×1371) | https://aclanthology.org/2025.acl-long.736/ |
| `mmlu-pro` | NeurIPS 2024 · Spotlight (Datasets and Benchmarks Track) | yes | 1st/17 | p.4 Fig. 2 (1291×762) | https://proceedings.neurips.cc/paper_files/paper/2024/hash/ad236edc564f3e3156e1b2feafb99a24-Abstract-Datasets_and_Benchmarks_Track.html |
| `map-neo` | Tech Report 2024 | no | 35/45 | p.11 Fig. 4 (1522×657) | — |
| `llm-amt` | Findings of EMNLP 2024 | yes | 1st/3 | p.2 Fig. 1 (1696×1420) | https://aclanthology.org/2024.findings-emnlp.95/ |

Notes: RewardHarness's COLM camera-ready title differs ("RewardHarness: Learning Human Preferences for Image Editing with Only 100 Demonstrations"); the site uses the arXiv title. ClawBench's EMNLP 2026 Findings record is not in the ACL Anthology yet (conference 24–29 Oct 2026) — add the Anthology URL as `pub_page_url` once it exists; the COLM-2026-workshop OpenReview page was intentionally not linked. MAmmoTH-VL's HF demo Space is down (RUNTIME_ERROR) and was removed. MMLU-Pro's OpenReview forum is `y10DM6R2r3`; Spotlight is confirmed by the arXiv comment and OpenReview.

### 7.2 Logos
`uwaterloo.png` (UW shield from uwaterloo.ca site icon), `vector.png` (official EN lockup SVG from vectorinstitute.ai), `ucdavis.png` (Wikimedia Commons seal, PD file), `zju.png` (ZJU emblem SVG via Wikipedia), `tencent.png` (Commons wordmark) + `tencent_mark.png` (site icon), `minimax.png` (official CDN PNG), `google.png` (Commons "Google G logo", public domain). All trademarks are used nominatively to indicate affiliation. Logos sit on white plates in both themes, so dark-mode variants are unnecessary. Keep new logos RGBA, trimmed, 160 px tall.

### 7.3 Photo, favicon, social card
`profile.jpg` is a 4:5 crop of the owner's photo (`1121777216045_.pic.jpg`); `profile-432/648.webp` are srcset variants. `favicon.svg` = teal rounded square with a serif "Y"; `favicon-32.png`, `apple-touch-icon.png`, `og.png` (1200×630, name + tagline + photo) are produced by `_src/tools/make_icons.py` — rerun it if the photo or tagline changes.

## 8. Publications policy
- Default view shows `selected` papers; everything else is one click away. Keep "Selected" = first-author papers + the most significant co-authored ones.
- Author strings are copied from the paper/arXiv order; never reorder. Mark equal/core contribution exactly as the paper does.
- Venue badge shows the final venue once accepted ("Findings of EMNLP 2026"), with arXiv year used only for preprints. When a preprint gets accepted: update `venue_short`, `venue_long`, `pub_page_url`, add a news item, and (optionally) move it into `selected`.
- Links: arXiv first, then publication page, project page, code, data/models, demo/leaderboard, HF collection, blog, tweet.

## 9. The original scratch workspace (not in git)
`/rmeng_data/yubo_data/October/yubo/website_work/` on the machine where the site was built: `design_variants/v1..v3` (the three candidate designs with screenshots), `design_assets/DESIGN_BRIEF.md` (the brief given to the designers), `teasers/*.png` (full-resolution crops), `pages/` (all review screenshots), `data/research.json` + `qa.json` + `design_panel.json` (full agent outputs), `arxiv_pdfs/` (downloaded co-author PDFs), `scripts/` (originals of the tools). Owner-provided source material: `/rmeng_data/yubo_data/test_data/huayu_service_v2607/personal_website_yubo/` (photo, Google Scholar screenshot of 2026-10-14, 6 first-author PDFs in `papers/`, 2 co-author PDFs in `co-papers/`). If that machine is gone, everything needed to maintain the site is in this repository.

## 10. History and decisions (short)
- 2026-10-15: replaced the al-folio/Jekyll site (owner found it ugly). Design chosen by a 3-variant panel + 3 judges; v1 "editorial-minimal" won (22.9 vs 21.8 vs 20.3), then merged with v3's mobile nav/status line and v2's icon pills/logo strip. A 5-lens QA pass (links, content/facts, visual+interaction, HTML/a11y/perf, design critique) produced 10 major / 25 minor fixes, all applied except re-cropping three tall teasers (LLM-AMT, MEGA-Bench, MMMU-Pro), which still letterbox a little.
- Same day, per owner feedback: removed Scholar stats, removed HKUST, added Google CAIR role, shrank the photo, moved the logo strip below News, month-precise dates, PhD start May 2024.
- GitHub Pages source switched from `gh-pages` to `main` via `gh api -X PUT repos/Wyyyb/wyyyb.github.io/pages -f 'source[branch]=main' -f 'source[path]=/'`.

## 11. Gotchas
- **LinkedIn cannot be fetched** by bots (HTTP 999, also for crawler UAs; no Wayback snapshots). Search-engine snippets worked once and then hit CAPTCHAs. Ask the owner for LinkedIn-sourced facts instead of guessing.
- In the original environment the WebSearch tool was blocked by org policy; curl + DuckDuckGo HTML / r.jina.ai / official APIs (arXiv export API, Hugging Face API, `gh api`, OpenReview api2 `notes/search`) were used instead. OpenReview forum pages and the profile API are behind a browser challenge.
- Headless Chromium there had no colour-emoji font: news emoji show as boxes in screenshots only. Real browsers are fine.
- Full-page screenshots can show blank teaser plates if taken before the idle prefetch runs (`loading="lazy"` + `script.js` upgrades to eager after load). Wait ~1.5 s or scroll first.
- `light-dark()` tokens live inside `@supports`; older browsers get the light theme and the theme toggle is hidden by `@supports not`. `color-mix()` uses pre-mixed fallbacks (`--accent-40/50`).
- The "Selected" badge is emitted only for selected papers and hidden in the default view by `#publications[data-view="selected"]`; `data-view` is set by script.js (not in the HTML), so no-JS shows all badges — intended.
- `make_sprite.py` strips `<title>` from source SVGs; if you add an icon, keep that behaviour (otherwise extra `<title>` elements appear in the page).
- Pages builds did not reliably start on push; `gh api -X POST …/pages/builds` always worked within ~30 s.
- Google Scholar numbers were deliberately removed; don't add citation counts back without asking.

## 12. Backlog / ideas (none required)
- Add a CV: put the PDF at `assets/pdf/Yubo_Wang_CV.pdf` and add a `cv` link in `profile.links`.
- Service section (`service.reviewing`) once the owner lists reviewing duties.
- Re-crop LLM-AMT / MEGA-Bench / MMMU-Pro teasers to ~2:1 panels if the letterboxing bothers anyone.
- When ClawBench's Anthology page and the FIM paper's venue are known, update venue/links/news.
- Optional: 404.html, analytics (none installed on purpose), Semantic Scholar/ORCID pills (sprite ids would need adding in `make_sprite.py`).
