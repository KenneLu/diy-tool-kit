# Changelog

Template library own versioning (TEMPLATE-VER), independent of any tool.

## 2026-09-19 (C-44: bare-name external commands in bats; PATH hands you a different program)

- **C-44 (FAIL, tool + template channel).** In `.bat`/`.cmd`, a **closed set of 8 commands**
  (`find` / `findstr` / `ping` / `tasklist` / `robocopy` / `where` / `reg` / `timeout`) must be called
  by **absolute path**, never by bare name. The mechanism (reme-dev hit it): on this machine
  **`where find` resolves to Git's `usr/bin/find.exe`**, ahead of System32 — the wait loop used
  `find /i "{exe}" file` to decide "is the old process still there", and **GNU `find` treats
  `smss.exe` as a filename and returns non-zero**, so the loop concluded "already exited" every time
  and went on to overwrite an exe **that was still running** (locked file, then robocopy's default
  million retries). `ping` is the same trap (GNU's `-n` means numeric, not count). **Same root as
  `dev/null`: the environment quietly supplies a program with the same name and different semantics,
  the code takes the wrong branch, and nothing reports an error.**
  * **Only the command position is judged** (line start, or the first token after `|`/`&`/`(`/`^`,
    including the `for /f ('cmd')` inline form); `rem`/`::` lines are exempt; a token containing a
    path separator counts as absolute. So prose that mentions `find`/`ping` (as `update_helper`'s
    `rem` block does at length) is not flagged.
  * **Measured: 17 sites** — template 3 (`build_release/build.bat:48`, `:171`, `release.bat:10`),
    dsh 2, l-s2t 5, ocx 2, reme 5 — **all of them `findstr` / `tasklist` / `robocopy`**.
  * **Calibration measured with `where`**: **only `find` and `timeout` are actually shadowed** here
    (Git's `usr/bin` first); the other six currently resolve to System32. So today's 17 sites are
    **latent** rather than live — but **PATH order is not ours to assume**, which is exactly
    discipline (12), so the criterion keeps the whole closed set.
  * **Five self-test legs**: bare name => red; absolute path => green; a mention inside `rem` =>
    green; the `for /f ('findstr ...')` form => red; a non-closed-set command => green.
- **The template's `update_helper` needs nothing here, and that is measured rather than assumed**: its
  rendered `apply.bat` already calls the System32 paths for `tasklist.exe`, `find.exe`, `Robocopy.exe`
  and WindowsPowerShell, with **zero bare-name hits**, and no `ping` remains. **C-33 and C-44 are
  independent** (one governs *ping-as-a-tick*, the other *bare-name resolution*); neither substitutes
  for the other, and each scans and reports on its own.
- **Discipline (12)**: **the resolution of any external name a criterion or program depends on changes
  with the environment (PATH order, same-named tools). Anything depending on an external name must
  either pin an absolute path, or it is handing the branch decision to the environment.** Filed next
  to discipline (11) — that one says *two layers sharing one transformation err together*, this one
  says *the startup environment silently swaps your branch*; both are "a factor outside the code
  quietly changed the execution path".


## 2026-09-19 (C2 landing moved to `tray_kit`; the evidence-swallowed-by-return family, third instance)

- **C2's home changes from `paths.py` to `modules/tray_kit/tray_kit.py`** (the lead withdrew the
  earlier `paths` decision on helpers-dev's evidence, which is harder than the semantic-ownership
  argument I had used). Measured here to confirm the premise: `tray_kit.py` **already** has
  `import ctypes` + `from ctypes import wintypes` and **12** `CreateMutexW` occurrences, whereas
  `paths.py` would need two new imports. The decisive reason is **cohabitation by family**: C2 and
  `acquire_single_instance` are both **kernel-object guards with process lifetime, both failing
  open** — keeping them together makes that family legible at a glance. The implementation still
  lives in `paths.py` 1.1.4 for now (`hold_no_delete` / `hold_exe_delete_guard`, already measured by
  C-37); moving it into `tray_kit` is a dispatch event (§4.1.39).
- **Third instance of "evidence swallowed by an earlier return"**, recorded in §4.1.29:
  helpers-dev's first `delete_protection_selftest` put the happy path's `return` inside `try`, so
  **`finally` ran and the function returned immediately, skipping the cleanup below it** — i.e. a
  **green run leaked one `c2-selftest-*` directory into `%TEMP%` every time**. The corrected version
  computes `result` first, does the cleanup, and returns once; it also **puts cleanup failure into
  `problems`** (in the original, a failed cleanup sat in `finally` where the already-computed return
  value swallowed it). Same family as C-32 and as `marker.unlink` running before `log`.
- **Retry boundary, recorded with it**: `_rmtree_verified`'s `delay` exists to absorb **transient
  locks** from Defender/indexers (there is precedent in `tests/_cleanup.py`), and **`tries × delay`
  exhausted means failure — it is not "retry until it succeeds"**; otherwise "retry" silently
  becomes "wait forever".
- The two reserved-semantics lines for the C2 relaxation are already in §4.1.29 and stay there:
  **what is relaxed is the refusal condition, not cleanliness**, and the handle must be held **by the
  running instance** (early, to process exit, failing open).

## 2026-09-19 (C-43: `:~` in an `if` condition aborts the whole script; narrow boundary)

- **C-43 (FAIL, tool + template channel), boundary pinned by ls2t-dev and adopted.** Only **one
  shape** is dangerous: a `:~` trailing/substring expansion (`:~-1` / `:~0,-1`) **inside a same-line
  `if` condition**. `%` expansion happens **before** the `if` is evaluated, so with the variable
  undefined the expansion drops a literal into the quotes, cmd reports
  `The syntax of the command is incorrect.` and **aborts the entire script** (it does not skip the
  line). Fix: use `for %%d in ("%VAR%") do set "VAR=%%~fd"` — `%%~f` does no substring expansion at
  parse time and cannot produce a broken quote.
  * **Nested `if` is harmless**: `local-speak2text/build.bat:84`
    (`if defined RUNNING_DIR if /i "%RUNNING_DIR%"=="%TARGET_DIR%" (`) contains **zero** `:~`, so it
    is plain `%VAR%` expansion — undefined yields `""` and the syntax still holds ⇒ **green**. A
    wide version ("flag any nested `if`") would have made **this very line a live false positive —
    in our own repo**, which is why the line is now a negative sample in the self-test, copied
    verbatim.
  * **Condition vs action** (measured here): `if defined X set "Y=%X:~0,-1%"` (dsh/ocx
    `build.bat:87`) has the `:~` on the **action** side, guarded by `if defined`, so an undefined
    variable expands to empty ⇒ **green**. The criterion therefore draws its line at "does `:~`
    appear **before** the action keyword".
  * **Measured: all four tools and the template are `[ok]`**; four self-test legs, three of them
    built from **real lines in our repos**.
- **Probe discipline for this class, recorded as §4.1.45-补** (ls2t-dev's method, reusable):
  ① the probe must take **only the guard region** and run with `cwd=<repo>` — the head's
  "release dir already exists" check exits first, so a whole-bat probe never reaches the guard (his
  first attempt was wasted that way); ② decide by **`rc` + marker, never by matching the text**
  `Syntax of the command is incorrect.` — cmd writes in the **OEM code page**, so a UTF-8 decode
  fails to match and **both cases read 0** (a false green). ⇒ **Do not build a criterion on text
  that may be misdecoded** (same family as §4.1.37 and discipline ⑪).
- **D1-04 gets its first positive instance**: ls2t-dev's **17:25 full build reached `[DONE]` with no
  instance running at all** (measured process count = 0 before the 1.4.0 directory was removed).
  Recorded next to the dsh/ocx negative instances — **a requirement with only counter-examples can't
  be told apart from an impossible one**; with a positive instance it becomes a proven operation.

## 2026-09-19 (C-42: `dev/null` in redirect position; and why the self-check was green anyway)

- **C-42 (FAIL, tool + template channel), narrowed on the lead's instruction.** In `.py`/`.bat`/`.cmd`
  the **redirect position must not contain `dev/null`** — matched as `>` (including `2>`, `>>`) plus
  optional whitespace plus `dev/null`. **Not** written as "`dev/` must not appear anywhere": that
  would false-positive on comments holding paths (`H:/Tools/dev/...`) and on URLs. Narrowed to the
  redirect position it has **zero false positives** — there is no legal reason for it there on
  Windows, where `> /dev/null` makes the command **not run at all** (`rc=0` in 0.03s, stderr says the
  path was not found; correct form: 0.68s, empty stderr).
- **The accident, by ls2t-dev**: patching through a **bash heredoc** rewrote `nul` into `/dev/null`
  **before Python ever saw it** (and flipped LF to CRLF), so the `powershell` sleep never ran —
  `tries` raced up at `tasklist` speed, 120 ticks burned in seconds, `:giveup` fired while the old
  process was still alive, **and the log still printed `120 polls x 1000ms (nominal budget 120s)`**.
  **All three existing judges were blind to it**: C-22 (still ASCII+CRLF), C-33 (looks for `ping`),
  `test_update_safety` (never reaches that redirect). **And his self-check was green** — he compared
  the **same literal**, rewritten by the same rule, so the comparison had to pass.
- **Text surface follows C-33's boundary (§4.1.37)**: `.py` masks comments/docstrings but **keeps
  other strings** (the rendered-bat template is a string — that is what must be scanned);
  `.bat`/`.cmd` drops `rem`/`::` lines. Otherwise **this criterion's own explanation would indict
  itself**.
- **The criterion caught a real false red on its first run — in itself.** The template channel
  reported `conformance_check.py:4087` twice: the positive sample I had just written
  (`BAT = "x >/dev/null 2>nul"`). Same lesson as C-33, second instance in one day: **a criterion's
  own fixtures necessarily contain the banned shape** ⇒ the scan surface now **excludes the
  instrument by absolute path and prints the exclusion** ("stale exclusion" and "never scanned" must
  not look alike).
- **Five self-test legs**: the three the lead named (redirect hit -> red; `H:/Tools/dev/x` in a
  comment -> green; `>nul` inside a template string -> green), a `.bat` shape -> red, and the reverse
  cell `devnull_like_name_ok` (`> dev/nullish` -> green, proving the narrowing reaches the whole
  word). **Measured: all four tools and the template are `[ok]`** (24/44/25/33 + 22 files).
- **Registered as §4.1.44 + discipline ⑪**, and as the **second instance in §4.1.20** next to the
  `ping` one — **opposite directions**: `ping` *waited too long* (9.0s/tick, a nominal 120s took
  ~18 minutes); `>/dev/null` **did not wait at all** (120 ticks in seconds). Both share the root
  cause — **nobody measured the assumed unit of waiting** — and both printed a "seconds" figure that
  was not true. ⇒ The conclusion gets wider: **don't just measure how long it waited; measure
  whether the command ran at all.**
- **Discipline ⑪ (the lead judged this more valuable than the criterion): when the *modifying* path
  and the *verifying* path share the same transformation layer, they err together.** Patching via
  heredoc and self-checking with the same literal means one rewrite rule acts on both sides, so the
  comparison **must** pass. ⇒ Acceptance must assert **a property no rewrite could satisfy**
  ("no `dev/null` in redirect position"), **not** "equals the string I expected"; and literal
  comparisons must be done in **bytes/hex** (ls2t-dev built `nul` from `bytes([0x6e,0x75,0x6c])`;
  the tail hex is `7d2220 3e6e756c 20 323e6e756c`). Same family as "the enumeration decides the
  horizon", "0 hits must print the scan surface" and "readings need a ruler".

## 2026-09-19 (C2 landing note: the release-dir guard was pushing users at the destructive action)

- **helpers-dev's framing, adopted verbatim by the lead, is now written into C2's registration
  (§4.1.29).** `build.bat` carries two guards, and their relationship is the point:
  * **(1)** `if exist "%RELEASE_DIR%"` -> error *"already exists. Delete it or bump VERSION"*
    (G1: one directory per version, reproducible);
  * **(2)** the D1-02 running-instance gate (refuses only when the live instance runs **from the
    target directory**).
  **What (1) actually achieves**: **rebuilding the same version is impossible; the only path is to
  delete the directory by hand** — and "manually `rm -rf` a release directory a live instance is
  running from" **is exactly the action that hollowed out 1.2.2 / 1.4.1**. In other words
  **that guard was pushing users toward that action.** This upgrades C2's motive from *"prevent a
  slip"* to **"dismantle a self-contradictory design"**.
- **With C2 in force** (a live instance holds a read handle on its own exe from early startup to
  process exit, failing open; measured `unlink` -> winerror 32 / `rmtree` -> 32 / parent `rename`
  -> 5), **guard (1) can safely be downgraded into guard (2)**: "directory already exists" goes from
  **ERROR to INFO/WARN** and merges into the same criterion (an instance running from it -> refuse;
  otherwise the script clears and rebuilds by itself).
- **Reserved semantics, written in as the one risky part of this relaxation** (helpers-dev's
  addition, adopted verbatim): **what is relaxed is the *refusal condition*, not *cleanliness*.**
  G1's "one version one directory, reproducible" must rest on **"always rebuild from scratch and
  reuse no file from the old directory"**, **not** on "existence -> refuse".
- **Precondition, all of it required**: C2's handle must be held **by the running instance** (taken
  early, held to process exit, fails open); otherwise this relaxation turns *safe failure* back into
  **silent hollowing**.
- **Announcement wording, to be repeated whenever this relaxation is mentioned**: **"the refusal
  condition was relaxed; the cleanliness requirement was not."**
- Doc-only: nothing under `modules/**` changed, so no dispatched hash moved and no re-copy is due.
  The `build.bat` edits themselves belong to the next dispatch wave (each tool's own file).

## 2026-09-19 (C-41: the "link unavailable" fallback must not reuse the saved checkbox)

- **C-41 (FAIL, tool channel + template channel).** The lead corrected two tools on the source
  question, so the rule is now a criterion: **the "confirm dialog unavailable" branch must be fixed
  to "do not stop the service"; it must not reuse the user's persisted checkbox.** The reason, in one
  line: **the checkbox was saved in a context where a dialog existed; when the link is broken the
  user was never asked.** Reusing it turns "an auxiliary mechanism broke" into "the user's running
  service is stopped without anyone confirming" — the theme of this whole round.
  * **Standard form** = dsh/ocx's hardcoded `False` (`return True, False`, two branches each).
    **reme and l-s2t originally followed the stored config**; both were corrected, and both **kept
    the history of having deviated** in place (reme's comment records "the old behaviour followed
    the saved config ... the lead withdrew that approval on 2026-09-19"; l-s2t's `_confirm_quit`
    docstring records the same clause).
  * **Why write the criterion now rather than later**: `tray_kit` is due to provide a unified form,
    and **a unified form is exactly where this grows back**. The criterion sits here, so the day
    that lands it gets verified by itself.
  * **Decidable form**: only the **fallback branches** are judged (`except` handlers and
    `if <x> is None:` bodies). A statement that feeds the quit decision **and** reads persisted
    config **and** touches a destructive key (`quit_stop*` / `quit_apply*` / `stop_tunnels` /
    `stop_reme` / `stop_service`) is red. **The native-dialog branch is not a violation** — there the
    user *was* asked (there is just no checkbox), which is why the criterion judges **per branch,
    not per file**.
  * **Measured**: template `modules/**` (3 quit-related functions, 6 fallback branches) and all four
    tools (6/7/6/8 functions; 21/16/21/19 branches) are **all `[ok]`** — nothing is wrong today; the
    criterion exists to keep the unified form from reintroducing it. **Five self-test legs**, two of
    them reverse cells (literal `False` in each shape ⇒ green; the **native branch reading config
    inside the `try` body ⇒ green**).
- **The declaration template gains a two-sentence rule (ls2t-dev's precise distinction).**
  What expires is **two different things** and they must be written separately:
  **content identity** (e.g. `f81a5922e2d8`) **is not wrong** — it identifies exactly that content
  and, *as a name, never expires*; the **binding assertion** ("**= what is on disk now**") is
  **time-bound** and becomes false the moment something changes. ⇒ Declare in two sentences:
  *"compared with `<old rev>`, only `X` changed — **new value N**"* (identity) plus *"**N is
  authoritative** (nothing has changed since)"* (assertion). Benefit: **"the old value is void" now
  has a clear object — the assertion is void, not the identity** — and nobody will read "the hash is
  void" as "that hash was computed wrong".

## 2026-09-19 (C-40: version directory vs autostart target; plus three escape corruptions repaired)

- **C-40 (FAIL), proposed by ls2t-dev, corrected twice by the lead.** It turns a discipline
  ("every owner should state which exe starts, and whether the version matches the source") into a
  **decidable property** — same move as C-38: **discipline -> property**. All three facts are read
  from **disk + registry**, so nobody has to remember anything.
  * **The lead's correction matters**: "the set of `release/` dirs == {VERSION}" is **false-red by
    construction** — `reme-helper/release/` = 1.2.4 + 1.2.5 and `dsh-helper/release/` = 1.8.1 + 1.8.2,
    i.e. it would flag **normal build history**. So two clauses, two levels:
    **① strong (FAIL)** the autostart target **must exist** and its directory must be
    `release/<source VERSION>/` **or** the stable install dir (`%LOCALAPPDATA%\<APP_ID>\app`);
    **② registry (WARN)** every dir that is not the current VERSION is an **orphan version** and must
    declare **whether it is still referenced** (`ORPHAN_VERSIONS`, two mandatory fields `why` +
    `reverify` per discipline ⑨/⑩ — it is a **coverage-off switch**).
    **Referenced orphan = must handle; unreferenced = cleanable.**
  * **Measured on this machine**: **dsh = FAIL** — source `main.py:33 VERSION="1.8.1"` while the Run
    key points at `release\dsh-helper-1.8.2\dsh-helper.exe`; ocx (1.2.1) and reme (1.2.5) match
    their source ⇒ ok; **l-s2t has no Run entry** ⇒ the strong clause does not apply. The **live dsh
    state is copied verbatim into the self-test as the positive sample**.
  * Six self-test legs, three of them reverse cells (target == release/VERSION; stable install dir;
    the same orphan **declared**). The judgement is a **pure function with an injectable
    `path_exists`** — otherwise the samples would have to be created on disk and would be **polluted
    by live state**.
  * **Wording discipline (ls2t-dev volunteered this; the lead judged it more valuable than the
    correct answer itself)**: when he confirmed l-s2t was consistent, he **added** that l-s2t *did*
    exhibit the pattern (`1.4.1` was a temporary version-bump build that ended as an empty shell),
    it was just **already cleaned up** — so the accurate statement is "**the pattern occurred and
    this repo has converged**", not "it never happened". ⇒ criteria and registries must distinguish
    **"never happened" (unverifiable)** from **"happened and converged" (verifiable, and more
    honest)**: entries are written as **current state + did it ever occur + how it converged**.
- **Three escape corruptions found in `CONFORMANCE.md` while adding the above, repaired byte-wise.**
  `\b`/`\a` inside text collapsed into control bytes (`0x08`, `0x07`) in the middle of paths:
  `reme\scripts\build.bat:22` had become `reme\scripts<0x08>uild.bat` and
  `%LOCALAPPDATA%\<APP_ID>\app` had become `<APP_ID><0x07>pp` — in **two** places. Repairing the
  control byte alone was **not enough**: those escapes **ate the following letter** (`\b` -> BEL
  consumed the `b`), so the fix had to restore `\build.bat` and `\app`, not just the backslash.
  This is the **same family as the two found earlier today** (§J ⑤/⑥) and it is the third time the
  shell/JSON layer has mangled backslashes in my pipeline — hence the rule already recorded: write
  these documents **byte-wise, with `chr(92)` for backslashes**, never through an escaping layer.
  Scan for leftover control characters is now part of the check (`0` remaining).

## 2026-09-19 (the declaration format gets a standing line; C-39 closes the snapshot family)

- **The declaration template now carries the `dirty=yes` explanation permanently** (CONFORMANCE
  §5.5, four fixed lines + a standing note). The lead's point: that sentence **is needed every
  single time** an announcement happens to sit next to other in-flight edits — **what needs
  explaining belongs in the format**, not in the author's memory. The note states it plainly:
  **`dirty` describes the whole worktree, not the declared files**; it must be read together with
  the per-path list ("these files have not changed a byte since their freeze commit"), so
  `dirty=yes` **does not invalidate an announcement** — and the test is simply: check the paths on
  line 3.
- **The second hash dialect gets its own section (§5.6) with a reproducible instance.** Same
  content, two rulers: `norm` for `.py` (strips `# TEMPLATE-*`), byte-for-byte for `.md`. Appending
  a single `# TEMPLATE-…` line moves `raw 8213f62be793 → f6b5d7711a26` while `norm` stays
  `0179f3bfda82` — so printing only one of them makes "the header/version moved" invisible, or
  misaligns with the `.py` comparison. (The historical example the lead quoted for this **does not
  hold**, and §5.6 says so.)
- **C-39 (FAIL, tool channel + template channel): a derived value must come from *this call's
  arguments*, not from a module-level current value or a definition-time snapshot.** Two instances
  of one family: `AsrEngine(model_dir=MODEL_DIR)` (§#46 — the user changed the config and nothing
  happened) and `budget_s` taking the module constant (`2 polls x 1000ms (nominal budget 120s)` —
  **a combination that cannot happen**; fixed in 1.4.4). Same family as "the numbers in the log must
  be numbers someone measured": that clause governs *unmeasured* numbers, this one governs *numbers
  taken from another input* — **both forms of a lying log**.
  * **Only the decidable half is judged**, in three bands: the default is a **rebound** module-level
    name ⇒ red; the default is a **mutable literal** ⇒ red; assigned once, immutable, never rebound
    ⇒ **passes** (all 13 such sites in the family are this kind, and their count is printed as the
    denominator). The third band **must** pass — otherwise it is a "flag every default argument"
    noise criterion, which is exactly the family of errors C-33 taught us.
  * Four self-test legs, two red and two green, including the reverse cell
    `immutable_constant_benign_ok`.
  * **What it does not cover**: a module constant written into an output string while the function
    also has an argument of its own (the `budget_s` shape) is **not** a default argument — that needs
    dataflow analysis. It is covered instead by **behavioural assertions in `sync_check --selftest`
    group E**, which **did not exist** despite `update_helper.py`'s docstring naming it as the place
    the criterion lives (§4.1.18's family: *a promised criterion that does not exist is no
    criterion*). Three legs added, including a real source mutation as the reverse cell.
- Family reading afterwards: **0 FAIL / 4 WARN / 0 BROKEN** — reme's C-27 is gone (reme-dev wired
  `hold_exe_delete_guard`), so the four C-38 WARNs are the whole board.

## 2026-09-19 (the criterion's fingerprint ended up in the product prose)

- **A real instance of "reword the product text so the criterion stops biting", located to a commit.**
  `modules/update_helper/update_helper.py`'s module docstring used to say, naturally:
  *"wait ticks no longer use `ping`: `ping -n 2 127.0.0.1` looks like 'sleep 1 second'…"* — that sits
  in a **docstring** (a string), while `_code_only_text` filtered only `#` and `rem`, so **C-33 read
  prose about code as code**. The chosen fix was **not** to the criterion: the sentence was rewritten
  to *"…no longer use `ping` (that is 'send ICMP and wait for replies', not sleeping): `-n 2` +
  loopback address"* — **splitting `ping` from `-n`** with a parenthetical and a separately quoted
  `-n 2`. Located in commit **`2afebbc`** (#40a, the dispatchable batch; diff lines 72/77) —
  **not** the batch that fixed C-33, which touched only `conformance_check.py` and three docs.
- **Why this is worse than the defect itself** (the lead's argument, and it is the decisive one):
  ① **the criterion's fingerprint is now in the product text** — the next reader cannot tell why the
  sentence is written that way; ② editing the text costs **four recopies every time**, while editing
  the criterion is **one change that turns all four green at once**.
- **Verified safe to revert the wording**: a probe putting the natural sentence back still comes out
  **GREEN** (`check_ping_tick`), because the criterion now removes **AST bare-string expressions**
  (§4.1.37). **Not done unilaterally**: restoring it touches `modules/**`, i.e. a **re-copy event**,
  so per §4.1.39 it goes through the dispatch flow (change → freeze → declare → re-copy) — recommended
  to ride the next wave's single recopy as TEMPLATE-VER 1.4.4 → 1.4.5.
- **Identity line: both hash dialects now have a measured discriminating instance** — appending a
  single `# TEMPLATE-…` line moves `raw 8213f62be793 → f6b5d7711a26` while `norm` stays
  `0179f3bfda82`. ⚠️ The instance the lead quoted for this ("`sync_check` 1.8.2→1.8.3: sha256 changed,
  norm did not") **does not hold**: both dialects changed across those two revisions, and no adjacent
  pair in either tool's history shows one changing without the other. **The mechanism is real; that
  particular example was not** — so the docstring carries my measured synthetic one instead.

## 2026-09-19 (before calling a fix "criteria-only": does it touch `modules/**`?)

- **New rule, from a case where nobody predicted it.** When the lead learned that C-33's reds were
  false reds, he thought "the criterion must change" — **not "changing it might touch a dispatched
  file"**. Changing anything under `modules/**` is a **re-copy event**: the four copies drift
  instantly, **already-declared dispatchable hashes are invalidated**, and every recipient re-copies
  for nothing. Registered as §4.1.39, with the mechanical form in two clauses that use existing
  machinery: ① **the increment declaration must list the `git diff --name-only` paths and state
  whether any of them is dispatched** (a commit id alone is not enough — this is exactly the cell
  that catches the accident); ② **if a criterion fix really would have to change `modules/**`, the
  default disposition is to redesign the criterion** (that is what C-33's fix did: **not one line
  under `modules/` needed to change**); if that is truly impossible, it must go through the dispatch
  flow (change → freeze → declare → re-copy) and **never ride an already-announced batch**.
- Same family as §4.1.36: **a fix that looks local widens its blast radius into places it cannot
  see** — there the blind spot moved out of the scan surface, here the drift moves into four copies.

## 2026-09-19 (whitelists become switches with two mandatory fields; C-33 measured at zero)

- **Every whitelist / registry entry now needs two mandatory fields: `why` (why it is not a leak —
  who declared it, at which line) and `reverify` (what must trigger a re-check).** The reviewer
  flagged the underlying hazard first: `TMP_DECLARED_PATHS` is **the only thing that can stop the
  shape leg from reporting**, so **a stale entry silently switches off one piece of coverage — and
  switching it off has no symptom at all** (indistinguishable from "0 hits" vs "never scanned").
  Same disease as the one discipline ⑥ covers, one level up: ⑥ says a reading needs its
  denominator; **⑩ says the denominator must be visible along with whoever turned it off.**
  * Worked example: `reme-helper-builddata` earns its place because `scripts/build.bat:22` declares a
    fixed path and the directory is rebuilt automatically — so its **re-verification trigger is
    "when that line changes"** (path moved, or no longer auto-rebuilt, or a cleanup was added ⇒ the
    entry is stale and the coverage it suppresses is already gone without anyone noticing).
  * Mechanical form: entries are structs (`{why, reverify}` for declared paths, `{prefix, why,
    reverify}` for `TMP_PREFIX_REGISTRY`), and **a missing field is now a red** (the old bare-string
    form counts as malformed). The failure message carries a paste-ready three-field sample instead
    of the old one-liner. `--temp-leak` prints **the number of active entries** and, for each,
    **both fields** — and it prints **all** of them, not only those currently present on disk,
    because an entry filters whether or not the directory exists right now.
  * New self-test legs with their own reverse cell: the real table must produce **0** problems (the
    validator is not just biting everything), a missing `reverify` must be caught, and the old
    bare-string form must be caught. Registry samples were updated to the three-field shape, with
    two new negative legs (`registry_bare_string_form_flagged`, `registry_missing_reverify_flagged`).
- **C-33 measured at zero red across the whole tree** (template channel + all four tools, and even
  the artificial `--roots my-diy-tool-template` invocation). Recorded in §4.1.20's evidence column
  together with both readings of the earlier batch — **the lead's "6 FAIL" and my measurement of
  "2 FAIL / 2 WARN by default, 5 self-hits under `--roots`"** — because readings must carry the
  ruler (§4.1.36) and because a later reader seeing "there were 6 FAILs" would otherwise conclude
  six real violations existed. **They were false reds: a mis-drawn exemption boundary, not tool
  defects.** None of them was a real finding.

## 2026-09-19 (C-38 changes shape: anchor at the startup line, one-shot lines do not count)

- **The first draft of C-38 would have gone green in the wrong place.** "The first N lines of the
  log must contain the data root" is **false-green by construction**: the reviewer measured the real
  logs — reme 6757 lines with 2 data-root lines (**first at #770**, 09-13), dsh 92 lines with 1
  (**#0**, 09-18), ocx 145 with 1 (**#0**), **l-s2t 284 with 0**. dsh/ocx's "compliance" came from a
  **one-shot `config migrated:`** line, i.e. it sat at the *oldest* end of the file.
- **Root cause:** `config seeded:` / `config migrated:` appear **only on the first seed/migration of
  a data root** — so *the one line that resolves attribution can never appear on a second start*.
  (`tmp0whlwvmi` could self-identify precisely because it was a **brand-new data root**.)
- **New shape, two clauses (lead's ruling, implemented):** ① the anchor is **the log line whose first
  string argument starts with `startup`**, and the data root must appear **within 20 lines after it**
  — **never the file's first N lines**, since an appended/rotated log's first lines are the *oldest*;
  ② **one-shot lines (`config seeded:` / `config migrated:`) must not count**, with a **negative
  sample** ("only a one-shot migration line ⇒ red"). The text also goes through `_masked_code_text`
  (prose does not count, §4.1.37), and the **anchors are printed in the detail** so a mis-identified
  anchor is visible.
- **Measured after the change: all four tools WARN** (dsh anchor `main.py:1763`, l-s2t `:1030` — both
  are the real boot lines, with no self-identification in the window; **reme's anchor is
  `main.py:7433 log(f"startup update check: …")`, a periodic check, not a boot marker** — its real
  boot line `:2897` prints a local `config={config}`, which cannot be read as a resolved path;
  **ocx has no anchor at all ⇒ unjudgeable**). **Unjudgeable is reported as WARN, not `[ok]`** —
  "green in the wrong place is worse than red". Six new self-test legs (1 positive + 4 negative +
  the anchor-shape cases) keep every clause of the new shape guarded.
- **Scheduled, not merged into this wave:** the actual "log the data root + config path on every
  start" line touches **four `main.py` startup blocks** and needs **one fixed format** (otherwise it
  grows five variants like the cmd guard did). The lead's reasons to defer: it is a **new gap**
  (all four red today), inserting a cross-repo format requirement now pushes the rebuild and #24
  further out, and its value is **retrospective** while the channel it replaces (session transcript)
  is already available and ruled on. ⇒ **This wave changes only the criterion and the docs**; the log
  line lands next wave, once, in one format. **Paste-ready sample and shape requirements: CONFORMANCE
  §4.1.38** — `log("data root: %s" % USER_DATA_DIR)` / `log("config   : %s" % CONFIG_PATH)`, placed
  within 20 lines *after* the tool's own `startup` line, printing the **resolved** values.
- **Also recorded:** reme's `config seeded:` line pointed at
  `…\release\reme-helper-1.0.7\config.json` ⇒ reme once seeded a config **from a very old release
  directory**. Filed as supporting evidence in §4.1.34: "a referenced orphan version is a state that
  must be handled" — this proves such references are not hypothetical, they already happened.

## 2026-09-19 (criteria read prose: C-33 false red fixed, C-30's second instance fixed)

- **`check_ping_tick` flagged its own docstring.** The explanation of *why* `ping -n 2` is banned
  contained the banned idiom, so the criterion read **prose about code** as **code**. Minimal
  reproduction (reviewer's): `#` comment green, `rem` line green, **docstring red**. Its five
  self-test legs were missing exactly the docstring one, so the false red stayed unnoticed until a
  real tree tripped it.
- **C-30 had a second instance of the same defect, measured here.** Its cleanup half searched the
  **raw** text for `rmtree(..., ignore_errors=True)`, and both `conformance_check.py`'s
  `_rmtree_strict` and `sync_check.py`'s `finally` **quote that banned old form in a docstring /
  comment** ("the author of C-30 has to obey C-30 itself") — i.e. **the instrument indicted itself
  on its own compliance note**. Two false reds under `--roots my-diy-tool-template`.
- **Fix, in four parts (template-only file; no dispatched file touched):** `_strip_docstrings()`
  blanks **bare string-expression statements** in the AST (language docstrings *plus* explanatory
  strings that are not first in a body; assignment/argument/concatenated strings are untouched —
  those are the rendered-bat templates and the criterion's own positive samples);
  `_masked_code_text()` masks comments **in place, preserving length and newlines**, for criteria
  that report `path:line` (C-30's registry key); C-30's cleanup half now scans the masked text;
  and the scan surface **excludes the instrument's own file by absolute path** and **prints the
  exclusion** (silent exclusion is indistinguishable from not scanning — same rule as C-30's
  per-root directory count).
- **The boundary, in the lead's words:** the "don't touch strings" exemption applies to
  **"code text that will be executed"**; docstrings/comments are **"text about code"** — both are
  STRING tokens, with different meaning. **This was a mis-drawn exemption boundary, not an
  implementation bug.** Same family as bare `mkdtemp()`'s "has a prefix or not" and C-22's "by file
  extension": **dividing exemptions by token type groups semantically different objects together**,
  so each such line needs a reverse cell.
- **New self-test legs (a missing leg is why the false red stayed green):** C-33 gains
  `ping_in_py_docstring_ok`, the reverse cell `ping_in_py_string_still_flagged` (the same sentence
  as a real string constant **must still go red**, proving the green comes from exempting the
  docstring, not the sentence), and `own_instrument_excluded_and_announced`; C-30 gains
  `prose_mention_in_docstring_ok` with the reverse cell `prose_mention_reverse_cell_flagged`.
  ⇒ **design discipline ⑨: every exemption boundary needs a self-test leg, and it needs a reverse
  cell.**
- **Measured after the fix:** C-33 green on the template (21 files) and on all four tools
  (22/24/43/25/32 files); C-30 green on the template. l-s2t's real `ping` tick was already fixed
  by ls2t-dev — `src/updater.py:233` renders `powershell … Start-Sleep`, and `:48`/`:225` are a
  comment and a `rem` line, correctly exempt.
- **Family reading after the batch: 1 FAIL / 2 WARN / 0 BROKEN** (reme C-27 `hold_exe_delete_guard`
  not yet wired; dsh and l-s2t C-38). **l-s2t's C-27 is gone** — ls2t-dev wired it in the meantime.

## 2026-09-19 (control-cell rule for verifiers; the cmd-idiom chapter is not inherited)

- **A criterion/verification script must carry a "control cell".** Folded into **C-22's docstring** and
  **CONFORMANCE §4.1.33** (both texts identical). The reviewer's own account: running only the
  *"VAR empty → abort"* cell produced the conclusion "this idiom always breaks"; adding the
  *"VAR has a value → must NOT break"* cell revealed that **the first failure was his own transplant
  artifact** — the guard region depends on its surrounding lines, so extracting it out of context
  changed its semantics. ⇒ Operational form: **a stand-in/extraction must be a minimal control, and it
  must have a reverse cell proving it "should not blow up (or should not go red)"** — minimal-variable
  method **plus** a control cell, or **the verification script itself will lie**. Same rule as
  "negative samples must cut both ways: a sample that is always red has no discriminating power".
- **STANDARDS §J gains a header note: the chapter collects *idioms themselves*, and does not assume they
  come from the template.** Evidence: `if defined X if "%X:~-1%"=="\" …` aborts the whole bat on the
  *"no instance running"* path — and **the template contains no such line**. Each repo hand-wrote its own
  guard. ⇒ The lesson outgrows the defect: **copy-based "one-of-five" comparison can only govern the part
  that gets copied**; the code *outside* the shared files has no authoritative original to compare against.
  That is a structural blind spot of the mechanism (same family as §4.1.18), and it is why per-repo
  verification has to be a probe run, not a diff.

## 2026-09-19 (C-2 lands as a mechanism; C-37 asserts it by measurement; two escape corruptions found)

- **C-2: "don't delete the running instance" stops being a discipline and becomes kernel-enforced.**
  `modules/paths/paths.py` **1.1.4** gains `hold_no_delete(path)` and `hold_exe_delete_guard(log=print)`:
  a handle opened **without `FILE_SHARE_DELETE`**. Measured by helpers-dev and reproduced here:
  `unlink` and `rmtree(<release dir>)` = **winerror 32**, `rename(<parent>)` = **winerror 5**, and the
  no-handle control **succeeds**. The failure direction is **loud** instead of "silently hollow out the
  directory while the instance is running in it". Lifetime = process lifetime (deliberately never closed,
  so no `finally` is needed). Hard requirements: taken **early, before any tray/window**; **fails open**
  (D3.2); **skipped in dev mode** (a handle on `python.exe` protects nothing).
  ⚠️ Boundary written into the clause: **an in-use marker inside the directory is detection only, never
  protection** — the marker sits *inside* the directory a blind delete removes, so it goes with it.
- **C-37 asserts the primitive by measurement, not by prose.** A new template-channel FAIL check:
  static half (the functions exist **and** the README declares `<!-- MUST-WIRE: hold_exe_delete_guard -->`
  — without it the four tools copy the code and never call it, which is exactly what C-27 exists for)
  plus a **property half** run on a temp file: while the handle is held, `unlink` and `rmtree(parent)`
  **must fail**; after release, `unlink` **must succeed** (the discriminating control — without it an
  implementation that can never open anything would pass). Selftest adds a **power sample**: a primitive
  with a share mode that **permits** deletion **must be caught** — a wrong share mode is invisible in the
  source, and only a real `unlink` can tell.
- **Two escape corruptions found in the docs, and my own byte check is why they hid.**
  `STANDARDS.md:492` held `System32<0x0c>ind.exe` (should be `System32\find.exe` — the row that
  documents the GNU-`find`-shadows-PATH pitfall, rewritten by the very pit it documents), and
  `CONFORMANCE.md` held `%TEMP%<0x0d>eme-helper-builddata` (should be `%TEMP%\reme-helper-builddata`).
  Both repaired **byte-wise**. The second exposed a gap in the check I had just written: it counted
  `CRLF` and lone `LF` and **never counted a lone CR** — so "mixed line endings" could hide in plain
  sight while the numbers said clean. §D7-10's EOL rule now demands all three counts.
  (Both were found only because a *comparable* claim existed — `ALIGNMENT §0`'s "0 occurrences of exotic
  whitespace" — which is the whole point of writing zero-claims down.)
- Also: **C-29 gains two "don't judge" samples** — `log=` given a *path* (`log_path`, `HELPER_UPDATE_LOG`)
  must be `[ok]`; those are l-s2t/reme's real shapes and flagging them is a false red. And two missing
  index rows were added to `CONFORMANCE §5.1` (**C-36 had never been registered there** — an index
  blind spot, this time mine).

## 2026-09-19 (C-30 leg B widened a second time; [BROKEN] tier; two of my own readings corrected)

Three corrections, all from the lead relaying the reviewer's measurements — and **two of them are
against me**.

- **C-30 leg B, second widening (1.9.2).** The previous signature still demanded `config.json`
  within depth ≤1 and looked for `*.log` **files**. The reviewer's real residue
  `tmp.6FcrxXYxmM\d\local-speak2text` (depth 3, **only `log/`**, no `config.json`) defeats both.
  The new rule was chosen **by measurement, not by argument**, on one scan (95 top dirs /
  647 entries): V0 old = **7** hits; V1 "`*.log` file at any depth" = **13** — and the 6 extra are
  **other programs' logs** (WebView cache `EBWebView/…/000003.log`, `vmware-Administrator`,
  `virtual_camera`, `kzip_sogou`, `ai/rp/task_outputs/…/output.log`) ⇒ **too wide, manufactures
  false reds**, rejected; V2 "a directory named `log` at any depth" = **8** ⇒ **adopted**
  (B3 says logs live in `<data root>/log/`, so "has a `log` dir" is the invariant). Residual FP =
  a foreign program's own `log/` (1 on the spot).
- **Declared locations are not leaks** (`TMP_DECLARED_PATHS`): `reme-helper-builddata` is a fixed
  path **written down** in reme `scripts/build.bat:22` (`REME_HELPER_DATA_DIR=%TEMP%\…`, no cleanup
  anywhere), and it was **permanently red**. The reviewer's control experiment gives the hard
  conclusion: **the shape leg can recognise a "data root", but cannot tell "belongs in %TEMP%" from
  "belongs on disk"** — so the leak verdict must come from **location + declaration**, not shape
  alone.
- **[BROKEN] is its own tier** (lead approved). A check that **raises** is instrument failure, not
  a detected violation: it now gets its own tag, **its own count** in the summary and **its own
  exit code** (otherwise it degrades into "a scary-looking WARN" that callers swallow). Origin:
  `check_md_tabs` kept a `@check` decorator on a helper that takes `Path` ⇒ four tools each
  reported an "exception", **looking like four broken tools**, and a whole round of investigation
  went the wrong way. §J records it as「幽灵判据」.
- **Two of my own readings, kept on the record**: (a) I reported the scan surface as "**643** top
  directories" — it was **entries** (dirs + files; **101 dirs / 634 entries**), and the surface is
  precisely the number two people must be able to compare, so `--temp-leak`'s RESULT line now
  prints **both, each labelled**; (b) the 20-name regression set is **self-calibrated** (the rule
  was calibrated on those names, then used to hit them) — that is **circular** and **not
  independent verification**, so "zero false positives" is withdrawn; the reviewer's independent
  re-implementation gives **14**. §J gains both as rows.
- Also in this batch: this file's own `selftest` now **consumes** `_rmtree_strict`'s return value
  (it called it and ignored the result — the very shape C-30 exists to catch).

## 2026-09-19 (C-36: assert the operator's *property*, not a frozen hash)

The lead's proposal, implemented as a check: **a property assertion is the mechanical form of
"the documented operator equals the implemented operator"** — no reader has to parse prose.

- **C-36 (template channel, FAIL)**: take any template `.py`, assert
  `sha256_text(LF) == sha256_text(CRLF) == sha256_text(CR)` **and** that it differs from a naive
  `split("\n")` control. Two clauses, both required:
  - the three-way equality is the *definition property* (**EOL-insensitivity**), independent of
    which sample file is used (freezing a literal hash would false-alarm the moment that file
    legitimately evolves);
  - the control is the **discriminating power** clause — without it, an operator that returns a
    constant would pass the first clause.
  Scan surface (discipline ⑥) prints operator name + sample file + all three variant hashes + the
  control value. Samples: the real operator must pass, and a **mutated operator**
  (`splitlines()` → `split("\n")`) must **fail** — that sample *is* the proof of discriminating
  power.
- **Why it exists**: the same口径 was described in prose twice, **incompletely both times** (first
  missing "trailing newline or not", then "normalize EOLs or not"). Each omission made a
  conscientious verifier compute a **false red** (`49b778fc7b26`, `e636cb41bf50`) while the
  copies were in fact correct. Prose and code are **two descriptions** of one rule, and the prose
  drifts first (the twin of discipline ⑦). Registered as **CONFORMANCE §4.1.24**; the first
  defence is `ALIGNMENT.md §0` now pointing at the single implementation.
- **Also in this batch: C-30's leg B was widened** after the lead reported fixed-name scratch
  dirs being missed. The old signature demanded "**exactly one** subdirectory", which is a
  *coincidental feature of the calibration sample*, not the invariant: synthetic shapes proved
  `log/{config.json,app.log}` hits while **“+ `ui-icons/`”** and **“`config.json` at top level”**
  both missed. New signature = `config.json` at depth ≤1 + any `*.log` under the top. Measured on
  the same day's 93 top-level dirs: old 4 hits → new 7, and the **3 new ones (`marker-e2e-*`) are
  previously invisible residue, not false positives**. Selftest samples updated (`two-subs` and
  `config-at-top` must now hit). Registered in **§4.1.17**.
- **And the batch's own accident, kept on the record**: while patching `_SHAPE_RULE` I used
  `read_text()` + `write_bytes()` and turned the 2968-line checker **LF-only** — the exact pair
  the §J row warns about, caught by byte read-back and repaired byte-wise. Third occurrence today,
  first one caused by me. Discipline did not stop it; reading the bytes did.

## 2026-09-19 (§B4 and §J each gain a positive example, and a naming discipline)

A rule that records only failures leaves behind deterrence and nothing else. Two edits, both
prompted by the lead after a reader **took a generic phrase personally**:

- **§B4's mirror counter-example now names the copiers** (dsh-helper and opencodex-helper, with
  the evidence that was already in the same paragraph: file mtime 16:09 vs my 16:06 edit, HEAD
  still `188bbcc`, eight files ` M`). The generic "实现者" was replaced because **a generic
  attribution of a fault makes every reader self-identify**: the tool that had done nothing
  wrong spent a round writing a rebuttal (l-s2t's evidence: its `log_kit.py` is still `VER
  1.0.2` with `def log(message)`, and `sync_check` reports `[lag] 1.0.2 -> 1.0.3` — i.e. the lag
  report is proof it *did not* copy), while the ones actually involved may read past it.
  **Discipline written in: name the fault or don't write it as a fault.**
- **And the same block now records the positive counterpart**: l-s2t **twice stopped at
  "uncommitted" and waited** (once before the i18n re-copy, once for `log_kit`) — exactly the
  behaviour the rule is meant to produce. Counter-example and positive example are a pair; a
  reader can now see **which step differs** between the two behaviours.
- **§J's stand-in signature row gains its positive half**: l-s2t's local `def log(*parts)`
  compatibility layer satisfies **both** 1.0.2 (single-arg closure) and 1.0.3 (print form)
  **without breaking anything to satisfy a check** — when the contract itself is evolving, the
  right move is **the union of the widths, not either one of them**.
- Byte evidence: `STANDARDS.md` CRLF=876 / LF-only=0 / TAB=0 / `sha256 83871832dd09313b`; C-28 `[ok]`.

## 2026-09-19 (design discipline ⑦: one rule, one implementation)

The lead turned a near-miss into a standing rule, and it closes a family this file has been
building all night:

- **⑦ "One matter, one check — never build a second, 'strengthened' copy."** Two implementations
  of the same rule **drift independently, each with its own false positives**, and end at "nobody
  knows which one to believe" — i.e. **the check itself becomes the new source of drift**. Sits
  beside the same family's "an index missing an entry is itself a blind spot" (§4.1.18).
- **The evidence is a refusal, not an accident**: while the reviewer's C-30 enhancement draft was
  still in flight, I declined to write my own "strengthened" prefix check — not to save effort, but
  because **two implementations of one rule give the contract two different rulers**. When the draft
  arrives it must be **merged into the single check**, not run alongside it.
- **Same family, second shape** (corrected by the lead the same day): mixing **a check's mechanism**
  with **a piece of forensic method** in one sentence. C-30 has read source from v1 (does the
  assignment's RHS contain `mkdtemp(`); "enumerate prefixes, then re-scan `%TEMP%`" is a
  **one-off measurement**, and the two belong in different documents — not in one sentence spoken
  in the voice of a second check.
- Landing rule: before adding anything, first ask **"does this already have an implementation or a
  draft?"** — if yes, extend that one (or wait for it); never run two side by side.
- Both copies updated: `CONFORMANCE.md` §5 (disciplines ①–⑦ in order, with the expansion) and this
  checker's docstring list, whose own first line says the index and the body must agree.

## 2026-09-19 (anchors: content hash *or* commit; §J gains the injection-lock row)

Three doc-level refinements, all from the lead, plus one row I earned the hard way.

- **§B4: the "copy the committed version" rule was a means stated as an end.** Replaced with the
  precise form: a declaration's **anchor is either a content hash (file sha256; normalized for
  `.py`, bytes for `.md`) or a commit sha (strictest: the `git rev-parse HEAD:<path>` blob id)**,
  and what actually holds the rule up is **anchor + drift detection** — `sync_check` is the drift
  detector, so reproducibility is guaranteed by *that*, not by the act of committing. Consequence
  written in: with a content-hash anchor and `sync_check` in place, **copies need not wait for the
  template to commit** (this is what unblocked #39); the strict form still stands, i.e. when the
  template does commit, the declaring side adds a line pointing the content anchor at that commit.
  The old wording in the same block ("the source must be the announced commit, not the disk at
  some moment") was updated too — leaving it would have contradicted the new paragraph.
- **§D7 item 10 (new): anchors and drift detection.** Three legal anchors, ordered by how absolute
  they are: revision + (when the worktree is dirty) file sha256 → answers "what was this repo at
  some moment"; **content hash** → git-independent and the best choice **across repos for the same
  template file**; **blob id** → strictly more absolute than "commit + line number" (it separates
  different worktrees of the same commit, makes the whole class of line-number drift disappear, and
  **equal content means an equal blob id across repos** — measured: dsh/ocx `update_helper.py` are
  both `fdc9f1b`). Plus the **`&&` discipline**: read the revision and take the evidence **in one
  shell invocation** — two invocations mean the revision and the evidence come from two different
  moments, which is just "evidence without a timestamp" written differently. And the pairing rule:
  **an anchor without drift detection is a sentence that will expire.**
- **§J: "the injection's precondition must be the one you meant to inject".** ls2t-dev caught
  himself: to reproduce "cannot delete" he locked the marker file, first with `share=0` — which
  **blocks reads too**, so the case actually measured "read fails" (something the real path never
  does). Correct: `FILE_SHARE_READ | FILE_SHARE_WRITE` (readable, not deletable; `FILE_SHARE_DELETE`
  is the permission bit that matters). Rule written as: **proving a failure was injected requires
  first proving that only the intended path is blocked** (the control read must succeed) —
  otherwise the red light points at the wrong repair target. Same family as "a stand-in must copy
  the production signature, no wider and no stricter".
- **And the §J escape row grew two new carriers, because I hit both while writing the row above.**
  ① Writing text that contains backticks through `python -c "…"` in a double-quoted shell string:
  the shell treats the backticks as **command substitution**, executes them and swallows the
  result — the line landed with **eight code spans silently emptied**, looking merely mis-formatted.
  ② `Path.read_text()` + `write_bytes()` **normalised the whole 867-line file from CRLF to LF-only**
  (read normalises, write does not restore). Both were caught by reading the bytes back, which is
  the only thing that does catch them — and the same session had already written "the only defence
  is mechanical read-back" into that very row. Five instances of this pit in one day now.
- Byte evidence: `STANDARDS.md` CRLF=867 / LF-only=0 / TAB=0 / `sha256 1954399b66638586`; template
  channel re-run: C-28 `[ok]` (`0 FAIL, 0 WARN`).

## 2026-09-19 (design discipline ⑥: "0 hits" and "nothing to hit" must look different)

The lead promoted a defect I hit while writing C-30 into a standing rule, and it is the third
face of a family this file already carries:

- **⑥ "A check reporting ok / not-applicable / 0 hits must print its scan surface"** (which
  paths, how many candidate sites, how many hits). **"I found nothing" and "I did not look"
  are indistinguishable in the output** — the shape this family keeps tripping over.
  ④ covers the **input shape** ("unrecognised ≠ violation"), §4.1.18 covers the **scope**
  ("the check exists ≠ the object is in range"), ⑥ covers the **coverage** ("no hit ≠ fine").
  Together they are the whole output side of a check.
- **The evidence is mine, and it is a near-miss worth keeping**: C-30 v1 only recognised the
  bare call `X = mkdtemp(...)`, so reme's `root = Path(tempfile.mkdtemp(...))` was **silently
  skipped** — **the one file that most needed checking was reported as "this check does not
  apply"**. After switching to "the assignment's right-hand side contains `mkdtemp(`" plus
  wrapper call sites, the real tree went to **reme 1 / l-s2t 9 / dsh 6 / ocx 6**.
- Landing requirements written into the rule: ① ok/not-applicable branches must print the scan
  surface (`--temp-leak` is the model: `%TEMP%` path / top-level dir count / prefix count /
  per-leg hit count / union); ② **samples must assert that number**, otherwise "scanned 0 files"
  disguises itself as green; ③ **a first run reporting "not applicable / 0 hits" is a suspicious
  signal, not a green light.**
- Both copies updated in the same edit — `CONFORMANCE.md` §5 (disciplines ①–⑥ in order, with the
  expansion) and this checker's module docstring list (the index there says of itself: "索引缺条目
  本身就是文档说谎", so leaving it at ①–⑤ would have been the very defect it describes).

## 2026-09-19 (freeze wave: the four LF files, `update_helper` 1.4.3, `autostart` 1.1.2)

Three defects that a *copy* amplifies, plus the CRLF conversion they have to travel with.
This is the **template side** of the wave only — the four tools are re-copied in the same
wave (change everything → freeze → announce; an announcement followed by another template
edit has to be re-issued naming what changed).

- **C-31's first-run finding is fixed, not just reported.** The four LF-only dispatched files
  (`modules/autostart/autostart.py`, `modules/icons/icons.py`,
  `modules/service_link/{README.md,service_link.py}`) were converted to CRLF **byte-wise**:
  `read_text()`/`write_text()` would have "fixed" the file while silently rewriting the very
  bytes under comparison (that pair normalises on read and translates `\n` on write — the
  exact mechanism that corrupted two files earlier tonight). C-31 now reports **27/27
  dispatched `.py`/`.md` CRLF**; before the conversion it was 4/27.
- **`update_helper` 1.4.3 — the sweeper could not see one of its two products.**
  `TEMP_PREFIX` carried a trailing `-` (`f"{APP_ID}-update-"`), so `glob(…-update-*)` never
  matched the replacement script `…-update.bat` (fixed name), and the cleanup branch only
  handled `is_dir()`. Every interrupted update therefore left one more `*-update.bat` in
  `%TEMP%` **permanently, and silently**. The prefix now stops at `-update`; the sweeper
  unlinks files as well as removing trees, age gate unchanged. Positive/negative control with
  a redirected `TMPDIR`: 3 stale artefacts removed, 2 fresh ones untouched.
- **`autostart` 1.1.2 — self-heal was silent where it should speak, and blind where it should
  see.** ① A missing `Run` entry and a failed registry read were swallowed by the same
  `except (FileNotFoundError, OSError): pass`, so "the user turned autostart off" and "we
  cannot read the key" printed exactly the same thing — nothing. *Not* creating an entry stays
  the rule (creating one would re-enable autostart the user disabled); each case now logs its
  own line, and neither writes to the registry. ② The dead-link test was
  `value != wanted and not os.path.exists(value.strip('"'))` — the `value == wanted` half
  short-circuits, and `strip('"')` can never resolve a **source-form** command line
  (`"…\pythonw.exe" "…\main.py"`), so *any* difference between the registered and the current
  command meant a pointless registry write on every start. The judgement is now "does every
  path in the command line exist" (`_cmd_targets` / `_cmd_alive`), and after rewriting we
  **re-read** the new target: if that is missing too, we say so instead of claiming
  `migrated`. Evidence: `H:\Tools\_verify-scratch\autostart_migrate_test.py` (fake `winreg`,
  the real registry is never touched) — **14/14 on 1.1.2**, and the same harness pointed at the
  pre-fix revision (`git show 33e99ff:…`) fails the silent / spurious-write cases. That
  difference is what makes this a measurement rather than a claim.
- **`service_link/README.md`**: the opencodex-helper "exit-signature kill" is recorded as a
  **historical** counter-example (already fixed) — ocx uses a checkbox, unchecked by default.
- Registered as **CONFORMANCE §4.1.21** (sweeper prefix) and **§4.1.22** (autostart self-heal);
  the `autostart.py` version row in §1 went 1.1.1 → 1.1.2 so C-04 stays honest.
- **CONFORMANCE §1 (L1) was audited against disk and was wrong in 6 of 9 rows** — the table
  declares "对外接口（稳定承诺）" and carries a version column, but **no check has ever watched
  that column** (C-04 only reads the tools' B2 table; the template channel only runs
  C-28/C-31/C-32/C-33). Worst offenders: `update_helper` **1.0.1 vs 1.4.3** and `tray_kit`
  **2.0.1 vs 2.2.0** — a reader would interpret the interface by the semantics of a version
  that is three releases old (1.0.1 is exactly the "two silent failures" revision from the B4
  arbitration rule). All rows now carry the on-disk `TEMPLATE-VER`, a `conformance_check.py`
  row was added (the table listed `sync_check` but not the checker that runs the table), and
  `paths.process_pending_update()` is marked deprecated. Registered as **§4.1.23**, with a
  proposed **C-34** (assert table version == file header) so the column cannot drift again —
  proposed, not implemented, so this batch stays scoped.
- **§J gained the read-only-bit row** (lead's re-measurement, after his own misstatement): the
  read-only attribute is **partial insurance, not a structural guarantee**. Measured: it stops
  `os.remove` / `del` / `shutil.rmtree` (`PermissionError`), but **not** `rmdir /s /q <parent>`
  (rc=0, directory gone) and **not** `robocopy /e /purge` (overwrites and clears the R bit,
  mode → `0o100666`). Positioning: it protects the delete-the-stand-in path only, and **cannot
  replace** R1 (stand-in always exists) + the `start` existence guards + the timeout-is-red
  rule. The row also records ls2t-dev's two implementation details: use `os.chmod(...S_IREAD)`
  rather than spawning `attrib.exe` (a console child flashes a black box — the family's own
  accident class), and clear the R bit recursively before cleanup because **robocopy copies it
  into snapshot/backup dirs** (they really went red on this once — hardening that introduces a
  new failure, so hardening needs its own self-proof).
- **Same row, self-applied**: my first wording said `_readonly_selfproof()` turns the whole
  boundary table into an executable control. Reading the function back showed it asserts **only
  the `del`/`unlink` row**; the `rmdir /s /q` and `robocopy` rows are measured once and
  documented, i.e. **evidence, not guarantee**. Corrected in place — claiming full coverage
  from a one-row control is exactly "partial coverage described as a structural guarantee",
  which is the lesson the row exists to record.
- One near-miss worth keeping: I "tidied" `service_link`'s `.spectators` into `.spectators()`
  out of habit; reading the source back showed it is a **plain attribute** (`self.spectators
  = []`), so the cell was restored with an explicit "(属性，非方法)" note. Same rule as §D7
  item 8 — enumerate the signature, never guess it.

## 2026-09-19 (identity line; `conformance_check` 1.9.1)

One line, printed by the tool about itself:
`# conformance_check 1.9.1  sha256:<raw>  norm:<normalized>  head:<short-sha>`.
`head` degrades to `?` when git is unavailable, not in a repo, or slow — an identity line must
never be the reason a check crashes.

- **Why**: tonight the *same* disagreement happened **three times** (`tray_kit` version, the
  `183`-line guard, C-11) — "which revision produced this output?" — and every time it was
  settled by hand, by comparing revision ids. An identity line lets any pasted output **prove
  its own identity**: the first line says whether it came from a stale snapshot or from the
  file on disk. It is also R-EVID **automated**: R-EVID asks evidence to carry its own
  timestamp; making the tool print its own identity is more reliable than asking every person
  to remember to paste one — structure instead of discipline.
- **Computed at runtime, never hard-coded**: a frozen hash string would itself go stale, which
  is exactly the failure mode this fixes.
- **Both hash families are printed on purpose**: `sha256` over the raw bytes, and `norm`
  (the `sync_check` normalization: drop `# TEMPLATE-*` lines, then hash). The family publishes
  both (`.py` comparisons use `norm`, `.md` uses bytes; ALIGNMENT §0 pins the operator), and
  printing only one invites someone to check it against the other and conclude "it does not
  match" — the same two-families trap already recorded there.
- Printed in both modes (normal run and `--selftest`), because a self-test result pasted
  without provenance is as ambiguous as any other evidence.

## 2026-09-19 (C-30 grew a coverage-gap alarm; `conformance_check` 1.9.0)

A check whose coverage can be switched off by renaming a literal to a variable is worse than
the leak it was supposed to catch. C-30 v1 only asked "is the cleanup of a mkdtemp root
verifiable?" and never asked **where the prefix came from**.

- **Prefixes are enumerated from source, never guessed.** `mkdtemp(prefix=...)` arguments are
  read via AST — including the **call sites of wrapper functions**: `tests/_cleanup.py` is
  `def scratch_dir(prefix): return mkdtemp(prefix=prefix)`, and dsh/ocx/l-s2t all pass their
  real prefixes as literals at the call sites. Judging the callee alone would paint all three
  red. (Guessing was already disproven twice: `opencodex-*` guessed vs `ocx-*` real — zero of 42
  matched; a `*/log/*.log` shape signature then missed ~14 more.)
- **Opaque prefixes must be registered, or the check goes red.** f-string / variable / missing
  `prefix` sites must appear in a module-level literal
  `TMP_PREFIX_REGISTRY = {"<relpath>:<lineno>": "equivalent-prefix"}`. Both the check and the
  runtime forensics read that table. A registry value that is not a literal is **red** (the check
  cannot read it, so it is a registration in name only); an entry that no longer matches any site
  (line drift) is **WARN**. Otherwise `prefix="reme-x-"` becomes `prefix=name` and silently
  leaves the coverage — the check would be able to disable itself.
- **The cleanup half now scans the whole tool, not just `tests/`.** That immediately surfaced
  **reme `src/main.py:7409`**: `work = Path(tempfile.mkdtemp(prefix=f"{APP_ID}-update-"))` at 7405,
  then `shutil.rmtree(work, ignore_errors=True)` on the download/verify early-exit path. Same
  defect, production code, previously invisible.
- **Acceptance is an increment, not a state.** `--temp-leak` lists `%TEMP%` hits (read-only,
  always exits 0 — historical residue must not paint it red); `--temp-leak-save` records a
  baseline and `--temp-leak-baseline` reports red **only on directories that appeared while the
  gate ran**. "Just clean it once" is not evidence — it is a single point in time. So is any
  measurement that finds residue: at 16:11 dsh's three leftovers were stamped 16:11 (the gate was
  running, so they were being produced then), while a later re-scan of the same 19 prefixes found
  **0 hits**. Both readings are true of their own moment; only the increment assertion can settle
  whether the leak still reproduces.
- **The runtime forensics grew a second leg, because prefix enumeration has a structural
  ceiling** (its coverage can never exceed the prefix literals in the scanned source). Measured
  on this machine: leg A (generator-derived prefixes) found **0**, while leg B — a name-agnostic
  **shape** signature — found **20**. Those 20 names (`icon-probe-*`, `smoke-proof-*`,
  `reme-gate-2.2.0`, `tmp*`) appear **nowhere** in the four tools' sources: some are bare
  `mkdtemp()` (system default prefix `tmp`), others come from probe scripts outside the scanned
  roots. "Leg A found nothing" and "there is nothing" were **the same output** — a check that
  could quietly go green. Shape rule, calibrated against the real objects:
  `<top>/<exactly one subdir>/config.json` **plus** any `*.log` under `<top>` — with
  "log must be non-empty" it would only have covered 11/20 (the rest have 0-byte logs; an empty
  file is still residue). The 20 are registered as the negative-sample regression set, and
  `--temp-leak` now always prints its **scan surface** (temp path, top-level dir count, prefix
  count, hits per leg), so "nothing found" can never again be confused with "nothing scanned".
  Bare `mkdtemp()` moved from FAIL to WARN in C-30 (derivable but weak — leg B is its real
  judge).
- **Opaque prefixes got a cheap second path: foldable module constants.** `APP_ID = "reme-helper"`
  plus `prefix=f"{APP_ID}-update-"` *is* derivable — constant-folding (module-level string
  literals only; a name reassigned or assigned a non-literal makes it unfoldable, "when in doubt,
  do not guess") turned reme's site green without asking anyone to write a registry entry. The
  remaining rule is two-state, as the reviewer upgraded it: **unregistered → FAIL, registered →
  OK** (leaving it at WARN would let "rename the literal to a variable" downgrade a FAIL to a
  WARN while the leak stayed). After folding, C-30's only real-tree red is reme's
  `rmtree(work, ignore_errors=True)`.
- **The template's own `.md` are now scanned too (C-28 pass over the template repo, once).**
  It turned out `main()` excluded the template with `d.name not in {..., TEMPLATE_DIR.name}`, so
  C-28 had never looked at the very files every copy descends from — **"a check exists" is not
  "the checked object is in scope"** (CONFORMANCE §4.1.18). Worst instance of the class: the
  C-28 rule text itself had **two real TABs** in its own CHANGELOG entry — the author meant the
  two characters `` `\t` `` and wrote a real TAB instead — and it was already in `HEAD`
  (`188bbcc`). *The document describing the trap had fallen into it.* The template pass runs
  through the new `TEMPLATE_CHECKS` registry (once, not once per tool).
- **New C-32 (FAIL): no "read the evidence -> delete the evidence -> report it" order.** The
  irreversible step must not precede a statement whose *call boundary* can fail: arity/signature
  mismatches, missing attributes and undefined names are raised **before** the callee's body runs,
  so the callee's own `try/except` cannot protect you — that is exactly how l-s2t really blew up
  under the C-29 contract conflict (TypeError + marker already deleted + the notice gone). The
  lead's first phrasing ("irreversible actions must come after every statement that might raise")
  was rejected as too wide: `log_kit.log()` swallows everything internally and **never raises**,
  so it would have reported `quit_watch_loop`'s `unlink -> log` five times. Final narrow form
  (the reviewer's third try, all three conditions at once): **D** a delete (`unlink/remove/
  rmtree/rmdir`) with receiver `rcv`; **A** *any* earlier assignment in the same function whose
  right-hand side **contains** `read_text`/`read_bytes` and whose receiver is **AST-identical**
  to `rcv`; **R** a later `log` call referencing A's name. Seven samples. Why the qualifiers had
  to be re-validated one by one (design discipline ⑤, now in CONFORMANCE): adding "same
  statement block" missed the canonical case entirely (0 hits); adding "the most recent
  assignment" landed on the `detail = ""` inside `except` (two assignments to one name) and got
  4 hits, **missing reme**; only "any earlier assignment" reached 5/5 true, zero false positives.
  The detector also needed to inspect the assignment's **right-hand side root**, not just its
  descendants — `detail = marker.read_text()` is a read when the call *is* the RHS, which the
  first version skipped (found by the sample, not by luck). Live findings: template + **dsh +
  ocx** `update_helper.pop_failed_update_note():385 -> 386 -> 390`; l-s2t and reme are already
  fixed (report first, delete last). Fixing the template implies the same "re-copyable freeze"
  constraint as C-31 for the dsh/ocx copies.
- **`ping -n 2 127.0.0.1` is not a one-second sleep, and the wait loop was lying about it.**
  On a machine that drops loopback ICMP (this one), each packet waits out the full timeout:
  `cmd /c "ping -n 2 127.0.0.1"` measured **9.04 / 9.00 / 9.00 s**. So the "1 s" tick was 9 s, the
  `UPDATE_WAIT_LIMIT = 120` "120 seconds" was ~18 minutes, and `:giveup` still logged
  `still running after 120s` — a log that lies. Same line shipped in the template plus four
  copies (dsh/ocx `update_helper.py`, l-s2t `updater.py`, reme `main.py`; reme also has
  `ping -n 9` in `scripts/build.bat`). The template now ticks with
  `powershell -NoProfile -Command "Start-Sleep -Milliseconds 1000"` (ICMP-free; launched from a
  DETACHED process it inherits no console, so no window appears; measured 1.29 s per tick
  including PowerShell startup), splits the constants into **polls** (`UPDATE_WAIT_LIMIT`) ×
  **ms per tick** (`UPDATE_WAIT_TICK_MS`) = nominal budget (`UPDATE_WAIT_BUDGET_S`, a **lower
  bound**), and the timeout line now reports `%tries% polls x {tick_ms}ms` instead of a "seconds"
  figure nobody measured. New mechanical check **C-33** forbids `ping` as a wait tick (comments
  and `rem` lines excluded — the thing to catch is the executed tick, including the one rendered
  from a `.py` string template); `sync_check.py`'s bat-semantics assertion follows. Same family as
  "robocopy rc=0 means *nothing was copied*": **every unit assumption in a wait/timeout must be
  measured, not assumed.**
- The tool now obeys its own rule: the selftest scratch dir is removed with `_rmtree_strict`
  (delete, read back, raise on failure) instead of `rmtree(..., ignore_errors=True)`.
- First run on the real tree: C-30 is 1 FAIL (reme, both halves), other three tools green.
  Samples grew to 11 (7 prefix + 4 cleanup), selftest ALL PASS.
- **New C-31 (WARN, template-only): dispatched `.py`/`.md` must be CRLF throughout.** C-22 only
  covers `.bat`/`.cmd`, so a dispatched `.py`/`.md` rewritten with LF line endings by an editor
  passes every layer — `py_compile` is green, and `sync_check` is green too (both sides LF, the
  normalized hashes still match). That is exactly how `log_kit.py` was caught: by reading the
  bytes back, not by a check. Since the template is copied, the template's line endings become
  the four tools' line endings. A new `TEMPLATE_CHECKS` registry runs template-scoped checks
  **once** (they describe the source, not any one tool), so C-31 does not print the same row four
  times. Scoped to `modules/**` `.py`/`.md`, excluding the template-only `build_release/` and
  `baseline/`. Four samples (CRLF ok / LF-only / mixed / template-only dir not flagged).
  First real run: **4 of 27 flagged** (`modules/autostart/autostart.py`, `modules/icons/icons.py`,
  `modules/service_link/README.md`, `modules/service_link/service_link.py`) — and the tool-side
  copies are LF too, so normalizing is a "re-copyable freeze" event (template + every affected
  copy in one wave); changing only the template would turn those copies into `[DIFF]` at once.

## 2026-09-19 (log contract: two shipped modules disagreed; `log_kit` 1.0.3; new C-29)

Two dispatched modules said different things, and **three tools each hid it in their own way**.

- **The conflict**: `update_helper` calls `log` in print form — 7 call sites, up to 5 positional
  arguments (`log("downloading", stem)`, `log("update staged:", staged, "->", target, "(bat %s)" % s)`).
  `log_kit.make_logger` handed out `def log(message)`: one argument. Wire the second into the
  first and it dies with `TypeError` on the lines you cannot avoid — every download (L407),
  every successful hand-off of the replace script (L257), every stale failure marker (L390).
- **Why it stayed invisible**: dsh wrote `def log(*parts)` and ocx wrote `def _log(*parts)` —
  both absorbed the mismatch, and dsh's docstring even says "模板 log_kit 待统一". l-s2t wrote a
  **narrower** `def log(message)` yet still passed `log=log` to template modules. Three local
  wrappers, three private accommodations: at the template level, nobody could ever see that two
  shipped modules contradicted each other. Same shape as the "majority is a false judge" rule in
  B4 — three accommodations look like consensus and are just three workarounds.
- **Fixed**: `log_kit` 1.0.3 makes `log(*parts)` (space-joined `str(part)`), matching its callers.
  The `log=` contract is now written into the `log_kit` / `update_helper` / `tray_kit` README
  interface tables (a dispatched file, so the four tool copies need a re-copy).
- **New C-29** makes it mechanical: a `log=<name>` handed to a template module must resolve to a
  tool-code definition that takes varargs. First run on the real tree flagged **l-s2t**
  (`src/main.py:80` plus `log=log` at `231`/`998`/`1043`). The defect was then **measured**, not
  inferred: a one-argument `log` passed to `launch_pending_cmd` / `pop_failed_update_note` raises
  `TypeError` on template lines L257 / L390, while a print-form `log` runs clean.
  Deliberately *not* judged: names that are not tool-code function definitions — reme's
  `log=HELPER_UPDATE_LOG` is a **log file path** handed to the bat template, and firing on it
  would be a diagnosis that contradicts the facts.
- Three samples (`varargs_log_ok` / `single_arg_wired_flagged` / `single_arg_unused_ok`); selftest
  is ALL PASS. STANDARDS §J gains "a more permissive stand-in hides contract conflicts — copy the
  production signature, err on the strict side".

## 2026-09-19 (C-11 false red fixed: recognize the PowerShell form, and WARN when unrecognized)

Same class as the C-10 false red, found the same way: dsh/ocx do their running-instance check
with **PowerShell `Get-Process -Name <APPNAME>`**, while C-11 only looked for
`tasklist | findstr` — so it reported "未找到运行检测" about tools that plainly have one.

- **Two forms recognized now**: `tasklist | findstr /c:"..."` and `Get-Process -Name <name>`;
  the match string is validated against `<APPNAME>.exe` either way.
- **Unrecognized ⇒ WARN, not FAIL** — and the framework now supports per-branch severity
  (`(ok, detail, "WARN")`), so "can't judge" no longer gets reported as a hard violation
  (design rule ①). The WARN message tells the reader to add their form to the check.
- Two samples: `neg_unrecognized_is_WARN` and `pos_powershell_form`. Real tree: **four tools ok**.
- **A fifth bite from the same J-坑**: writing these samples, `
` inside heredocs turned into
  real bytes twice more (broken comment, split literals). Both are now built with explicit byte
  values (`bytes([13, 10])`); the harness rules in §D7 cover the family of causes, and this is
  now the fourth distinct occasion in one day.

## 2026-09-19 (C-10 false red fixed on reme; C-28 .md TAB probe)

The lead found C-10 reporting a **false red with an inverted diagnosis** on reme, and both
halves of the analysis were right.

- **Root cause, precisely**: reme's `smoke()` is *correct* — the probe is passed as an argument
  to a `check(...)` helper — but (a) my "consumed" rule only counted probe calls inside
  `if`/`while`/`assert` tests, so it scored `guarded=0, plain=0`, and (b) the fallback branch
  matched the guard names **as text over the whole function body**, where line 7563 has them
  **inside a comment** (`别用它 single_instance_free()`). So it printed "smoke 里是**真跑守卫**"
  about a function that has no guard call at all.
- **Fix**: "consumed" now means **the return value is used** — a bare `ast.Expr` call is
  `plain`, everything else (condition, `assert`, boolean op, **argument to a helper**,
  assignment) is `guarded`. The guard fallback now looks for **AST call nodes**
  (`_calls(fn, _GUARD_NAMES)`), never text. Same lesson as before: a comment must never be able
  to change a verdict.
- **Two samples added, named for the two failure modes**:
  `pos_probe_passed_to_check_helper` (must pass) and `pos_guard_name_in_comment_only` (must
  pass — reme's exact shape), plus `neg_real_guard_ast` (a real `acquire_single_instance` call
  node still fails). Real tree: **all four tools ok**, reme included.
- **C-28 (WARN)**: `.md` files must not contain 0x09. The lead's ruling: do **not** widen it to
  every text file (`.py` indentation, `.json` escapes are legitimate), but a hand-written CJK
  doc with a TAB is always an accident — which is exactly the incident I hit when a `\t` inside
  a Python string landed in CHANGELOG.md as a real TAB. Positive/negative samples included.
- **That J-坑 recurred twice more while writing this very entry**: the heredoc turned my
  `\t`/`

` into real bytes twice (once inside the C-28 sample itself, once in a comment
  about it). Both were caught by reading the bytes back and are now written with **explicit byte
  values** (`bytes([9])`, `bytes([13, 10])`). Three occurrences in one day, all in code that was
  *about* this hazard.

## 2026-09-19 (E group: the second reachable path — empty snapshot — now runs for real)

The lead traced a second route to the same modal-box hang: `:install_failed` is entered when
the *copy* fails, and the **restore** can then "succeed" while copying nothing (the snapshot
step returns 0 for an empty install dir — the same robocopy semantics again), so the old
`errorlevel 8` test passes and the script starts an exe that is not there.

- **The guard for that branch shipped in 1.4.2** (`if not exist "{newexe}" goto install_dead`,
  generated line 70) — the line numbers quoted in the review are 1.4.0's.
- **New runtime case** (`sync_check.py` 1.8.2, E group): STAGE passes the pre-copy check but the
  copy is **failure-injected** (`goto install_failed`), TARGET has no exe and SNAPSHOT is empty.
  Four assertions, all green in **0.4s**: it exits (a modal box would hang it), the log shows
  `RESTORE FAILED` — i.e. it really reached `:install_dead` — **no exe was started**, and the
  marker plus the work dir are kept for a human. A static keypoint also pins the guard's
  position (after `:install_failed`, before that `start`), so the reverse sample reports it.
- **Same trap, twice**: the selector for the injection first looked for the *expanded* stage
  path in the script body — but the body contains `%STAGE%`. The harness note is in the code.

## 2026-09-19 (paths deprecation notice; i18n 2.2.0 — LANG becomes a derived read)

Both rulings from the lead, executed.

- **`modules/paths/README.md`: `process_pending_update()` marked deprecated** with the reason
  spelled out (no rc check; on failure it `unlink`s the pending file and deletes `UPDATE_DIR`,
  destroying the staged source *and* the evidence) and the three-step disposal plan
  (notice → land the stable-install mode in `update_helper` and switch l-s2t off its fork →
  delete the function and `UPDATE_PENDING`, 5-way cascade; steps 2 and 3 do not interleave).
  The audit stands: zero live callers today, so urgency is low — but it ships inside four
  copies and the document used to promise it.
- **`i18n` 2.1.1 → 2.2.0: `LANG` is no longer a rebindable module global.** State moved into
  `_STATE` and `LANG` is now **derived by a module-level `__getattr__`** — there is no scalar to
  rebind, and `from .i18n import *` cannot carry it (`import *` does not move derived names), so
  the defect that cost us a menu that never refreshed **cannot be reproduced structurally**.
  This is the same shape `update_helper` 1.4.0 adopted; C-23 flagging all four tools is what
  showed it was a *template-level* form problem rather than one tool's slip.
  Reverse proof: `LANG in vars(package)` → False, `LANG in vars(submodule)` → False, and
  `init('en')` still flips `LANG`/`current_lang()`/`t()` immediately.

## 2026-09-19 (C-25/26/27: three clauses for the day's defects; update_helper 1.4.2)

Four defects surfaced today that **none of the 76 existing clauses could catch**, so three of
them are now mechanical checks (C-22, the byte one, shipped earlier).

- **C-25 门禁步骤必须"既存在又能被执行"** — an invocation whose path is missing is a FAIL
  (reme's `build.bat:201` was `tests<TAB>est_update_bat.py`: the whole gate never ran, and with
  D1-01 ahead of it, it never even got the chance to fail). A call sitting after a **top-level**
  unconditional `exit /b` / `goto :eof` is also reported as dead code; `exit /b` inside an
  `if (...)` block is *conditional* and does not count — the first version flagged every tool's
  normal gates, which is exactly the false red the discipline warns about.
- **C-26 `start` 前必须存在性守卫** — `robocopy` returning rc 0 means **"nothing copied, no
  error"**, so "only exclude >=8" calls an empty stage a success and the following `start`
  points at a missing exe: a GUI-subsystem modal box that `DETACHED_PROCESS` cannot suppress.
  Every `start "" "<path>"` needs an existence guard. It scans **`.py` templates too** —
  the update bats are rendered, so scanning only `.bat` files found nothing (first version
  reported "no start calls" for all four tools).
- **C-27 采纳 = 拷贝 + 接线** — a module README declares `<!-- MUST-WIRE: symbol -->`; the
  checker looks for the symbol **in tool code** (`src/**/*.py`, excluding the copied module
  and `__init__.py` re-exports). `sync_check` saying `[ok]` only proves the files were copied:
  dsh/ocx had `sweep_stale_update_dirs` / `pop_failed_update_note` **only in the README they
  copied**, with zero code references. Declarations are read from the **template** copy so the
  requirement takes effect immediately instead of waiting for a re-copy. It now fails dsh/ocx on
  `launch_pending_cmd` only — which is exactly pending tasks #27/#28.
- **`update_helper` 1.4.1 → 1.4.2**: the reviewer found the **third** unguarded `start`
  (`:install_failed`, after the restore). rc<8 means "the restore did not error", not "the exe
  is there" — a snapshot can be missing it. Every branch reaching a `start` must verify on its
  own; a guard elsewhere does not prove this one. (C-26 as written still accepts a guard
  *somewhere* on the flow — path-specific reachability needs control-flow analysis; the runtime
  E-group sample covers the empty-stage path end to end.)
- **The E group caught my own violation**: the first version of that new comment block was
  written **in Chinese inside the ASCII-only bat template** — `E ASCII-only` failed. The rule
  I spent the day enforcing is enforced by the asset, on me.

## 2026-09-19 (update_helper 1.4.0 → 1.4.1: the failure paths now preserve the scene alike)

The lead's task text asked for "不启动 + 写 marker + **保留现场**". Re-reading my own
`:stage_invalid` path against that wording found a real inconsistency: it wrote the marker but
went to `:cleanup`, which **deletes the staged package** — while `:install_failed` keeps it.
Same failure class, two different treatments, and the one that discarded the evidence was the
one where the evidence is most interesting ("what exactly was staged?").

- **`:stage_invalid` now goes to `:cleanup_keep`** (1.4.1): the staged package survives for a
  human; only the poll file and the script itself are removed. The 1-hour
  `sweep_stale_update_dirs()` still reclaims it, so this costs disk for at most an hour.
- **E group follows** (`sync_check.py` 1.8.1): the runtime assertion flips from "work removed"
  to "**work preserved**", and a static keypoint pins `goto cleanup_keep` inside the
  `:stage_invalid` block. Reverse sample still reports it as missing.
- VER bumped because the bytes changed; the previous "no change, keep 1.4.0" announcement is
  superseded by this commit (file-level, see the hand-off list).

## 2026-09-19 (update_helper: the empty-stage reverse proof now runs the bat for real)

The lead's review asked for a runtime reverse sample for the two `start` sites (empty stage ⇒
`robocopy` rc 0–7 ⇒ judged success ⇒ install dir wiped ⇒ `start` on a missing exe pops a
**modal** box that `DETACHED_PROCESS` cannot suppress ⇒ the bat blocks forever).

- **The guards themselves shipped in 1.4.0** (`7d0d000`) and are unchanged: the staged package
  is validated **before** anything is touched (`goto :stage_invalid`), and the post-copy path
  checks the exe again (`if not exist "{newexe}" goto install_failed`). No module change was
  needed, so **`modules/update_helper/` stays at 1.4.0** — bumping the VER without changing the
  bytes would make the declared version lie about the file.
- **New runtime reverse sample** (`sync_check.py` 1.8.0, E group): the generated `apply.bat` is
  written into a `%TEMP%` sandbox and **executed with an empty stage**, asserting five things:
  the script exits in well under a second (a modal box would hang it), it writes
  `update.failed`, **the install directory is untouched** (`/purge` never ran), the work dir is
  removed (it reached `:cleanup`), and the script deletes itself. The sandbox's install dir has
  **no exe**, so nothing gets launched — but note a missing path still pops the "Windows cannot
  find" modal and blocks forever (a dialog depends on the *path*, not the directory); if the
  guard ever fails, this case hangs, which is exactly what its "exits in 0.3s" assertion
  catches. Measured: `0.3s`, all five green.
- Why this had to be a run, not an assertion on the text: the text assertions can only show the
  guard is *written*; they cannot show the path is *blocked*. The failure mode is a GUI-subsystem
  dialog, which no process flag can suppress — the only observable is "it never returns".
- **Semantics note**: `:stage_invalid` does not touch the install dir, writes the marker, and
  then **brings the previous version back if it exists** (same as `:install_failed`). "No start"
  refers to the missing *new* exe; the old one is what the user gets back, so the tool is not
  left dead. The second guard ends in `:install_dead` (no start at all) when the copy is bad.

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
