#!/usr/bin/env python3
"""Build index.html for wyyyb.github.io from _src/data.json + _src/template.html.j2.

Usage:  python3 _src/build.py [SITE_DIR]     (default SITE_DIR = repository root containing _src/)
Requires: jinja2, Pillow (only to read image sizes).
"""
import json, os, sys, re, datetime, shutil
from urllib.parse import urlparse

sys.path.append('/home/ubowang_google_com/.local/lib/python3.10/site-packages')
import jinja2
from PIL import Image

SRC = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.dirname(SRC)
data = json.load(open(os.path.join(SRC, 'data.json'), encoding='utf-8'))

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
# Icon ids refer to <symbol>s in _src/icons.svg (built by _src/tools/make_sprite.py from Font Awesome Free + Academicons).
ICONS = {
    'envelope': 'i-envelope', 'google-scholar': 'i-scholar', 'github': 'i-github',
    'x-twitter': 'i-x', 'linkedin': 'i-linkedin', 'cv': 'i-cv',
}
LINK_ICONS = {
    'arXiv': 'i-arxiv', 'Paper': 'i-file', 'Project Page': 'i-globe',
    'Code': 'i-github', 'Dataset': 'i-database', 'Models': 'i-cube',
    'Demo': 'i-play', 'Leaderboard': 'i-ranking', 'HF Collection': 'i-layers',
    'Blog': 'i-pen', 'Tweet': 'i-x', 'OpenReview': 'i-book',
    'ACL Anthology': 'i-book', 'NeurIPS': 'i-book', 'Publication Page': 'i-book',
    'PDF': 'i-cv',
}
SHORT_NAMES = {
    'fim-midtraining': 'FIM Mid-Training', 'one-shot-cft': 'One-shot CFT', 'scholarcopilot': 'ScholarCopilot', 'cft': 'CFT',
    'mmlu-pro': 'MMLU-Pro', 'llm-amt': 'LLM-AMT', 'clawbench': 'ClawBench', 'critique-coder': 'Critique-Coder',
    'minimax-m2': 'MiniMax-M2', 'rewardharness': 'RewardHarness', 'supergpqa': 'SuperGPQA', 'mmmu-pro': 'MMMU-Pro',
    'mammoth-vl': 'MAmmoTH-VL', 'mega-bench': 'MEGA-Bench', 'map-neo': 'MAP-Neo',
}


def img_size(rel):
    p = os.path.join(SITE, rel)
    try:
        with Image.open(p) as im:
            return im.size
    except Exception:
        return (None, None)


def link_view(l):
    label, url = l['label'], l['url']
    host = urlparse(url).netloc
    title = None
    if label == 'Paper' and 'arxiv.org' in host:
        label = 'arXiv'
    elif label == 'Publication Page':
        if 'openreview.net' in host: label = 'OpenReview'
        elif 'aclanthology.org' in host: label = 'ACL Anthology'
        elif 'neurips.cc' in host: label = 'NeurIPS'
    if label == 'Tweet':
        title = 'Announcement on X'
    return {'label': label, 'url': url, 'icon': LINK_ICONS.get(label, 'i-link'), 'title': title}


def distinction_badge(d):
    d = (d or '').strip()
    for k in ('Best Paper', 'Outstanding', 'Oral', 'Spotlight', 'Highlight'):
        if k.lower() in d.lower():
            return k
    return ''


# ---- publications -> year groups ----
pubs = []
for pub in data['publications']:
    v = dict(pub)
    v['short_name'] = SHORT_NAMES.get(pub['key'], pub['title'].split(':')[0])
    v['distinction_badge'] = distinction_badge(pub.get('distinction'))
    links = [link_view(l) for l in pub['links']]
    # keep one of arXiv/Paper first
    v['links'] = links
    v['primary_url'] = next((l['url'] for l in links if l['label'] in ('arXiv', 'Paper')), pub.get('arxiv_url') or (links[0]['url'] if links else '#'))
    v.setdefault('month', 1); v.setdefault('selected', False); v.setdefault('first_author', False)
    v.setdefault('authors_html', ''); v.setdefault('summary', ''); v.setdefault('highlight', ''); v.setdefault('distinction', '')
    if pub.get('teaser'):
        w, h = img_size(pub['teaser'])
        if w is None:
            print(f"WARNING: teaser missing for {pub['key']}: {pub['teaser']}", file=sys.stderr)
            v['teaser'] = None
        else:
            v['teaser_w'], v['teaser_h'] = w, h
    pubs.append(v)
def display_year(p):
    """Group by publication year when the paper has a venue; preprints/tech reports use the arXiv year."""
    vs = p['venue_short']
    m = re.search(r'(20\d\d)', vs)
    if m and not re.match(r'(arXiv|Tech Report|Preprint)', vs, re.I):
        return int(m.group(1))
    return p['year']
