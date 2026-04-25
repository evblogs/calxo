---
title: "FD Calculator: Calculate Fixed Deposit Maturity (Quarterly Compounding)"
description: "Free FD calculator using the standard quarterly compounding that every Indian bank applies. Compare maturity values across SBI, HDFC, ICICI, post office and small finance bank rates with simple, monthly, quarterly and yearly compounding."
date: 2026-04-25
lastmod: 2026-04-25
type: "calculator"
url: /investment/fd-calculator/
keywords: "fd calculator, fixed deposit calculator, fd maturity calculator, sbi fd calculator, hdfc fd calculator, fd interest calculator, calxo"
categories:
- Investment Calculators
author: vignesh
---

The calculator below uses **quarterly compounding** by default — the convention SBI, HDFC, ICICI, Axis, BoB and almost every Indian bank uses for cumulative FDs. You can switch to monthly, half-yearly, annual or simple interest if your specific bank or instrument compounds differently (some corporate FDs and post office schemes do).

For a typical 5-year FD, quarterly compounding adds about 0.2 percentage points to your effective yield over the headline rate. Small but real money on a ₹10 lakh deposit.

{{< fd-calculator >}}

## How FD interest is calculated

The compound-interest formula every Indian bank's FD system uses:

`M = P × (1 + r / n)^(n × t)`

Inputs:

- **P** is the deposit amount (principal)
- **r** is the annual interest rate as a decimal (7% = 0.07)
- **n** is the number of compounding periods per year (4 for quarterly)
- **t** is the tenure in years

Quarterly compounding means interest is calculated and added to the principal every three months, then the next quarter's interest is calculated on the new (higher) base. This is why "compounded quarterly" beats "simple interest" on the same headline rate.

If you've taken a **non-cumulative FD** (interest paid out monthly or quarterly to your savings account instead of being reinvested), there is no compounding — the bank just credits `P × r / n` to your account each period and returns the principal at maturity. Use the simple-interest mode in the calculator for that case.

## Worked example: ₹1,00,000 at 7% for 5 years

A standard ₹1 lakh, 5-year cumulative FD at SBI's 2026 retail rate of 7%.

The math:

- P = 1,00,000
- r = 0.07
- n = 4 (quarterly)
- t = 5
- M = 1,00,000 × (1 + 0.07/4)^20 = 1,00,000 × (1.0175)^20

| Metric | Value |
|---|---|
| Maturity value | ₹1,41,478 |
| Interest earned | ₹41,478 |
| Effective annual yield | 7.19% |

The effective yield (7.19%) is higher than the headline rate (7.00%) because of the quarterly compounding. This is the number to compare across banks if you're shopping for an FD — banks sometimes quote "7.5% simple" which can actually be **worse** than "7.0% quarterly compounded" for longer tenures.

## How compounding frequency affects maturity

Same ₹1 lakh, 7% rate, 5 years, varying compounding:

| Compounding | Maturity | Effective yield |
|---|---|---|
| Simple interest | ₹1,35,000 | 7.00% (flat) |
| Annual | ₹1,40,255 | 7.00% |
| Half-yearly | ₹1,41,060 | 7.13% |
| **Quarterly (most banks)** | **₹1,41,478** | **7.19%** |
| Monthly (some corp FDs) | ₹1,41,763 | 7.23% |

The jump from simple to quarterly is meaningful: ₹6,478 extra on a ₹1 lakh, 5-year deposit. From quarterly to monthly is a much smaller jump — the law of diminishing returns kicks in fast as you shorten the compounding period.

## How tenure scales the effective return

Same ₹1 lakh at 7% quarterly:

| Tenure | Maturity | Interest earned |
|---|---|---|
| 1 year | ₹1,07,186 | ₹7,186 |
| 2 years | ₹1,14,888 | ₹14,888 |
| 3 years | ₹1,23,144 | ₹23,144 |
| 5 years | ₹1,41,478 | ₹41,478 |
| 7 years | ₹1,62,529 | ₹62,529 |
| 10 years | ₹2,00,160 | ₹1,00,160 |

A 10-year FD at 7% **doubles your money**. That's the rule-of-72 in action: 72 ÷ 7 ≈ 10.3 years to double. Useful sanity check whenever a bank quotes you something — divide 72 by the rate to estimate the doubling time, regardless of compounding frequency.

## When FD makes sense in 2026

FD has become less attractive over the last decade as rates have come down and equity options have opened up. But it still has a clean role:

