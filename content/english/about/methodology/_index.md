---
title: "Methodology: How Calxo Builds and Verifies Each Calculator"
description: "How Calxo verifies the formula, sources the rates, and reviews each calculator for accuracy. Editorial standards, formula verification process, and the public list of statutes and circulars we cite."
url: /about/methodology/
lastmod: 2026-04-25
---

Every calculator on Calxo follows the same five-step build-and-review process. Here's the full methodology, the sources we cite, and the editorial standards we hold the content to.

## How a Calxo calculator is built

**Step 1 — Identify the underlying statute or industry standard.** EMI uses the reducing-balance formula in the RBI Master Direction on Loans and Advances. HRA exemption follows section 10(13A) read with Rule 2A of the Income Tax Rules. GST follows the rate schedules notified by the GST Council. We start by reading the actual rule, not a fintech blog.

**Step 2 — Verify the formula against three top-ranking sources.** For each calculator we cross-check the math against at least three of: ClearTax, Groww, Income Tax Department, RBI bulletin, EPFO calculator, NHB guidelines, AMFI fact sheet, or the relevant bank's published rate card. If the numbers diverge, we audit the difference and disclose it on the page.

**Step 3 — Build the widget with current 2026 defaults.** Every calculator ships with realistic April 2026 numbers as defaults — current home loan rates (8.5–9.0% range), PPF at 7.1%, equity CAGR around 12%, and the FY 2025-26 income-tax slabs from the Finance Act 2025. The defaults are reviewed each quarter.

**Step 4 — Document the sources at the bottom of the page.** Every calculator page lists the actual statute, master direction, or circular we used. No vague "industry experts" or "as per various sources" — only specific, verifiable references you can look up.

**Step 5 — Re-review every quarter.** Tax rates and small-savings rates change quarterly. Bank lending rates move with the repo rate. We revisit each calculator's defaults at the start of every quarter and update the `Last reviewed` date in the trust banner if anything changed.

## What we will never do

- **Store your inputs.** Every calculation runs in your browser. We don't proxy through a server, we don't log keystrokes, we don't have an analytics event for "user typed ₹X". The math happens locally.
- **Push you toward affiliate products.** Some calculator sites are built by lender marketing teams. Calxo is bank-, AMC-, and broker-agnostic. If we mention a specific bank or fund it's because we're citing a published rate or fact sheet.
- **Hide assumptions.** Every formula is documented on the page. Every default value is explicit. If the math depends on an assumption (e.g., quarterly compounding, end-of-period contribution), we state it.
- **Use AI to generate calculator math.** Static AI summaries on blog posts are clearly disclosed. The calculator JavaScript is hand-written and reviewed.

## Sources we cite (public list)

These are the primary references behind Calxo calculators, with the relevant area in brackets:

- **Reserve Bank of India** — Master Directions on Loans and Advances, Interest Rate on Deposits, Foreign Exchange Management [Loan, FD, Currency]
- **Central Board of Direct Taxes (CBDT)** — Income Tax Act 1961, Finance Act amendments, circulars [Income Tax, Capital Gains, TDS]
- **Goods and Services Tax Council** — rate schedules, notifications [GST]
- **Ministry of Finance** — Public Provident Fund Scheme 2019, NSC, KVP, SCSS quarterly rate notifications [PPF, NPS, small savings]
- **Employees' Provident Fund Organisation (EPFO)** — contribution rates, EPS rules [EPF, gratuity provisioning convention]
- **AMFI (Association of Mutual Funds in India)** — fund classification, performance benchmarks [SIP, lumpsum, ELSS]
- **National Stock Exchange (NSE)** — Nifty rolling-return data [equity return assumptions]
- **State Stamp Acts and Registration Departments** — state-specific rates [Stamp Duty]
- **Payment of Gratuity Act, 1972** — formula, eligibility, ₹20L cap [Gratuity]
- **Bank rate cards** — SBI, HDFC, ICICI, Axis, BoB, LIC HFL, Bajaj Finance [home loan, FD, personal loan, eligibility caps]

When a specific calculator depends on additional sources (e.g., a Supreme Court ruling for HRA, an ITAT precedent for gratuity forfeiture), we add the citation in the "Sources" block at the bottom of that page.

## Who writes and reviews this

Calxo follows a **writer + reviewer** model — the same pattern medical-content sites and reputable finance publications use to keep editorial independent of any single voice.

**Author / writer**: **Vignesh** drafts the calculator pages, blog posts, and methodology updates. He has been writing about Indian personal finance, tax, and consumer banking for 8+ years.

**Editorial reviewer**: **[Prem Anand](https://www.linkedin.com/in/prem-anand-a207771a5/)** reviews each calculator and blog post for accuracy, regulatory currency, and clarity before it goes live. Prem is a BFSI content specialist with 10+ years of experience covering banking, financial services, and insurance, with bylines across **Mint, Moneycontrol, Outlook India, AP News** and other major publications.

Calxo is independent — no investor, AMC, lender or insurer funds the editorial. The "Last reviewed" date in each calculator's trust banner is the date Prem signed off on that page's current state.

For corrections, methodology questions, or rate updates that lag the official notification, email us at the address on the [About page](/about/) — corrections are usually merged within 48 hours, with the `Last reviewed` date updated visibly.

## Setting up feedback collection (internal note)

Negative feedback from the "Was this helpful?" widget and calculator thumbs-down is sent to a Google Sheet via a Google Apps Script web app. Setup steps:

1. **Create a sheet** named `Calxo Feedback` with headers in row 1: `Timestamp | Slug | Reason | Other | URL | Title | User Agent`
2. **Open Apps Script** (Extensions → Apps Script in the sheet)
3. Paste this code and save:
   ```javascript
   function doPost(e) {
     try {
       var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
       var data = JSON.parse(e.postData.contents);
       sheet.appendRow([
         new Date(),
         data.slug || '',
         data.reason || '',
         data.other || '',
         data.url || '',
         data.title || '',
         data.userAgent || ''
       ]);
       return ContentService.createTextOutput(JSON.stringify({ ok: true }))
         .setMimeType(ContentService.MimeType.JSON);
     } catch (err) {
       return ContentService.createTextOutput(JSON.stringify({ ok: false, err: String(err) }))
         .setMimeType(ContentService.MimeType.JSON);
     }
   }
   ```
4. **Deploy → New deployment → Web app**
   - Execute as: **Me**
   - Who has access: **Anyone**
5. Copy the deployment URL (`https://script.google.com/macros/s/.../exec`)
6. Paste into `hugo.toml` → `[params]` → `feedbackEndpoint = "..."`

Until the endpoint is configured, feedback is logged to `localStorage` only (key `cx-feedback-log`, capped at 50 entries) and not transmitted off the device.

## Quarterly review schedule

| Quarter | Items reviewed |
|---|---|
| Q1 (Apr–Jun) | Income tax slabs after Finance Act, small-savings rate notification, EPF rate |
| Q2 (Jul–Sep) | Mid-year repo rate review, bank FD rate cards, capital gains rate stability |
| Q3 (Oct–Dec) | Festival-season home/auto loan rate movements, GST council notifications |
| Q4 (Jan–Mar) | Pre-budget review, expected slab changes, market CAGR assumptions vs realised |

Every page's trust banner shows the date of the last review for that specific calculator.
