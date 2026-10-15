# HANDOVER — wyyyb.github.io (Yubo Wang's personal homepage)

> 中文摘要：这是王钰博（Yubo Wang）个人学术主页的交接文档，面向以后维护或重新设计本站的人类与 AI agent。网站是纯静态站点（HTML/CSS/vanilla JS），内容全部在 `_src/data.json`，运行 `python3 _src/build.py` 生成 `index.html`，推送到 `main` 分支即部署（GitHub Pages 从 `main` 根目录直接提供服务）。本文档记录：站点现状、仓库结构、数据模型与内容约定、设计系统、素材来源（论文 teaser 图如何裁出、logo 来源与许可）、构建/部署/验收流程（含“加一篇论文”的完整步骤）、已确认的个人事实与“动手前要先问站主”的清单、历史决策、已知坑和待办。改内容前先读第 2 节和第 5 节的 Recipe。

_Last updated: 2026-10-15. Owner: Yubo Wang (GitHub `Wyyyb`). This document was reviewed by two independent agents (a maintainer dry-run and a fact check) and corrected accordingly._

---

## 1. Status at a glance

| Item | Value |
|---|---|
| Live URL | https://wyyyb.github.io/ |
| Repository | https://github.com/Wyyyb/wyyyb.github.io — branch `main`, root `/` |
| Hosting | GitHub Pages, "Deploy from a branch" (`main`, `/`), legacy build type, `.nojekyll` present (no Jekyll). Read the settings with `gh api repos/Wyyyb/wyyyb.github.io/pages` |
| Stack | Static HTML + CSS + vanilla JS. No framework, no package.json. Generator: Python 3 + Jinja2 + Pillow (`_src/build.py`) |
| Source of truth | `_src/data.json` (edit this, then rebuild). `index.html` is generated but hand-editable |
| Old site | al-folio/Jekyll version archived on branch `al-folio-archive`; the stale `gh-pages` branch is unused (ask the owner before deleting either) |
| Design | Editorial-minimal: Newsreader (serif) + Inter, cream/charcoal light & dark themes, single teal accent; publication rows with a teaser at left (Haozhe Wang / Jon Barron style) plus Dongfu-Jiang-style hero pills, chips, badges and logo strip |
| Page weight | 74,884 B HTML (incl. the inline SVG icon sprite) + 22.2 KB CSS + 6.7 KB JS + images ≈ 1.4 MB (15 WebP teasers 1105 KB, logo PNGs 202 KB, hero photo 30 KB `profile-432.webp` / 57 KB `profile-648.webp` via srcset; `profile.jpg` 142 KB is only fetched by browsers without srcset) + Google Fonts |

**Deploy verification (after pushing):** a push to `main` starts a Pages build by itself (every commit on 2026-10-15 got one within ~3 s; ~20–30 s to `built`). Poll `gh api repos/Wyyyb/wyyyb.github.io/pages/builds/latest --jq '.status,.commit'` until `built` for your commit, then prove the *content* is live, e.g. `curl -s -H 'Cache-Control: no-cache' https://wyyyb.github.io/ | grep -c 'id="pub-<new-key>"'` (expect 1) or grep for the new `footer.updated` text. The CDN caches with `max-age=600`, so allow up to 10 minutes / hard-refresh before concluding a deploy failed. `gh api -X POST repos/Wyyyb/wyyyb.github.io/pages/builds` is only a fallback when no build appears after ~1 min (issuing it while a push build is running just adds a harmless `errored, duration 0` entry).

## 2. The owner — confirmed facts, preferences, and things NOT to do

**Confirmed by the owner (chat, 2026-10-15) or by primary sources:**
- Yubo Wang (王钰博). Ph.D. student in Computer Science, University of Waterloo, **May 2024 – Present**; advisor Prof. Wenhu Chen (TIGER-Lab); affiliated with the Vector Institute; collaborating with TIGER-Lab since 2023 (first Waterloo-affiliated paper Sept 2023).
- Student Researcher, **Google Cloud AI Research (CAIR)**, **Aug 2026 – Jan 2027**, working on automated research methods.
- Research Intern, **MiniMax**, **Jun 2025 – Dec 2025**, pre-training and mid-training for the MiniMax-M2 series (listed contributor of the MiniMax-M2 technical report).
- Applied Scientist, **Tencent Smart Healthcare**, **Apr 2021 – Aug 2023** (his older homepage called the job "NLP Algorithm Engineer"; LinkedIn says Applied Scientist; the owner accepted "Applied Scientist").
- M.S. in Computer Science, UC Davis, **Sep 2019 – Jan 2021**. B.Eng. in Computer Science, Chu Kochen Honors College, Zhejiang University, **Aug 2015 – Jun 2019**.
- Handles: email y726wang@uwaterloo.ca; GitHub `Wyyyb`; X `@YuboWang726`; Google Scholar `s_ZW7voAAAAJ` (~4,000 citations, h-index 11 in Oct 2026); LinkedIn `in/yubo-wang-1321a7195`.

