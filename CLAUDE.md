# Calxo.in — Project Instructions for Claude

## Site overview
- Hugo static site: free Indian personal finance calculators
- Deploy: `git push origin master` → Netlify auto-deploys
- Base URL: https://www.calxo.in
- Repo: /Users/luckychamp/calxo
- Theme: gojournal-hugo (3-col layout: left nav + content + right sidebar)
- Calculator shortcodes: layouts/shortcodes/
- Content pages: content/english/{section}/
- Blog posts: content/english/blog/
- GSC indexing script: pythonfiles/calxo_gsc_index.py (run after adding new pages)

---

## Blog content writing rules — follow ALL of these every time

These rules exist because AI-generated content scores 100% on AI detectors.
The goal is to write like a knowledgeable human who typed this in one sitting.

### Structure
- Subheadings must be **nouns or short phrases** — never questions
  ✓ "The FOIR formula every bank uses"
  ✗ "What is FOIR and how does it work?"
- Use numbered sections with **prose paragraphs underneath**, not bullet lists
- Vary paragraph length drastically — some 1 sentence, some 6 sentences

### Sentence rhythm (most important)
- Mix sentence lengths aggressively in every paragraph
  Short. Like this. Then follow it with a longer sentence that has multiple clauses, a specific number or example, and doesn't end where you expect it to.
- Never write 4+ consecutive sentences of similar length
- Use passive voice naturally: "is capped at", "is calculated by", "was raised in Budget 2025"

### Word choices
- Repeat the main keyword/topic noun constantly — do NOT swap synonyms
  (AI avoids repetition; humans repeat naturally)
- Drop technical terms (FOIR, CIBIL, TDS, LTCG, 87A) without defining every one
- Mix formal financial terms with casual Indian-English phrases
- Include Hindi words/phrases where natural: "SIP karo", "bhai", salary slabs

### Transitions
- NO transition words: never use "furthermore", "moreover", "additionally",
  "it's worth noting", "it is important to", "in conclusion", "to summarize",
  "when it comes to", "plays a crucial role", "it's crucial", "ensure that"
- Start new paragraphs directly — no connector phrases

### Human voice markers
- Add one real-feeling scenario per post: a specific person, salary, city, situation
  e.g. "My friend Rohit got a ₹3 lakh year-end bonus..."
  e.g. "Someone paying ₹25,000 rent in Bengaluru on ₹15 lakh salary..."
- State opinions directly: "Don't. Seriously." / "I want to flip a table."
- Occasionally repeat the same idea in different words across paragraphs
  (humans do this; AI considers it redundant and avoids it)
- Never define every term introduced — assume some reader knowledge

### What to never do
- No rhetorical questions as paragraph openers
- No parallel bullet lists where every item starts the same way
- No "In this article, we will cover..." meta-references
- No clean 3-part or 5-part structures where every section is same length
- No "plays a key role", "leverage", "delve", "tapestry", "in today's world"

### Punctuation: NO em-dashes (—)
- AI detectors flag em-dashes heavily because models overuse them
- Replace ALL em-dashes with: comma, period, parentheses, or just remove
  ✗ "Banks rarely show that split — and honestly it's the most useful number"
  ✓ "Banks rarely show that split, and honestly it's the most useful number"
- En-dashes (–) for ranges like "10–15%" are fine to keep
- The em-dash character is U+2014, en-dash is U+2013, hyphen is `-`. Different.

### Required: at least one infographic per blog post (image preferred)
Use a real image file. Save at `/static/images/blog/<descriptive-slug>.svg`
or `.png`/`.webp`. Filename and alt text MUST describe the content
specifically — not `image1.png`, `infographic.png`, `chart.png`.

```markdown
![Section 10(13A) HRA exemption formula: minimum of three components](/images/blog/hra-formula-three-components.svg)
```

Good filenames: `foir-cap-by-bank-2026.svg`, `sip-vs-lumpsum-10yr-corpus.png`.
Bad filenames: `infographic.png`, `image1.svg`, `Untitled.png`.

Good alt text: full sentence describing what the image shows + the post's
main keyword. Bad alt text: "infographic", "chart", "image".

Optional: text-based shortcodes for fast in-line callouts (no image hosting):

```
{{< infographic-stat
  number="₹12.75L"
  label="Salaried gross income that pays zero tax under new regime"
  sub="FY 2025-26 onwards" >}}
```
Use after the strongest claim in the intro to anchor the article visually.

```
{{< infographic-compare
  left-tag="Sovereign safe" left-title="PPF" left-num="7.1%" left-label="…"
  right-tag="Equity, market-linked" right-title="ELSS" right-num="12-14%" right-label="…"
  winner="right" winner-text="ELSS wins by ~₹17 lakh post-tax over 15 years" >}}
```
Use whenever the post compares two options side-by-side.

```
{{< infographic-flow
  title="The 30-second decision tree"
  step1="Got a lumpsum sitting in your account?|If no, SIP from monthly salary."
  step2="Is your horizon 7+ years?|If no, debt fund or FD."
  step3="Would a 40% drawdown make you panic-sell?|If yes, STP over 6-12 months."
  step4="Long horizon, won't panic, money ready?|Lumpsum into index or flexi-cap."
>}}
```
Use for decision rules / step-by-step guidance. Up to 8 steps supported.

### Daily-publishing checklist (auto-content generator must satisfy ALL)
Before marking a post as `status: done` in calxo_content_queue.json, the post
must have:
- [ ] Zero em-dashes (—). Run `grep -c "—" <file>` and confirm 0.
- [ ] At least 1 infographic shortcode (stat / compare / flow).
- [ ] At least 3 specific numbers grounded in real Indian context (₹ amounts,
      CAGR percentages, current 2026 rates from RBI/CBDT/AMFI).
- [ ] Original Indian-context scenario (not generic "investor" or "user")
      — name a city, salary band, age, or relatable situation.
- [ ] No banned words (delve, leverage, tapestry, navigate-as-verb, robust,
      seamless, comprehensive, in today's, whether you're, dive into, it's
      important to note).
- [ ] An ai_summary field with 4-5 bullets (rendered as the toggle at top
      of the article).
- [ ] At least 2 outbound internal links to relevant calculators in
      related_calcs and at least 1 link inside the prose body.
- [ ] First paragraph hooks with a real situation, contrarian fact, or
      specific number — not "In this article, we'll cover…"

---

## Calculator development rules

- Each calculator needs: shortcode (layouts/shortcodes/) + content page (content/english/{section}/)
- Content page front matter must include `type: "calculator"` for auto-discovery in sidebar
- Use unique CSS ID per shortcode (e.g. `#cx-pl`, `#cx-bike`) to avoid conflicts
- Slider + number input always paired and synced via syncPair() JS function
- Result panel: dark blue gradient, grid pattern overlay, white text
- Mobile: grid-template-columns collapses to 1fr at 760px
- After adding new pages: update pythonfiles/calxo_gsc_index.py URLS list and run it

---

## GSC indexing
- Script: /Users/luckychamp/calxo/pythonfiles/calxo_gsc_index.py
- Service account: evblog-in@evblogs-url-indexing.iam.gserviceaccount.com
- Credentials: /Users/luckychamp/gojournal/pythonfiles/gsc-key.json
- Run after every deploy that adds new pages

---

## Sidebar broken URL reference (fixed)
- HRA calculator: /salary/hra-calculator/ (NOT /tax/hra-calculator/)
- CTC to In-Hand: /salary/takehome-calculator/ (NOT /salary/ctc-to-in-hand-calculator/)
