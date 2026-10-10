---
name: editable-port
description: Move all the copy from one Shopify product page/template into another template while keeping the target's styling and theme-editor editability. Use when the user asks for an "editable port" ("do an editable port of X into Y"), or to move a page's words, bullets and sections into another template so they stay editable in the theme editor.
---

# Editable port

"Do an editable port of `<source>` into `<target>`": move every word from the
source page (headings, paragraphs, bullets, reviews, FAQs, stats, prices,
placeholders) into the target product template. The result keeps the
target's look and every word stays editable in the theme editor.

Theme edits reach the store through git only: edit the template JSON, commit,
push. Shopify syncs the branch.

## Procedure

1. **Read the source.** If it's a template of hardcoded sections
   (`sections/<name>-*.liquid`), read each section's markup for the copy.
   List every chunk: eyebrow, heading, paragraphs, lists, stats, charts,
   tables, reviews, FAQs, CTAs, and `[GAP: …]` / `[BRAND]` placeholders.
2. **Inventory the target.** For each section in the target template, list
   its type, its text/image settings and its block types from the section's
   `{% schema %}`. Note which settings are content (text, richtext, image,
   url, product) and which are style (colors, sizes, padding, fonts).
3. **Map** each source chunk to a target section type that can hold it.
   Write the mapping down before editing. If the user also asked for
   **prebuilt only**, load that skill and use its section-choice rules here.
4. **Edit the template JSON with a script.** Hand-editing a 100 KB minified
   template is error-prone.
   - Change content settings only. Keep every style setting as it is.
   - Need more sections than the target has? Deep-copy an existing section of
     the right type (it keeps its styling), with a new section id and new
     block ids.
   - Need more blocks? Copy an existing block of that type as the style
     template, then set its content.
   - Target blocks or sections with no source equivalent: set
     `"disabled": true`. Never delete them.
   - Clear images that belong to the old product (set to `""`). Quantity
     break and similar blocks fall back to the product's own image.
   - Clear a hard-linked product override (e.g. `current_product`) so the
     template shows whichever product it's assigned to.
   - Keep `[GAP: …]` and `[BRAND]` exactly as written.
   - Every word must land in a theme-editor setting. Never hardcode copy in
     `.liquid` files.
5. **Check how the settings render** before relying on them: read the
   section's Liquid for blank checks, `show_*` toggles, schema defaults that
   fill unset settings (e.g. accordion items 5–6), counters that parse
   numbers (a leading `+` or `$` can end up as a suffix), and limits (e.g.
   the comparison table's 3 columns).
6. **Validate.** Run
   `python3 .claude/skills/editable-port/validate_template.py templates/<target>.json`.
   It must report 0 problems, apart from ones that already exist in the
   original template.
7. **Commit and push**, then tell the user:
   - where each source section landed
   - what was hidden
   - anything that didn't fit (dropped table columns, charts turned into
     numbers)
   - which image slots need uploads