> Note: `_src/provenance/research.json → bio` was written *before* these confirmations and still records the research pass's guesses — PhD start "Spring 2025" (from Wenhu Chen's lab page), MiniMax "at least Dec 2025 – May 2026", Tencent "NLP Algorithm Engineer, 2021–2023 (months unknown)", and an HKUST research-assistant entry at confidence 0.4. Where they differ, the owner-confirmed values above and `_src/data.json` win; never "correct" data.json from research.json's bio block.

**Owner preferences (explicit requests):**
- No citation / h-index statistics on the page (`profile.scholar_stats` is `null`; the template renders nothing when null).
- Do **not** mention an HKUST research-assistant position (removed on request; do not reintroduce it from old search snippets or from research.json).
- Hero photo stays modest (168×210 desktop, 144×180 tablet, 96×120 phone).
- The affiliation logo strip must not sit in the hero; it lives between News and Publications.
- Dates everywhere are month-precise ("Mon YYYY – Mon YYYY", en dash with spaces; "Present" for ongoing).

**Where each fact lives — change all copies:**

| fact | places |
|---|---|
| job / degree titles and dates | `_src/data.json` → `experience[]` / `education[]`; `about.paragraphs[0]` (watch tense words such as "currently" and the inline Tencent/MiniMax dates); the matching 💼 `news[]` item (leave past items as history); §2 of this document |
| tagline / eyebrow / affiliations | `profile.tagline`, `profile.eyebrow`, `profile.affiliations`, `profile.description_meta`; the social card `assets/img/og.png` is rendered from the same fields by `_src/tools/make_icons.py` (rerun it, §7.3); `<title>` uses `profile.eyebrow` + the first affiliation name |
| handles | `profile.links` (icons: envelope, google-scholar, github, x-twitter, linkedin, cv), `profile.email`; `twitter:site` is derived from the X link; JSON-LD `sameAs` from all links; `repo_url` is hard-coded in build.py |
| background colours | tokens in `_src/style.css` (declared twice, see §6) and the two `<meta name="theme-color">` tags in the template |

**Ask the owner before you:** re-add citation counts / h-index; mention HKUST; change which papers are `selected`, reorder authors or change contribution marks; enlarge the hero photo or move the logo strip; assert a venue for the FIM paper (double-blind review until ~late Jan 2027) or label anything "under review"; state any fact whose only source is LinkedIn; add a new institution logo (trademark use) or a CV PDF; change the tagline/eyebrow wording; add analytics, new CDNs or third-party scripts; delete the `gh-pages` or `al-folio-archive` branches; change the design references or accent colour.

**Unverified / do not assert:**
- Any Vector Institute programme title beyond "affiliated with" (papers list Vector as an affiliation from June 2025 on).
- The FIM mid-training paper (arXiv 2607.12463) is under double-blind review (an ICLR 2027 submission exists on OpenReview). Keep it labelled "arXiv 2026" until decisions; never write "under review at ICLR".
- Google Scholar attributes "PIN: A knowledge-intensive dataset for paired and interleaved multimodal documents" (arXiv 2406.13923; 7 citations in the 2026-10-14 screenshot) to him because of a different "Y. Wang" in the author list; the arXiv author list does not include him — intentionally **excluded** (source: the owner-provided Scholar screenshot, not recorded in `_src/provenance/`). Semantic Scholar also wrongly merges arXiv 2604.12243 and 2605.12500 (other Yubo Wangs) — exclude.

## 3. Repository layout

