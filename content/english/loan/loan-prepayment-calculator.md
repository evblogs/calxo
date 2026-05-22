---
title: "Loan Prepayment Calculator: Interest Saved & Tenure Reduction"
description: "Free loan prepayment calculator for India. See exactly how much interest you save and how many months you cut off your home, car or personal loan by making one lump-sum prepayment. Works for any bank."
date: 2026-05-23
lastmod: 2026-05-23
type: "calculator"
url: /loan/loan-prepayment-calculator/
keywords: "loan prepayment calculator, home loan prepayment calculator, part payment calculator, loan prepayment interest saved india, home loan part payment benefit"
categories:
- Loan Calculators
author: vignesh
---

Your year-end bonus just landed. Or you sold some equity and have ₹2 lakh sitting idle. The question everyone Googles but most bank relationship managers can't answer clearly: if I dump this into my home loan, how much interest do I actually save?

The calculator below gives you the exact number. Plug in your loan details, your prepayment amount, and when you plan to make it. The result shows interest saved and how many months your loan closes early.

{{< loan-prepayment-calculator >}}

## How prepayment works (and why banks default to tenure reduction)

When you make a part-payment, banks in India do one of two things: reduce your EMI while keeping the same tenure, or keep your EMI the same and reduce the tenure. RBI guidelines give you the right to choose. But most PSU banks (SBI, PNB, Bank of Baroda) default to tenure reduction, and this is almost always the better option financially.

Here is why. Every extra rupee sitting in your outstanding principal is earning 8.5% returns for the bank, guaranteed, risk-free. The tenure-reduction option removes that principal permanently and prevents it from accruing interest for years. EMI reduction just gives you a slightly smaller monthly bill while still leaving most of the principal intact for longer.

This calculator uses the tenure-reduction model because that is the standard for home loans in India.

## The maths behind the result

Standard EMI formula:

`EMI = P × i × (1+i)^n / ((1+i)^n − 1)`

where P = loan amount, i = monthly interest rate, n = total months.

After k EMI payments, outstanding principal:

`Outstanding = P × (1+i)^k − EMI × ((1+i)^k − 1) / i`

Post-prepayment, new principal = outstanding − prepayment amount. New remaining months (same EMI):

`n' = −log(1 − new_principal × i / EMI) / log(1+i)`

Interest saved = (EMI × n − P) − (EMI × (k + n') + prepayment − P)

In plain terms: original total interest minus new total interest (including the prepayment itself).

## Worked example: ₹50 lakh home loan, ₹3 lakh prepayment after 2 years

My colleague Suresh took a ₹50 lakh home loan at 8.5% for 20 years. His EMI is ₹43,391. Two years in, he gets a promotion bonus of ₹3 lakh and puts it entirely into his loan.

| Metric | Value |
|---|---|
| Original tenure | 240 months (20 years) |
| New tenure after prepayment | 207 months (~17 yrs 3 months) |
| Months cut off | 33 months |
| Interest saved | ₹3,96,000 approx |

He paid ₹3 lakh to save ₹3.96 lakh in interest. That is a guaranteed 32% return in nominal terms (tax-free, since it is interest cost reduction, not income). No equity fund promises that.

{{< infographic-stat
  number="₹3.96L"
  label="Interest saved on a ₹50L loan with one ₹3L prepayment at 8.5%"
  sub="And 33 months off the tenure" >}}

## When prepayment makes sense and when it does not

Prepayment is not always the best use of a lump sum. The benchmark is your home loan interest rate after the Section 24(b) tax deduction.

If your loan is at 8.5% and you are in the 30% tax bracket claiming ₹2 lakh interest deduction, your effective loan cost is roughly 8.5% × (1 − 0.30) = 5.95%. An index fund averaging 11–12% over 10+ years handily beats 5.95%. In that case, invest the lump sum rather than prepaying.

If your loan is above 9.5%, you are in the 0% or 5% bracket, or you have already used up your Section 24 deduction, prepaying is almost always better. Guaranteed 9.5%+ return is very hard to beat with any safe investment.

Two other situations where prepayment wins: you are within 5 years of tenure end (principal is nearly zero so prepayment saves disproportionately less, but the emotional freedom matters), and your home loan has a floating rate that keeps rising.

## Part-payment charges to watch out for

Home loans with floating rates cannot attract prepayment penalties under RBI guidelines (circular DBOD.No.Dir.BC.13/13.03.00/2012-13). But watch for:

- Fixed-rate home loans: banks can charge 2–3% of the prepaid amount
- Personal loans: typically 2–5% prepayment penalty regardless of fixed or floating
- Car loans: most private banks charge 5% for foreclosure within the first year, tapering to 2% by year 3

Ask your bank for the exact foreclosure/part-payment fee before you decide. The calculator does not account for these charges, so factor them in when comparing against investing the money instead.

## Frequently asked questions

### Should I make multiple small prepayments or one big one?

One big prepayment earlier beats multiple smaller ones later. The reason: every rupee of principal that is removed early avoids interest for more months. ₹3 lakh at month 12 saves more than three separate ₹1 lakh prepayments at months 24, 36, and 48. Front-load when you can.

### Does the bank recalculate EMI automatically after prepayment?

For tenure-reduction mode: no. Your EMI stays the same. The bank just marks the new lower tenure in their system. You will see fewer remaining EMIs, not a smaller bill.

For EMI-reduction mode: yes, your next statement will show a lower EMI and the same original tenure.

Ask the bank to confirm which mode they applied. Get it in writing or at minimum take a screenshot of your loan statement immediately after the prepayment posts.

### How many prepayments can I make per year?

RBI does not cap the number for floating-rate home loans. Most banks allow multiple per year. Some impose a minimum prepayment amount (SBI requires at least 3 EMIs' worth per transaction). Check your sanction letter for specific conditions.

### What happens if I prepay more than the outstanding principal?

You cannot. The bank will cap the prepayment at the current outstanding principal and return the excess, or apply it toward the next EMI depending on the processing date. The calculator handles this by showing 0 months remaining if your prepayment equals or exceeds outstanding principal.

## Sources

- RBI Master Circular on Interest Rates on Advances (prepayment penalty prohibition on floating rate loans)
- NHB guidelines on housing finance prepayment
- SBI Home Loan product terms and part-payment policy, 2025
