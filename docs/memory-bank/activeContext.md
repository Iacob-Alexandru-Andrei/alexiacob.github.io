# Active Context

## 2026-02-11
- Completed a second refactor+compaction pass focused on authored website source.
- Consolidated content architecture around data-driven home/profile/publication metadata and reusable includes.
- Removed unreferenced local feature-adapter JavaScript modules in `assets/js/` while preserving runtime behavior for currently generated pages.
- Verified site generation with `bundle _2.3.25_ exec jekyll build --quiet` after compaction.
- Deferred strict template guardrail sync (22 deltas) to a dedicated pass to avoid mixing policy sync with content-architecture refactors.