```
index.html                 generated page (python3 _src/build.py). Hand-editable: each publication is wrapped in <!-- PUB: key --> … <!-- /PUB: key -->;
                           news items and experience/education rows are plain <li> elements under one section comment (<!-- NEWS: … -->, <!-- EXPERIENCE: … -->, <!-- EDUCATION: … -->)
style.css, script.js       copies of _src/style.css and _src/script.js written by build.py (edit the _src versions, never the root copies)
sitemap.xml                written by build.py on every build (lastmod = build date); robots.txt is static
assets/img/profile.jpg     hero portrait (845×1056) + profile-432.webp / profile-648.webp (srcset variants)
assets/img/teasers/*.webp  one teaser per publication, named by publication key, ≤1000 px wide, quality 88
assets/img/logos/*.png     institution logos (RGBA, trimmed; 160 px tall except tencent.png, the 640×109 wordmark; *_mark.png = near-square marks for the 52 px row tiles). Current: google.png 157×160, minimax.png 160×160, tencent.png 640×109, tencent_mark.png 145×160, ucdavis.png 160×160, uwaterloo.png 139×160, vector.png 438×160, zju.png 160×160
assets/img/favicon.svg, favicon-32.png, apple-touch-icon.png, og.png (1200×630 social card)
_src/data.json             ALL content (see §4)
_src/template.html.j2      Jinja2 template (autoescape on). Inserted unescaped with |safe: about.paragraphs[], news[].html, publications[].authors_html,
                           experience[]/education[].details, and the JSON-LD; every other field (titles, summaries, highlights, dates, link labels) is escaped
_src/build.py              renders the template; computes year groups, link labels/icons, image sizes, publications_meta, JSON-LD, sitemap; copies css/js
_src/style.css             design tokens + all styles (see §6)
_src/script.js             theme toggle, Selected/All filter, news "show more" (NEWS_LIMIT = 6), scroll-spy, deep links
_src/icons.svg             inline SVG sprite (Font Awesome Free 6.5.2 CC BY 4.0 + Academicons SIL OFL); regenerate with _src/tools/make_sprite.py (§7.4)
_src/tools/pdfkit.py       PDF figure finder/cropper used to cut the teasers (§7.1)
_src/tools/teaser_webp.py  PNG → WebP export for teasers (names the .webp after the PNG basename)
_src/tools/shot.py         Playwright screenshot helper: shot.py URL OUT.png WIDTH full|viewport light|dark (waits networkidle + 1.5 s)
_src/tools/make_icons.py   regenerates favicon PNGs and og.png from favicon.svg + profile.jpg + data.json profile fields (Playwright, needs network for Google Fonts)
_src/tools/make_sprite.py  downloads the icon SVGs (caches them in the git-ignored _src/tools/_icon_sources/) and rebuilds _src/icons.svg
_src/provenance/research.json      verified per-paper metadata with sources and notes (authors + marks, venue evidence, every link checked, teaser crop coordinates), plus bio facts with source URLs (superseded where they conflict with §2)
_src/provenance/papers_manifest.json  the paper list that drove the research pass (arXiv ids, claimed venues, PDFs used)
_src/provenance/site_content.json     the original hand-written content block (frozen snapshot; data.json is the live copy)
README.md, HANDOVER.md
```

Python dependencies: `jinja2` + `Pillow` (build.py; Pillow is also used by pdfkit.py and teaser_webp.py); `playwright` + Chromium (shot.py, make_icons.py); `pymupdf` (pdfkit.py). `build.py` and all tools start with `sys.path.append('/home/ubowang_google_com/.local/lib/python3.10/site-packages')` from the original environment — harmless elsewhere; delete if you like. Git auth on a new machine: `gh auth login` then `gh auth setup-git` (pushes are HTTPS; no credential helper is configured in the repo).

## 4. Content model (`_src/data.json`)

Top-level keys: `profile`, `about`, `news`, `experience`, `education`, `service`, `footer`, `affiliation_logos`, `publications`, `publications_meta` (informational; recomputed by build.py).

### 4.1 profile
`name`, `name_cn` (王钰博), `eyebrow` ("Ph.D. Student in Computer Science"), `tagline`, optional `og_tagline` (shorter wording for the social card only), `affiliations` [{name,url}] (hero line joined with " · "; the first one also ends the `<title>`), `location`, `photo_portrait`, `email`, `links` [{label,url,icon}] with icon ∈ {envelope, google-scholar, github, x-twitter, linkedin, cv} (mapped to sprite symbols by `ICONS` in build.py; to show a CV pill add `{"label":"CV","url":"assets/pdf/Yubo_Wang_CV.pdf","icon":"cv"}` and create `assets/pdf/`), `chips` (research keywords), `scholar_stats` (null = hidden), `site_url`, `description_meta`.

### 4.2 about
`paragraphs`: list of HTML strings (inserted unescaped). `interests`: [{label, items:[{name,url}]}] rendered as the two-column table under the prose. Keep the first paragraph's facts in sync with §2 and with `experience`/`education`.

### 4.3 news
Newest first. `{"date":"YYYY-MM", "emoji":"🎉", "html":"…"}` — `date` must be `YYYY-MM` (rendered "Mon YYYY"), `emoji` optional, `html` inserted unescaped. The first 6 are shown; the rest sit behind "Show all N updates". The limit is `NEWS_LIMIT` in `_src/script.js` (the `news_limit=6` passed by build.py only fills an HTML comment) — change both if you change it. Conventions used so far: acceptances 🎉 with the venue in bold (`<strong>COLM 2026</strong>`); the MMLU-Pro NeurIPS Spotlight uses 🏆; releases 🚀 (the ClawBench release uses its mascot 🦀); tech reports 📄; jobs 💼; adoption/benchmark news 📊. Reuse these rather than inventing new ones.

### 4.4 publications
One object per paper (file order does not matter; build.py sorts).

**Required keys** (build.py fails or misbehaves without them): `key`, `title`, `venue_short`, `year`, `links` (may be `[]`). Strongly recommended: `arxiv_url`, `month` (defaults to 1), `authors_html`, `summary`, `selected`, `first_author`, `teaser`. **Not read by the build at all** (kept for humans/provenance): `venue_long`, `pub_page_url`, `highlight_source_url`, `github_stars`, `n_authors`, `teaser_alt`, `teaser_verified`.

