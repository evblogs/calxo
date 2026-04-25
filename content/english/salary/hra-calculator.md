---
title: "HRA Calculator: Calculate House Rent Allowance Exemption (Section 10(13A))"
description: "Free HRA exemption calculator under section 10(13A) of the Income Tax Act. Computes the exempt portion as the minimum of three statutory components — actual HRA, 50%/40% of basic, and rent minus 10% of basic — for metro and non-metro cities."
date: 2026-04-25
lastmod: 2026-04-25
type: "calculator"
url: /salary/hra-calculator/
keywords: "hra calculator, hra exemption calculator, section 10 13a, house rent allowance calculator, hra metro non metro, hra tax exemption india, calxo"
categories:
- Salary & HR Calculators
author: vignesh
---

The calculator below applies the standard **section 10(13A)** rule for House Rent Allowance: the exempt amount is the **lowest of three values**, and only that lowest amount escapes income tax. Plug in your monthly basic plus DA, the HRA your salary slip shows, and the rent you actually pay. The widget computes all three components, highlights the winning one, and tells you the rough tax you save assuming you're in the highest slab.

A note on the regime: HRA exemption under section 10(13A) is allowed **only under the old tax regime**. If you've opted into the new regime (the default from FY 2025-26), HRA is fully taxable. Run the new vs old comparison on the [income tax calculator](/tax/income-tax-calculator/) before relying on HRA savings.

{{< hra-calculator >}}

## How HRA exemption is calculated

The Income Tax Act, section 10(13A) read with Rule 2A, says the exempt portion of HRA is the **minimum of**:

1. **Actual HRA received** from the employer for the period
2. **50% of (Basic + DA forming part of retirement benefits)** if you live in a metro city, or **40%** if non-metro
3. **Rent paid minus 10% of (Basic + DA)** for the same period

Whatever's smallest is the exempt amount; the rest of your HRA is taxable.

The "metro" definition in this context is narrower than people assume. Only **Delhi, Mumbai, Chennai and Kolkata** count as metros for HRA purposes. Bengaluru, Hyderabad, Pune, Ahmedabad, Gurgaon, Noida — all non-metro for HRA. The 50% versus 40% split is in the Income Tax Rules and hasn't been updated to reflect actual rent levels in tier-1 cities, so most Bengaluru and Hyderabad employees end up exempting a smaller share of their HRA than equivalent Delhi colleagues do.

## What counts as "salary" for HRA?

For the 50%/40% calculation and the rent-minus-10% calculation, "salary" means:

- **Basic salary** (always)
- **Dearness allowance (DA)** — only if it's "forming part of retirement benefits" (i.e., used to compute PF, gratuity, pension). Most private-sector DA is not retirement-linked, so most private-sector employees use Basic alone. Government employees use Basic + DA.
- **Commission** — only the part computed as a fixed percentage of turnover achieved, per the *Gestetner Duplicators* Supreme Court ruling. Discretionary bonuses and target-linked variable pay are excluded.

HRA itself, special allowance, conveyance, LTA, medical and other allowances do **not** count. Use only the components that form the basic compensation.

## Worked example: ₹50,000 basic in Bengaluru

Take a software engineer in Bengaluru with the following monthly salary structure:

- Basic + DA: ₹50,000
- HRA from employer: ₹25,000
- Actual rent paid: ₹22,000
- City: non-metro (40%)

Annual figures:

| Component | Annual value |
|---|---|
| ① Actual HRA received | ₹3,00,000 |
| ② 40% of (Basic + DA) | ₹2,40,000 |
| ③ Rent paid − 10% of Basic = (22,000 − 5,000) × 12 | ₹2,04,000 |

**Lowest = ③ = ₹2,04,000**. So ₹2,04,000 of your annual HRA is exempt; the remaining ₹96,000 is taxable. Approximate tax saved at the 30% slab + 4% cess: about **₹63,648** per year.