for p in pubs:
    p['display_year'] = display_year(p)
pubs.sort(key=lambda p: (p['display_year'], p['year'], p['month'], p.get('first_author', False)), reverse=True)
# publications_meta is derived here (the value in data.json is informational only)
pubs_meta = {
    'count': len(pubs), 'selected_count': sum(1 for p in pubs if p['selected']),
    'has_equal_marks': any('*' in p['authors_html'] for p in pubs), 'has_core_marks': any('†' in p['authors_html'] for p in pubs),
}
groups = []
for p in pubs:
    if not groups or groups[-1]['year'] != p['display_year']:
        groups.append({'year': p['display_year'], 'pubs': []})
    groups[-1]['pubs'].append(p)

# ---- news ----
news = []
for n in data['news']:
    y, m = n['date'].split('-')[:2]
    news.append(dict(n, date_label=f"{MONTHS[int(m) - 1]} {y}"))

# ---- logos & photo ----
def with_logo_size(rows):
    out = []
    for r in rows:
        r = dict(r)
        if r.get('logo_square') and img_size(r['logo_square'])[0] is None:
            print(f"WARNING: square logo missing: {r['logo_square']}", file=sys.stderr); r['logo_square'] = None
        if r.get('logo'):
            w, h = img_size(r.get('logo_square') or r['logo'])
            if w is None:
                print(f"WARNING: logo missing: {r['logo']}", file=sys.stderr); r['logo'] = None
            else:
                r['logo_w'], r['logo_h'] = w, h
        out.append(r)
    return out

aff = []
for o in data.get('affiliation_logos', []):
    w, h = img_size(o['logo'])
    if w is None:
        print(f"WARNING: logo missing: {o['logo']}", file=sys.stderr); continue
    aff.append(dict(o, w=w, h=h, wordmark=(w / h) > 1.8))
photo_w, photo_h = img_size(data['profile']['photo_portrait'])
variants = [(f"assets/img/profile-{w}.webp", w) for w in (432, 648) if img_size(f"assets/img/profile-{w}.webp")[0]]
photo_srcset = ', '.join(f"{p} {w}w" for p, w in variants)

prof = data['profile']
scholar_url = next((l['url'] for l in prof['links'] if l['icon'] == 'google-scholar'), '#')
x_url = next((l['url'] for l in prof['links'] if l['icon'] == 'x-twitter'), '')
x_handle = ('@' + x_url.rstrip('/').rsplit('/', 1)[-1]) if x_url else ''
jsonld = {
    '@context': 'https://schema.org', '@type': 'Person',
    'name': prof['name'], 'alternateName': prof['name_cn'], 'url': prof['site_url'],
    'image': prof['site_url'] + prof['photo_portrait'], 'email': 'mailto:' + prof['email'],
    'jobTitle': prof['eyebrow'],
    'affiliation': [{'@type': 'Organization', 'name': a['name'], 'url': a['url']} for a in prof['affiliations']],
    'sameAs': [l['url'] for l in prof['links'] if not l['url'].startswith('mailto:')],
}

env = jinja2.Environment(loader=jinja2.FileSystemLoader(SRC), autoescape=True, trim_blocks=False, lstrip_blocks=False)
tpl = env.get_template('template.html.j2')
html = tpl.render(
    p=prof, about=data['about'], news=news, news_limit=6, pub_groups=groups, pubs_meta=pubs_meta,
    x_handle=x_handle, title_affiliation=(prof['affiliations'][0]['name'] if prof.get('affiliations') else ''),
    experience=with_logo_size(data['experience']), education=with_logo_size(data['education']),
    service=data.get('service'), footer=data['footer'], affiliation_logos=aff,
    photo_w=photo_w, photo_h=photo_h, photo_srcset=photo_srcset, scholar_url=scholar_url, repo_url='https://github.com/Wyyyb/wyyyb.github.io',
    build_id=datetime.date.today().strftime('%Y%m%d'), jsonld=json.dumps(jsonld, ensure_ascii=False),
    icon_id=lambda k: ICONS.get(k, 'i-link'),
)
html = re.sub(r'\n{3,}', '\n\n', html)
with open(os.path.join(SITE, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(html)
for fn in ('style.css', 'script.js'):
    shutil.copyfile(os.path.join(SRC, fn), os.path.join(SITE, fn))
with open(os.path.join(SITE, 'sitemap.xml'), 'w', encoding='utf-8') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>%s</loc><lastmod>%s</lastmod></url></urlset>\n'
            % (prof['site_url'], datetime.date.today().isoformat()))
print(f"built {os.path.join(SITE, 'index.html')} ({len(html.encode('utf-8'))//1024} KiB): {len(pubs)} publications ({pubs_meta['selected_count']} selected) in {len(groups)} year groups, {len(news)} news items, {len(aff)} logos; sitemap.xml lastmod {datetime.date.today().isoformat()}")
