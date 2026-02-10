# alexiacob.github.io

Personal research website rebuilt with **al-folio as the core theme**.

## Features
- al-folio-driven site structure and styling.
- Home/About, Publications, CV, Blog, LinkedIn posts, and X posts routes.
- Data-driven publications and CV from `_data/*.yml`.
- Deterministic social post collections:
  - `_linkedin_posts/*`
  - `_x_posts/*`
- RSS feed at `/feed.xml`.

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

## Sync Workflow

Run from the global repo root:

```bash
uv run python scripts/writing/sync_website_content.py \
  --website-dir /Users/iacobalexandru/projects/global/alexiacob.github.io \
  --linkedin-dir /Users/iacobalexandru/projects/global/linkedin_posts \
  --x-dir /Users/iacobalexandru/projects/global/twitter_posts \
  --cv-tex /Users/iacobalexandru/projects/global/alex_iacob_cv/main.tex \
  --build-cv-pdf
```

This synchronizes LinkedIn/X markdown social posts and CV TeX/PDF artifacts.
Each synced post contains an `external_url` front matter field. Add your
public social URL there (for example, the final LinkedIn/X post URL).
