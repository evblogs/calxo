"""
Calxo.in — Google Search Console Indexing API
Only submits URLs that haven't been submitted before.
Tracks submissions in calxo_gsc_submitted.json.

Run: python3 calxo_gsc_index.py
Add new pages to URLS list — already-submitted ones are skipped automatically.
"""

import json, time, os
from pathlib import Path
from datetime import datetime

# Local default (Mac); CI/other hosts override via GSC_CREDENTIALS_PATH.
CREDENTIALS_FILE = os.environ.get(
    "GSC_CREDENTIALS_PATH", "/Users/luckychamp/gojournal/pythonfiles/gsc-key.json")
BASE_URL         = "https://www.calxo.in"
TRACKER_FILE     = Path(__file__).parent / "calxo_gsc_submitted.json"

# All pages — add new ones here. Already-submitted URLs are skipped.
URLS = [
    # Home
    "/",

    # Loan
    "/loan/",
    "/loan/emi-calculator/",
    "/loan/foir-calculator/",
    "/loan/home-loan-eligibility/",
    "/loan/car-loan-calculator/",
    "/loan/education-loan-calculator/",
    "/loan/stamp-duty-calculator/",
    "/loan/personal-loan-calculator/",
    "/loan/bike-loan-calculator/",

    # Investment
    "/investment/",
    "/investment/sip-calculator/",
    "/investment/lumpsum-calculator/",
    "/investment/fd-calculator/",
    "/investment/rd-calculator/",
    "/investment/ppf-calculator/",
    "/investment/compound-interest-calculator/",
    "/investment/nps-calculator/",
    "/investment/ups-pension-calculator/",
    "/investment/nps-vatsalya-calculator/",
    "/investment/crorepati-clock/",

    # Tax
    "/tax/",
    "/tax/income-tax-calculator/",
    "/tax/tds-calculator/",
    "/tax/old-vs-new-tax-regime/",
    "/tax/capital-gains-calculator/",
    "/tax/freelancer-tax-44ada-calculator/",

    # GST
    "/gst/",
    "/gst/gst-calculator/",
    "/gst/lifetime-bill/",

    # Salary
    "/salary/",
    "/salary/hra-calculator/",
    "/salary/takehome-calculator/",
    "/salary/gratuity-calculator/",
    "/salary/epf-calculator/",
    "/salary/salary-hike-calculator/",
    "/salary/salary-breakup-excel/",
    "/salary/salary-to-hourly-calculator/",
    "/salary/maternity-leave-calculator/",

    # Blog
    "/blog/",
    "/blog/sip-vs-lumpsum-india/",
    "/blog/how-much-home-loan-on-salary/",
    "/blog/old-vs-new-tax-regime-fy-2025-26/",
    "/blog/50-30-20-budget-rule-india/",
    "/blog/car-depreciation-india/",
    "/blog/credit-card-interest-calculation-india/",
    "/blog/ctc-full-form-in-salary/",
    "/blog/debt-to-income-ratio-india/",
    "/blog/emergency-fund-how-much-india/",
    "/blog/epf-interest-calculation-india/",
    "/blog/fd-vs-rd-which-is-better/",
    "/blog/gold-investment-india-returns/",
    "/blog/gratuity-calculation-formula-india/",
    "/blog/home-loan-prepayment-saves-money/",
    "/blog/how-hra-exemption-is-calculated/",
    "/blog/inflation-impact-on-savings-india/",
    "/blog/net-worth-calculation-india/",
    "/blog/ppf-maturity-amount-calculation/",
    "/blog/ppf-vs-elss-80c/",
    "/blog/rd-interest-calculation-formula/",
    "/blog/reverse-gst-calculation-india/",
    "/blog/section-80c-deductions-complete-guide/",
    "/blog/sovereign-gold-bond-vs-gold-etf/",
    "/blog/stamp-duty-registration-charges-india/",
    "/blog/sukanya-samriddhi-yojana-calculator/",
    "/blog/tds-on-salary-how-it-works/",
    "/blog/ups-vs-nps-which-is-better-2026/",
    "/blog/30-lakh-ctc-take-home-salary/",
    "/blog/35-lakh-ctc-take-home-salary/",
    "/blog/6-lakh-ctc-take-home-salary/",
    "/blog/8-lakh-ctc-take-home-salary/",
    "/blog/home-loan-vs-renting-india/",
    "/blog/loan-amortization-interest-heavy-start/",

    # Investment — new calcs
    "/investment/cagr-calculator/",
    "/investment/simple-interest-calculator/",
    "/investment/stock-average-calculator/",
    "/investment/step-up-sip-calculator/",
    "/investment/inflation-calculator/",
    "/investment/retirement-calculator/",
    "/investment/gold-calculator/",
    "/investment/ssy-calculator/",

    # Loan — new calcs
    "/loan/loan-prepayment-calculator/",
    "/loan/credit-card-payoff-calculator/",

    # Tax — new calcs
    "/tax/nps-tax-benefit-calculator/",

    # Health — new calcs
    "/health/bmr-calculator/",

    # Author
    "/about/vignesh/",

    # Categories
    "/categories/",
    "/categories/conversion-calculators/",
    "/categories/gst-calculators/",
    "/categories/health-calculators/",
    "/categories/investment-calculators/",
    "/categories/investment/",
    "/categories/loan-calculators/",
    "/categories/loans/",
    "/categories/math-calculators/",
    "/categories/salary--hr-calculators/",
    "/categories/salary/",
    "/categories/tax-calculators/",

    # Conversion
    "/conversion/",
    "/conversion/currency-converter/",
    "/conversion/petrol-price-today/",
    "/conversion/petrol-price-bangalore/",
    "/conversion/petrol-price-chennai/",
    "/conversion/petrol-price-delhi/",
    "/conversion/petrol-price-mumbai/",
    "/conversion/petrol-price-kolkata/",
    "/conversion/petrol-price-hyderabad/",
    "/conversion/petrol-price-pune/",
    "/conversion/petrol-price-ahmedabad/",
    "/conversion/petrol-price-jaipur/",
    "/conversion/petrol-price-lucknow/",
    "/conversion/petrol-price-noida/",
    "/conversion/petrol-price-chandigarh/",
    "/conversion/petrol-price-bhopal/",
    "/conversion/petrol-price-indore/",
    "/conversion/petrol-price-patna/",
    "/conversion/petrol-price-ranchi/",
    "/conversion/petrol-price-raipur/",
    "/conversion/petrol-price-bhubaneswar/",
    "/conversion/petrol-price-guwahati/",
    "/conversion/petrol-price-thiruvananthapuram/",
    "/conversion/petrol-price-kochi/",
    "/conversion/petrol-price-coimbatore/",
    "/conversion/petrol-price-visakhapatnam/",
    "/conversion/petrol-price-nagpur/",
    "/conversion/petrol-price-surat/",
    "/conversion/petrol-price-vadodara/",
    "/conversion/petrol-price-ludhiana/",
    "/conversion/petrol-price-agra/",
    "/conversion/petrol-price-varanasi/",
    "/conversion/petrol-price-dehradun/",

    # Health
    "/health/",
    "/health/bmi-calculator/",
    "/health/tdee-calculator/",
    "/health/body-fat-calculator/",
    "/health/water-intake-calculator/",
    "/health/calorie-deficit-calculator/",
    "/health/ideal-weight-calculator/",
    "/health/ovulation-calculator/",
    "/health/period-calculator/",
    "/health/bmi-calculator-men/",

    # Math
    "/math/",
    "/math/percentage-calculator/",
    "/math/date-calculator/",
    "/math/age-calculator/",
    "/math/margin-calculator/",
    "/math/discount-calculator/",

    # Business / SaaS
    "/business/",
    "/business/cac-calculator/",
    "/business/ltv-calculator/",
    "/business/ltv-cac-calculator/",
    "/business/mrr-calculator/",
    "/business/churn-rate-calculator/",
    "/business/break-even-calculator/",
    "/business/gross-margin-calculator/",
    "/business/roi-calculator/",

    # Static
    "/about/",
    "/privacy-policy/",
    "/terms-and-conditions/",
    "/embed/",
    "/search/",
]


