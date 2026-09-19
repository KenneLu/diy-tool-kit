# Changelog

Template library own versioning (TEMPLATE-VER), independent of any tool.

## 2026-09-19 (arbitration rule + update_helper rewritten to reme semantics, 1.1.0 → 1.3.0)

The user set the rule for common-module conflicts, and it immediately changed a verdict:
**when versions of a shared module disagree, reme-helper's implementation is the standard —
not whichever version has more adopters, because everyone can be wrong together.**

- **STANDARDS B4 gained the arbitration rule with its rationale.** "Majority" is a
  *bogus judge* here, for a structural reason: this family distributes by **copying files**,
  not by resolving dependencies. A defect written into the template is copied verbatim by
  every tool that adopts it, so the more it spreads, the more it looks like consensus —
  counting adopters means **certifying a mistake by its own propagation range**. The only
  valid judge is *has it been verified end to end*: reme's update chain has shipped
  releases, replaced real installations and handled rollback; the template's 1.0.x was a
  **synthetic** implementation that had never been run once — while dsh/ocx had adopted it.
  Deviation from reme is still allowed (premise ② of the "allowed inconsistency" rules),
  but the burden of a *verifiable* better reason lies with the deviating side; the rule
  also requires the verdict to be mechanised where possible (C-21 came from reme's correct
  shape — no mutable globals copied into the package namespace).
- **`modules/update_helper/` rewritten to reme semantics, contract unchanged** (`1.1.0 →
  1.3.0`). 1.2.0 had already ported waiting/limit/backup/`/purge`/sweep/quota-hint; a full
  read of reme's bat (this time reading it *whole*) showed the template was still missing
  **the entire failure path**, so 1.3.0 adds:
  * **snapshot before the copy, rotated to backup only after a copy that succeeded** —
    1.2.0 deleted the old backup *before* the new files landed, i.e. it tore down the
    rollback source first;
  * **`robocopy` rc is checked (>=8 = failure)**: on failure **never start the new exe**,
    restore from the snapshot and start the previous version; if the restore also fails,
    **start nothing**, keep the snapshot for manual recovery;
  * **failure marker** (`update.failed`) + `pop_failed_update_note()`, read once on next
    startup — the tray is already gone, so the next start is the only chance to speak;
  * **sha256 missing is a failure too** (`verify_zip_sha256`, fail-closed). 1.2.0's
    "no `.sha256` file, skip verify" was a **silent pass**, which reme already classifies
    as a security gap. All four tools' `release.yml` upload `.zip.sha256`, so no update
    breaks.
  `check_update` / `download_and_prepare` signatures are unchanged — dsh/ocx call sites
  need no edit (they do need the new startup calls, see below).
- **`sync_check.py` 1.5.0 — `--selftest` gains group E**: 17 positive assertions on the
  generated `.bat` (wait loop, no pipe, limit, snapshot-before-copy, rc check, restore,
  marker, cleanup, ASCII-only) plus a **reverse** sample (the old synthetic shape) that
  must be *reported as missing* — otherwise the assertions could pass vacuously. Two
  harness lessons are recorded in the docstring: the script body contains **cmd variables**
  (`%WORK%`, `%FAILED%`), not the Python-expanded paths; and the comments deliberately
  contain the literal `"tasklist | find"` as the counter-example, so a whole-file grep
  would mistake the explanation for a real pipe.
