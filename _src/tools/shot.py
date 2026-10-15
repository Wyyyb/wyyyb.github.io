import sys
sys.path.append('/home/ubowang_google_com/.local/lib/python3.10/site-packages')
from playwright.sync_api import sync_playwright
url, out = sys.argv[1], sys.argv[2]
width = int(sys.argv[3]) if len(sys.argv) > 3 else 1280
full = (sys.argv[4] != "viewport") if len(sys.argv) > 4 else True
scheme = sys.argv[5] if len(sys.argv) > 5 else "light"
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": width, "height": 900}, device_scale_factor=1, color_scheme=scheme)
    pg = ctx.new_page()
    pg.goto(url, wait_until="networkidle")
    pg.wait_for_timeout(1500)
    pg.screenshot(path=out, full_page=full)
    print("saved", out)
    b.close()
