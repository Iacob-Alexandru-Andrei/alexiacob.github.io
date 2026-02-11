# Principles

- Keep one source of truth per content domain (bibliography, card metadata, homepage pin order).
- Prefer include-based rendering composition over repeated Liquid blocks across pages.
- Keep homepage copy and CTA wiring data-driven so non-code content edits do not require template rewrites.
- Remove optional feature adapters when corresponding features are disabled and unreferenced in generated output.
- Treat template guardrail synchronization as a separate lane from product/content refactors.
