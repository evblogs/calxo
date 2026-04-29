"""
Calxo.in — Daily Petrol & Diesel Price Updater
Scrapes city-wise fuel prices from goodreturns.in and updates data/petrol-prices.json.
Run nightly via launchd. Commits + pushes → triggers Netlify rebuild.

Cron: run at 6:30 AM IST (after OMC revision at 6 AM)
"""

import json, re, time, subprocess
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

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "en-IN,en;q=0.9",
}

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


def fetch_price(city_slug):
    """Return (petrol, diesel) float prices for a city slug, or None on failure."""
    url = f"https://www.goodreturns.in/petrol-price/{city_slug}.html"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=12)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        prices = {}
        for fuel in ("petrol", "diesel"):
            # goodreturns uses a table with class 'fuel-price-table' or similar
            # Look for the current price in span/td containing the ₹ amount
            pattern = re.compile(r'[\d]+\.[\d]+')
            # Try multiple selectors for resilience
            for sel in [
                f'[data-fuel="{fuel}"] .current-price',
                f'.{fuel}-price .price',
                f'#{fuel}-price',
            ]:
                tag = soup.select_one(sel)
                if tag:
                    m = pattern.search(tag.get_text())
                    if m:
                        prices[fuel] = float(m.group())
                        break

            # Fallback: scan all text nodes for price near fuel keyword
            if fuel not in prices:
                text = soup.get_text()
                idx = text.lower().find(fuel + " price")
                if idx != -1:
                    snippet = text[idx:idx+100]
                    m = re.search(r'₹?\s*([\d]{2,3}\.[\d]{1,2})', snippet)
                    if m:
                        val = float(m.group(1))
                        if 70 < val < 130:  # sanity check
                            prices[fuel] = val

        if "petrol" in prices and "diesel" in prices:
            return prices["petrol"], prices["diesel"]
    except Exception as e:
        print(f"  ERROR {city_slug}: {e}")
    return None, None


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

    for slug, city_name, state in CITY_MAP:
        petrol, diesel = fetch_price(slug)
        if petrol and diesel:
            city_lookup[city_name] = {
                "city": city_name,
                "state": state,
                "petrol": petrol,
                "diesel": diesel,
            }
            print(f"  ✓ {city_name}: petrol ₹{petrol} | diesel ₹{diesel}")
            updated_count += 1
        else:
            print(f"  ✗ {city_name}: scrape failed — keeping previous price")
            failed.append(city_name)
        time.sleep(1.2)  # polite crawl rate

    # Rebuild ordered city list
    existing["cities"] = [city_lookup[name] for _, name, _ in CITY_MAP if name in city_lookup]
    existing["updated"] = today
    save(existing)

    print(f"\n  Updated: {updated_count}/{len(CITY_MAP)} cities | Failed: {len(failed)}")
    if failed:
        print(f"  Failed cities: {', '.join(failed)}")

    # Update lastmod + prices in all petrol content pages
    print("\n  Updating page front matter...")
    city_lookup_final = {c["city"]: c for c in existing["cities"]}
    for page in PETROL_PAGES:
        city_name = CITY_PAGE_MAP.get(page.name)
        city_prices = city_lookup_final.get(city_name) if city_name else None
        update_page_lastmod(page, today, city_prices)

    print("\n  Pushing to git...")
    git_commit_push(today)
    print("\n  Done. Netlify will rebuild in ~1 minute.")


if __name__ == "__main__":
    main()
