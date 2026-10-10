---
name: chart-images
description: Render coded chart images (bar charts, timelines, dot grids, price comparisons) and simple visuals (seals, badges) as transparent PNGs styled to this Shopify theme, for use in a section's image slot. Use when the user asks for "chart images", a chart or graph on the store, or to turn page data into an image.
---

# Chart images

Charts are drawn in code with matplotlib so they can be regenerated when a
number changes. The source of truth is `chart-images/make_charts.py`; each
image is one block in that script.

## Procedure

1. Load the `dataviz` skill for the chart-form and labeling method.
2. Add or edit a block in `chart-images/make_charts.py`, reusing its helpers
   (`clean`, `save`) and constants.
   - **Colors:** theme orange `ACCENT` (`#ff5801`) for the key value only;
     `CONTEXT` gray (`#8c8c8c`) for comparisons; `DARK` and `LIGHT` for a
     third state; `INK` (`#444444`) and `MUTED` (`#666666`) for text. Never
     put text in the series color, except a single headline delta.
   - **Font:** Inter, close to the theme's system sans.
   - **Output:** transparent background, 200 dpi.
   - **Text in the image:** values and axis/category labels only. Titles,
     captions and sources stay in editable section settings.
   - **Scales:** one per panel. Values of very different sizes (e.g. a
     $1,000 shot vs an $8 supplement) go in separate panels, not on one axis.
   - Label every bar with its value.
3. Install matplotlib if needed (`pip install matplotlib`), then render:
   `python3 chart-images/make_charts.py chart-images`
4. **Look at every PNG** (Read the file) and fix label collisions before
   going further.
5. Commit the script and PNGs. Then place each image: use the **shopify
   upload** skill if the store token is available; otherwise send the PNGs to
   the user with a table of which section slot each goes in.

## Existing images

| File | Section slot |
|---|---|
| `glp1-chart-famine-shed-timeline.png` | image-with-text "It isn't a vitamin problem…" |
| `glp1-chart-zepbound.png` | statistics-column "Same drug. Same trials…" |
| `glp1-chart-bmj.png` | statistics-column "The shot. The shed. The numbers." |
| `glp1-chart-trial.png` | statistics-column "100 adults. 90 days…" |
| `glp1-chart-price.png` | image-with-text "Women on GLP-1s already pay…" |
| `glp1-guarantee-seal.png` | image-with-text guarantee |
