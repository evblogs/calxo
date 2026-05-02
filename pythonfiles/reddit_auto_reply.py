#!/usr/bin/env python3
"""
Calxo Reddit Auto-Reply Bot
============================
Finds relevant personal finance questions on Reddit (personalfinanceindia,
IndiaTax, IndiaInvestments) using RapidAPI, generates helpful human-sounding
answers with a natural Calxo calculator link, and saves them to a review
queue JSON for manual/automated posting.

When REDDIT credentials are set, it can post directly via PRAW.

Run:   python pythonfiles/reddit_auto_reply.py
       python pythonfiles/reddit_auto_reply.py --dry-run   (fetch + score only)
       python pythonfiles/reddit_auto_reply.py --post       (auto-post via PRAW)

Review queue: pythonfiles/reddit_reply_queue.json
Posted log:   pythonfiles/reddit_replied.json
"""

import json
import os
import sys
import time
import random
import argparse
import ssl
from datetime import datetime
from pathlib import Path
import http.client
import urllib.request

try:
    import certifi
    _SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _SSL_CONTEXT = ssl.create_default_context()

# ── Optional PRAW for posting ────────────────────────────────────────────────
try:
    import praw
    PRAW_AVAILABLE = True
except ImportError:
    PRAW_AVAILABLE = False

# ── OpenAI ───────────────────────────────────────────────────────────────────
try:
    from openai import OpenAI
except ImportError:
    print("openai package not found. Run: pip install openai")
    sys.exit(1)

# ── dotenv ───────────────────────────────────────────────────────────────────
try:
    from dotenv import load_dotenv
    # Load calxo .env first, fallback to gojournal .env
    calxo_env = Path(__file__).parent / ".env"
    gojournal_env = Path("/Users/luckychamp/gojournal/pythonfiles/.env")
    if calxo_env.exists():
        load_dotenv(calxo_env, override=True)
    elif gojournal_env.exists():
        load_dotenv(gojournal_env, override=True)
except ImportError:
    pass

# ── Config ───────────────────────────────────────────────────────────────────
RAPIDAPI_KEY       = os.getenv("RAPIDAPI_KEY", "504a398d26msh494811fb032dea1p112cb1jsn1c38f9aed33c")
RAPIDAPI_HOST      = "reddit34.p.rapidapi.com"
OPENAI_API_KEY     = os.getenv("OPENAI_API_KEY")
REDDIT_CLIENT_ID   = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_PASSWORD    = os.getenv("REDDIT_PASSWORD")
REDDIT_USERNAME    = os.getenv("REDDIT_USERNAME", "Temporary_Meeting182")

QUEUE_FILE    = Path(__file__).parent / "reddit_reply_queue.json"
REPLIED_FILE  = Path(__file__).parent / "reddit_replied.json"

TARGET_SUBREDDITS = [
    "personalfinanceindia",
    "IndiaTax",
    "IndiaInvestments",
]

# Max posts to fetch per subreddit per run
FETCH_LIMIT   = 25
# Min relevance score to include in queue
MIN_SCORE     = 3
# Max new replies to generate per run (API cost guard)
MAX_GENERATE  = 8