Minimal new entry (paste, then fill in):
```json
{"key": "my-paper", "selected": true, "first_author": true,
 "title": "Title", "authors_html": "<b>Yubo Wang</b>, Co Author", "n_authors": 2,
 "venue_short": "arXiv 2026", "venue_long": "arXiv preprint arXiv:2610.xxxxx", "distinction": "",
 "year": 2026, "month": 10, "arxiv_url": "https://arxiv.org/abs/2610.xxxxx", "pub_page_url": "",
 "links": [{"label": "Paper", "url": "https://arxiv.org/abs/2610.xxxxx"}],
 "summary": "One concrete sentence, no hype.", "highlight": "",
 "teaser": "assets/img/teasers/my-paper.webp"}
```

Field semantics:
- `key` — slug; also the teaser filename and the deep-link id `#pub-<key>` (a deep link to a non-selected paper switches the page to the All view).
- `title`, `authors_html` — authors as HTML; **`<b>Yubo Wang</b>`** always; `*` = equal contribution, `†` = core contributors, exactly as the paper marks them (the legend line appears automatically when such marks exist). For >10 authors use "First, Second, Third, …, <b>Yubo Wang</b>, …, Last" (SuperGPQA keeps arXiv's pseudo-author as a prefix: "M-A-P Team: Xinrun Du, …"; MAP-Neo uses the plain form; MiniMax-M2 is "MiniMax (218 contributors in alphabetical order, incl. <b>Yubo Wang</b>)").
- `venue_short` (badge text: "NeurIPS 2024", "Findings of EMNLP 2026", "arXiv 2026", "Tech Report 2026"), `venue_long` (bookkeeping), `distinction` (free text; a second badge appears only when it contains Spotlight / Oral / Best Paper / Outstanding / Highlight).
- `year`, `month` — **first arXiv version** date. Grouping uses the *publication* year when `venue_short` contains a 20xx year and does not start with `arXiv`, `Tech Report` or `Preprint` (case-insensitive); otherwise the arXiv year (`display_year` in build.py). Within a group: newest arXiv year/month first, first-author papers before co-authored ones on ties (sort key `(display_year, year, month, first_author)`, descending).
- `arxiv_url`, `pub_page_url` — **bookkeeping only**: `arxiv_url` is used just as the title/teaser link fallback when `links` has no Paper/arXiv entry; `pub_page_url` is never rendered. Everything visible comes from `links`.
- `links`: [{label,url}] in display order. Labels understood by build.py: Paper (shown as "arXiv" when the URL is on arxiv.org), Publication Page (shown as OpenReview / ACL Anthology / NeurIPS by host), Project Page, Code, Dataset, Models, Demo, Leaderboard, HF Collection, Blog, Tweet, PDF. Anything else gets a generic link icon. Only add links you have opened. ClawBench deliberately has no publication-page link (its `pub_page_url` is the COLM 2026 WAB workshop page, not an EMNLP record).
- `summary` — one sentence, ≤ ~28 words, concrete, no hype. `highlight` — optional ≤12-word verified fact (e.g. "1,000+ GitHub stars", "Adopted by the Hugging Face Open LLM Leaderboard").
- `selected` — shown in the default view (currently the 6 first-author papers + ClawBench + Critique-Coder = 8). The "Selected" badge is emitted only for selected papers and shown only in the All view.
- `teaser` — `assets/img/teasers/<key>.webp` or null. null (or a missing file — build.py prints `WARNING: teaser missing` and treats it as null) renders a labelled dotted placeholder tile; the label is `SHORT_NAMES[key]` from build.py when present, otherwise the title up to the first colon. Adding a key to `SHORT_NAMES` is optional and only affects placeholder tiles.

`publications_meta` ({count, selected_count, has_equal_marks, has_core_marks}) is **recomputed by build.py** from the publication list and fills the Selected/All button numbers, the no-JS status line ("15 papers, 8 marked Selected.") and the legend; the copy in data.json is informational and may be left stale.

### 4.5 experience / education
`{role|degree, org, org_url, where (experience only — the education template ignores it), dates, logo, logo_square (optional square mark for wide wordmarks, used in the 52 px tile), logo_text (fallback monogram when no logo), details (raw HTML)}`. Empty `dates`/`where`/`details` are simply omitted. Order = newest first.

### 4.6 affiliation_logos
The logo strip between News and Publications: [{name,url,logo}]. Wordmarks (aspect > 1.8) automatically get the `is-wordmark` class (rendered at 72 % plate height).

### 4.7 footer / service
`footer.copyright`, `footer.updated` ("Last updated: October 2026" — **bump it whenever content changes**), `footer.credit`. `service` is null (section hidden); set `{"reviewing": "…"}` to show a Service section.

## 5. Build, deploy, verify

**Recipe — add a paper (≈15 min):**
1. Cut the teaser (§7.1) → `assets/img/teasers/<key>.webp` (name the PNG `<key>.png` so `teaser_webp.py` produces the right filename).
2. Append the publication object to `_src/data.json → publications` (template in §4.4; `selected: true` to show it by default; `teaser: null` is allowed).
3. Prepend a `news` item (§4.3). If the paper is representative, add it to `about.interests` too.
4. Bump `footer.updated`.
5. `python3 _src/build.py` — read stderr: `WARNING: teaser missing for <key>` / `logo missing` mean a wrong path (the build still succeeds and silently falls back to a placeholder). The build also rewrites `sitemap.xml`.
6. Run the checks below, open the screenshots, then commit and push; verify the live page (§1).

**Recipe — change a date / title / tagline:** edit every place listed in §2 "Where each fact lives", rebuild, rerun `_src/tools/make_icons.py` if the tagline/eyebrow/name changed (it regenerates og.png from data.json), run the checks, push.

```bash
# from the repository root
python3 _src/build.py            # -> index.html, style.css, script.js, sitemap.xml
python3 - <<'EOF'                # HTML sanity (tags balanced)
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
python3 - <<'EOF'                # no horizontal overflow + live counts (Playwright)
import os, sys; sys.path.append('/home/ubowang_google_com/.local/lib/python3.10/site-packages')
from playwright.sync_api import sync_playwright
url = 'file://' + os.path.abspath('index.html')
with sync_playwright() as p:
    b = p.chromium.launch()
    for w in (320, 360, 375, 414, 768, 1024, 1280):
        pg = b.new_page(viewport={'width': w, 'height': 900}); pg.goto(url, wait_until='networkidle'); pg.wait_for_timeout(300)
        sw = pg.evaluate('document.documentElement.scrollWidth'); print(w, 'OK' if sw <= w else f'OVERFLOW scrollWidth={sw}'); pg.close()
    pg = b.new_page(viewport={'width': 1280, 'height': 900}); pg.goto(url, wait_until='networkidle'); pg.wait_for_timeout(500)
    print(pg.inner_text('.pubs-status'), '|', [pg.inner_text(f'.seg button[data-view={v}]') for v in ('selected', 'all')])
    b.close()
EOF
python3 _src/tools/shot.py file://$PWD/index.html /tmp/desktop.png 1280 full light
python3 _src/tools/shot.py file://$PWD/index.html /tmp/mobile.png 375 full light
python3 _src/tools/shot.py file://$PWD/index.html /tmp/dark.png 1280 viewport dark
# Auth on a new machine: gh auth login && gh auth setup-git
git add -A && git commit -m "…" && git push origin main      # the push triggers the Pages build (see §1 for verification)
```

Acceptance checklist before pushing (all green on 2026-10-15):
1. No overflow at 320–1280 px and the status line / button counts match the number of papers (snippet above).
2. Light and dark screenshots look intentional (dark: images are dimmed automatically, §6).
3. Selected/All toggle: counts, `aria-pressed`, status line ("Showing N selected of M papers." / "Showing all M papers."); the "Selected" badge is visible only in the All view.
4. Every new URL opened manually; arXiv ids match titles.
5. `footer.updated` bumped (sitemap `lastmod` is automatic).
6. If the photo, name, eyebrow, tagline or affiliations changed: `python3 _src/tools/make_icons.py` rerun and `assets/img/og.png` checked. Social scrapers cache cards for days.

Cache note: the `?v=` query on css/js is the build *date*; a second deploy on the same day keeps the same cache-buster, and GitHub Pages serves with `Cache-Control: max-age=600`, so returning visitors may see the old CSS for up to 10 minutes.

## 6. Design system (why it looks the way it does)

References the owner chose: https://jdf-prog.github.io/ (Dongfu Jiang; information architecture: hero pills/chips, logo strip, badges, timeline rows) and https://haozheh3.github.io/ (Haozhe Wang; calm teaser-left publication rows, one-line summaries, show selected/all), secondary https://cs.uwaterloo.ca/~w2ren/ (Weiming Ren). Three full variants were built and judged (visual, usability, code/a11y lenses); the editorial-minimal variant won and was merged with the best ideas of the others, then fixed per a 5-lens QA pass. The saved variants/screenshots are not in the repo (see §9).

Tokens (`:root` in `_src/style.css`). **Every colour token is declared twice**: a plain light value in `:root` (fallback for browsers without `light-dark()`) and a `light-dark(light, dark)` value inside `@supports (color: light-dark(#000, #fff))`. Modern browsers honour only the second block — editing the plain line alone changes nothing. Keep the light value identical in both places.
- Background `#faf8f3` / dark `#171614`; elevated `#f1ede5` / `#201f1b`; image plate `#ffffff` / `#dcd9d2`.
- Ink `#1e1c19` / `#ebe7df`, ink-2 `#4f4b45` / `#b9b3a8`, ink-3 `#6f6a62` / `#908a7f` (ink-3 measures 5.06:1 light / 5.28:1 dark on `--bg` and 4.60 / 4.81 on `--bg-elev`; the one sub-AA pairing is dark ink-3 on dark `--accent-soft` = 4.34:1, which only occurs inside a `.pub:target` row after a deep link).
- Accent teal `#1f6b63` / `#7cc7bb` (links, chips, active segment), accent-ink `#175b54` / `#9ad9cf`, accent-soft `#e3eeeb` / `#1c2a28`, pre-mixed `--accent-40/50` for browsers without `color-mix()`; venue badge umber `#6a5a3a` on `#f0eadd` (dark `#c9b68f` on `#272319`; 5.6:1 / 7.9:1).
- Type: Newsreader 500 for name, section titles, year labels, publication titles; Inter 400/500/600 for everything else; body 17 px / 1.65; measure 880 px; the CJK name uses system CJK fonts.
- Layout: single column; hero = text + 168×210 photo (grid, centred); sections separated by hairlines, not cards; publication row = `--figure-w` 240 px plate (16:9, `object-fit: contain`, white plate) + text; the year label shares the figure column; hover tint on rows.
- Breakpoints: ≤900 px (figure 184 px, photo 144 px), ≤720 px (hero becomes photo-beside-name via `display: contents`, single-column pub rows, stacked footer), ≤640 px (header becomes a static two-row block: brand + theme toggle, then all five links; no horizontal scrolling), ≤340 px (tighter nav).
- Theme: follows the OS; the toggle persists to localStorage and is forgotten again when the choice matches the OS; constant accessible name "Dark theme" with `aria-pressed`. Dark-mode dimming is automatic for any `<img>` inside `.pub-figure`, `.logo-plate`, `.mono` or `.hero-photo` (`filter: brightness(.88) contrast(1.02)`, declared once for `[data-theme="dark"]` and once for the OS dark preference) — new teasers/logos need nothing; an image placed elsewhere must be added to **both** selector lists. Never create dark variants of images; they sit on the white plate.
- Icons: inline SVG sprite, `<svg class="icon"><use href="#i-github"/></svg>`; no icon-font CDNs.
- Accessibility: landmarks, fixed-position skip link, one h1, heading order h1→h2→h3 (year)→h4 (title), `role="list"` on styled lists, focus rings, `aria-live` status for the filter, reduced-motion handling, print stylesheet prints all papers/news.
- No-JS: all papers and news visible; toggle/controls hidden; status line reads "15 papers, 8 marked Selected."

**Recolouring a badge (both themes).** Venue badge = `.badge-venue { background: var(--venue-bg); color: var(--venue); }`; distinction badge uses `--accent-soft`/`--accent-ink`; the Selected badge uses `--accent-ink` text with an `--accent-40` border. Procedure: (1) edit the token on both declarations (plain and `light-dark()`); (2) keep text/background contrast ≥ 4.5:1 in each theme (badges are 12 px semibold); (3) `python3 _src/build.py`; (4) check both themes with `shot.py … light` / `… dark`, or read `getComputedStyle(document.querySelector('.badge-venue')).backgroundColor` in a Playwright context with `color_scheme='dark'`.

## 7. Assets and how they were made

### 7.1 Publication teasers
Owner requirement: each teaser is cut from the paper itself — the **method/system/pipeline overview figure**, or the conceptual teaser (usually Fig. 1) — never a results table. Procedure with `_src/tools/pdfkit.py` (PyMuPDF):
```bash
python3 _src/tools/pdfkit.py info  PAPER.pdf 3            # captions, image rects, drawing clusters, SUGGESTED figure bbox per caption, text blocks (PDF points, origin top-left)
python3 _src/tools/pdfkit.py page  PAPER.pdf 3 /tmp/p3.png --zoom 2 --grid   # page with a labelled 50-pt grid to read coordinates off
python3 _src/tools/pdfkit.py clip  PAPER.pdf 3 X0 Y0 X1 Y1 /tmp/<key>.png --zoom 4   # crop + auto-trim white margins (pad 12 px)
python3 _src/tools/teaser_webp.py /tmp/<key>.png --out assets/img/teasers   # -> assets/img/teasers/<key>.webp (≤1000 px wide, q88); prints ratio=
```
`X0 Y0 X1 Y1` are placeholders — take them from `info` ("suggested figure bbox" under the right caption) or from the `--grid` render. `info` only recognises text blocks starting with "Figure N:" / "Fig. N.", so a page without such a caption legitimately prints `captions: 0` — move to the page with the overview figure. **Name the PNG after the publication key**: `teaser_webp.py` names the WebP after the PNG basename and `data.json` `teaser` must be `assets/img/teasers/<key>.webp`. Rules used: exclude caption/body text/arXiv stamp; include all panels and legends; aim for aspect 1.25–2.4 (the plate is 16:9 with letterboxing); if a figure is very wide, crop the overview sub-panel (done for FIM: left+middle panels of Fig. 1; ClawBench: left+middle of Fig. 1). Every crop was reviewed visually; coordinates are recorded in `_src/provenance/research.json → teasers[]` (add new ones there if you want the provenance to stay complete).

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
| `mmlu-pro` | NeurIPS 2024 · Spotlight | yes | 1st/17 | p.4 Fig. 2 (1291×762) | https://proceedings.neurips.cc/paper_files/paper/2024/hash/ad236edc564f3e3156e1b2feafb99a24-Abstract-Datasets_and_Benchmarks_Track.html |
| `map-neo` | Tech Report 2024 | no | 35/45 | p.11 Fig. 4 (1522×657) | — |
| `llm-amt` | Findings of EMNLP 2024 | yes | 1st/3 | p.2 Fig. 1 (1696×1420) | https://aclanthology.org/2024.findings-emnlp.95/ |

Notes: RewardHarness's COLM camera-ready title differs ("RewardHarness: Learning Human Preferences for Image Editing with Only 100 Demonstrations"); the site uses the arXiv title. ClawBench's EMNLP 2026 Findings record is not in the ACL Anthology yet (conference 24–29 Oct 2026) — when it appears, add `{"label": "Publication Page", "url": "<anthology URL>"}` to its `links` (and copy it to `pub_page_url`). MAmmoTH-VL's HF demo Space is down (RUNTIME_ERROR) and was removed. MMLU-Pro's OpenReview forum is `y10DM6R2r3`; Spotlight is confirmed by the arXiv comment and OpenReview.

### 7.2 Logos
`uwaterloo.png` (UW shield from the uwaterloo.ca site icon), `vector.png` (official EN lockup SVG from vectorinstitute.ai), `ucdavis.png` (Wikimedia Commons seal, PD file), `zju.png` (ZJU emblem SVG via Wikipedia; a non-free emblem hosted under fair use), `tencent.png` (Commons wordmark) + `tencent_mark.png` (site icon), `minimax.png` (official CDN PNG), `google.png` (Commons "Google G logo", public domain; added 2026-10-15 after the research pass). All trademarks are used nominatively to indicate affiliation. Provenance lives in `_src/provenance/research.json → logos` with two caveats: it still contains an `hkust` entry (the HKUST role was removed — do not resurrect the logo) and has no entry for `google.png`; the sizes recorded there are the scratch originals (256 px tall / 640 px wide) — repo copies were resized to 160 px tall except `tencent.png`. Logos sit on white plates in both themes, so dark variants are unnecessary. Keep new logos RGBA and trimmed, 160 px tall for marks; a wide wordmark may stay wider than tall but then add a square `*_mark.png` and reference it as `logo_square` for the experience/education tiles.

### 7.3 Photo, favicon, social card
`profile.jpg` is a 4:5 crop of the owner's photo; `profile-432/648.webp` are srcset variants (regenerate with Pillow if the photo changes: resize to 432 and 648 px wide, WebP q86). `favicon.svg` = teal rounded square with a serif "Y". `favicon-32.png`, `apple-touch-icon.png` and `og.png` (1200×630: eyebrow, name + 王钰博, tagline, affiliations, photo) are produced by `_src/tools/make_icons.py` (Playwright + Chromium; loads Inter/Newsreader from Google Fonts, so it needs network; writes directly into `assets/img/`; a rerun without changes is byte-identical, so a git diff means a real change). The card text is read from `_src/data.json → profile` (`eyebrow`, `name`, `name_cn`, `tagline` or the optional shorter `og_tagline`, `affiliations`) — rerun the script after changing any of them or the photo, then look at `assets/img/og.png`.

### 7.4 Icons
**Adding an icon** (e.g. an ORCID pill): 1) add `'i-orcid': (AI + 'orcid.svg', None)` to `ICONS` in `_src/tools/make_sprite.py` (FA = Font Awesome Free 6.5.2, AI = Academicons 1.9.6, both on jsDelivr; give a FA fallback for Academicons ids); 2) `python3 _src/tools/make_sprite.py` — needs network, rewrites `_src/icons.svg`; rerunning it unchanged reproduces the committed sprite byte-for-byte; 3) map it: for a hero/footer pill add `'orcid': 'i-orcid'` to `ICONS` in `_src/build.py` and use `"icon": "orcid"` in `profile.links`; for a publication link add the display label to `LINK_ICONS` (unknown labels fall back to `i-link`); 4) `python3 _src/build.py` — the sprite is inlined by `{% include 'icons.svg' %}` in the template. The script strips `<title>`, `fill`, `class` and `id` attributes from the source SVGs so icons inherit `currentColor` and add no tooltips.

