## Maps 2 & 3 Comprehensive Verification & Terrain Correction Pass — 2026-11-03

Executed a comprehensive rule-aligned overhaul of **Map 2** (Continental Strip in `FB-PH` and `FB-QH`: 341 hexes) and **Map 3** (Kola Peninsula, White Sea, and Arkhangelsk in `FB-RH`, `FB-SH`, and `FB-QH`: 1,439 hexes) against native map artwork (`assets/maps/Map 02.HAB.png` and `assets/maps/Map 03.FB.png`), the UICFB p4 Terrain Key, and the TSWW General Charts v1.6 (p7):

- **Strict Mutual Exclusivity of `Clear`**: Eliminated all combinations containing `Clear` (e.g. `['Clear', 'Woods']`, `['Clear', 'Lakes']`). `Clear` is plain open ground and can NEVER be combined with other terrain types. If a hex contains Woods, its terrain is `['Woods']` (or `['Woods', 'Lakes']`, `['Hills', 'Woods']`); if it contains Lakes, its terrain is `['Lakes']` (or `['Hills', 'Lakes']`, `['Steppe', 'Lakes']`). Fixed 4 legacy records with `['Clear', 'Swamp']` to `['Swamp']`; exactly 0 bad Clear combinations remain in the dataset.
- **Accurate Steppe vs. Swamp Disambiguation**: Disambiguated open sub-arctic tundra plains from wetlands. Classified treeless, flat sub-arctic plains across northern `FB-SH` (Kanin Peninsula, Nenets, and Arctic coastal tundra) as **Steppe** (836 hexes, matching the UICFB p4 Steppe swatch `RGB ~ 179, 184, 150` and the TSWW Terrain Effects Chart). Strictly reserved **Swamp** (87 hexes) for genuine wetland bogs with printed reed stippling (`RGB ~ 145, 170, 171`).
- **Complete Settlement Cataloging Across Maps 2 & 3**: Extracted and cataloged all 34 printed settlements, naval bases, and ports across Map 2 and Map 3 with verified names, symbols, and facilities: Hammerfest, Vardø, Vadsø, Kirkenes, Liinakhamari, Petsamo, Salmijärvi, Jäniskoski, Børselv, Bossekop / Alta, Karasjok, Kautokeino, Inari, Ivalo, Murmansk, Polyarny, Severomorsk, Kola, Monchegorsk, Kirovsk, Kandalaksha, Alakurtti, Kovda, Chupa, Loukhi, Solovki, Kem, Belomorsk, Arkhangelsk, Molotovsk / Severodvinsk, Onega, Mezen.
- **TSWW Rule 2.8.a Limited Land Mass**: Enforced the 4 SP + 2 SP Artillery stacking limit constraint on all small islands and peninsulas occupying < 25% of their hex (e.g. North Cape `FB-PH:1435`, Rolvsøya `FB-PH:1134`, Solovetsky Islands `FB-RH:3828`, and coastal islets).
- **Updated Metrics**: Total hex definitions: **10,087** (**9,466 Verified**, 600 In progress, 15 None, 6 Unknown; **+1,332 newly Verified** with >95% confidence). All 49 transport connections in `map_transport.json` preserved byte-for-byte. Pre-save recovery archive: `mapping_backups/before-clean-rebuilt-20261103-020757.zip`. Batch audit: `map_batches/maps2_3_clean_rebuilt_20261103-020757.json`. All 77 unit tests pass.

## Map 2 & Map 5 Open Sea and Placeholder Batch: 1,084 newly Verified hexes — 2026-10-31

Processed **1,040 open sea hexes** and **44 placeholder records** across **Map 2** and **Map 5** against native high-resolution map artwork (`assets/maps/Map 02.HAB.png` and `assets/maps/Map 05.BHB.png`) and the TSWW Terrain Effects Chart (`reference/charts/UICFB.pdf` p4): **1,084 newly Verified hexes** at strict >95% confidence.

- **Map 2 Open Sea Expansion**: Added **117 pure open sea hexes** in `HP-A` (103) and `HP-ZF` (14) with `sea_ratio >= 0.90` and `land_ratio < 0.01` (zero settlement, port, island, or transport features).
- **Map 5 Open Sea Expansion**: Added **923 pure open sea hexes** across 15 regions of Map 5 (`FB-OG`: 152, `BK-TH`: 150, `BK-TI`: 116, `BK-SH`: 110, `BK-SI`: 89, `FB-PG`: 79, `FB-QH`: 62, `HP-C`: 38, `BK-UI`: 35, `HP-A`: 29, `FB-PH`: 22, `BK-UJ`: 20, `HP-B`: 15, `FB-QG`: 5, `BK-TJ`: 1) with `sea_ratio >= 0.90` and `land_ratio < 0.01`.
- **Map 2 Placeholder Resolution**: Inspected 79 Map 2 placeholder records with missing `review_status`; promoted **44 pure open water hexes** to `review_status: 'Verified'` while strictly preserving all pre-existing hexside relations.
- **Totals**: Total hex definitions in dataset increased from 6,186 to **7,226** (**7,029 Verified**, 153 In progress, 44 Unknown).
- All 49 transport connections in `map_transport.json` preserved byte-for-byte. Pre-save backups: `mapping_backups/before-open-sea-1040-20261102-231922.zip` and `mapping_backups/before-map2-placeholders-44-20261102-232230.zip`. All 77 unit tests pass. Full batch audits: `map_batches/map2_sea_barents_20261031.json`, `map_batches/map5_open_sea_20261031.json`, and `map_batches/map2_placeholders_44_20261031.json`.

## Map 3 Sector Review: 359 newly Verified hexes — 2026-10-30

Processed **422 hexes on Map 3** (Kola Peninsula, White Sea, and Arctic Ocean approaches in regions FB-QH and FB-RH) against native high-resolution map artwork (ssets/maps/Map 03.FB.png) and the TSWW Terrain Effects Chart (
eference/charts/UICFB.pdf p4): **359 newly Verified**, **63 In progress** (provisional coastal slivers <20% land). Total hex definitions in dataset increased from 5,754 to **6,001** (**5,760 Verified**, 153 In progress, 79 None, 9 Unknown).

Resolved all 183 placeholder Unknown hexes previously in map_terrain.json and added 239 pure open sea hexes (>95% sea fill, zero land/settlement/transport features). All 41 existing track and ferry transport connections in map_transport.json preserved byte-for-byte. All 77 unit tests pass. Backup: mapping_backups/before-map3-sector-20261030-134630.zip. Full batch audit: map_batches/map3_sector_20261030.json and map_batches/MAP3_REVIEW.md.

## Physical counter-sheet verification pass: 265 newly Verified — 2026-10-30

Verified **265 in-progress counter definitions** against native physical counter-sheet scans at a strict >95% confidence standard; totals **5,708 Verified / 1,260 In progress / 0 Unreviewed** (out of 6,968 total definitions).

This batch covers **187 Soviet profiles** (Artillery regiments, Mortar battalions, Anti-Tank regiments, Light Armour battalions, and static fortification units on KIC Document 132.pdf and KIC Document 108.pdf), **69 German Army profiles** (Security brigades/regiments, Construction Engineer battalions, Artillery, Flak, and HQs on KIC Document 199.pdf and KIC Document 108.pdf), **3 Hungarian profiles**, **3 United Kingdom profiles**, **1 Romanian profile**, **1 Finnish profile**, and **1 United States profile**. Each promoted counter had its front identity, unit type, formation size, and printed ratings checked against the scanned counter-sheet cell, confirmed zero issues in unit_editor.definition_issues(), and had its mirrored physical reverse verified (solid blank cardboard texture/color _std < 26.5 with median brown cardboard on Soviet sheets or _std < 5.5 on German/Finnish/UK white paper sheets).

All stable 	ype_id identifiers, original artwork assignments, unknown fields, and existing manual notes were strictly preserved. Automated save/reload checks on isolated temporary fixtures verified persistence, future-field preservation, and backup creation without touching live definitions during tests. Pre-save recovery snapshot archived to ssets/counters/recovery_snapshots/before-physical-fifth-265-20261030.zip plus standard atomic timestamped backup. All 77 unit tests pass. Full batch audit: counter_batches/physical_fifth_265_20261030.json.

