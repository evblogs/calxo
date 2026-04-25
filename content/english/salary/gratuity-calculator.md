---
title: "Gratuity Calculator: Payment of Gratuity Act, 1972 (Covered & Non-Covered)"
description: "Free gratuity calculator using the exact formula from the Payment of Gratuity Act, 1972. Computes gratuity for both covered (÷26) and non-covered (÷30) employers, applies the ₹20 lakh tax-free cap, and handles the 6-month rounding rule."
date: 2026-04-25
lastmod: 2026-04-25
type: "calculator"
url: /salary/gratuity-calculator/
keywords: "gratuity calculator, gratuity calculation india, payment of gratuity act, gratuity formula, gratuity tax exemption, calxo"
categories:
- Salary & HR Calculators
author: vignesh
---

The calculator below applies the **Payment of Gratuity Act, 1972** formula and rounding rules. It also distinguishes between covered employers (those with 10+ employees, where the Act applies and the divisor is 26) and non-covered employers (where companies pay gratuity by policy and the divisor is 30).

If you're checking what your employer owes you on resignation or retirement after 5+ years of service, this is the number you should be comparing against the F&F statement. Differences usually come from one of three things: HRA being incorrectly counted in basic, fractional years not being rounded, or the ₹20 lakh tax exemption being applied wrongly.

{{< gratuity-calculator >}}

## How gratuity is calculated

The Payment of Gratuity Act, 1972 (PGA) lays down a single formula for covered employees:

`Gratuity = (Last drawn Basic + DA) × 15 × Years of service ÷ 26`

The 15 represents 15 days' wages for every completed year of service. The divisor 26 represents the assumed working days per month (excluding 4 weekly offs). For employees not covered by the Act, the divisor is 30 instead — a slightly less favourable formula that some non-Act employers (smaller firms, certain service industries) follow voluntarily.

**Salary** for gratuity means **Basic + DA forming part of retirement benefits** only. HRA, conveyance, special allowance, performance bonus and ESOP cash-outs are all excluded. This catches a lot of people because most CTC structures are HRA-heavy and Basic-light.

## Eligibility under the Act

Section 4(1) of the PGA: gratuity is payable on termination of employment if the employee has rendered **five or more years of continuous service**. Termination includes:

- Resignation (after 5 years)
- Retirement / superannuation
- Death (5-year minimum waived; nominee gets gratuity)
- Permanent disability or disablement (5-year minimum waived)
- Retrenchment / redundancy
- Termination by employer (gratuity is payable unless dismissal is for moral turpitude or proven misconduct as per service rules)

Notice period worked counts toward continuous service. Maternity / paternity leave, sick leave (up to limits) and lay-off period also count. Strike days where the strike is held legal also count; illegal strikes don't.

## The 6-month rounding rule

Under the PGA, **fractional years are rounded based on the last incomplete year**:

- **6 months or more** in the last incomplete year → rounded **up** to next full year
- **Less than 6 months** → rounded **down** (truncated)

So 4 years 7 months counts as 5 years (eligible). 4 years 5 months counts as 4 years (not eligible). 8 years 9 months counts as 9 years for gratuity computation; 8 years 5 months counts as 8 years.

The calculator above handles this automatically when you enter fractional years (use 0.5 increments). The bigger gotcha: the rule applies under the Act (covered employers); for non-covered employers, the rounding is usually strict — only completed years count. Check your appointment letter / gratuity policy for the convention if your employer is non-covered.

## Worked example: ₹50,000 basic + DA, 10 years (covered employer)

A typical mid-career resignation case from a 200-employee tech company.

- Last drawn Basic + DA: ₹50,000 per month
- Years of service: 10
- Covered employer (Act applies, divisor 26)

`Gratuity = 50,000 × 15 × 10 / 26 = 50,000 × 150 / 26 = ₹2,88,462`

That's the gross gratuity. Since it's well below the ₹20 lakh statutory cap, the entire ₹2,88,462 is **tax-free** under section 10(10) of the Income Tax Act.

If the same person had served 8 years 7 months, it rounds to 9 years → gratuity = ₹2,59,615. If only 4 years 11 months, rounds to 5 years → ₹1,44,231 (just barely eligible). If 4 years 5 months, rounds to 4 years → not eligible at all under the Act.

## Tax treatment of gratuity

Section 10(10) of the Income Tax Act exempts gratuity up to certain limits:

| Recipient | Tax-free limit |
|---|---|
| Government employees | Fully exempt (no cap) |
| Private sector covered under the Act | Lower of: ₹20,00,000 OR actual gratuity OR (Basic+DA) × 15 × Y ÷ 26 |
| Private sector not covered under the Act | Lower of: ₹20,00,000 OR actual gratuity OR (Basic+DA) × 15 × Y ÷ 30 (and the ten-month-average rule) |

