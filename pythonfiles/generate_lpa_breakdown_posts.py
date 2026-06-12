#!/usr/bin/env python3
"""
Generate the LPA in-hand breakdown blog posts that were missing from Calxo's
salary cluster (the gaps vs the Jupiter salary-calculator LPA table).

Every rupee figure is computed with the SAME math as
layouts/shortcodes/takehome-calculator.html (new regime, 50% basic,
HRA 50% of basic, statutory 12% EPF, Karnataka professional tax, FY 2025-26),
so the numbers match the on-site widget exactly.

Self-contained: no network, no API key. Run from repo root.
"""

import os
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BLOG_DIR = REPO / "content" / "english" / "blog"
TODAY = "2026-06-11"

# ─────────────────────── Indian number formatting ───────────────────────
def fmt(n):
    n = int(round(n))
    neg = n < 0
    s = str(abs(n))
    if len(s) > 3:
        last3 = s[-3:]
        rest = s[:-3]
        parts = []
        while len(rest) > 2:
            parts.insert(0, rest[-2:]); rest = rest[:-2]
        if rest:
            parts.insert(0, rest)
        s = ",".join(parts) + "," + last3
    return ("-" if neg else "") + s

def rupee(n):
    return "₹" + fmt(n)

# ─────────────────────── widget math (verified) ───────────────────────
def compute(CTC, reg="new", basicPct=0.50, hraPct=0.50, pt=2400):
    Basic = CTC * basicPct
    HRA = Basic * hraPct
    employerPF = Basic * 0.12
    employeePF = employerPF
    gratuity = Basic * 0.0481
    Special = CTC - Basic - HRA - employerPF - gratuity
    if Special < 0:
        Special = 0
    annualGross = Basic + HRA + Special
    stdDed = 75000 if reg == "new" else 50000
    taxable = max(0, annualGross - stdDed)
    if reg == "new":
        slabs = [(400000, 0), (800000, .05), (1200000, .10), (1600000, .15),
                 (2000000, .20), (2400000, .25), (float("inf"), .30)]
    else:
        slabs = [(250000, 0), (500000, .05), (1000000, .20), (float("inf"), .30)]
    tax = 0; prev = 0; breakup = []
    for top, rate in slabs:
        if taxable <= prev:
            break
        amt = (taxable if taxable <= top else top) - prev
        if amt > 0 and rate > 0:
            breakup.append((rate, amt * rate))
        tax += amt * rate; prev = top
        if taxable <= top:
            break
    taxBefore = max(0, tax)
    rebate = 0
    if reg == "new" and taxable <= 1200000:
        rebate = min(taxBefore, 60000)
    if reg == "old" and taxable <= 500000:
        rebate = min(taxBefore, 12500)
    taxAfter = taxBefore - rebate
    if reg == "new" and taxable > 1200000 and rebate == 0:
        excess = taxable - 1200000
        if taxAfter > excess:
            taxAfter = excess
    rate = 0
    if taxable > 50000000:
        rate = 0.25 if reg == "new" else 0.37
    elif taxable > 20000000:
        rate = 0.25
    elif taxable > 10000000:
        rate = 0.15
    elif taxable > 5000000:
        rate = 0.10
    surcharge = taxAfter * rate
    cess = (taxAfter + surcharge) * 0.04
    incomeTax = taxAfter + surcharge + cess
    annualTake = annualGross - employeePF - pt - incomeTax
    return dict(CTC=CTC, Basic=Basic, HRA=HRA, Special=Special,
                employerPF=employerPF, gratuity=gratuity, gross=annualGross,
                employeePF=employeePF, pt=pt, taxable=taxable,
                taxBefore=taxBefore, rebate=rebate, surcharge=surcharge,
                cess=cess, tax=incomeTax, take=annualTake,
                monthly=annualTake / 12, breakup=breakup)

