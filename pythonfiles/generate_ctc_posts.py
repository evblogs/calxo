#!/usr/bin/env python3
"""
Generate CTC take-home salary posts for Calxo.in
Creates posts for 10L, 12L, 20L, 25L CTC — clusters with existing 15L post.
"""

import os, subprocess, time
from pathlib import Path
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv("/Users/luckychamp/gojournal/pythonfiles/.env")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BLOG_DIR = Path("/Users/luckychamp/calxo/content/english/blog")

SYSTEM_PROMPT = """You write blog posts for Calxo.in, a free Indian personal finance calculator site.
Write exactly like a knowledgeable human who typed this. Every post must feel like a real person wrote it.

STRUCTURE RULES:
- Subheadings = nouns or short phrases, NEVER questions
- Numbered sections with full prose paragraphs underneath, not bullet lists
- Vary paragraph length: some 1 sentence, some 5-6 sentences

SENTENCE RHYTHM:
- Mix lengths aggressively. Short. Like this. Then follow with a longer sentence that has sub-clauses,
  a specific rupee amount or percentage, and doesn't end where you expect it to.
- Never write 4+ consecutive sentences of similar length
- Use passive voice naturally: "is capped at", "is calculated by", "was raised in Budget 2025"

WORD CHOICES:
- Repeat the main keyword/noun constantly — do NOT swap synonyms
- Drop technical terms (FOIR, TDS, 87A, EPF) without defining every one
- Mix formal financial terms with casual Indian-English
- Include Hindi where natural: "SIP karo", "bhai", salary "hike"

TRANSITIONS — NEVER USE:
furthermore, moreover, additionally, it's worth noting, it is important to,
in conclusion, to summarize, when it comes to, plays a crucial role, ensure that

HUMAN VOICE MARKERS:
- Add one specific scenario with a name, salary, city (e.g. "My colleague Rahul in Hyderabad...")
- State opinions directly: "Don't. Seriously." / "Most people get this wrong."
- Assume reader knowledge — don't define every term introduced

CRITICAL: Never use em dashes (—). Use commas or new sentences instead."""

