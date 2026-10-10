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

## Prebuilt only

"Prebuilt only" means: no custom Liquid of any kind (no new or edited
`.liquid` sections/blocks, no custom-liquid blocks). Use only the theme's
existing sections, and pick the one whose layout suits the content visually,
not just one that can hold the words:

- Long story text (eyebrow + heading + several paragraphs) goes in
  image-with-text, which has an eyebrow block and spaced paragraphs. Don't
  cram it into a statistics column subtitle; that subtitle has no paragraph
  spacing, so keep it to one short paragraph.
- Charts become coded chart images (rendered with matplotlib from
  `chart-images/` sources, transparent PNG, theme orange `#ff5801` for the key
  value, grays for comparisons). They go in a section's existing image slot,
  e.g. the statistics column with image on the right and below on mobile.
  Keep chart text to values and axis labels; titles and sources stay in
  editable settings.
- Image pickers only accept files from Shopify Files, so new images are
  committed to `chart-images/` and uploaded by the user in the theme editor.
