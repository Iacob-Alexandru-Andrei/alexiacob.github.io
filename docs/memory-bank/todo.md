# TODO

- [ ] Execute dedicated strict template guardrail sync pass for the 22 reported deltas.
  - Anchor: `guardrails/policy.toml`
- [ ] Decide whether to keep or prune currently unused SCSS partials (`_distill.scss`, `_tabs.scss`, `_teachings.scss`, `_typograms.scss`) after visual regression review.
  - Anchor: `assets/css/main.scss`
- [ ] Add CI check that fails when non-minified `assets/js/*.js` files are unreferenced by generated pages.
  - Anchor: `.pre-commit-config.yaml`
