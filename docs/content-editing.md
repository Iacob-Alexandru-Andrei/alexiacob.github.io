# Content Editing Guide

## Home page and bio copy
- Edit `_data/home.yml` for hero text, CTA order, featured card count, and updates section copy.
- Edit `_data/profile.yml` for profile/about information used by `/about/`, `bio.txt`, and `cv.json` exports.

## Social and contact links
- Edit `_data/social_links.yml`.
- Keep each `id` stable because home page CTA buttons reference these ids.

## Publications and paper cards
- Full bibliography source: `_bibliography/papers.bib`.
- Homepage featured order: `_data/featured_publications.yml`.
- Card text/badges/links: `_data/publication_meta.yml`.

## Blog posts
- Start from `templates/blog-post-template.md`.
- Create a new file in `_posts/` named `YYYY-MM-DD-your-slug.md`.
- Posts automatically appear in `/blog/` and `/updates/`.

## News and social streams
- News items: `_news/*.md`.
- LinkedIn mirror entries: `_linkedin_posts/*.md`.
- X mirror entries: `_x_posts/*.md`.
- Add `external_url` in front matter when you have the final public post URL.

## Validate before publishing
```bash
bundle exec jekyll build --quiet
```
