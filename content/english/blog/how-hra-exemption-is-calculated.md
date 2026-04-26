---
title: "How HRA Exemption is Calculated: The Actual Formula"
description: "HRA exemption is the minimum of three values, most salaried employees claim less than they're entitled to. Here's the exact formula, worked examples for metro and non-metro cities, and when HRA beats home loan interest."
date: 2026-04-25
lastmod: 2026-04-25
author: vignesh
categories:
- Tax
tags:
- HRA
- salary
- income tax
- exemption
related_calcs:
  - { label: "HRA Exemption Calculator", url: "/salary/hra-calculator/" }
  - { label: "Income Tax Calculator (FY 2025-26)", url: "/tax/income-tax-calculator/" }
  - { label: "Take-Home Salary Calculator", url: "/salary/takehome-calculator/" }
ai_summary: |
  - **HRA exemption is the MINIMUM of three things**: actual HRA received, 50% of basic (metro) or 40% (non-metro), and rent paid minus 10% of basic salary.
  - Metro cities for HRA purposes are only **Delhi, Mumbai, Chennai, Kolkata**. Bengaluru, Hyderabad, Pune, Gurgaon are all non-metro.
  - Most renters in metros are bottlenecked by component 3 (rent minus 10% of basic), not the 50% rule.
  - HRA is **only available under the old tax regime**. New regime (default FY 2025-26) does not allow HRA exemption.
  - Rent paid to parents counts, but they must declare it as income. Bank transfer + written agreement keeps it clean for scrutiny.
---

Most salaried Indians overclaim or underclaim HRA, sometimes by tens of thousands a year, simply because they treat the formula as one number when it's actually three. The Income Tax Department exempts only the smallest of the three. Knowing which one binds for you decides how much real tax you save.

This is not a complicated rule. Section 10(13A) read with Rule 2A spells out a clean three-way comparison. The reason most people get it wrong is that payroll software just shows the final exempt number, never the calculation, and the rules read like a riddle if nobody walks you through them.

{{< infographic-stat number="3" label="Components compared. The smallest is your HRA exemption." sub="Section 10(13A), Income Tax Rules" >}}

## The three components, in plain English

Pull these three numbers and pick the smallest. That's your exempt HRA for the year.

1. **Actual HRA your employer paid you.** Look at Form 16 Part B, the line that says "House Rent Allowance under section 10(13A)". This is the upper ceiling on what you can ever claim.
2. **50% of (Basic + DA forming part of retirement benefits)** if you live in a metro city. **40%** if you live anywhere else. For most private-sector employees, DA is zero, so this collapses to 50% or 40% of Basic.
3. **Rent paid minus 10% of (Basic + DA).** Annual figures. If your monthly rent is ₹25,000 and basic is ₹50,000, this becomes (25,000 × 12) − (5,000 × 12) = ₹2.4 lakh.

The exempt amount is **min(component 1, component 2, component 3)**. The remainder of your HRA gets added to taxable salary.

## Metro vs non-metro is narrower than you think

Only **Delhi, Mumbai, Chennai, and Kolkata** are metros for HRA purposes. The Income Tax Rules haven't been updated to reflect modern Indian property markets, so:

- Bengaluru, Hyderabad, Pune, Gurgaon, Noida, Ahmedabad: non-metro. 40% of basic.
- Delhi, Mumbai, Chennai, Kolkata: metro. 50%.

A software engineer paying ₹40,000 rent in Bengaluru gets the 40% slab. The same engineer paying ₹40,000 rent in Mumbai gets 50%. Same income, same job, ₹50,000 difference in annual exemption ceiling. Worth knowing if you're choosing between cities.

## Worked example: Bengaluru engineer, ₹50K rent, ₹50K basic

A typical product engineer in Koramangala. Monthly basic + DA: ₹50,000. Monthly HRA from employer: ₹25,000. Monthly rent: ₹40,000.

Annual numbers:

