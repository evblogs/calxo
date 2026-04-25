---
title: "Currency Converter: Live INR Exchange Rates (USD, EUR, GBP, AED, SGD)"
description: "Free currency converter with live rates for 20+ currencies relevant to Indian users — USD, EUR, GBP, AED, SGD, AUD, SAR, QAR, JPY and more. Updates automatically; falls back to indicative rates if the live source is unreachable."
date: 2026-04-25
lastmod: 2026-04-25
type: "calculator"
url: /conversion/currency-converter/
keywords: "currency converter, usd to inr, eur to inr, aed to inr, gbp to inr, sgd to inr, exchange rate calculator, india, calxo"
categories:
- Conversion Calculators
author: vignesh
---

The converter below pulls live rates from a free public exchange-rate source (open.er-api.com, refreshed daily from interbank quotes). It supports the 20+ currencies that matter most to Indian users — NRIs in the Gulf and Singapore, freelancers paid in USD, importers handling EUR/GBP, students in CAD/AUD, and travellers shopping in JPY/THB.

The rate you see here is the **mid-market reference rate** — what a bank's treasury desk uses for internal pricing. The rate you actually get when you remit money or swipe a card is **mid-market plus a margin** (typically 1-3% spread plus a fixed fee). For real planning, treat the calculator's number as the floor of what your costs could be.

{{< currency-converter >}}

## How currency conversion works in India

Three different rates exist for any currency pair, and most people see at least two of them in the same week:

1. **Mid-market rate**: the midpoint between buy and sell rates on the interbank market. This is what Google, X, Reuters, and the calculator above show. **You don't get this rate** unless you're a bank treasury moving ₹100 crore at a time.

2. **Card / forex card / bank wire rate**: mid-market plus a 1.5-3% margin. This is what shows up on your credit card statement when you pay in foreign currency, on a SBI/HDFC forex card load, or when you wire money via your bank.

3. **Cash / airport rate**: mid-market plus 4-7% margin. The worst rate, used at airport kiosks and small money changers. Avoid unless you have no alternative.

For a ₹83.45/USD mid-market rate:

- A bank wire might cost you ₹85.00 to buy USD (1.9% margin)
- A credit card swipe in USD might bill you ₹85.50 (2.5% margin + ~3.5% foreign currency markup)
- An airport money changer might give you ₹81.00 when you sell USD back (3% margin against you)

The 5-7% gap between best and worst rates is real money on a $5,000 wire — that's ₹25,000-35,000 of difference for the same transaction. The calculator helps you spot when you're being overcharged.

## Common Indian use-cases

**NRI remittance from Gulf / Singapore / US**

If you're sending money to India, the cheapest rates are usually through:

- Wise (formerly TransferWise) for amounts under ₹5 lakh — typically 0.4-0.7% margin
- Remitly, Xoom, and Paytm Forex for promotional rates (sometimes negative spread on first transfer)
- Bank wires (NEFT/SWIFT) — convenient but 2-4% margin and often a fixed fee

For amounts above ₹50 lakh, talk to your bank's NRI relationship manager directly — they negotiate rates for repatriation in tranches.

**Freelancer paid in USD/EUR**

Most freelancers receive payments through Payoneer, PayPal, Wise, or direct USD wire to their NRE/Domestic account. The conversion rate from each is dramatically different:

- PayPal: usually mid-market + 3-4% (worst of the bunch)
- Payoneer: mid-market + 2% + $1.50/withdraw
- Wise: mid-market + 0.5-0.7%
- Direct bank wire: mid-market + 2-3%, plus correspondent bank fees

If you're earning $5K/month freelance, switching from PayPal to Wise saves about ₹2.5L/year in conversion fees.

**Importer paying in EUR/USD**

Forward contracts and limit orders matter more than spot rates. Banks offer forwards locking in a rate for 1-12 months ahead — useful when you've quoted a customer in INR and need to fix the import cost. Rate is typically mid-market plus 2-3% premium per year.

**Travel forex card vs credit card**

For trips to Europe, US, UK, Singapore — load a forex card before departure. Bank-issued forex cards (SBI Multi-Currency, HDFC ForexPlus, ICICI Travel Card) typically charge mid-market + 0.5-1.5% one-time, then no markup at swipe. Compare with a credit card's foreign-currency markup of 3-3.5% per swipe + GST. For a 10-day trip with ₹2L of card spend, the forex card saves ₹4-6K.

## Worked example: $1,000 freelance payment

You earn $1,000 from a US client. Comparing the rate paths:

| Channel | Effective rate | INR you receive | vs mid-market |
|---|---|---|---|
| Mid-market (Reuters) | ₹83.45 | ₹83,450 | — |
| Wise INR account | ₹83.05 | ₹83,050 | −0.48% (₹400 cost) |
| Payoneer + bank withdraw | ₹81.66 | ₹81,660 | −2.14% (₹1,790 cost) |
| Direct USD wire to bank | ₹81.79 | ₹81,790 | −1.99% (₹1,660 cost) |
| PayPal | ₹80.62 | ₹80,620 | −3.39% (₹2,830 cost) |

