# Calxo — Project Memory

This file is the canonical state of the Calxo project. It captures what's
built, the conventions to follow, and the patterns that recur across the
site. New sessions (Claude or human) should read this first.

Last reviewed: 2026-04-26.

---

## What Calxo is

A Hugo static site of free Indian personal-finance calculators with
companion blog posts. Live at https://www.calxo.in. Deploy is via
`git push origin master` to a GitHub repo (`evblogs/calxo`); Netlify
auto-builds and ships within ~30 seconds.

Repository root: `/Users/luckychamp/calxo`.
Theme: `gojournal-hugo` (overridden heavily; we mostly use our own layouts).

---

## Site inventory (as of Apr 26, 2026)

### Calculators (24 total, type=calculator in front-matter)

| Section | Slug |
|---|---|
| **Loan** (6) | emi-calculator, foir-calculator, home-loan-eligibility, stamp-duty-calculator, car-loan-calculator, education-loan-calculator |
| **Investment** (7) | sip-calculator, lumpsum-calculator, fd-calculator, rd-calculator, ppf-calculator, nps-calculator, compound-interest-calculator |
| **Tax** (4) | income-tax-calculator, old-vs-new-tax-regime, capital-gains-calculator, tds-calculator |
| **Salary** (4) | hra-calculator, takehome-calculator, gratuity-calculator, epf-calculator |
| **GST** (1) | gst-calculator |
| **Conversion** (1) | currency-converter |

Each calculator = one shortcode at `layouts/shortcodes/<slug>.html` plus
one content page at `content/english/<section>/<slug>.md`. The shortcode
is invoked from the markdown via `{{< slug >}}`.

### Blog posts (6, all FY 2025-26 / 2026 current)

- `old-vs-new-tax-regime-fy-2025-26`
- `sip-vs-lumpsum-india`
- `ppf-vs-elss-80c`
- `how-much-home-loan-on-salary`
- `how-hra-exemption-is-calculated`
- `what-15-lakh-ctc-actually-means` (pillar/hub post bridging Take-Home,
  Income Tax, HRA, EPF, Gratuity calcs)

Every blog post must have:
- Zero em-dashes (verify with `grep -c "—"`)
- ≥1 SVG image at `/static/images/blog/<descriptive-slug>.svg` with full
  descriptive alt text
- `ai_summary` front-matter (5 bullets, rendered as toggle at top)
- `related_calcs` front-matter (≥2 calculator URLs)
- ≥1 inline calculator link in the prose
- Real Indian-context scenario (city, salary band, named person)
- Math verified against the actual calculator widget JavaScript

### Layouts

- `layouts/calculator/single.html` — calculator page (3-col: left category
  nav + content + right calc-sidebar). Includes byline (writer + reviewer),
  trust strip, helpful counter, action bar (👍 👎 🔗 </> 99), Share/Embed/
  Cite tabbed modal, embed CTA.
- `layouts/calculator/single.embed.html` — minimal page used as iframe
  source. Renders just the widget + "Powered by Calxo" footer. Used by
  the embed feature for natural backlinks.
- `layouts/blog/single.html` — blog post (2-col: content + sidebar).
  Includes AI-summary toggle (default open), TOC with active-section
  highlighting + reading-progress bar, byline (writer + reviewer), Share/
  Print/Download action row (icon-on-top, no border, page-count tooltip
  on Download), and "Was this helpful?" widget at the bottom.
- `layouts/blog/list.html` — blog index with topic-themed gradient cover
  cards (Tax = violet, Investing = blue, etc.).
- `layouts/_default/list.html` — calculator section landing pages with
  branded cover cards.
- `layouts/index.html` — homepage with hero search (Google-style live
  autocomplete), 6 category cards, popular-calculator grid, latest blog.
- `layouts/partials/header.html` — sticky header. Single-row layout
  (logo + mega nav + mobile hamburger). ClearTax-style mega menu with
  per-category column groupings and inline SVG icons per calc slug.
- `layouts/partials/feedback-modal.html` — shared "Sorry to hear, what
  went wrong?" modal. Opens on blog "No" button or calculator
  thumbs-down. POSTs to a Google Apps Script web app (URL configured in
  hugo.toml `params.feedbackEndpoint`); falls back to localStorage.
- `layouts/search/list.html` — `/search/` page with Fuse.js fuzzy search
  reading from `/index.json`. Live results, URL-shareable via `?q=`.
- `layouts/about/list.html`, `layouts/privacy-policy/list.html`,
  `layouts/404.html` — static helper pages.
- `layouts/shortcodes/infographic-stat.html` — big-number stat card.
- `layouts/shortcodes/infographic-compare.html` — A vs B card with
  optional winner highlight.
- `layouts/shortcodes/infographic-flow.html` — vertical numbered step
  list (up to 8 steps, "title|description").
- `layouts/shortcodes/infographic-steps.html` — horizontal step row
  (up to 5 steps, with circular icons; available but rarely needed).

### Static assets

- `/static/images/logo.svg` — primary logo
- `/static/images/blog/*.svg` — 12 blog infographics, all kebab-case
  descriptive filenames (e.g. `tax-regime-slabs-fy-2025-26.svg`,
  `ctc-to-take-home-waterfall-15-lakh.svg`)

---

## Conventions and rules

### Writing rules (CLAUDE.md is the canonical source — read that first)