# ─────────────────────── value helpers ───────────────────────
def lpa_label(lpa):
    return str(int(lpa)) if float(lpa).is_integer() else str(lpa).rstrip("0").rstrip(".")

def lpa_lakh_word(lpa):
    return lpa_label(lpa) + " Lakh"

def slug_for(lpa):
    if lpa == 100:
        return "1-crore-ctc-take-home-salary"
    s = lpa_label(lpa).replace(".", "-")
    return f"{s}-lakh-ctc-take-home-salary"

def short_label(lpa):
    if lpa == 100:
        return "₹1Cr"
    return "₹" + lpa_label(lpa) + "L"

def slab_sentence(breakup):
    names = {0.05: "5%", 0.10: "10%", 0.15: "15%", 0.20: "20%",
             0.25: "25%", 0.30: "30%"}
    parts = [f"{rupee(t)} in the {names[r]} slab" for r, t in breakup]
    return ", ".join(parts)

# ─────────────────────── existing pages (for the ladder) ───────────────────────
EXISTING = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
            20, 25, 30, 35, 40, 45, 50, 60, 75, 100]

# new pages to build (missing from Jupiter LPA table)
MISSING = [1, 1.5, 2, 2.3, 3.8, 3.9, 4.5, 5.5, 8.5, 9.2, 9.5, 9.6, 9.8,
           11.5, 13.5, 16.5, 17.5, 19, 21, 22, 22.5, 24, 26, 28, 34, 36,
           37, 85, 90]

ALL_VALUES = sorted(set(EXISTING) | set(MISSING))

def ctc_of(lpa):
    return int(round((1_00_00_000 if lpa == 100 else lpa * 1_00_000)))

def band(lpa):
    if lpa <= 2.3:
        return "micro"
    if lpa <= 5.5:
        return "entry"
    if lpa <= 13.5:
        return "midzero"
    if lpa <= 28:
        return "taxed"
    if lpa < 50:
        return "high"
    return "surcharge"

# scenario pools (indexed for per-page variety)
NAMES = ["Rohit", "Sneha", "Karthik", "Ananya", "Vikram", "Priya", "Arjun",
         "Meera", "Faisal", "Divya", "Naveen", "Ritika", "Sandeep", "Pooja",
         "Aakash", "Nisha", "Manish", "Shruti", "Imran", "Kavya", "Rahul",
         "Deepa", "Varun", "Tanvi", "Harish", "Lakshmi", "Gaurav", "Swati",
         "Aditya"]
CITIES = ["Pune", "Bengaluru", "Hyderabad", "Chennai", "Gurugram", "Noida",
          "Indore", "Jaipur", "Kochi", "Ahmedabad", "Coimbatore", "Nagpur",
          "Mysuru", "Bhubaneswar", "Chandigarh", "Vadodara", "Lucknow",
          "Visakhapatnam", "Surat", "Bhopal", "Kolkata", "Mumbai", "Delhi",
          "Faridabad", "Rajkot", "Madurai", "Ranchi", "Guwahati", "Patna"]
ROLES = {
    "micro": ["a customer-support trainee", "a field sales executive",
              "a data-entry associate", "a retail store associate"],
    "entry": ["a junior associate", "a graduate trainee", "a support engineer",
              "an operations executive"],
    "midzero": ["a software engineer", "a business analyst", "a QA engineer",
                "a marketing associate", "an accounts executive"],
    "taxed": ["a senior engineer", "a product manager", "a team lead",
              "a senior analyst", "a project manager"],
    "high": ["an engineering manager", "a senior product manager",
             "a regional sales head"],
    "surcharge": ["a director of engineering", "a VP of sales",
                  "a senior principal engineer"],
}