## 8. Publications policy
- Default view shows `selected` papers; everything else is one click away. Keep "Selected" = first-author papers + the most significant co-authored ones (ask the owner before changing the set).
- Author strings are copied from the paper/arXiv order; never reorder. Mark equal/core contribution exactly as the paper does.
- Venue badge shows the final venue once accepted ("Findings of EMNLP 2026"); arXiv year only for preprints. When a preprint is accepted: set `venue_short` (badge text) and `venue_long`; **add `{"label": "Publication Page", "url": "<OpenReview / Anthology / proceedings URL>"}` as the second entry of `links`** — that is the only thing that renders a link (build.py relabels it OpenReview / ACL Anthology / NeurIPS by host); copy the same URL into `pub_page_url` for the record; put Spotlight/Oral/Best Paper wording in `distinction` (it becomes the second badge); add a 🎉 news item; optionally set `selected: true`; bump `footer.updated`.
- Link order: arXiv first, then publication page, project page, code, data/models, demo/leaderboard, HF collection, blog, tweet.

## 9. The original scratch workspace (not in git)
`/rmeng_data/yubo_data/October/yubo/website_work/` on the machine where the site was built: `design_variants/v1..v3` (the three candidate designs with screenshots), `design_assets/DESIGN_BRIEF.md` (the brief given to the designers), `teasers/*.png` (full-resolution crops), `pages/` (all review screenshots), `data/research.json` + `qa.json` + `design_panel.json` + `handover_critique.json` (full agent outputs), `arxiv_pdfs/` (downloaded co-author PDFs), `scripts/` (originals of the tools). Owner-provided source material: `/rmeng_data/yubo_data/test_data/huayu_service_v2607/personal_website_yubo/` (photo, Google Scholar screenshot of 2026-10-14, 6 first-author PDFs in `papers/`, 2 co-author PDFs in `co-papers/`). If that machine is gone, everything needed to maintain the site is in this repository.

