# Changelog

Template library own versioning (TEMPLATE-VER), independent of any tool.

## 2026-09-19 (C-22 bat byte hygiene; a generated-bat LF instance found by it)

The lead's byte scan of the family's `.bat`/`.cmd` files turned the "bats are CRLF + ASCII"
line into a requirement, so it is now a mechanical check rather than a sentence.

- **`conformance_check.py` 1.3.0 — new C-22**: every `.bat`/`.cmd` in a tool repo must be
  **CRLF, contain no 0x09, and be pure ASCII**, reported per file and per line. Build output
  and scratch directories are skipped (`release/ out/ dist/ _internal/ .cache/ .verify-scratch/`)
  because they are neither hand-written nor committed. Five selftest samples pin the three
  corruptions (TAB, LF-only, non-ASCII) plus a mixed case and a clean file.
- **State on the real tree**: the three instances from the lead's scan are **already fixed**
  by their owners — `reme-helper/scripts/build.bat` (was `tests<TAB>est_update_bat.py`),
  `local-speak2text/release.bat` and `run.bat` (were LF-only) now all report
  `CRLF/LF=0/TAB=0/nonASCII=0`. C-22's only remaining hit is
  `reme-helper/.cache/gate_proof.bat` — a **generated, git-ignored** scratch script written
  by a verification run: the file is not authored source (hence the exemption) but it is
  still the *evidence* for the J-坑 "a script that writes a .bat silently produces LF".
- **Template side**: C-22 does not scan the template repo, so
  `modules/build_release/verify_build_bat.py` gained the same byte check for the template's
  own bats — the template is the dispatch source, so one TAB here becomes four in the tools.
