#!/usr/bin/env python3
"""Helper for extracting teaser figures from PDFs.

Subcommands:
  info   PDF PAGE                 -> print captions, image rects, drawing clusters, text blocks, auto-suggested figure bboxes
  page   PDF PAGE OUT.png [--zoom Z] [--grid]  -> render whole page (grid = labelled 50pt lines for coordinate estimation)
  clip   PDF PAGE X0 Y0 X1 Y1 OUT.png [--zoom Z] [--no-trim] [--pad P]  -> render a rectangle (PDF points, origin top-left) and trim white borders
All coordinates are PDF points with origin at the TOP-LEFT of the page (PyMuPDF convention). PAGE is 1-based.
"""
import sys
sys.path.append('/home/ubowang_google_com/.local/lib/python3.10/site-packages')
import argparse, re
import pymupdf
from PIL import Image, ImageDraw, ImageChops


def union(rects):
    r = pymupdf.Rect(rects[0])
    for x in rects[1:]:
        r |= pymupdf.Rect(x)
    return r


def caption_blocks(page):
    caps = []
    for b in page.get_text("dict")["blocks"]:
        if b["type"] != 0:
            continue
        s = " ".join(sp["text"] for l in b["lines"] for sp in l["spans"])
        s = re.sub(r"\s+", " ", s).strip()
        m = re.match(r"(Figure|Fig\.)\s*(\d+)\s*[:.]", s)
        if m:
            caps.append({"num": int(m.group(2)), "bbox": pymupdf.Rect(b["bbox"]), "text": s})
    return caps


def graphics_rects(page):
    rects = []
    for img in page.get_images(full=True):
        try:
            for r in page.get_image_rects(img[0]):
                if r.width > 5 and r.height > 5:
                    rects.append(("img", r))
        except Exception:
            pass
    for d in page.get_drawings():
        r = pymupdf.Rect(d["rect"])
        if r.width > 2 or r.height > 2:
            rects.append(("draw", r))
    return rects


def suggest_bbox(page, cap, rects):
    """Figure region above a caption: cluster graphics upward from the caption with gap < 28pt."""
    cb = cap["bbox"]
    cands = [r for _, r in rects if r.y1 <= cb.y0 + 3 and r.x1 > cb.x0 - 10 and r.x0 < cb.x1 + 10]
    if not cands:
        return None
    cands.sort(key=lambda r: -r.y1)
    cur = pymupdf.Rect(cands[0])
    for r in cands[1:]:
        if cur.y0 - r.y1 < 28:
            cur |= r
    # include text spans that fall inside/overlap the figure region (labels)
    txt = page.get_text("dict")
    pad = pymupdf.Rect(cur.x0 - 4, cur.y0 - 4, cur.x1 + 4, cur.y1 + 4)
    for b in txt["blocks"]:
        if b["type"] != 0:
            continue
        for l in b["lines"]:
            for sp in l["spans"]:
                sb = pymupdf.Rect(sp["bbox"])
                if sb.intersects(pad) and sb.y1 <= cb.y0 + 2:
                    inter = sb & pad
                    if inter.get_area() > 0.5 * sb.get_area():
                        cur |= sb
    cur = pymupdf.Rect(cur.x0 - 3, cur.y0 - 3, cur.x1 + 3, min(cur.y1 + 3, cb.y0))
    return cur & page.rect


