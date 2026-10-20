# Rules implementation checklist

Prepared 2026-10-20. Source IDs and citation conventions are in [REFERENCE_SOURCES.md](REFERENCE_SOURCES.md). This is an implementation backlog, not a claim that the rules have been automated. No gameplay-rule implementation is included in this documentation task.

User-confirmed approach: R16a governs general rules. Declare all Combat Phase attacks before resolving any; resolve individually afterward. Retain fractions unless a mechanic specifies otherwise. Work through the rulebook in small slices of one or two features; do not implement a whole system in one pass. SRC-04 is a timing note, not an unresolved question. Source decisions are recorded; F01 remains unchecked because its persisted campaign profile is not implemented.

## Current baseline

| Capability | Current status | What remains manual |
|---|---|---|
| Hex/map geometry and terrain/transport entry | Implemented tools; data still being reviewed | Completeness/correctness of each hex, boundary and connection |
| Counter identification and ratings | Manual editor with completeness checks | Printed-rating interpretation, rule classifications, national exceptions; a Verified record is not proof of implemented rules |
| Placement and stack inspection | Implemented mechanics | Setup legality, stacking-point limits, ownership and side restrictions |
| Face flipping, including generated blank reverses | Implemented mechanics using reviewed assignments | Whether/when the change is legal and what it means; not every alternate is reduced strength |
| Movement | Implemented manual relocation | Path, MP spending, terrain/ZOI, supply and phase legality |
| History and Undo/Redo | Implemented for place/flip/move | Rule-related costs/effects, dice, resources, phases and explanations are not recorded yet |
| Turn/phase, weather, supply, combat, administration, victory | Not implemented | All gameplay determinations |
| Dice (Rule 2.C.1) | Implemented in `rules/dice.py` through `DiceService`; Game > Roll Dice; automatic/manual human rolls, automatic AI API | Mechanics requesting the appropriate roll and any special interpretation/modifier; animation deferred |
| Attack-result recording | Validated backend/history scaffolding only | Attack declaration, combat calculation/effects, combat interface, AAR generation |
| Side/team setup | Local setup UI, nation lists/assignments, placed-counter balancing and persistence implemented | Date-dependent allegiance, neutrality/defection rules, counter-action permissions, AI opponents and network/PBEM transport |

## Deferred during front-to-back review

Recorded 2026-10-20: defer the data-dependent applications below, while retaining the implemented side/player setup. Deferred means not implemented and still handled manually, not omitted from the game. Revisit when the relevant data and dependent systems are ready; the entire map/catalog need not be finished if a particular rule's required subset is verified.

| Rule (R16a) | Status | Prerequisites / revisit trigger |
|---|---|---|
| 2.E Initiative, printed p8 / PDF p10 | Deferred | Campaign calendar, applicable-location registry, verified ownership/control inputs, geographic scope and political/national exceptions. Dice are available, but cannot determine whether an initiative check is required without these inputs. |
| 2.F opening allegiance/defection, printed p9 / PDF p11 | Partial: editable setup exists; automatic changes deferred | Dated national political rules, events and applicable starting-state data. Setup choices are not automatic political rulings. |
| 2.F.1 National boundaries | Deferred | Verified national-boundary mapping and dated module/P&E exceptions. |
| 2.F.2 Seat of government | Deferred | Identified government markers, campaign location/status tracking and relevant political effects. |
| 2.F.3 Neutral nations | Deferred legality enforcement | Verified territorial affiliation, dated permissions/P&E and OB exceptions; movement, retreat and air-overflight validation. Neutral setup entries alone do not enforce these rules. |
| 2.F.4 National contingents | Deferred combat effects | Explicit reviewed contingent affiliation (separate from nationality and player ownership), national exceptions and combat factor calculations. |
| 2.F.5 Unreliability | Deferred | Reviewed OB/P&E unreliability flags, Success Table transcription/validation and combat modifier pipeline. General dice rolling alone does not implement this check. |
| 2.F.6 Garrisons | Deferred | National OB/OA requirements, off-map force records, activation events, initial-phase timing and any selected fog-of-war rules. |

