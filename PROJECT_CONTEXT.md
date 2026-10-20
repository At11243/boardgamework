# TSWW Barbarossa project context

## Current code organization

`main.py` is the root application entry point. Python implementation modules are grouped into `maps/` (view, terrain editor, geometry, mapping helpers, campaign/grid definitions and grid import), `counters/` (browser, editor, state, face rendering, stack inspector and counter import), `game/` (action history, history panel, dice dialog), and `rules/` (independent rules systems). Automated tests live in `tests/`. Older bare filenames elsewhere in this context describe these relocated modules.

Run the main app with `.venv/Scripts/python.exe main.py`, the editor with `.venv/Scripts/python.exe -m counters.unit_editor`, and tests with `.venv/Scripts/python.exe -B -m unittest discover -s tests -v`. See README.md for importer commands. Original artwork, reference PDFs, terrain/transport JSON, catalogs, reviewed definitions, backups and campaign-save formats retain their data locations/format. Mapping backups and grid importer paths follow the moved definitions in `maps/`; backup archive member names remain unchanged.

The unit editor also supports direct-file launching (`counters/unit_editor.py`, including IDE Run File): when launched outside a package it adds its resolved project root to the import path. Package imports/module launching retain their normal behavior. Resource paths remain anchored to the project, not the shell's working directory.

Unit-editor navigation saves must not rebuild the counter list inside `finish_pending_edits`: the enclosing selection handler still holds Qt list items. Pending-edit saves use `save_definition(refresh_selection=False)` and refresh saved-status visibility in place; explicit Save can rebuild normally. Regression tests cover the previously reproduced deleted-QListWidgetItem error, search-save, filtered navigation and Cancel preserving edits. Tests use temporary definitions only.

## Purpose and priorities

Build a native Python/PySide6 TSWW Barbarossa companion. We are learning the game, so clear explanations, rule references, collaborative development, and concrete things to test are important.

Game modes, in priority order:
1. Guided play controlling both sides, also alongside a physical game: phases, resources, calculations, and reminders.
2. Play by email.
3. Computer opponents, beginning with one small scenario and the grand campaign before extending to all scenarios.
4. Online multiplayer.

Long-term features: scenario setup, reinforcements, optional-rule selection, chart access, configurable keybindings, and AAR generation from a structured action history.

## Visual direction

Preserve original map and counter artwork. Generate surrounding interface graphics primarily in code. Eventually offer selectable themes, including a color workstation (gray panels, teal/navy, amber, beveled controls) and early desktop publishing (cream, burgundy/blue, ruled sections). Keep theme work separate from unit-editor work.

## Current implementation

`main.py` runs the map/campaign companion. `map_view.py` handles rendering, hex selection, terrain/transport editing, overlays, counter placement, and campaign persistence. `terrain_editor.py` provides mapping controls; `hex_model.py`, campaign/grid definitions, and mapping helpers support geometry and data. `counter_browser.py` provides the searchable imported catalog. Import utilities read VASSAL content.

`unit_editor.py` is a separate catalog metadata editor with shared identification, front/back images and face identity, category-specific ratings, per-face ground formats/type overrides, review tracking, atomic saves, and timestamped backups.

Mapping and counter metadata are still entered manually. Do not assume every mapped hex or imported counter is verified. Naval and commander editing exists but has not been tested with representative counters.

## Data principles

- Imported `assets/counters/counter_catalog.json` is separate from manually reviewed `unit_definitions.json`. Preserve stable `type_id` values.
- Definitions describe counters; campaign instances will hold position, active face, losses, movement used, and changing state.
- Preserve unknown fields and existing entries during updates.
- Blank ratings mean unknown; zero is real; N/A explicitly means not applicable.
- Do not infer rules or ratings solely from filenames. Not all alternate faces represent reduced strength.
- Generate blank reverses in code using stored color and front-image dimensions.
- Older shared ground formats must still load into both faces.

## Confirmed examples

GE Inf XX 87 @126.FB: Ground unit, German Army, Infantry, Division. Front: combined strength 12, movement 6, Full strength, printed XX. Back: combined strength 6, movement 6, Reduced, printed Reduced.

GE Hvy Art II 143.FB: Ground unit on both appearances. Artillery image `GE Hvy Art II 143.FB.png`, ratings 3-2-6. Alternate `GE CD 143 L3.FB.png`, coastal-defense Level 3. VASSAL labels this appearance "Emplace as CD". This motivated independent ground formats and type overrides per face. Neither filename identifies a conventional back; review manually.