CTC_CONFIGS = [
    {
        "ctc_lakh": 10,
        "ctc_num": "10,00,000",
        "basic_pct": 50,
        "basic": "5,00,000",
        "hra": "2,00,000",
        "special_allowance": "2,16,527",
        "employer_pf": "60,000",
        "gratuity_provision": "24,050",
        "annual_gross": "9,15,950",
        "employee_pf": "60,000",
        "prof_tax": "2,400",
        "income_tax": 0,
        "monthly_takehome": "71,300",
        "annual_takehome": "8,55,550",
        "takehome_pct": "85.6",
        "regime": "new",
        "state": "Karnataka",
        "city": "Bengaluru",
        "note": "Below ₹12.75L taxable, section 87A rebate zeroes out the tax entirely",
        "slug": "10-lakh-ctc-take-home-salary",
        "title": "10 Lakh CTC Take-Home Salary 2025-26: ₹71,300/Month In-Hand Breakdown",
        "description": "₹10L CTC = ₹71,300/month in-hand under new tax regime. Full breakdown: employer PF ₹60K, zero income tax (87A rebate), professional tax. Old vs new regime compared.",
        "other_ctcs": [
            ("12 lakh CTC", "/blog/12-lakh-ctc-take-home-salary/"),
            ("15 lakh CTC", "/blog/what-15-lakh-ctc-actually-means/"),
            ("20 lakh CTC", "/blog/20-lakh-ctc-take-home-salary/"),
            ("25 lakh CTC", "/blog/25-lakh-ctc-take-home-salary/"),
        ],
        "tax_note": "Zero income tax. The 87A rebate (₹60,000) fully covers the slab tax because taxable income stays under ₹12 lakh. This is one of the sweetest spots in the new regime.",
    },
    {
        "ctc_lakh": 12,
        "ctc_num": "12,00,000",
        "basic_pct": 50,
        "basic": "6,00,000",
        "hra": "2,40,000",
        "special_allowance": "2,59,830",
        "employer_pf": "72,000",
        "gratuity_provision": "28,860",
        "annual_gross": "10,99,140",
        "employee_pf": "72,000",
        "prof_tax": "2,400",
        "income_tax": 0,
        "monthly_takehome": "85,395",
        "annual_takehome": "10,24,740",
        "takehome_pct": "85.4",
        "regime": "new",
        "state": "Karnataka",
        "city": "Pune",
        "note": "Taxable income stays just under ₹12L after standard deduction, so 87A rebate covers the full slab tax",
        "slug": "12-lakh-ctc-take-home-salary",
        "title": "12 Lakh CTC Take-Home Salary 2025-26: ₹85,395/Month In-Hand Breakdown",
        "description": "₹12L CTC = ₹85,395/month in-hand under new tax regime. Zero income tax if taxable stays under ₹12L. Full breakdown with employer PF, gratuity provision, professional tax.",
        "other_ctcs": [
            ("10 lakh CTC", "/blog/10-lakh-ctc-take-home-salary/"),
            ("15 lakh CTC", "/blog/what-15-lakh-ctc-actually-means/"),
            ("20 lakh CTC", "/blog/20-lakh-ctc-take-home-salary/"),
            ("25 lakh CTC", "/blog/25-lakh-ctc-take-home-salary/"),
        ],
        "tax_note": "Zero income tax. ₹12L CTC sits right at the boundary of the 87A rebate. After standard deduction of ₹75,000, taxable income is ₹10,24,140, well under ₹12L. The full slab tax is covered by the ₹60,000 rebate.",
    },
    {
        "ctc_lakh": 20,
        "ctc_num": "20,00,000",
        "basic_pct": 50,
        "basic": "10,00,000",
        "hra": "4,00,000",
        "special_allowance": "3,80,700",
        "employer_pf": "1,20,000",
        "gratuity_provision": "48,100",
        "annual_gross": "18,31,900",
        "employee_pf": "1,20,000",
        "prof_tax": "2,400",
        "income_tax": "1,79,400",
        "monthly_takehome": "1,27,508",
        "annual_takehome": "15,30,100",
        "takehome_pct": "76.5",
        "regime": "new",
        "state": "Karnataka",
        "city": "Bengaluru",
        "note": "Taxable crosses ₹12L so 87A rebate stops applying — this is where the tax bite really starts",
        "slug": "20-lakh-ctc-take-home-salary",
        "title": "20 Lakh CTC Take-Home Salary 2025-26: ₹1,27,508/Month In-Hand Breakdown",
        "description": "₹20L CTC = ₹1,27,508/month in-hand under new tax regime. Tax crosses ₹12L threshold so 87A rebate stops. Full breakdown: employer PF ₹1.2L, income tax ₹1.79L.",
        "other_ctcs": [
            ("10 lakh CTC", "/blog/10-lakh-ctc-take-home-salary/"),
            ("12 lakh CTC", "/blog/12-lakh-ctc-take-home-salary/"),
            ("15 lakh CTC", "/blog/what-15-lakh-ctc-actually-means/"),
            ("25 lakh CTC", "/blog/25-lakh-ctc-take-home-salary/"),
        ],
        "tax_note": "Income tax of ₹1,79,400 under new regime. Taxable income after standard deduction is ₹17,56,900. Slab tax: ₹0 (up to ₹4L) + ₹20,000 (₹4-8L at 5%) + ₹40,000 (₹8-12L at 10%) + ₹75,000 (₹12-16L at 15%) + ₹35,000 (₹16-17.57L at 20%) = ₹1,70,000 + 4% cess ₹6,800 = ₹1,76,800. Marginal relief doesn't apply here.",
    },
    {
        "ctc_lakh": 25,
        "ctc_num": "25,00,000",
        "basic_pct": 50,
        "basic": "12,50,000",
        "hra": "5,00,000",
        "special_allowance": "4,26,463",
        "employer_pf": "1,50,000",
        "gratuity_provision": "60,125",
        "annual_gross": "23,29,875",
        "employee_pf": "1,50,000",
        "prof_tax": "2,400",
        "income_tax": "3,51,000",
        "monthly_takehome": "1,52,205",
        "annual_takehome": "18,26,475",
        "takehome_pct": "73.1",
        "regime": "new",
        "state": "Karnataka",
        "city": "Bengaluru",
        "note": "At 25L CTC, you're firmly in the 20% slab. Take-home drops to ~73% of CTC.",
        "slug": "25-lakh-ctc-take-home-salary",
        "title": "25 Lakh CTC Take-Home Salary 2025-26: ₹1,52,205/Month In-Hand Breakdown",
        "description": "₹25L CTC = ₹1,52,205/month in-hand under new tax regime. Income tax ₹3.51L, employer PF ₹1.5L. Full line-by-line breakdown for the 20% tax slab earner.",
        "other_ctcs": [
            ("10 lakh CTC", "/blog/10-lakh-ctc-take-home-salary/"),
            ("12 lakh CTC", "/blog/12-lakh-ctc-take-home-salary/"),
            ("15 lakh CTC", "/blog/what-15-lakh-ctc-actually-means/"),
            ("20 lakh CTC", "/blog/20-lakh-ctc-take-home-salary/"),
        ],
        "tax_note": "Income tax of ₹3,51,000 under new regime. Taxable after standard deduction is ₹22,54,875. Slab tax computes to ₹3,37,500 + 4% cess ₹13,500 = ₹3,51,000. You're now fully in the 20% slab for income between ₹16L and ₹20L, and 25% slab for the chunk above ₹20L.",
    },
]