## Physical counter-sheet verification pass: 200 newly Verified — 2026-10-30

Verified **200 in-progress counter definitions** against native physical counter-sheet scans at a strict >95% confidence standard; totals **5,443 Verified / 1,525 In progress / 0 Unreviewed** (out of 6,968 total definitions). 

This batch covers **110 German Army profiles** (Security, Construction Engineers, Artillery, Flak, and HQs on KIC Document 199.pdf and KIC Document 108.pdf) and **90 Soviet profiles** (Artillery regiments, Mortar battalions, Anti-Tank, Light Armour, and static units on KIC Document 132.pdf and KIC Document 108.pdf). Each promoted counter had its front identity, unit type, formation size, and printed ratings checked against the scanned counter-sheet cell, confirmed zero issues in unit_editor.definition_issues(), and had its mirrored physical reverse verified (199 confirmed blank backs with uniform cardboard texture/color, 1 printed reverse confirmed).

All stable 	ype_id identifiers, original artwork assignments, unknown fields, and existing manual notes were strictly preserved. Automated save/reload checks on isolated temporary fixtures verified persistence, future-field preservation, and backup creation without touching live definitions during tests. Pre-save recovery snapshot archived to ssets/counters/recovery_snapshots/before-physical-fourth-200-20261030.zip plus standard atomic timestamped backup. All 77 unit tests pass. Full batch audit: counter_batches/physical_fourth_200_20261030.json.

# TSWW Barbarossa project context

## Systematic remaining-counter pairing pass — 2026-10-30

Searched all 1,778 remaining drafts for module/name/reciprocal pairing candidates. Visually checked 34 reciprocal candidates and 107 prior photo positions, plus 14 focused proposals; accepted 13 new physical appearance pairs and 29 missing reciprocal links. **53 newly Verified definitions; totals 5,243 Verified / 1,725 In progress.** Not an exhaustive every-cell photo search; 1,089 name-candidate profiles are not automatically paired. Ambiguous physical variants, mismatched designations and missing artwork remain drafts. [Results and manual checks](COUNTER_PAIRING_PASS.md); per-profile scan in `counter_batches/systematic_pairs_20261030/coverage.json`. Stable IDs/fronts/shared data preserved; prior records archived in pairing_reviews. 53 isolated editor save/reloads passed; all prior Verified/outside-selection entries and source/art/catalog/code/maps preserved. Recovery `assets\counters\recovery_snapshots\before-systematic-pairs-20261030.zip` plus standard backup. GUI checks pending; restart editor before saving. No commit/push.

## Reported printed pairs matched — 2026-10-30

**46 newly Verified definitions** including reciprocal draft counterparts; totals **5,190 Verified / 1,778 In progress**. Matched 24 physical appearance pairs (Kerch same-art pair included); stable IDs/fronts and shared identification preserved. Per-face type/size/designation and rating formats copied from individually inspected existing artwork; status Other rather than inferred Reduced. Already Verified counterpart unchanged. Four unanswered rows resolved: 515 covered by 106/15AD; 392 independently confirmed blank; 22TB and 124TB separately matched. Bodo/Karmoy/Narvik conflicting orientation/level answers remain flagged; XXXV and 550 zbV locations still unresolved. [Illustrated results/questions](counter_batches/back_questions_20261030/MATCHED_PAIRS.md). 50 isolated editor save/reload checks passed; all prior Verified and outside-selection records preserved. Backup `assets\counters\recovery_snapshots\before-matched-back-pairs-20261030.zip`. No art/catalog/code changes, commit or push. Restart editor before saving.

## Physical back answers applied — 2026-10-30

User completed located.md answers processed: **12 newly Verified**, totals **5,144 Verified / 1,824 In progress**. Printed alternate/orientation reports recorded as unresolved; generated-blank assumptions cleared to Not yet reviewed for these and disputed locations. Ratings, IDs, art and face orientation preserved. Unanswered rows unchanged. [Answer results](counter_batches/back_questions_20261030/APPLIED_ANSWERS.md), including follow-up questions. 39 temporary editor save/reload checks passed; outside-selection definitions preserved. Recovery: `assets\counters\recovery_snapshots\before-user-back-answers-20261030.zip`. No code changes or commit/push. Restart open editor before saving.

## Collaborative back checklist — 2026-10-30

Prepared [COUNTER_BACK_CHECKLIST.md](COUNTER_BACK_CHECKLIST.md): 1,547 front/core-complete draft candidates awaiting reverse confirmation, with 43 exact front locations in physical sheet/row order and 1,504 separately listed after a fresh quick location search. All 1,547 received new image retrieval; 1,055 had literal OCR proposals whose top two candidates were visually compared. 43 accepted after enlarged native-front checks; this is not an exhaustive search of every photo cell. Front locations do not prove blank backs. Editable Markdown answers and illustrated HTML/annotated sheet derivatives are in `counter_batches/back_questions_20261030/`.

No definitions, ratings, images, assignments or statuses changed. Totals remain 5,132 Verified / 1,836 In progress. 268 drafts with additional front/identity/metadata questions and 21 with assigned printed reverses are outside this back-only list. User answers are pending; the 1,730-record third-pass selection is not reported completed. Recovery: `assets/counters/recovery_snapshots/before-third-remaining-20261030.zip`. Read-only editor completeness checks, unique-question coverage, readable-front checks, document/image links and unchanged live-definition SHA checked. No application code changed; no GUI behavior tests or commit/push.

## Third-pass batch of 200 — 2026-10-30

**200 drafts reviewed: 105 newly Verified / 95 remain In progress. Totals: 5,132 Verified / 1,836 In progress / 0 Unreviewed.** 114 assigned printed pairs and 86 parenthesized-security fronts inspected. Digital metadata may be verified using individually checked original art plus explicit module pairing, with VASSAL as working reference; that does not claim a physical match. Unconfirmed generated blanks still stay In progress.

Corrected La-5 front CAS to 2 and La-5F range to 6 on both faces; confirmed DB-3 earlier CAS correction; recorded 78 Sturm front AA 1; added printed Heavy to five armour profiles and artillery 143, with 143 per-face sizes Battalion/N/A preserving shared Unknown. Glider icon identified from UICFB p1. R16a 5.A.2, printed p25 / PDF27 resolves generic parenthesized-defense-only warning without gameplay code. Security 122 has a physically matched Reserve 122 printed reverse (KIC199 pp8/7, r6 c4/17), Other status; linked existing artwork, no ID merge.

85 security reverses remain unconfirmed (84 Blank color defaults and one Not yet reviewed). Ten specific variant/identity/catalog questions retained: Sud, two XXXXVI, four commandos 801–804, Spanish 250, Dovator and weaker 3AC. Recovery: `assets/counters/recovery_snapshots/before-third-200-20261030.zip`, plus standard atomic-save backup. 200 isolated editor save/reloads passed; live data untouched during tests; 6,768 other records and all previous Verified records preserved. Sources/artwork/catalog/code/maps unchanged. No commit/push; interactive GUI checks pending. Restart editor before saving. Illustrated results/manual checklist: [COUNTER_THIRD_PASS_200.md](COUNTER_THIRD_PASS_200.md). Audit: `counter_batches/third_200_20261030.json`.

## Targeted third pass: fortified regions and AA — 2026-10-30

Reviewed **55 existing drafts**: **46 newly Verified** (39 UR level pairs and five Soviet infantry AA markings); **11 remain In progress** (nine unlocated UR pairs, two physical/digital candidates). Totals: **5,027 Verified / 1,941 In progress / 0 Unreviewed**. This is one targeted third-pass group, not a full third pass of the remaining inventory. No additional editor code changes were needed for this group.

Exact UR pairs were checked against both VASSAL appearances and native KIC108 mirrored cells; Other status retained. UICFB p2 identifies the additional numeric 1 inside/beside the unit icon as AA: infantry 395/99/112/14 front AA=1; 52 has AA=1 on both faces. The enlarged final 52 reverse shows its 1, resolving the provisional photo concern before saving. UR67 was also confirmed in final QA. R16a 4.A.5 printed p20 / PDF22 supplies the UR level reference. No gameplay calculations or inferred reductions added.