## Focused validation task

Provide Check Definition and Verified-save checks for core identification, image readability, back-appearance review, and core ratings on applicable faces. Accept zero and N/A, skip blank reverse ratings, respect each face's ground format, and leave optional attributes/modifiers optional. Incomplete definitions remain saveable as Unreviewed/In progress. Verified saves with issues offer Return to Editing or Save as In Progress. Keep saved indicators/counts consistent and never change review statuses merely on opening. Test persistence and legacy formats with temporary fixtures. These are metadata-completeness checks, not gameplay-rule validation.

The initial completeness policy requires designation, category, nationality, service, type, and size (explicit N/A is acceptable where appropriate). Ground core fields follow each face's format; AA is optional except for dedicated AA format, and torpedoes remain optional. Air core fields are attack, aircraft type/code, air defense, and range. Naval core fields are ship type, gunnery, protection, and tactical speed. Commander core fields are rank and movement; bonuses/modifiers are optional. These are editor workflow choices, not assertions about TSWW rules. Representative naval/commander counters still need manual review.

## Counter mechanics: first slice

Campaign saves now include a top-level `units` list of placed instances, each with stable `unit_id`, catalog `type_id`, chosen `image_path`, canonical `hex_key`, `active_face`, and `stack_order` (ascending bottom to top). Older version-1 campaign saves without this list load with no placed instances. The existing hex-property `units` lists are retained as legacy data; stack membership is derived from each top-level instance's `hex_key`.

Current catalog placement does not resolve reviewed faces: `active_face` is `unassigned`, preserving the exact chosen image without guessing its meaning. Click selection highlights a counter; the Hex Stack dock lists the selected hex top first and lets the user select covered instances. Selection does not reorder a stack. There is no stacking legality enforcement. Gameplay rules and themes remain separate. Counter/image save validation happens before replacing the current campaign, and unknown campaign/instance fields are preserved.

## Counter flipping

The Hex Stack dock offers Flip Selected Counter, with a visible reason when unavailable. The first flip requires a Verified definition, resolved front/back assignments, readable artwork, and a placed image matching exactly one assigned face by path. No filename-based face inference occurs. Mapping modes disable flipping. Alternate appearances do not imply reduced strength or apply gameplay effects.

On first flip, the instance stores a `face_assignment` snapshot (front/back paths, back appearance, blank-back color). Later flips and campaign reloads use this snapshot rather than silently changing with definition edits. Blank backs are generated in code with the stored color and front-image dimensions; no generated artwork is written to disk. For a blank back, `image_path` retains the front source and `active_face` identifies the generated reverse. Identity, position, stack order, and unknown instance fields remain unchanged.

## Manual movement

Select an instance, click Move Selected Counter in Hex Stack, then click a playable destination hex. The counter retains identity, face, image, and other instance state, and enters the destination stack on top. Clicking the source hex leaves stack order unchanged. Cancel Move or Escape abandons a pending move; invalid destinations leave it pending. Panning remains available, while stack selection and flipping are disabled during destination picking. Enabling a mapping mode cancels the pending move. Pending moves are transient UI state; saves persist completed positions only.

Movement costs, allowances, phase restrictions, and stacking/movement legality are not implemented yet and remain the player's responsibility. The playable-map boundary check is a geometry check, not gameplay legality. Automated tests cover cancellation, destination clicks, stack membership/order, preservation of flipped appearance, and save/load with temporary data. Full-map visual behavior needs manual testing.

## Structured counter action history

Placement, flipping, and completed movement now append version-1 structured records with unique action IDs, UTC timestamps, kind, instance ID, readable descriptions, and deep-copied before/after instance snapshots. The Counter History dock (tabbed with Hex Stack, reopenable through View) shows applied versus undone entries and offers Undo/Redo. It records no selection, panning, cancelled moves, same-hex moves, or terrain/transport edits. Undo/Redo is disabled during mapping modes and pending movement.

Campaign saves include `action_history` with `entries` and an applied-action `cursor`. Undo restores exact prior instance state and stack order; redo restores the same instance IDs and recorded face assignments without consulting changed definitions. A new action after Undo replaces the redo branch. History is a local editable timeline, not an immutable audit trail, and is not yet an AAR or PBEM implementation. Old saves without history start a new empty history while retaining their existing counters as the baseline. History cannot undo actions predating that baseline.

