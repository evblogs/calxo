"""
Calxo.in — Google Search Console weekly performance report.

Pulls the last 7 full days of Search Analytics data (clicks, impressions,
CTR, average position), compares them week-over-week against the prior 7
days, and lists the top queries and pages. Prints to stdout, saves a dated
markdown report under pythonfiles/gsc_weekly_reports/, and posts a summary
to Slack.

Run: python3 calxo_gsc_report.py
     python3 calxo_gsc_report.py --end 2026-07-13   # override the end date

Auth: uses the same service-account key as calxo_gsc_index.py, but needs the
read-only Search Console scope (webmasters.readonly). The service account
must be added as a user on the calxo.in property in Search Console
(Settings -> Users and permissions) or the API returns 403.
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Local default (Mac); CI/other hosts override via GSC_CREDENTIALS_PATH.
CREDENTIALS_FILE = os.environ.get(
    "GSC_CREDENTIALS_PATH", "/Users/luckychamp/gojournal/pythonfiles/gsc-key.json")

# Search Console property. Domain property by default; override with GSC_SITE_URL
# (e.g. "https://www.calxo.in/" for a URL-prefix property).
SITE_URL   = os.environ.get("GSC_SITE_URL", "sc-domain:calxo.in")
BASE_URL   = "https://www.calxo.in"
REPORT_DIR = Path(__file__).parent / "gsc_weekly_reports"

# GSC finalises data with a lag, so end the window a few days back by default.
DATA_LAG_DAYS = 3
ROW_LIMIT     = 10


def get_credentials():
    from google.oauth2 import service_account
    scopes = ["https://www.googleapis.com/auth/webmasters.readonly"]
    return service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=scopes
    )


def query(session, start, end, dimensions=None, row_limit=ROW_LIMIT):
    """Run one searchAnalytics query and return the list of rows."""
    import urllib.parse
    site = urllib.parse.quote(SITE_URL, safe="")
    endpoint = f"https://www.googleapis.com/webmasters/v3/sites/{site}/searchAnalytics/query"
    body = {
        "startDate": start,
        "endDate": end,
        "rowLimit": row_limit,
    }
    if dimensions:
        body["dimensions"] = dimensions
    resp = session.post(endpoint, json=body)
    if resp.status_code != 200:
        err = resp.json().get("error", {}).get("message", resp.text)
        raise RuntimeError(f"GSC API {resp.status_code}: {err}")
    return resp.json().get("rows", [])


def totals(rows):
    """Aggregate clicks / impressions / CTR / position from ungrouped rows."""
    if not rows:
        return {"clicks": 0, "impressions": 0, "ctr": 0.0, "position": 0.0}
    r = rows[0]
    return {
        "clicks":      int(r.get("clicks", 0)),
        "impressions": int(r.get("impressions", 0)),
        "ctr":         r.get("ctr", 0.0) * 100,
        "position":    r.get("position", 0.0),
    }


def delta(cur, prev):
    if prev == 0:
        return "n/a" if cur == 0 else "new"
    pct = (cur - prev) / prev * 100
    arrow = "▲" if pct >= 0 else "▼"
    return f"{arrow} {abs(pct):.0f}%"


def fmt_query_rows(rows):
    out = []
    for r in rows:
        key = r.get("keys", ["?"])[0]
        out.append({
            "key":         key,
            "clicks":      int(r.get("clicks", 0)),
            "impressions": int(r.get("impressions", 0)),
            "ctr":         r.get("ctr", 0.0) * 100,
            "position":    r.get("position", 0.0),
        })
    return out


def build_report(session, start, end, prev_start, prev_end):
    cur  = totals(query(session, start, end))
    prev = totals(query(session, prev_start, prev_end))
    top_queries = fmt_query_rows(query(session, start, end, ["query"]))
    top_pages   = fmt_query_rows(query(session, start, end, ["page"]))
    return cur, prev, top_queries, top_pages


def render_markdown(start, end, prev_start, prev_end, cur, prev, top_queries, top_pages):
    lines = []
    lines.append(f"# Calxo.in — GSC weekly report")
    lines.append("")
    lines.append(f"**Window:** {start} to {end}  (vs {prev_start} to {prev_end})")
    lines.append(f"**Property:** `{SITE_URL}`")
    lines.append("")
    lines.append("| Metric | This week | Last week | WoW |")
    lines.append("|---|---:|---:|---:|")
    lines.append(f"| Clicks | {cur['clicks']:,} | {prev['clicks']:,} | {delta(cur['clicks'], prev['clicks'])} |")
    lines.append(f"| Impressions | {cur['impressions']:,} | {prev['impressions']:,} | {delta(cur['impressions'], prev['impressions'])} |")
    lines.append(f"| CTR | {cur['ctr']:.2f}% | {prev['ctr']:.2f}% | {delta(cur['ctr'], prev['ctr'])} |")
    lines.append(f"| Avg position | {cur['position']:.1f} | {prev['position']:.1f} | {delta(prev['position'], cur['position'])} |")
    lines.append("")

    lines.append("## Top queries")
    lines.append("")
    lines.append("| Query | Clicks | Impr. | CTR | Pos. |")
    lines.append("|---|---:|---:|---:|---:|")
    for q in top_queries:
        lines.append(f"| {q['key']} | {q['clicks']:,} | {q['impressions']:,} | {q['ctr']:.1f}% | {q['position']:.1f} |")
    lines.append("")

    lines.append("## Top pages")
    lines.append("")
    lines.append("| Page | Clicks | Impr. | CTR | Pos. |")
    lines.append("|---|---:|---:|---:|---:|")
    for p in top_pages:
        page = p["key"].replace(BASE_URL, "") or "/"
        lines.append(f"| {page} | {p['clicks']:,} | {p['impressions']:,} | {p['ctr']:.1f}% | {p['position']:.1f} |")
    lines.append("")
    return "\n".join(lines)


def post_slack(start, end, cur, prev, top_queries):
    """Post a summary to Slack via webhook (same .env as the indexer)."""
    import urllib.request
    import ssl
    env_file = os.environ.get("SLACK_ENV_PATH",
                              "/Users/luckychamp/gojournal/pythonfiles/.env")
    webhook = os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook:
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

    top = "\n".join(
        f"  • {q['key']} — {q['clicks']} clicks, {q['impressions']} impr, pos {q['position']:.1f}"
        for q in top_queries[:5]
    ) or "  • (no data)"
    msg = (
        f"*calxo.in — GSC weekly report — {start} to {end}*\n\n"
        f"• Clicks       : {cur['clicks']:,}  ({delta(cur['clicks'], prev['clicks'])} WoW)\n"
        f"• Impressions  : {cur['impressions']:,}  ({delta(cur['impressions'], prev['impressions'])} WoW)\n"
        f"• CTR          : {cur['ctr']:.2f}%\n"
        f"• Avg position : {cur['position']:.1f}\n\n"
        f"*Top queries:*\n{top}"
    )
    try:
        payload = json.dumps({"text": msg}).encode()
        req = urllib.request.Request(
            webhook, data=payload, headers={"Content-Type": "application/json"})
        ctx = ssl.create_default_context()
        urllib.request.urlopen(req, timeout=10, context=ctx)
        print("  Slack notification sent.")
    except Exception as e:
        print(f"  Slack failed: {e}")


def main():
    import google.auth.transport.requests as google_requests

    # Determine the 7-day window (allow --end YYYY-MM-DD override).
    end_override = None
    if "--end" in sys.argv:
        end_override = sys.argv[sys.argv.index("--end") + 1]

    end_date   = (datetime.strptime(end_override, "%Y-%m-%d") if end_override
                  else datetime.now() - timedelta(days=DATA_LAG_DAYS))
    start_date = end_date - timedelta(days=6)
    prev_end   = start_date - timedelta(days=1)
    prev_start = prev_end - timedelta(days=6)

    start, end             = start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")
    prev_start_s, prev_end_s = prev_start.strftime("%Y-%m-%d"), prev_end.strftime("%Y-%m-%d")

    print("=" * 65)
    print("  Calxo.in — GSC weekly performance report")
    print("=" * 65)
    print(f"\n  Property : {SITE_URL}")
    print(f"  Window   : {start} to {end}")
    print(f"  Baseline : {prev_start_s} to {prev_end_s}\n")

    try:
        creds  = get_credentials()
        authed = google_requests.AuthorizedSession(creds)
    except Exception as e:
        print(f"  ERROR loading credentials: {e}")
        print(f"  (looked for key at: {CREDENTIALS_FILE})")
        print("  In CI this usually means the GSC_KEY_JSON secret is unset/empty.")
        sys.exit(1)

    try:
        cur, prev, top_queries, top_pages = build_report(
            authed, start, end, prev_start_s, prev_end_s)
    except RuntimeError as e:
        print(f"  ERROR: {e}")
        if "403" in str(e):
            print("  The service account likely lacks access to this property.")
            print("  In Search Console -> Settings -> Users and permissions, add:")
            print("    evblog-in@evblogs-url-indexing.iam.gserviceaccount.com")
            print("  Or set GSC_SITE_URL to the correct property (sc-domain: vs URL-prefix).")
        sys.exit(1)

    md = render_markdown(start, end, prev_start_s, prev_end_s,
                         cur, prev, top_queries, top_pages)
    print(md)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = REPORT_DIR / f"{end}.md"
    out_file.write_text(md + "\n")
    latest = REPORT_DIR / "latest.md"
    latest.write_text(md + "\n")
    print(f"\n  Saved report -> {out_file}")

    post_slack(start, end, cur, prev, top_queries)


if __name__ == "__main__":
    main()