def load_tracker():
    if TRACKER_FILE.exists():
        return json.loads(TRACKER_FILE.read_text())
    return {}

def save_tracker(tracker):
    TRACKER_FILE.write_text(json.dumps(tracker, indent=2))

def get_credentials():
    from google.oauth2 import service_account
    scopes = ["https://www.googleapis.com/auth/indexing"]
    return service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=scopes
    )

def submit_url(session, url):
    endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"
    resp = session.post(endpoint, json={"url": url, "type": "URL_UPDATED"})
    return resp.status_code, resp.json()


def post_slack(submitted, total, errors):
    """Post a summary to #evblogs-dailypost via Slack webhook."""
    import urllib.request, ssl
    env_file = "/Users/luckychamp/gojournal/pythonfiles/.env"
    webhook = None
    try:
        for line in open(env_file).read().splitlines():
            if line.startswith("SLACK_WEBHOOK_URL="):
                webhook = line.split("=", 1)[1].strip().strip('"').strip("'")
                break
    except Exception:
        pass
    if not webhook:
        print("  Slack: webhook not found, skipping.")
        return

    today   = datetime.now().strftime("%d %b %Y")
    done    = len([u for u in load_tracker()])
    remaining = total - done
    lines   = "\n".join(f"  • {u.replace(BASE_URL,'')}" for u in submitted) or "  • (none)"
    msg = (
        f"*calxo.in — GSC Indexing API — {today}*\n\n"
        f"• Submitted today  : {len(submitted)} URLs\n"
        f"• Total done       : {done} / {total} URLs\n"
        f"• Remaining        : {remaining} URLs\n\n"
        f"*Today's batch:*\n{lines}"
        + (f"\n\n⚠️ {len(errors)} failed: " + ", ".join(u for u,_ in errors) if errors else "")
    )
    try:
        payload = json.dumps({"text": msg}).encode()
        req = urllib.request.Request(webhook, data=payload, headers={"Content-Type": "application/json"})
        ctx = ssl.create_default_context()
        urllib.request.urlopen(req, timeout=10, context=ctx)
        print("  Slack notification sent.")
    except Exception as e:
        print(f"  Slack failed: {e}")