A freelancer doing $5K/month who switches from PayPal to Wise saves about ₹14,200 every month — ₹1.7 lakh per year. That's free money for one switch.

## Where rates come from (and why they vary)

The "mid-market rate" you see on Google, this calculator, Reuters, and Bloomberg is computed from quotes on the interbank market — the wholesale FX market where banks trade with each other. India's currency market settles primarily through CCIL (Clearing Corporation of India), and rates are continuous through the trading day.

The retail rate banks offer you is set off this mid-market, plus a markup determined by:

- **Volatility**: when INR is moving fast (Election Day, RBI MPC meetings, Fed announcements), spreads widen
- **Amount**: bigger trades get tighter spreads (₹50L+ gets 0.5% margin; ₹50K gets 2-3%)
- **Channel**: airport kiosk pays for rent; online platforms pay almost nothing
- **Liquidity of the pair**: USD/INR is super liquid (low spread); KWD/INR is thin (wider spread)

The calculator shows the mid-market reference. Your actual transaction rate will be 0.5-7% worse, depending on the channel.

## Frequently asked questions

### How fresh are the rates shown?

The live rates come from open.er-api.com which updates daily from interbank reference quotes. The status line under the result shows "Live rates" or "Using indicative rates" depending on whether the live fetch succeeded. If the API is unreachable (rare), the calculator falls back to indicative April 2026 rates so the widget still works.

### Why does the bank's rate differ from this?

Mid-market vs retail spread (explained above). The calculator shows what the wholesale market is doing; banks add a margin for their cost of doing business with you. Always compare a bank's quoted rate against the mid-market and ask why there's a gap. If the gap is more than 2%, ask for a better rate or switch to a fintech remittance platform.

### Are the rates the same as the RBI reference rate?

Close but not identical. The RBI publishes a daily reference rate at 1:30 PM IST based on selected bank quotes. The interbank rate moves continuously through the day; RBI's reference is a snapshot. For tax-related calculations (capital gains on foreign assets, foreign salary attribution), the **SBI TT buying rate** on the relevant date is what most CAs use.

### Which is the best app to send money to India?

For amounts under ₹5L, **Wise** is consistently cheapest. **Remitly Express** and **Xoom** sometimes beat Wise on promotional first-transfer rates but are usually 0.5-1% more expensive on subsequent transfers. **Western Union** and bank wires are 1.5-3% more expensive than Wise. For amounts above ₹25L, talk to your bank's NRI desk directly — they may match or beat fintech rates for relationship-banking customers.

### How is foreign currency taxed in India?

Income from foreign sources (freelance income, foreign salary, foreign rental, foreign dividends) is **taxed at slab rate** as if earned in India. The RBI reference rate (or SBI TT buying rate) on the date of receipt is used to convert to INR for tax computation. Forex gains from holding foreign currency are taxed as **capital gains** if held above 24 months (LTCG, slab + indexation removed post-2023) or as **other income** for shorter holds. Keep records of conversion rates on each receipt date — your CA will need them.

### What's the LRS limit for sending money abroad?

Under the Liberalised Remittance Scheme (LRS), every Indian resident can remit up to **$2,50,000 per financial year** for permitted purposes (education, travel, gifts, investments, property). Above $2,50,000 requires RBI prior approval. The 20% TCS that was introduced in October 2023 applies to LRS remittances above ₹7L per FY (with exceptions for education and medical). The TCS is creditable against your final income tax liability — it's a cashflow burden, not an extra tax.

### Are the GCC currencies (AED, SAR, QAR) pegged?

Yes. The UAE Dirham (AED), Saudi Riyal (SAR), Qatari Riyal (QAR), Omani Rial (OMR), and Bahraini Dinar (BHD) are all **pegged to USD** at fixed rates. The pegs have been stable for decades. Their INR rates therefore move only as USD/INR moves. KWD (Kuwait) is pegged to a basket and floats slightly. So if you're sending money from the Gulf to India, the relevant news is USD/INR, not the local currency.

### Can I trust crypto exchanges for currency conversion?

Technically yes (you can convert via USDT or USDC), but the post-2022 1% TDS on crypto trades and 30% tax on crypto gains makes this an expensive option. There are also frequent banking restrictions on funding crypto exchanges from Indian bank accounts. For genuine remittance, regulated channels (Wise, banks, RBI-authorised dealers) are the right path.

## Sources

- Reserve Bank of India: Foreign Exchange Management Act (FEMA) and LRS scheme rules
- Clearing Corporation of India (CCIL): interbank rate publishing
- open.er-api.com: free public exchange-rate API used by the calculator
- Income Tax Act 1961: Section 90 (DTAA), Section 91 (foreign tax credit), foreign currency conversion rules