def cmd_info(a):
    doc = pymupdf.open(a.pdf)
    page = doc[a.page - 1]
    print(f"page {a.page}/{len(doc)} size={page.rect.width:.0f}x{page.rect.height:.0f} pt")
    rects = graphics_rects(page)
    imgs = [r for k, r in rects if k == "img"]
    print(f"raster images: {len(imgs)}")
    for r in imgs[:20]:
        print(f"  img rect: {r.x0:.0f} {r.y0:.0f} {r.x1:.0f} {r.y1:.0f}")
    draws = [r for k, r in rects if k == "draw"]
    if draws:
        u = union(draws)
        print(f"vector drawings: {len(draws)} union: {u.x0:.0f} {u.y0:.0f} {u.x1:.0f} {u.y1:.0f}")
    caps = caption_blocks(page)
    print(f"captions: {len(caps)}")
    for c in caps:
        b = c["bbox"]
        print(f"  Figure {c['num']} caption bbox: {b.x0:.0f} {b.y0:.0f} {b.x1:.0f} {b.y1:.0f} | {c['text'][:150]}")
        s = suggest_bbox(page, c, rects)
        if s:
            print(f"    -> suggested figure bbox: {s.x0:.0f} {s.y0:.0f} {s.x1:.0f} {s.y1:.0f}  (w={s.width:.0f} h={s.height:.0f})")
        else:
            print("    -> no graphics found above caption")
    print("text blocks (bbox | first 60 chars):")
    for b in page.get_text("dict")["blocks"]:
        if b["type"] != 0:
            continue
        s = " ".join(sp["text"] for l in b["lines"] for sp in l["spans"])
        s = re.sub(r"\s+", " ", s).strip()
        r = pymupdf.Rect(b["bbox"])
        print(f"  {r.x0:4.0f} {r.y0:4.0f} {r.x1:4.0f} {r.y1:4.0f} | {s[:60]}")


def cmd_page(a):
    doc = pymupdf.open(a.pdf)
    page = doc[a.page - 1]
    pix = page.get_pixmap(matrix=pymupdf.Matrix(a.zoom, a.zoom), alpha=False)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    if a.grid:
        dr = ImageDraw.Draw(im)
        step = 50
        for x in range(0, int(page.rect.width) + 1, step):
            X = x * a.zoom
            dr.line([(X, 0), (X, im.height)], fill=(255, 120, 120), width=1)
            dr.text((X + 2, 2), str(x), fill=(200, 0, 0))
        for y in range(0, int(page.rect.height) + 1, step):
            Y = y * a.zoom
            dr.line([(0, Y), (im.width, Y)], fill=(120, 120, 255), width=1)
            dr.text((2, Y + 2), str(y), fill=(0, 0, 200))
    im.save(a.out)
    print(f"saved {a.out} {im.width}x{im.height} (zoom {a.zoom}, page {page.rect.width:.0f}x{page.rect.height:.0f} pt)")


def trim(im, pad):
    bg = Image.new(im.mode, im.size, (255, 255, 255))
    diff = ImageChops.difference(im, bg).convert("L")
    diff = diff.point(lambda p: 255 if p > 12 else 0)
    bbox = diff.getbbox()
    if not bbox:
        return im
    x0, y0, x1, y1 = bbox
    x0 = max(0, x0 - pad); y0 = max(0, y0 - pad)
    x1 = min(im.width, x1 + pad); y1 = min(im.height, y1 + pad)
    return im.crop((x0, y0, x1, y1))


def cmd_clip(a):
    doc = pymupdf.open(a.pdf)
    page = doc[a.page - 1]
    clip = pymupdf.Rect(a.x0, a.y0, a.x1, a.y1) & page.rect
    pix = page.get_pixmap(matrix=pymupdf.Matrix(a.zoom, a.zoom), clip=clip, alpha=False)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    if not a.no_trim:
        im = trim(im, a.pad)
    im.save(a.out)
    print(f"saved {a.out} {im.width}x{im.height} px (clip {clip.x0:.0f} {clip.y0:.0f} {clip.x1:.0f} {clip.y1:.0f}, zoom {a.zoom})")


p = argparse.ArgumentParser()
sub = p.add_subparsers(dest="cmd", required=True)
s = sub.add_parser("info"); s.add_argument("pdf"); s.add_argument("page", type=int); s.set_defaults(f=cmd_info)
s = sub.add_parser("page"); s.add_argument("pdf"); s.add_argument("page", type=int); s.add_argument("out"); s.add_argument("--zoom", type=float, default=2); s.add_argument("--grid", action="store_true"); s.set_defaults(f=cmd_page)
s = sub.add_parser("clip"); s.add_argument("pdf"); s.add_argument("page", type=int)
for k in ("x0", "y0", "x1", "y1"): s.add_argument(k, type=float)
s.add_argument("out"); s.add_argument("--zoom", type=float, default=4); s.add_argument("--no-trim", action="store_true"); s.add_argument("--pad", type=int, default=12); s.set_defaults(f=cmd_clip)
a = p.parse_args(); a.f(a)