The **₹20 lakh cap** was raised from ₹10 lakh in March 2018 (CBDT Notification S.O. 1213(E)). The cap is **cumulative across employers** — if you've already received ₹15 lakh tax-free gratuity from a previous employer, only ₹5 lakh of the next gratuity is tax-free, regardless of how long you've worked.

For amounts above the cap, the excess is added to your salary income and taxed at your marginal slab. Most senior employees with high basic eventually breach the cap; that's when planning matters.

## When you might breach the ₹20 lakh cap

Roughly when (Basic + DA) × Years of service > ₹34.7 lakh under the covered formula. Examples that breach the cap:

| Last Basic + DA | Years to breach ₹20L cap |
|---|---|
| ₹1,00,000/month | 35 years |
| ₹1,50,000/month | 23 years |
| ₹2,00,000/month | 17 years |
| ₹3,00,000/month | 12 years |
| ₹5,00,000/month | 7 years |

Senior management at large companies routinely cross the cap — the excess gets taxed at 30% + cess. The 2018 amendment raising the cap from ₹10L to ₹20L was overdue; many CHROs argue it should now be ₹40L given salary inflation, but no Bill has been moved.

## Frequently asked questions

### What if my employer says they don't pay gratuity?

If the employer has 10 or more employees (or had 10+ at any point in the preceding 12 months), the **Payment of Gratuity Act applies whether or not the employer wants it to**. Refusal to pay is a violation. File a complaint with the Controlling Authority under the PGA in your state's Labour Commissioner office. Many tech and IT firms try to argue that employees on consultant agreements aren't covered — most of these arguments lose at the Controlling Authority stage if the relationship was effectively employer-employee.

### Is gratuity paid if I'm fired for misconduct?

Section 4(6) of the PGA: gratuity can be **forfeited fully or partially** for termination due to (a) wilful omission or negligence causing damage/destruction (only to the extent of damage caused), or (b) riotous/disorderly conduct, or any act involving moral turpitude in the course of employment. The forfeiture must be proven through the disciplinary process. For ordinary performance-based dismissal, gratuity is still payable.

### What about contract employees and consultants?

The Act covers anyone in continuous employment under an employer, regardless of designation. Most "contractors" who work full-time at an employer's premises with employer-provided tools and direction are legally employees, not consultants — and are covered by the Act. The structure of the contract is less important than the working reality. Several Supreme Court rulings have read into this.

### Does notice period count toward service?

Yes. The notice period is part of your employment. Whether you serve it physically or are paid in lieu, it counts as continuous service for gratuity calculation. If you serve a 90-day notice, your last day at work is 90 days before your separation date — gratuity is calculated on the separation date, including the notice period.

### Can I get gratuity from multiple employers?

Yes — every employer where you complete 5+ years pays gratuity separately. The ₹20L tax exemption is **cumulative** across employers (once you've received ₹20L tax-free in your career, all future gratuity is taxable), but the gratuity itself is paid afresh by each employer.

### What if my employer goes bankrupt?

Gratuity, like other employee dues, has priority status in the liquidation waterfall under the Insolvency and Bankruptcy Code (IBC). Employee dues including gratuity are paid before unsecured creditors. In practice, recovery rates vary — government PSUs almost always pay; private-sector liquidations often recover only partial amounts. Many large employers contribute to a trust managed by LIC's Group Gratuity Scheme, which provides a fund-protected pool independent of the company's solvency.

### Does the calculator account for DA separately?

The calculator's "Basic + DA" field is the combined value. Most private-sector employees in India have Basic-only and zero DA (DA is mostly a public-sector and traditional manufacturing concept). For private sector, just enter your Basic. For PSU / government / older PSE / banking employees, enter the sum of Basic + DA as it appears in your payslip.

### Is there interest on delayed gratuity payment?

Yes. Section 7(3A) of the PGA: gratuity must be paid within **30 days** of becoming due. If delayed beyond that, simple interest is payable from the due date until actual payment, at the rate notified by the Central Government (currently 10% per annum). Most employers settle within 30 days; if yours hasn't, send a written demand letter referencing section 7(3A) — it usually unblocks things.

## Sources

- Payment of Gratuity Act, 1972 (Government of India)
- Income Tax Act 1961: Section 10(10) and CBDT Notification S.O. 1213(E) (2018)
- Ministry of Labour and Employment: Gratuity rules and amendments
- Supreme Court ruling: Continuous service definition and notice period inclusion