Hard rules:
- **Zero em-dashes (—)**. Use commas, periods, parens, or just remove.
- **No banned AI words**: delve, leverage, tapestry, navigate (verb),
  robust, seamless, comprehensive, in today's, whether you're, dive into,
  let's explore, it's important to note.
- Subheadings are nouns or short phrases, never questions.
- Mix sentence lengths aggressively. Short. Then a longer sentence with
  multiple clauses, a specific number or example, that doesn't end where
  you expect it to.
- Use Indian-English: rupee figures with ₹ and lakh/crore notation;
  occasional Hindi where natural ("SIP karo", "bhai").
- Real scenarios: name a city, salary band, age, situation. Don't write
  about a generic "investor" or "user".
- Internal links: ≥2 calculator links per blog post in the prose body
  (not just the related_calcs sidebar).

### Math accuracy rule (added Apr 26 after a real bug)

If a blog post computes an output that the calculator widget produces
(take-home, EMI, tax, HRA exemption, etc.), the rupee figures in the
prose **must match** what the actual calculator JavaScript computes for
that scenario. Don't copy numbers from a different scenario in another
post.

To verify: open `layouts/shortcodes/<slug>.html`, find the `compute()`
function, plug in the inputs, and walk through. Common gotcha: basic
salary as a percentage of CTC vs annual gross — the take-home calc uses
`Basic = CTC * basicPct`, so on a ₹15L CTC at 50%, basic is ₹7.5L (not
₹6L which would be 50% of ₹12L CTC).

### Design rules

- Brand colours: primary #2563eb, dark #1e3a8a, accent #06b6d4, ink
  #0f172a, text-mid #475569, mute #94a3b8, success #10b981.
- Font: Plus Jakarta Sans throughout (loaded once in head.html, applied
  globally to `html, body, body *` with `!important`).
- Spacing: Hero sections 4rem padding; section gaps 2-3rem; card padding
  1.4rem; form input padding .6rem .8rem.
- Border radius: 14px on cards, 10px on inputs/CTAs, 999px on pills.
- Shadows: subtle 0 4px 14px rgba(15, 23, 42, .08) for cards;
  0 14px 40px rgba(15, 23, 42, .14) for elevated modals.
- Calculator widgets: dark blue gradient result panel
  (`linear-gradient(135deg, #1e3a8a 0%, #2563eb 50%, #06b6d4 100%)`)
  with grid-pattern overlay. White text. Numbers in 2.4rem 800-weight.
- SVG infographics: never decorative — every visual element should
  represent a real number. Bar widths must be proportional to values.
  When changing values, recheck widths.

### URL conventions

- Calculators: `/<section>/<slug>/` (e.g. `/loan/emi-calculator/`)
- Embedded version: `/<section>/<slug>/embed/` (auto-generated by Hugo
  Embed output format)
- Blog: `/blog/<slug>/`
- Methodology: `/about/methodology/`
- Search: `/search/?q=<query>`

---

## Daily content automation

A GitHub Actions workflow (`.github/workflows/daily-content.yml`) runs
daily and generates one blog post from the queue at
`pythonfiles/calxo_content_queue.json`. The generator script is
`pythonfiles/calxo_daily_content.py`.

The auto-generator must satisfy the daily-content checklist in CLAUDE.md
before marking a post `status: done`. Failures should be raised as commit
warnings, not silent skips.

---

## Active integrations

- **Netlify** — hosting and auto-deploy on push to master
- **Google Analytics** — G-11QNFDC0CH (in head.html)
- **Google Search Console** — owned via DNS verification (run
  `pythonfiles/calxo_gsc_index.py` after major releases to push new URLs
  for indexing)
- **Google Apps Script** — feedback endpoint for the "What went wrong?"
  modal (URL goes in `hugo.toml` params.feedbackEndpoint; setup steps
  in /about/methodology/)

---

## Things to do next (open backlog)

- Wire up the Google Apps Script feedback endpoint (currently falling
  back to localStorage only)
- Build NPS Tier I vs Tier II comparison blog post (links to NPS calc)
- Build "How home loan prepayment compares to investing the surplus"
  blog post (links to EMI + SIP + Compound Interest calcs)
- Add Sukanya Samriddhi calculator (small-savings scheme for daughters,
  high search volume during tax season)
- Add 80C deduction stack visualiser shortcode (PPF + ELSS + insurance +
  EPF + home loan principal, showing how to fill the ₹1.5L cap)
- Real image alt-text audit (CLAUDE.md says alt text must be a full
  sentence with the post's main keyword; some older blogs may lag)
- Performance pass: lazy-load below-the-fold SVGs, defer Fuse.js until
  search interaction

---

## Common pitfalls (real bugs caught in past sessions)

1. **Copying numbers between posts without recomputing**: a ₹12L CTC
   example was copy-pasted into a ₹15L CTC post. Always recompute when
   the input scenario changes.
2. **SVG bar widths not matching values**: when the labelled rupee value
   changes, the bar's pixel width must be re-proportioned. Otherwise
   the chart lies visually even if the labels are correct.
3. **Em-dashes leaking back in during rewrites**: easy to type one
   accidentally. Always run `grep -c "—" content/english/blog/*.md`
   after editing and confirm 0.
4. **Empty Hugo nav links**: previously the nav pointed to `/blog/` but
   the content directory was `/post/`. Make sure menu URLs in hugo.toml
   match real content sections.
5. **`.cx-hero` `overflow: hidden` clipped the autocomplete dropdown**:
   the homepage hero originally clipped descendants. Removed the
   overflow and added clip-path on `::before` to keep the grid pattern
   contained.
