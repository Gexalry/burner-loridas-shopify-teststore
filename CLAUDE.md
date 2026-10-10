# Theme notes

## Editable port

"Do an editable port of `<source>` into `<target>`" means: move all the copy
(headings, paragraphs, bullets, reviews, FAQs, stats, prices) from the source
page into the target product template, keeping the target's look and
editability.

- Use only the target template's existing section and block types, and keep
  their style settings (fonts, colors, sizes, padding). Change content
  settings only.
- When the source has more sections than the target, duplicate an existing
  section of the right type (keeping its styling) rather than writing new
  Liquid.
- Every word must end up in a theme-editor setting. Don't hardcode copy in
  `.liquid` files.
- Hide (`"disabled": true`) target blocks/sections that have no source
  equivalent instead of deleting them.
- Clear images that belong to the old product, so the editor shows an empty
  image slot.
- Keep placeholders like `[GAP: ...]` and `[BRAND]` as-is.
- Validate every setting/block id against the section `{% schema %}` before
  pushing.

Charts become stat blocks or text, since the theme has no chart section.
