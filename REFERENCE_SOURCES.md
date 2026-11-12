# Local rules and reference sources

Inspected 2026-10-20. This is a source inventory and targeted comparison, not a complete rule-by-rule reconciliation. No reference PDF was modified. The inventory includes 14 files representing 13 distinct byte sequences: the two UICFB copies are identical (SHA-256 verified).

## Citation convention

`R16a 6.3.c.i, printed p35 / PDF p37` identifies the edition, rule, printed page and one-based PDF viewer page. Both rulebooks have two opening pages before printed page 1; cited body pages therefore have PDF page = printed page + 2. Page references must always include an edition: pagination differs between editions. `C16 p7` refers to the chart's printed page 7 and PDF page 7. UIC/supply diagram references use one-based PDF pages.

Page links below open the source file; the written locator is authoritative if a viewer ignores a page fragment.

## Inventory

| ID | Local source | PDF pages | Identification and intended use |
|---|---|---:|---|
| R16a | [TSWW_PRODUCTON_RULES_V1_6a.pdf](reference/rules/TSWW_PRODUCTON_RULES_V1_6a.pdf) | 182 | Cover/footer: v1.6a, copyright 2023. User-selected governing general rulebook. Other documents retain their own editions and require reconciliation where relevant. |
| R16 | [TSWW_PRODUCTON_RULES_V1_6_PRINT.pdf](reference/rules/TSWW_PRODUCTON_RULES_V1_6_PRINT.pdf) | 176 | Cover/footer: v1.6, copyright 2019. Comparison edition and original companion to the v1.6 charts. |
| C16 | [TSWW GENERAL CHARTS v1.6.pdf](reference/charts/TSWW%20GENERAL%20CHARTS%20v1.6.pdf) | 35 | Charts and rules both labelled v1.6, copyright 2019. Tables require visual transcription and reconciliation with the selected rule edition. |
| UIC | [charts/UICFB.pdf](reference/charts/UICFB.pdf) | 4 | Unit Identification Table, map/terrain identification, colour/service and strategic-map keys; copyright 2019. Images/icons are material to interpretation. |
| UIC-copy | [reference/UICFB.pdf](reference/UICFB.pdf) | 4 | Byte-identical duplicate of UIC; do not treat as independent evidence. |
| SUP | [Supply Picture Barbarossa.pdf](reference/charts/Supply%20Picture%20Barbarossa.pdf) | 10 | Explanatory supply diagrams: continental p1; extended/AGHQ p2; overseas with QM p3; optional rail p4; without QM p5; river p6; air p7; ferries p8; mixed chain p9; closing page p10. Supporting illustrations, not an independent rules edition. |
| SUP-QM | [Supply Picture Barbarossa - OS wth QM.pdf](reference/charts/Supply%20Picture%20Barbarossa%20-%20OS%20wth%20QM.pdf) | 1 | Separate overseas/QM diagram. Related to SUP p3, but not a byte-identical file and not assumed to be an exact content duplicate. |
| MAP | [Map Layout and Regauge file.pdf](reference/charts/Map%20Layout%20and%20Regauge%20file.pdf) | 2 | Map arrangement p1; German rail regauging map/notes p2. Inspect with transportation and national rules. |
| AX-OB | [Axis OB PRINT.pdf](reference/orders_of_battle/Axis%20OB%20PRINT.pdf) | 108 | Axis order of battle; cover copyright 2019. Setup/appearance and national exceptions, for later data work. |
| MIN-OB | [Axis Minor Nations PRINT.pdf](reference/orders_of_battle/Axis%20Minor%20Nations%20PRINT.pdf) | 41 | Axis minor-nation OB; cover copyright 2019. |
| SU-OB | [Soviet OB Print v1.7.pdf](reference/orders_of_battle/Soviet%20OB%20Print%20v1.7.pdf) | 85 | Soviet OB; filename says v1.7, cover copyright 2019. Filename version is not proof of compatibility with R16a. |
| WA-OB | [Western Allied OB PRINT.pdf](reference/orders_of_battle/Western%20Allied%20OB%20PRINT.pdf) | 50 | Western Allied OB; cover copyright 2019. |
| START | [FB AT STARTS PRINT.pdf](reference/orders_of_battle/FB%20AT%20STARTS%20PRINT.pdf) | 126 | At-start setups; cover copyright 2019. Inventory only; no scenario chosen or implemented. |
| AX-REP | [FB Axis Replacements.pdf](reference/orders_of_battle/FB%20Axis%20Replacements.pdf) | 8 | Replacement schedules; PDF p1 contains German and other Axis schedules. Numerical tables have not been transcribed/validated. |

`reference_source_inventory.json` records the file hashes and page counts from this inspection.

## Edition comparison and decision register

User decisions recorded 2026-10-20: use R16a as the governing general rulebook; declare all attacks in the Combat Phase before resolving any, then calculate/resolve attacks individually; retain fractions unless the applicable mechanic explicitly specifies another method. These decisions are documented policy, not implemented gameplay checks. The user believes R16a shipped with the physical game; this provenance is unconfirmed, and page count alone does not establish authority.