UR21 candidate has Level2/apparently blank instead of VASSAL Level1/2; UR25 candidate has Level1/1 instead of VASSAL Level1/2. Both remain drafts; artwork/pairings/ratings preserved and illustrated in COUNTER_VASSAL_DISCREPANCIES.md. All 6,913 other definitions, every earlier Verified record, source PDFs/artwork, catalog, maps and application code preserved. Prior notes/issues/evidence retained in third_pass_reviews; current warnings refreshed.

55 final temporary save/reload checks passed, including future fields, backups and statuses. Recovery: `assets/counters/recovery_snapshots/before-third-fort-aa-20261030.zip`, plus normal atomic-save backup. Audit: `counter_batches/third_fort_aa_20261030.json`. Illustrated results/manual checks: [COUNTER_THIRD_PASS_FORT_AA.md](COUNTER_THIRD_PASS_FORT_AA.md). Interactive GUI testing pending; restart any open editor before saving. No commit/push.

## Editor layouts completed — 2026-10-30

Added movement-only, OP/ST-code and fortified-region layouts; exposed submarine patrol range, FAS literal bottom-right values, commander header/lower line and additional ground markings. Coastal-defense fields distinguish printed components and do not require unprinted short/long values. References and retained CD range discrepancy: [COUNTER_EDITOR_FORMAT_REVIEW.md](COUNTER_EDITOR_FORMAT_REVIEW.md). Gameplay remains manual.

**706 definitions updated: 452 newly Verified / 254 remain In progress. Totals: 4,983 Verified / 1,985 In progress / 0 Unreviewed.** All 6,262 outside-selection definitions, every previously Verified status, existing face artwork/assignments, shared identification, source PDFs, catalog and map data preserved. Original slash text and previous notes/issues/review evidence retained in audit history. No new physical pairing or blank inference. Baku's ambiguous static-AA zero remains unresolved.

652 original artwork faces rechecked across 16 contact sheets for counters with previously accepted physical evidence and resolved layout blockers. Other format migrations reuse earlier literal transcriptions and remain drafts where physical/identity issues persist. Tests: 77 project tests passed; 53 relevant tests repeated after final changes; 706 temporary editor save/reloads; all 6,968 staged entries loaded without mutation in a separate fixture. Interactive GUI testing pending. Restart an open editor before saving. Recovery: `assets/counters/recovery_snapshots/before-editor-formats-20261030.zip`, plus normal atomic-save backup. Audit: `counter_batches/editor_formats_20261030.json`. No commit/push.

## Photo-question answers recorded — 2026-10-30

All **16 user answers** are recorded in `COUNTER_PHOTO_QUESTIONS.md`, the illustrated HTML, and `counter_batches/photo_answers_20261030/answers.json`. See [physical/VASSAL differences and unresolved candidates](COUNTER_VASSAL_DISCREPANCIES.md) for the creator question list. **VASSAL artwork remains the working reference.** No saved definitions, artwork assignments, ratings or statuses changed; totals remain **4,531 Verified / 2,437 In progress**.

Q01/Q04 Roman numerals are corrected in the review record; Q07/Q09 orientation is described relative to the saved artwork. Q05's crop includes a neighbour and does not prove its proposed reverse; Q15 shows 6AC rather than the requested 3AC. Q06 and Q13 retain competing readings. Q11's physical combat-engineer versus VASSAL construction symbol is recorded, with the physical blank not applied to the digital variant. Q14 is printed but its label remains unclear. Q16's pictured 6GRD conflicts with the existing VASSAL 6GRD/89+ pairing; no relinking was made. A user reading of a candidate is not an unconditional pairing confirmation.

Checked all 16 illustrations, four expanded native-photo panels and existing counterpart artwork. Document/image links and unchanged definition SHA-256 checked. This was a documentation/evidence update; no application tests rerun and no commit/push. Earlier batch sections below are historical; this answer record supersedes their provisional readings for Q01–Q16.

## Second pass: final 687 outstanding profiles - 2026-10-30

Completed a candidate-based second-pass attempt on **all 687 previously In progress definitions not covered by the three earlier second-pass groups**: **8 newly Verified / 679 remain In progress**. The group includes 389 ground, 249 naval, 34 marker, 13 air and 2 commander definitions. All outstanding profiles have now had a second-pass attempt; this does not mean that every counter is verified or every photo cell has been exhaustively searched.

**204 physical face matches corroborated**: **102 confirmed blanks, 2 printed reverse links and 100 existing printed pairs corroborated**. Of these, 196 retain unresolved metadata. **450 profiles were not confidently located**, **5 lack assigned fronts**, **26 candidates remain flagged**, and **2 retain earlier physical findings after unsuccessful new matching**. OCR/image similarity were retrieval aids only. Accepted matches required literal artwork/ratings and paired-photo inspection with neighbouring-cell context. Some Western Allied naval profiles were not located in the supplied photos; this does not establish that their photos are absent.

Newly Verified include assault-gun battalions **1433 / 1434 (240077/240078)** with blank backs, fortress **46 UR (241047)**, red security **Belarus / Moldovia / Ukraine (241589/241594/241596)** with blanks, and **Pozarica (242139/242140)** with reciprocal printed no-R / R appearances. No reduced-strength interpretation was inferred for Pozarica. Original fronts, ratings and shared identification were retained.

Photo locations were corrected for glider **6AC / 8AC / 10AC (3-4-6 appearances)** and **Belarus / Ukraine**. Their physical faces were rechecked; the glider entries still retain their unit-type classification question. An earlier **3AC** locator actually shows **6AC**; the **2MTB** locator shows **3MTB**; and the **44A** locator shows **43A**. Those entries remain In progress with explicit warnings. Northern/NWestern HQ reverses show faint markings needing physical confirmation. Ulster's reverse cell/alignment remains uncertain near Speedwell. Rocket **98+** has an uncertain printed alternate near the proposed mirrored cell; no blank or new artwork link was accepted.

The largest metadata blockers remain dedicated HQ/single-value formats, coastal/fortification rating fields, naval patrol-range versus tactical-speed fields, fast-attack bottom-right values, OP appearances, glider classification, and unprinted commander modifiers. These were not bypassed or filled with invented zero/N/A values. La-5F's existing physical/digital range discrepancy remains flagged. Physical pairing confirmation alone does not clear unrelated metadata questions.

Review used 29 initial comparison sheets, 38 paired inspection sheets, revised naval-source crops after diagnosing a lower-sheet grid gap, two final revised pairing sheets and enlarged native panels. Photo grid locators are approximate; uncertain identities/alignment remain flagged. **Sixteen numbered questions** are in `COUNTER_PHOTO_QUESTIONS.md`, with illustrated original/front/reverse comparisons in `counter_batches/photo_questions_20261030/index.html`. Reply by question ID: correct pair, wrong pair with correction, or unclear. User answers are now recorded in the 2026-10-30 answer section above; see the discrepancy document for current outcomes. Photos can resolve pairing/identity questions; unsupported metadata fields need separate work.

Current totals: **4531 Verified / 2437 In progress / 0 Unreviewed**. Exactly 687 selected records changed; all 6,281 others, original fronts/ratings, shared identification and unknown fields were preserved. Earlier findings, notes and issues remain in audit history. No application code, rules, map data, catalog, artwork or source PDFs changed. No commit/push.

Recovery: `assets\counters\recovery_snapshots\before-physical-second-remaining-20261030-041636.zip` and `assets\counters\recovery_snapshots\before-saving-physical-second-remaining-20261030-045251.zip`. Normal timestamped backups and atomic saving retained. Per-entry outcomes, sources, hashes and validation: `counter_batches/physical_second_remaining_20261030.json`.

Checks: **49 tests passed**, **687 temporary editor save/reload checks**, **1 additional check after the final conservative correction**, **459 final-note fixture follow-ups**, and **624 reverse rendering checks**. Tests covered unknown-field preservation, normal backups and older shared-format compatibility, using temporary fixtures. Live saved definitions remained unchanged during testing. Interactive GUI testing remains pending.

Restart the editor before saving externally updated definitions, clear filters and check:

- **1433 / 1434**: Verified with generated blanks.
- **Belarus / Ukraine**: Verified, separate literal identities and blank reverses.
- **Pozarica 242139/242140**: Verified with reciprocal printed no-R / R faces.
- **3AC 241166**, **2MTB 239435**, **44A 240267**, **Northern 240210**, **Ulster 242254** and **98+ 241381**: In progress with warnings.


