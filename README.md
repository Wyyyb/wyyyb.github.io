# wyyyb.github.io

Personal academic homepage of **Yubo Wang (王钰博)** — https://wyyyb.github.io/

Plain HTML + CSS + a little vanilla JavaScript. No framework, no Jekyll, no build step required to deploy: GitHub Pages serves this branch (`main`, root) as-is.

## Layout

```
index.html          the page (generated from _src/, but hand-editable)
style.css           styles (light + dark theme; copied from _src/style.css)
script.js           Selected/All toggle, theme toggle, news "show more", nav highlight
assets/img/         profile photo, publication teasers (assets/img/teasers/*.webp), logos, favicon, og.png
_src/data.json      ALL site content: profile, about, news, publications, experience, education
_src/template.html.j2 + _src/build.py   generator (python3 + jinja2 + Pillow)
_src/tools/         pdfkit.py (cut teasers from PDFs), teaser_webp.py, shot.py (screenshots), make_icons.py, make_sprite.py
_src/provenance/    verified publication metadata with sources (research.json), paper manifest, original content block
HANDOVER.md         full handover document for future maintainers / agents
```

## How to update the site

**Option A — edit the data file, then rebuild (recommended)**

1. Edit `_src/data.json`:
   - a new paper → add an object to `publications` (`key`, `title`, `authors_html` with `<b>Yubo Wang</b>`, `venue_short`, `year`, `month`, `links`, `summary`, `selected`, `teaser` path), and drop its teaser image into `assets/img/teasers/`;
   - a new news item → prepend to `news` (`date: "YYYY-MM"`, `emoji`, `html`);
   - dates/roles → `experience`, `education`.
2. Run `python3 _src/build.py` from the repository root (needs `pip install jinja2 pillow`). It rewrites `index.html`, `style.css` and `script.js`.
3. Commit and push to `main`. If GitHub Pages does not pick it up within a minute, request a build: `gh api -X POST repos/Wyyyb/wyyyb.github.io/pages/builds`.

**Option B — edit `index.html` directly.** Every publication, news item and row is a clearly delimited block (`<!-- PUB: key --> … <!-- /PUB: key -->`). If you go this route, stop running the generator (it would overwrite your edits) or mirror the change in `_src/data.json`.

## Handover

**Read `HANDOVER.md` first** if you are maintaining or redesigning this site (content model, design system, asset provenance, build/deploy/QA procedure, owner facts and preferences, gotchas).

## Notes

- Teaser images were cropped from the papers' method-overview figures (see each paper's PDF) and encoded as WebP, 1000 px wide.
- Fonts: Newsreader + Inter from Google Fonts (system-font fallback if the CDN is unreachable). Icons are an inline SVG sprite (`_src/icons.svg`, Font Awesome Free + Academicons), so no icon-font CDN is needed.
- The previous al-folio/Jekyll version of the site is preserved on the `al-folio-archive` branch.
- Design inspired by the homepages of Jon Barron, Haozhe Wang and Dongfu Jiang.