# ─────────────────────── ladder table ───────────────────────
def ladder(lpa, window=4):
    idx = ALL_VALUES.index(lpa)
    lo = max(0, idx - window)
    hi = min(len(ALL_VALUES), idx + window + 1)
    rows = ["| CTC | Monthly take-home | Income tax / year |", "|---|---|---|"]
    for v in ALL_VALUES[lo:hi]:
        r = compute(ctc_of(v))
        url = f"/blog/{slug_for(v)}/"
        lbl = short_label(v)
        taxtxt = "Zero" if r["tax"] < 1 else rupee(r["tax"])
        cell = f"[{lbl}]({url})"
        mono = rupee(r["monthly"])
        if v == lpa:
            rows.append(f"| **{cell}** | **{mono}** | **{taxtxt}** |")
        else:
            rows.append(f"| {cell} | {mono} | {taxtxt} |")
    return "\n".join(rows)

# ─────────────────────── body builders per band ───────────────────────
def component_table(r):
    return "\n".join([
        "| Component | Annual | Monthly |",
        "|---|---|---|",
        f"| Basic salary | {rupee(r['Basic'])} | {rupee(r['Basic']/12)} |",
        f"| HRA (50% of basic) | {rupee(r['HRA'])} | {rupee(r['HRA']/12)} |",
        f"| Special allowance | {rupee(r['Special'])} | {rupee(r['Special']/12)} |",
        f"| Employer PF (12% of basic) | {rupee(r['employerPF'])} | {rupee(r['employerPF']/12)} |",
        f"| Gratuity provision (4.81%) | {rupee(r['gratuity'])} | {rupee(r['gratuity']/12)} |",
        f"| **Total CTC** | **{rupee(r['CTC'])}** | **{rupee(r['CTC']/12)}** |",
    ])

def takehome_table(r, taxlabel):
    return "\n".join([
        "| Item | Annual | Monthly |",
        "|---|---|---|",
        f"| Gross salary (excl. employer PF + gratuity) | {rupee(r['gross'])} | {rupee(r['gross']/12)} |",
        f"| Less: Employee PF | {rupee(r['employeePF'])} | {rupee(r['employeePF']/12)} |",
        f"| Less: Professional tax (Karnataka) | {rupee(r['pt'])} | {rupee(r['pt']/12)} |",
        f"| Less: Income tax | {taxlabel} | {rupee(r['tax']/12) if r['tax']>=1 else '₹0'} |",
        f"| **In-hand** | **{rupee(r['take'])}** | **{rupee(r['monthly'])}** |",
    ])

