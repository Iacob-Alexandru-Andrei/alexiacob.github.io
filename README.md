# alexiacob.github.io

Personal research website rebuilt with **al-folio as the core theme**.

## Features
- al-folio-driven site structure and styling.
- Home/About, Publications, CV, and Blog routes.
- Data-driven publications and CV from `_data/*.yml`.
- CV and publication sync automation from canonical LaTeX + DBLP sources.
- RSS feed at `/feed.xml`.

## Content Editing

Use the focused guide for day-to-day content updates:

- `docs/content-editing.md`

Quick pointers:

- Home copy and CTA order: `_data/home.yml`
- Profile/bio text: `_data/profile.yml`
- Featured paper cards: `_data/featured_publications.yml` and `_data/publication_meta.yml`
- Full publications list: `_bibliography/papers.bib`
- New blog posts: start from `templates/blog-post-template.md` and add files under `_posts/`

## Local Development

Use Homebrew Ruby 3.3 + Bundler 2.3.25:

```bash
cd /Users/iacobalexandru/projects/global/alexiacob.github.io
/opt/homebrew/opt/ruby@3.3/bin/bundle _2.3.25_ install
/opt/homebrew/opt/ruby@3.3/bin/bundle _2.3.25_ exec jekyll serve --host 127.0.0.1 --port 4000 --livereload false
```

Open:

```text
http://127.0.0.1:4000/
```

## CV + Publications Sync

Run locally from the website repo root:

```bash
python3 scripts/sync_cv_and_publications.py \
  --cv-source-file /path/to/Standard_CV_2023/main.tex
```

This updates:

- `assets/cv/main.tex` (canonical LaTeX source copy)
- `_data/cv.yml` (website CV sections generated from LaTeX)
- `_bibliography/papers.bib` (DBLP-backed bibliography with venue-priority dedupe)
- `_data/publication_citations.json` (BibTeX-derived citation strings for homepage cards)

Automation is configured in:

- `.github/workflows/sync-cv-publications.yml`

If `Iacob-Alexandru-Andrei/Standard_CV_2023` is private, set a `CV_SYNC_TOKEN`
repository secret so the workflow can read it.