# ── Calculator keyword → URL map ─────────────────────────────────────────────
CALC_MAP = {
    "salary":       ("Salary Take-Home Calculator",     "https://www.calxo.in/calculators/salary-calculator/"),
    "ctc":          ("CTC to In-Hand Salary Calculator","https://www.calxo.in/calculators/salary-calculator/"),
    "take.home":    ("Salary Take-Home Calculator",     "https://www.calxo.in/calculators/salary-calculator/"),
    "in.hand":      ("Salary Take-Home Calculator",     "https://www.calxo.in/calculators/salary-calculator/"),
    "income tax":   ("Income Tax Calculator",           "https://www.calxo.in/calculators/income-tax-calculator/"),
    "tds":          ("Income Tax Calculator",           "https://www.calxo.in/calculators/income-tax-calculator/"),
    "itr":          ("Income Tax Calculator",           "https://www.calxo.in/calculators/income-tax-calculator/"),
    "old regime":   ("Old vs New Tax Regime Calculator","https://www.calxo.in/calculators/income-tax-calculator/"),
    "new regime":   ("Old vs New Tax Regime Calculator","https://www.calxo.in/calculators/income-tax-calculator/"),
    "emi":          ("EMI Calculator",                  "https://www.calxo.in/calculators/emi-calculator/"),
    "home loan":    ("EMI Calculator",                  "https://www.calxo.in/calculators/emi-calculator/"),
    "car loan":     ("EMI Calculator",                  "https://www.calxo.in/calculators/emi-calculator/"),
    "loan":         ("EMI Calculator",                  "https://www.calxo.in/calculators/emi-calculator/"),
    "sip":          ("SIP Calculator",                  "https://www.calxo.in/calculators/sip-calculator/"),
    "mutual fund":  ("SIP Calculator",                  "https://www.calxo.in/calculators/sip-calculator/"),
    "invest":       ("SIP Calculator",                  "https://www.calxo.in/calculators/sip-calculator/"),
    "fd":           ("FD Calculator",                   "https://www.calxo.in/calculators/fd-calculator/"),
    "fixed deposit":("FD Calculator",                   "https://www.calxo.in/calculators/fd-calculator/"),
    "ppf":          ("PPF Calculator",                  "https://www.calxo.in/calculators/ppf-calculator/"),
    "gst":          ("GST Calculator",                  "https://www.calxo.in/calculators/gst-calculator/"),
    "hra":          ("HRA Exemption Calculator",        "https://www.calxo.in/calculators/hra-calculator/"),
    "gratuity":     ("Gratuity Calculator",             "https://www.calxo.in/calculators/gratuity-calculator/"),
    "epf":          ("EPF Calculator",                  "https://www.calxo.in/calculators/epf-calculator/"),
    "pf":           ("EPF Calculator",                  "https://www.calxo.in/calculators/epf-calculator/"),
    "lpa":          ("Salary Take-Home Calculator",     "https://www.calxo.in/calculators/salary-calculator/"),
    "per annum":    ("Salary Take-Home Calculator",     "https://www.calxo.in/calculators/salary-calculator/"),
    "compound":     ("Compound Interest Calculator",    "https://www.calxo.in/calculators/compound-interest-calculator/"),
    "interest":     ("Compound Interest Calculator",    "https://www.calxo.in/calculators/compound-interest-calculator/"),
    "retirement":   ("Retirement Calculator",           "https://www.calxo.in/calculators/retirement-calculator/"),
    "nps":          ("NPS Calculator",                  "https://www.calxo.in/calculators/nps-calculator/"),
}

# Keywords that strongly indicate a personal finance question (not news/rant)
QUESTION_SIGNALS = [
    "how much", "should i", "help me", "advice", "planning", "calculate",
    "what is", "how do", "need guidance", "confused", "lpa", "ctc",
    "take home", "salary", "tax", "emi", "sip", "fd", "invest", "save",
    "income", "pf", "gratuity", "hra", "regime", "loan",
]


# ── Helpers ──────────────────────────────────────────────────────────────────

def load_json(path: Path, default):
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return default