def main():
    import sys
    import google.auth.transport.requests as google_requests

    force = "--force" in sys.argv   # re-submit all URLs regardless of tracker

    print("=" * 65)
    print("  Calxo.in — GSC Indexing API")
    print("=" * 65)

    tracker   = load_tracker()
    full_urls = [BASE_URL + path for path in URLS]
    new_urls  = full_urls if force else [u for u in full_urls if u not in tracker]

    print(f"\n  Total URLs       : {len(full_urls)}")
    print(f"  Already submitted: {len(full_urls) - len(new_urls)}")
    print(f"  To submit now    : {len(new_urls)}")
    if force:
        print("  (--force: re-submitting all)")

    if not new_urls:
        print("\n  Nothing new to submit. Add URLs to URLS list or use --force.")
        return

    try:
        creds  = get_credentials()
        authed = google_requests.AuthorizedSession(creds)
    except Exception as e:
        print(f"\n  ERROR loading credentials: {e}")
        print(f"  (looked for key at: {CREDENTIALS_FILE})")
        print("  In CI this usually means the GSC_KEY_JSON secret is unset/empty.")
        sys.exit(1)

    print()
    results = {"success": [], "error": []}

    for url in new_urls:
        status, body = submit_url(authed, url)
        if status == 200:
            results["success"].append(url)
            tracker[url] = datetime.now().strftime("%Y-%m-%d")
            print(f"  ✓  {url}")
        else:
            err = body.get("error", {}).get("message", str(body))
            results["error"].append((url, err))
            print(f"  ✗  {url}  →  {err}")
        time.sleep(0.5)

    save_tracker(tracker)

    print(f"\n{'='*65}")
    print(f"  Done. {len(results['success'])} submitted, {len(results['error'])} failed.")
    print(f"  Tracker saved → {TRACKER_FILE}")

    if results["error"]:
        print("\n  Failed URLs:")
        for url, err in results["error"]:
            print(f"    {url}  →  {err}")

    print(f"\n  Check GSC → Indexing → Pages in 24–48 hours.")

    # Post to Slack
    if results["success"] or results["error"]:
        post_slack(results["success"], len(full_urls), results["error"])


if __name__ == "__main__":
    main()
