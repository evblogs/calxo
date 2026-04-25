"""
Calxo.in — Low Competition Keyword Discovery (India)
Uses GenerateKeywordIdeas to discover long-tail variants around each
calculator category, then filters for competition = LOW (1).

Run: python3 calxo_kw_lowcomp.py
"""

import os, time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path("/Users/luckychamp/gojournal/pythonfiles/.env"))

GEO_INDIA = "geoTargetConstants/2356"

# Seeds — one or two head terms per category to generate ideas from
SEEDS = {
    "EMI":              ["emi calculator", "loan emi calculator india"],
    "Home Loan":        ["home loan calculator india", "housing loan calculator"],
    "Personal Loan":    ["personal loan calculator india", "personal loan emi calculator"],
    "Car Loan":         ["car loan emi calculator india", "vehicle loan calculator"],
    "Education Loan":   ["education loan calculator india", "student loan emi calculator"],
    "SIP":              ["sip calculator india", "mutual fund sip returns calculator"],
    "FD":               ["fixed deposit calculator india", "fd interest calculator"],
    "RD":               ["recurring deposit calculator india", "rd maturity calculator"],
    "PPF":              ["ppf calculator india", "ppf maturity amount calculator"],
    "Lumpsum":          ["lumpsum investment calculator india", "one time mutual fund calculator"],
    "Compound Interest":["compound interest calculator india", "ci calculator"],
    "NPS":              ["nps calculator india", "national pension scheme calculator"],
    "Income Tax":       ["income tax calculator india 2025", "salary tax calculator india"],
    "Old vs New Regime":["new tax regime vs old tax regime calculator", "which tax regime is better calculator"],
    "GST":              ["gst calculator india", "reverse gst calculator"],
    "TDS":              ["tds calculator india", "tds on fd calculator", "tds on salary calculator"],
    "HRA":              ["hra exemption calculator india", "house rent allowance calculator"],
    "Gratuity":         ["gratuity calculator india", "gratuity calculation formula india"],
    "Take-Home":        ["in hand salary calculator india", "ctc to take home calculator"],
    "EPF":              ["epf calculator india", "pf corpus calculator retirement"],
    "Capital Gains":    ["capital gains tax calculator india", "ltcg stcg calculator"],
    "Stamp Duty":       ["stamp duty calculator india", "property registration charges calculator"],
    "FOIR":             ["foir calculator india", "loan eligibility foir calculator"],
}


def get_ads_client():
    from google.ads.googleads.client import GoogleAdsClient
    return GoogleAdsClient.load_from_dict({
        "developer_token":   os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN"),
        "client_id":         os.getenv("GOOGLE_ADS_CLIENT_ID"),
        "client_secret":     os.getenv("GOOGLE_ADS_CLIENT_SECRET"),
        "refresh_token":     os.getenv("GOOGLE_ADS_REFRESH_TOKEN"),
        "login_customer_id": os.getenv("GOOGLE_ADS_CUSTOMER_ID", "").replace("-", ""),
        "use_proto_plus":    True,
    })


COMP_LABEL = {0: "UNKNOWN", 1: "LOW", 2: "MEDIUM", 3: "HIGH", 4: "VERY_HIGH"}

def fetch_ideas(client, seed_keywords, cat_label):
    """Use GenerateKeywordIdeas to get related long-tail keywords."""
    svc = client.get_service("KeywordPlanIdeaService")
    cid = os.getenv("GOOGLE_ADS_CUSTOMER_ID", "").replace("-", "")
    results = []

    req = client.get_type("GenerateKeywordIdeasRequest")
    req.customer_id = cid
    req.geo_target_constants.extend([GEO_INDIA])
    req.language             = "languageConstants/1000"
    req.keyword_plan_network = client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH
    req.include_adult_keywords = False
    req.keyword_seed.keywords.extend(seed_keywords)

    try:
        response = svc.generate_keyword_ideas(request=req)
        for idea in response:
            kw   = idea.text.lower().strip()
            vol  = idea.keyword_idea_metrics.avg_monthly_searches if idea.keyword_idea_metrics else 0
            comp_val = int(idea.keyword_idea_metrics.competition) if idea.keyword_idea_metrics else 0
            comp = COMP_LABEL.get(comp_val, "UNKNOWN")
            results.append((cat_label, kw, vol, comp))
    except Exception as e:
        print(f"  Warning ({cat_label}): {e}")

    time.sleep(0.5)
    return results


