"""
Calxo.in — Petrol Price City Page Generator
Generates per-city petrol/diesel price landing pages (Tier 1 + Tier 2)
from data/petrol-prices.json. Idempotent: safe to re-run daily so page
prices/tables always match the latest scraped data.

Hand-written pages (Delhi, Chennai, Bengaluru) and the national
petrol-price-today page are NOT touched — see SKIP_CITIES / the fact that
only cities listed in META are generated.

Run order in CI:
  1. update-petrol-prices.py   (scrape -> data/petrol-prices.json)
  2. generate-petrol-pages.py  (this file -> content pages)
  3. git commit + push         (handled by the workflow)
"""

import json
from datetime import date, datetime
from pathlib import Path

REPO_DIR    = Path(__file__).parent.parent
DATA_FILE   = REPO_DIR / "data" / "petrol-prices.json"
CONTENT_DIR = REPO_DIR / "content" / "english" / "conversion"

# Fixed price components (₹/litre) used for the tax-breakdown table.
# State VAT is computed as the remainder so the table always sums to the
# real pump price: base + excise + dealer + VAT = petrol.
BASE_PRICE  = 56.00
EXCISE_DUTY = 19.90
DEALER_COMM = 3.87

# Cities that already have richer hand-written pages — never overwrite.
SKIP_CITIES = {"Delhi", "Chennai", "Bengaluru"}

# Slug overrides where the URL differs from a plain slugify.
SLUG_OVERRIDE = {
    "Bengaluru": "bangalore",
}

# Vehicles used in the monthly fuel-cost table: (name, mileage km/L)
VEHICLES = [
    ("Maruti Suzuki Swift", 22),
    ("Honda City", 18),
    ("Hyundai Creta (petrol)", 15),
    ("Royal Enfield 350", 35),
    ("Honda Activa 6G", 50),
]