The loader validates snapshot shapes, canonical hexes, action IDs, cursor, replay consistency with saved counters, and historical image readability before replacing the campaign. Unknown action/history/instance fields are retained. Undo/Redo preloads required artwork before changing state, and a failure leaves the cursor and current counters intact. Automated tests use temporary saves and images; full-map manual testing remains necessary.

## Rules planning (2026-10-20)

The user manually validated counter mechanics and history, and wants the rules foundation before scenarios. Defer scenario selection and the final interface redesign. See `REFERENCE_SOURCES.md` for the local PDF inventory, edition/page conventions, targeted inspection scope, and unresolved conflicts. `reference_source_inventory.json` stores source fingerprints and page counts. See `RULES_IMPLEMENTATION_CHECKLIST.md` for rule-system work items, dependencies and completion criteria.

Local general rules are v1.6 (2019) and v1.6a (2023); local charts identify v1.6 (2019). The user selected R16a as governing general rules. They interpret chart p1 as individual attack resolution: all Combat Phase attacks must first be declared before any results are calculated/resolved. SRC-02 is therefore resolved for this project; retain the wording discrepancy for traceability. SRC-04 is an implementation timing note, not an open user question. The user confirmed retaining fractions by default and applying explicitly specified mechanic-specific methods locally.

Work slowly through the rulebook, one or two features at a time. The proposed first slice is Rule 2.A-B exact fractional arithmetic and cumulative effects with citations/tests; recorded dice (2.C) follows separately. Do not jump directly to implementing the entire phase engine. No gameplay rules or persisted rules profile were implemented in the planning/decision documentation tasks. Inspection was targeted, not a full errata or numerical chart reconciliation. Ask about new ambiguities or optional-rule choices when their mechanics are reached; there is no current blocking user question. The user's recollection that v1.6a shipped with their physical game remains unconfirmed provenance.

## First rules code: dice and result scaffolding

Subsequent user direction prioritised dice rather than unused arithmetic helpers. The UI-independent `rules/` package is the home for rules code: `dice.py` contains `DiceService`, roll interpretation and validation; `combat_records.py` contains attack-result scaffolding. `__init__.py` retains existing public imports, including the `roll_dice` convenience function. The map owns a `DiceService` with an injectable random source. Saved record formats and behavior are unchanged by this refactor. Future rule systems should have their own modules rather than one giant Rules class. v1.6a Rule 2.C.1, printed p8 / PDF p10, supports 1D10, explicitly summed 2D10, and percentile (tens then ones). Raw faces are decimal digits 0-9: a single 0 means 10, summed 0+0 is 20, percentile 00 is 100. Requests must identify the correct mode; text mentioning two dice does not automatically mean sum. More than two dice is outside this slice.

Human rolls support automatic generation or manual physical-face entry. AI API requests always generate automatically and reject manual faces; no computer opponent exists yet. Game > Roll Dice opens a basic campaign-bound dialog. Each confirmed roll records its ID, UTC timestamp, raw faces, interpreted value, source/method/controller, optional purpose and rule locator. Opening/closing the dialog alone records nothing. Animation is deferred; it must eventually display a determined recorded result, never choose a new one.

The Action History dock (renamed from Counter History) now handles `dice_roll` and `attack_result` events alongside counter changes. These events have validated payloads and null before/after snapshots: Undo/Redo deactivates/reactivates the record without rerolling or changing counters. Existing branch behavior applies, so this remains an editable local timeline, not a tamper-proof PBEM audit log.

`attack_result_record` and `MapView.record_attack_result` provide AAR scaffolding for participant instance IDs, target hex, manual outcome, notes, and embedded dice records. This is backend scaffolding, not a combat dialog/calculator, attack-declaration engine, casualty application, or AAR exporter. History persists events and cursor with backward compatibility; invalid recorded dice/history is rejected before replacing the campaign. Automated tests use temporary data. Rounding remains the confirmed policy (retain fractions unless a specific mechanic says otherwise); no generic rounding or combat calculations were added.

## Player and nation setup

Unit-editor update: each face identity tab now has an editable `Face unit size`, stored as `faces.front/back.unit_size_override`. Null/missing/blank means use the shared `unit_size`; old definitions keep their shared fallback. Completeness checks use the effective size of each applicable face and skip blank reverses. Wing and Squadron are offered in the size lists; no values are inferred or migrated on opening. Printed size/status text is independent transcription of the actual artwork and stays blank when no text is printed. For an ordinary air counter, a shared Wing with back override Squadron is supported. No air-loss or other gameplay rules were added.

