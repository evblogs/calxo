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