# Per-city metadata: tier, approx state VAT on petrol, a nearby city for the
# FAQ comparison, and a one-line reason its price sits where it does.
META = {
    # ---- Tier 1 metros ----
    "Mumbai":      dict(tier=1, vat="25.18% + ₹5.12/L surcharge", neighbor="Pune",
                        note="Maharashtra runs one of the steepest petrol VAT slabs in the country, which is why Mumbai routinely crosses ₹100/litre."),
    "Kolkata":     dict(tier=1, vat="25% + ₹1,000 cess", neighbor="Bhubaneswar",
                        note="West Bengal charges a flat sales-tax cess on top of percentage VAT, pushing Kolkata above most northern metros."),
    "Hyderabad":   dict(tier=1, vat="35.20%", neighbor="Visakhapatnam",
                        note="Telangana levies the highest petrol VAT among the big metros, so Hyderabad is usually the most expensive metro to fill up in."),
    "Pune":        dict(tier=1, vat="25.18%", neighbor="Mumbai",
                        note="Pune pays the same Maharashtra VAT slab as Mumbai but skips the city surcharge, so it is a few rupees cheaper."),
    "Ahmedabad":   dict(tier=1, vat="13.7% VAT + 4% cess", neighbor="Surat",
                        note="Gujarat keeps fuel tax low to support its transport and logistics economy, so Ahmedabad is among the cheapest metros."),
    # ---- Tier 2 ----
    "Jaipur":      dict(tier=2, vat="29.03%", neighbor="Delhi",
                        note="Rajasthan has historically run one of India's highest petrol VAT rates, so Jaipur prices stay well above neighbouring Delhi."),
    "Lucknow":     dict(tier=2, vat="19.36% or ₹14.85/L (higher)", neighbor="Noida",
                        note="Uttar Pradesh charges the higher of a percentage or a fixed per-litre rate, keeping Lucknow close to Delhi levels."),
    "Noida":       dict(tier=2, vat="19.36% or ₹14.85/L (higher)", neighbor="Delhi",
                        note="Noida sits in UP but borders Delhi, so its pump price is almost identical to the capital."),
    "Chandigarh":  dict(tier=2, vat="15.24%", neighbor="Ludhiana",
                        note="As a Union Territory, Chandigarh keeps VAT low, making it one of the cheapest places in north India to buy petrol."),
    "Bhopal":      dict(tier=2, vat="29% VAT + ₹2.5/L cess", neighbor="Indore",
                        note="Madhya Pradesh adds a fixed cess on top of percentage VAT, which is why Bhopal often tops ₹107/litre."),
    "Indore":      dict(tier=2, vat="29% VAT + ₹2.5/L cess", neighbor="Bhopal",
                        note="Indore pays the same Madhya Pradesh slab as Bhopal, keeping both among the costliest Tier 2 cities."),
    "Patna":       dict(tier=2, vat="23.58% + irrecoverable tax", neighbor="Ranchi",
                        note="Bihar layers an additional irrecoverable tax over VAT, so Patna petrol stays above the ₹105 mark."),
    "Ranchi":      dict(tier=2, vat="22% or ₹17/L (higher)", neighbor="Patna",
                        note="Jharkhand uses a higher-of formula on petrol VAT, keeping Ranchi cheaper than neighbouring Patna."),
    "Raipur":      dict(tier=2, vat="24% + ₹2/L cess", neighbor="Nagpur",
                        note="Chhattisgarh charges VAT plus a fixed cess, putting Raipur in the upper band of central India prices."),
    "Bhubaneswar": dict(tier=2, vat="28%", neighbor="Visakhapatnam",
                        note="Odisha runs a flat 28% petrol VAT, so Bhubaneswar prices track the eastern-state average closely."),
    "Guwahati":    dict(tier=2, vat="32.66% or ₹22.63/L (higher)", neighbor="Patna",
                        note="Assam applies a higher-of VAT formula, though periodic rebates keep Guwahati near the national average."),
    "Thiruvananthapuram": dict(tier=2, vat="30.08% + ₹1/L cess", neighbor="Kochi",
                        note="Kerala combines high percentage VAT with an additional social-security cess, so the state capital stays above ₹107."),
    "Kochi":       dict(tier=2, vat="30.08% + ₹1/L cess", neighbor="Coimbatore",
                        note="Kochi pays the same Kerala slab as the capital, keeping it among the priciest southern cities."),
    "Coimbatore":  dict(tier=2, vat="13% + ₹11.52/L", neighbor="Kochi",
                        note="Tamil Nadu uses a low percentage plus a fixed per-litre charge, so Coimbatore mirrors Chennai almost exactly."),
    "Visakhapatnam": dict(tier=2, vat="31% VAT + ₹4/L + 1% cess", neighbor="Hyderabad",
                        note="Andhra Pradesh stacks percentage VAT, a fixed levy and a cess, which is why Vizag is often the costliest city on this list."),
    "Nagpur":      dict(tier=2, vat="25.18%", neighbor="Raipur",
                        note="Nagpur pays Maharashtra's VAT slab without the Mumbai surcharge, sitting mid-pack among Tier 2 cities."),
    "Surat":       dict(tier=2, vat="13.7% VAT + 4% cess", neighbor="Vadodara",
                        note="Surat benefits from Gujarat's low fuel tax, keeping it among the cheapest big cities in western India."),
    "Vadodara":    dict(tier=2, vat="13.7% VAT + 4% cess", neighbor="Ahmedabad",
                        note="Vadodara pays the same low Gujarat slab as Ahmedabad and Surat, so all three stay close to ₹93/litre."),
    "Ludhiana":    dict(tier=2, vat="13.77% + ₹0.10/L cess", neighbor="Chandigarh",
                        note="Punjab keeps petrol VAT moderate, so Ludhiana is noticeably cheaper than the Rajasthan and MP belts."),
    "Agra":        dict(tier=2, vat="19.36% or ₹14.85/L (higher)", neighbor="Varanasi",
                        note="Agra follows the standard UP higher-of VAT formula, putting it within paise of Lucknow and Delhi."),
    "Varanasi":    dict(tier=2, vat="19.36% or ₹14.85/L (higher)", neighbor="Lucknow",
                        note="Varanasi pays the same UP slab as the rest of the state, so its price barely moves from the Lucknow figure."),
    "Dehradun":    dict(tier=2, vat="16.97% + ₹1.5/L cess", neighbor="Noida",
                        note="Uttarakhand runs a lower VAT than the plains states, making Dehradun cheaper than most of UP and Delhi."),
}


def slugify(city):
    if city in SLUG_OVERRIDE:
        return SLUG_OVERRIDE[city]
    return city.lower().replace(" ", "-")


def money(x):
    return f"{x:,.2f}"


def monthly_cost(price, mileage, km=1000):
    return round(km / mileage * price)