- **Emergency fund**: 3–6 months of expenses parked at a bank you can break the FD with same-day. Yield isn't the goal here; instant liquidity is.
- **Senior citizen monthly income**: senior citizens get an extra 0.50% on most FDs (SCSS gives 8.20% as of April 2026). Combined with the new ₹50,000 80TTB deduction on FD interest, it's a clean post-retirement instrument.
- **Tax-saving FD**: 5-year tax-saver FDs qualify under section 80C up to ₹1.5L. Lower returns than ELSS or PPF, but zero risk and zero lock-in fuss for someone who doesn't want equity exposure.
- **Short-horizon goals (1–3 years)**: equity is too volatile, debt funds have indexation gone, FD wins on simplicity and predictability for fixed-time goals.
- **Rate-cycle peaks**: in 2023–24 when banks were offering 7.5–8.0% on 3–5 year FDs, locking in those rates was clearly better than what we have in 2026.

For long-term (10+ years) wealth-building, FD almost never beats a diversified equity SIP. Run the [SIP calculator](/investment/sip-calculator/) at 12% return for the same 10-year horizon and the difference is roughly 2–2.5x.

## Frequently asked questions

### Is FD interest taxable?

Yes, fully — under "Income from other sources" at your marginal slab rate. There's no special concession for FDs. If your total FD interest income in a year exceeds ₹40,000 (₹50,000 for senior citizens), the bank deducts 10% TDS at source. You can submit Form 15G (or 15H for seniors) to avoid TDS if your total income is below the basic exemption limit. The interest still has to be reported in your ITR — TDS being absent doesn't mean tax-free.

### What's the difference between cumulative and non-cumulative FD?

Cumulative FD reinvests the interest quarterly, you get one big maturity payout at the end. Non-cumulative pays interest to your savings account monthly, quarterly, half-yearly or annually, and returns just the principal at maturity. Total interest earned is slightly less in non-cumulative because there's no compounding on the paid-out interest. Pick cumulative if you're saving for a goal; non-cumulative if you need monthly cash flow (most retirees pick this).

### Are small finance bank FD rates safe?

Up to ₹5,00,000 per bank per depositor, all FDs are insured by DICGC (Deposit Insurance and Credit Guarantee Corporation, an RBI subsidiary). This includes small finance banks (Equitas, Ujjivan, AU, Suryoday etc.) and even cooperative banks. Above ₹5L, the deposit is on the bank's balance sheet — small finance banks have higher default risk than large PSU/private banks, so the 1–1.5% extra rate they offer is compensation for that risk. For amounts above ₹5L, split across two banks if you want to stay fully insured.

### Can I break the FD before maturity?

Yes. Banks charge a penalty of 0.5–1.0% on the rate that was applicable for the tenure actually completed. Example: ₹1L at 7% for 5 years, broken at 2 years — bank applies the 2-year card rate (say 6.5%) minus 1% penalty = 5.5%, recomputes interest. Some banks waive this for senior citizens. Check the FD terms before opening. Tax-saver FDs (5-year 80C) cannot be broken at all — the lock-in is statutory, not just contractual.

### What's better in 2026: FD or debt mutual fund?

FD is simpler and the post-2023 tax change has hurt debt MFs significantly — they're now taxed at slab rate without indexation, just like FD interest. So for taxable accounts in the 30% slab, the post-tax return is roughly similar between a 7% FD and a 7.5% debt fund. FD wins on simplicity and capital protection; debt fund wins if you need flexibility (no fixed tenure, partial withdrawals). For a pure fixed-tenure goal, FD's predictability is hard to beat in 2026.

### Why does the calculator show different results from my bank's number?

A few reasons:

- **Compounding frequency**: most banks use quarterly, but some niche schemes (post office NSC, KVP, corporate FDs from NBFCs) use annual or half-yearly
- **Interest computation method**: SBI uses end-of-quarter compounding; some PSU banks use start-of-quarter; the difference is tiny but real
- **Day-count convention**: a few banks use 365.25 days for leap-year adjustment; most use 365
- **TDS treatment**: bank may show net of TDS in your statement, calculator shows gross

If your bank's number is off by more than 0.5%, ask them for the formula they're using. They're regulated by RBI to disclose this on request.

### Does the calculator work for senior citizen FDs and tax-saver FDs?

Yes — formula is identical. For senior citizen rate, just type the higher rate (typically 0.50% above standard). For 5-year tax-saver FDs, set tenure to 5 and use the bank's tax-saver rate (often slightly lower than the regular 5-year rate; check first). The 80C deduction itself isn't part of this calculator — that goes through the [income tax calculator](/tax/income-tax-calculator/).

## Sources

- Reserve Bank of India: Master Direction on Interest Rate on Deposits
- DICGC (Deposit Insurance Corporation): coverage rules and ₹5L limit
- SBI, HDFC, ICICI, Axis Bank fixed deposit rate cards (April 2026)
- Income Tax Act 1961: Sections 80TTA, 80TTB, 194A (TDS on FD interest)
