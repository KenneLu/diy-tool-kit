# Changelog

Template library own versioning (TEMPLATE-VER), independent of any tool.

## 2026-09-19 (template freeze: sync_check 1.3.0 + three module fixes)

This round closes the "one-of-five" blind spots the conformance audit found, then
freezes the template so the four tools can re-copy in a controlled wave.

- **`sync_check.py` 1.2.0 → 1.3.0** — three blind spots closed (CONFORMANCE §4.1.9):
  1. **Blueprints are no longer skipped wholesale**; compared file-by-file, a lagging
     blueprint now reports `[lag]` (yellow, non-blocking) with `copy VER -> template VER`.
  2. **Layout channel**: any file under `src/modules/<module>/` that shares a name with
     a template file is compared **even without a `TEMPLATE-FROM` header**; a header-less
     mismatch is `[NOHDR]` (yellow). A whole module that was never adopted is
     `[MISSING-MODULE]`, and a file missing from an adopted module is `[MISSING-FILE]`.
  3. `__init__.py` is now compared too. `TEMPLATE-MODULE: <module>` resolution was fixed
     to map `__init__.py` to the template's `__init__.py` (it used to be compared against
     `<module>.py`, producing a false red).
  Default scan is limited to family tools (`src/` + build gate `build.bat`). Yellow labels
  never change the exit code; only undeclared `[DRIFT]` / `[MISS]` do.
- **`modules/*/__init__.py` unified** — `# TEMPLATE-MODULE: <module> | TEMPLATE-VER: <ver>`
  plus `from .<module> import *  # noqa: F401,F403` (CRLF, ASCII-only); each `__init__.py`
  VER mirrors its module's VER. `modules/icons/__init__.py` added.
- **`modules/appconfig/appconfig.py` 1.0.0 → 1.0.1** — removed a self-contradiction:
  `icons.py` 2.0.0 calls `ICON_DRAW(256)` (single arg), but the template documented
  `ICON_DRAW(ctx, size)` and never defined `ICON_ASSET`. Now `ICON_DRAW(size) -> PIL.Image`
  and an explicit `ICON_ASSET = None` (asset wins when set).
- **`modules/tray_kit/tray_kit.py` 2.0.1 → 2.0.2** — user-visible strings in
  `confirm_quit_dialog` / `warn_duplicate_instance` are now injectable
  (`title/body_text/confirm_text/cancel_text/message`) with Chinese defaults, so i18n
  tools satisfy E4-02; an empty `checkbox_text` no longer renders a blank checkbox.
  Backward compatible.
- **`modules/paths/paths.py` 1.1.2 → 1.1.3** — `CONFIG_PATH` can be pinned via
  `<APP_ID-derived>_CONFIG`, delivering what the module README had promised all along
  (CONFORMANCE §4.1.5: the template had regressed against its own blueprint).
- **NEW `ALIGNMENT.md`** — the "one-of-five" convergence table: template-file × four-tool
  matrix, target state / exact location / change list / risk per non-SAME cell, the
  do-not-align list with OVERRIDE wording, and an execution order.
- Module READMEs (`appconfig`, `paths`, `tray_kit`) updated to match the code.

**Cascade (intentional):** `paths` 1.1.3 and `tray_kit` 2.0.2 must be re-copied by the
tools; at the freeze instant dsh/ocx go red by design. The sync wave follows this commit.

## 2026-09-19 (conformance layer added; docs corrected against disk)

Trigger: local-speak2text 1.4.0 could not start at all since 1.2.0 — an illegal
mutex name made the single-instance guard report "already running" on every launch.
Three layers of protection (smoke / gates / review) stayed green because
**nothing said what to check**. This round turns the prose spec into checkable rows.

- **NEW `CONFORMANCE.md`** — 76 numbered atomic clauses × 4 tools status matrix,
  reproducible check command per row, five deep-dive tables (exit / single-instance /
  service hosting / naming / docs), a registry of spec-vs-disk contradictions (§4),
  and a "can be scripted today" checklist (§5.1, C-01..C-20).
- **STANDARDS**: framework header now four documents (README→STANDARDS→CONFORMANCE→REVIEW);
  **A3-03 reversed** — named mutex is adopted (`tray_kit` 2.0.1 already standardised it),
  with two hard rules: name may not contain a second backslash after the `Local\` prefix,
  and **a guard that fails must fail open**; **new D3.1** — diagnostic switches (`--smoke`)
  must not bypass the normal startup path; **new D3.2** — every guard must declare its
  failure direction (family answer: open); B2 registry version for reme-helper 1.2.4→1.2.5.
- **README**: four-piece framework, CONFORMANCE wired into the assembly guide and tree.
- **REVIEW**: T7 row corrected — the claim that l-s2t is the `--quit` blueprint was false
  (no `--quit` on disk); R1 now points at CONFORMANCE §5.1.
- **blueprints.txt**: documents the exemption's blind spot — an exempted blueprint is
  never checked, so template progress leaves it behind silently; each template bump now
  requires the blueprint to answer "follow / not follow" with a REVIEW note.
- **modules/paths/README.md**: corrected — the template does **not** read `<APP>_CONFIG`
  (its own blueprint did; the template regressed). Fix registered as a TODO because it
  must be synced to dsh/ocx in the same batch or sync_check goes red.
- **modules/icons/README.md**: interface table corrected to the actual
  `base_image()` / `make_icons(base_dir)` / `python src/icons.py`.

## 2026-09-18 (standards alignment, no module code changed)

- STANDARDS / README / REVIEW / blueprints updated per user rulings (2026-09-18):
  - **D16 version-tier authority & release cadence** (STANDARDS B3/G3): +0.0.1 AI-tierable
    with per-commit verification; **+0.1 / +1 user-approval only**; batch commits allowed
    for independent changes but a full regression pass is required before version bump +
    push; routine maintenance does NOT release — releases batch up when commits
    accumulate; no unattended "bump + push + release" pipeline (G3 item 6).
  - **B4 principle #3: template-everything, no special cases** — all four tools consume
    templates (`src/modules/<module>/` whole-folder adoption: README + code + `__init__.py`);
    when a tool cannot fit, improve the template's interface/architecture (readability and
    maintainability first) instead of exempting the tool; code/data separation is the floor.
    blueprints.txt is a temporary migration state, list only shrinks.
  - REVIEW: #2 (inline-equivalent modules) and #3 (reme-helper blueprint exemption)
    redirected to the new policy; R3 explicitly includes human regression as the release gate.
  - STANDARDS J pitfalls +3: frozen smoke ≠ dev-mode runnable / commit message ≠ disk fact /
    py_compile catches syntax only.
  - B2 registry versions refreshed to on-disk values.

## 1.0.0

- Initial library: T1 appconfig, T2 paths (with data-root env redirect per F11),
  T3 autostart, T4 update_helper, T5 i18n skeleton, T6 icons, T7 tray_kit,
  T10 sync_check, T12 log_kit, build/release scripts and CI workflow skeletons.
- Blueprints: local-speak2text (mechanisms), reme-helper (tray discipline,
  logging parameters, menu standard D14).