| Component | Annual value |
|---|---|
| ① Actual HRA received | ₹3,00,000 |
| ② 40% of basic (non-metro) | ₹2,40,000 |
| ③ Rent − 10% of basic = (40,000 − 5,000) × 12 | ₹4,20,000 |

The smallest is **₹2,40,000**. That's the exempt HRA for the year. The remaining ₹60,000 of HRA gets taxed at the slab rate. At 30% slab plus 4% cess, that's ₹18,720 of tax on the unexempt portion.

If the same person moved to Mumbai with the same rent and basic, component 2 becomes 50% × ₹6L = ₹3,00,000. That now ties with component 1, but component 3 stays at ₹4,20,000. The exempt amount jumps from ₹2,40,000 to ₹3,00,000, saving an extra ₹18,720 in tax just from the metro classification.

## Why component 3 usually binds

If your rent is roughly half of your basic salary or more, component 3 is the smallest. That's the situation for most renters in tier-1 cities, where rent has outpaced salary growth for the last decade.

Run the numbers in the [HRA exemption calculator](/salary/hra-calculator/) for your own salary and rent, and you'll see one of three outcomes:

- Component 1 binds: your employer is structuring HRA too low. Ask payroll to bump it up.
- Component 2 binds: you're in a metro and your rent is unusually low compared to basic. Either restructure salary or accept the cap.
- Component 3 binds: your rent is high relative to basic. Most common case for tier-1 renters.

## Rent paid to parents: the rule and the gotchas

Yes, you can pay rent to your parents and claim HRA. Several Income Tax Tribunal rulings have upheld this, including *Meena Vaswani v. ACIT* (ITAT Mumbai, 2017). Two conditions:

1. The parent must own the property (or be paying rent themselves on it).
2. The parent must declare this rental income on their own ITR.

If your parent is in a lower tax slab than you, the family unit saves real money. A child in the 30% slab paying ₹3 lakh rent to a parent in the 5% slab effectively transfers ₹3 lakh of taxable income from a 30% bucket to a 5% bucket. Annual saving: roughly ₹75,000.

What gets rejected in scrutiny: cash payments, no rent agreement, parent not filing ITR, payments timed weirdly (one annual lump sum instead of monthly). Treat it like a real rental: bank transfer monthly, written agreement, regular timing.

## When the new tax regime kills HRA

Under the new tax regime (default from FY 2025-26), HRA exemption is **not allowed**. Your full HRA gets added to taxable salary. So if HRA was a meaningful part of your tax planning under the old regime, switching to new regime drops the exemption entirely.

Quick rule of thumb. If your annual exempt HRA under the old regime exceeds about ₹2.5 lakh, the loss from new-regime switch may outweigh the lower slab benefit. Run both regimes through the [income tax calculator](/tax/income-tax-calculator/) before declaring to payroll.

## Documents to keep

The tax department asks for these if you're picked for scrutiny:

- Rent receipts for every month, signed by the landlord
- Rent agreement showing tenancy and amount
- Landlord PAN if your annual rent crosses ₹1,00,000 (mandatory under Rule 26C)
- Bank statements showing rent transferred via NEFT or UPI

Cash rent payments above ₹50,000/month are red-flagged automatically in 2026. Move to bank transfers if you haven't already.

## What changed recently

Nothing in the HRA formula itself has changed in years. The only meaningful 2025 change was the new tax regime becoming the default. So if you're new to the workforce or just shifted regimes, the HRA decision is now: stay on old regime to keep HRA, or switch to new regime and accept full HRA tax.

The cross-over point depends on your full deduction stack, not just HRA. Plug your numbers into both regimes and pick the cheaper one. The [HRA exemption calculator](/salary/hra-calculator/) handles the section 10(13A) maths; the [income tax calculator](/tax/income-tax-calculator/) handles the regime comparison.

## Sources

- Income Tax Act 1961: Section 10(13A) and Rule 2A
- CBDT Circular No. 8/2018: simultaneous HRA + home loan interest claim
- Meena Vaswani v. ACIT, ITAT Mumbai (2017): rent to parents
- Income Tax Rule 26C: PAN requirement above ₹1L annual rent