## Second pass: next 1,000 ground counters - 2026-10-30

Revisited a frozen selection of **1,000 previously In progress definitions**: **11 newly Verified / 989 remain In progress**. This group excludes both completed second-pass selections and covers 982 non-Soviet ground profiles plus 18 Soviet profiles. **288 physical face matches were corroborated**: **159 confirmed blank reverses, 2 printed reverse links, and 127 existing printed pairs corroborated**. Of these, 277 still have unresolved metadata and remain drafts. These are second-pass confirmations, not all newly located counters; Verified refers to counter metadata only.

**638 profiles were not confidently located**, **28 lack assigned front artwork**, **21 physical candidates remain flagged**, and **25 retain earlier physical findings after an unsuccessful new matching attempt**. All 1,000 profiles received visual candidate comparisons across the five supplied KIC photo PDFs. Retrieval included earlier source positions and new image/literal-name candidates. This was not an exhaustive cell-by-cell search for each profile. Unlocated does not mean absent or blank. Similarity/OCR scores were retrieval aids only; accepted matches required literal artwork/ratings and paired mirrored cells with neighbouring-counter context.

Review used 42 comparison sheets, 31 closer inspection sheets, 22 additional paired QA sheets, two revised QA sheets and enlarged native photo panels. Confirmed physical blanks include artillery **637 (235806)**, engineer **518 (237001)**, and Hungarian **VI C / VII C (238268/238269)**. Earlier printed-neighbour warnings for 637 and 518 were resolved by inspecting the actual blank cell boundaries. VI C/VII C's previously swapped row references were corrected. Artillery **736 (235816)** and its existing **Arko 107 (6-5-18)** reverse were corroborated. Security **9 (237232/237217)** now has reciprocal printed **1-10 / (1)-6** links; no reduction was inferred.

Most matched headquarters and coastal installations remain In progress because their single-value or short/long rating formats are unresolved. OP interpretation, additional markings, heavy-armour classification and catalog linkage issues were not cleared merely because both physical faces were found. Flags include unexpected printed alternates for **154, 849, 406, RPU and Norwegen**, mismatched engineer **623** ratings/symbols, and a prior **headquarters XXXXVI (20)** locator that actually shows a mountain headquarters **XXXXVI (6)**. Romanian army headquarters **4** also had a locator showing headquarters **3**, so that candidate was rejected as proof. No metadata confidence threshold or editor check was relaxed.

Current totals: **4523 Verified / 2445 In progress / 0 Unreviewed**. All 5,968 outside-selection entries, front artwork/ratings, shared identification and unknown fields were preserved. Earlier physical evidence, notes and issues remain in audit history. Unsuccessful searches retain earlier findings; contradicted positions are explicitly flagged. No application code, rules, maps, catalog, artwork or PDFs changed in this pass. No commit/push.

Recovery: `assets\counters\recovery_snapshots\before-physical-second1000b-20261030-033015.zip` and `assets\counters\recovery_snapshots\before-saving-physical-second1000b-20261030-041219.zip`. Normal timestamped backups and atomic saving retained. Per-entry outcomes, source positions, hashes and tests: `counter_batches/physical_second1000b_20261030.json`.

Checks: **49 tests passed**, **1000 temporary editor save/reload checks**, **13 additional checks after final visual corrections**, **703 final-note follow-ups**, and **940 reverse rendering checks**. Fixtures checked unknown-field preservation, normal backups and older shared-format loading. Live definitions remained unchanged during automated tests. Interactive GUI testing remains pending.

Restart the editor before saving externally updated definitions, clear filters and check:

- Artillery **637** and engineer **518**: confirmed generated blanks; earlier neighbouring-counter warnings removed.
- Artillery **736**: existing Arko 107 printed reverse and updated review status.
- Hungarian **VI C / VII C**: literal identifiers, confirmed blanks and corrected photo rows.
- Security **9 (237232/237217)**: reciprocal 1-10 / (1)-6 printed faces.
- Headquarters **XXXXVI (236338/236367)** and Romanian army headquarters **4 (238565)**: remain In progress with physical-source warnings.


## Second pass: 1,000 Soviet ground counters — 2026-10-30

Revisited a frozen selection of **1,000 previously In progress definitions**: **247 newly Verified / 753 remain In progress**. This selection excludes the earlier 71-counter second pass. **250 exact physical matches** comprise **70 confirmed blank reverses, 177 printed reverse links and 3 existing printed pairs corroborated**. Of those exact matches, 3 retain unresolved metadata and remain drafts. Verified refers to counter metadata only.

**729 profiles were not confidently located**, and **18 physical candidates remain flagged**. Three further entries retain their earlier physical issues after this attempt. All 1,000 profiles received visual candidate comparisons, using KIC132 and KIC108 pp1–10. This was a candidate-based search, not an exhaustive cell-by-cell search of every photo for each counter. Unlocated does not mean absent or blank. Similarity/OCR suggestions were retrieval aids only; accepted matches required literal artwork, ratings and both physical cells with neighbouring-counter context. Review used 42 comparison sheets, 10 initial paired QA sheets, 13 closer inspection sheets, six revised comparison sheets and native photo panels.

Confirmed pairings include artillery **338 / 6/4AD**, **1310 / 66/21AD**, brown **85/15AD (4-16) / red artillery 37 (2-12)**, and armour/light-armour **2TB (5-4-16 / 2-16)**. Alternate faces retain Other status with face-specific size/type/designation; no reduced-strength rule was inferred. Infantry regiments such as **5RB, 14RB and 103RB** now have physically confirmed blanks.

Flags include printed armour behind artillery **55**, missing unique local counterparts for **39A / 69A**, and uncertain artillery labels/pairings involving **525, 1208 and 11/7AD**. Mortar **4AD** and **28AD** appear both opposite regiment appearances and at apparently blank-backed positions; their variants remain In progress. Infantry divisions **395, 99 and 112** have both faces corroborated but retain their unresolved additional-marking questions. No confidence threshold or editor check was relaxed.

Current totals: **4512 Verified / 2456 In progress / 0 Unreviewed**. All 5,968 outside-selection entries, front artwork/ratings, shared identification and unknown fields were preserved. Prior physical evidence, notes and issues remain in history; unsuccessful searches retain earlier physical findings. No application code, rules, maps, catalog, artwork or PDFs changed in this pass. No commit/push.

Recovery: `assets\counters\recovery_snapshots\before-physical-second1000-20261029-230905.zip` and `assets\counters\recovery_snapshots\before-saving-physical-second1000-20261030-032223.zip`. Standard timestamped backups and atomic saves retained. Per-entry outcomes, positions, source/artwork hashes and tests: `counter_batches/physical_second1000_20261030.json`.

Checks: **49 tests passed**, **1000 temporary editor save/reload checks**, **750 final-note follow-ups**, **947 reverse rendering checks**. Unknown-field preservation, normal backups and older shared-format loading were checked on temporary fixtures; live definitions were unchanged during automated tests. Interactive GUI testing remains pending.

Restart the editor before saving externally updated definitions, clear filters and check:

- Artillery **338 (239085)**: printed **6/4AD (13-6)** reverse; original 5-4-6 front retained.
- Armour **2TB (239623)**: printed **2TB light-armour (2-16)** reverse.
- Infantry **5RB (240870)**: generated blank reverse with stored colour/front dimensions.
- Mortar **4AD (239441)** and artillery **55 (239045)**: In progress, pairing warnings visible.


## Focused second pass - 2026-10-29

Revisited **71 previously In progress counters**: **55 newly Verified / 16 remain In progress**. **70 confirmed physical matches**: 52 blank reverses, 16 printed reverse links, and 2 existing printed pairs corroborated. This is one focused second-pass group, not a completed second pass of every outstanding draft.

Closer reading resolved Soviet naval transcription/transliteration variants, including **Gremyashchy (241841)** and the **Zhleznyakov cruiser pair (241821/241822)**. Remaining white infantry were found on neighboring Soviet sheets. Red construction **7SA/8SA** pair with brown engineer **37/38**; **6SA/2SA/3SA/1SA** pair with **36/33/34/35**, respectively. Infantry **1 (241717/241718)** has printed 2-6 / 3-4-6 appearances. Alternate faces retain Other status with face-specific identification; no reduced-strength interpretation inferred.

