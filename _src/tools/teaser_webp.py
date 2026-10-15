#!/usr/bin/env python3
"""Convert teaser PNGs (output of pdfkit.py clip) into the site's WebP format.
Usage: python3 teaser_webp.py SRC.png [SRC2.png ...] --out assets/img/teasers   (max width 1000 px, quality 88)"""
import sys, os
sys.path.append('/home/ubowang_google_com/.local/lib/python3.10/site-packages')  # harmless elsewhere
from PIL import Image
args = sys.argv[1:]
out = 'assets/img/teasers'
if '--out' in args:
    i = args.index('--out'); out = args[i + 1]; args = args[:i] + args[i + 2:]
os.makedirs(out, exist_ok=True)
for f in args:
    im = Image.open(f).convert('RGB'); w, h = im.size; maxw = 1000
    if w > maxw:
        im = im.resize((maxw, round(h * maxw / w)), Image.LANCZOS)
    dst = os.path.join(out, os.path.splitext(os.path.basename(f))[0] + '.webp')
    im.save(dst, 'WEBP', quality=88, method=6)
    print(f"{dst}: {im.size[0]}x{im.size[1]} ratio={im.size[0]/im.size[1]:.2f} {os.path.getsize(dst)//1024} KB")
