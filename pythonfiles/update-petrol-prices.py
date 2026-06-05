"""
Calxo.in — Daily Petrol & Diesel Price Updater
Scrapes city-wise fuel prices from goodreturns.in and updates data/petrol-prices.json.
Run nightly via launchd. Commits + pushes → triggers Netlify rebuild.

Cron: run at 6:30 AM IST (after OMC revision at 6 AM)
"""

import json, re, time, subprocess, random, os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path

import requests
from bs4 import BeautifulSoup

DATA_FILE   = Path(__file__).parent.parent / "data" / "petrol-prices.json"
REPO_DIR    = Path(__file__).parent.parent
CONTENT_DIR = REPO_DIR / "content" / "english" / "conversion"

# All petrol-related content pages whose lastmod should stay current
PETROL_PAGES = [
    CONTENT_DIR / "petrol-price-today.md",
    CONTENT_DIR / "petrol-price-delhi.md",
    CONTENT_DIR / "petrol-price-bangalore.md",
    CONTENT_DIR / "petrol-price-chennai.md",
]

# City-specific price patterns for updating page titles and descriptions
CITY_PAGE_MAP = {
    "petrol-price-delhi.md":     "Delhi",
    "petrol-price-bangalore.md": "Bengaluru",
    "petrol-price-chennai.md":   "Chennai",
}

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0",
]

def _headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-IN,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

# Tuning: short per-request timeout, a couple of retries, bounded concurrency.
REQUEST_TIMEOUT = 6      # seconds per attempt (was 12, sequential)
MAX_RETRIES     = 2      # attempts per city
MAX_WORKERS     = 8      # concurrent city fetches
PRICE_MIN, PRICE_MAX = 55.0, 160.0   # sanity range for ₹/litre

# Map of city slug (goodreturns URL) → our city name + state
CITY_MAP = [
    ("delhi",              "Delhi",             "Delhi"),
    ("mumbai",             "Mumbai",            "Maharashtra"),
    ("chennai",            "Chennai",           "Tamil Nadu"),
    ("kolkata",            "Kolkata",           "West Bengal"),
    ("bangalore",          "Bengaluru",         "Karnataka"),
    ("hyderabad",          "Hyderabad",         "Telangana"),
    ("pune",               "Pune",              "Maharashtra"),
    ("ahmedabad",          "Ahmedabad",         "Gujarat"),
    ("jaipur",             "Jaipur",            "Rajasthan"),
    ("lucknow",            "Lucknow",           "Uttar Pradesh"),
    ("noida",              "Noida",             "Uttar Pradesh"),
    ("chandigarh",         "Chandigarh",        "Chandigarh"),
    ("bhopal",             "Bhopal",            "Madhya Pradesh"),
    ("indore",             "Indore",            "Madhya Pradesh"),
    ("patna",              "Patna",             "Bihar"),
    ("ranchi",             "Ranchi",            "Jharkhand"),
    ("raipur",             "Raipur",            "Chhattisgarh"),
    ("bhubaneswar",        "Bhubaneswar",       "Odisha"),
    ("guwahati",           "Guwahati",          "Assam"),
    ("thiruvananthapuram", "Thiruvananthapuram","Kerala"),
    ("kochi",              "Kochi",             "Kerala"),
    ("coimbatore",         "Coimbatore",        "Tamil Nadu"),
    ("visakhapatnam",      "Visakhapatnam",     "Andhra Pradesh"),
    ("nagpur",             "Nagpur",            "Maharashtra"),
    ("surat",              "Surat",             "Gujarat"),
    ("vadodara",           "Vadodara",          "Gujarat"),
    ("ludhiana",           "Ludhiana",          "Punjab"),
    ("agra",               "Agra",              "Uttar Pradesh"),
    ("varanasi",           "Varanasi",          "Uttar Pradesh"),
    ("dehradun",           "Dehradun",          "Uttarakhand"),
]


def _sane(val):
    return val is not None and PRICE_MIN <= val <= PRICE_MAX


def _extract_fuel_price(soup, text, fuel):
    """Pull a single fuel price from the page using layered strategies."""
    # 1) Structured selectors (cheap, precise when present).
    dec = re.compile(r'[\d]{2,3}\.[\d]{1,2}')
    for sel in (f'[data-fuel="{fuel}"] .current-price',
                f'.{fuel}-price .price', f'#{fuel}-price'):
        tag = soup.select_one(sel)
        if tag:
            m = dec.search(tag.get_text())
            if m and _sane(float(m.group())):
                return float(m.group())

    # 2) Prose near the "<fuel> price" phrase (handles "Rs." or "₹").
    idx = text.lower().find(fuel + " price")
    if idx != -1:
        m = re.search(r'(?:₹|Rs\.?)?\s*([\d]{2,3}\.[\d]{1,2})', text[idx:idx + 120])
        if m and _sane(float(m.group(1))):
            return float(m.group(1))

    # 3) Any sane decimal within a wider window after the first fuel mention.
    idx = text.lower().find(fuel)
    if idx != -1:
        for m in re.finditer(r'([\d]{2,3}\.[\d]{1,2})', text[idx:idx + 200]):
            if _sane(float(m.group(1))):
                return float(m.group(1))
    return None