Continue reviewing the next section without coding around these missing inputs. Mark further dependent rules as deferred individually, with the same source/prerequisite detail. Do not infer that Section 2.G ownership/control is ready merely because map geometry exists.

## Completion contract for every rule slice

- [ ] Identify the exact edition, rule/subrule, printed page, PDF page, chart page and applicable footnotes.
- [ ] Read the entire relevant passage and visually inspect each table/icon before transcription.
- [ ] List dependencies, national exceptions, optional settings and unresolved source conflicts. Do not silently merge editions.
- [ ] Define required inputs and return `insufficient information` when required metadata, mapping or state is unknown. Zero is a value, N/A is explicit, blank is unknown.
- [ ] Implement calculations and legality in Python independent of PySide6 widgets. Keep definitions separate from mutable instances and campaign state.
- [ ] Return a result with explanation, inputs, modifier breakdown, source locators, and unresolved/manual checks.
- [ ] Test normal examples, boundaries, exceptions, unknown inputs, cumulative effects and rounding. Derive examples from identified rules rather than merely mirroring implementation.
- [ ] Persist new state atomically; retain unknown fields, existing backup behavior and older-save compatibility. Use temporary test data.
- [ ] Make related state/resource changes one reversible history action where appropriate. Record dice outcomes so redo does not reroll.
- [ ] Expose only the controls needed to use the implemented behavior. Label manual checks honestly and give concrete manual tests.

## 0. Sources and foundations (first)

| ID | Work item | Source / dependency | Acceptance target |
|---|---|---|---|
| F01 | [ ] Record a governing rules profile and explicit source overrides | SRC-01/SRC-02; R16a 2.L p12 / PDF p14 | Edition/options saved with campaign; unresolved contradictions remain visible |
| F02 | [ ] Source locator and decision-result structures | Source inventory and completion contract | Calculations distinguish allowed, prohibited, insufficient information, and manual-only checks |
| F03 | [ ] Exact fractions, cumulative modifiers and rule-specific rounding | R16a 2.A-C p8 / PDF p10 | Fractions retained by default; pursuit-specific floor tested separately; no global integer rounding |
| F04 | [x] D10, percentile and recorded randomness | R16a 2.C.1 p8 / PDF p10; `rules/dice.py`, `test_rules.py`, `test_counter_mechanics.py` | 1D10, explicit 2D10 sum, percentile; automatic/manual human entry, automatic AI; persisted raw faces/results; redo never rerolls. Automated checks passed; physical-game UI still needs manual verification. No chart-specific overrides implemented. |
| F05 | [ ] Side/nation/contingent, date, ownership and unit classification model (partial: local side/team setup implemented) | R16a 2.D-H pp8-10 / PDF pp10-12; 5.A pp25-27 / PDF pp27-29; UIC pp1,3 | `rules/sides.py`, `game/player_setup_dialog.py`: human 1×1 default; AI setup restricted to 1×1; asymmetric teams, manual assignments and placed-instance balancing. No filename inference. Allegiance/date/contingent rules and permission enforcement remain manual. |
| F06 | [ ] Optional-rule registry and dependencies | R16a contents and optional-rule passages below | Explicit recorded settings; do not enable options accidentally by importing a table |

## 1. Turn sequence and guided play

Anchor: R16a Rule 6 printed pp34-35 / PDF pp36-37; comparison R16 pp35-36 / PDF pp37-38; C16 p1. Follow the recorded SRC-02 interpretation: all attacks declared before individual resolution. The first implementation can track phases/reminders while dependent computations remain explicitly manual.