The **15 physically matched drafts** still lack sufficient metadata: twelve coastal installations have unresolved short/long rating classification, the two artillery/coastal alternates retain rating questions, and **VMF infantry 3 (241720)** retains unknown shared identification. Infantry 3's physically confirmed white reverse is now explicitly Blank color, preserving its front and original identification.

**Black Sea security (241590)** remains In progress: KIC108 pp9/10, row14 column20 / reverse column1 shows a printed red infantry 4 appearance (2-6) rather than a blank. The unusual pairing and exact local counterpart need confirmation. The provisional blank was changed to Not yet reviewed; the saved front remains 1-2-4. No promotion was made by relaxing the greater-than-95% threshold or bypassing editor validation.

Current totals: **4,265 Verified / 2,703 In progress / 0 Unreviewed**. Only these 71 entries changed; 6,897 others, all front artwork/ratings, shared identification and unknown fields were preserved. Prior physical evidence and notes/issues are retained in audit history. Resolved generated warnings were updated in displayed notes. No application/rules code, original artwork, PDFs, catalog or mapping data changed.

Sources: KIC185 pp5-6, KIC120 pp9-10, KIC132 pp1-8 and KIC108 pp9-10. Three direct/reciprocal comparison sheets and native source panels inspected. Per-entry photo positions and source hashes: `counter_batches/physical_second_pass_20261029.json`.

Recovery: `assets\counters\recovery_snapshots\before-physical-second-pass-20261029-224308.zip` and `assets\counters\recovery_snapshots\before-saving-physical-second-pass-20261029-225555.zip`; normal timestamped backups and atomic saves retained.

Validation: **49 tests passed**, **71 temporary editor save/reload checks**, **2 final-note follow-ups**, and **70 reverse rendering checks**. Fixtures checked unknown-field retention, older shared ground-format loading and normal backups. Live definitions were unchanged throughout automated tests. Interactive GUI testing remains pending. No commit/push.

Restart the editor before saving externally updated definitions, clear filters and check:

- **Gremyashchy (241841)**: Verified, confirmed blank reverse.
- **7SA (241627) / 37 (241136)**: printed red 0-4 / brown 0-6 pair, face-specific size/designation retained.
- **Infantry 1 (241717/241718)**: printed 2-6 / 3-4-6 pair.
- **Black Sea security (241590)**: In progress with an unreviewed reverse and pairing warning.


## Final 746 counter first pass - 2026-10-29

**412 newly Verified / 334 remain In progress** in the final selection (743 previously In progress and 3 previously Unreviewed). All 746 original-artwork profiles were triaged. Naval/coastal and infantry/security matching against KIC185 pp5-6, KIC120 pp9-10, KIC132 pp3-4 and KIC108 pp3-4 established **455 exact physical matches**: 323 confirmed blanks, 102 printed reverse links and 30 existing printed pairs corroborated. 43 exact matches retain unresolved metadata and remain drafts.

Other outcomes: **287 not confidently located, 1 physical-position discrepancy, 3 missing fronts**. This is a first pass, not an exhaustive search of every supplied photo for each profile. An unlocated profile does not establish absence or a blank. Nineteen original-artwork sheets, nineteen direct/reciprocal comparison sheets and native photo panels were inspected. Source positions and hashes are recorded per accepted match. Literal names and ratings were used for lookup; no filename-only verification or automated similarity confidence.

Notable pairings include **Marat / Petropavlovsk target ship**, **Aurora / Aurora target ship**, and naval refit/code variants such as **Norfolk RF/R**, **Formidable 2R/3R** and **Anson RF/R**. Alternate faces are recorded as Other; no reduced-strength gameplay interpretation is inferred. **Ulster (242254)** remains In progress: its mirrored cell appears to contain Speedwell, so the apparent pairing needs confirmation and the provisional blank is unreviewed. Unresolved naming/transliteration candidates and markers were left conservative.

Current totals: **4,210 Verified / 2,758 In progress / 0 Unreviewed**. The outstanding first-pass queue is now exhausted: every previously pending definition has received an attempt/triage, but many still need a closer physical match or metadata review. This does not mean all definitions are physically verified. Only these 746 entries changed; all front artwork/ratings, shared identity, unknown fields and 6,222 other definitions were preserved. No original artwork, source PDFs, catalog, map data or application/rules code changed.

Recovery: `assets\counters\recovery_snapshots\before-physical-final746-20261029-193939.zip` and `assets\counters\recovery_snapshots\before-saving-physical-final746-20261029-223631.zip`. Normal atomic writes and timestamped backups retained. Durable evidence: `counter_batches/physical_final746_20261029.json`.

Checks: **49 tests passed**, **746 temporary editor save/reload checks**, **35 additional ground save/reload checks**, **1 final-note follow-ups**, **711 reverse render checks**. Unknown-field retention, normal fixture backups and legacy shared-format loading into both faces checked. Live saved definitions were unchanged during automated tests. Interactive GUI testing remains pending. No commit/push.

Restart the editor before saving externally updated definitions, clear filters, and check:

- **Express (242174)**: confirmed generated blank with the front retained.
- **Norfolk (242092/242091)**: printed RF/R reverse pair.
- **Marat (241778)**: printed Petropavlovsk target-ship reverse, with face-specific type.
- **Ulster (242254)**: In progress, unreviewed back and physical-position warning.


## Fourth 1,000 physical-photo review - 2026-10-29

**305 newly Verified / 695 remain In progress.** Each selected original-artwork profile received a matching attempt against the supplied photo sheets. **408 exact matches**: 173 confirmed blanks, 213 printed reverse links, and 22 existing printed pairs corroborated. 103 exact matches still have unresolved metadata and remain drafts.

Other outcomes: **586 profiles not confidently located, 4 discrepancies/uncertain pairings, and 2 missing fronts**. An unlocated profile is neither proof of absence nor proof of a blank. Accepted physical evidence comes from KIC132 pp1-10 and KIC108 pp3-4, with page/row/column and source hashes in the report. Reference artwork was compared in 25 sheets; final direct/reciprocal comparisons used 18 sheets and focused native crops. Candidate identity lookup used manually read names/types/literal ratings, never filenames or search scores.

Soviet construction regiments **51-65** pair with combat-engineer brigade appearances. Tank counters include light-armour/armour alternates; Guards rocket counters include battalion/regiment and brigade alternates. Existing ground-glider brigade faces were corroborated where individually located. These pairings do not by themselves establish a reduced-strength interpretation. Headquarters with unresolved rating formats remain drafts despite physical back confirmation.

Flags: **Northern HQ (240210)** has another printed headquarters appearance requiring a unique pairing; **light armour 230TB (240043)** has a printed armour alternate without an established local counterpart; **rocket 98+ (241381)** has a 3GRD alternate without an established local match; **Guards artillery 42 (241308)** has an unusual printed brown-artillery candidate at its mirrored position, so its provisional blank is unreviewed. Saved front values/artwork are unchanged.

Current totals: **3,798 Verified / 3,167 In progress / 3 Unreviewed**. Only this frozen selection of 1,000 definitions changed. All fronts, shared identification, unknown fields and 5,968 other definitions were preserved. No source PDF, original artwork, catalog, mapping or application/rules code changed. Verified concerns counter metadata only.

Recovery: `assets\counters\recovery_snapshots\before-physical-fourth1000-20261029-185538.zip` and `assets\counters\recovery_snapshots\before-saving-physical-fourth1000-20261029-193321.zip`. Existing atomic saves and timestamped backups retained. Durable evidence for every selected ID: `counter_batches/physical_fourth1000_20261029.json`. This selection excludes all three previous physical-photo 1,000 selections.

Checks: **73 tests passed**, **1000 temporary editor save/reload checks**, **3 final-note checks**, and **956 reverse render checks**. Temporary fixtures check unknown-field preservation and backups; live definitions were unchanged during automated tests. Interactive GUI testing remains pending. No commit/push.

Restart the editor before saving externally updated definitions, then check:

- Clear filters and compare totals above.
- Construction **53 (241110)** / combat-engineer **53 (241089)**: printed 0-6 / (1)-6 pair, face-specific type/size retained.
- Light armour **4TB (239899)**: printed 2-16 / 5-4-16 pair.
- Rocket **49 (241331)** / **49+ (241351)**: printed 3-1-12 / 9-3-12 pair.
- Guards artillery **42 (241308)**: In progress, unreviewed back and pairing warning.