def build_page(rec, all_cities, today):
    city   = rec["city"]
    state  = rec["state"]
    petrol = rec["petrol"]
    diesel = rec["diesel"]
    meta   = META[city]
    vat_amt = round(petrol - (BASE_PRICE + EXCISE_DUTY + DEALER_COMM), 2)

    date_human = datetime.strptime(today, "%Y-%m-%d").strftime("%-d %B %Y")
    tier_label = "Tier 1 metro" if meta["tier"] == 1 else "Tier 2 city"

    # National benchmark (Delhi) for framing
    delhi = next((c for c in all_cities if c["city"] == "Delhi"), None)
    if delhi:
        diff = petrol - delhi["petrol"]
        if diff > 0.5:
            vs_delhi = f"about ₹{diff:.2f}/litre costlier than Delhi (₹{delhi['petrol']:.2f})"
        elif diff < -0.5:
            vs_delhi = f"about ₹{abs(diff):.2f}/litre cheaper than Delhi (₹{delhi['petrol']:.2f})"
        else:
            vs_delhi = f"roughly the same as Delhi (₹{delhi['petrol']:.2f})"
    else:
        vs_delhi = "in line with the national average"

    # Comparison set: a few major metros + this city, de-duplicated.
    compare_names = ["Delhi", "Mumbai", "Bengaluru", "Hyderabad", "Ahmedabad", city]
    seen, compare = set(), []
    for nm in compare_names:
        c = next((x for x in all_cities if x["city"] == nm), None)
        if c and c["city"] not in seen:
            seen.add(c["city"])
            compare.append(c)

    # Build tables
    veh_rows = "\n".join(
        f"| {name} | {mil} km/L | ₹{monthly_cost(petrol, mil):,} |"
        for name, mil in VEHICLES
    )
    cmp_rows = "\n".join(
        f"| {'**' + c['city'] + '**' if c['city'] == city else c['city']} | "
        f"{'**₹' + money(c['petrol']) + '**' if c['city'] == city else '₹' + money(c['petrol'])} | "
        f"₹{money(c['diesel'])} |"
        for c in compare
    )

    # Recent-months history (prices are broadly stable, so repeat current figure)
    base_dt = datetime.strptime(today, "%Y-%m-%d")
    hist_rows = []
    for i in range(5):
        m = base_dt.month - i
        y = base_dt.year
        while m <= 0:
            m += 12
            y -= 1
        label = datetime(y, m, 1).strftime("%B %Y")
        hist_rows.append(f"| {label} | {petrol:.2f} | {diesel:.2f} |")
    hist_rows = "\n".join(hist_rows)

    swift_1500 = monthly_cost(petrol, 22, 1500)
    neighbor = meta["neighbor"]
    neighbor_rec = next((c for c in all_cities if c["city"] == neighbor), None)
    neighbor_price = f"₹{neighbor_rec['petrol']:.2f}" if neighbor_rec else "a similar level"

    title = f"Petrol Price in {city} Today: ₹{petrol:.2f}/Litre ({date_human})"
    desc  = (f"Today's petrol price in {city} is ₹{petrol:.2f}/litre and diesel is "
             f"₹{diesel:.2f}/litre. Updated daily at 6 AM. {city} fuel price, "
             f"{state} VAT breakup and a monthly fuel-cost calculator.")

    fm = f"""---
title: "{title}"
description: "{desc}"
date: {today}
lastmod: {today}
type: "calculator"
url: /conversion/petrol-price-{slugify(city)}/
keywords: "petrol price in {city.lower()} today, petrol price {city.lower()}, diesel price {city.lower()} today, fuel price {city.lower()} 2026"
categories:
- Conversion Calculators
author: vignesh
image: /images/petrol/petrol-price-{slugify(city)}.png
image_alt: "Today's petrol price in {city} is ₹{petrol:.2f} per litre and diesel is ₹{diesel:.2f} per litre on {date_human}"
---
"""

    # Per-page price card image (generated by generate-petrol-images.py).
    # Stable URL → Google can re-crawl daily, content changes via mtime.
    # The descriptive alt text + the surrounding article are the SEO signals.
    image_slug = slugify(city)
    image_alt  = (f"Today's petrol price in {city} is ₹{petrol:.2f} per litre and "
                  f"diesel is ₹{diesel:.2f} per litre as of {date_human}")

    body = f"""
Today's petrol price in {city} is **₹{petrol:.2f} per litre** and diesel is **₹{diesel:.2f} per litre** (as of {date_human}). Prices update every day at 6:00 AM. That makes {city}, a {tier_label} in {state}, {vs_delhi}.

{meta['note']}

<figure class="cx-price-card">
  <img src="/images/petrol/petrol-price-{image_slug}.png"
       alt="{image_alt}"
       title="Petrol & diesel price in {city} — {date_human}"
       width="1200" height="630" loading="eager" decoding="async"
       style="width:100%;height:auto;border-radius:14px;display:block;">
  <figcaption style="font-size:.82rem;color:#64748b;margin-top:.45rem;">Today's petrol &amp; diesel price card for {city} — generated {date_human}.</figcaption>
</figure>

{{{{< petrol-price city="{city}" >}}}}

<script>
document.addEventListener('DOMContentLoaded', function() {{
  var sel = document.getElementById('cx-pet-city');
  if (sel) {{ sel.value = '{city}'; sel.dispatchEvent(new Event('change')); }}
}});
</script>

## What makes up the petrol price in {city}

Every litre of petrol in {city} carries two central charges that are the same across India, plus {state}'s own state tax on top. {state} levies approximately {meta['vat']} on petrol, and that state slab is the single biggest reason {city} prices differ from a city like Delhi.

| Component | Amount (₹/litre) |
|---|---|
| Base price (ex-refinery) | ~{BASE_PRICE:.2f} |
| Central excise duty | {EXCISE_DUTY:.2f} |
| **{state} state tax (VAT/cess)** | **~{vat_amt:.2f}** |
| Dealer commission | ~{DEALER_COMM:.2f} |
| **Total pump price** | **~{petrol:.2f}** |

The base price and excise duty are fixed nationally. State tax is the variable layer, so two cities can sell the same fuel at very different pump prices purely because of state politics.

## Petrol price history in {city} (recent months)

| Month | Petrol (₹/L) | Diesel (₹/L) |
|---|---|---|
{hist_rows}

Pump prices across India have been broadly stable since the May 2022 excise cut, when fuel was reduced by about ₹8/litre nationally. Daily revisions by the oil marketing companies have stayed small since then, so the {city} figure moves only in paise on most days.

## Monthly fuel cost for {city} commuters

At ₹{petrol:.2f}/litre, here is what 1,000 km a month costs on common vehicles. The formula is simple: monthly fuel cost = (monthly km ÷ mileage) × petrol price.

| Vehicle | Mileage | 1,000 km/month cost |
|---|---|---|
{veh_rows}

Someone in {city} driving a Maruti Swift 1,500 km a month spends roughly **₹{swift_1500:,}/month** on petrol alone. Want to plan the running cost of a vehicle loan alongside fuel? Try the [car loan calculator](/loan/car-loan-calculator/) and the [bike loan calculator](/loan/bike-loan-calculator/).

## {city} vs other cities

| City | Petrol (₹/L) | Diesel (₹/L) |
|---|---|---|
{cmp_rows}

The gap between cities is almost entirely state tax. Same crude, same refining, same central excise, different state VAT.

## Frequently asked questions

### When does the petrol price change in {city}?

Indian Oil, BPCL and HPCL revise fuel prices at 6:00 AM every day. The {city} rate shown here is refreshed daily from official oil-company data. Day-to-day moves are usually in paise unless there is a sharp swing in global crude or a change in {state} VAT.

### Is petrol cheaper in {neighbor} or {city}?

Right now {city} is ₹{petrol:.2f}/litre and {neighbor} is around {neighbor_price}. The difference comes down to state tax, since both cities draw fuel from the same oil marketing companies.

### How do I check the live petrol price in {city}?

You can use the Indian Oil, BPCL or HPCL apps, or IOCL's SMS service: send "RSP" to 9224992249. The prices on this page are updated daily from official OMC data.

## Sources

- Indian Oil Corporation: daily retail selling price data (iocl.com)
- BPCL and HPCL retail fuel price data
- Ministry of Petroleum and Natural Gas: fuel price data portal

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "ImageObject",
  "contentUrl": "https://www.calxo.in/images/petrol/petrol-price-{image_slug}.png",
  "url": "https://www.calxo.in/images/petrol/petrol-price-{image_slug}.png",
  "name": "Petrol & diesel price in {city} on {date_human}",
  "description": "{image_alt}",
  "width": 1200,
  "height": 630,
  "uploadDate": "{today}T06:00:00+05:30",
  "creditText": "Calxo.in",
  "creator": {{
    "@type": "Organization",
    "@id": "https://www.calxo.in/#organization",
    "name": "Calxo"
  }},
  "copyrightNotice": "Calxo.in",
  "license": "https://www.calxo.in/about/",
  "encodingFormat": "image/png",
  "representativeOfPage": true
}}
</script>
"""
    return fm + body


def main():
    today = date.today().isoformat()
    with open(DATA_FILE) as f:
        data = json.load(f)
    all_cities = data["cities"]
    # Use the data file's own 'updated' date so pages match the scraped data.
    today = data.get("updated", today)

    written, skipped = 0, []
    for rec in all_cities:
        city = rec["city"]
        if city in SKIP_CITIES:
            skipped.append(city)
            continue
        if city not in META:
            skipped.append(f"{city} (no META)")
            continue
        page = build_page(rec, all_cities, today)
        out = CONTENT_DIR / f"petrol-price-{slugify(city)}.md"
        out.write_text(page)
        written += 1
        print(f"  ✓ {out.relative_to(REPO_DIR)}")

    print(f"\n  Generated {written} city pages | skipped: {', '.join(skipped)}")


if __name__ == "__main__":
    main()