_MONTHS = ("january february march april may june july august september "
           "october november december").split()


def _extract_date(text):
    """Best-effort 'as on' date from page text. Returns a date or None."""
    low = text.lower()
    # "13 May 2026" / "13 May, 2026"
    m = re.search(r'(\d{1,2})\s+(' + "|".join(_MONTHS) + r')[a-z]*,?\s+(20\d\d)', low)
    if m:
        try:
            return date(int(m.group(3)), _MONTHS.index(m.group(2)) + 1, int(m.group(1)))
        except ValueError:
            pass
    # "May 13, 2026"
    m = re.search(r'(' + "|".join(_MONTHS) + r')[a-z]*\s+(\d{1,2}),?\s+(20\d\d)', low)
    if m:
        try:
            return date(int(m.group(3)), _MONTHS.index(m.group(1)) + 1, int(m.group(2)))
        except ValueError:
            pass
    # ISO or dd-mm-yyyy
    m = re.search(r'(20\d\d)-(\d{2})-(\d{2})', low)
    if m:
        try:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            pass
    m = re.search(r'(\d{2})[-/](\d{2})[-/](20\d\d)', low)
    if m:
        try:
            return date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        except ValueError:
            pass
    return None


def fetch_from_url(url):
    """Fetch one source URL. Returns (petrol, diesel, as_on_date|None) or None."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(url, headers=_headers(), timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            text = soup.get_text(" ", strip=True)
            petrol = _extract_fuel_price(soup, text, "petrol")
            diesel = _extract_fuel_price(soup, text, "diesel")
            if _sane(petrol) and _sane(diesel):
                return petrol, diesel, _extract_date(text)
        except Exception:
            pass
        time.sleep(0.4 * attempt)
    return None


# Per-source slug aliases (sites name a few cities differently).
SLUG_ALIASES = {
    "ndtv":       {"Bengaluru": "bangalore", "Thiruvananthapuram": "trivandrum"},
    "bankbazaar": {"Bengaluru": "bangalore", "Thiruvananthapuram": "thiruvananthapuram"},
    "cardekho":   {"Bengaluru": "bangalore", "Thiruvananthapuram": "thiruvananthapuram"},
}


def _slug_for(source, city_name, gr_slug):
    if source == "goodreturns":
        return gr_slug
    alias = SLUG_ALIASES.get(source, {}).get(city_name)
    return alias or city_name.lower().replace(" ", "-")


# Source URL builders. Add/remove freely — failures are tolerated.
SOURCES = [
    ("goodreturns", lambda s: f"https://www.goodreturns.in/petrol-price/{s}.html"),
    ("ndtv",        lambda s: f"https://www.ndtv.com/fuel-prices/petrol-price-in-{s}-city"),
    ("bankbazaar",  lambda s: f"https://www.bankbazaar.com/fuel/petrol-price-in-{s}.html"),
    ("cardekho",    lambda s: f"https://www.cardekho.com/petrol-price-in-{s}-city"),
]


def _median(values):
    vals = sorted(values)
    n = len(vals)
    if n == 0:
        return None
    mid = n // 2
    return vals[mid] if n % 2 else round((vals[mid - 1] + vals[mid]) / 2, 2)


def fetch_price(city_name, gr_slug):
    """Multi-source fetch. Query every source, then pick the one with the
    freshest 'as on' date. If no source exposes a date, fall back to the
    median of all sane readings (robust to a single bad source).

    Returns (petrol, diesel, provenance_str) or (None, None, None).
    """
    results = []  # list of (source, petrol, diesel, date|None)
    for source, build in SOURCES:
        slug = _slug_for(source, city_name, gr_slug)
        got = fetch_from_url(build(slug))
        if got:
            p, d, dt = got
            results.append((source, p, d, dt))

    if not results:
        return None, None, None

    dated = [r for r in results if r[3] is not None]
    if dated:
        # Whoever has the most recently updated data wins.
        source, p, d, dt = max(dated, key=lambda r: r[3])
        return p, d, f"{source} (as on {dt.isoformat()})"

    # No dates anywhere: consensus median across sources.
    p = _median([r[1] for r in results])
    d = _median([r[2] for r in results])
    names = "+".join(sorted({r[0] for r in results}))
    return p, d, f"{names} (median of {len(results)})"


# ── Official source: data.gov.in OGD daily fuel-price API ──────────────────
# This is the only source that reliably works from a datacenter/CI IP. It
# needs a free API key (register at https://data.gov.in -> My Account -> API
# key) supplied via the DATA_GOV_API_KEY secret, and a resource id pointing at
# the current daily fuel-price dataset via DATAGOV_RESOURCE_ID. Both are read
# from the environment so nothing is hardcoded; absent either, this is inert.
DATAGOV_RESOURCE_ID = os.environ.get("DATAGOV_RESOURCE_ID", "")

_CITY_NORMALISE = {
    "bangalore": "Bengaluru", "bengaluru": "Bengaluru",
    "trivandrum": "Thiruvananthapuram", "vizag": "Visakhapatnam",
}


def _norm_city(name):
    return _CITY_NORMALISE.get(name.strip().lower(), name.strip().title())


def _num(v):
    try:
        f = float(str(v).replace(",", "").strip())
        return f if PRICE_MIN <= f <= PRICE_MAX else None
    except (TypeError, ValueError):
        return None


def fetch_datagov(api_key, want_cities):
    """Return {our_city_name: (petrol, diesel, date|None)} from data.gov.in.

    Records are parsed by fuzzy key match so the loader survives minor schema
    changes. Only cities we track, with both fuels in a sane range, are kept.
    """
    if not api_key or not DATAGOV_RESOURCE_ID:
        return {}
    url = f"https://api.data.gov.in/resource/{DATAGOV_RESOURCE_ID}"
    params = {"api-key": api_key, "format": "json", "limit": 2000}
    try:
        resp = requests.get(url, params=params, headers=_headers(), timeout=15)
        resp.raise_for_status()
        records = resp.json().get("records", [])
    except Exception as e:
        print(f"  data.gov.in fetch failed: {e}")
        return {}

    wanted = {c.lower(): c for c in want_cities}
    out = {}
    for rec in records:
        low = {(k or "").lower(): v for k, v in rec.items()}
        city_v = next((low[k] for k in low if k in
                       ("city", "centre", "center", "location",
                        "metrocity", "metro_cities")), None)
        if city_v is None:
            continue
        target = wanted.get(_norm_city(str(city_v)).lower())
        if not target:
            continue
        petrol = next((_num(low[k]) for k in low
                       if "petrol" in k and _num(low[k]) is not None), None)
        diesel = next((_num(low[k]) for k in low
                       if "diesel" in k and _num(low[k]) is not None), None)
        if petrol is None or diesel is None:
            continue
        dval = next((low[k] for k in low if "date" in k), None)
        dt = _extract_date(str(dval)) if dval else None
        prev = out.get(target)
        if not prev or (dt and (prev[2] is None or dt > prev[2])):
            out[target] = (petrol, diesel, dt)
    return out


def load_existing():
    with open(DATA_FILE) as f:
        return json.load(f)


def save(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"  Saved {DATA_FILE}")


def update_page_lastmod(page_path, today, city_prices=None):
    """Update lastmod in a petrol page's front matter. Optionally update title/description price."""
    if not page_path.exists():
        print(f"  SKIP {page_path.name} — file not found")
        return False
    text = page_path.read_text()

    # Update lastmod
    text = re.sub(r'lastmod:\s*\S+', f'lastmod: {today}', text)

    # For city pages, update the price in title and description if prices changed
    if city_prices:
        city = city_prices["city"]
        petrol = city_prices["petrol"]
        diesel = city_prices["diesel"]
        # Update title price (e.g. "₹94.77/Litre")
        text = re.sub(
            r'(title:.*?₹)[\d.]+(/Litre)',
            lambda m: f'{m.group(1)}{petrol:.2f}{m.group(2)}',
            text
        )
        # Update description petrol price
        text = re.sub(
            r'(petrol price in .+? is \*\*₹)[\d.]+( per litre)',
            lambda m: f'{m.group(1)}{petrol:.2f}{m.group(2)}',
            text, flags=re.IGNORECASE
        )
        # Update description diesel price
        text = re.sub(
            r'(diesel is \*\*₹)[\d.]+( per litre)',
            lambda m: f'{m.group(1)}{diesel:.2f}{m.group(2)}',
            text, flags=re.IGNORECASE
        )
        # Update the date in title parenthesis e.g. "(29 April 2026)"
        from datetime import datetime
        date_str = datetime.strptime(today, "%Y-%m-%d").strftime("%-d %B %Y")
        text = re.sub(r'\(\d+ \w+ 20\d\d\)', f'({date_str})', text)

    page_path.write_text(text)
    print(f"  ✓ Updated lastmod in {page_path.name}")
    return True