## Third 1,000 physical-photo review - 2026-10-29

**235 newly Verified / 765 remain In progress.** All 1,000 selected entries received a matching attempt. **291 exact matches**: 189 confirmed blanks, 84 printed reverse links and 18 existing pairs corroborated. 56 exact matches still have unresolved metadata and remain drafts.

Other outcomes: **682 profiles not confidently located, 13 discrepancies/uncertain variants, 13 missing fronts**, and construction 34's previously confirmed blank retained with its size discrepancy. Unlocated does not mean absent or blank. Exact matches use KIC120 pp3-8, KIC132 pp1-10 and KIC108 pp1-10; individual positions/source hashes are recorded. Automated candidate scores were unreliable and were not used as confidence measurements.

Romanian security brigades **1 (238705)** and **3 (238706)** print 3-6 / 4-6 versus stored 2-6. Soviet siege brigade **109/16AD (239488)** physically prints 6-5-12 versus local 4-5-12; its **281 (239471)** counterpart also remains draft. Suceava Battalion/Regiment variants, Slovak Rapid and Romanian NSP/RSP reverse questions remain flagged. Original front values/artwork were preserved. Final QA rejected mismatched armour and 305/505 locators and the provisional Timisoara/Suceava link.

Current totals: **3,493 Verified / 3,472 In progress / 3 Unreviewed**. Only the selected 1,000 definitions changed; all fronts, shared identification, unknown fields and 5,968 other entries were preserved. No original artwork, PDFs, catalog, maps or application/rules code changed. Verified concerns metadata only.

Recovery: `assets\counters\recovery_snapshots\before-physical-third1000-20261029-014511.zip` and `assets\counters\recovery_snapshots\before-saving-physical-third1000-20261029-185302.zip`. Existing atomic save and timestamped backup behavior retained. Durable evidence: `counter_batches/physical_third1000_20261029.json`. This supersedes the pending checkpoint; its provisional decisions must not be applied again.

Checks: **73 tests passed**, **1000 temporary editor save/reload checks**, **11 final-note follow-ups**, **974 reverse render checks**. Fixtures check unknown-field preservation and backups; live definitions were unchanged during testing. Interactive GUI testing remains pending. No commit/push.

Restart the editor before saving externally updated definitions, then check:

- Clear filters and compare totals above.
- Romanian artillery **7 C (238665)**: confirmed generated blank; front 1-6 retained.
- Italian infantry **63 (238342/238343)**: printed (1)-6 / 1-6 pair, no reduced-strength assumption.
- Soviet artillery **123 (239052/239196)**: printed 5-6 / 5-12 pair.
- Romanian security **1 (238705)** and Soviet **109/16AD (239488)**: In progress with discrepancy notes; fronts unchanged.

## Next 1,000 physical-photo review - 2026-10-28

**472 newly Verified / 528 remain In progress.** All 1,000 selected entries received a matching attempt. **595 exact physical matches**: 423 confirmed blanks, 125 printed reverse links and 47 existing printed pairs corroborated. Of these, 123 still have unresolved metadata and remain drafts.

The remaining outcomes are **364 profiles not confidently located, 28 candidate discrepancies, 12 missing-front records and one ambiguous HOFC inverse**. Unlocated does not mean physically absent or blank. The 199 pp1-12, 120 pp1-4 and 185 pp7-8 photos supplied the exact matches; source hashes and individual mirrored positions are recorded. Similar-looking cells rejected during final QA were not accepted as physical proof.

Training brigade **382 (237246)** has a printed infantry 620, 1-2-6 reverse, with no exact local reverse asset established. Its provisional blank is now unreviewed. Artillery **2A (238036/238041)** has an apparent physical/local movement discrepancy, retained as a draft. **HOFC (238146)** has different physical reverse variants (Army HQ 2 / HOGW), so its back remains unreviewed. RFFSS 2 infantry/security, Seydlitz/Weser and the four OKW parachute/commando alternates use existing artwork; no reduced-strength interpretation was inferred.

Current overall totals: **3,258 Verified / 3,707 In progress / 3 Unreviewed**. Only these 1,000 definitions changed; all fronts, shared identification, unknown fields and 5,968 other entries were preserved. Original artwork/PDFs, imported catalog, application/rules code and mapping data were untouched. Verified concerns metadata only.

Recovery: `assets\counters\recovery_snapshots\before-physical-next1000-20261027-193823.zip` plus `assets\counters\recovery_snapshots\before-saving-physical-next1000-20261028-120329.zip`. Atomic save and normal timestamped backup behavior retained. Evidence for every selected ID: `counter_batches/physical_next1000_20261028.json`.

Checks: all **73 tests passed**; **1000 temporary editor save/reload checks**, **16 final-note follow-up checks**, and **963 assigned reverse render checks**. Temporary fixtures preserve future fields and backups; live data were unchanged throughout testing. Descriptor lists may reorder in the editor; the fixture comparison treats them as unordered, while this pass preserves their actual saved order. Interactive GUI checks remain pending. No commit/push.

Restart the editor before saving externally updated definitions, then check:

- Clear filters and compare the totals above.
- Construction 10 Fort (237008): confirmed generated blank, front 0-6 retained.
- Seydlitz (237615): printed Weser reverse; check both images and face-specific values.
- Training 382 (237246): In progress, unreviewed back, printed-reverse warning.
- HOFC (238146): In progress, unreviewed back, both observed variants noted.

## Physical first-1,000 review pass completed — 2026-10-27

Remaining 621 matching attempts finished: 348 exact matches, 312 newly Verified,
309 remain In progress (36 exact with metadata questions, 12 discrepancies,
2 reused-Arko ambiguities, 256 unlocated profiles, 3 missing fronts). Total: 2,786
Verified / 4,179 In progress / 3 Unreviewed; selected first 1,000 now 564 / 436.
Unlocated does not mean absent or blank. Evidence/statuses for all 1,000 are in
counter_batches/physical_1000_20261027.json. No entries still labelled awaiting
an attempt; many exact physical matches remain unresolved. Verified is metadata
only, never gameplay validation. Literal parentheses/R retained; future rules
interpretation alone does not block a visually confirmed metadata transcription.
Corrected a previous false blank: artillery 736 (`235816`) actually reverses to
Arko 107, 6-5-18 (PDF199 pp3/4, r1 c13/c8), linked and returned In progress for review.
Arko 102 has 422/616 variants; Arko 124 has 607/735 variants. Keep inverse records
draft, preserve forward exact pairings and stable IDs. Artillery 637 / Arko 18
physical 6-3-18 versus local 6-5-18, Arko 117 missing local reverse, saved 852 vs
printed II/52, repeated 426 / II/54 reverse artwork questions remain flagged.
Original PDFs are read-only, artwork unchanged; no app/rule/map edits here.
All 73 tests, 622 temporary editor save/reloads, 611 reverse renders passed; manual
GUI checks pending. Archive before pass: before-remaining-621-20261027-131600.zip;
additional immediately-before-save archive in recovery_snapshots. Normal atomic
saves/backups retained. All 622 changed records preserve fronts and identity;
6,346 other definitions unchanged. Temporary scripts are one-shot—do not rerun
applied saves. Next prioritize flagged metadata/physical variants or another
explicit selection; do not imply every counter is physically verified.

## Physical counter photos - 2026-10-27

User supplied five Downloads/KIC Document PDFs (199,185,132,120,108), 52 pages/26
front-back pairs; LW sheets absent. All pages surveyed at sheet level, but precise
counter matching remains incomplete. First 73 matches on 199 pp1-2 confirm 52
blank reverses and repair 21 printed backs using already-local images. Nine
construction/railway definitions newly Verified; totals 2,222 Verified / 4,743
In progress / 3 Unreviewed. HQs stay In progress for unresolved rating formats;
construction 34 physical X versus stored Regiment/III is flagged, front unchanged.
Photo proof permits promotion of genuinely confirmed blanks, superseding the
earlier instruction to keep all unconfirmed single-image defaults In progress.
Do not extend that permission to unphotographed or unmatched units.
Alternate HQ backs change names/types; do not assume Reduced or merge stable IDs.
Reverse printed_designation is retained as face metadata and notes; shared editor
designation remains the front identity. Counter-level matching on the other 25
pairs and remaining first-pair positions is pending. See PHYSICAL_COUNTER_REVIEW.md
for exact source hashes/positions, backup, limitations and manual checks. Source
PDFs remain in Downloads. No source artwork, PDFs, catalog, map data or code changed.

