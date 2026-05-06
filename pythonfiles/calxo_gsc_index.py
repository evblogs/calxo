"""
Calxo.in — Google Search Console Indexing API
Submits all calxo.in pages to the Indexing API for faster crawling.

SETUP (one-time):
  1. Go to GSC → Settings → Users & permissions → Add user
  2. Add: evblog-in@evblogs-url-indexing.iam.gserviceaccount.com
  3. Set role: Owner (required for Indexing API)
  4. Enable "Indexing API" at console.cloud.google.com for the project

Run: python3 calxo_gsc_index.py
"""

import json, time
from pathlib import Path

CREDENTIALS_FILE = "/Users/luckychamp/gojournal/pythonfiles/gsc-key.json"
BASE_URL         = "https://www.calxo.in"

# All pages — update this list as new pages are added
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

    # Tax
    "/tax/",
    "/tax/income-tax-calculator/",
    "/tax/gst-calculator/",
    "/tax/tds-calculator/",
    "/tax/old-vs-new-tax-regime/",
    "/tax/capital-gains-calculator/",

    # Salary
    "/salary/",
    "/salary/hra-calculator/",
    "/salary/takehome-calculator/",
    "/salary/gratuity-calculator/",
    "/salary/epf-calculator/",
    "/salary/salary-hike-calculator/",

    # Blog
    "/blog/",
    "/blog/sip-vs-lumpsum-india/",
    "/blog/how-much-home-loan-on-salary/",
    "/blog/old-vs-new-tax-regime-fy-2025-26/",

    # Conversion
    "/conversion/",
    "/conversion/currency-converter/",
    "/conversion/petrol-price-today/",

    # Math
    "/math/",
    "/math/percentage-calculator/",
    "/math/date-calculator/",
    "/math/age-calculator/",

    # Static
    "/about/",
    "/privacy-policy/",
    "/terms-and-conditions/",
]


def get_credentials():
    from google.oauth2 import service_account
    scopes = ["https://www.googleapis.com/auth/indexing"]
    creds  = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=scopes
    )
    return creds


def submit_url(session, url, notification_type="URL_UPDATED"):
    """Submit a URL to the Indexing API."""
    endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"
    payload  = {"url": url, "type": notification_type}
    resp     = session.post(endpoint, json=payload)
    return resp.status_code, resp.json()


def main():
    import google.auth.transport.requests as google_requests

    print("=" * 65)
    print("  Calxo.in — GSC Indexing API Submission")
    print("=" * 65)

    try:
        creds   = get_credentials()
        authed  = google_requests.AuthorizedSession(creds)
    except Exception as e:
        print(f"\n  ERROR loading credentials: {e}")
        print("  Make sure the service account JSON is at:")
        print(f"  {CREDENTIALS_FILE}")
        return

    full_urls = [BASE_URL + path for path in URLS]
    print(f"\n  Submitting {len(full_urls)} URLs...\n")

    results   = {"success": [], "error": []}

    for url in full_urls:
        status, body = submit_url(authed, url)
        if status == 200:
            results["success"].append(url)
            print(f"  ✓  {url}")
        else:
            err = body.get("error", {}).get("message", str(body))
            results["error"].append((url, err))
            print(f"  ✗  {url}  →  {err}")
        time.sleep(0.5)   # stay under quota (600 req/day)

    print(f"\n{'='*65}")
    print(f"  Done. {len(results['success'])} submitted, {len(results['error'])} failed.")

    if results["error"]:
        print("\n  Failed URLs:")
        for url, err in results["error"]:
            print(f"    {url}")
            print(f"      → {err}")

    # Common error messages and fixes
    if results["error"]:
        msgs = " ".join(e for _, e in results["error"]).lower()
        if "permission" in msgs or "403" in msgs:
            print("\n  FIX: Service account not added as Owner in GSC.")
            print("  → GSC → calxo.in → Settings → Users & permissions")
            print("  → Add: evblog-in@evblogs-url-indexing.iam.gserviceaccount.com (Owner)")
        if "not enabled" in msgs or "api" in msgs:
            print("\n  FIX: Indexing API not enabled.")
            print("  → console.cloud.google.com → APIs & Services → Enable 'Indexing API'")

    print(f"\n  Note: Google processes indexing requests within minutes to hours.")
    print(f"  Check coverage in GSC → Indexing → Pages in 24–48 hours.")


if __name__ == "__main__":
    main()