- [ ] **P01 Calendar and initiative:** game turn versus player turn, side order, rollover and phase cursor; Rule 6.1-2 and 2.E p8 / PDF p10. Ownership-dependent initiative needs known control of applicable locations; the optional five-day variant must be a distinct supported mode or explicitly unsupported.
- [ ] **P02 Initial phase:** special-event reminders, general supply/isolation, LP/GSP expenditures, administration, offensive supply distribution, air pools/readiness and naval-cooperation assignments; 6.3.a. Handle both players' responsibilities, not only the phasing side.
- [ ] **P03 Movement substeps/windows:** pre-movement airbase attacks and naval spotting, naval segments/cooperation, ground and transport activity, remaining air missions; 6.3.b. Capture timing qualifications and optional air-order randomisation.
- [ ] **P04 Combat substeps:** declaration, supply, CAS/carpet bombing/interceptions, isolation/replacement check, NGS/ground combat and ordered loss/retreat/advance handling; 6.3.c.
- [ ] **P05 Reaction:** non-phasing participation and eligibility reminders; 6.3.d and 7.C.2.h p38 / PDF p40.
- [ ] **P06 Pursuit:** naval movement and ground allowances by unit class/supply, tactical rate and rounding exception; 6.3.e; C16 p4; reconcile special-unit exceptions.
- [ ] **P07 Air return and turn end:** basing/landing checks, replacement accounting, spotting-marker cleanup and next player turn; 6.3.f-g.
- [ ] **P08 Persistence/history:** save phase/substep, acting side, unresolved reminders and completed decisions; make phase transitions reversible without undoing unrelated mapping edits.

Acceptance examples: two player turns complete one game turn; weather occurs at game-turn boundary rather than twice; both sides can act in specified windows; a manual supply reminder cannot be represented as an automatically passed supply check.

## 2. Geography, climate and facilities

| ID | Work item | Rulebook anchor (R16a printed / PDF pages) | Charts / dependencies |
|---|---|---|---|
| G01 | [ ] Climate/weather, temperature, freezing, mud and Arctic effects | 3.A-C pp13-18 / pp15-20 | C16 pp29-31; date/weather-zone metadata, F04 |
| G02 | [ ] Terrain/hexside semantics and unit movement classes | 3.C p18 / p20; 5.A pp25-27 / pp27-29; 7.C-D pp37-38 / pp39-40 | UIC terrain key; C16 pp7-9; do not treat unknown terrain as clear |
| G03 | [ ] Fortifications and ownership/state | 4.A pp19-20 / pp21-22 | C16 p8; levels, damage, construction |
| G04 | [ ] Airbase, port/shipyard, RMY, oil and factory capacity/state | 4.B-F pp20-23 / pp22-25 | C16 pp9-10, 15; facility type, capacity and damage |

## 3. Ground movement, stacking and ZOI

| ID | Work item | Rulebook anchor (R16a printed / PDF pages) | Charts / acceptance |
|---|---|---|---|
| M01 | [ ] Explicit route and MP ledger | 7.A/C pp37-38 / pp39-40 | Path rather than teleport; history records route/cost and preserves face |
| M02 | [ ] Tactical, operational, administrative modes | 7.D pp38-39 / pp40-41 | C16 pp7-9; cannot silently combine incompatible movement modes |
| M03 | [ ] Terrain/hexside/road/weather cost evaluator | 7.C-F pp37-43 / pp39-45; 3.A-B | C16 pp7-9 incl. footnotes; prohibited/road-only distinct from high cost |
| M04 | [ ] ZOI projection and entry/exit costs | 5.A.9 p26 / p28; 7.B/C pp37-38 / pp39-40 | C16 p11; full/reduced/none, terrain and supply dependencies |
| M05 | [ ] Stacking points, limits and phase-end checks | 5.A.5-8 pp25-26 / pp27-28 | C16 pp4,9; transient passage vs end-of-phase checks; artillery allowance and reduced-state exceptions |
| M06 | [ ] Rail, road, river, ferry capacity and damage/regauging | 7.F pp40-43 / pp42-45 | C16 p9; MAP p2; engineers and national exceptions |
| M07 | [ ] Special-unit and ownership rules | 7.G-H pp44-45 / pp46-47; 5.A.3 p25 / p27 | Support-unit distinctions; semi-motorised, ski, mountain etc.; C16 pp17-18 |
| M08 | [ ] Reaction/pursuit eligibility and allowance | 7.C.2.h p38 / p40; 6.3.d-e p35 / p37 | C16 p4; combat-location history, supply, class and rounding |
| M09 | [ ] Overruns and movement combat | 7.E pp39-40 / pp41-42 | C16 p11; stacking, ZOI, combat and supply dependencies; not part of a simple cost calculator |

