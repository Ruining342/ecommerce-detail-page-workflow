# Lossless Long-Page Assembly

Use this after all pages in a complete detail-page set are generated and approved. The goal is one reproducible long PNG plus the original page PNGs.

## Delivery contract

- Preserve the approved page files as separate deliverables.
- Assemble pages vertically in explicit numeric/content order, from the hero page through the closeout page.
- Use `scripts/stitch_long_page.py`; do not rebuild the long page with Image2, Canva, a design editor, or manual drag-and-drop.
- Apply no resize, crop, gap, padding, filter, color conversion, text change, or redesign.
- Require equal source widths and equal color modes. Fix a mismatched source page instead of normalizing the whole set.
- Do not use an unordered glob as the input list. Resolve and pass every filename explicitly so `第10页` cannot be placed before `第2页`.
- Reject duplicate inputs and missing pages.

## Command

Run from the skill directory with a Python environment that has Pillow. If system Python lacks Pillow, load the bundled workspace dependencies and use their Python executable.

```bash
python3 scripts/stitch_long_page.py \
  --output "/absolute/output/商品详情页_完整长图.png" \
  "/absolute/pages/第1屏_首屏.png" \
  "/absolute/pages/第2屏_卖点.png" \
  "/absolute/pages/第N屏_收尾.png"
```

Use `--overwrite` only when the user authorized replacement or the output is a disposable task artifact being regenerated.

## Required verification

Treat the command as successful only when it exits with code 0 and reports all of:

```text
PAGES=N
SIZE=source_width x sum_of_source_heights
ORDER=1>2>...>N
PIXEL_MATCH=N/N
```

Then confirm the output exists and opens as a PNG. Report the file path, page count, dimensions, and pixel-match result. If verification fails, do not claim the long page is complete.

For a one-page request or an explicitly partial page-generation task, preserve the separate page output and skip automatic assembly. Assemble a partial subset only when the user asks for a combined image of that confirmed subset.
