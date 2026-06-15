---
title: "LLM Cost Calculator: Compare API Pricing Across Models (2026)"
description: "Free LLM API cost calculator. Compare token pricing for Claude, GPT, Gemini, DeepSeek, Mistral, Grok and open-weight models side by side. Enter your tokens and request volume, see cost per request and per month in USD or INR."
date: 2026-06-15
lastmod: 2026-06-15
type: "calculator"
url: /business/llm-cost-calculator/
keywords: "llm cost calculator, llm api pricing calculator, token cost calculator, openai vs claude pricing, gpt vs gemini cost, llm pricing comparison, ai api cost calculator, cost per million tokens"
categories:
- Business Calculators
author: vignesh
---

Two models can do the same job and bill you 50 times apart for it. The same summarisation task that costs about ₹0.005 a call on Gemini Flash-Lite runs closer to ₹0.25 a call on a frontier model, and at a few million calls a month that gap is a real line item, not a rounding error.

The calculator below takes your token sizes and monthly volume and prices the workload across every major model at once, sorted cheapest first. Switch between USD and INR, and open the advanced panel to factor in prompt caching and batch mode.

{{< llm-cost-calculator >}}

{{< infographic-stat
  number="up to 50×"
  label="Cost spread between the cheapest and priciest model for the same workload"
  sub="Input + output token pricing, 2026 list rates" >}}

## How LLM API pricing works

Almost every API prices per **million tokens** (often written $/MTok), and it charges **input and output separately**. Input is everything you send: the system prompt, the conversation history, the user's question, any documents pasted in. Output is only what the model generates back.

Output is the expensive side. Most models charge 4 to 6 times more per output token than per input token, because generating tokens is more compute-heavy than reading them. Claude Opus 4.8 sits at $5 input and $25 output. GPT-5.4 is $2.50 and $15. So a workload that reads a lot and writes a little (classification, extraction, routing) is cheap, while one that writes long responses (drafting, code generation, agents) is where the bill grows.

A token is roughly **0.75 of an English word**, or about 4 characters. So 1,000 words is close to 1,333 tokens. The calculator has a Words option if you would rather think in words than tokens.

## Input tokens versus output tokens

The split matters more than the headline rate. Take a support bot that ingests a 3,000 token knowledge-base chunk plus a short question, then replies in 150 tokens. That is 3,000-ish input and 150 output per call. On a model priced at $1 input and $5 output, input dominates the cost even though output is dearer per token, because there is so much more of it.

Flip it for a code-generation tool: a 500 token prompt that produces a 4,000 token file. Now output is the whole bill. The cheapest model for the support bot may not be the cheapest for the code tool. Run both shapes through the calculator and the ranking can reorder.

## Prompt caching and batch mode

Two levers cut the bill without changing models, and the advanced panel models both.

**Prompt caching** stores a stable prefix (a long system prompt, a fixed document) so repeat requests are not re-charged at full input rate. The cached portion bills at the model's cache-read rate, which is roughly a tenth of the normal input rate for most providers. If 80% of your input is a fixed prompt sent on every call, caching that 80% is close to a 70% cut on input cost. Set the cached share slider to model it.

**Batch mode** trades speed for price: submit requests as a batch, accept a turnaround of up to 24 hours, and most providers knock 50% off both input and output. Good for overnight jobs, evals, and bulk processing. Useless for anything a user is waiting on. Open-weight models hosted on third parties usually do not offer a batch discount, so the toggle only applies where it is real.

## A worked example

Say you run a document-summarisation feature: 4,000 input tokens, 600 output tokens, 200,000 requests a month.

On **Gemini 3.1 Flash-Lite** ($0.25 in, $1.50 out): each call is (4,000 ÷ 1,000,000 × $0.25) + (600 ÷ 1,000,000 × $1.50) = $0.001 + $0.0009 = $0.0019. Across 200,000 calls, about **$380/month**.

On **Claude Opus 4.8** ($5 in, $25 out): each call is $0.02 + $0.015 = $0.035, so about **$7,000/month** for the identical workload.

Same feature, an 18× gap. Now add 75% prompt caching on the input (the summarisation instructions are fixed) and the cheaper model drops further. The point is not that the flagship is overpriced, it is that you should match the model to the job, and the calculator makes that ranking obvious in one screen.

## Picking the right model, not just the cheapest

Price is one axis. A model that is a tenth the cost but needs two retries to get a usable answer is not actually cheaper. The honest workflow: shortlist 2 or 3 models that clear your quality bar on a real sample of your own prompts, then use this calculator to rank those on cost. Do not pick purely on the table, and do not pick purely on benchmarks.

For agent and tool-use workloads, output token counts balloon because the model reasons across many steps, so the output rate matters far more than for a single-shot call. For high-volume, low-stakes classification, a budget model at output rates under $1/MTok will usually win outright.

## Frequently asked questions

### Why is my actual bill higher than the calculator shows

Three usual reasons. Your real input is bigger than you think once you count the system prompt and conversation history on every turn. Reasoning models emit hidden thinking tokens that are billed as output. And retries, failed calls, and tool-call round trips all add tokens the napkin maths skips. Treat the calculator as the floor, then pad for overhead.

### Are these prices current

Prices were verified on the date shown under the calculator, against provider pricing pages. LLM pricing changes often, new models land monthly, and old ones get repriced. Check the provider's official page before you commit a budget. The numbers here are stored in one data file on the site and refreshed periodically.

### How accurate is the words to tokens conversion

The 1.33 tokens-per-word figure is a solid average for English prose. Code, JSON, and non-English text tokenise differently, sometimes much higher. For a real estimate, count tokens with the provider's own tokenizer rather than relying on a word multiplier.

### Does the INR figure use a live exchange rate

No. It uses a fixed USD to INR rate stored with the pricing data and shown beneath the calculator. Currency moves daily, so treat the rupee figure as indicative. The USD figure is the one providers actually bill in.

### What about fixed or monthly fees

This calculator covers usage-based token pricing only, which is how the major APIs bill. Some providers add seats, throughput commitments, or minimum spends on enterprise plans. Those are separate from per-token cost and not modelled here.

## Related calculators

- [ROI Calculator](/business/roi-calculator/) - work out the return on an AI feature against its running cost
- [Gross Margin Calculator](/business/gross-margin-calculator/) - see how inference cost eats into per-unit margin
- [Break-Even Calculator](/business/break-even-calculator/) - find the volume where an AI product pays for itself
- [CAC Calculator](/business/cac-calculator/) - factor AI support costs into customer acquisition
- [MRR Calculator](/business/mrr-calculator/) - track the recurring revenue your AI feature drives

## Sources

- Provider list pricing pages: Anthropic, OpenAI, Google Gemini, DeepSeek, Mistral, xAI, and Together AI, verified on the date shown in the calculator
- Token convention: 1 token is approximately 0.75 English words, or about 4 characters
- Batch pricing: most first-party APIs offer a 50% discount on batch (asynchronous) processing
- Prompt caching: cached input tokens bill at a reduced cache-read rate, roughly a tenth of the standard input rate for most providers