User-approved notation is Axis players × Allied players. Game > Players and Nations provides local setup, editable player names, nation allegiance, nationality aliases and whole-nation assignments. Two-player mode defaults to 1×1; AI setup requires 1×1 with exactly one AI-controlled side. Pass-and-play, online-setup and PBEM-setup permit independent team sizes from one to the number of nations on that side. Online/PBEM transport and AI opponents are not implemented. Player assignments do not yet enforce permissions on counter actions.

The authoritative roster source is the local four-page UICFB.pdf, PDF p3 National Colour Identifiers, per user confirmation. The user's other 2021 key may belong to a different game; do not import extra nations from it. `game/nation_roster.py` groups branches under nations: eight Axis nations and ten Allied nations, plus an explicit Inter Allied control pool (not counted toward maximum team size). Spanish forces appear under Axis in the key; these are editable chart-force defaults, not a declaration that sovereign Spain is at war. LW foreign contingents are not automatically mapped to sovereign nations. The local key has no neutral-nation list; users can add nations and choose Neutral. The Soviet Union is grouped on the Allied side for this setup. Allegiance and player ownership remain separate; automatic entry/defection and neutrality legality are not implemented (v1.6a 2.D-F, printed pp8-9 / PDF pp10-11).

`rules/sides.py` validates setup, exposes side lists, counts placed instances using Verified unit-definition nationality and explicit case/whitespace-normalized aliases, and suggests a deterministic greedy whole-nation split independently per side. Catalog type counts, filenames and unreviewed metadata are never used as balancing weights. Unknown/unmatched instances are reported; suggestions may be uneven when one nation dominates and remain manually editable. Unknown counts are excluded, not presumed zero-sized forces. Suggestions are user-triggered, not silently regenerated after opening or changing counter data.

Campaign `player_setup` persists roster, player IDs/names/controllers, play mode and assignments. Older saves default to the chart roster and human 1×1. Validation occurs before replacing the campaign; unknown setup/nation/player fields are retained. Setup editing uses a copy so Cancel changes nothing. Setup is configuration outside the counter Undo/Redo timeline. Automated tests use synthetic nations and temporary campaign files; full campaign UI/save/reload still needs manual validation.

## Deferred rules during book review

Rule 2.E initiative automation and the data-dependent applications of 2.F are explicitly deferred: boundaries, seat-of-government effects, neutrality restrictions, contingent combat effects, unreliability and garrisons, plus automatic allegiance/defection. Keep implemented local side/team setup. These rules need verified territorial/unit/OB inputs and calendar, political, phase or combat systems; they remain manual. See the checklist's deferred register for individual sources and revisit triggers. Do not require the entire map/catalog to be complete if a specific rule's required subset is ready. Continue front-to-back review and defer other dependent applications explicitly rather than guessing missing inputs.

## Counter-entry automation removed

The user tried the Luftwaffe draft-automation pilot and requested its removal. Counter metadata entry remains manual. The Automation menu, draft builder/preview/import code and dedicated automation tests were removed. Do not reintroduce automation unless requested. Existing saved definitions (including any drafts the user may have imported) and backups were not edited or deleted. `counters/unit_storage.py` remains the manual editor's atomic save and timestamped backup helper. Selection fixes, per-face sizes, direct IDE launching and all other manual-editor features remain in place.

The user subsequently authorized assistant visual transcription in reviewable batches of five, without restoring automation. The first manual batch added IDs `vassal:133:235515` through `vassal:133:235519` (He111H16 LT, He115B2 FAV, He115C1 FAV, Ju88A1, Ju88A1 S). Both images were individually inspected; entries were saved In progress with full Wing front/reduced Squadron back, exact printed ratings/codes, and source notes. The user subsequently checked all five and marked them Verified.

The user then authorized the remaining Luftwaffe aircraft only, excluding ground units. Added 130 entries, IDs 235520-235649, as In progress, preserving all 25 prior definitions and metadata. The former Luftwaffe checklist has been consolidated into `AIRCRAFT_REVIEW_BATCH.md` after user verification. Three artwork exceptions remain incomplete (235522 missing images; gliders 235638-235639 single-image special markings), and 235640 has literal M with general type Unknown. LW Croat/Estonian force groupings follow UICFB p3 without sovereign-nationality inference. Human review is pending. Close/reopen an already-running unit editor before further saves so its in-memory definitions include these additions. No production automation feature was restored.

