# Progress

## 2026-02-11
- Structural refactor completed for home/updates/social rendering with shared includes.
- Publication data model simplified to:
  - `_bibliography/papers.bib` (bibliography source of truth)
  - `_data/publication_meta.yml` (card metadata)
  - `_data/featured_publications.yml` (ordered homepage pins)
- Content authoring workflow documented in `docs/content-editing.md` with a blog template at `templates/blog-post-template.md`.
- Authored source-code surface reduced by ~30.8% in measured scope (templates + custom SCSS + non-minified local JS):
  - Before: 6615 LOC
  - After: 4575 LOC
  - Delta: -2040 LOC