def post_body(lpa, i):
    r = compute(ctc_of(lpa))
    ro = compute(ctc_of(lpa), "old")
    b = band(lpa)
    name = NAMES[i % len(NAMES)]
    city = CITIES[i % len(CITIES)]
    role = ROLES[b][i % len(ROLES[b])]
    L = lpa_label(lpa)
    pct = r["take"] / r["CTC"] * 100
    monthly = rupee(r["monthly"])
    grossM = rupee(r["gross"] / 12)
    ctc_str = ctc_of(lpa)

    out = []

    # ── opening anecdote ──
    if b == "micro":
        out.append(
            f"{name} took {role} job in {city} on ₹{L} lakh a year. The offer "
            f"letter showed {rupee(ctc_str/12)} a month, so {name} planned around "
            f"that figure. The first salary credit was {monthly}. None of the gap is "
            f"income tax, because at ₹{L} lakh you pay zero. It is provident fund and a "
            f"little professional tax, plus the slice of CTC that an offer letter counts "
            f"but a bank account never receives.")
    elif b == "entry":
        out.append(
            f"{name} signed a ₹{L} lakh offer as {role} in {city}. The letter said "
            f"{rupee(ctc_str/12)} a month. The bank credit was {monthly}. At ₹{L} lakh "
            f"there is still no income tax to blame, the whole gap is your own EPF, a "
            f"₹{fmt(r['pt'])} professional tax, and the employer PF plus gratuity that "
            f"live inside CTC and never reach you. In-hand works out to about "
            f"{pct:.0f}% of CTC, close to the best ratio you will ever see.")
    elif b == "midzero":
        gap = ro["monthly"] and (r["monthly"] - ro["monthly"])
        out.append(
            f"{name} moved to a ₹{L} lakh role as {role} in {city} and had to pick a "
            f"tax regime on the joining form. New regime: {monthly} a month, zero income "
            f"tax. Old regime with no real deductions: {rupee(ro['monthly'])} a month, "
            f"because ₹{L} lakh gets taxed {rupee(ro['tax'])} there. Same CTC, "
            f"{rupee(gap)} a month difference, decided by one checkbox. At ₹{L} lakh the "
            f"new regime wins by a distance.")
    elif b == "taxed":
        out.append(
            f"{name} negotiated a ₹{L} lakh package as {role} in {city}, up from a "
            f"lower band, and expected the raise to land in full. It did not. Monthly "
            f"in-hand is {monthly}, which is about {pct:.0f}% of CTC. The 87A rebate is "
            f"gone at this level, so income tax of {rupee(r['tax'])} a year is now a "
            f"real line on the payslip, not a number the rebate quietly erases.")
    elif b == "high":
        out.append(
            f"{name} crossed into a ₹{L} lakh package as {role} in {city}. The headline "
            f"sounds like {rupee(ctc_str/12)} a month. The account sees {monthly}. "
            f"Income tax alone is {rupee(r['tax'])} a year here, the 30% slab is in play "
            f"on the top slice of income, and take-home settles near {pct:.0f}% of CTC. "
            f"This is the band where structuring the CTC actually starts paying back.")
    else:  # surcharge
        out.append(
            f"{name} signed a ₹{L} lakh package as {role} in {city}. At this level a new "
            f"line shows up that nobody at lower salaries deals with: surcharge. Taxable "
            f"income crosses ₹50 lakh, so a 10% surcharge stacks on the income tax "
            f"itself. Monthly in-hand is {monthly}, roughly {pct:.0f}% of CTC, with "
            f"{rupee(r['tax'])} a year going to tax including that surcharge.")

    out.append(f'\n{{{{< takehome-calculator ctc="{ctc_str}" >}}}}\n')

    taxsub = ("zero income tax" if r["tax"] < 1
              else f"income tax {rupee(r['tax'])}/year")
    out.append(
        "{{< infographic-stat\n"
        f'  number="{monthly}"\n'
        f'  label="Monthly in-hand from ₹{L}L CTC (new regime, Karnataka, 50% basic)"\n'
        f'  sub="FY 2025-26, {taxsub}" >}}}}\n')

    out.append(f"## What ₹{L} lakh CTC actually contains\n")
    out.append(f"Standard 50% basic structure at ₹{L}L:\n")
    out.append(component_table(r) + "\n")
    out.append(
        f"Employer PF plus gratuity comes to {rupee(r['employerPF']+r['gratuity'])}. "
        f"That money sits inside the ₹{L} lakh CTC and never lands in your salary "
        f"account. Your gross salary, the part payroll actually pays, is "
        f"{rupee(r['gross'])} a year.\n")

    out.append("## Take-home calculation (new regime)\n")
    taxlabel = "₹0" if r["tax"] < 1 else rupee(r["tax"])
    out.append(takehome_table(r, taxlabel) + "\n")

    # tax working
    if r["tax"] < 1 and not r["breakup"]:
        out.append(
            f"Taxable income after the ₹75,000 standard deduction is "
            f"{rupee(r['taxable'])}, below the ₹4 lakh first slab of the new regime. So "
            f"income tax is zero. The only money leaving your gross is your own PF of "
            f"{rupee(r['employeePF'])} and ₹{fmt(r['pt'])} of professional tax.\n")
    elif r["tax"] < 1 and r["breakup"]:
        out.append(
            f"Tax working: gross {rupee(r['gross'])} minus the ₹75,000 standard "
            f"deduction leaves taxable income of {rupee(r['taxable'])}. The slab tax "
            f"adds up to {rupee(r['taxBefore'])} ({slab_sentence(r['breakup'])}), but "
            f"taxable income stays under the ₹12 lakh line, so the section 87A rebate of "
            f"up to ₹60,000 wipes the whole amount. Tax payable: zero.\n")
    else:
        out.append(
            f"Tax working: gross {rupee(r['gross'])} minus the ₹75,000 standard "
            f"deduction leaves taxable income of {rupee(r['taxable'])}. Slab tax is "
            f"{slab_sentence(r['breakup'])}, totalling {rupee(r['taxBefore'])}." +
            (f" A 10% surcharge of {rupee(r['surcharge'])} applies because taxable income "
             f"crosses ₹50 lakh." if r['surcharge'] > 0 else "") +
            f" Add 4% cess of {rupee(r['cess'])} and the income tax is {rupee(r['tax'])} "
            f"a year. The 87A rebate does not apply once taxable income is past ₹12 "
            f"lakh.\n")

    # ── band-specific section ──
    if b == "micro":
        out.append("## The real-world wrinkles at this salary\n")
        out.append(
            f"Your monthly gross of about {grossM} is under the ₹21,000 ESI ceiling, so "
            f"ESI usually applies: you contribute 0.75% and your employer 3.25%, and you "
            f"get health cover in return. The calculator above does not model ESI, so "
            f"your slip may show a small extra deduction. Several states also waive "
            f"professional tax below a monthly income threshold, which means your actual "
            f"deduction could be ₹{fmt(r['pt'])} lighter than the table. Ask payroll for "
            f"the detailed slip so you know exactly which heads apply.\n")
        out.append(
            f"The ₹{fmt(r['employeePF']/12)} a month going into PF is not really a loss. "
            f"Your employer matches it, so close to {rupee(r['employeePF']*2/12)} a month "
            f"is being saved for you at around 8.25% tax-free. Track it with the "
            f"[EPF calculator](/salary/epf-calculator/).\n")
    elif b == "entry":
        out.append(f"## Why {pct:.0f}% of CTC is about as good as it gets\n")
        out.append(
            f"Your in-hand at ₹{L} lakh is {rupee(r['take'])}, which is roughly "
            f"{pct:.0f}% of CTC. Hold on to that ratio, because it only falls from here. "
            f"As salary climbs, income tax takes a bigger cut and the share reaching your "
            f"hand drops: about 80% near ₹16 lakh, 75% near ₹30 lakh, under 60% at ₹1 "
            f"crore. Early on, almost everything you earn is yours, which is exactly when "
            f"the savings habit is cheapest to build.\n")
        out.append(
            f"The {rupee(r['employeePF']/12)} a month into PF is part of that. Your "
            f"employer adds another {rupee(r['employerPF']/12)}, so about "
            f"{rupee((r['employeePF']+r['employerPF'])/12)} a month is quietly compounding "
            f"for you. Watch it grow with the [EPF calculator](/salary/epf-calculator/).\n")
    elif b == "midzero":
        gap_y = ro["take"] and (r["take"] - ro["take"])
        out.append("## New regime vs old regime at this salary\n")
        out.append(
            f"This is the band where the regime choice is the whole game. Under the new "
            f"regime, taxable income of {rupee(r['taxable'])} sits under the ₹12 lakh "
            f"line, so the section 87A rebate still reaches it and income tax is zero. "
            f"Switch to the old regime with no major deductions and the same ₹{L} lakh is "
            f"taxed {rupee(ro['tax'])} a year, pulling monthly in-hand down to "
            f"{rupee(ro['monthly'])}. That is {rupee(gap_y)} a year, gone for ticking the "
            f"wrong box.\n")
        out.append(
            f"The old regime only catches up if you genuinely stack deductions: the full "
            f"₹1.5 lakh under 80C, ₹25,000 of 80D health cover, ₹50,000 of NPS under "
            f"80CCD(1B), and real HRA exemption from rent paid. Without most of that, stay "
            f"on the new regime. Run your actual numbers both ways in the "
            f"[take-home calculator](/salary/takehome-calculator/) before you commit on "
            f"the joining form.\n")
    elif b == "taxed":
        out.append("## Where the 87A rebate stops and tax begins\n")
        out.append(
            f"At ₹{L} lakh the 87A rebate is no longer in the picture. Taxable income of "
            f"{rupee(r['taxable'])} is past the ₹12 lakh ceiling, so the full slab tax of "
            f"{rupee(r['taxBefore'])} is payable, which after 4% cess is "
            f"{rupee(r['tax'])} a year. Every extra rupee of CTC at this level is taxed at "
            f"your top slab, so a raise here delivers a lot less to your hand than the "
            f"headline suggests.\n")
        out.append(
            f"The single best move in this band is employer NPS under 80CCD(2). Up to 14% "
            f"of basic routed as an employer NPS contribution is deductible even in the "
            f"new regime, which at ₹{L} lakh can shave ₹20,000 to ₹35,000 off your annual "
            f"tax. Ask HR whether your flexi-benefits portal allows it. Confirm the new "
            f"figure in the [income tax calculator](/tax/income-tax-calculator/).\n")
    elif b == "high":
        out.append("## The 30% slab and what to do about it\n")
        out.append(
            f"At ₹{L} lakh the top slice of your income is taxed at 30% under the new "
            f"regime. Slab tax works out to {slab_sentence(r['breakup'])}, and the total "
            f"income tax is {rupee(r['tax'])} a year. Take-home holds near {pct:.0f}% of "
            f"CTC, and the only honest way to lift it is to restructure CTC, not to chase "
            f"deductions the new regime ignores.\n")
        out.append(
            f"Employer NPS under 80CCD(2) is the lever that still works: up to 14% of "
            f"basic, deductible in the new regime, which at this salary can save ₹40,000 "
            f"or more a year. Food coupons and telephone reimbursement add small tax-free "
            f"amounts on top. Plug the revised structure into the "
            f"[take-home calculator](/salary/takehome-calculator/) to see the gain.\n")
    else:  # surcharge
        out.append("## The surcharge layer above ₹50 lakh\n")
        out.append(
            f"Once taxable income crosses ₹50 lakh, a 10% surcharge is added on top of the "
            f"income tax itself. At ₹{L} lakh your taxable income is {rupee(r['taxable'])}, "
            f"so the surcharge of {rupee(r['surcharge'])} stacks onto slab tax of "
            f"{rupee(r['taxBefore'])}, and 4% cess applies on the combined figure. The "
            f"result is {rupee(r['tax'])} of income tax a year and take-home of about "
            f"{pct:.0f}% of CTC.\n")
        out.append(
            f"At this level the deductions that survive in the new regime are limited, but "
            f"employer NPS under 80CCD(2) still helps, and the surcharge makes every "
            f"rupee of deduction worth a little more than its face value. Model your exact "
            f"structure in the [take-home calculator](/salary/takehome-calculator/) and "
            f"sanity-check the tax with the "
            f"[income tax calculator](/tax/income-tax-calculator/).\n")

    # ── ladder ──
    out.append("## How take-home moves across the salary ladder\n")
    out.append(ladder(lpa) + "\n")
    out.append(
        "All figures: new regime, Karnataka professional tax, 50% basic structure, FY "
        "2025-26. Plug your own CTC and city into the "
        "[take-home salary calculator](/salary/takehome-calculator/) for an exact "
        "number.\n")

    # ── sources ──
    out.append("## Sources\n")
    out.append(
        "- Income Tax Act 1961: Section 115BAC new regime slabs, ₹75,000 standard "
        "deduction, Section 87A rebate (FY 2025-26)\n"
        "- EPFO: 12% employee plus 12% employer PF contribution on basic salary\n"
        "- Payment of Gratuity Act 1972: 4.81% gratuity provision formula\n"
        "- State Professional Tax Acts (Karnataka rate used as the representative figure)")

    return "\n".join(out)

