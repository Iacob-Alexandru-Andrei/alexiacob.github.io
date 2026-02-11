# Tech Context

- Site stack: Jekyll + `al-folio` remote theme.
- Local authored presentation logic primarily lives in:
  - `_pages/`
  - `_includes/`
  - `_data/`
  - `_sass/` (project partials)
  - `assets/js/` (local setup scripts)
- Current enabled runtime JS surface for generated pages is centered on:
  - `assets/js/theme.js`
  - `assets/js/no_defer.js`
  - `assets/js/common.js`
  - `assets/js/copy_code.js`
  - `assets/js/jupyter_new_tab.js`
- Removed local JS adapters were unreferenced across current generated pages and are covered by upstream theme assets when needed.