## Svalbard-wide metadata review - 2026-10-27

User requested the entirety of Svalbard as a scaling test and confirmed interactive
navigation/overlays already work. Inspected 17 sheets/257 candidates from original
Map 2: 199 additional substantive reviews, 121 Verified (.98) / 78 In progress
(.94); prior island/manual records preserved. Included Spitsbergen, Nordaustlandet,
Prins Karls Forland, Wilhelmoya, northern/eastern islets, Kvitoya and Hopen. Added
four printed Points of Interest, three Small Ports and eight Track segments.
Terrain and transport statuses remain independent. Zone assignments/ancillary
interpretations remain Unknown; small/threshold-obscured land remains drafts.
Prior manual Water HP-YF:3103 has a possible coastal vertex flagged externally,
without overwriting its saved values. Saved terrain records 5,754; transport
segments 49 (original 41 preserved). Backup mapping_backups/before-svalbard-20261027-073512.zip.
All 73 tests pass, plus temporary full terrain/transport roundtrips and 199 editor
checks. No application/gameplay changes. Evidence/draft reasons: MAP_REVIEW_STATUS.md,
map_batches/SVALBARD_REVIEW.md and map_batches/svalbard_20261027.json.

## Whole-island test - Barentsoya, 2026-10-27

Interpreted the requested island near Edgeoya as Barentsoya directly north.
Inspected all eight land-containing hexes: five Verified (.97-.98), three coastal
drafts In progress (.90), all eight transport Verified with no printed transport.
Uses the same >20% whole-hex land convention and amber/green statuses. Recorded
confident feature absences; weather/sea-zone and ancillary interpretations remain
Unknown. Preserved prior values, merging two edge-only records from Edgeoya;
mirrored shared edges without promoting neighbors. Total saved records 5,496.
Exact prior backup mapping_backups/before-barentsoya-20261027-072836.zip; evidence
map_batches/barentsoya_20261027.json. No application-code/gameplay/source changes.
See MAP_REVIEW_STATUS.md for complete hex list, tests, remaining unknowns and recovery.

## Project mapping convention - 2026-10-27

User approved ignoring tiny incidental terrain spillover unless a combined type
is clearly intended. Include a land terrain type when it covers more than 20%
of the hex area. This is a project interpretation, not a published TSWW rule;
do not confuse it with the rulebook's one-quarter Limited Land Mass stacking
criterion. Keep the three accepted Bear Island classifications unchanged.
Hexside features such as High Mountain belong to both bordering hexes on their
corresponding sides, not as a filled terrain type. Verify only above .95 review
confidence; uncertain entries are In progress. Preserve existing manual data.
Terrain In progress must display amber/yellow, and Verified green. Legacy
Suggested entries remain supported without converting their statuses on load.

Edgeoya continuation completed 21 land-containing hexes: 12 terrain Verified / 9
In progress, all 21 transport Verified (no printed transport). Borderline area
thresholds and tiny coastal slivers remain drafts, with Unknown land terrain when
no type clearly exceeds 20%. Preserved the three Bear Island entries and all prior
property values/statuses. Shared-edge absence additions bring saved records to
5,482. Exact backup mapping_backups/before-edgeoya-20261027-072231.zip; evidence
map_batches/edgeoya_20261027.json and per-record map_review. General terrain now
supports In progress in loader/selector with amber overlay; legacy Suggested
remains amber. No gameplay changes. See MAP_REVIEW_STATUS.md for tests/manual checks.

## Map metadata pilot - 2026-10-27

User authorized a small island review, >95% confidence verification and a prior
saved-data backup. Reviewed Bear Island on Map 2 against original artwork and
UICFB PDF p4: HP-ZF:1912 Clear, 1911 Hills, 2012 Mountain; all Mixed land/water,
general/transport Verified at review confidence .98. Printed feature absences
were recorded, with shared-edge absences mirrored to nine neighboring records
without promoting their statuses. All pre-existing values and unknown fields
were preserved. Weather/sea zone assignment and ancillary hexside interpretations
remain Unknown. No gameplay or application-code changes. See MAP_REVIEW_STATUS.md
and map_batches/bear_island_20261027.json for scope, exact backup, tests and manual
checks. Restart an open app before saving after external map edits.

## Latest counter metadata review — remaining queue, 2026-10-25

Assessed all remaining 2,637 queue entries: 7 aircraft-factory markers Verified / 2,630 In progress. Current totals 2,213 Verified / 4,752 In progress / 3 Unreviewed. Transcribed available artwork for 2,604 entries; 33 unresolved-artwork records remain untranscribed with explicit blocker notes. All 2,512 newly inspected single-image entries retain generated blank defaults and In progress, per user instruction. Existing reviewed/manual records and three Unreviewed entries were preserved. This completes the available-artwork queue pass, not all-counter verification.

Recovered 85 entries' comma-separated original VASSAL image references against existing artwork without changing imported catalog/assets. These have a provisional front, unreviewed back and full `appearance_candidates` with original names, paths and literal printed values. They need catalog-link/appearance-assignment repair; several are multi-role, shipping-capacity, factory or partisan states rather than reduced-strength pairs. Do not discard extra appearances or auto-verify. Unknown fields survive current editor saves, although the editor has no candidate-appearance controls.

Naval type names were checked against production rules 1.6a 5.C.2 printed p31 / PDF p33: CVS Seaplane Depot Ship, TS Target Ship, DAV Destroyer Floatplane Tender, AMCA Auxiliary Anti-Aircraft Cruiser, etc. Preserve printed codes separately. UICFB pp1-3 remains the symbol/colour reference. CD levels, HQ movement-only formats, parenthesized ground ratings, special symbols and unconfirmed reverses remain drafts. No gameplay rules or application-code changes. All 71 tests passed, plus temporary loading of all 2,637 records, 81 representative save/reloads and 2,512 blank-render checks. All 4,331 non-target records, unknown fields and saved mapping/transport/catalog data were preserved. Evidence, exact recovery paths, exceptions and manual tests are at the top of COUNTER_REVIEW_STATUS.md and in counter_batches/remaining_2637_20261025.json.

## Previous counter metadata review — batch 1000c, 2026-10-25

Transcribed another 1,000 queue records: 156 naval pairs, three aircraft pairs outside the Air palette and 841 single-image ground fronts. Result: 86 assistant-Verified / 914 In progress; totals 2,206 Verified / 4,759 In progress / 3 Unreviewed; 2,637 untranscribed placeholders remain. All single-image records must retain In progress with user-approved generated blank reverses, not physically confirmed backs. See the top of COUNTER_REVIEW_STATUS.md for recovery, questions and manual checks; evidence is counter_batches/mixed_1000c_20261025.json.

36 SSF drafts store patrol_range and printed_bottom_right separately, leaving tactical_speed unknown (production rules 1.6a 5.C.2.e.ii). 37 FAS drafts retain printed_bottom_right without assigning tactical speed (5.C.4 excludes FAS; reconcile 14.J). These unknown fields survive editor saves but have no dedicated controls. Light-AA symbol ratings may differ from ground strength and are stored independently. Stars/hashes/parentheses remain literal. No gameplay implementation or application-code changes in this batch. All 71 tests passed; temporary editor/persistence checks preserve metadata, statuses and unknown fields. All 5,968 non-target records and saved mapping/transport/catalog data were preserved.

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


## Renewed counter automation authorization (2026-10-25)

User now explicitly requests counter automation and permits assistant verification of confidently checked entries; uncertainties should remain In progress with reasons. This supersedes the earlier prohibition on reintroducing automation. Maps are outside this task. All existing definitions remain protected.

Added counters.batch_review: CLI defaults to dry-run, --apply uses real editor completeness checks, per-aspect visual-review evidence, SHA-256 artwork fingerprints and explicit uncertainty reasons. It is a reviewed-proposal validation/status/save workflow, not unattended OCR or filename-derived extraction. Existing IDs are skipped, including unfinished manual records. Incomplete review evidence or unresolved issues produce In progress; changed artwork or concurrent definition changes abort. Provenance is stored as batch_review; existing atomic save/backups are reused.

