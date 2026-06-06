"""
Calxo.in — Daily Petrol Price Card Image Generator
Builds one 1200×630 PNG card per city from data/petrol-prices.json. The
cards live at static/images/petrol/petrol-price-<slug>.png and are picked
up by each city page (inline article image + og:image + twitter:image) and
by sitemap-images.xml for Google Images.

Run order in CI:
  1. update-petrol-prices.py    (refresh data/petrol-prices.json)
  2. generate-petrol-pages.py   (regenerate 27 derived city pages)
  3. generate-petrol-images.py  (this — render PNG cards with today's price)
  4. git commit + push          (handled by the workflow)

Image SEO baked in:
  • Descriptive filename `petrol-price-<slug>.png` (keyword match)
  • Stable URL (Google can re-crawl the same path daily)
  • Width/height attributes set in the Hugo page → no CLS
  • Alt text rendered by the page template includes the live price + date
  • Schema.org ImageObject added on the page (separate work)
  • Card text is large enough to be readable in search image carousels

Idempotent: re-running produces byte-identical output for the same JSON,
so empty diffs naturally skip git commits.
"""

import json, os, sys
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO_DIR  = Path(__file__).parent.parent
DATA_FILE = REPO_DIR / "data" / "petrol-prices.json"
OUT_DIR   = REPO_DIR / "static" / "images" / "petrol"

# Slug overrides where the URL differs from a plain slugify of the city name.
# (Matches generate-petrol-pages.py.)
SLUG_OVERRIDE = {
    "Bengaluru": "bangalore",
}


def slugify(city: str) -> str:
    return SLUG_OVERRIDE.get(city, city.lower().replace(" ", "-"))


# ── Layout constants ──────────────────────────────────────────────────────
W, H = 1200, 630
PADDING = 64

# Brand palette (matches the site)
NAVY   = (15,  23,  42)    # #0f172a — deepest text
INDIGO = (30,  58, 138)    # #1e3a8a
BLUE   = (37,  99, 235)    # #2563eb
CYAN   = (6,  182, 212)    # #06b6d4
WHITE  = (255, 255, 255)
MUTED  = (191, 219, 254)   # #bfdbfe — translucent blue text


# ── Font discovery — works on Ubuntu GH runners + local macOS ─────────────
def _font(size: int, weight: str = "Bold") -> ImageFont.FreeTypeFont:
    """Return a TrueType font that supports the ₹ glyph.

    Tested chain:
      1. DejaVu Sans (Ubuntu default, has ₹ since 2.37)
      2. Noto Sans (newer Ubuntu)
      3. Helvetica.ttc (macOS, only basic ₹ support)
      4. Arial Bold (macOS extras)
    """
    candidates = [
        # Linux (GitHub Actions runner)
        f"/usr/share/fonts/truetype/dejavu/DejaVuSans-{weight}.ttf",
        f"/usr/share/fonts/truetype/noto/NotoSans-{weight}.ttf",
        # macOS
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        # macOS HomeBrew / fontconfig
        "/opt/homebrew/share/fonts/DejaVuSans-Bold.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    # Should not happen, but fall back to a default raster font so the script
    # never crashes — output just looks plain.
    return ImageFont.load_default()


def _lerp_color(a, b, t):
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))


def _draw_gradient(img: Image.Image, top, bottom) -> None:
    """Vertical gradient (no numpy required)."""
    draw = ImageDraw.Draw(img)
    for y in range(H):
        draw.line([(0, y), (W, y)], fill=_lerp_color(top, bottom, y / H))