If the same person moved to Mumbai with identical basic and rent, ② becomes 50% × ₹6L = ₹3,00,000, but ③ stays at ₹2,04,000 (rent didn't change). Component ③ is still the binding constraint, so the exemption stays the same. Most middle-income renters end up bottlenecked by component ③ — the rent they actually pay determines exemption more than the city does.

## Why component ③ usually wins

Look at the formula: `Rent − 10% × Basic`. Unless your rent is **at least 50% of basic** (metro) or 40% (non-metro), component ② won't be the binding constraint. Most salaries are structured with HRA at 40–50% of basic, so component ① often beats ② in metros only when the employer is generous with HRA structuring.

In practice:

- If you pay rent equal to ~50% of your basic (very common for renters in tier-1 cities), component ③ binds — your real rent number drives everything.
- If you pay much lower rent (paying-guest, shared, sub-metro), components ① or ② may bind instead, and you lose exemption potential.
- If you pay rent to your parents, you can still claim HRA — but the parents must declare that rental income on their own ITR, and ideally the rent should be paid by bank transfer with a written rent agreement. The IT Department flags this in scrutiny if it looks artificial.

## Documents to keep for HRA

The Income Tax Department can ask for proof, especially during e-verification or scrutiny. Keep:

- **Rent receipts** for every month, signed by the landlord
- **Rent agreement** showing tenancy terms and amount
- **Landlord's PAN** if your annual rent crosses ₹1,00,000 (mandatory under Rule 26C)
- **Bank statements** showing rent transferred via NEFT/UPI (cash payments are now red-flagged in scrutiny, especially for HRA above ₹50,000/month)
- **Form 16** with HRA component shown by the employer

If you're paying rent to a relative, treat it like a real arms-length transaction: agreement, bank transfer, regular timing, landlord declaring income. Half-baked arrangements get rejected and the full HRA becomes taxable.

## Frequently asked questions

### Can I claim HRA and home loan interest at the same time?

Yes, both — under the old regime — if the situations are genuinely independent. Common case: you own a flat in your home town (claim home loan interest u/s 24) and rent in the city you work in (claim HRA u/s 10(13A)). The IT Department has clarified this in CBDT Circular No. 8/2018. Even if both properties are in the same city, it's permissible if you can show the owned property is genuinely not occupied (e.g., it's let out, or under construction, or far from your workplace).

### What if I move mid-year between metro and non-metro?

The 50%/40% calculation should be done period-wise. April–September in Mumbai gets 50%; October–March in Bengaluru gets 40%. Most employer payroll systems handle this if you update the address; otherwise compute it manually at filing time. The same applies if your rent or basic changes mid-year — break the year into windows and compute each separately.

### Does new tax regime allow HRA exemption?

No. Under the default new regime (115BAC), section 10(13A) HRA exemption is not available — your full HRA is taxable. If your HRA exemption potential is significant (i.e., component ③ is large because you pay high rent), the old regime might be cheaper despite lower slabs in the new regime. Compute both regimes against your actual deduction stack on the [income tax calculator](/tax/income-tax-calculator/) and pick whichever pays less.

### Can I claim HRA without rent receipts?

For annual HRA up to ₹3,000/month (₹36,000/year), the employer can grant exemption based on a self-declaration without receipts. Above that, you need rent receipts and (if rent > ₹1L/year) the landlord's PAN. If you don't have receipts and the HRA component is large, the employer is required to deny the exemption at TDS time.

### What's the deal with HRA paid to parents?

It's allowed, but it has to be a real transaction: parents must own the property (or pay rent themselves on it), you must transfer rent via bank, parents must show this rental income on their ITR, and ideally there should be a written agreement. If the parents are in a lower tax slab than you, the family unit saves tax overall — perfectly legal under section 10(13A) and confirmed in multiple ITAT rulings (Meena Vaswani v. ACIT, ITAT Mumbai, 2017). What gets rejected is fictitious rent — payments routed back via cash, no tenancy reality, parents in same household sharing the same flat.

### Is HRA taxable if I live in my own house?

Yes, fully taxable. You can't claim HRA exemption if you don't actually pay rent. This catches a lot of people who structure their salary with high HRA assuming they'll get the exemption regardless. If you live in your own home, your full HRA component is added to taxable income. Switch the calculator's regime/strategy or restructure your salary slip with HR if your living situation is going to be permanent.

### How does HRA work for self-employed people?

Section 10(13A) is only for salaried employees. Self-employed taxpayers and freelancers can't claim HRA. They can claim **section 80GG** instead, which works similarly but caps the deduction at the lower of: ₹5,000/month, 25% of total income, or rent − 10% of total income. The 80GG cap is much smaller in practice, so self-employed renters in metros end up subsidising less rent through the tax code than salaried colleagues do.

### Is exempt HRA shown in Form 16?

Yes. Look at Part B of your Form 16 — there's a line "House Rent Allowance under section 10(13A)" with the exempt amount. The taxable portion shows up under "Salary as per provisions of section 17(1)". Cross-check this against the calculator's output; if the employer has computed less than what the rule allows, you can claim the differential at filing time.

## Sources

- Income Tax Act 1961: Section 10(13A) and Rule 2A
- CBDT Circular No. 8/2018: Home loan and HRA simultaneous claim
- Gestetner Duplicators Pvt Ltd v. CIT (1979) 117 ITR 1 (SC) — definition of "salary" for HRA
- Meena Vaswani v. ACIT, ITAT Mumbai (2017) — HRA paid to parents
- Income Tax Rule 26C: PAN of landlord requirement above ₹1L annual rent