USER_TEMPLATE = """Write a comprehensive blog post for Calxo.in about {ctc_lakh} lakh CTC take-home salary in India for FY 2025-26.

KEY NUMBERS (use exactly these — pre-calculated):
- CTC: ₹{ctc_num}
- Basic (50% of CTC): ₹{basic}
- HRA (40% of basic): ₹{hra}
- Special Allowance: ₹{special_allowance}
- Employer PF (12% of basic): ₹{employer_pf}
- Gratuity provision (4.81% of basic): ₹{gratuity_provision}
- Annual Gross (what payroll pays): ₹{annual_gross}
- Employee PF: ₹{employee_pf}
- Professional tax ({state}): ₹{prof_tax}
- Income tax (new regime): ₹{income_tax}
- Annual take-home: ₹{annual_takehome}
- Monthly take-home: ₹{monthly_takehome}
- Take-home as % of CTC: {takehome_pct}%

TAX CONTEXT: {tax_note}

INTERNAL LINKS TO INCLUDE (use these exact markdown links):
- Take-home calculator: [take-home salary calculator](/salary/takehome-calculator/)
- Income tax calculator: [income tax calculator](/tax/income-tax-calculator/)
- HRA calculator: [HRA exemption calculator](/salary/hra-calculator/)
- Old vs new regime: [old vs new tax regime article](/blog/old-vs-new-tax-regime-fy-2025-26/)
- EMI calculator: [EMI calculator](/loan/emi-calculator/)
- SIP calculator: [SIP calculator](/investment/sip-calculator/)

CROSS-LINKS TO OTHER CTC POSTS (link these naturally in the content):
{cross_links}

REQUIRED SECTIONS:
1. Opening anecdote (friend/colleague in {city} getting first salary, confused by gap)
2. "The five layers between offer letter and bank account" (explain each deduction layer)
3. "What CTC actually contains" (basic, HRA, special allowance, employer PF, gratuity)
4. Worked example table (CTC → take-home step by step, use exact numbers above)
5. "How the regime choice changes take-home" (table comparing new regime vs old regime scenarios)
6. "Five things HR won't tell you" (variable pay, EPF taxability, gratuity vesting, etc.)
7. "How to actually increase take-home" (employer NPS, food coupons, flexi-benefits)
8. Take-home % at different CTCs (mini table with 6L, 10L, 12L, 15L, 20L, 25L, 50L, 1Cr)
9. FAQ section (5 questions, no question-format headings — use statement headings)
10. "What to actually do with this" (practical closing, links to calculators)

Length: 2,000-2,500 words. Output ONLY the markdown body — no frontmatter, no title heading at top.
Start directly with the opening anecdote paragraph."""