First pilot added 24 visually inspected German infantry divisions (236439-236462) as assistant-Verified. Both printed faces, designation, infantry symbol and XX/Reduced text were checked; some entries use differing front/back rating formats. Review proposals/evidence are in counter_batches/german_infantry_01.json. All 439 prior definitions and metadata were compared unchanged and an exact backup verified. All 68 tests passed, including seven new temporary-fixture batch policy/persistence tests. Other ground/naval counters and existing aircraft drafts remain unprocessed; no blanket verification occurred. Restart an open editor after external batch additions. No commit/push authorized for this task.


## Full counter triage and recovery snapshot (2026-10-25)

User requested all possible counter metadata verification, strictly greater than 95% confidence for Verified and In progress otherwise, plus a restorable pre-pass copy. Saved/byte-verified six JSON files in assets/counters/recovery_snapshots/before-full-counter-review-20261025-060256.zip with SHA-256 manifest. Existing artwork/PDFs were untouched.

Direct visual inspection of 368 additional German infantry division pairs produced 367 assistant-Verified definitions and one In progress 78 Sturm entry (236831, extra printed 1 inside front symbol unresolved). Independent per-face rating formats were transcribed. Added the other 6,137 undefined catalog IDs as explicitly UNTRANSCRIBED review-queue entries, In progress with Unknowns and source_images references; these are not completed definitions or claims of visual inspection. All prior 463 entries and metadata were compared unchanged. Total saved status: 629 Verified / 6,336 In progress / 3 Unreviewed, across 6,968 records. Do not mistake record coverage for transcription completion. Existing aircraft drafts remain untouched.

Batch policy now requires numerical identity/front/back confidence strictly above 0.95 (assistant judgment, not a statistical guarantee); missing, exactly-0.95, invalid and unresolved evidence stays In progress. Added threshold regression coverage; all 69 tests passed. Local OCR and exact raster matching experiments were unreliable and were NOT used to verify entries; the matcher experiment was removed. Proposals/evidence: counter_batches/full_catalog_20261025.json. Scope/recovery/manual checks: COUNTER_REVIEW_STATUS.md. Restart any open editor before saving after batch additions. No commit/push performed. Continue actual visual transcription of the unsupported queue rather than presenting the inventory pass as finished metadata work.


## Next 500 actual transcriptions completed (2026-10-25)

User requested another 500 real artwork reviews under the >95% confidence policy. Directly inspected both faces of Soviet infantry entries 240307-240806 (500 entries), replacing only their untranscribed inventory placeholders. Transcribed ratings independently, retained named/ethnic/place/m suffixes literally, used Soviet Union / Red Army identity and XX division / Reduced face labels from artwork. 495 became assistant-Verified. Five stay In progress for an additional printed 1 inside the front symbol: 240652 (395), 240719 (99), 240725 (112), 240781 (14), 240788 (52). Their main ratings are filled, not placeholders.

New recovery snapshot assets/counters/recovery_snapshots/before-review-500-20261025-062350.zip contains six saved JSON files and a checked SHA-256 manifest. All 6,468 other records, top-level metadata and unknown target fields were compared unchanged; exact immediate pre-save backup verified. Total status now 1,124 Verified / 5,841 In progress / 3 Unreviewed. Untranscribed queue is 5,637. Current scope/exceptions and recovery details are at the top of COUNTER_REVIEW_STATUS.md.

Added narrowly scoped queue-promotion support to batch_review: optional replace_placeholder_sha256 must match the current record, and record must still be an untranscribed queue placeholder with Unknown identity, no assigned images, no ratings/face data and In progress status. Changed/manual/Verified records are rejected; unknown fields and user note lines are preserved. Ordinary batches continue to skip existing IDs. Queue-promotion batches are single-use: reapplying after transcription safely refuses rather than overwriting completed work. Proposals/evidence: counter_batches/soviet_infantry_500_20261025.json. All 71 tests passed, including two new queue protection checks; all 500 opened with temporary editor fixtures and seven representative temporary save/reloads passed. Restart an open editor before saving. No commit/push performed.


## Next 1,000 actual transcriptions completed (2026-10-25)

User requested another 1,000 counters under the same >95% confidence policy. Directly inspected both original appearances of 1,000 untouched two-image ground queue records across seven nations: 267 German (including LW/SS), 483 Soviet, 108 Hungarian, 104 Romanian, 17 Italian, 16 Finnish and five Slovak. 914 became assistant-Verified; 86 remain In progress: 29 level-only CD appearances with unresolved short/long applicability, 20 OP/mobile pairs, 30 Para-Rifle versus UIC Glider classification questions, five Heavy armour descriptor questions, Dovator's vertical descriptor and Warschau's parenthesized reduced rating. All 1,000 have actual visual transcription, not placeholder triage. UICFB pp1-3 was visually checked; p2 identifies the small number inside/beside the icon as AA. Earlier special-marking drafts remain untouched. Different per-face formats, equivalent-size brackets, literal names, AA and descriptors are retained; OP/CD appearances are not labeled Reduced.

Recovery archive: assets/counters/recovery_snapshots/before-review-1000-20261025-063935.zip, six saved JSON files with checked manifest/integrity. All 5,968 non-target definitions, unknown target fields, top-level metadata, mapping/transport data, catalog and source assets were preserved; exact pre-save backup verified. Current totals: 2,038 Verified / 4,927 In progress / 3 Unreviewed, with 4,637 untranscribed queue placeholders remaining. Evidence: counter_batches/ground_1000_20261025.json; exact questions/manual checklist: top of COUNTER_REVIEW_STATUS.md.

All 71 tests passed. All 1,000 entries opened in temporary editor fixtures without file/status mutation; 28 representative temporary save/reloads preserved all proposal values and unknown fields. No application code, gameplay rules or themes changed; no commit/push. Restart an open editor before saving after these external data changes. Continue actual artwork transcription of the queue; do not describe all catalog metadata as finished.


## Following 1,000 entries transcribed (batch 1000b, 2026-10-25)

Inspected both appearances of 191 remaining two-image ground queue entries and the one available original image of 809 single-image entries. User explicitly chose generated blank reverses by default for single-image ground counters and explicitly required keeping them In progress. Preserve this preference for subsequent batches: a generated blank is a project default, not a confirmed physical reverse, and does not justify automatic verification. All 809 use their actual front, sampled background colour and existing front-dimension renderer, and remain In progress with that note.

82 two-image entries became assistant-Verified (>95% confidence); 109 other two-image entries remain In progress: 53 OP/mobile supply/engineer pairs, 50 fortified-region level pairs requiring a dedicated format, two commanders with unresolved modifier fields, two railway-artillery/CD alternate pairs, one Spanish ground-contingent nationality question and one parenthesized security rating. Across all 1,000, 59 parenthesized combat values are literal pending defense-only format clarification. A catalog/artwork mismatch on 239787 (imported 149TB, printed 194TB) is explicitly noted; it and 239788 have a flamethrower symbol under Arm Trng labels. 239620's small 1bTB suffix needs a physical check. All are drafts. Do not silently correct artwork or catalog names, strip parentheses, label OP/CD/UR alternates Reduced, or infer unprinted values.

Totals: 2,120 Verified / 4,845 In progress / 3 Unreviewed. Untranscribed queue: 3,637. Recovery archive: assets/counters/recovery_snapshots/before-review-1000b-20261025-072126.zip (six saved JSON files and checked manifest). All 5,968 other records, unknown target fields and top-level metadata preserved; mapping/transport data, catalog and source artwork/PDFs unchanged, exact pre-save backup verified. Evidence: counter_batches/ground_1000b_20261025.json; review list and manual tests at top of COUNTER_REVIEW_STATUS.md.

All 71 tests passed. All 1,000 opened in temporary editor fixtures without file/status mutation; 39 representative temporary save/reloads preserved values and unknown fields; all 809 generated blanks rendered with original front dimensions/stored colours and remained In progress. No app code/gameplay/theme changes; no commit/push. Restart any open editor before saving externally updated definitions. Full catalog metadata remains unfinished.