def main():
    print("Connecting to Google Ads API...")
    client = get_ads_client()

    all_ideas = []
    for cat, seeds in SEEDS.items():
        print(f"  Fetching ideas: {cat}...")
        ideas = fetch_ideas(client, seeds, cat)
        all_ideas.extend(ideas)
        print(f"    → {len(ideas)} ideas returned")

    # Deduplicate by keyword text
    seen = {}
    for cat, kw, vol, comp in all_ideas:
        if kw not in seen or seen[kw][1] < vol:
            seen[kw] = (cat, vol, comp)

    deduped = [(kw, cat, vol, comp) for kw, (cat, vol, comp) in seen.items()]

    # Filter: LOW competition only
    low_comp = [(cat, kw, vol, comp) for kw, cat, vol, comp in deduped if comp == "LOW"]
    low_comp.sort(key=lambda x: -x[2])

    print(f"\n{'='*75}")
    print(f"  CALXO — LOW COMPETITION KEYWORDS (India)")
    print(f"  Total ideas fetched: {len(deduped)} | LOW competition: {len(low_comp)}")
    print(f"{'='*75}\n")

    if not low_comp:
        print("  No LOW competition keywords found. Showing MEDIUM with vol 100–3,000:\n")
        medium = [(cat, kw, vol, comp) for kw, cat, vol, comp in deduped
                  if comp == "MEDIUM" and 100 <= vol <= 3000]
        medium.sort(key=lambda x: -x[2])
        low_comp = medium

    print(f"  {'Category':<22} {'Keyword':<50} {'Volume':>8}  Competition")
    print("-" * 90)
    for cat, kw, vol, comp in low_comp:
        marker = " ★" if vol >= 1000 else ""
        print(f"  {cat:<22} {kw:<50} {vol:>8,}  {comp}{marker}")

    # Group by category for a clean summary
    print(f"\n\n{'='*75}")
    print("  BY CATEGORY — LOW COMPETITION ONLY")
    print(f"{'='*75}")
    cats_seen = {}
    for cat, kw, vol, comp in low_comp:
        cats_seen.setdefault(cat, []).append((kw, vol))

    for cat, rows in sorted(cats_seen.items(), key=lambda x: -sum(r[1] for r in x[1])):
        rows.sort(key=lambda r: -r[1])
        total_vol = sum(r[1] for r in rows)
        print(f"\n── {cat} ({len(rows)} keywords, {total_vol:,} total vol/mo) ──")
        for kw, vol in rows:
            print(f"    {kw:<52} {vol:>8,}/mo")

    print(f"\n\n{'='*75}")
    print("  RECOMMENDED PAGES TO BUILD (by category, vol > 0)")
    print(f"{'='*75}")
    built = {
        "emi-calculator", "foir-calculator", "sip-calculator", "fd-calculator",
        "ppf-calculator", "lumpsum-calculator", "compound-interest-calculator",
        "sip-calculator", "currency-converter", "gst-calculator",
        "income-tax-calculator", "hra-calculator", "gratuity-calculator",
        "takehome-calculator", "rd-calculator", "epf-calculator",
        "home-loan-eligibility", "tds-calculator",
    }
    for cat, rows in sorted(cats_seen.items(), key=lambda x: -sum(r[1] for r in x[1])):
        rows.sort(key=lambda r: -r[1])
        if rows[0][1] > 0:
            print(f"  {cat:<22} → top keyword: \"{rows[0][0]}\" ({rows[0][1]:,}/mo)")


if __name__ == "__main__":
    main()
