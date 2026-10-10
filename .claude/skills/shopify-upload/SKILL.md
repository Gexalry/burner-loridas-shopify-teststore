---
name: shopify-upload
description: Upload images to the Shopify store's Files and wire them into theme image slots, or make other non-theme store changes (products, pages, policies) through the Shopify Admin API. Use when the user asks for a "shopify upload", to upload images to the store, or to create or edit products, pages or policies.
---

# Shopify upload

**Git vs API:**
- **Online Store (theme) edits:** always through git (commit the template
  JSON, push). Never push theme changes with the Shopify CLI or the Admin
  API.
- **What git can't do:** uploading to Files, products, pages, policies. These
  go through the Admin API.

**Needs:**
- `SHOPIFY_STORE` (e.g. `yth4ru-9g.myshopify.com`) and `SHOPIFY_ADMIN_TOKEN`
  (`shpat_…`) set in the cloud environment's settings. A new session is
  needed after adding them.
- Network access to the store domain and
  `shopify-staged-uploads.storage.googleapis.com`.

Never print, echo or log the token. To check it exists, test only that the
variable is non-empty. Never ask the user to paste it in chat.

## Upload images and wire them in

1. Run `python3 .claude/skills/shopify-upload/upload_files.py <png> [<png> …]`.
   For each file it:
   - creates a staged upload
   - posts the file
   - calls `fileCreate`
   - waits until the file is READY
   - prints `<local file> -> shopify://shop_images/<filename>`

   It was written before a token was available, so on the first real run,
   check the output and fix it if Shopify's API has changed.
2. Set each section's image setting in the template JSON to the printed
   `shopify://shop_images/<filename>` value:
   - `image` for statistics-column and image-with-text
   - `desktop_image` for roadmap
3. Validate with
   `python3 .claude/skills/editable-port/validate_template.py templates/<name>.json`,
   then commit and push.
4. If the file already exists in Files (re-upload), Shopify may rename it with
   a suffix. Always use the filename the script prints.

## Other Admin API work

Use GraphQL at `https://$SHOPIFY_STORE/admin/api/<version>/graphql.json`
with header `X-Shopify-Access-Token`. Confirm with the user before anything
customers would see goes live, such as publishing a product or changing a
policy.

- **Products** (`productCreate`, `productUpdate`): to change which page a
  product uses, set `templateSuffix` (e.g. `default-copy` for
  `product.default-copy.json`). To show the product on the Online Store,
  `publishablePublish` it.
- **Pages:** `pageCreate`, `pageUpdate`.
- **Policies:** `shopPolicyUpdate`.

The app's scopes cover files, products, inventory, publications, pages,
content, legal policies and navigation. Not covered: themes (by design),
orders, discounts.
