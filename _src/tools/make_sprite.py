#!/usr/bin/env python3
"""Download the icon SVGs used by the site and assemble an inline <svg> sprite at _src/icons.svg.
Font Awesome Free 6.5.2 icons: CC BY 4.0 (https://fontawesome.com/license/free). Academicons: SIL OFL 1.1."""
import re, sys, os, urllib.request
import os
W = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))  # repository root
FA = 'https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.5.2/svgs/'
AI = 'https://cdn.jsdelivr.net/gh/jpswalsh/academicons@1.9.6/svg/'
ICONS = {  # id: (source, fallback)
    'i-envelope': (FA + 'solid/envelope.svg', None),
    'i-scholar': (AI + 'google-scholar.svg', FA + 'solid/graduation-cap.svg'),
    'i-github': (FA + 'brands/github.svg', None),
    'i-x': (FA + 'brands/x-twitter.svg', None),
    'i-linkedin': (FA + 'brands/linkedin-in.svg', None),
    'i-arxiv': (AI + 'arxiv.svg', FA + 'regular/file-lines.svg'),
    'i-file': (FA + 'regular/file-lines.svg', None),
    'i-globe': (FA + 'solid/globe.svg', None),
    'i-database': (FA + 'solid/database.svg', None),
    'i-cube': (FA + 'solid/cube.svg', None),
    'i-play': (FA + 'solid/play.svg', None),
    'i-ranking': (FA + 'solid/ranking-star.svg', None),
    'i-layers': (FA + 'solid/layer-group.svg', None),
    'i-pen': (FA + 'solid/pen-nib.svg', None),
    'i-book': (FA + 'solid/book-open.svg', None),
    'i-link': (FA + 'solid/link.svg', None),
    'i-cv': (FA + 'regular/file-pdf.svg', None),
}
os.makedirs(f'{W}/_src/tools/_icon_sources', exist_ok=True)
def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode('utf-8')
symbols = []; report = []
for iid, (url, fb) in ICONS.items():
    svg = None; used = url
    for u in [url] + ([fb] if fb else []):
        try:
            svg = fetch(u); used = u; break
        except Exception as e:
            report.append(f'{iid}: {u} -> {e}')
    if not svg:
        print('FAILED', iid); continue
    open(f'{W}/_src/tools/_icon_sources/{iid}.svg', 'w').write(svg)
    vb = re.search(r'viewBox="([^"]+)"', svg).group(1)
    inner = re.sub(r'<!--.*?-->', '', svg, flags=re.S)
    inner = re.search(r'<svg[^>]*>(.*)</svg>', inner, re.S).group(1).strip()
    inner = re.sub(r'<title[^>]*>.*?</title>', '', inner, flags=re.S | re.I)  # no tooltip/title noise from the source SVGs
    inner = re.sub(r'\s+', ' ', inner)
    inner = re.sub(r'\s(fill|class|id)="[^"]*"', '', inner)  # inherit currentColor
    symbols.append(f'<symbol id="{iid}" viewBox="{vb}">{inner}</symbol>')
    report.append(f'{iid}: OK from {used.split("/")[-2]}/{used.split("/")[-1]} ({len(inner)} chars)')
sprite = ('<!-- Inline icon sprite. Font Awesome Free 6.5.2 icons (fontawesome.com) are CC BY 4.0; '
          'Academicons (jpswalsh.github.io/academicons) are SIL OFL 1.1. -->\n'
          '<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true">\n' + '\n'.join(symbols) + '\n</svg>')
open(f'{W}/_src/icons.svg', 'w').write(sprite)
print('\n'.join(report)); print('sprite bytes', len(sprite), 'symbols', len(symbols))
