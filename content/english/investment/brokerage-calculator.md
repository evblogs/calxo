---
title: "Brokerage Calculator: Zerodha, Upstox, Angel One Equity Brokerage (Free)"
description: "Calculate exact brokerage, STT, GST, exchange charges and stamp duty for delivery, intraday and F&O trades. Supports Zerodha, Upstox, Angel One, Groww and custom rates."
date: 2026-05-28
lastmod: 2026-05-28
type: "calculator"
categories: ["Investment Calculators"]
url: /investment/brokerage-calculator/
h1: "Brokerage Calculator"
ai_summary:
  - "Discount brokers like Zerodha, Upstox, Groww charge zero brokerage on equity delivery. Intraday and F&O are charged at min(0.03%, ₹20) per executed order."
  - "STT is the largest charge on delivery trades: 0.1% on both buy and sell sides. On intraday it drops to 0.025% on sell only."
  - "Full-service brokers (ICICI Direct, HDFC Securities) charge 0.275-0.55% on delivery, often 10-15x more than discount brokers."
  - "GST is 18% on brokerage + exchange transaction charges + SEBI fees, not on STT or stamp duty."
  - "DP charges of ₹15.34 (₹13 + 18% GST + DP fee) apply only on equity delivery sells, not intraday."
faqs:
  - q: "What is brokerage in stock market?"
    a: "Brokerage is the fee your broker charges for executing a buy or sell trade on your behalf. Discount brokers (Zerodha, Upstox, Groww) charge a flat fee: typically ₹20 per executed order or 0.03%, whichever is lower. Full-service brokers (ICICI, HDFC) charge a percentage of trade value, usually 0.25-0.55%."
  - q: "How do I calculate Zerodha brokerage?"
    a: "Equity delivery at Zerodha: zero brokerage. Intraday: min(0.03% of turnover, ₹20) per executed order. Futures: same as intraday. Options: flat ₹20 per executed order regardless of premium. The calculator on this page uses these exact rates."
  - q: "Why are my actual charges higher than just the brokerage?"
    a: "Brokerage is only one component. STT (0.025-0.1% depending on trade type), exchange transaction charges (0.00322% for equity), SEBI charges (₹10 per crore), stamp duty (0.003-0.015%), GST (18% on brokerage + exchange + SEBI), and DP charges (₹15.34 on delivery sells) add up. On delivery, STT alone is often more than 10x the brokerage."
  - q: "Is Zerodha really free for delivery?"
    a: "Yes for the brokerage component. Zerodha, Upstox, Groww, Dhan and most discount brokers charge ₹0 brokerage on equity delivery (NSE/BSE cash market). You still pay STT, exchange fees, stamp duty, GST and DP charges on delivery sells. For a ₹1 lakh delivery trade, total non-brokerage charges typically run ₹125-170."
  - q: "What is DP charges and when does it apply?"
    a: "DP charges (Depository Participant charges) are levied when shares move out of your demat account, which happens on sells of equity delivery only. Zerodha charges ₹13.5 + ₹2 GST = ₹15.34 per scrip per day. It does NOT apply on intraday, F&O, or buys. Sell 5 different stocks on one day, you pay ₹15.34 × 5."
  - q: "How is STT calculated on options?"
    a: "Options STT is 0.1% of the premium turnover on the sell side only. This catches many F&O traders by surprise. If you sell options worth ₹50,000 premium, STT is ₹50. On exercise of in-the-money options, STT is 0.125% of intrinsic value, which is why many traders square off before expiry rather than exercising."
  - q: "Brokerage rules for FY 2025-26"
    a: "STT, exchange charges, SEBI fees and stamp duty rates remain unchanged for FY 2025-26. Stamp duty went uniform across India under the 2020 Indian Stamp (Amendment) Act: 0.015% on delivery buy, 0.003% on intraday/F&O buy. GST stays at 18% on brokerage and applicable charges."
related_calcs:
  - /investment/stock-average-calculator/
  - /investment/dividend-yield-calculator/
  - /tax/capital-gains-calculator/
  - /investment/cagr-calculator/
---

{{< brokerage-calculator >}}

## What you actually pay per trade

Brokerage looks like the big number on your contract note. It isn't. For most discount-broker users, brokerage is the smallest component of total charges. STT, exchange fees, stamp duty, SEBI charges and GST stack up and dominate.

The calculator above accepts any buy/sell price, quantity and broker, and computes every charge separately so you can see exactly where the money goes.

