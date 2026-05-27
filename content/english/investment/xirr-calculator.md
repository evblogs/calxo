---
title: "XIRR Calculator: Calculate Mutual Fund XIRR Returns Online (Free)"
description: "Free XIRR calculator for mutual fund SIP investors. Calculate the annualised XIRR return on your SIP portfolio — or enter custom cash flows for irregular investments. No sign-up."
date: 2026-05-27
lastmod: 2026-05-27
type: "calculator"
categories: ["Investment Calculators"]
url: /investment/xirr-calculator/
h1: "XIRR Calculator"
ai_summary:
  - "XIRR is the annualised return on a series of cash flows on different dates — more accurate than CAGR for SIP investments where money is invested gradually."
  - "Enter your monthly SIP amount, how many months you have invested, and your current portfolio value to get your XIRR instantly."
  - "Use Custom Cash Flows mode to calculate XIRR on irregular investments — multiple purchase dates, partial redemptions, or lumpsum + SIP combos."
  - "XIRR above 12% is considered good for an equity mutual fund; PPF gives 7.1% XIRR and long-term Nifty 50 averages around 13%."
  - "XIRR is higher than CAGR for SIP portfolios because not all the money was invested from day one — only the last instalment was at risk for the full period."
faqs:
  - q: "What is XIRR in mutual funds?"
    a: "XIRR (Extended Internal Rate of Return) is the annualised return that accounts for the exact dates and amounts of each cash flow. For SIP investors it is more accurate than CAGR because CAGR assumes a single lumpsum was invested at the start, while XIRR treats each monthly SIP as a separate investment made on its actual date."
  - q: "What is a good XIRR for a mutual fund SIP?"
    a: "For equity mutual funds, an XIRR of 12–15% over 7+ years is considered good. Large-cap or index funds have delivered 12–13% XIRR historically. Mid-cap and small-cap funds can deliver 15–18% in strong bull runs but with higher volatility. Anything below 7% is underperforming PPF, which is risk-free."
  - q: "Why is my XIRR different from CAGR?"
    a: "CAGR treats your entire investment as if it was made on day one. XIRR correctly accounts for the fact that your first SIP instalment has been invested the longest, while your most recent instalment has barely been invested at all. For a growing portfolio, XIRR will usually be higher than CAGR because the earlier, smaller investments have compounded the longest."
  - q: "How is XIRR calculated?"
    a: "XIRR solves for the rate r that makes the Net Present Value (NPV) of all your cash flows equal to zero. Each investment is a negative cash flow and the current portfolio value is a positive cash flow. The calculation uses Newton-Raphson iteration to find the exact annualised rate that satisfies this equation. This calculator does that entirely in your browser."
  - q: "Can XIRR be negative?"
    a: "Yes. If your current portfolio value is less than the total amount you invested, your XIRR will be negative. This means you have lost money in real rupee terms. A negative XIRR of -5% means you are losing about 5% per year on your investment."
  - q: "What is the difference between XIRR and absolute return?"
    a: "Absolute return is simply (current value - invested amount) / invested amount × 100. It does not account for time. XIRR annualises that return, so a 50% absolute return over 3 years is very different from a 50% absolute return over 10 years. XIRR lets you compare returns across different time periods and different investments fairly."
related_calcs:
  - /investment/sip-calculator/
  - /investment/cagr-calculator/
  - /investment/lumpsum-calculator/
  - /investment/step-up-sip-calculator/
---

{{< xirr-calculator >}}

## What XIRR actually means for your SIP

CAGR gets used everywhere in mutual fund marketing. It looks clean: your fund returned 14.2% CAGR over 5 years. But for a SIP investor, that number is misleading. CAGR assumes your entire investment was sitting in the fund from day one. Your SIP wasn't.

Your first ₹5,000 has been compounding for 60 months. Your second ₹5,000 for 59 months. Your most recent ₹5,000 for exactly one month. XIRR handles this correctly by treating each cash flow as a separate investment on its actual date.

This is why XIRR is the only number that matters for SIP performance. AMCs are now required to report XIRR in CAMS and Kuvera statements for exactly this reason.

## XIRR vs CAGR: a quick example

Take a ₹5,000 monthly SIP for 5 years (₹3 lakh invested). If the current value is ₹4.8 lakh, the numbers look like this:

- **Absolute return**: 60% (calculated as 1.8L gain / 3L invested)
- **CAGR**: ~9.9% (treats ₹3L as invested 5 years ago)
- **XIRR**: ~20.4% (correctly accounts for monthly cash flows)

XIRR looks much higher than CAGR here. This is expected, and correct. The average rupee was only invested for about 2.5 years, not 5.

## What counts as a good XIRR

{{< infographic-compare
  left-tag="Risk-free" left-title="PPF / FD" left-num="7–8%" left-label="XIRR benchmark floor"
  right-tag="Equity" right-title="Index fund" right-num="12–14%" right-label="Long-term Nifty 50 average"
  winner="right" winner-text="Equity beats FD/PPF by ~5-6% XIRR over 10+ years" >}}

A simple benchmark: if your equity SIP XIRR is below 10%, you should review the fund choice. Nifty 50 index funds have delivered around 12–13% XIRR over most 10-year rolling periods. Actively managed large-cap funds that charge 1–1.5% expense ratio need to clear at least 13–14% just to justify the fee over an index.

For debt funds: compare against your FD rate. A liquid fund returning 7.5% XIRR when your FD is at 7% is barely worth the complexity.

## How to use the custom cash flows mode

The SIP mode assumes equal monthly investments. If your reality is messier — you missed some months, you added a lumpsum once, or you partially redeemed — use Custom Cash Flows.

{{< infographic-flow
  title="Custom XIRR in 3 steps"
  step1="Switch to Custom Cash Flows tab"
  step2="Enter each investment as a negative amount with its actual date (e.g., -10000 on 2023-06-01)"
  step3="Enter your current portfolio value in the Current Portfolio Value field and calculate" >}}

The calculator adds today's date as the final positive cash flow automatically. Sort your entries by date (oldest first) for the most accurate result.

## Why XIRR can look very high for short-duration SIPs

If you started a SIP 12 months ago and markets have done well, your XIRR might show 40–50%. This looks impressive but it is partly a math artefact. The average investment has only been deployed for 6 months, so even a modest 20% absolute gain annualises to a very high XIRR. Give it 5–7 years before drawing conclusions.

For lumpsum investments, XIRR and CAGR will be identical since there is only one cash flow date.