def save_json(path: Path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def rapidapi_get(endpoint: str, querystring: dict) -> dict:
    """Call RapidAPI reddit34 endpoint, return parsed JSON or {}."""
    params = "&".join(f"{k}={v}" for k, v in querystring.items())
    url = f"https://{RAPIDAPI_HOST}/{endpoint}?{params}"
    req = urllib.request.Request(url, headers={
        "x-rapidapi-key":  RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST,
    })
    try:
        with urllib.request.urlopen(req, context=_SSL_CONTEXT, timeout=15) as res:
            raw = res.read().decode("utf-8")
        return json.loads(raw)
    except Exception as e:
        print(f"  [RapidAPI] error on {endpoint}: {e}")
        return {}

def fetch_posts(subreddit: str, sort: str = "new", limit: int = FETCH_LIMIT) -> list:
    """Fetch posts from a subreddit. Returns list of post dicts.

    Response shape from reddit34 RapidAPI:
    {success: true, data: {cursor: ..., posts: [{data: {...}}, ...]}}
    """
    resp = rapidapi_get("getPostsBySubreddit", {
        "subreddit": subreddit,
        "sort": sort,
        "limit": str(limit),
    })
    # Navigate to the posts array
    if isinstance(resp, dict) and resp.get("success"):
        raw = resp.get("data", {}).get("posts", [])
    elif isinstance(resp, list):
        raw = resp
    else:
        return []

    posts = []
    for item in raw:
        # Each item is wrapped: {data: {id, title, selftext, score, ...}}
        if isinstance(item, dict) and "data" in item and isinstance(item["data"], dict):
            p = item["data"]
        elif isinstance(item, dict):
            p = item
        else:
            continue

        post_id = p.get("id", "")
        if not post_id:
            continue

        posts.append({
            "id":           post_id,
            "subreddit":    subreddit,
            "title":        p.get("title", ""),
            "selftext":     p.get("selftext") or p.get("body", ""),
            "score":        p.get("score", 0),
            "num_comments": p.get("num_comments", 0),
            "url":          p.get("url", ""),
            "permalink":    p.get("permalink", ""),
            "created":      p.get("created_utc", 0),
        })
    return posts

def score_relevance(post: dict) -> tuple[int, str, str]:
    """
    Score a post 0–10 for Calxo relevance.
    Returns (score, matched_calc_name, calc_url).
    """
    text = (post["title"] + " " + post["selftext"]).lower()
    score = 0
    best_calc_name = ""
    best_calc_url  = ""

    # Question signals
    for sig in QUESTION_SIGNALS:
        if sig in text:
            score += 1
            break  # one signal is enough

    # Calculator keyword matches (pick the best-matching calc)
    calc_hits = {}
    for kw, (calc_name, calc_url) in CALC_MAP.items():
        if kw in text:
            calc_hits[calc_url] = calc_hits.get(calc_url, 0) + 1
            if not best_calc_name:
                best_calc_name = calc_name
                best_calc_url  = calc_url

    if calc_hits:
        # Pick calc with most keyword hits
        best_calc_url = max(calc_hits, key=calc_hits.get)
        # Find its name
        for kw, (cn, cu) in CALC_MAP.items():
            if cu == best_calc_url:
                best_calc_name = cn
                break
        score += min(len(calc_hits) * 2, 6)  # up to 6 points for calc relevance

    # Boost for posts with decent engagement
    if post["num_comments"] >= 5:
        score += 1
    if post["score"] >= 10:
        score += 1

    # Penalise very short posts (probably memes/news)
    if len(text) < 80:
        score -= 2

    return max(score, 0), best_calc_name, best_calc_url


# ── GPT-4.1 answer generation ─────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a knowledgeable Indian personal finance person answering questions on Reddit's r/personalfinanceindia.

TONE RULES (very important):
- Write exactly like a real Reddit commenter who knows Indian finance well
- Casual, direct, slightly informal — not a corporate blog post
- Use Indian-English naturally: "lakhs", "crore", "bhai" occasionally, "₹" symbol
- Mix short punchy sentences with longer explanatory ones
- NO em dashes, NO "furthermore/moreover/additionally"
- NO "I hope this helps" or "feel free to ask" or "great question"
- NO markdown headers (##, **bold headers**) — just plain paragraphs
- You CAN use bold **like this** for specific numbers or key terms only
- Keep it 150–220 words — tight and useful

CALCULATOR MENTION RULES:
- Mention the Calxo calculator naturally at the end, once only
- DO NOT say "I work for" or "I made" or "shameless plug" — just "I use [calc name] at calxo.in for this"
- The link must feel like a genuine recommendation, not an ad
- Only mention it if it genuinely helps the OP's specific question

FORMAT:
- 2–3 paragraphs
- End with the calculator mention as the last sentence or second-to-last
- No sign-off line"""


def generate_answer(post: dict, calc_name: str, calc_url: str) -> str:
    """Generate a Reddit reply using GPT-4.1."""
    if not OPENAI_API_KEY:
        return ""

    client = OpenAI(api_key=OPENAI_API_KEY)

    user_prompt = f"""Reddit post from r/{post['subreddit']}:

Title: {post['title']}

Body:
{post['selftext'][:1200] if post['selftext'] else '(no body — title only)'}

Write a helpful Reddit reply. Naturally mention the {calc_name} at {calc_url} at the end if it genuinely helps them."""

    for attempt in range(3):
        try:
            resp = client.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": user_prompt},
                ],
                temperature=0.75,
                max_tokens=400,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            if "529" in str(e) or "overloaded" in str(e).lower():
                wait = 30 * (2 ** attempt)
                print(f"  [GPT] overloaded, retrying in {wait}s...")
                time.sleep(wait)
            else:
                print(f"  [GPT] error: {e}")
                return ""
    return ""


# ── PRAW posting ─────────────────────────────────────────────────────────────

def post_reply_praw(post_id: str, subreddit: str, reply_text: str) -> bool:
    """Post a reply via PRAW. Returns True on success."""
    if not PRAW_AVAILABLE:
        print("  [PRAW] praw not installed. Run: pip install praw")
        return False
    if not all([REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_PASSWORD]):
        print("  [PRAW] Missing REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET / REDDIT_PASSWORD in .env")
        return False
    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            password=REDDIT_PASSWORD,
            username=REDDIT_USERNAME,
            user_agent=f"CalxoBot/0.1 by {REDDIT_USERNAME}",
        )
        submission = reddit.submission(id=post_id)
        submission.reply(reply_text)
        return True
    except Exception as e:
        print(f"  [PRAW] error posting: {e}")
        return False


# ── Main pipeline ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Calxo Reddit Auto-Reply Bot")
    parser.add_argument("--dry-run", action="store_true", help="Fetch and score only, no GPT calls")
    parser.add_argument("--post",    action="store_true", help="Auto-post via PRAW (needs Reddit creds)")
    parser.add_argument("--subreddits", default=",".join(TARGET_SUBREDDITS),
                        help="Comma-separated subreddit list")
    args = parser.parse_args()

    subreddits = [s.strip() for s in args.subreddits.split(",")]

    # Load state
    queue    = load_json(QUEUE_FILE, [])
    replied  = load_json(REPLIED_FILE, {})   # post_id → {replied_at, subreddit, title}

    already_queued_ids = {item["id"] for item in queue}
    already_replied_ids = set(replied.keys())

    print(f"\n{'='*60}")
    print(f"Calxo Reddit Bot — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Mode: {'dry-run' if args.dry_run else ('auto-post' if args.post else 'queue')}")
    print(f"Subreddits: {', '.join(subreddits)}")
    print(f"Already replied: {len(already_replied_ids)} posts")
    print(f"{'='*60}\n")

    new_candidates = []

    # ── Step 1: Fetch and score ───────────────────────────────────────────────
    for sub in subreddits:
        print(f"Fetching r/{sub}...")
        posts = fetch_posts(sub, sort="new", limit=FETCH_LIMIT)
        # Also grab hot posts for more relevant content
        hot_posts = fetch_posts(sub, sort="hot", limit=15)
        all_posts = {p["id"]: p for p in posts + hot_posts if p["id"]}.values()

        sub_candidates = 0
        for post in all_posts:
            pid = post["id"]
            if not pid:
                continue
            if pid in already_replied_ids or pid in already_queued_ids:
                continue

            rel_score, calc_name, calc_url = score_relevance(post)
            if rel_score < MIN_SCORE:
                continue
            if not calc_name:
                continue

            post["relevance_score"] = rel_score
            post["calc_name"]       = calc_name
            post["calc_url"]        = calc_url
            new_candidates.append(post)
            sub_candidates += 1

        print(f"  → {len(posts)} new + {len(hot_posts)} hot fetched, {sub_candidates} relevant")
        time.sleep(1)  # be gentle with API

    # ── Step 2: Sort by relevance, cap at MAX_GENERATE ───────────────────────
    new_candidates.sort(key=lambda x: (-x["relevance_score"], -x.get("num_comments", 0)))
    to_process = new_candidates[:MAX_GENERATE]

    print(f"\nTop {len(to_process)} candidates for reply generation:")
    for i, p in enumerate(to_process, 1):
        print(f"  {i}. [{p['relevance_score']}] r/{p['subreddit']} — {p['title'][:70]}")
        print(f"     calc: {p['calc_name']} | comments: {p['num_comments']} | score: {p['score']}")

    if args.dry_run:
        print("\n[dry-run] Stopping here. No GPT calls made.")
        return

    if not to_process:
        print("\nNo new relevant posts found. Nothing to do.")
        return

    # ── Step 3: Generate answers ──────────────────────────────────────────────
    print(f"\nGenerating {len(to_process)} answers via GPT-4.1...")
    newly_queued = 0

    for post in to_process:
        print(f"\n  Generating for: {post['title'][:60]}...")
        answer = generate_answer(post, post["calc_name"], post["calc_url"])
        if not answer:
            print("  [skip] GPT returned empty answer")
            continue

        entry = {
            "id":             post["id"],
            "subreddit":      post["subreddit"],
            "title":          post["title"],
            "post_url":       f"https://www.reddit.com/r/{post['subreddit']}/comments/{post['id']}/",
            "calc_name":      post["calc_name"],
            "calc_url":       post["calc_url"],
            "relevance_score": post["relevance_score"],
            "generated_reply": answer,
            "generated_at":   datetime.now().isoformat(),
            "status":         "pending",
        }

        # ── Step 4: Post or queue ─────────────────────────────────────────────
        if args.post:
            print(f"  Posting via PRAW to r/{post['subreddit']}...")
            # Respect Reddit rate limits — wait between posts
            time.sleep(random.uniform(30, 60))
            success = post_reply_praw(post["id"], post["subreddit"], answer)
            if success:
                entry["status"] = "posted"
                entry["posted_at"] = datetime.now().isoformat()
                replied[post["id"]] = {
                    "replied_at": entry["posted_at"],
                    "subreddit":  post["subreddit"],
                    "title":      post["title"],
                    "calc_used":  post["calc_name"],
                }
                save_json(REPLIED_FILE, replied)
                print(f"  ✅ Posted!")
            else:
                entry["status"] = "failed"
                print(f"  ❌ Post failed — added to queue for manual review")
                queue.append(entry)
        else:
            queue.append(entry)
            newly_queued += 1
            print(f"  ✅ Added to queue")

        time.sleep(2)

    # ── Save queue ────────────────────────────────────────────────────────────
    save_json(QUEUE_FILE, queue)

    print(f"\n{'='*60}")
    print(f"Done.")
    if not args.post:
        print(f"  {newly_queued} new replies added to review queue: {QUEUE_FILE}")
        print(f"  Review the queue, then run with --post to post them,")
        print(f"  or manually copy the 'generated_reply' text to Reddit.")
    print(f"  Total in queue: {len(queue)}")
    print(f"  Total posted:   {len(replied)}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
