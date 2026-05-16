---
title: "Salary Calculator Excel: Free Breakup Sheet + Live CTC Calculator (FY 2025-26)"
description: "Calculate your salary breakup online, then download the full breakup as an Excel sheet. Indian CTC structure (Basic, HRA, LTA, Special, EPF, PT, Income Tax) for FY 2025-26. New + Old regime. No sign-up."
date: 2026-05-09
lastmod: 2026-05-09
type: "calculator"
url: /salary/salary-breakup-excel/
keywords: "salary calculator excel, ctc calculator in excel, salary calculator excel sheet, salary breakup calculator excel, salary breakup format in excel, salary calculation in excel, salary calculator excel sheet with formula, ctc calculator in excel free, salary calculator india, calxo"
categories:
- Salary Calculators
author: vignesh
ai_summary:
  - "Live salary breakup calculator with one-click Excel download. Enter CTC, regime, city, EPF mode, get the full annual + monthly breakup."
  - "Excel file has every line item (Basic, HRA, LTA, Special, EPF, PT, Income Tax, Cess) plus the inputs used, ready to paste into your payroll sheet."
  - "All formulas shown below the calculator. Copy them straight into Google Sheets or your own .xlsx."
  - "Built for FY 2025-26 Indian payroll: New regime 87A rebate up to ₹12L taxable, Old regime up to ₹5L, surcharge tiers, 4% cess."
  - "No sign-up, no email gate, no PDF wall. The Excel download is one click."
---

Most salary calculators online give you a number on the screen. That works for a quick check, but if you're an HR manager structuring offer letters, a finance lead reviewing payroll, or an employee comparing two job offers, you actually want the breakup **in Excel**. Sortable, editable, shareable with your CFO.

The tool below does both. Use the live calculator on the left, then hit "Download Excel" and a complete .xls sheet lands in your downloads folder. Same numbers, ready to paste into your own payroll template.

{{< salary-breakup-excel >}}

{{< infographic-stat
  number="₹85,395 / mo"
  label="Take-home on ₹12L CTC under New Regime (FY 2025-26)"
  sub="Default scenario shown above, Karnataka PT, statutory EPF" >}}

## The Excel file structure (what you download)

The downloaded .xls file mirrors what's on screen. Three sections:

**Earnings.** Basic Pay, HRA, LTA, Special Allowance, totalled to Gross Salary. Each row shows annual and monthly columns.

**Deductions.** EPF employee contribution, Professional Tax for your state, Income Tax + 4% Cess, totalled.

**Net In-Hand.** Annual and monthly take-home, highlighted in green.

**CTC reconciliation.** Annual CTC, employer PF, gratuity provision (4.81% of Basic). This is the part most salary slips hide. Useful when you're checking why your CTC and gross don't match.

**Inputs used.** The exact settings (regime, city, basic %, HRA %, EPF mode, PT state). When you share the file with HR or your spouse, they know exactly what assumptions went into the numbers.

Excel opens this file directly. So does Google Sheets, LibreOffice, Apple Numbers, and Zoho Sheet. No conversion needed.

## Indian salary formulas (paste these into your own sheet)

This is the part HR folks bookmark. Every formula your payroll system uses, in Excel syntax. The cell references assume your CTC is in cell B2.

### Salary structure

```
Component       | Excel formula
─────────────────────────────────────────────────────
Basic Pay       | =B2 * 50%
HRA             | =Basic * 50%    (Metro)
                | =Basic * 40%    (Non-metro)
LTA             | (user-defined, typically ₹0–₹50,000)
Employer PF     | =MIN(Basic*12%, 21600)
Gratuity        | =Basic * 4.81%
Special Allow.  | =B2 - Basic - HRA - LTA - Employer_PF - Gratuity
Gross Salary    | =Basic + HRA + LTA + Special
```

The 50% basic and 50% HRA defaults match the new wage code recommendations and standard private-sector practice. Some PSUs and government rules use 40%-30% splits.

### Deductions

```
Component       | Excel formula
─────────────────────────────────────────────────────
EPF (employee)  | =MIN(Basic*12%, 21600)
Professional Tax| =LOOKUP(state, KA:2400, MH:2500, TN:2496, ...)
Standard Ded.   | =75000  (New regime)
                | =50000  (Old regime)
```

EPF caps at ₹1,800/month (₹21,600/year) when the employer opts for the statutory minimum. Most large IT companies and MNCs pay the full 12% of basic, not the cap. PSUs and small companies often cap.

### HRA exemption (Old regime only)

```
HRA_received        = Basic * 50%   (or 40%)
HRA_50pct_basic     = Basic * 50%    (Metro)
HRA_40pct_basic     = Basic * 40%    (Non-metro)
HRA_rent_minus_10   = MAX(0, Actual_Rent - Basic * 10%)

HRA_exempt = MIN(HRA_received, HRA_pct_basic, HRA_rent_minus_10)
```

