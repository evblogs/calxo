#!/usr/bin/env python3
"""
Regenerate data/llm-pricing.json for the LLM cost comparison calculator.

This file is the single source of truth for model pricing. To refresh:
  1. Check each provider's official pricing page (URLs in SOURCES below).
  2. Update the PRICES rows (USD per 1M tokens: input, output).
  3. Update FX_USD_INR and bump VERIFIED to today.
  4. Run:  python3 pythonfiles/update_llm_pricing.py
  5. Rebuild the site so the shortcode picks up the new data.

cache_read is auto-derived as ~0.1x of input (the rough cross-provider
convention) unless an explicit value is given as a 4th tuple element.
Open-weight rows hosted on third parties get no batch discount and no
cache discount (cache_read == input).
"""

import json
from pathlib import Path
from datetime import date

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "data" / "llm-pricing.json"

VERIFIED = "2026-06-15"
FX_USD_INR = 86.0

SOURCES = {
    "Anthropic": "https://www.anthropic.com/pricing",
    "OpenAI": "https://openai.com/api/pricing/",
    "Google": "https://ai.google.dev/pricing",
    "DeepSeek": "https://api-docs.deepseek.com/quick_start/pricing",
    "Mistral": "https://mistral.ai/pricing",
    "xAI": "https://x.ai/api",
    "Open-weight": "https://www.together.ai/pricing",
}

# (provider, id, display, input, output[, cache_read][, host])
# input/output are USD per 1,000,000 tokens.
PRICES = [
    ("Anthropic", "claude-fable-5",       "Claude Fable 5",        10.0, 50.0),
    ("Anthropic", "claude-opus-4-8",      "Claude Opus 4.8",        5.0, 25.0),
    ("Anthropic", "claude-sonnet-4-6",    "Claude Sonnet 4.6",      3.0, 15.0),
    ("Anthropic", "claude-haiku-4-5",     "Claude Haiku 4.5",       1.0,  5.0),

    ("OpenAI",    "gpt-5.5",              "GPT-5.5",                5.0, 30.0),
    ("OpenAI",    "gpt-5.4",              "GPT-5.4",                2.5, 15.0),
    ("OpenAI",    "gpt-5.4-mini",         "GPT-5.4 Mini",           0.75, 4.5),
    ("OpenAI",    "gpt-5.4-nano",         "GPT-5.4 Nano",           0.2,  1.25),

    ("Google",    "gemini-3.1-pro",       "Gemini 3.1 Pro",         2.0, 12.0),
    ("Google",    "gemini-3.5-flash",     "Gemini 3.5 Flash",       1.5,  9.0),
    ("Google",    "gemini-3.1-flash-lite","Gemini 3.1 Flash-Lite",  0.25, 1.5),
    ("Google",    "gemini-2.5-flash-lite","Gemini 2.5 Flash-Lite",  0.1,  0.4),

    ("DeepSeek",  "deepseek-v3",          "DeepSeek V3",            0.14, 0.28),
    ("DeepSeek",  "deepseek-r1",          "DeepSeek R1",            0.55, 2.19),

    ("Mistral",   "mistral-large-3",      "Mistral Large 3",        2.0,  6.0),
    ("Mistral",   "mistral-medium-3",     "Mistral Medium 3",       0.4,  2.0),
    ("Mistral",   "mistral-small-3.1",    "Mistral Small 3.1",      0.2,  0.6),
    ("Mistral",   "ministral-8b",         "Ministral 8B",           0.1,  0.1),

    ("xAI",       "grok-4",               "Grok 4",                 3.0, 15.0),
    ("xAI",       "grok-4-fast",          "Grok 4 Fast",            0.2,  0.5),

    # open-weight, hosted on a third party: no batch, no cache discount
    ("Open-weight", "llama-4-maverick",   "Llama 4 Maverick",       0.27, 0.85, None, "Together AI"),
    ("Open-weight", "qwen-3.6-plus",      "Qwen 3.6 Plus",          0.5,  3.0,  None, "Together AI"),
]


def build():
    models = []
    for row in PRICES:
        provider, mid, display, inp, out = row[:5]
        host = row[6] if len(row) > 6 else (row[5] if len(row) > 5 and isinstance(row[5], str) else "")
        explicit_cache = row[5] if len(row) > 5 and isinstance(row[5], (int, float)) else None
        open_weight = bool(host)
        if explicit_cache is not None:
            cache = explicit_cache
        elif open_weight:
            cache = inp            # no cache discount on third-party hosts
        else:
            cache = round(inp * 0.1, 4)
        models.append({
            "provider": provider, "id": mid, "display": display,
            "input": inp, "output": out, "cache_read": cache,
            "batch": not open_weight, "host": host or "",
        })

    return {
        "verified": VERIFIED,
        "fx_usd_inr": FX_USD_INR,
        "fx_note": "USD to INR rate as of %s, approximate. Edit fx_usd_inr to refresh." % VERIFIED,
        "disclaimer": ("List prices per 1M tokens (USD). Cache-read is the discounted rate for "
                       "cached input tokens and is approximate (provider conventions vary, roughly "
                       "0.1x of input for most). Always confirm against the provider's official "
                       "pricing page before relying on these numbers."),
        "sources": SOURCES,
        "models": models,
    }


if __name__ == "__main__":
    data = build()
    OUT.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(REPO)} with {len(data['models'])} models, verified {VERIFIED}.")
