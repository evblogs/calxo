---
title: "GST Calculator: Add or Remove GST from Any Amount (India, 2026)"
description: "Free GST calculator with all current Indian slabs (0%, 0.25%, 3%, 5%, 12%, 18%, 28%). Add GST to a base price or extract GST from a tax-inclusive total. Splits into CGST + SGST or IGST automatically."
date: 2026-04-25
lastmod: 2026-04-25
type: "calculator"
url: /gst/gst-calculator/
keywords: "gst calculator, gst calculator india, reverse gst calculator, cgst sgst calculator, igst calculator, gst slab calculator, calxo"
categories:
- GST Calculators
author: vignesh
---

The calculator below handles both directions of GST that small businesses, freelancers and finance teams actually need: **adding GST to a base price** when you're raising an invoice, and **extracting GST from a tax-inclusive total** when a vendor's MRP or invoice already includes it. It also splits the GST correctly into CGST + SGST for intra-state transactions, or IGST for inter-state (B2B between states, or export under LUT).

Pick a slab (most goods and services in India sit at 18%), choose add or remove mode, and you're done.

{{< gst-calculator >}}

## How GST is calculated

GST in India is a destination-based tax with a fairly simple math layer on top:

**Adding GST (forward calculation):**
`GST = Base × Rate / 100`
`Total = Base + GST`

**Removing GST (reverse calculation):**
`Base = Total × 100 / (100 + Rate)`
`GST = Total − Base`

A common mistake on social media and even some calculators: people compute "remove GST" as `Total × Rate / 100`. That's wrong — it gives you GST on the inclusive amount, not the GST that was actually levied on the base. The correct reverse formula uses the `100 / (100 + R)` factor, which the calculator above applies.

## CGST + SGST vs IGST

GST in India is structured as:

- **Intra-state transaction** (buyer and seller in same state): rate is split equally into **CGST** (Central GST, goes to the Centre) and **SGST** (State GST, goes to the state). For an 18% sale, that's 9% CGST + 9% SGST. The buyer sees one combined 18% line on the invoice.
- **Inter-state transaction** (buyer and seller in different states): the full rate is charged as **IGST** (Integrated GST). For an 18% sale, that's a single 18% IGST line. The Centre later devolves the state's share back to the destination state.
- **Union Territory transaction**: replaces SGST with **UTGST**. The math is identical to CGST + SGST.

Practical impact: it changes nothing about the rate you pay, but it changes which GSTIN code goes on the invoice and which input tax credit (ITC) ledger gets used. If you mark intra-state as inter-state on the GSTR-1, you'll have to file a correction — a common error in the first year of GST registration.

## Current GST slabs in India (2026)

The GST Council periodically rationalises rates. As of 2026 the slabs in active use are:

| Slab | Items / services |
|---|---|
| **0%** | Fresh fruit and vegetables, milk, cereals, salt, healthcare and education services, books |
| **0.25%** | Rough diamonds and precious stones |
| **3%** | Gold, silver, jewellery |
| **5%** | Packaged food, footwear under ₹1,000, transport (rail, ride-share), small restaurants |
| **12%** | Apparel above ₹1,000, processed food, business-class air travel, mid-range services |
| **18%** | Most services (telecom, banking, IT, consulting), most consumer goods, restaurants in AC hotels |
| **28%** | Luxury cars, ACs, large TVs, tobacco, aerated drinks, online gaming, premium hotels (₹7,500+/night) |

Plus a **GST compensation cess** on items in the 28% slab (cars, tobacco, aerated drinks). The cess is on top of the 28% and varies by item — small petrol cars get 1%, mid-size cars 17%, large SUVs and tobacco much more. The calculator above doesn't include the compensation cess; you'd add it separately if applicable.

## Worked example: ₹10,000 service invoice at 18%

You're a freelance designer in Karnataka raising an invoice on a Karnataka client.

- Base service amount: ₹10,000
- GST rate: 18%
- Transaction type: intra-state

The math:

| Line | Amount |
|---|---|
| Base | ₹10,000 |
| CGST @ 9% | ₹900 |
| SGST @ 9% | ₹900 |
| **Invoice total** | **₹11,800** |

If the same client were in Tamil Nadu instead, you'd charge IGST 18% = ₹1,800 as a single line. Total still ₹11,800. The customer's input tax credit treatment differs, but for the cash flow it's identical.