Acceptance examples to derive and verify: zero-MP unit; exact remaining allowance; road-only terrain; river crossing; Arctic road exception; reduced versus full ZOI; phase-end overstacking versus passing through; unknown adjacent hex; movement on an alternate face with a different type.

## 4. Logistics (must inform final movement/combat results)

Anchor: R16a Rule 15 pp113-128 / PDF pp115-130; C16 pp2,14-15; SUP/SUP-QM. Diagrams are explanatory and cannot replace the numbered rules.

- [ ] **L01 Supply graph:** national sources, LOC, MSR/QMSR/RSR, valid transport connections and route blockers; 15.A-G.
- [ ] **L02 System profiles:** continental, overseas with QM, optional overseas without QM, and exceptions; 15.C-F. Keep alternative systems distinct (SRC-07).
- [ ] **L03 Supply/isolation lifecycle:** general versus offensive supply, E/U progression, phase-of-onset tracking, collapse and recovery; 15.G-J. Do not interpret marker colour as side.
- [ ] **L04 Distribution:** terminals, motor/river/air QM, daisy chains, AG/Army/Corps HQ roles and capacities; 15.K-P.
- [ ] **L05 Resource ledger:** LP/GSP production, spending, stockpiles, capture, island and naval supply; 15.Q-X. Group expenditure and resulting state change into one history transaction.
- [ ] **L06 Modifiers:** feed supply status into movement, pursuit, airbase capacity and combat calculations with a visible explanation; C16 p2, reconciled with R16a 15.I-J.

Acceptance examples: a broken transport link; a unit in range but isolated; distinct continental/overseas chain permissions; E/U change in the correct recurring initial phase; insufficient resource stock; unknown route metadata returns insufficient information.

## 5. Ground combat

Anchor: R16a Rule 10 pp73-80 / PDF pp75-82; C16 pp3-4,7-12,17-18; 5.A.10 p26 / PDF p28. SRC-02 is resolved by the recorded user interpretation.

- [ ] **C01 Declaration and eligibility:** adjacent targets, participation, prohibited terrain, support exceptions and attack commitment; 10.A/C; Rule 6.
- [ ] **C02 Factor pipeline:** per-unit ratings, terrain, weather, supply, national contingents, CEV/BAI, special units and optional Going; 10.B/C/I/L/O. Preserve fractions until specified rounding.
- [ ] **C03 Odds selection and CRT:** ratios, percentile selection between columns, D10/DRM and table bounds; 10.B. Published 34-versus-9 example on p73 / PDF p75 must be examined for its stated rounding convention before turning it into an oracle.
- [ ] **C04 Armour/AT/engineers and other special modifiers:** 10.K-M; C16 pp10-12,17-18; verified classifications required.
- [ ] **C05 Results transaction:** losses, reduced/full distinctions, elimination, retreat, blocked retreat, advance and stacking; 10.D-H/J and 6.3.c.v. A generic flip is not a combat loss.
- [ ] **C06 Airborne/special attacks and optional Going:** 10.N-O pp79-80 / PDF pp81-82; C16 pp9,11. Explicit option settings and air/transport prerequisites.

## 6. Air and naval systems

