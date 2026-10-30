# Template readiness, 30 October 2026

## Purpose and acceptance

The owner identifies coursegen as a reusable template to standardize authored
courses. The baseline contained only a license.
A dependable first version must create a standalone project without overwriting
existing work, centralize metadata, provide a coherent worked example, and build
usable reader output with reproducible checks.

## Completed

- Standard Quarto structure, title/author/language customization, consistent
  navigation and an explicitly synthetic example. License is copied unchanged;
  authors must review rights for their own content.
- A Python standard-library generator with nonblank metadata, safe YAML quoting
  (JSON-compatible YAML), and refusal of existing or recursive destinations.
- CI creates a fresh example, renders it, checks links and publishes a build
  artifact for review. It performs no site deployment.
- Instructor notes are excluded from the rendered site and search data. Their source is visible to repository readers; confidential material must be stored separately.

## Verification observed locally

Python scaffold tests: 3 passed. Fresh creation and Quarto 1.10.19 rendering
passed. Four rendered HTML pages pass local resource/link/fragment checks.
No instructor directory or answer key is published.
Chromium 153 desktop (1366 px) and mobile (390 px) screenshots were opened and
visually checked; no overflow or page errors on the final run. An initial
course load emitted a transient Popper error; a diagnostic reload and the final
fresh-browser check did not reproduce it. This is not evidence of hosted CI.

Run the README commands, then `python3 scripts/check_render.py PATH_TO_PROJECT`.
Tests and render logs are retained in the workspace audit dated 2026-10-30.

## Roadmap and boundaries

1. Essential creation, rendering and navigation criteria are satisfied locally.
2. Everyday maintenance: keep generator tests and rendered-link checks in CI;
   review the artifact before publication.
3. Add subject-specific chapters/lessons and review authorship, accessibility of
   added media, references and licensing before release.
4. PDF/print styling, LMS export and automated deployment are deferred until a
   concrete target requires them. No deployment or hosted CI result is claimed.
