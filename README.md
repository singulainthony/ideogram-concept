# One Logo In: an unofficial Ideogram concept

**Unofficial concept by Anthony Carnevale.** This page isn't affiliated with, endorsed by or made by Ideogram, and it uses no Ideogram logos or brand assets.

It's a one-page landing page built as a portfolio piece for Ideogram's *Design Engineer, Brand & Marketing* role. The proof on the page is a real 9-asset campaign that I generated with Ideogram 4.0 reference images for my own business, North York Tech Help.

Live: https://singulainthony.github.io/ideogram-concept/

## What's on the page

1. **Hero + CTA:** "One logo in. A whole campaign out." with a link to try reference images on Ideogram.
2. **The campaign:** all 9 renders at their true aspect ratios. Click one to see its exact prompt and Ideogram's "stays the same" plan.
3. **How I made this:** the prompt agent (Hermes Agent running DeepSeek V4.1 Flash), Ideogram 4.0 with a logo reference, batch variations in ComfyUI, QA notes for the product team, and the ship step.
4. **For teams:** one enterprise pitch slide with speaker notes.
5. **Who made this:** contact details.

## Headline test

| | Headline | Hypothesis |
|---|---|---|
| A (control) | One logo in. *A whole campaign out.* | It names the mechanism, and the proof sheet backs it up right away. |
| B (challenger) | Look like you have a design team. *Even when it's just you.* | It sells the emotional outcome to solo owners and doesn't mention the feature. |

I'd test **B against A**. The primary metric is click-through to Ideogram, with scroll depth to the proof sheet as a guardrail. To preview B, open the page with `?h=b`.

## Build

The page is hand-written HTML, CSS and JS with no framework and no build step. It was built with Claude Code.

```bash
python3 -I tools/prepare_assets.py ~/Downloads/ideogram_download_YYYY-MM-DD   # resize renders, extract prompts → data/assets.json
python3 -m http.server 4410                                                   # preview at http://localhost:4410
```