| ID | Work item | R16a printed / PDF pages | Chart navigation |
|---|---|---|---|
| A01 | [ ] Aircraft type/code abilities, readiness and basing | 5.B pp28-30 / pp30-32; 4.B p20 / p22 | C16 pp10,15,17-18,26-27 |
| A02 | [ ] Missions, range, interception, escort, transport and return | Rule 8 pp47-60 / pp49-62 | C16 pp26-27,32; Rule 6 timing; optional 8.E/I/J |
| A03 | [ ] Air-to-air combat | Rule 11 pp81-83 / pp83-85 | C16 pp5,12,26 |
| A04 | [ ] AA combat and mission effects | Rule 12 pp85-86 / pp87-88 | C16 p6; organic/positional/mobile/naval AA distinctions |
| N01 | [ ] Naval task groups, segments, movement, fuel, time at sea | Rule 9 pp61-71 / pp63-73; 5.C pp31-33 / pp33-35 | C16 pp19-26; multi-segment participation |
| N02 | [ ] Spotting, transport, amphibious operations, submarines | 9.I-L pp63-71 / pp65-73 | C16 pp19-21,25-26; ownership, ports, supply, fog of war |
| N03 | [ ] Naval combat, damage, repair, NGS, night/interception | Rule 13 pp87-97 / pp89-99 | C16 pp19-24,33; reconcile table values and optional 13.S |

## 7. Special systems, administration, national rules and victory

- [ ] **S01 Breakdowns, engineering and repair/demolition:** 14.A-B pp99-102 / PDF pp101-104; C16 p10. Include construction state, MP/resource use and weather effects.
- [ ] **S02 Special forces, artillery HQ, transport/base units, partisans, river flotillas/RSPs and leaders:** 14.C-H/K pp102-110 / PDF pp104-112; C16 pp11,13,15,17-18. Each requires its own tested slice.
- [ ] **S03 Optional systems:** fog of war (2.K), five-day variant (2.L), tactical rebasing (8.E), mid-course interception/AA (8.I-J), Going (10.O), naval interception (13.S), mines (14.I), fast attack squadrons (14.J), WMD (14.L), no-QM overseas supply (15.E), and optional air-order randomisation in Rule 6. Inventory may expand after detailed national-rule review; unsupported options must not silently operate.
- [ ] **D01 Administration:** ground/air/naval replacements, repairs and pools; Rule 16 pp131-135 / PDF pp133-137; C16 pp13,15,23; AX-REP and OB references when scheduled data is added.
- [ ] **D02 Political/economic and national exceptions:** Rule 17 pp137-167 / PDF pp139-169. Germany 17.C.4 begins p145 / PDF p147; USSR 17.C.10 begins p156 / PDF p158. National modifiers are dependencies of earlier systems, not permission to ignore them until the end.
- [ ] **D03 Strategic-map integration:** Rule 18 pp169-172 / PDF pp171-174; UIC strategic-map key. Track as a distinct subsystem; no tactical/strategic-scale conversions by assumption.
- [ ] **D04 Victory and surrender:** Rule 19 p173 / PDF p175; C16 pp34-35. Later take explicit game/scenario inputs; no scenario work is part of this phase.
- [ ] **D05 OB/appearance and setup data:** AX-OB/MIN-OB/SU-OB/WA-OB/START/AX-REP. Deferred per user direction; keep versioned source references ready for future imports and exceptions.

## Suggested first coding slice after this inspection

1. Per subsequent user direction, the first implemented slice is Rule 2.C.1 dice and result-recording scaffolding, rather than arithmetic helpers. Human auto/manual and AI automatic rolling are implemented; verify the basic UI manually next.
2. Fraction retention and mechanic-specific rounding remain policy for future calculations; do not add unused generic rounding code. Cumulative-effect helpers and each mechanic's rounding/tests can be introduced when calculations need them. No phase tracking or movement enforcement is part of the dice slice.
3. Continue concepts, classifications and geography in rulebook order, one or two features at a time, revisiting dependencies as needed. Later draft the Rule 6 phase specification and implement it in small slices rather than all of P01-P08 together.
4. Build ground movement and later systems with explicitly unavailable final rulings where required metadata or dependent rules are still missing. Continue logistics/stacking and combat dependencies before claiming complete movement legality.

The final interface redesign, scenario selection and computer opponents remain outside this backlog's immediate work. This file is the tracker to update as each rule slice is implemented; checking a row requires both implementation and validation evidence.