- **STANDARDS**: B1's bat line now points at the executable criterion, with the **self-proof
  obligation** ("after every added/edited bat line, run C-22") and the reason the corruptions
  are invisible: they never error, they only make *one line* silently stop working — and if an
  earlier gate stops the build first, that line is never reached. **J 坑 gained two entries**:
  the escaping one (`"\t"` written into a file becomes a real TAB), and the console-subsystem
  fake-exe one (a modal console window pops on the user's desktop, and its cwd makes the
  cleanup delete fail silently, leaving an empty shell directory — today's user report).
  ⚠️ **This very CHANGELOG entry reproduced that J 坑**: it was written from a Python string
  where `\t` was interpreted, so the first version contained a literal TAB (found by re-reading
  the bytes; fixed in `cbad9b0`). The lesson is not "be careful" — it is **verify the bytes of
  what you just wrote**, which is exactly what C-22 automates for bat files.

## 2026-09-19 (ALIGNMENT: icons closed as [decl]; the second update path assessed)

Two verdicts the lead asked for; **no code changed** for either.

- **`icons` (7.3): closed as `[decl]`.** Function-by-function semantic diff against reme's
  three inlined functions. The build-time half is **identical** — generation timing, artefact
  names, `TRAY_SIZES`, `TASKBAR_SIZES` (value-for-value; the template source already cites
  reme as the origin of that list), and the multi-frame `save(sizes=[...])` write. The
  difference is the graphic itself: reme hardcodes its "R" mark, while the template injects
  it per app via `ICON_DRAW(size)` / `ICON_ASSET` — that is the *definition* of the T6
  extraction, so "make the template match reme" does not apply (it would bake one tool's
  trademark into a shared module). Residual absorbable item, low priority: `icon_font()`'s
  font fallback chain (only useful to tools that draw text).
- **`paths.process_pending_update()` (7.4): assessed, not touched.** Template copy at
  `paths.py:82-96` does destroy evidence (`os.system(robocopy /MIR)`, rc never read, then
  unconditional `unlink` + `rmtree`). **One correction to the working assumption**: l-s2t does
  **not** call that copy — `main.py:33` imports it from its own `updater.py:320`, a fork that
  already implements everything the lead asked for (rc checked, `subprocess.run([...])`,
  `/e /purge`, and on rc>=8 it keeps `pending` + staged files and writes the marker). dsh/ocx/
  reme never call it at all. So the harm today is not "actively destroying" but "a landmine
  shipped inside four copies plus a documented API". Absorption cost: 5-way `paths` cascade,
  the `RUN_DIR`-based `UPDATE_PENDING` needs a data-dir home, and the two update paths
  (startup catch-up vs exit-time bat) must be ordered or made mutually exclusive, otherwise
  one update can be applied twice. Proposed order: land the stable-install entry in
  `update_helper` → switch l-s2t and delete its fork → only then remove the `paths` copy.

## 2026-09-19 (tray_kit 2.2.0 — one validity criterion for all three; C-10 now AST-based)

The lead's review of the 2.1.0 delivery asked for two things that were genuinely missing, so
this round adds them (2.1.0 stays as the historical step; dsh/ocx should re-copy).

- **`tray_kit` 2.1.0 → 2.2.0: the name-validity rule is now a single shared function.**
  New public **`mutex_name_ok(name)`** — non-empty `str`, `Local` namespace prefix, and no
  further backslash after the prefix. `acquire_single_instance`, `mutex_name_is_valid` and
  `single_instance_free` **all call it**; previously the guard did no validation and the
  probe only asked the kernel, i.e. two criteria for one rule. Consequences:
  * the guard now rejects an illegal name **before** touching the kernel, logs it, and
    **fails open** (`return True`, D3.2) — a programming error must not brick the tool; the
    build-time probe is what turns it red (D3.3);
  * `_derive_mutex_name()` is the single derivation point (`mutex_name or f"Local\\{app_id}-single-instance"`),
    so the guard and the probe cannot drift apart;
  * a docstring escape bug (`\`` inside a non-raw docstring) was caught by importing with
    `-W error::SyntaxWarning` — it would have printed a SyntaxWarning in every consumer.
- **`conformance_check.py` C-10 is now AST-based**, as requested: it takes the real
  `def smoke` body (any nesting), requires a probe call whose result **is consumed** by an
  `if` / `while` / `assert`, and reports "called but unchecked" separately. A new selftest
  sample pins the case a substring judge silently accepted: the probe name appearing **only
  in a comment**.
- **STANDARDS §D3.3 extended** with the shared-criterion requirement and the AST judgement;
  §D3.1 now points at it explicitly ("coverage must not be traded away to avoid the hang").
  The **J 坑 list** gains "modal dialog on an unattended path" — it degrades "turns red" into
  "hangs forever", and this family has now hit it twice.
- **`sync_check --selftest` group F grew to 7**: adds the shape matrix (None / "" / no prefix /
  `Global\` / second backslash / non-str), "the guard fails open on an illegal name and logs
  it", and keeps the earlier occupied-name and no-stray-handle assertions.
- **Cascade: all four tools re-copy `modules/tray_kit/` (2.2.0 — three files).** dsh/ocx had
  already taken 2.1.0 and wired the probe, so for them this is a re-copy only; l-s2t and reme
  still need the copy plus the probe call in `smoke()`.

## 2026-09-19 (tray_kit 2.1.0 — the smoke probe; D3.3; C-10 now tells "covered" from "bypassed")

`--smoke` must cover the single-instance guard, but "run the real guard in smoke" is not an
option: with the user's tray running, the guard takes the duplicate path and pops a **modal**
box, which hangs unattended builds. dsh/ocx had no guard coverage in `smoke()` at all, and a
recent "move `--smoke` before the guard" fix traded coverage away to dodge the hang. The
answer is to **change the form, not the position**.

- **`modules/tray_kit/` 2.0.2 → 2.1.0**: new public
  **`mutex_name_is_valid(app_id, mutex_name=None)`** — the probe l-s2t had inlined. It asks
  "does the kernel accept this name", **does not hold the lock and shows no dialog**;
  `ERROR_ALREADY_EXISTS` counts as valid (the name being taken *proves* the kernel accepts
  it), so unlike `single_instance_free()` it is unaffected by a running instance — which is
  exactly why the latter cannot be used as a smoke assertion (false red).
  `__init__.py` VER follows; README interface table gains the probe (and documents
  `single_instance_free`, which had been missing from the table).
- **STANDARDS §D3.3** (new): the correct shape for smoke guard coverage is a **probe**, not
  the real guard; "moving `--smoke` earlier" is explicitly **not** coverage. Records that
  this modal-box shape has now been hit twice in this family (l-s2t `test_startup_path.py`,
  ocx `--smoke`) and that any modal dialog on an unattended path degrades "turns red" into
  "hangs forever".
- **`conformance_check.py` 1.2.0 — C-10 judgement rewritten** so it separates the three
  cases instead of matching a substring: probe + result checked → ok; probe called but
  result ignored → FAIL ("coverage ≠ call"); **real guard** in smoke → FAIL (modal box);
  nothing → FAIL. `single_instance_free` deliberately does not count as a probe. Four
  selftest samples pin the four shapes.
  Real tree: **l-s2t ok; dsh — no coverage; ocx — real guard in smoke (the modal hazard);
  reme — no coverage.**
- **Cascade: all four tools must re-copy `modules/tray_kit/`** (`tray_kit.py`,
  `__init__.py`, `README.md`). Adoption for dsh/ocx/reme is "add the probe to `smoke()` and
  make it fail the build", which is also what closes C-10 family-wide.

## 2026-09-19 (state rule into STANDARDS D6; update_helper 1.4.0; reme reference re-audit)

reme-dev published `reme-helper/UPDATE-CHAIN-REFERENCE.md` (`10c76df`) as the comparison
baseline. Re-auditing against it produced one new rule, one module hardening, and three
corrections to conclusions people (including me) were carrying around.

- **STANDARDS gains §D6 — "状态的唯一写入点与暴露方式"**: state is exposed either as a
  **container mutated in place** or through an **accessor**; state promised to outside
  readers must have a **single write point**; a module-level scalar rebound via `global`
  while outsiders read it through a package `import *` is banned. One shape, three real
  silent failures: `i18n.LANG` (menu stayed Chinese), `update_helper.PENDING_CMD` (update
  downloaded, never installed), and reme's `tray_signature()` missing the update state
  (the "download and update" item never lit up). The rule carries a **mechanical ladder**:
  C-21 (FAIL, already broken) → C-23 (WARN, fragile shape) → C-24 (WARN, menu state not
  in the signature).
- **`modules/update_helper/` 1.3.0 → 1.4.0**, absorbing §1/§2 of the baseline's transport
  list as *structure* rather than convention:
  * state now lives in a `_PUBLISHED` dict mutated in place; `UPDATE_READY` / `PENDING_CMD`
    are **read-only derived** values from a module-level `__getattr__` — there is no
    rebindable scalar left. Reverse self-proof: put the old `from .update_helper import *`
    facade back and the package no longer receives those names at all (loud error) instead
    of receiving a dead `None` (silent).
  * **new `launch_pending_cmd()`** — `CREATE_NO_WINDOW | DETACHED_PROCESS`, the reme form.
    Previously "how to launch it" was left to the consumer, so tools wrote
    `os.system('start "" /min …')` themselves; the bat must outlive the parent and must not
    flash a console, and that belongs to this module.
  * **empty stage is intercepted before anything is touched** (reviewer-reported hazard):
    `robocopy /e /purge` from a swept/empty stage returns 0–7 and would **wipe the install
    dir**, after which `start ""` on a missing exe pops a modal error box nobody can
    dismiss — the bat hangs forever. Now: no exe in stage → don't touch the install dir,
    write the failure marker, bring the old version back. Every `start` also gained an
    existence guard (start a non-existent exe is the one unrecoverable action here).
- **`conformance_check.py`: new C-23 / C-24** (C-22 is taken by the bat hygiene task),
  both WARN, both with `--selftest` positive/negative samples. On the real tree C-23
  correctly names `modules/i18n/i18n.py: LANG` in three tools (the same fragile shape,
  still to be converted) and C-24 names dsh/ocx's missing menu-signature mechanism, while
  reme and l-s2t pass. The first C-24 regex swallowed a *different* function body whenever
  the signature had a return annotation (`def f() -> tuple:` has no `):`), which produced a
  false red on reme — the fix and the reason are recorded in a code comment.
- **`sync_check.py` selftest group E** grew from 17 to 21 assertions: the five new ones
  cover "no `global` rebinding", "the two names are not module globals", "an in-place write
  is visible immediately", "`import *` does not carry the derived names", and the two bat
  guards.
- **Three carried-over conclusions corrected** (recorded in `ALIGNMENT.md` §7.2):
  1. "the template copied reme's sha256-skip" — no: 1.2.0 did, **1.3.0 is fail-closed**, and
     reme fixed its side the same day. The difference no longer exists.
  2. "the template has persistent throttling, reme doesn't" — **half true**: the throttle
     state is a per-process dict, so a restart still hits GitHub once. The baseline document
     calls it "persistent", which the code does not support. Behaviour left as-is (one
     request per launch is fine against a 60/hour quota) but the wording is corrected.
  3. "the template's apply.cmd also skips the robocopy rc check" — the *memory* was of the
     right shape in the wrong file: `apply.cmd` **does** check rc (1.3.0). The real gap is
     `modules/paths/paths.py: process_pending_update()` — `robocopy /MIR` with no rc check,
     no rollback, and `return True` regardless. reme has no counterpart, so under the
     arbitration rule it is not the baseline; it is an **unpermitted gap** with two options
     (merge into `update_helper`, or keep it and check rc / drop `/MIR`). Both touch
     `paths.py`, which four tools consume byte-identically → escalated as a decision, not
     changed unilaterally.

## 2026-09-19 (build.bat VERSION parse: end-to-end evidence, and a repeatable harness for it)

Asked to swap the template's VERSION parse for the form that has **end-to-end** evidence
(l-s2t's real `build.bat` run) rather than fragment-level evidence. The swap had already
happened in the D1 round — the template's `build.bat`/`release.bat` have used the two-step
form since `7da61e7`, and no `delims=^"` shape remains anywhere. What was missing was the
**evidence level**, so this round adds it as an asset:

- **`modules/build_release/verify_build_bat.py`** — the template `build.bat` is
  instantiated per its documented usage (fill `<APP_ID>`/`<APP_ID_UC>`), dropped into a
  throwaway tool skeleton under `%TEMP%`, and **executed for real by cmd.exe**; only phase 0
  output is observed. Four samples, and the harness exits non-zero if any fails:
  * **A** two-step parse + a `VERSION` line carrying a trailing CJK comment →
    `[VERSION] 1.4.0  release: release\e2etool-1.4.0`;
  * **B** pre-create `release\e2etool-1.4.0` → the script refuses **by that parsed name**,
    so the parsed value provably drives a real filesystem judgement (phase 0.2);
  * **C / B2** reverse: put the recorded old `"tokens=2,* delims=="` back → the version
    becomes `"1.4.0"  # 发版时才?` (the comment swallowed, then mangled by the code page)
    and the pre-created directory is **not** recognised. Without this pair the forward
    assertions could pass vacuously.
- **Why not a fragment test**: cmd behaviour depends on context (setlocal, variable state,
  code page, `for /f` environment). The 1.2.0 `findstr`-prefix episode was exactly a
  fragment that "looked right and was wrong in both branches". This harness runs the real
  file, not an excerpt.
- `modules/build_release/README.md` now documents the two-step form, why `"tokens=2,*"` is
  banned, and the harness. Template-only directory (excluded from `sync_check`) — **no
  cascade**; the two-step lines in the tools already match (l-s2t points at
  `src\modules\appconfig\appconfig.py`, template at `src\main.py`: same shape, one source).

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