## Worked example: extract GST from ₹11,800 inclusive

A vendor sends you a tax-inclusive bill of ₹11,800 and just writes "incl. 18% GST" on it. You need to know the base for accounting.

- Total: ₹11,800
- Rate: 18%
- Base = 11,800 × 100 / 118 = **₹10,000**
- GST = 11,800 − 10,000 = **₹1,800**

If the vendor had divided ₹11,800 by 1.18 they'd get the right answer. If they multiplied ₹11,800 by 18%, they'd get ₹2,124, which is wrong. The reverse-mode toggle on the calculator above is the easiest sanity check.

## When to use the GST calculator

A few real situations where this is the actually useful tool, not a generic "tax tool":

- **B2B invoicing**: confirm CGST/SGST split versus IGST before raising the invoice
- **MRP back-calculation**: figure out the manufacturer's pre-GST price from the printed MRP
- **Quotation review**: a client sends you a number "with all taxes" — you need to back into the base for negotiation
- **Composition scheme reconciliation**: extract base values from inclusive purchase invoices to file GSTR-4
- **Reverse charge mechanism (RCM)**: compute the GST you need to pay yourself on certain notified services
- **Input tax credit reconciliation**: match the GST in your purchase ledger against GSTR-2B

## Frequently asked questions

### What's the difference between GST and VAT?

GST replaced the old layered system of VAT, service tax, excise, octroi, entry tax and a dozen others when it was rolled out on 1 July 2017. VAT existed only at the state level and varied between states; GST is uniform across the country with the CGST/SGST/IGST split handling the federal-state revenue share. For everyday math purposes, GST works just like the old VAT — add a rate, get the total — but the rates and rules are pan-India.

### Why are some items still outside GST?

Petrol, diesel, ATF, natural gas, alcohol for human consumption, and electricity are still outside the GST framework. They're taxed by state governments under separate excise / VAT regimes, which is why fuel prices vary noticeably from state to state while a Maggi packet doesn't. The GST Council has discussed bringing fuel under GST since 2018; no consensus yet.

### Can a small business avoid registering for GST?

Yes, up to a turnover threshold. As of 2026, the threshold for goods is ₹40 lakh annual turnover (₹20 lakh for special-category states), and for services it's ₹20 lakh (₹10 lakh for special-category states). Below that you don't have to register. Above it, you must — even if you choose to charge zero GST under exemption, you still need a GSTIN.

### What is the composition scheme?

A simplified scheme for small businesses (turnover up to ₹1.5 crore) where you pay a fixed flat rate (1% for traders, 5% for restaurants, 6% for service providers) on turnover instead of regular GST. You **can't** charge GST to your customer or claim input tax credit. Mostly used by retailers, small dhabas and manufacturing units that sell directly to end consumers.

### How do I figure out the right GST rate for my product?

Use the HSN code (for goods) or SAC code (for services). Each HSN/SAC has a specific notified rate. The CBIC website at cbic-gst.gov.in has a rate finder. If you're a freelancer or consultant, you're almost certainly at 18% (SAC 9983 / 9985 / 9989 group). If you sell physical products, look up the HSN code first.

### Is there GST on Zomato / Swiggy orders?

Yes. Restaurants charge 5% GST (no input tax credit). Cloud kitchens are typically 18%. The aggregator platforms (Zomato, Swiggy) collect the GST from you on behalf of the restaurant under the e-commerce operator rules. The breakdown shows up on your tax invoice — the calculator above is useful for separating base food cost from GST when you're claiming as a business expense.

### Is GST charged on imports?

Yes — IGST is charged at the customs gateway on the assessable value plus basic customs duty. So an import invoice of ₹1,00,000 with 10% BCD = ₹10,000, then 18% IGST on (1,00,000 + 10,000) = ₹19,800. The IGST is creditable as input tax for businesses; the BCD is not. Use the calculator's "add" mode with ₹1,10,000 and 18% to get the IGST component.

## Sources

- Central Board of Indirect Taxes and Customs (CBIC): GST Rate Schedule 2024 / 2025 update
- Goods and Services Tax Council notifications: latest rate revisions
- ClearTax and Tally Solutions GST documentation
- GST Acts (CGST, SGST, IGST, UTGST), Government of India