The three-condition minimum is straight from Section 10(13A). The exemption is the **least** of the three. If you don't pay rent or live with parents (no rent receipts), HRA exemption is zero.

### Income tax (New Regime FY 2025-26)

```
Standard Deduction    | =75000
Taxable Income        | =Gross - 75000

Slab tax              | =IFS(
                      |   Taxable<=400000, 0,
                      |   Taxable<=800000, (Taxable-400000)*5%,
                      |   Taxable<=1200000, 20000 + (Taxable-800000)*10%,
                      |   Taxable<=1600000, 60000 + (Taxable-1200000)*15%,
                      |   Taxable<=2000000, 120000 + (Taxable-1600000)*20%,
                      |   Taxable<=2400000, 200000 + (Taxable-2000000)*25%,
                      |   TRUE, 300000 + (Taxable-2400000)*30%
                      | )

87A Rebate            | =IF(Taxable<=1200000, MIN(Slab_tax, 60000), 0)
Marginal Relief       | =IF(AND(Taxable>1200000, Tax>(Taxable-1200000)),
                      |     Taxable-1200000, Tax)
Cess                  | =(Tax + Surcharge) * 4%
Final Tax             | =Tax + Surcharge + Cess
```

The 87A rebate makes income up to ₹12 lakh taxable (which means ₹12,75,000 gross after standard deduction) **completely tax-free** under the new regime. This was a huge change in Budget 2025. Most salary calculators built before April 2025 still use the old ₹7L rebate threshold.

### Income tax (Old Regime FY 2025-26)

```
Standard Deduction    | =50000
Section 80C cap       | =MIN(investments_80C, 150000)
Section 80D cap       | =MIN(health_premium, 25000)
                      | =MIN(health_premium, 50000)  (if age 60+)
NPS 80CCD(1B) cap     | =MIN(nps_amount, 50000)
Section 24(b) cap     | =MIN(home_loan_interest, 200000)

Taxable Income        | =Gross - 50000 - 80C - 80D - NPS - 24b - HRA_exempt

Slab tax (age <60)    | =IFS(
                      |   Taxable<=250000, 0,
                      |   Taxable<=500000, (Taxable-250000)*5%,
                      |   Taxable<=1000000, 12500 + (Taxable-500000)*20%,
                      |   TRUE, 112500 + (Taxable-1000000)*30%
                      | )

87A Rebate (Old)      | =IF(Taxable<=500000, MIN(Slab_tax, 12500), 0)
Cess                  | =(Tax + Surcharge) * 4%
```

Old regime keeps the slabs Indian taxpayers grew up with. Lower exemption limit, but lets you claim every section deduction. Best for people with home loans (heavy 24b), high 80C savers, and salaried folks who pay rent and have proper rent receipts.

### Surcharge (both regimes)

```
Surcharge rate (New Regime)
  income > ₹50L  and ≤ ₹1Cr → 10%
  income > ₹1Cr  and ≤ ₹2Cr → 15%
  income > ₹2Cr               → 25%  (capped)

Surcharge rate (Old Regime)
  income > ₹50L  and ≤ ₹1Cr → 10%
  income > ₹1Cr  and ≤ ₹2Cr → 15%
  income > ₹2Cr  and ≤ ₹5Cr → 25%
  income > ₹5Cr               → 37%
```

