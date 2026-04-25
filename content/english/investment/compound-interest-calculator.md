---
title: "Compound Interest Calculator: Annual, Quarterly, Monthly Compounding"
description: "Free compound interest calculator with all standard compounding frequencies — annual, half-yearly, quarterly, monthly, daily and simple interest. Computes maturity, interest earned, and effective annual yield using the standard A = P(1 + r/n)^(nt) formula."
date: 2026-04-25
lastmod: 2026-04-25
type: "calculator"
url: /investment/compound-interest-calculator/
keywords: "compound interest calculator, compound interest formula, ci calculator, daily compounding calculator, monthly compounding, calxo"
categories:
- Investment Calculators
author: vignesh
---

The calculator below works for any one-time deposit at a fixed rate over any tenure, with any standard compounding frequency. Use it whenever you need to translate a quoted "X% per annum compounded Y" into a real maturity value — for FDs, RDs, NCDs, NSC, KVP, corporate bonds, or any savings instrument that quotes interest with a frequency.

The single most useful number it shows is the **effective annual yield** — the equivalent flat annual rate, after factoring compounding. That's the apples-to-apples number to compare across instruments quoting different compounding conventions.

{{< compound-interest-calculator >}}

## How compound interest is calculated

The standard formula:

`A = P × (1 + r / n)^(n × t)`

- **A** is the amount at maturity
- **P** is the principal
- **r** is the annual interest rate (as a decimal — 10% = 0.10)
- **n** is the number of compounding periods per year
- **t** is the time in years

For simple interest (no compounding):

`A = P + P × r × t`

The compound formula adds interest to principal every period and computes the next period's interest on the new (higher) base. Simple interest charges only on the original principal for the entire term — much less interest, and almost no instrument in modern Indian banking actually uses simple interest except very short money-market borrowings and some agricultural loans.

## Compounding frequencies that matter

| Frequency | n | When you'll see it |
|---|---|---|
| Annually | 1 | NSC, KVP, EPF, PPF, most government small-saving schemes |
| Half-yearly | 2 | Some senior-citizen schemes (SCSS), few corporate FDs |
| **Quarterly** | **4** | **Standard for most Indian bank FDs** (SBI, HDFC, ICICI, Axis, BoB) |
| Monthly | 12 | Some NBFCs, some corporate FDs, savings account interest at most banks |
| Daily | 365 | Some HNI savings accounts, foreign-currency deposits |
| Continuous | ∞ | Theoretical limit; not used in real Indian instruments |

Higher frequency means slightly higher effective return at the same headline rate. The jump from annual to quarterly is meaningful (~0.5% effective on a 7% headline); quarterly to daily is much smaller (~0.1%).

## Worked example: ₹1,00,000 at 10% for 5 years, quarterly

The default scenario above.

- P = ₹1,00,000
- r = 0.10
- n = 4 (quarterly)
- t = 5

`A = 1,00,000 × (1 + 0.10/4)^(4 × 5) = 1,00,000 × 1.025^20 = 1,00,000 × 1.6386`

| Metric | Value |
|---|---|
| Principal | ₹1,00,000 |
| Maturity | ₹1,63,862 |
| Interest earned | ₹63,862 |
| Effective annual yield | 10.38% |

The effective yield (10.38%) is higher than the headline rate (10%) because of quarterly compounding. This is the right number to compare across instruments quoting different conventions.

## How frequency changes the math

Same ₹1 lakh, 10% rate, 5 years, varying compounding:

| Frequency | Maturity | Effective yield |
|---|---|---|
| Simple interest | ₹1,50,000 | 10.00% (flat) |
| Annual | ₹1,61,051 | 10.00% |
| Half-yearly | ₹1,62,889 | 10.25% |
| **Quarterly** | **₹1,63,862** | **10.38%** |
| Monthly | ₹1,64,531 | 10.47% |
| Daily | ₹1,64,861 | 10.52% |
| Continuous (theoretical) | ₹1,64,872 | 10.52% |

The diminishing-returns pattern is clear: simple → annual is a huge jump (₹11K extra), annual → quarterly adds ₹2.8K, quarterly → daily adds ₹1K. After daily, more frequency doesn't help meaningfully — you've essentially converged on continuous compounding.

## How tenure compounds the difference

Same ₹1 lakh at 10% quarterly:

| Tenure | Maturity | Interest |
|---|---|---|
| 1 year | ₹1,10,381 | ₹10,381 |
| 3 years | ₹1,34,489 | ₹34,489 |
| 5 years | ₹1,63,862 | ₹63,862 |
| 7 years | ₹1,99,651 | ₹99,651 |
| 10 years | ₹2,68,506 | ₹1,68,506 |
| 15 years | ₹4,39,979 | ₹3,39,979 |
| 20 years | ₹7,20,957 | ₹6,20,957 |
| 30 years | ₹19,21,863 | ₹18,21,863 |