# ─────────────────────── frontmatter ───────────────────────
def ai_summary(lpa):
    r = compute(ctc_of(lpa))
    ro = compute(ctc_of(lpa), "old")
    L = lpa_label(lpa)
    pct = r["take"] / r["CTC"] * 100
    bullets = [
        f"₹{L} lakh CTC gives {rupee(r['monthly'])}/month in-hand under the new regime "
        f"(50% basic, Karnataka PT)",
    ]
    if r["tax"] < 1:
        bullets.append("Income tax is zero under the new regime at this CTC")
    else:
        bullets.append(f"Income tax is {rupee(r['tax'])}/year, about {r['tax']/r['CTC']*100:.1f}% of CTC")
    bullets.append(
        f"Employer PF {rupee(r['employerPF'])} and gratuity {rupee(r['gratuity'])} sit "
        f"inside CTC and never reach your bank")
    bullets.append(f"In-hand is about {pct:.0f}% of CTC at this level")
    if ro["tax"] > r["tax"] + 1:
        bullets.append(
            f"Old regime with no major deductions taxes the same CTC {rupee(ro['tax'])}, "
            f"so the new regime is the default winner here")
    else:
        bullets.append(
            "Use the on-site take-home calculator to test your exact structure and city")
    return bullets

def make_post(lpa, i):
    r = compute(ctc_of(lpa))
    L = lpa_label(lpa)
    word = lpa_lakh_word(lpa)
    monthly = rupee(r["monthly"])
    slug = slug_for(lpa)
    taxdesc = ("Zero income tax under the new regime."
               if r["tax"] < 1 else f"Income tax {rupee(r['tax'])}/year.")
    title = f'{word} CTC Take-Home Salary 2025-26: {monthly}/Month In-Hand Breakdown'
    desc = (f"₹{L}L CTC = {monthly}/month in-hand (new regime, 50% basic). {taxdesc} "
            f"Full component breakdown of employer PF, gratuity, professional tax and "
            f"the gap between offer letter and bank credit.")
    summary = ai_summary(lpa)
    summary_yaml = "\n".join(f"- {s}" for s in summary)
    related = "\n".join([
        '  - { label: "Take-Home Salary Calculator", url: "/salary/takehome-calculator/" }',
        '  - { label: "Income Tax Calculator (FY 2025-26)", url: "/tax/income-tax-calculator/" }',
        '  - { label: "EPF Calculator", url: "/salary/epf-calculator/" }',
        '  - { label: "Gratuity Calculator", url: "/salary/gratuity-calculator/" }',
        '  - { label: "Salary Hike Calculator", url: "/salary/salary-hike-calculator/" }',
    ])
    fm = (
        "---\n"
        f'title: "{title}"\n'
        f'description: "{desc}"\n'
        f"date: {TODAY}\n"
        f"lastmod: {TODAY}\n"
        "author: vignesh\n"
        "categories:\n- Salary\n"
        'tags: ["Salary", "Tax planning", "FY 2025-26", "CTC"]\n'
        "ai_summary:\n"
        f"{summary_yaml}\n"
        "related_calcs:\n"
        f"{related}\n"
        "---\n\n"
    )
    return slug, fm + post_body(lpa, i)

def main():
    written = []
    for i, lpa in enumerate(MISSING):
        slug, content = make_post(lpa, i)
        path = BLOG_DIR / f"{slug}.md"
        path.write_text(content, encoding="utf-8")
        written.append(slug)
        print(f"  wrote {slug}.md")
    print(f"\n{len(written)} posts written.")

if __name__ == "__main__":
    main()
