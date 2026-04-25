"""
Calxo.in — Calculator Keyword Research (India)
Fetches India search volumes + competition for all calculator categories.
Outputs easy-win keywords: good volume + LOW competition.

Run: python3 calxo_keyword_research.py
"""

import os, time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path("/Users/luckychamp/gojournal/pythonfiles/.env"))

GEO_INDIA = "geoTargetConstants/2356"

KEYWORDS = {
    "EMI": [
        "emi calculator",
        "home loan emi calculator",
        "personal loan emi calculator",
        "car loan emi calculator",
        "loan emi calculator",
        "emi calculator india",
        "monthly emi calculator",
        "emi calculator for home loan",
        "emi calculator for personal loan",
        "hdfc emi calculator",
        "sbi emi calculator",
        "icici emi calculator",
        "axis bank emi calculator",
        "bike loan emi calculator",
        "education loan emi calculator",
    ],
    "SIP": [
        "sip calculator",
        "sip return calculator",
        "sip calculator india",
        "mutual fund sip calculator",
        "sip calculator online",
        "monthly sip calculator",
        "sip maturity calculator",
        "best sip calculator",
        "sip calculator 10 years",
        "sip calculator 20 years",
        "sip amount calculator",
        "sip investment calculator",
        "sip calculator for 1 crore",
        "sip calculator zerodha",
        "groww sip calculator",
    ],
    "FD": [
        "fd calculator",
        "fixed deposit calculator",
        "fd maturity calculator",
        "fd interest calculator",
        "sbi fd calculator",
        "hdfc fd calculator",
        "icici fd calculator",
        "post office fd calculator",
        "fd calculator online",
        "fd calculator india",
        "fd calculator quarterly",
        "fd rate calculator",
        "fd calculator 1 year",
        "fd calculator 5 years",
        "bank fd calculator",
    ],
    "RD": [
        "rd calculator",
        "recurring deposit calculator",
        "rd maturity calculator",
        "sbi rd calculator",
        "post office rd calculator",
        "rd interest calculator",
        "rd calculator online",
        "rd calculator india",
        "monthly rd calculator",
        "rd calculator 2 years",
        "rd calculator 5 years",
        "hdfc rd calculator",
        "recurring deposit maturity calculator",
        "rd calculator quarterly",
    ],
    "PPF": [
        "ppf calculator",
        "ppf maturity calculator",
        "ppf interest calculator",
        "ppf calculator india",
        "ppf return calculator",
        "ppf calculator online",
        "ppf calculator 15 years",
        "ppf investment calculator",
        "ppf calculator sbi",
        "ppf calculator post office",
        "ppf yearly calculator",
        "ppf calculator with extension",
        "ppf balance calculator",
        "ppf calculator 2025",
        "ppf calculator 2026",
    ],
    "Income Tax": [
        "income tax calculator",
        "income tax calculator india",
        "income tax calculator 2025-26",
        "income tax calculator 2024-25",
        "new tax regime calculator",
        "old vs new tax regime calculator",
        "salary income tax calculator",
        "income tax calculator online",
        "income tax calculator for salaried",
        "it calculator india",
        "income tax calculator fy 2025-26",
        "tax calculator india 2026",
        "income tax calculator after budget 2025",
        "how much income tax do i pay",
        "take home salary calculator after tax",
    ],
    "GST": [
        "gst calculator",
        "gst calculator india",
        "gst calculator online",
        "gst amount calculator",
        "18% gst calculator",
        "12% gst calculator",
        "5% gst calculator",
        "28% gst calculator",
        "gst inclusive calculator",
        "gst exclusive calculator",
        "reverse gst calculator",
        "gst tax calculator",
        "gst calculation formula",
        "gst on invoice calculator",
        "cgst sgst calculator",
    ],
    "HRA": [
        "hra calculator",
        "hra exemption calculator",
        "hra calculator india",
        "hra tax calculator",
        "hra calculation formula",
        "hra calculator for metro city",
        "hra calculator online",
        "house rent allowance calculator",
        "hra exemption calculator online",
        "hra calculator salary",
        "hra deduction calculator",
        "section 10 hra calculator",
        "hra claim calculator",
    ],
    "Gratuity": [
        "gratuity calculator",
        "gratuity calculation formula",
        "gratuity calculator india",
        "gratuity amount calculator",
        "gratuity calculator online",
        "gratuity calculator for private sector",
        "gratuity calculator after 5 years",
        "gratuity payment calculator",
        "how to calculate gratuity",
        "gratuity eligible years calculator",
        "gratuity calculator 2025",
        "gratuity taxable calculator",
    ],
    "EPF / PF": [
        "epf calculator",
        "pf calculator",
        "provident fund calculator",
        "epf balance calculator",
        "epf corpus calculator",
        "pf retirement calculator",
        "epfo calculator",
        "epf interest calculator",
        "pf amount calculator",
        "epf calculator india",
        "pf calculator monthly",
        "employee provident fund calculator",
        "epf maturity calculator",
        "pf corpus calculator",
        "epf calculator retirement",
    ],
    "TDS": [
        "tds calculator",
        "tds calculation",
        "tds on fd calculator",
        "tds calculator india",
        "tds rate calculator",
        "tds on salary calculator",
        "tds on rent calculator",
        "tds deduction calculator",
        "section 194a tds calculator",
        "tds on professional fees calculator",
        "tds calculator online",
        "how to calculate tds",
        "tds on interest calculator",
        "tds calculator 2025-26",
        "tds calculator for contractor",
    ],
    "Home Loan Eligibility": [
        "home loan eligibility calculator",
        "housing loan eligibility calculator",
        "home loan amount calculator",
        "how much home loan can i get",
        "home loan calculator eligibility",
        "sbi home loan eligibility calculator",
        "hdfc home loan eligibility",
        "icici home loan eligibility",
        "home loan eligibility based on salary",
        "home loan eligibility check",
        "home loan eligibility calculator india",
        "maximum home loan amount calculator",
        "home loan affordability calculator",
    ],
    "Take-Home Salary": [
        "take home salary calculator",
        "in hand salary calculator",
        "salary calculator india",
        "net salary calculator",
        "ctc to in hand salary calculator",
        "salary breakup calculator",
        "monthly salary calculator",
        "salary calculator after tax india",
        "net take home salary calculator",
        "salary calculator 2025",
        "salary calculator for 10 lpa",
        "salary calculator for 15 lpa",
        "salary calculator for 20 lpa",
        "gross to net salary calculator india",
        "ctc calculator india",
    ],
    "Lumpsum": [
        "lumpsum calculator",
        "lumpsum investment calculator",
        "lumpsum return calculator",
        "mutual fund lumpsum calculator",
        "lumpsum sip calculator",
        "lumpsum vs sip calculator",
        "lumpsum calculator india",
        "lumpsum calculator online",
        "lumpsum maturity calculator",
        "one time investment calculator",
    ],
    "Compound Interest": [
        "compound interest calculator",
        "compound interest calculator india",
        "compound interest calculator online",
        "daily compound interest calculator",
        "monthly compound interest calculator",
        "annual compound interest calculator",
        "compound interest formula calculator",
        "simple vs compound interest calculator",
        "compound interest calculator with monthly contributions",
        "ci calculator india",
    ],
    "Currency Converter": [
        "currency converter",
        "usd to inr calculator",
        "dollar to rupee converter",
        "currency converter india",
        "inr to usd calculator",
        "forex calculator india",
        "currency exchange calculator",
        "gbp to inr calculator",
        "euro to inr calculator",
        "currency rate calculator",
    ],
    "FOIR": [
        "foir calculator",
        "foir calculation",
        "fixed obligations to income ratio calculator",
        "loan eligibility foir",
        "foir home loan",
        "foir calculator india",
        "what is foir in home loan",
        "foir calculator sbi",
    ],
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


def fetch_volumes(client, keywords):
    svc     = client.get_service("KeywordPlanIdeaService")
    cid     = os.getenv("GOOGLE_ADS_CUSTOMER_ID", "").replace("-", "")
    results = {}

    for i in range(0, len(keywords), 100):
        batch = keywords[i:i + 100]
        req   = client.get_type("GenerateKeywordHistoricalMetricsRequest")
        req.customer_id = cid
        req.keywords.extend(batch)
        req.geo_target_constants.extend([GEO_INDIA])
        req.language             = "languageConstants/1000"
        req.keyword_plan_network = client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH
        try:
            for r in svc.generate_keyword_historical_metrics(request=req).results:
                kw   = r.text.lower().strip()
                vol  = r.keyword_metrics.avg_monthly_searches if r.keyword_metrics else 0
                comp = str(r.keyword_metrics.competition).split(".")[-1] if r.keyword_metrics else "UNKNOWN"
                results[kw] = (vol, comp)
        except Exception as e:
            print(f"  Warning: {e}")
        time.sleep(0.4)

    return results


def main():
    # Flatten all keywords
    all_kws = sorted(set(kw.lower() for kws in KEYWORDS.values() for kw in kws))
    print(f"Fetching India volumes for {len(all_kws)} Calxo keywords...\n")

    client  = get_ads_client()
    vol_map = fetch_volumes(client, all_kws)

    # Build category results
    print(f"\n{'='*75}")
    print(f"  CALXO.IN — EASY WIN KEYWORDS (India, LOW competition, sorted by volume)")
    print(f"{'='*75}\n")

    # Competition mapping: 0=UNKNOWN, 1=LOW, 2=MEDIUM, 3=HIGH, 4=VERY_HIGH
    COMP_LABEL = {"0": "UNKNOWN", "1": "LOW", "2": "MEDIUM", "3": "HIGH", "4": "VERY_HIGH"}

    easy_wins = []
    all_rows  = []

    for cat, kws in KEYWORDS.items():
        for kw in kws:
            vol, comp_raw = vol_map.get(kw.lower(), (0, "0"))
            comp = COMP_LABEL.get(str(comp_raw), str(comp_raw))
            all_rows.append((cat, kw, vol, comp))
            # Easy win for a new site: MEDIUM or UNKNOWN competition, 100–20000/month
            # (LOW comp barely exists in finance; MEDIUM + low volume is the real opportunity)
            if comp in ("LOW", "MEDIUM", "UNKNOWN") and 100 <= vol <= 20000:
                easy_wins.append((cat, kw, vol, comp))

    easy_wins.sort(key=lambda x: -x[2])

    # Print easy wins
    print(f"  Filter: MEDIUM/LOW/UNKNOWN competition, 100–20,000 searches/month")
    print(f"  (Sweet spot for a new site — high enough to matter, achievable to rank)\n")
    print(f"{'Category':<22} {'Keyword':<48} {'Volume':>8}  Competition")
    print("-" * 90)
    for cat, kw, vol, comp in easy_wins:
        marker = " ★" if vol >= 5000 else (" ✓" if vol >= 1000 else "")
        print(f"  {cat:<20} {kw:<48} {vol:>8,}  {comp}{marker}")

    # Print by category (all)
    print(f"\n\n{'='*75}")
    print("  ALL KEYWORDS BY CATEGORY")
    print(f"{'='*75}")
    for cat, kws in KEYWORDS.items():
        rows = [(kw, *vol_map.get(kw.lower(), (0, "0"))) for kw in kws]
        rows.sort(key=lambda x: -x[1])
        print(f"\n── {cat} ──")
        print(f"  {'Keyword':<48} {'Volume':>8}  Competition")
        for kw, vol, comp_raw in rows:
            comp = COMP_LABEL.get(str(comp_raw), str(comp_raw))
            flag = ""
            if comp == "LOW":                         flag = "  ← EASY WIN"
            elif comp == "MEDIUM" and vol <= 20000:   flag = "  ← TARGET"
            elif comp == "HIGH":                      flag = ""
            elif comp == "UNKNOWN" and vol >= 100:    flag = "  ← GAP?"
            print(f"  {kw:<48} {vol:>8,}  {comp}{flag}")

    print(f"\n\n{'='*75}")
    print("  SUMMARY")
    print(f"{'='*75}")
    print(f"  Total easy wins (LOW comp, 500+ vol): {len(easy_wins)}")
    for cat in KEYWORDS:
        cat_wins = [r for r in easy_wins if r[0] == cat]
        if cat_wins:
            print(f"    {cat:<22} {len(cat_wins)} easy wins, top: {cat_wins[0][1]} ({cat_wins[0][2]:,}/mo)")


if __name__ == "__main__":
    main()
