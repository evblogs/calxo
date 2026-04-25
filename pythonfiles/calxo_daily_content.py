#!/usr/bin/env python3
"""
Calxo.in — Daily Content Generator
Generates 2 blog posts per run using Claude API, commits to master,
and submits new URLs to Google Search Console Indexing API.

Run: python3 calxo_daily_content.py
GitHub Actions: runs daily at 3:00 AM UTC (8:30 AM IST)
"""

import json, os, subprocess, time, sys
from datetime import datetime
from pathlib import Path

QUEUE_FILE    = Path(__file__).parent / "calxo_content_queue.json"
BLOG_DIR      = Path(__file__).parent.parent / "content/english/blog"
BASE_URL      = "https://www.calxo.in"
POSTS_PER_RUN = int(os.environ.get("POSTS_PER_RUN", "2"))
GSC_CREDS     = os.environ.get(
    "GSC_CREDENTIALS_PATH",
    "/Users/luckychamp/gojournal/pythonfiles/gsc-key.json"
)

# ── Writing rules injected into every generation call ──────────────────────
SYSTEM_PROMPT = """You write blog posts for Calxo.in, a free Indian personal finance calculator site.
Every post must pass AI content detectors — write exactly like a knowledgeable human who typed this.

STRUCTURE RULES:
- Subheadings = nouns or short phrases, NEVER questions
  ✓ "The FOIR formula every bank uses"
  ✗ "What is FOIR and how does it work?"
- Numbered sections with full prose paragraphs underneath, not bullet lists
- Vary paragraph length: some 1 sentence, some 5-6 sentences

SENTENCE RHYTHM (most important):
- Mix lengths aggressively in every paragraph
  Short. Like this. Then follow with a longer sentence that has sub-clauses,
  a specific rupee amount or percentage, and doesn't end where you expect it to.
- Never write 4+ consecutive sentences of similar length
- Use passive voice naturally: "is capped at", "is calculated by", "was raised in Budget 2025"

WORD CHOICES:
- Repeat the main keyword/noun constantly — do NOT swap synonyms (humans repeat; AI varies)
- Drop technical terms (FOIR, CIBIL, TDS, LTCG, 87A) without defining every one
- Mix formal financial terms with casual Indian-English
- Include Hindi where natural: "SIP karo", "bhai", salary "hike"

TRANSITIONS:
- NEVER use: furthermore, moreover, additionally, it's worth noting, it is important to,
  in conclusion, to summarize, when it comes to, plays a crucial role, ensure that,
  it's crucial, it should be noted
- Start new paragraphs directly — no connector filler

HUMAN VOICE MARKERS:
- Add one specific scenario with a name, salary, city e.g. "My colleague Priya in Pune..."
  or "Someone earning ₹12 lakh in Bengaluru with a ₹25,000 monthly rent..."
- State opinions directly: "Don't. Seriously." / "Most people get this wrong."
- Occasionally repeat the same idea in slightly different words (humans do this naturally)
- Assume reader knowledge — don't define every term introduced

NEVER DO:
- Rhetorical questions as paragraph openers
- Parallel bullet lists where every item starts the same way
- "In this article, we will cover..." or "This guide will help you..."
- "plays a key role", "leverage", "delve", "tapestry", "in today's world", "game changer"
- Clean 3-part or 5-part structures where every section is the same length

FORMAT:
- Return complete Hugo markdown with YAML front matter — nothing else, no preamble
- 900–1200 words
- Use ₹ symbol with real Indian amounts
- Include one markdown table with actual data/rates
- Link to the provided calculator URL naturally mid-article (not just a forced CTA at the end)
- End on a direct practical note, not a motivational summary"""


# ── Queue helpers ───────────────────────────────────────────────────────────
def load_queue():
    with open(QUEUE_FILE, encoding="utf-8") as f:
        return json.load(f)

def save_queue(queue):
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2, ensure_ascii=False)

def get_pending(queue, n):
    return [item for item in queue if item["status"] == "pending"][:n]


# ── Content generation ──────────────────────────────────────────────────────
def generate_post(item, client):
    import anthropic
    today = datetime.now().strftime("%Y-%m-%d")

    tags_yaml = "\n".join(f"- {t}" for t in item["tags"])

    user_prompt = f"""Write a blog post for Calxo.in:

Topic: {item["title"]}
Target keyword: "{item["target_keyword"]}" — use naturally 4–6 times
Intent: informational — reader wants to understand how to calculate this
Calculator link: [{item["calculator_label"]}]({item["calculator_url"]}) — link once mid-article
Category: {item["category"]}
Date: {today}

Start with this exact front matter (fill in description yourself, ~150 chars, keyword-first):
---
title: "{item["title"]}"
description: "{item["description"]}"
date: {today}
lastmod: {today}
author: vignesh
categories:
- {item["category"]}
tags:
{tags_yaml}
---

Write the post now. No preamble — start the content immediately after the front matter closing ---"""

    msg = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}]
    )
    return msg.content[0].text.strip()