The famous **"Rule of 72"** estimates how long for money to double: 72 ÷ rate ≈ years to double. At 10%, that's 7.2 years; the calculator shows ~7.3 years to actually double quarterly, so the rule is accurate within ±2%.

## When to use which compounding mode

- **Simple interest mode**: short bridge loans, hundi-based business credit, some government bonds with fixed coupon (no reinvestment)
- **Annual**: NSC, KVP, EPF (8.25% in FY 2024-25), PPF (7.10%), Sukanya Samriddhi
- **Half-yearly**: SCSS (Senior Citizens Savings Scheme), some corporate FDs, RBI Floating Rate Savings Bonds
- **Quarterly**: All major Indian bank cumulative FDs, recurring deposits (effectively quarterly with monthly contributions), most NBFC FDs
- **Monthly**: Some NBFC FDs (Bajaj Finance, Mahindra Finance), most savings accounts (interest credited quarterly but computed daily)
- **Daily**: HNI sweep-in deposits, USD/EUR foreign-currency accounts, some corporate treasury products

When in doubt, use **quarterly** — it's the default for almost all retail Indian banking products.

## Frequently asked questions

### Why does my bank's FD show a different number?

A few reasons:

- **Day count convention**: most banks use 365 days; a few use 360 (especially older treasury products) or 365.25 for leap-year adjustment. Tiny but real differences.
- **Compounding start date**: some banks compound from deposit date, others from start of next quarter — affects the first quarter's interest.
- **Interest credit timing**: cumulative FDs compound at end of quarter; non-cumulative pay out and don't compound.
- **TDS withholding**: bank may show net of TDS in maturity preview if your interest exceeds ₹40K (₹50K for seniors).

If your bank's number is more than 0.5% off from this calculator, ask them for the formula. They'll have a one-page disclosure under RBI's transparency norms.

### How is RD (recurring deposit) different?

RD = monthly contributions instead of one-time principal. The math is the future-value-of-annuity formula, not pure compound interest:

`A = R × [(1 + i)^n − 1] × (1 + i) / i`

where R is monthly contribution, i is monthly rate (annual ÷ 4 for quarterly compounding ÷ 3 for monthly equivalent), n is months. Use the [SIP calculator](/investment/sip-calculator/) for RD-style monthly contributions; this calculator is for one-time deposits only.

### What's the difference between APR and APY?

APR (Annual Percentage Rate) = the headline annual rate. APY (Annual Percentage Yield) = the effective rate after compounding. The calculator shows APY as "effective annual yield". A 10% APR compounded quarterly = 10.38% APY. When comparing instruments, **always compare APY**, not APR — that's the only fair comparison.

### Does this work for negative interest rates?

Mathematically yes (rate can be negative), but in practice no Indian instrument has had negative rates. Foreign-currency deposits in EUR or JPY occasionally went briefly negative around 2016-2020. You can plug a negative rate to see the maturity, but it's a curiosity.

### How is compound interest taxed in India?

Same as any interest income — under "Income from other sources" at your marginal slab rate. There are exceptions: PPF, EPF (above 5-year tenure), NSC reinvested interest (reinvested portion is treated as fresh deposit and gets 80C deduction), Sukanya Samriddhi, and life insurance maturity (under 10(10D) conditions) are tax-free. Bank FDs, corporate FDs, NCDs, RDs, savings account interest above ₹10K (₹50K for seniors u/s 80TTB) — all taxed at slab.

### Why does compounding matter so much over decades?

Because the interest itself starts earning interest. After 30 years at 10%, the interest earned on interest exceeds the original principal. The math:

| Year | Principal alone | Compound (10% quarterly) | Interest on interest |
|---|---|---|---|
| 10 | ₹1,00,000 | ₹2,68,506 | ₹68,506 |
| 20 | ₹1,00,000 | ₹7,20,957 | ₹5,20,957 |
| 30 | ₹1,00,000 | ₹19,21,863 | ₹17,21,863 |

In year 30, interest-on-interest is ₹17 lakh out of ₹18 lakh total interest — almost all of it. Einstein's apocryphal quote about compounding being "the eighth wonder of the world" lands better when you actually run the numbers.

### Can I use this for crypto / equity returns?

You can, but be careful about the assumption. Compound interest assumes a **fixed** rate. Crypto and equity returns are volatile — a 12% average return doesn't actually compound at 12% every quarter. The calculator gives you the projection if returns were perfectly steady; reality includes drawdowns and recoveries. For equity goal-planning, the calculator is fine for a back-of-the-envelope estimate, but actual outcomes will sit anywhere in a wide range around the calculated value.

## Sources

- Reserve Bank of India: Master Directions on Interest Rate on Deposits
- Indian Banks' Association: standard compounding conventions for cumulative FDs
- Income Tax Act 1961: Sections 80TTA, 80TTB, 194A
- Government of India small savings notifications (PPF, NSC, KVP, SCSS rates)
