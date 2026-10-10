---
name: prebuilt-only
description: Lay out Shopify page content using only the theme's existing sections, picking the section whose layout fits the content visually, with no custom Liquid. Use when the user says "prebuilt only", asks for visual fixes to a ported or crammed page, or wants a section to look less compact without new code.
---

# Prebuilt only

No custom Liquid of any kind. That means no new or edited `.liquid` sections,
blocks or snippets, and no custom-liquid blocks. Use only the theme's
existing sections, and choose each one because its layout suits the content
visually, not just because it can hold the words. Change content and
content-layout settings (image side, column count) through the template
JSON in git.

## Section choices that work in this theme

| Content | Section | Why |
|---|---|---|
| Long story: eyebrow + heading + several paragraphs | `image-with-text` (subtitle block, heading block, paragraph block) | Paragraphs get 0.5em spacing and the subtitle block works as an eyebrow |
| Numbers with a chart | `statistics-column`: short subtitle, stat blocks, `image` on the right (`image_position_desktop: right`, `image_position_mobile: below`) | Its subtitle has no paragraph spacing, so keep it to one short paragraph |
| Parallel short items (fix cards, claims, trust strip) | `store-features` card grid (`desktop_columns` = item count, up to 5) | Not a narrow list |
| Steps or timeline | `roadmap` (badge, title, description per step) | |
| Comparison | `product-comparison` | Max 3 columns. Cells take a check/cross or text |
| Reviews | `testimonials` | Set `verified: false` unless reviews are real and verified |
| FAQ | `store-faq` | |
| Short centered statement + button (why now, final CTA) | `rich-text` (subtitle, title, subtitle, button) | |
| Story next to a visual (guarantee seal, price chart) | `image-with-text` with the visual in the image slot | |

## Rules

- Alternate image sides between consecutive `image-with-text` sections.
- Charts and simple visuals (seals, badges) become coded images. Use the
  **chart images** skill, then put them in the section's image slot.
- Replaced sections are hidden (`"disabled": true`), never deleted.
- Validate with `python3 .claude/skills/editable-port/validate_template.py templates/<name>.json`
  before pushing.
- Image pickers only take files from Shopify Files. Upload with the
  **shopify upload** skill if the store token is available; otherwise send
  the user the PNGs and say which slot each one goes in.