- **`ALIGNMENT.md` gained §7 (provenance inventory vs reme, per module)** — including the
  finding that `MISSING-MODULE` does **not** mean reme never did it: `autostart` /
  `update_helper` / `icons` are **inlined** in reme's `main.py` (declared as such at
  `main.py:61-63`). Verdicts recorded there: `autostart` keeps the template's stable-install
  form (premise ②, verifiable: it survives a version-directory swap, which is exactly the
  bug reme's own `sync_autostart_path` patches); `icons` is **undecided / logged as a gap**.
  §7.1 is the `update_helper` audit — reme semantic keypoints × landed state (1.0.1 /
  1.2.0 / 1.3.0) and the **rewrite-not-patch** conclusion with its reasoning, plus five
  remaining differences recorded as differences, not as "aligned".
- **Cascade**: dsh/ocx must re-copy `modules/update_helper/` (all three files, `[DIFF]`),
  and add two startup calls (`sweep_stale_update_dirs()`, `pop_failed_update_note()`);
  `sync_check.py` itself produces no cascade.

## 2026-09-19 (public build flow skeleton: STANDARDS D1 + build.bat / release.bat)

User asked for the shared build/test **flow** to be unified across the four tools,
with reme-helper as the reference. Turned into a template-side artifact.

- **STANDARDS D1 rewritten as a step skeleton** (phase / step / judgement+exit /
  trigger), with three **INSERT POINTS** where tool-specific steps may go and
  nothing else may be invented:
  0 preflight (VERSION parse / target dir free / target-directory guard) →
  1 cheap gates (compile → template sync → i18n (T1) → tray suites → tests) →
  2 business selftest (real resources) →
  3 package (icon → PyInstaller → assemble → deliverable checks) →
  4 frozen verify (smoke with dual env pin → trigger checks → DONE).
- **Skeleton vs step-set are explicitly separated** (the user's boundary):
  "the skeleton is uniform" means the phases, order, failure style, isolation and
  flags are the same everywhere; "which steps a tool has" follows its triggers.
  So dsh/ocx having **no `tests/`** is a **gap** (their capabilities exist), not a
  different skeleton — and reme having 8 suites is not something others must copy.
- **Common conventions pinned**: gate lives in root `build.bat` (a thin forwarder to
  `scripts\build.bat` is allowed, but logic may exist in one place only); `VERSION`
  is read from one source and `build.bat`/`release.bat` must agree; the running check
  uses `%APPNAME%` (no literals); every gated instance pins **both**
  `<APP_UC>_DATA_DIR` and `<APP_UC>_CONFIG`; `norun`/`nopause` flags are uniform.
- **`modules/build_release/build.bat` rewritten to the skeleton**, folding in this
  round's fixes: (a) VERSION parsed with the **two-step** form (split on `=`, drop
  quotes, take the first token) — verified under cmd against trailing-comment and CJK
  variants; the earlier `delims=^"` shape is gone as too fragile in escaping
  contexts; (b) the running guard blocks only when the live instance's directory **is**
  the target dir; (c) that same guard now precedes **every** delete of a release dir,
  including a new `clean --force` subcommand; (d) the frozen smoke pins both env vars.
- **`release.bat` aligned**: same two-step VERSION parse, same single source as
  build.bat (a trailing comment can no longer produce a garbage tag).
- Template-only change (`modules/build_release/` is excluded from `sync_check`) —
  **no cascade**; the four tools adopt it on their own schedule.

## 2026-09-19 (update_helper 1.1.0 — same state-copy bug, second instance)

The conformance auditor found the i18n defect again, in `update_helper`, and this time
it killed a whole feature silently: dsh/ocx automatic updates were dead.

- **`modules/update_helper/__init__.py` no longer copies state** (same fix as i18n
  2.1.1): only the functions are bound; `UPDATE_READY` / `PENDING_CMD` / `REPO` / … are
  delegated to the submodule through a PEP 562 `__getattr__`. The old
  `from .update_helper import *` copied `PENDING_CMD` into the package, while
  `download_and_prepare`'s `global PENDING_CMD` rebound the submodule's copy — so the
  tool read a permanent `None` from the package and **`apply.cmd` was never launched**:
  the update downloaded and never installed, with no error anywhere.
- **`UPDATE_READY` now actually gets assigned.** It was defined, documented in the
  README and read by the dsh/ocx menus (`enabled=lambda: update_helper.UPDATE_READY is
  not None`), but no code ever set it — the "download and update" item was grey forever,
  and `download_update_menu` would have built a `.../vNone/...-None-...zip` URL.
  `check_update()` now publishes the result via `_publish()`: a real newer version sets
  it, "not newer" clears it, and a network failure leaves the last known value alone.
- **Accessors added**: `update_ready()` / `pending_cmd()` are the recommended readers
  (the i18n 2.1.1 rule: state is read through an accessor, never as a mutable global).
  The globals stay for compatibility and now read live through the delegation.
- **New conformance check C-21** (in `conformance_check.py`, with a `--selftest` that
  reverse-proves it on synthetic samples): for every `src/modules/<m>/`, if
  `__init__.py` does `from .<m> import *` **and** `<m>.py` has a public module-level name
  rebound via `global`, it is reported as "state that gets statically copied — external
  reads get a stale value". This shape has now appeared twice and both times failed
  silently; C-21 makes a third instance mechanical to catch. On the current tree it
  names exactly `dsh-helper` and `opencodex-helper` (`src/modules/update_helper/__init__.py: PENDING_CMD`).

## 2026-09-19 (i18n 2.1.1 — the package no longer copies mutable state)

A real user-visible bug, root cause in the template: `modules/i18n/__init__.py` did
`from .i18n import *`, which **copies** `LANG` into the package namespace. After
`i18n.init('en')` the submodule was English and `t()` returned English, but
`i18n.LANG` read from the package was still `'zh'`. local-speak2text's
`_menu_signature()` read that stale value, so switching language changed the
notification but never rebuilt the menu — **the menu stayed Chinese forever**.

- **`modules/i18n/__init__.py` rewritten to not copy state.** Only the *functions*
  are bound (they read submodule globals at call time); everything else (`LANG`,
  `TABLES`, `KEY_MIN_SET`) goes through a **PEP 562 module-level `__getattr__`** that
  delegates to the submodule on every read. `LANG` must therefore never appear in an
  import here — binding it would recreate the dead copy and silently disable the
  delegation. This is the shape reme-helper already had (`from . import i18n` plus no
  mutable globals), which makes the bug structurally impossible.
- **`modules/i18n/i18n.py` gains `current_lang()`** — the recommended reader. `LANG`
  stays for compatibility and is documented as internal.
- **Regression folded into `sync_check.py --selftest` (group D)** — asserts the
  language read *from the package namespace* flips immediately on `init('en')` / back
  on `init('zh')`, that `t()` follows, and that `LANG` is not a static copy. Reading
  only the submodule would not catch this bug. Reverse self-proof: re-adding a `LANG`
  import to the package makes D1 (LANG appears in the package namespace) and D2
  (reports `zh`) fail, with the exit code at 1.
  Why folded in rather than kept as a root-level script: a script with no caller is
  dead code — it would never run again. `--selftest` is the family's established
  "repeatable reverse proof" slot, so the assertion inherits "breaks → exit 1".
- **VERSION 2.1.0 → 2.1.1**; `modules/i18n/README.md` documents `current_lang()` and
  the rule "state is read through an accessor, never as a mutable global".
- **Docs (task #9): release cadence recorded.** STANDARDS **G3 item 7** (+ pointer in
  B3): development does local commits only and does **not** touch the version number;
  bump + tag + push happen together as the single "release" action, and unreleased
  work lives under `## Unreleased`. CONFORMANCE **§4.1.12** records the rule and the
  currently non-conforming instances (dsh 1.8.2 / ocx 1.2.2 / reme 1.2.6 / l-s2t
  1.4.1 are bumped-but-unreleased; rollback is the tool owners' task).

## 2026-09-19 (sync_check 1.4.0 — module READMEs are no longer invisible)

Fourth blind spot, found by the lead's independent full-hash comparison rather than
by the checker itself: `scan_tool()` used `rglob("*.py")`, so every module `README.md`
was outside the comparison. "Adopt the whole folder" means **README + `__init__.py` +
code**, but only the `.py` half had a gate — module docs could drift forever.

- **`sync_check.py` 1.3.0 → 1.4.0** — scan range widened from `*.py` to the module's
  full comparison set (`.py` + `.md`), reusing the same `[ok]` / `[NOHDR]` /
  `[MISSING-FILE]` semantics. Template-only directories (`baseline/`, `build_release/`)
  are excluded so they don't produce 4×N false MISSINGs, and `__pycache__` (and other
  generated dirs) are skipped so `.pyc` files don't flood the report.
  This touches only `sync_check.py` — it is not consumed by the tools, so there is
  **no cascade**.
- **ALIGNMENT.md** — documents the fourth blind spot, fixes the formal definition of
  "adopt the whole folder" (README + `__init__.py` + code, all byte-normalised), and
  records the measured four-way snapshot: l-s2t 0 DIFF (17 SAME), dsh/ocx 1 DIFF each
  (appconfig README), reme 7 DIFF (5 READMEs + i18n ×2).

Measured after the change: 0 drift; 9 `[NOHDR]` (reme's 5 module READMEs, dsh/ocx
appconfig READMEs, reme i18n ×2) and 6 `[MISSING-FILE]` (dsh/l-s2t/ocx each missing
`icons/README.md` and `icons/__init__.py`). Yellow only; exit code stays 0.

Follow-up in the same round (two corrections):

- **`.md` now compares byte-for-byte and reports `[DIFF]`, never `[NOHDR]`**
  (CONFORMANCE §4.1.10a). The line-stripping normaliser was built for *code* copies
  (drop the provenance header, then hash); markdown headings also start with `#`, so a
  `# TEMPLATE-FROM:` line would be silently dropped and a header-carrying README would
  compare equal to a header-less one. Policy: module READMEs carry **no** TEMPLATE
  header and must be byte-identical. Self-proved by planting a header-bearing README
  copy in a scratch tool: it reports `[DIFF]`, exit code stays 0.
- **`modules/paths/README.md:18` corrected** — it still claimed l-s2t's
  `LOCALSPEAK2TEXT_*` was "the one known exception" to the env-var derivation. That
  exception no longer exists (l-s2t renamed to `LOCAL_SPEAK2TEXT_*`); the sentence was
  wrong and had been copied byte-for-byte into all four tools. No VER bump: module
  READMEs are unversioned prose, and the interface itself (`<APP_ID-derived>_CONFIG`)
  is unchanged — only the stale exception note is gone.
- **Module-level OVERRIDE covers the README** — when any `.py` in a tool's module dir
  declares `TEMPLATE-LOCAL-OVERRIDE`, the whole module is intentionally diverged, so its
  README cannot match the template: that mismatch now reports `[decl]` instead of
  `[DIFF]` (reme's heavy-form `i18n/`). `[NOHDR]` is now emitted only for `.py`; the
  `.md` path never suggests "add a header", because that is the forbidden action.

Self-proof (three samples, reproducible): (A) header-bearing `.md` → `[DIFF]`;
(B) byte-identical `.md` → `[ok]`; (C) module with `TEMPLATE-LOCAL-OVERRIDE` and a
differing README → `[decl]`.

The self-proof is now a **repeatable regression switch**, not a one-off command:
`python sync_check.py --selftest` builds the three synthetic samples in a temp dir,
asserts the classification, and exits non-zero if any of them regresses. A one-off
command disappears with the session; a judgement that silently breaks later is exactly
what a regression sample exists to catch. The `[NOHDR]` message is also now explicitly
`.py`-scoped and states that READMEs must **not** be given headers — the old wording
("add a header") was correct for code and actively wrong for docs.

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
