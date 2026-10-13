# Agent instructions: Land Clearing Charlotte

The live site is `charlotte-land-clearing/` (static HTML, deployed at https://landclearingcharlotte.com/).

## Keep `charlotte-land-clearing/sitemap.xml` in sync (required)

Any time you add, delete, rename, or redirect a page, update the sitemap in the same change:

- **Added page** (new folder with `index.html`): add a `<url>` entry with `<loc>https://landclearingcharlotte.com/{slug}/</loc>`, `<lastmod>` (today's date), and `<priority>` (1.0 home, 0.9 core pillars, 0.7 sub-services, 0.6 city pages, 0.5 tips/articles).
- **Deleted or renamed page:** remove or update its `<url>` entry. Never leave a sitemap URL that returns 404.
- **Edited page:** update that page's `<lastmod>`.
- **Do not list** noindex pages or the legal pages (privacy-policy, cookies-policy, terms-and-conditions).
- The `<loc>` must match the page's canonical URL exactly (new domain, trailing slash).

Before finishing, verify that every folder with an `index.html` is in the sitemap (except the excluded legal pages) and that every sitemap URL has a matching page.

Also follow the URL rules in `docs/charlotte-land-clearing-silo-structure.md` when creating pages.