def generate_post(config):
    cross_links = "\n".join([f"- {label}: [{label}]({url})" for label, url in config["other_ctcs"]])

    prompt = USER_TEMPLATE.format(
        ctc_lakh=config["ctc_lakh"],
        ctc_num=config["ctc_num"],
        basic_pct=config["basic_pct"],
        basic=config["basic"],
        hra=config["hra"],
        special_allowance=config["special_allowance"],
        employer_pf=config["employer_pf"],
        gratuity_provision=config["gratuity_provision"],
        annual_gross=config["annual_gross"],
        employee_pf=config["employee_pf"],
        prof_tax=config["prof_tax"],
        income_tax=config["income_tax"],
        annual_takehome=config["annual_takehome"],
        monthly_takehome=config["monthly_takehome"],
        takehome_pct=config["takehome_pct"],
        tax_note=config["tax_note"],
        state=config["state"],
        city=config["city"],
        cross_links=cross_links,
    )

    resp = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=4000,
    )
    return resp.choices[0].message.content.strip()


def write_post(config, body):
    today = datetime.now().strftime("%Y-%m-%d")

    # Build related_calcs
    related = [
        '  - { label: "Take-Home Salary Calculator", url: "/salary/takehome-calculator/" }',
        '  - { label: "Income Tax Calculator (FY 2025-26)", url: "/tax/income-tax-calculator/" }',
        '  - { label: "HRA Exemption Calculator", url: "/salary/hra-calculator/" }',
        '  - { label: "EPF Calculator", url: "/salary/epf-calculator/" }',
        '  - { label: "Gratuity Calculator", url: "/salary/gratuity-calculator/" }',
    ]

    cross_link_lines = "\n".join([
        f'  - {{ label: "{label}", url: "{url}" }}' for label, url in config["other_ctcs"]
    ])

    frontmatter = f"""---
title: "{config['title']}"
description: "{config['description']}"
date: {today}
lastmod: {today}
author: vignesh
tags: ["Salary", "Tax planning", "FY 2025-26", "CTC"]
categories:
- Salary
related_calcs:
{chr(10).join(related)}
cross_links:
{cross_link_lines}
---

"""

    filepath = BLOG_DIR / f"{config['slug']}.md"
    filepath.write_text(frontmatter + body)
    print(f"  Written: {filepath.name}")
    return filepath


def submit_to_gsc(url):
    from google.oauth2 import service_account
    from google.auth.transport.requests import Request
    import requests as req
    creds = service_account.Credentials.from_service_account_file(
        "/Users/luckychamp/gojournal/pythonfiles/gsc-key.json",
        scopes=["https://www.googleapis.com/auth/indexing"]
    )
    creds.refresh(Request())
    r = req.post(
        "https://indexing.googleapis.com/v3/urlNotifications:publish",
        headers={"Authorization": f"Bearer {creds.token}"},
        json={"url": url, "type": "URL_UPDATED"}
    )
    return r.status_code


if __name__ == "__main__":
    print(f"Generating {len(CTC_CONFIGS)} CTC posts...\n")

    for config in CTC_CONFIGS:
        slug = config["slug"]
        filepath = BLOG_DIR / f"{slug}.md"

        if filepath.exists():
            print(f"  Skipping {slug} (already exists)")
            continue

        print(f"  Generating: {config['ctc_lakh']}L CTC post...")
        body = generate_post(config)
        write_post(config, body)
        time.sleep(2)

    print("\nCommitting to git...")
    result = subprocess.run(
        ["git", "add", "content/english/blog/"],
        cwd="/Users/luckychamp/calxo", capture_output=True, text=True
    )

    result = subprocess.run(
        ["git", "commit", "-m", "Add CTC salary cluster: 10L, 12L, 20L, 25L take-home posts"],
        cwd="/Users/luckychamp/calxo", capture_output=True, text=True
    )
    print(result.stdout or result.stderr)

    result = subprocess.run(
        ["git", "push", "origin", "master"],
        cwd="/Users/luckychamp/calxo", capture_output=True, text=True
    )
    print(result.stdout or result.stderr)

    print("\nSubmitting URLs to GSC Indexing API...")
    base = "https://www.calxo.in"
    for config in CTC_CONFIGS:
        url = f"{base}/blog/{config['slug']}/"
        status = submit_to_gsc(url)
        print(f"  {url} → {status}")

    print("\nDone.")
