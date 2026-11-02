# ArtSpark website

Static website for ArtSpark — *Your Trusted Partner in Academic Excellence*.

## Publish

The site is hosted on **GitHub Pages** from the `docs/` folder of the `main` branch. Every push to `main` republishes it within a minute or two.

It is live now at https://isuranga2002.github.io/artspark-website/ while LK Domain Registry activates **artspark.edu.lk** (the DNS records are already saved there). Once the domain is active:

1. Create `docs/CNAME` containing the single line `artspark.edu.lk`, commit and push.
2. In the repo's Settings → Pages, confirm the custom domain shows `artspark.edu.lk`, then tick **Enforce HTTPS** when it becomes available.

To host elsewhere instead, upload everything inside `docs/` to the host's root folder. No server code or database is needed.

Before going live:

1. Open `src/build.py` and check the `CONFIG` block at the top:
   - `site_url` — the real domain (currently `https://artspark.edu.lk`). It is used for canonical links, the sitemap and Google's structured data.
   - `email` — empty means email is hidden on every page. Add one to show it.
   - `social` — add Facebook / Instagram / TikTok links when ready.
2. Run `python3 src/build.py` to regenerate the pages, then commit and push.
3. After launch, add the site to **Google Search Console** and submit `https://<domain>/sitemap.xml`.
4. Create a **Google Business Profile** with the same name and WhatsApp number. This matters most for local search in Sri Lanka.

## Edit

- Text, services, FAQ, history: `src/build.py`, then re-run the build.
- Photos and fonts: add an Unsplash photo id to `PHOTOS` in `src/optimize_assets.py`, run it, then run the build. Images are served as resized WebP from `docs/assets/img`.
- Colours, fonts, layout: `docs/styles.css` (tokens at the top).
- Menu, scroll animations, order form: `docs/site.js`.
- Logo, icons and the social-share image: generated from `src/logo-source.png` by `python3 src/make_assets.py` (needs Pillow).
- Student reviews: add only **real** reviews to the `REVIEWS` list in `src/build.py`. The reviews section appears automatically once the list has entries.

## What's included for SEO

- A unique title, meta description and canonical URL on every page
- Open Graph and Twitter share cards (1200×630 image)
- Schema.org JSON-LD: ProfessionalService, WebSite, BreadcrumbList, Service list and FAQPage
- `sitemap.xml`, `robots.txt`, `llms.txt` (for AI answer engines) and a web app manifest with icons
- A single H1 per page, descriptive alt text, lazy-loaded responsive images with fixed dimensions, a custom 404 page
- Original wording throughout, not copied from Writexel, so neither site is flagged as duplicate content