This is why high earners migrated to New Regime in 2025-26. The surcharge cap of 25% (vs the old regime's 37%) plus higher rebate threshold flipped the math for most ₹50 lakh+ earners.

## What a typical Indian CTC actually contains

If you've ever opened your offer letter and counted 14 line items, this is why. A realistic Indian CTC breakup for a ₹12 lakh package looks like this:

| Component | Annual | Notes |
|---|---:|---|
| Basic Pay | ₹6,00,000 | 50% of CTC under new wage code |
| HRA | ₹3,00,000 | 50% of basic (metro) |
| LTA | ₹0 to ₹50,000 | Tax-exempt twice in 4 years if claimed |
| Special Allowance | ~₹99,140 | Balancing figure |
| Employer EPF | ₹72,000 | 12% of basic |
| Gratuity provision | ₹28,860 | 4.81% of basic, paid on exit |
| **CTC** | **₹12,00,000** | Total cost to company |

Below this, deductions take their cut: employee EPF (₹72,000), professional tax (₹2,400 in Karnataka), and income tax. Under the new regime with the ₹12 lakh rebate threshold, this scenario lands at ₹0 income tax. Take-home: ₹85,395/month.

The gap between CTC (₹12L) and in-hand (₹10.25L/yr) is mostly the EPF contributions, gratuity provision, and PT. Income tax adds very little until CTC crosses ₹15-17 lakh under the new regime.

## When the new wage code (2019) kicks in

Indian salaries are slowly migrating to a 50% basic structure because of the Code on Wages 2019. The four labour codes were notified in 2025 with phased rollout. The big change for salary structures:

Basic Pay must be **at least 50% of total wages** for PF, gratuity, and bonus computation. If your offer letter still has 35% basic and 50% special allowance, your CFO is reading the new circular and your structure is changing soon.

What this does to take-home: higher PF deduction (12% of higher basic), higher gratuity provision, slightly less take-home today but a much bigger PF corpus at retirement and a bigger gratuity on exit. Net effect on most ₹10-20L earners: ₹2,000 to ₹5,000 less monthly in-hand for the same CTC.

## FAQs

**Where do I download the salary calculator Excel sheet?**

Right here. Set your inputs in the calculator above, then click "Download Excel". The file generates from your current numbers on the page. It's an .xls file that opens directly in Excel, Google Sheets, LibreOffice, and Apple Numbers.

**Can I edit the formulas in the downloaded file?**

The downloaded .xls is a values-only export, not a formula sheet. The numbers are computed in your browser and pasted as values. If you want formula-based cells, copy the formulas from the "Indian salary formulas" section above into a fresh sheet. That's a one-time setup, then you reuse the file.

**Does the Excel work for FY 2024-25 instead of 2025-26?**

The slabs and rebate amounts in the downloaded file match FY 2025-26 (Budget 2025 rules). If you need FY 2024-25 numbers, change two values manually:
- New regime rebate: ₹25,000 (not ₹60,000)
- New regime rebate threshold: ₹7L taxable (not ₹12L)
- New regime slabs were slightly different (Budget 2025 rewrote them)

**What if my company uses a different basic/HRA split?**

Move the Basic % slider. Common alternatives: 40% basic + 50% HRA (older private sector), 30% basic + 60% HRA (illegal under new wage code but still common in informal contracts), 60% basic + 40% HRA (post-wage-code-compliant, IT bellwethers).

**Why does my actual salary slip show different numbers?**

Three usual reasons. One, your company has variable pay or performance bonus that isn't in the monthly slip. Two, your TDS is computed assuming you'll claim certain deductions (which you confirm via Form 12BB in April). Three, leave encashment, bonus, and one-time payments hit specific months and skew that month's slip.

**Is the Excel download safe? Does it send my data anywhere?**

No data leaves your browser. The calculation runs locally, the Excel file is generated locally, and the download happens directly from your browser. Calxo doesn't have an account system, an analytics-tracker on inputs, or any server that processes salary numbers. Open developer tools and check network tab if you want to verify.

**Is this a salary calculation excel sheet I can save and reuse?**

Yes. Click "Download Excel" to save your salary calculation excel sheet locally. Reopen it any time, copy it into your team's payroll workbook, or send it to HR. The file is a plain .xls with no macros, no external links, and no Calxo branding stripped from the worksheet itself (only the file footer mentions the source). If you want to convert it to .xlsx, open in Excel and use Save As.

**Can I use this for senior citizen tax calculation?**

The Old Regime slabs change for people aged 60+ (exempt up to ₹3L) and 80+ (exempt up to ₹5L). This page uses the under-60 slabs by default. For more accurate senior-citizen Old Regime math, use the [Take-Home Salary Calculator](/salary/takehome-calculator/) which has age band selection.

## Related calculators

- [Take-Home Salary Calculator](/salary/takehome-calculator/): full version with age bands, 80C/80D/NPS/24(b) inputs, and best-regime auto-recommendation
- [HRA Exemption Calculator](/salary/hra-calculator/): just the HRA calc, with rent and city inputs
- [Income Tax Calculator](/tax/income-tax-calculator/): both regimes, slab-by-slab
- [Gratuity Calculator](/salary/gratuity-calculator/): how much gratuity you'll get on exit
- [EPF Calculator](/salary/epf-calculator/): corpus projection at retirement
- [Salary Hike Calculator](/salary/salary-hike-calculator/): see the in-hand impact of a raise

## Sources

- Income Tax Act, 1961 — Section 10(13A): HRA exemption rules; Section 16: standard deduction ₹75,000 (FY 2025-26)
- Employees' Provident Fund and Miscellaneous Provisions Act, 1952 — 12% employee contribution on basic salary
- Employees' State Insurance Act, 1948 — ESI applicability threshold: gross salary up to ₹21,000/month
- State-specific Professional Tax schedules — Maharashtra, Karnataka, Tamil Nadu, Andhra Pradesh, West Bengal
