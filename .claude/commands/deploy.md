# /deploy — Calxo Full Deploy & Verify Workflow

Run this after every `git push` or whenever Netlify shows a build failure.

## What this does (in order)

1. **Local Hugo build** — catch errors before they hit Netlify
2. **Fix common Hugo errors** — Unicode chars, template issues, shortcode bugs
3. **Push & watch Netlify** — poll until READY or ERROR
4. **Verify new pages live** — HTTP 200 check on recently changed files
5. **Report** — summary of what's live, what failed, what needs manual GSC indexing

---

## Step 1 — Run local Hugo build

```bash
cd /Users/luckychamp/calxo && hugo --gc --minify --cleanDestinationDir --baseURL https://www.calxo.in/ 2>&1
```

**If build succeeds** (no ERROR lines, ends with "Total in Xms") → go to Step 3.

**If build errors**, go to Step 2.

---

## Step 2 — Diagnose & fix Hugo build errors

Common Calxo build errors and fixes:

### Unicode characters in shortcode JS
Hugo's template engine processes shortcode files and chokes on non-ASCII chars in JS strings.

**Symptoms:** `unexpected − in expression` or similar parse errors pointing to a `.html` shortcode file.

**Fix:** Search for Unicode minus `−` (U+2212), smart quotes `"` `"`, em-dashes `—`, etc. inside `<script>` blocks in shortcodes. Replace with ASCII equivalents (`-`, `"`, `--`).

```bash
grep -rn "[^\x00-\x7F]" /Users/luckychamp/calxo/layouts/shortcodes/ | grep -v "₹\|–\|×\|°\|·"
```

### ai_summary as list vs string
Blog posts using `ai_summary` as a YAML list break the blog template if the template calls `markdownify` on it directly.

**Symptom:** Error in `layouts/blog/single.html` around `.Params.ai_summary`.

**Fix:** Wrap in `reflect.IsSlice` check (already done in current template). If a new post has `ai_summary:` as a list, ensure the template handles both.

### Smart quotes in shortcode parameters
`{{< calculator ctc="1200000" >}}` with curly quotes breaks Hugo.

**Fix:** Replace `"` `"` with straight `"` in frontmatter/shortcode calls.

```bash
grep -rn '[""]' /Users/luckychamp/calxo/content/ | grep "{{<"
```

### After fixing, rebuild:
```bash
cd /Users/luckychamp/calxo && hugo --gc --minify --cleanDestinationDir --baseURL https://www.calxo.in/ 2>&1 | grep -E "ERROR|Total"
```

Commit the fix, then push.

---

## Step 3 — Push & watch Netlify deploy

```bash
source /Users/luckychamp/gojournal/pythonfiles/.env
until [ "$(curl -s -H "Authorization: Bearer $NETLIFY_TOKEN" \
  "https://api.netlify.com/api/v1/sites/96695ab1-e3a0-4849-9c49-972deb7e2938/deploys?per_page=1" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)[0]['state'])")" = "ready" ]; do
  sleep 5
done
echo "✅ Netlify READY"
```

If it stays in ERROR state, fetch the error:
```bash
source /Users/luckychamp/gojournal/pythonfiles/.env
DEPLOY_ID=$(curl -s -H "Authorization: Bearer $NETLIFY_TOKEN" \
  "https://api.netlify.com/api/v1/sites/96695ab1-e3a0-4849-9c49-972deb7e2938/deploys?per_page=1" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)[0]['id'])")
curl -s -H "Authorization: Bearer $NETLIFY_TOKEN" \
  "https://api.netlify.com/api/v1/deploys/$DEPLOY_ID" \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print('ERROR:', d.get('error_message')); print('STATE:', d['state'])"
```

---

## Step 4 — Verify new pages are live (HTTP 200)

Check recently added/changed pages:
```bash
# Get pages changed in last commit
git -C /Users/luckychamp/calxo diff HEAD~1 --name-only | grep "content/english" | sed 's|content/english||;s|\.md$|/|;s|^|https://www.calxo.in|'
```

Then curl each:
```bash
for url in <urls_from_above>; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "$url")
  [ "$code" = "200" ] && echo "✅ $url" || echo "❌ $code $url"
done
```

---

## Step 5 — Report & next steps

After successful deploy, output:

```
✅ DEPLOYED — Calxo.in
Commit: <hash> <message>
Pages live: X new, Y total
Hugo build: clean
Netlify: READY

New pages for manual GSC indexing (tomorrow after 3:30am IST):
- https://www.calxo.in/...
- https://www.calxo.in/...

Reminder: Manual URL Inspection quota ~10/day. API submissions don't work reliably.
```

---

## Key constants

| Item | Value |
|---|---|
| Repo | `/Users/luckychamp/calxo` |
| Netlify Site ID | `96695ab1-e3a0-4849-9c49-972deb7e2938` |
| Netlify Token | `$NETLIFY_TOKEN` in `/Users/luckychamp/gojournal/pythonfiles/.env` |
| GSC quota resets | 3:30am IST daily |
| GSC indexing | Manual URL Inspection ONLY (API is unreliable) |
| Base URL | `https://www.calxo.in` |
| Shortcodes dir | `layouts/shortcodes/` |
| Content dir | `content/english/{section}/` |