def git_commit_push(today):
    add_paths = ["data/petrol-prices.json"] + [
        str(p.relative_to(REPO_DIR)) for p in PETROL_PAGES if p.exists()
    ]
    cmds = [
        ["git", "-C", str(REPO_DIR), "add"] + add_paths,
        ["git", "-C", str(REPO_DIR), "commit", "-m", f"[auto] Update petrol prices — {today}"],
        ["git", "-C", str(REPO_DIR), "push", "origin", "master"],
    ]
    for cmd in cmds:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  Git warning: {result.stderr.strip()}")
        else:
            print(f"  {' '.join(cmd[2:])}: OK")


def main():
    today = date.today().isoformat()
    print("=" * 60)
    print(f"  Calxo — Petrol Price Updater ({today})")
    print("=" * 60)

    existing = load_existing()
    city_lookup = {c["city"]: c for c in existing["cities"]}

    updated_count = 0
    failed = []
    used_datagov = False

    # Primary, CI-reliable source: official data.gov.in API (if configured).
    want = [name for _, name, _ in CITY_MAP]
    datagov = fetch_datagov(os.environ.get("DATA_GOV_API_KEY"), want)
    if datagov:
        used_datagov = True
        print(f"  data.gov.in returned {len(datagov)} cities")

    # Per city: prefer the official API, else best-effort multi-site scrape
    # (the scrape generally only succeeds from a residential IP, not CI).
    def work(entry):
        slug, city_name, state = entry
        dg = datagov.get(city_name)
        if dg and dg[0] and dg[1]:
            dt = dg[2]
            prov = f"data.gov.in (as on {dt.isoformat()})" if dt else "data.gov.in"
            return city_name, state, dg[0], dg[1], prov
        petrol, diesel, prov = fetch_price(city_name, slug)
        return city_name, state, petrol, diesel, prov

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = [pool.submit(work, e) for e in CITY_MAP]
        for fut in as_completed(futures):
            city_name, state, petrol, diesel, prov = fut.result()
            if petrol and diesel:
                city_lookup[city_name] = {
                    "city": city_name, "state": state,
                    "petrol": petrol, "diesel": diesel,
                }
                print(f"  ✓ {city_name}: petrol ₹{petrol} | diesel ₹{diesel}  [{prov}]")
                updated_count += 1
            else:
                print(f"  ✗ {city_name}: no live source returned data — keeping previous price")
                failed.append(city_name)

    # Rebuild ordered city list. 'updated' is the display date (advances daily,
    # matching the OMC daily-revision cycle). 'prices_verified' is honest: it
    # only moves to today when a real source actually returned prices.
    prev_verified = existing.get("prices_verified") or existing.get("updated")
    existing["cities"] = [city_lookup[name] for _, name, _ in CITY_MAP if name in city_lookup]
    existing["updated"] = today
    if updated_count > 0:
        existing["prices_verified"] = today
        src = ("data.gov.in API + best-effort scrape" if used_datagov
               else "best-effort multi-site scrape")
        existing["source"] = f"{src} — {updated_count}/{len(CITY_MAP)} cities refreshed {today}"
    else:
        existing["prices_verified"] = prev_verified
        existing["source"] = (
            f"Prices held since {prev_verified} (no live source returned data "
            f"this run); displayed date reflects the daily revision cycle")
    save(existing)

    print(f"\n  Refreshed with live data: {updated_count}/{len(CITY_MAP)} | "
          f"held from previous: {len(failed)}")
    if updated_count == 0:
        print("  NOTE: no live prices fetched. Set DATA_GOV_API_KEY + "
              "DATAGOV_RESOURCE_ID, or run from a residential IP, for real updates.")

    # Update lastmod + prices in all petrol content pages
    print("\n  Updating page front matter...")
    city_lookup_final = {c["city"]: c for c in existing["cities"]}
    for page in PETROL_PAGES:
        city_name = CITY_PAGE_MAP.get(page.name)
        city_prices = city_lookup_final.get(city_name) if city_name else None
        update_page_lastmod(page, today, city_prices)

    # In CI the workflow regenerates the city pages and commits everything in
    # one shot, so skip the script's own git push when CALXO_SKIP_GIT is set
    # (or --no-git is passed).
    import sys
    skip_git = os.environ.get("CALXO_SKIP_GIT") or "--no-git" in sys.argv
    if skip_git:
        print("\n  CALXO_SKIP_GIT set — skipping git (workflow will commit).")
    else:
        print("\n  Pushing to git...")
        git_commit_push(today)
    print("\n  Done. Netlify will rebuild in ~1 minute.")


if __name__ == "__main__":
    main()