def _draw_grid_overlay(img: Image.Image) -> None:
    """Subtle white grid like the on-site result cards, for that 'data' feel."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    step = 28
    line_color = (255, 255, 255, 14)   # ~5% opacity
    for x in range(0, W, step):
        draw.line([(x, 0), (x, H)], fill=line_color, width=1)
    for y in range(0, H, step):
        draw.line([(0, y), (W, y)], fill=line_color, width=1)
    img.alpha_composite(overlay)


# ── Single card render ────────────────────────────────────────────────────
def render_card(city: str, state: str, petrol: float, diesel: float,
                date_iso: str, out_path: Path,
                footer_url: str | None = None) -> None:
    """Render one city's daily price card.

    `footer_url` overrides the default `calxo.in/conversion/petrol-price-<slug>/`
    when the slug doesn't follow the per-city pattern (e.g. the national card)."""
    # Pretty date e.g. "6 June 2026"
    dt = datetime.strptime(date_iso, "%Y-%m-%d")
    nice_date = dt.strftime("%-d %B %Y")

    # Canvas
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    _draw_gradient(img, INDIGO, BLUE)
    _draw_grid_overlay(img)
    draw = ImageDraw.Draw(img)

    # Fonts (sized to fit a 1200×630 canvas without overlap)
    f_brand     = _font(38, "Bold")
    f_section   = _font(28, "Bold")
    f_city      = _font(82, "Bold")
    f_state     = _font(28, "Bold")
    f_label     = _font(28, "Bold")
    f_petrol    = _font(150, "Bold")
    f_unit      = _font(40, "Bold")
    f_diesel_lbl= _font(28, "Bold")
    f_diesel    = _font(52, "Bold")
    f_meta      = _font(24, "Bold")

    # ── Header row ───────────────────────────────────────────────────────
    draw.text((PADDING, PADDING - 8), "calxo", fill=WHITE, font=f_brand)
    draw.text((PADDING + 158, PADDING + 6),
              "Daily Indian Fuel Price Tracker",
              fill=MUTED, font=f_meta)

    # Top-right badge
    badge_text = "PETROL PRICE TODAY"
    bb = draw.textbbox((0, 0), badge_text, font=f_section)
    badge_w = bb[2] - bb[0]
    badge_x = W - PADDING - badge_w - 20
    badge_y = PADDING - 4
    pad_x, pad_y = 18, 10
    draw.rounded_rectangle(
        [(badge_x - pad_x, badge_y - pad_y),
         (badge_x + badge_w + pad_x, badge_y + (bb[3] - bb[1]) + pad_y)],
        radius=14, fill=CYAN,
    )
    draw.text((badge_x, badge_y), badge_text, fill=NAVY, font=f_section)

    # ── City + state ─────────────────────────────────────────────────────
    draw.text((PADDING, 124), city.upper(), fill=WHITE, font=f_city)
    draw.text((PADDING, 218), f"{state}, India", fill=MUTED, font=f_state)

    # ── Big petrol price ─────────────────────────────────────────────────
    label_y = 264
    draw.text((PADDING, label_y), "PETROL", fill=MUTED, font=f_label)

    price_text = f"₹ {petrol:.2f}"
    price_y = label_y + 34
    draw.text((PADDING, price_y), price_text, fill=WHITE, font=f_petrol)

    pb = draw.textbbox((0, 0), price_text, font=f_petrol)
    price_w = pb[2] - pb[0]
    draw.text((PADDING + price_w + 16, price_y + 90),
              "/ litre", fill=MUTED, font=f_unit)

    # ── Diesel inline (well below the big price) ─────────────────────────
    diesel_y = 478
    draw.text((PADDING, diesel_y + 16), "DIESEL", fill=MUTED, font=f_diesel_lbl)
    draw.text((PADDING + 122, diesel_y),
              f"₹ {diesel:.2f} / litre",
              fill=WHITE, font=f_diesel)

    # ── Footer pinned to bottom edge ─────────────────────────────────────
    footer_y = H - PADDING + 6
    draw.text((PADDING, footer_y), f"Updated: {nice_date}",
              fill=MUTED, font=f_meta)
    src_text = footer_url or ("calxo.in/conversion/petrol-price-" + slugify(city) + "/")
    sb = draw.textbbox((0, 0), src_text, font=f_meta)
    src_w = sb[2] - sb[0]
    draw.text((W - PADDING - src_w, footer_y), src_text,
              fill=MUTED, font=f_meta)

    # Save as PNG
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(out_path, "PNG", optimize=True)


# ── Main ─────────────────────────────────────────────────────────────────
def main() -> int:
    with open(DATA_FILE) as f:
        data = json.load(f)
    date_iso = data.get("updated") or datetime.utcnow().date().isoformat()

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    written = 0
    for city in data["cities"]:
        slug = slugify(city["city"])
        out = OUT_DIR / f"petrol-price-{slug}.png"
        try:
            render_card(
                city=city["city"],
                state=city["state"],
                petrol=float(city["petrol"]),
                diesel=float(city["diesel"]),
                date_iso=date_iso,
                out_path=out,
            )
            print(f"  ✓ {out.relative_to(REPO_DIR)}")
            written += 1
        except Exception as e:
            print(f"  ✗ {city['city']}: {e}", file=sys.stderr)

    # National roll-up card for /conversion/petrol-price-today/. Uses Delhi as
    # the reference (lowest VAT among the metros, most cited figure) plus a
    # cross-city min/max range so the og:image conveys the spread.
    try:
        delhi = next(c for c in data["cities"] if c["city"] == "Delhi")
        petrols = [float(c["petrol"]) for c in data["cities"]]
        diesels = [float(c["diesel"]) for c in data["cities"]]
        # Cheapest/most expensive city by petrol
        cheap = min(data["cities"], key=lambda c: float(c["petrol"]))
        dear  = max(data["cities"], key=lambda c: float(c["petrol"]))
        out = OUT_DIR / "petrol-price-today.png"
        render_card(
            city="India",
            state=f"₹{cheap['petrol']:.2f} {cheap['city']} – ₹{dear['petrol']:.2f} {dear['city']}",
            petrol=float(delhi["petrol"]),
            diesel=float(delhi["diesel"]),
            date_iso=date_iso,
            out_path=out,
            footer_url="calxo.in/conversion/petrol-price-today/",
        )
        print(f"  ✓ {out.relative_to(REPO_DIR)} (national roll-up)")
        written += 1
    except Exception as e:
        print(f"  ✗ national roll-up: {e}", file=sys.stderr)

    print(f"\n  Generated {written} card images "
          f"({W}×{H}) for {date_iso} → {OUT_DIR.relative_to(REPO_DIR)}/")
    return 0 if written else 1


if __name__ == "__main__":
    sys.exit(main())