## Zerodha vs full-service brokers

A ₹1 lakh delivery trade (buy ₹100 × 1,000 shares, sell ₹100 × 1,000 shares) breaks down differently across brokers:

{{< infographic-compare
  left-tag="Discount" left-title="Zerodha" left-num="₹0 brokerage" left-label="Total charges ~₹260: STT ₹200, DP ₹15, exchange/SEBI/GST/stamp ~₹45"
  right-tag="Full-service" right-title="ICICI Direct" right-num="₹550 brokerage" right-label="Total charges ~₹810: brokerage at 0.275%, plus all the same statutory charges"
  winner="left" winner-text="Discount brokers save ~₹550 per ₹1 lakh delivery trade" >}}

Active traders making 50-100 delivery trades a year save ₹25,000-50,000 by switching from a full-service to a discount broker. That is real money.

## Why STT bites delivery traders the hardest

STT (Securities Transaction Tax) is the single largest charge on any equity delivery trade in India: 0.1% on both buy and sell sides. On a ₹1 lakh round trip, that is ₹200 of STT alone, more than the entire brokerage at a full-service broker.

Intraday traders escape this. STT on intraday is only 0.025% on the sell side, meaning a ₹1 lakh intraday trade costs ₹25 in STT vs ₹200 on delivery. This 8x difference is one of the reasons why intraday remains popular despite the higher risk.

## The hidden ₹15.34 on every delivery sell

DP charges are a quiet drain on small delivery sells. Zerodha charges ₹13.5 + ₹1.84 GST = ₹15.34 per scrip every time you sell from delivery, regardless of trade size.

This means a small ₹2,000 delivery sell on 5 stocks costs you ₹76.70 in DP charges alone, before brokerage or STT. The fee is flat per scrip per day. Investors with small portfolios (under ₹20,000 per stock) feel this disproportionately.

Workaround: Some brokers (Dhan, Sky, mStock) waive DP charges entirely. Worth checking if you trade small delivery quantities often.

## F&O charge structure

Futures and options have very different charge profiles from equity:

| Charge | Equity Delivery | Equity Intraday | Futures | Options |
|---|---|---|---|---|
| Brokerage (Zerodha) | ₹0 | min(0.03%, ₹20) | min(0.03%, ₹20) | flat ₹20 |
| STT | 0.1% buy + 0.1% sell | 0.025% sell only | 0.02% sell only | 0.1% premium sell |
| Exchange charge | 0.00322% | 0.00322% | 0.00173% | 0.0353% |
| Stamp duty | 0.015% buy | 0.003% buy | 0.002% buy | 0.003% buy |

Options trading carries the highest exchange transaction charge by far: 0.0353% on premium turnover, more than 10x equity's 0.00322%. On a ₹1,00,000 premium options sell, exchange charge alone is ₹353.

## Choosing a broker by trade type

If you do mostly equity delivery: Zerodha, Groww, Dhan are nearly identical. Pick on app quality.

If you do intraday: Zerodha and Upstox have the cheapest combined charge structure once you account for the ₹20 cap.

If you do F&O regularly: Zerodha (₹20 flat options brokerage) wins for high-volume option traders. Upstox matches on ₹20 cap but charges 0.05% on intraday.

If you do investment-only delivery (1-2 trades per quarter): Full-service brokers might be acceptable because the brokerage difference is irrelevant at low frequency, and you get research and advisory.

## Capital gains tax: the after-tax view

The brokerage calculator above shows pre-tax P&L. For a complete picture, equity delivery profits trigger capital gains tax separately:

- **Short-term capital gains (held under 12 months):** 20% (post-Budget 2024)
- **Long-term capital gains (held 12+ months):** 12.5% on gains above ₹1.25 lakh per year (post-Budget 2024)

Intraday profits are taxed as business income at your slab rate, not capital gains. F&O profits are also business income. Use the [capital gains calculator](/tax/capital-gains-calculator/) for after-tax math on your delivery trades.

## A note on contract notes

Brokers send a daily contract note (PDF) that itemises every charge for every trade you did that day. Compare your calculator output to the actual contract note to confirm accuracy. Small discrepancies are usually due to rounding of paise on exchange charges and SEBI fees.

If you spot a large discrepancy, check whether the trade was executed in multiple orders (multiple ₹20 brokerages) or whether there was a partial fill. Both can change the total.