## 10. History and decisions (short)
- 2026-10-15: replaced the al-folio/Jekyll site (owner found it ugly). Design chosen by a 3-variant panel + 3 judges; v1 "editorial-minimal" won (22.9 vs 21.8 vs 20.3), then merged with v3's mobile nav/status line and v2's icon pills/logo strip. A 5-lens QA pass (links, content/facts, visual+interaction, HTML/a11y/perf, design critique) produced 10 major / 25 minor fixes, all applied except re-cropping three tall teasers (LLM-AMT, MEGA-Bench, MMMU-Pro), which still letterbox a little.
- Same day, per owner feedback: removed Scholar stats, removed HKUST, added the Google CAIR role, shrank the photo, moved the logo strip below News, month-precise dates everywhere, PhD start May 2024, MiniMax description.
- GitHub Pages source switched from `gh-pages` to `main` via `gh api -X PUT repos/Wyyyb/wyyyb.github.io/pages -f 'source[branch]=main' -f 'source[path]=/'`.
- Handover: this document + tools + provenance committed; reviewed by a maintainer dry-run and a fact-check agent; build.py now derives `publications_meta`, `sitemap.xml`, `<title>` and `twitter:site`, and make_icons.py reads the card text from data.json.

## 11. Gotchas
- **LinkedIn cannot be fetched** by bots (HTTP 999, also for crawler UAs; no Wayback snapshots). Search-engine snippets worked once and then hit CAPTCHAs. Ask the owner for LinkedIn-sourced facts instead of guessing.
- In the original environment the WebSearch tool was blocked by org policy; curl + DuckDuckGo HTML / r.jina.ai / official APIs (arXiv export API, Hugging Face API, `gh api`, OpenReview api2 `notes/search`) were used instead. OpenReview forum pages and the profile API are behind a browser challenge.
- Headless Chromium there had no colour-emoji font: news emoji show as boxes in screenshots only. Real browsers are fine.
- Full-page screenshots can show blank teaser plates if taken before the idle prefetch runs (`loading="lazy"`; `script.js` switches images to eager in a `requestIdleCallback` (timeout 2 s) after `load`). `shot.py` waits for `networkidle` + 1.5 s; scroll first if plates still come out blank.
- `light-dark()` tokens live inside `@supports`; older browsers get the light theme and the theme toggle is hidden by `@supports not`. `color-mix()` uses pre-mixed fallbacks (`--accent-40/50`).
- `data-view` on `#publications` is set by script.js (not in the HTML), so no-JS shows the Selected badges — intended.
- `make_sprite.py` strips `<title>` from source SVGs; keep that behaviour when adding icons.
- Pushes to `main` trigger a Pages build by themselves; `gh api -X POST …/pages/builds` is only a fallback (a POST during a running build adds a harmless `errored, duration 0` entry).
- Google Scholar numbers were deliberately removed; don't add citation counts back without asking.

## 12. Backlog / ideas (none required)
- Add a CV: put the PDF at `assets/pdf/Yubo_Wang_CV.pdf` and add `{"label":"CV","url":"assets/pdf/Yubo_Wang_CV.pdf","icon":"cv"}` to `profile.links`.
- Service section (`service.reviewing`) once the owner lists reviewing duties.
- Re-crop LLM-AMT / MEGA-Bench / MMMU-Pro teasers to ~2:1 panels if the letterboxing bothers anyone.
- When ClawBench's Anthology page and the FIM paper's venue are known, update venue/links/news (§8).
- Optional: 404.html, analytics (none installed on purpose), Semantic Scholar/ORCID pills (§7.4).
