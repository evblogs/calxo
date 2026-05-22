---
title: "Retirement Calculator India: How Much Corpus Do You Need?"
description: "Free retirement corpus calculator for India. Find out exactly how much you need to retire, what monthly SIP to start today, and how inflation erodes your retirement expenses. Covers any age and lifestyle."
date: 2026-05-23
lastmod: 2026-05-23
type: "calculator"
url: /investment/retirement-calculator/
keywords: "retirement calculator india, retirement corpus calculator, how much to retire india, retirement planning calculator, retirement savings calculator india"
categories:
- Investment Calculators
author: vignesh
---

The honest answer to "how much do I need to retire?" is: more than you think, and the gap between your guess and the actual number is usually startling. Not because the math is hard. Because inflation compounds in the same merciless way that your investments do, but in the opposite direction.

The calculator below does the full computation: inflates today's expenses to retirement day, figures out the corpus that sustains them for however many years you plan, and tells you the monthly SIP to start building it right now.

{{< retirement-calculator >}}

## How the corpus number is calculated

There are three steps.

**Step 1: Inflation-adjusted expenses at retirement.** Whatever you spend today in monthly expenses gets inflated by your assumed rate for the number of years until retirement. If you spend ₹50,000/month today and retire in 30 years, your retirement-day expenses at 6% inflation will be ₹50,000 × (1.06)^30 = ₹2,87,175/month.

**Step 2: Corpus required.** Post-retirement, your corpus earns returns but expenses keep rising with inflation. The real monthly return is calculated as (1 + post-ret return) / (1 + inflation) − 1. The corpus required is the present value of that monthly expense stream over your retirement years, discounted at the real return rate.

`Corpus = Monthly expense at retirement × (1 − (1 + real_i)^(−N)) / real_i`

where N = retirement months and real_i = real monthly return.

**Step 3: Monthly SIP.** How much to invest monthly, starting today, to reach that corpus by retirement using your pre-retirement return assumption.

`SIP = Corpus × i / ((1+i)^n − 1) × 1/(1+i)`

where i = monthly pre-retirement rate, n = months to retirement.

## Worked example: Aditya, 32 years old, Bengaluru

Aditya is 32, earns ₹1.5 lakh/month in Bengaluru, and spends roughly ₹75,000/month (rent, food, EMIs, lifestyle). He wants to retire at 60. Realistic life expectancy for retirement planning: 85 years (25 years in retirement).

Default assumptions:
- Inflation: 6%
- Pre-retirement return (SIP in equity): 12%
- Post-retirement return (balanced fund / FD mix): 7%

Running the calculator:

| Output | Value |
|---|---|
| Years to retirement | 28 |
| Monthly expenses at retirement | ₹3,83,559 |
| Total corpus required | ₹4.77 crore |
| Monthly SIP to start today | ₹21,200 |

That ₹21,200/month is 14% of his take-home. Manageable. If he waits 5 years to start (age 37), the same calculation requires ₹38,000/month. Wait another 5 (age 42), it jumps to ₹69,000/month. The SIP required roughly doubles every 5 years of delay because the compounding runway shrinks.

{{< infographic-stat
  number="₹21,200"
  label="Monthly SIP at age 32 to retire comfortably at 60 with ₹75K/month expenses"
  sub="Waiting 5 years makes it ₹38,000/month" >}}

## The biggest mistake in retirement planning

Using today's expenses without inflation is the most common error. Someone sees ₹50,000/month expenses, figures they need ₹1 crore (assuming 5% drawdown) and calls it done. They have not accounted for the fact that ₹50,000 in 2026 will be worth roughly ₹16,000 in 2056. The actual corpus needed for that same standard of living, inflated at 6%, is closer to ₹4–5 crore depending on life expectancy.

The second mistake is using a post-retirement return higher than inflation. If you plan to park your retirement corpus entirely in FDs at 7% and inflation runs at 6%, your real return is 1%. After tax, it is negative. Your corpus shrinks in real terms every year. You need at least some equity allocation post-retirement to maintain purchasing power.

## What return to use post-retirement

| Corpus allocation | Realistic post-ret return |
|---|---|
| 100% FD / debt | 6.5–7% (pre-tax) |
| 70% debt, 30% equity | 7.5–8.5% |
| 50% debt, 50% equity | 9–10% |
| 100% equity | 11–12% (high volatility risk) |

Most Indian retirees should target a 70/30 or 60/40 debt-equity mix at retirement. 7% is the conservative post-retirement return to use if you want a plan that works even in bad market years.

## What about EPF, PPF, and NPS?

The calculator gives you the SIP needed from scratch. In practice, EPF accumulates throughout your career (employer contributes 12% of basic). A 32-year-old with ₹50,000 basic salary will accumulate roughly ₹1.5–2 crore in EPF by age 60 (conservative estimate). PPF at maximum ₹1.5 lakh/year for 30 years at 7.1% grows to about ₹1.47 crore. NPS adds another layer.

Reduce the calculator's required corpus by your projected EPF + PPF + NPS balance to get the actual SIP gap you need to fill. Use the [EPF Calculator](/salary/epf-calculator/) and [PPF Calculator](/investment/ppf-calculator/) to estimate those balances.

## The 4% rule, India context

The 4% rule says withdraw 4% of corpus annually and it should last 30 years (from US research, 1990s). In India, applying it blindly is problematic. Indian inflation is structurally higher (6% vs US 2–3%), so a 4% withdrawal rate combined with 6% inflation means your real corpus depletes faster. Indian equity returns are also higher (12% nominal vs 8–10% US), which partially compensates.

A more India-appropriate withdrawal rate for a 25-year retirement horizon with 6% inflation and 7% post-retirement return is closer to 3.5–4%. The calculator handles this precisely rather than using a rule of thumb. The corpus it generates sustains your inflation-adjusted expenses for exactly the retirement years you specify, using your chosen return assumption.

## Frequently asked questions

### I'm 45 and have nothing saved. Is it too late?

No, but you need a larger SIP or a more modest lifestyle target. A 45-year-old planning to retire at 65 (20 years) with ₹60,000/month today's expenses needs roughly ₹3.5 crore corpus and a ₹38,000/month SIP at 12% return. Uncomfortable, but achievable. The key is not to keep delaying.

### Should I factor in rental income?

Yes, if you own property that will generate reliable rental income post-retirement. Subtract that monthly rental (inflated to retirement year if it will grow) from your post-retirement expense requirement before computing corpus. A second flat generating ₹30,000/month now that grows to ₹1.5 lakh by retirement (at 6% rent inflation over 25 years) meaningfully reduces the corpus you need to build.

### What about children's education and marriage expenses?

Don't mix them into the retirement calculator. Build a separate goal for each major expense: education in 15 years, marriage in 20 years. Use the [SIP Calculator](/investment/sip-calculator/) for each goal independently. Mixing goals in one calculator leads to under-saving for both.

### The SIP number looks impossible. What do I do?

Accept a later retirement age, lower monthly expenses post-retirement, or both. Retiring at 63 instead of 60 gives 3 more years of SIP contributions and 3 fewer years of corpus drawdown. Adjusting lifestyle from ₹75,000 to ₹55,000/month in retirement drops the corpus requirement significantly. The calculator lets you iterate all these levers.

## Sources

- RBI: Indian CPI inflation data, 2000–2025
- PFRDA: NPS annuity rates and corpus benchmarks 2025
- EPFO: Interest rate and contribution history
- RBI: FD benchmark rates, repo rate corridor 2025–26