Subsequent artwork repair: 235522's two original images were present in the image inventory but missed by the importer because they share a comma-separated VASSAL appearance field. The importer now resolves these lists while preferring exact filenames (including names containing commas); the existing catalog and definition image links were repaired with backups. User confirmed gliders 235638-235639 use their single image as front and a generated blank reverse; stored background is sampled `#c4e5f8`. Ratings, sizes and review statuses were preserved; remaining incomplete identification/special ratings still need review. Importer regression checks use synthetic temporary modules only.

User-requested aircraft label/notes consistency pass: expanded five dual-role general Unit type labels (B/D, B/R, HB/T), distinguished RB as Rocket Bomber, and resolved M as Minesweeper from v1.6a 5.B.3 (printed p28 / PDF p30). Literal per-face codes and all ratings remain unchanged. Updated 38 Verified entries' assistant notes to reflect completed user review, including removing obsolete Ju88A4 V missing-artwork claims. All 155 saved entries' review statuses, other fields and metadata were preserved; atomic save with exact backup verified. This was saved-data cleanup, not an automatic notes/status feature.

Glider size decision: user approved treating DFS230 (235638) and Go242 (235639) as reduced Squadrons by default. Shared size is Squadron, front status Reduced, and blank reverses remain unchanged. Notes identify this as the agreed project interpretation, not an explicit rulebook confirmation or a conclusion from the circle/reverse-side marker. Ratings and review statuses were preserved.

Glider editor metadata: Air units with shared type Glider or literal face code G show per-face tug attack/defense modifiers, tug bombing restriction, tug range modifier, aircraft code and capacity. These are distinct aircraft-face string fields (`tug_attack_modifier`, `tug_defense_modifier`, `tug_bombing_restriction`, `tug_range_modifier`), not ordinary aircraft combat ratings. Completeness requires these glider fields plus code and capacity on applicable faces, accepts zero/N/A, and skips blank reverses. Ordinary hidden fields and unknown saved data survive mode changes and saves; old records are not migrated on opening. Tooltips retain the provisional interpretation of the two -1 markings. Bombing and range references: v1.6a 5.B.3.a.vi and 10.N.4.a.iv; no gameplay effects are implemented. Existing saved definitions were not edited as part of this code change. Tests use temporary data; all 61 tests passed, including three new glider regression checks.

User completed the Luftwaffe review and corrected Croat/Estonian contingent nationality to Germany, with service Luftwaffe Croat Forces / Luftwaffe Estonian Forces. Preserve that convention; Spanish aircraft remain nationality Spain, service Luftwaffe. User prioritizes finishing all aircraft before naval or ground counters.

Subsequent authorized batch added all 284 remaining undefined aircraft as In progress (139 Soviet, 52 Romanian, 25 Hungarian, 17 Finnish, 13 Bulgarian, 11 RAF, 11 RN, 6 Slovak, 4 Italian, 4 USN, 2 USAAF), preserving all 155 existing definitions and statuses. See `AIRCRAFT_REVIEW_BATCH.md` for exceptions, tests, backups and review checklist. Four compact BR/RB/RA general types remain Unknown pending interpretation; literal artwork ratings/codes are transcribed. Two image pairs (Romanian Me109F2 and RN Albacore) have full-strength artwork first. Repaired only the Romanian Me109F2 catalog image references with a backup. All 284 were opened/checked with temporary editor data, eight representative temporary save/reloads passed, and all 61 tests passed. No undefined Air-palette catalog entries remain, but new drafts still require user verification. Restart any open editor before saving to avoid stale in-memory data. No production automation, gameplay code, naval/ground definitions or artwork was changed.


## Private repository maintenance

The user authorized cleanup and a private GitHub checkpoint after finishing the Luftwaffe review. All 152 first-batch aircraft are Verified; their stale assistant notes were cleaned (135 entries in this pass), preserving all other definition fields, unknown metadata and second-batch drafts. The obsolete separate Luftwaffe checklist and temporary review artifacts were removed; useful reference/checklist/context documents, all application code (including legacy root rules.py), original artwork/PDFs and data backups were retained. Unit definitions are now explicitly versioned; original assets, imported catalogs, local backups, temporary files and reference PDFs remain ignored. Aircraft review progress and remaining exceptions are in AIRCRAFT_REVIEW_BATCH.md. All 61 temporary-fixture tests passed. Restart the editor before saving after external note changes.