| ID | Evidence | Consequence / disposition |
|---|---|---|
| SRC-01 | R16 cover/footer identifies v1.6/2019; R16a identifies v1.6a/2023. C16 p1 identifies v1.6/2019. | Resolved by user: R16a governs general rules; R16 is comparison material, C16 remains separately versioned tables. Flag new contradictions as encountered. A campaign rules profile and complete errata reconciliation are not yet implemented. |
| SRC-02 | C16 p1 Combat Phase describes individual attack declaration. R16 6.3.c.i printed p36 / PDF p38 and R16a 6.3.c.i printed p35 / PDF p37 instead require declaration of all attacks. | Resolved by user interpretation: declare all attacks in the Combat Phase before any attack results are calculated/resolved; then calculate and resolve attacks individually in the permitted order. User regards the chart as shorthand for individual resolution, not permission to declare additional attacks after seeing results. Preserve the wording discrepancy for traceability; no implementation blocker remains. |
| SRC-03 | R16 Rule 6 begins printed p35 / PDF p37; R16a begins p34 / PDF p36. Rule 15 begins R16 p109 / PDF p111 versus R16a p113 / PDF p115. | Never reuse an old page number as a citation for the new edition. This is confirmed pagination drift, not itself proof of a substantive rule change. |
| SRC-04 | R16a 6.3.b.iii.1, p34 / PDF p36 explicitly places airbase attacks and spotting ahead of other movement, despite naval/ground items appearing earlier in the numbered list. C16 p1 visually leads with those air tasks. | Implementation note, not a question or conflict: honour explicit pre-movement timing. A phase engine needs ordered substeps and interruption windows, not just seven flat labels. No user decision is required. |
| SRC-05 | R16a 2.A, p8 / PDF p10 retains fractions by default; 6.3.e, p35 / PDF p37 explicitly rounds pursuit allowance down. C16 p7 contains combined Going/combat/movement cells and road-only qualifications. | Confirmed by user: retain fractions by default; apply any explicitly specified mechanic-specific calculation/rounding method locally. No global rounding policy should override it. Transcribing only a trailing number from a terrain cell loses material restrictions. |
| SRC-06 | R16a Appendix 22.B, printed pp178-180 / PDF pp180-182 maps chart titles to chart pages; C16 pp17-18 rely on graphical unit icons and small qualifiers. | Use the appendix as a navigation aid, not proof that every v1.6 numeric value has been checked against v1.6a. Visually verify tables/icons/notes before creating machine-readable rules. |
| SRC-07 | SUP/SUP-QM explain alternative supply paths. R16a 15.C-E, printed pp115-117 / PDF pp117-119 distinguishes systems and an optional no-QM system. | Keep systems/options separate; do not combine permissions from different diagrams into one unrestricted supply graph. Detailed supply reconciliation remains future work. |

## Inspection scope

Extracted searchable text from the local reference set; read rulebook contents/indexes, opening identification, arithmetic/dice concepts, ground-unit/stacking and movement material, order of play, and selected combat material. Surveyed chart page contents and supporting diagrams. Visually checked representative order-of-play, terrain, unit identification and supply pages, including the v1.6 combat declaration page. Inspected OB covers/openings for inventory, not every roster entry. This does not certify every rule, chart cell, national exception, OB entry, or cross-edition change.

No outstanding user decision blocks the first foundations slice. Review optional-rule choices and detailed numerical ambiguities when their mechanics are reached, not as an upfront questionnaire. Work through the rulebook slowly, one or two features at a time, beginning with Rule 2 foundations. Scenario selection and the final interface redesign remain deferred.

## Side-setup roster clarification

The user confirmed using the local UICFB as the correct reference rather than their other 2021 key. The local key has four pages: National Colour Identifiers on PDF p3 and Strategic Map Terrain Information on p4; no neutral roster is present. Setup groups service branches under their nations, keeps Inter Allied as a distinct control pool, and treats the Axis/Western Allied/Soviet headings as editable force-group defaults. These are not date-sensitive national war-entry rulings. Nation aliases are explicit matching conveniences, not rules assigning foreign contingents. Neutral nations remain manually addable. See PROJECT_CONTEXT.md for the implemented setup scope.


## Counter metadata layout clarification — 2026-10-30

UICFB PDF p2 and R16a 4.A.3.a.i-iv (printed p19 / PDF21) distinguish printed CD components: 3/2 has level 3 and long component 2; total short-range gunnery includes both components and is not calculated by the metadata editor. R16a describes CD levels 1–8, but VASSAL artwork includes higher values (for example Trondheim 18/2 and 22/5). Preserve the artwork values under the user's VASSAL-reference policy; flag this as a rule/artwork discrepancy for future gameplay implementation rather than imposing a cap.

R16a 5.C.2.e.ii-iii (printed p32 / PDF34) identifies SSF bottom-right values as patrol range and separately gives a combat speed. R16a 5.C.4 (printed p33 / PDF35) excludes both SSF and FAS from printed tactical-speed ratings. FAS bottom-right values remain literal metadata until their interpretation is established. UICFB PDF p2 states unprinted commander modifiers have no effect; metadata completeness does not require invented zero/N/A entries. These are editor/data-layout decisions, not implemented gameplay calculations. See [COUNTER_EDITOR_FORMAT_REVIEW.md](COUNTER_EDITOR_FORMAT_REVIEW.md).
