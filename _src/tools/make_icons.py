import sys, os
sys.path.append('/home/ubowang_google_com/.local/lib/python3.10/site-packages')
from playwright.sync_api import sync_playwright
import os
W = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))  # repository root
svg = open(f'{W}/assets/img/favicon.svg').read()
import base64
b64 = base64.b64encode(open(f'{W}/assets/img/profile.jpg','rb').read()).decode()
icon_html = lambda size: f"""<html><head><style>html,body{{margin:0;background:transparent}}</style></head><body><div style="width:{size}px;height:{size}px">{svg.replace('width="64" height="64"', f'width="{size}" height="{size}"')}</div></body></html>"""
import json, html as _html
_d = json.load(open(f'{W}/_src/data.json', encoding='utf-8'))['profile']
_aff = ' · '.join(a['name'] for a in _d['affiliations'])
_tag = _d.get('og_tagline') or _d['tagline']          # optional shorter wording for the card: profile.og_tagline
og_html = f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Newsreader:opsz,wght@6..72,400;6..72,500&display=swap">
<style>
html,body{{margin:0}} body{{width:1200px;height:630px;background:#faf8f3;font-family:Inter,system-ui,sans-serif;color:#1e1c19;display:flex;align-items:center;justify-content:space-between;padding:72px 84px;box-sizing:border-box}}
.eyebrow{{font-size:20px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:#6f6a62;margin:0 0 18px}}
h1{{font-family:Newsreader,Georgia,serif;font-weight:500;font-size:84px;line-height:1.05;letter-spacing:-.015em;margin:0;display:flex;align-items:baseline;gap:22px}}
h1 span{{font-family:'Noto Sans SC','PingFang SC',sans-serif;font-size:40px;color:#6f6a62;font-weight:400;border-left:2px solid #cfc8bb;padding-left:22px}}
.tag{{font-family:Newsreader,Georgia,serif;font-size:30px;line-height:1.4;color:#4f4b45;margin:28px 0 0;max-width:660px}}
.aff{{font-size:22px;color:#6f6a62;margin:30px 0 0}} .aff b{{color:#1f6b63;font-weight:600}}
img{{width:300px;height:375px;object-fit:cover;border-radius:22px;border:1px solid #e5e0d6;box-shadow:0 2px 6px rgba(30,28,25,.08)}}
</style></head><body><div><p class="eyebrow">{_html.escape(_d['eyebrow'])}</p><h1>{_html.escape(_d['name'])} <span>{_html.escape(_d['name_cn'])}</span></h1>
<p class="tag">{_html.escape(_tag)}</p>
<p class="aff"><b>{_html.escape(_d['affiliations'][0]['name'])}</b>{(' · ' + _html.escape(' · '.join(a['name'] for a in _d['affiliations'][1:]))) if len(_d['affiliations']) > 1 else ''}</p></div><img src="data:image/jpeg;base64,{b64}"></body></html>"""

with sync_playwright() as p:
    b = p.chromium.launch()
    for size, name in ((32, 'favicon-32.png'), (180, 'apple-touch-icon.png')):
        pg = b.new_page(viewport={'width': size, 'height': size}, device_scale_factor=1)
        pg.set_content(icon_html(size)); pg.wait_for_timeout(300)
        pg.screenshot(path=f'{W}/assets/img/{name}', omit_background=True, clip={'x':0,'y':0,'width':size,'height':size})
        pg.close(); print('icon', name)
    pg = b.new_page(viewport={'width': 1200, 'height': 630}, device_scale_factor=1)
    pg.set_content(og_html); pg.wait_for_load_state('networkidle'); pg.wait_for_timeout(800)
    pg.screenshot(path=f'{W}/assets/img/og.png'); print('og.png')
    b.close()