# ── File writing ────────────────────────────────────────────────────────────
def write_post(item, content):
    BLOG_DIR.mkdir(parents=True, exist_ok=True)
    filepath = BLOG_DIR / f"{item['id']}.md"
    filepath.write_text(content, encoding="utf-8")
    return filepath


# ── GSC indexing ────────────────────────────────────────────────────────────
def submit_to_gsc(url):
    try:
        from google.oauth2 import service_account
        import google.auth.transport.requests as google_requests

        creds = service_account.Credentials.from_service_account_file(
            GSC_CREDS, scopes=["https://www.googleapis.com/auth/indexing"]
        )
        session  = google_requests.AuthorizedSession(creds)
        endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"
        resp     = session.post(endpoint, json={"url": url, "type": "URL_UPDATED"})
        return resp.status_code == 200
    except Exception as e:
        print(f"     GSC error: {e}")
        return False


# ── Git commit + push ───────────────────────────────────────────────────────
def git_commit_push(filepaths, message):
    repo_root = Path(__file__).parent.parent

    for fp in filepaths:
        subprocess.run(["git", "add", str(fp)], cwd=repo_root, check=True)
    subprocess.run(["git", "add", str(QUEUE_FILE)], cwd=repo_root, check=True)

    subprocess.run(["git", "commit", "-m", message], cwd=repo_root, check=True)

    # Pull before push to avoid conflicts with other commits
    subprocess.run(
        ["git", "pull", "--rebase", "origin", "master"],
        cwd=repo_root, check=True
    )
    subprocess.run(["git", "push", "origin", "master"], cwd=repo_root, check=True)


# ── Main ────────────────────────────────────────────────────────────────────
def main():
    print("=" * 62)
    print("  Calxo Daily Content Generator")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}")
    print("=" * 62)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("\n  ERROR: ANTHROPIC_API_KEY not set.")
        sys.exit(1)

    import anthropic
    client = anthropic.Anthropic(api_key=api_key)

    queue   = load_queue()
    items   = get_pending(queue, POSTS_PER_RUN)

    if not items:
        print("\n  Queue empty — no pending posts. Add more items to calxo_content_queue.json")
        return

    print(f"\n  Generating {len(items)} post(s)...\n")

    written  = []
    new_urls = []

    for item in items:
        print(f"  → {item['title']}")
        try:
            content  = generate_post(item, client)
            filepath = write_post(item, content)

            # Mark as done in queue
            for q in queue:
                if q["id"] == item["id"]:
                    q["status"]         = "done"
                    q["published_date"] = datetime.now().strftime("%Y-%m-%d")

            written.append(filepath)
            new_urls.append(f"{BASE_URL}/blog/{item['id']}/")
            print(f"     ✓  {filepath.name}")

        except Exception as e:
            print(f"     ✗  Failed — {e}")

        time.sleep(2)  # avoid API rate limits

    if not written:
        print("\n  Nothing written. Exiting.")
        return

    # Save updated queue
    save_queue(queue)

    # Commit and push
    titles = " + ".join(
        next(q["title"] for q in queue if q["id"] == fp.stem)
        for fp in written
    )
    commit_msg = (
        f"[auto] Add blog posts: {titles[:70]}\n\n"
        f"Generated by calxo_daily_content.py — {datetime.now().strftime('%Y-%m-%d')}\n\n"
        f"Co-Authored-By: Claude <noreply@anthropic.com>"
    )

    print(f"\n  Committing and pushing {len(written)} file(s)...")
    try:
        git_commit_push(written, commit_msg)
        print("  ✓  Pushed to master → Netlify deploying")
    except subprocess.CalledProcessError as e:
        print(f"  ✗  Git error: {e}")
        return

    # Submit new URLs to GSC
    print(f"\n  Submitting {len(new_urls)} URL(s) to GSC Indexing API...")
    for url in new_urls:
        ok = submit_to_gsc(url)
        print(f"  {'✓' if ok else '✗'}  {url}")
        time.sleep(0.5)

    print(f"\n  Done — {len(written)} post(s) published and indexed.")
    print(f"  Queue remaining: {sum(1 for q in queue if q['status'] == 'pending')} pending")


if __name__ == "__main__":
    main()
