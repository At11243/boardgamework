# Counter metadata review status

## Physical counter-sheet verification pass: 265 newly Verified — 2026-10-30

Verified **265 in-progress counter definitions** against native physical counter-sheet scans at a strict >95% confidence standard; totals **5,708 Verified / 1,260 In progress / 0 Unreviewed** (out of 6,968 total definitions).

This batch covers **187 Soviet profiles** (Artillery regiments, Mortar battalions, Anti-Tank regiments, Light Armour battalions, and static fortification units on KIC Document 132.pdf and KIC Document 108.pdf), **69 German Army profiles** (Security brigades/regiments, Construction Engineer battalions, Artillery, Flak, and HQs on KIC Document 199.pdf and KIC Document 108.pdf), **3 Hungarian profiles**, **3 United Kingdom profiles**, **1 Romanian profile**, **1 Finnish profile**, and **1 United States profile**. Each promoted counter had its front identity, unit type, formation size, and printed ratings checked against the scanned counter-sheet cell, confirmed zero issues in unit_editor.definition_issues(), and had its mirrored physical reverse verified (solid blank cardboard texture/color _std < 26.5 with median brown cardboard on Soviet sheets or _std < 5.5 on German/Finnish/UK white paper sheets).

All stable 	ype_id identifiers, original artwork assignments, unknown fields, and existing manual notes were strictly preserved. Automated save/reload checks on isolated temporary fixtures verified persistence, future-field preservation, and backup creation without touching live definitions during tests. Pre-save recovery snapshot archived to ssets/counters/recovery_snapshots/before-physical-fifth-265-20261030.zip plus standard atomic timestamped backup. All 77 unit tests pass. Full batch audit: counter_batches/physical_fifth_265_20261030.json.

## Physical counter-sheet verification pass: 200 newly Verified — 2026-10-30

Verified **200 in-progress counter definitions** against native physical counter-sheet scans at a strict >95% confidence standard; totals **5,443 Verified / 1,525 In progress / 0 Unreviewed** (out of 6,968 total definitions). 

This batch covers **110 German Army profiles** (Security, Construction Engineers, Artillery, Flak, and HQs on KIC Document 199.pdf and KIC Document 108.pdf) and **90 Soviet profiles** (Artillery regiments, Mortar battalions, Anti-Tank, Light Armour, and static units on KIC Document 132.pdf and KIC Document 108.pdf). Each promoted counter had its front identity, unit type, formation size, and printed ratings checked against the scanned counter-sheet cell, confirmed zero issues in unit_editor.definition_issues(), and had its mirrored physical reverse verified (199 confirmed blank backs with uniform cardboard texture/color, 1 printed reverse confirmed).

All stable 	ype_id identifiers, original artwork assignments, unknown fields, and existing manual notes were strictly preserved. Automated save/reload checks on isolated temporary fixtures verified persistence, future-field preservation, and backup creation without touching live definitions during tests. Pre-save recovery snapshot archived to ssets/counters/recovery_snapshots/before-physical-fourth-200-20261030.zip plus standard atomic timestamped backup. All 77 unit tests pass. Full batch audit: counter_batches/physical_fourth_200_20261030.json.

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

## Completed first-1,000 photo review pass — 2026-10-27

The remaining **621** have each received a matching attempt. **312 newly Verified;
309 remain In progress.** There are **348 exact physical matches**: 155 confirmed
blank reverses, 166 printed reverse links, and 27 existing printed pairs confirmed.
Of those exact matches, 36 remain drafts for unresolved metadata/format questions.
The rest comprise 12 physical candidate discrepancies, two reused-Arko pairing
ambiguities, 256 exact profiles not confidently located, and three missing-front
artwork records. An unlocated profile is not proof of absence or a blank reverse.

One prior error was corrected: artillery **736 (`235816`)** has printed **Arko 107
6-5-18**, not a blank reverse (PDF199 pp3/4, r1 c13/c8). It was returned from
Verified to In progress and explicitly flagged. No existing front ratings or
identification fields were changed in this pass.

Current totals: **2,786 Verified / 4,179 In progress / 3 Unreviewed**. Within the
frozen first 1,000 selection, **564 Verified / 436 In progress**. This completes
the review pass, while exact matching and metadata resolution remain open for
the flagged entries. See `counter_batches/physical_1000_20261027.json` for every ID.

Recovery archives: `assets/counters/recovery_snapshots/before-saving-physical-621-20261027-193354.zip` and the
start-of-pass archive `assets/counters/recovery_snapshots/before-remaining-621-20261027-131600.zip`.
The earlier whole-follow-up archive and normal timestamped backups remain available.
All **73 tests passed**, plus **622 temporary editor save/reload checks** and
**611 assigned reverse rendering checks**. Unknown fields and all 6,346 other
definitions were preserved. Original artwork, PDFs, application code and mapping
data were untouched. Interactive checks remain unperformed; no commit or push.

Restart the editor before saving externally updated definitions, then check:

- Clear filters and check the totals above.
- Artillery 736: printed Arko 107 reverse, status Other, correction note, In progress.
- Artillery 422: printed Arko 102 reverse; Arko 102 itself remains In progress because copies also reverse to artillery 616.
- Engineer 754: confirmed generated blank reverse; front 0-6 preserved.
- Artillery 637 / Arko 18: rating-version discrepancy noted; In progress.

## Historical initial physical photo pass - 2026-10-27

Totals at that checkpoint: **2,222 Verified / 4,743 In progress / 3 Unreviewed**. Surveyed all
52 pages of five supplied photo PDFs at sheet level; individual matching is
incomplete. Matched 73 German Army counters on KIC Document 199.pdf pp1-2:
52 physical blanks confirmed and 21 printed reverse links repaired using existing
local images, with nine construction/railway entries newly Verified. Most HQs
remain In progress for unresolved editor rating formats. Construction 34 has a
physical X versus stored Regiment/III discrepancy; front data were preserved.
No unmatched counter was promoted. See PHYSICAL_COUNTER_REVIEW.md for source
inventory, exact backup, all matched IDs/positions, outstanding work and checks.
Evidence: counter_batches/physical_backs_20261027.json and physical_back_review
metadata. Earlier counts below describe historical batches.

## Latest completed pass: the remaining 2,637 queue entries

**7 assistant-Verified / 2,630 In progress.** Inspected the remaining available original artwork: 1,833 Ground-palette entries, 642 Naval-palette entries, 44 entries outside those palettes, plus all recovered appearances of 85 initially unlinked records. **2,604 entries now have artwork transcription; 33 remain untranscribed because no direct local artwork could be located.** Inspection covered 71 regular contact sheets and 15 recovered-appearance sheets. This completes the available-artwork pass over the queue, not verification of every counter.

Current totals: **2,213 Verified / 4,752 In progress / 3 Unreviewed**, across 6,968 records. The seven new Verified entries are **aircraft-factory markers**, whose two images clearly show full versus Half Capacity. They are not aircraft units. No numeric production capacity or economic rule was inferred.

### Why most entries remain In progress

- **2,512 single-image entries:** available fronts transcribed, generated blank reverses stored with sampled colour and original front dimensions, and explicitly kept In progress under the user's existing instruction. Unprinted values remain unknown; zero and printed punctuation are retained.
- **85 recovered records:** comma-separated VASSAL appearance references resolve to existing files under assets/counters/images despite empty catalog image lists. These include four commando records, 16 industrial records, 38 partisan records and 27 naval/shipping records. The first inspected appearance is assigned as a provisional front; every candidate's original name, path and literal printed values is retained in `appearance_candidates` and the notes. Back assignment remains unreviewed. No catalog, artwork or imported assets were rewritten. A focused catalog-link/appearance-assignment repair remains necessary; some records have up to ten appearances and must not be forced into conventional full/reduced pairs.
- **33 unresolved-artwork records:** explicitly assessed as blocked, with unknown identity/ratings preserved. Their notes retain REVIEW QUEUE ONLY and their visual checks remain false. Generic, dummy and prototype-dependent entries may require source-module trait resolution, rather than a missing physical counter.

The remaining ground fronts include HQs, engineers, armour, AA/AT, security, airborne/glider, railway, siege, training and coastal-defense counters. Movement-only HQ values use an Unknown ground format with the literal bottom value retained; no combat strength was invented. CD levels, including slash-separated text, remain literal pending short/long interpretation. Railway R remains text. Imported Heavy labels without a visible heavy bar need manual interpretation; the descriptor was not inferred solely from the imported label. The single image for `GE Sec X 202 back` explicitly prints Reduced, so its available front assignment has Reduced status; IDs were not merged. Special ethnic/foreign-contingent identities and composite symbols remain reviewable drafts.

Naval ship codes, gunnery, protection, AA, torpedo, bottom-right values and capacity/codes were read independently. Final type-label cross-check uses production rules 1.6a **5.C.2, printed p31 / PDF p33**: for example CVS = Seaplane Depot Ship, TS = Target Ship, DAV = Destroyer Floatplane Tender, AMCA = Auxiliary Anti-Aircraft Cruiser. SS/SSF patrol range and unresolved FAS numbers remain separate from tactical speed; no conditional speed was copied into a general rating. Stars and hashes remain printed marks. Sources for symbols, sizes and colours: **UICFB PDF pp1-3**; naval layout/type references **5.C, printed pp31-33 / PDF pp33-35**. No gameplay rules were implemented.

Evidence: `counter_batches/remaining_2637_20261025.json`, saved notes, `batch_review` and recovered `appearance_candidates`. Confidence is assistant review judgment, not a statistical guarantee. The three existing Unreviewed records and all earlier reviewed/manual records were preserved.

### Recovery and checks

Recovery archive: `assets/counters/recovery_snapshots/before-review-remaining-20261025-221507.zip`. Exact backup before this entire pass: `assets/counters/unit_definition_backups/unit-definitions-20261025-223923-987417.json`. A second normal backup, `unit-definitions-20261025-224123-151971.json`, precedes the final naval type-label correction. Use the archive or the first backup to restore the state before this pass.

All **71 automated tests passed**. All **2,637 entries** loaded in temporary editor data without changing statuses or file bytes; **81 representative save/reloads** checked saved values, unknown fields, recovered appearances and document metadata. All **2,512 blank reverses** rendered at front dimensions and stored colours. All **4,331 non-target definitions**, unknown target fields, document metadata, catalog, saved mapping/transport JSON and inspected artwork hashes were preserved/checked. Saves were atomic with exact-byte backups. No application code changed; no commit or push. Interactive review and physical reverses remain untested.

### Short manual checklist

1. Close and reopen the editor before saving; clear filters and expect 2,213 Verified. The seven new Verified records are Factory markers, not Ground/Air units.
2. Inspect `SU Factory Aircraft Ilyushin`: normal factory front, Half Capacity alternate; neither is a reduced-strength aircraft counter.
3. Inspect `RO Mot Lt AA III 3A`: ground 2-16 and separate AA 1; generated blank reverse; In progress after save/reopen.
4. Inspect `GE Sec X 202 back`: front explicitly Reduced, 1-6, generated blank reverse, In progress. Inspect `GE OKW Para Cdo II 801`: provisional motorized/amphibious front (1)-20, recovered alternative values in notes, unreviewed back.
5. Inspect a CVS or TS draft for corrected naval type wording and an oil marker for literal Cat values without inferred nationality.

### Unresolved artwork: 33 records

These were searched by direct original-image references, comma-separated alternatives, the importer filename hashes and case-insensitive exact names in the image index. No matching local artwork was located; ratings were not guessed. Some may depend on unresolved VASSAL prototypes.

| ID suffix | Imported name |
| --- | --- |
| 238011 | HU Positional AA Lt |
| 238428 | RO Positional AA |
| 238770 | SL Positional AA |
| 237380 | LW Positional AA |
| 237319 | LW Positional AA |
| 237808 | FI Positional AA |
| 237782 | BU NSS |
| 237781 | BU Seat of Governent |
| 237876 | FI NSS |
| 237875 | FI Seat of Governent |
| 238137 | HU NSS |
| 238136 | HU Seat of Governent |
| 238331 | IT NSS |
| 238558 | RO NSS |
| 238557 | RO Seat of Governent |
| 238781 | SL NSS |
| 238780 | SL Seat of Governent |
| 239004 | SU PVO Positional AA |
| 235652 | GE Mot Lt AA II 28.FB |
| 238941 | SU PVO Positional AA |
| 238354 | IT Mtn Ski II MC.FB |
| 238666 | RO Mtn Ski III Rotta.FB |
| 237985 | FI SSF Dummy |
| 241772 | VMF Positional AA |
| 239289 | SU SMot Hvy Art III 56.FB |
| 238763 | RO SSF Dummy |
| 237758 | KM SSF Dummy |
| 242391 | RN SSF Dummy |
| 242001 | VMF SSF Dummy |
| 236393 | GE NSS |
| 236392 | GE Seat of Governent |
| 240301 | SU NSS |
| 240300 | SU Seat of Governent |

### Recovered appearances requiring catalog/face review: 85 records

Candidate artwork is already local. The imported catalog remains unchanged. A provisional front allows inspection; stored alternate appearances must be reviewed before assigning a physical reverse.

| ID suffix | Imported name | Appearances |
| --- | --- | --- |
| 237096 | GE OKW Para Cdo II 801.FB | 4 |
| 237097 | GE OKW Para Cdo II 802.FB | 4 |
| 237098 | GE OKW Para Cdo II 803.FB | 4 |
| 237099 | GE OKW Para Cdo II 804.FB | 4 |
| 242009 | SU Factory Armour Chelyabinsk | 2 |
| 242010 | SU Factory Armour Gorky | 2 |
| 242011 | SU Factory Armour Kharkov | 4 |
| 242012 | SU Factory Armour Leningrad | 10 |
| 242013 | SU Factory Armour Nizhny Tagil | 2 |
| 242014 | SU Factory Armour Stalingrad | 2 |
| 242015 | SU Factory Armour Sverdlovsk | 2 |
| 242016 | SU Factory Artillery Izhevsk | 2 |
| 242017 | SU Factory Artillery Kovrov | 2 |
| 242018 | SU Factory Artillery Leningrad | 6 |
| 242019 | SU Factory Artillery Molotov | 2 |
| 242020 | SU Factory Artillery Nizhny Tagil | 2 |
| 242021 | SU Factory Artillery Podlipki | 2 |
| 242022 | SU Factory Artillery Sverdlovsk | 2 |
| 242023 | SU Factory Artillery Tula | 2 |
| 242024 | SU Factory Artillery Zlatoust | 2 |
| 237766 | GE LC.FB | 2 |
| 237767 | GE RF Nord.FB | 2 |
| 237728 | KM Fast NSP D.FB | 2 |
| 237727 | KM Fast NSP.FB | 2 |
| 237724 | KM LC.FB | 2 |
| 237725 | KM NSP.FB | 4 |
| 237765 | LW LC.FB | 2 |
| 242468 | RN-USN NSP.FB | 2 |
| 242465 | USN NSP.FB | 2 |
| 242467 | USN-SU NSP.FB | 2 |
| 242377 | RN Fast NSP.FB | 2 |
| 242380 | RN LC.FB | 2 |
| 242375 | RN NSP.FB | 4 |
| 242378 | RN-SU NSP.FB | 2 |
| 242379 | RN-USN NSP.FB | 2 |
| 241958 | RN-SU NSP.FB | 2 |
| 241959 | USN-SU NSP.FB | 2 |
| 241960 | VMF LC.FB | 2 |
| 241957 | VMF NSP.FB | 4 |
| 238757 | RO NSP.FB | 2 |
| 238759 | RO RSP.FB | 2 |
| 237790 | BU NSP.FB | 2 |
| 237980 | FI FAS T Class.FB | 2 |
| 237982 | FI NSP.FB | 4 |
| 238303 | HU RSP.FB | 2 |
| 242407 | NO NSP.FB | 2 |
| 241247 | SU Partisan Cav III A.FB | 3 |
| 241248 | SU Partisan Cav III B.FB | 3 |
| 241249 | SU Partisan Cav III C.FB | 3 |
| 241250 | SU Partisan Cav III D.FB | 3 |
| 241251 | SU Partisan Cav III E.FB | 3 |
| 241252 | SU Partisan Cav III F.FB | 3 |
| 241215 | SU Partisan Inf III 1.FB | 3 |
| 241224 | SU Partisan Inf III 10.FB | 3 |
| 241225 | SU Partisan Inf III 11.FB | 3 |
| 241226 | SU Partisan Inf III 12.FB | 3 |
| 241227 | SU Partisan Inf III 13.FB | 3 |
| 241228 | SU Partisan Inf III 14.FB | 3 |
| 241229 | SU Partisan Inf III 15.FB | 3 |
| 241230 | SU Partisan Inf III 16.FB | 3 |
| 241231 | SU Partisan Inf III 17.FB | 3 |
| 241232 | SU Partisan Inf III 18.FB | 3 |
| 241233 | SU Partisan Inf III 19.FB | 3 |
| 241216 | SU Partisan Inf III 2.FB | 3 |
| 241234 | SU Partisan Inf III 20.FB | 3 |
| 241235 | SU Partisan Inf III 21.FB | 3 |
| 241236 | SU Partisan Inf III 22.FB | 3 |
| 241237 | SU Partisan Inf III 23.FB | 3 |
| 241238 | SU Partisan Inf III 24.FB | 3 |
| 241239 | SU Partisan Inf III 25.FB | 3 |
| 241240 | SU Partisan Inf III 26.FB | 3 |
| 241217 | SU Partisan Inf III 3.FB | 3 |
| 241218 | SU Partisan Inf III 4.FB | 3 |
| 241219 | SU Partisan Inf III 5.FB | 3 |
| 241220 | SU Partisan Inf III 6.FB | 3 |
| 241221 | SU Partisan Inf III 7.FB | 3 |
| 241222 | SU Partisan Inf III 8.FB | 3 |
| 241223 | SU Partisan Inf III 9.FB | 3 |
| 241241 | SU Partisan Inf X A.FB | 3 |
| 241242 | SU Partisan Inf X B.FB | 3 |
| 241243 | SU Partisan Inf X C.FB | 3 |
| 241244 | SU Partisan Inf X D.FB | 3 |
| 241245 | SU Partisan Inf X E.FB | 3 |
| 241246 | SU Partisan Inf X F.FB | 3 |
| 241983 | VMF RSP.FB | 4 |

## Previous completed batch: 1,000 entries (batch 1000c)

**86 assistant-Verified / 914 In progress.** Visually transcribed both appearances of 156 naval entries and three aircraft entries found outside the Air palette, plus the available fronts of 841 single-image ground entries. This covered 31 contact sheets. The ground entries include assault guns, heavy/artillery, rockets, mortars, engineers and light AA.

Current totals: **2,206 Verified / 4,759 In progress / 3 Unreviewed**, across 6,968 records. **2,637 untranscribed queue placeholders remain.** Earlier totals below are historical. All 841 single-image entries use generated blank reverses and remain In progress, per the user's explicit decision; these are not physically confirmed backs.

The 73 naval drafts comprise **36 submarine flotillas** and **37 fast attack squadrons**. Submarine bottom-right numbers are patrol range in sea zones, stored separately as `patrol_range` and `printed_bottom_right`; tactical speed is unknown. FAS bottom-right numbers are retained literally as `printed_bottom_right` pending interpretation. These extra fields survive editor saves but lack dedicated editor controls. Sources: production rules 1.6a, 5.C.2.e.ii and 5.C.4, printed pp32-33 / PDF pp34-35; FAS rules 14.J need to be reconciled before assigning a movement meaning. No gameplay mechanics were implemented.

Identification and rating layout references: UICFB PDF pp1-3; naval codes and symbols in production rules 1.6a 5.C.2, 5.C.5-6 (printed pp31-33 / PDF pp33-35), river flotillas 14.H (printed p106). Printed stars, hashes, parentheses, zeros and codes are retained literally. Light-AA symbol ratings are stored separately from the bottom ground combat rating: for example SU 41A has AA 4 with ground 1-12. Three imported motorized-heavy-artillery labels visibly show a single semi-motorized dot and were recorded accordingly. Small designations on 239324/239325 remain specific physical-counter questions. Parenthesized ground ratings remain literal draft questions.

Evidence and precise per-entry questions: `counter_batches/mixed_1000c_20261025.json`, saved notes and `batch_review` metadata. Verification covers counter metadata only; confidence is assistant review judgment, not a statistical guarantee. Existing reviewed/manual records were not revisited or promoted.

Recovery archive: `assets/counters/recovery_snapshots/before-review-1000c-20261025-212252.zip`; exact immediate pre-save backup: `assets/counters/unit_definition_backups/unit-definitions-20261025-213832-527859.json`. Archive integrity and saved-file bytes checked. All **5,968 non-target records**, unknown target fields, top-level metadata, imported catalog and saved mapping/transport data were preserved. Original artwork and PDFs were untouched.

Validation: **71 tests passed**; all 1,000 entries loaded in a temporary editor without status/file mutation; **43 representative temporary save/reloads**, including all three aircraft and naval patrol-range fields, preserved proposal values and unknown fields. All **841 blank reverses** rendered with original front dimensions and stored colours. Dry-run and applied reports agree. No application code changed during this batch; no commit or push. Interactive review remains manual.

Manual checks:

1. Close and reopen the editor before saving externally updated data; clear filters and expect 2,206 Verified.
2. Inspect Verified `KM MSF M1-A M`: full front gunnery 10, back 5, AA 1 / *, movement 4, code M.
3. Inspect In progress `SU SMot Lt AA II 41A`: ground 1-12, AA 4, generated blank reverse; it must stay In progress after save/reopen.
4. Inspect a submarine and FAS draft: tactical speed remains unknown and the printed bottom-right number is explained in notes. Check Verified `FF F Yak-1bis` for Wing / Squadron sizes and independent face ratings.

## Previous completed batch: 1,000 entries (batch 1000b)

**82 assistant-Verified / 918 In progress.** Inspected both original appearances of the remaining 191 two-image ground queue entries and the available original image of 809 single-image entries (31 contact sheets). All 1,000 now have actual artwork transcription rather than untranscribed inventory placeholders. This includes training, militia/reserve, supply, engineer, fortified-region, infantry, armour, light armour and artillery counters, plus two commanders found in the Ground palette.

**User decision: use the one imported image as front and generate a blank reverse by default, but keep these entries In progress.** Applied this to all 809 single-image entries, storing their sampled background colours and using the existing renderer's front-image dimensions. These are project-default reverses, not claims that physical backs were examined or confirmed blank. Do not auto-promote them just because front completeness passes. This default does not change previously reviewed records.

Current totals: **2,120 Verified / 4,845 In progress / 3 Unreviewed**, across 6,968 records. **3,637 untranscribed queue placeholders remain.** The 918 drafts comprise the 809 single-image records plus 109 two-image records with the questions below. Earlier counts below are historical.

### Remaining questions from this batch

- **53 OP/mobile pairs:** supply terminals, quartermasters and engineer HQ/port/airbase engineers; literal OP/ST, printed capacities and mobile ratings were retained. Neither appearance was inferred to be Reduced.
- **50 fortified-region pairs:** Level text stored independently on both faces. They need a dedicated ground rating format; they are not Coastal Defense counters or conventional reduced-strength pairs.
- **Two commanders:** Mannerheim and Siilasvuo; rank, name, movement, readable numeric modifiers and literal header/lower-line text are recorded. Fields lacking printed numeric modifiers were not filled with invented zero/N/A values.
- **Two VMF railway-artillery/CD pairs:** printed mobile ratings and emplaced level text retained; CD short/long applicability still needs confirmation, including the literal Level 0/5 appearance.
- **One Spanish Volunteer division:** Spain is provisional pending the project nationality convention for ground contingents.
- **One Slovak security pair** prints (1)-4 / (0)-4. Across the entire batch, 59 entries have parenthesized combat values (58 are single-image drafts); parentheses are retained literally pending defense-only applicability/format confirmation.
- **Single-image identity questions:** 239787 is imported as `149TB` but the artwork prints `194TB`; its designation reflects the artwork and the mismatch is noted. It and 239788 have a flamethrower-tank symbol under imported Arm Trng names; classification needs review. The small suffix on 239620's `1bTB` designation also remains a physical-counter question.

No gameplay rules or new editor formats were added. Identification references remain UICFB PDF pp1-3. Source artwork and imported names corroborate one another; ratings were read from artwork, not calculated from filenames or another face. Review confidence is assistant judgment, not a statistical accuracy guarantee. Evidence and precise per-entry questions: `counter_batches/ground_1000b_20261025.json`, saved notes and `batch_review` metadata.

### Recovery and validation

Recovery archive: `assets/counters/recovery_snapshots/before-review-1000b-20261025-072126.zip`. Its six saved JSON files and SHA-256 manifest passed archive/byte checks. Exact immediate pre-save backup: `unit-definitions-20261025-073735-927202.json` in `assets/counters/unit_definition_backups/`. All **5,968 non-target records**, unknown target fields, top-level metadata, mapping/transport data and imported catalog were compared unchanged. Original artwork/PDFs were untouched.

All **71 tests passed**. All 1,000 entries opened with temporary editor data without changing saved statuses or file bytes; **39 representative temporary save/reloads** preserved proposal values, unknown fields and metadata. All **809 generated blank reverses** rendered at the original front dimensions and stored colours. Dry-run and applied reports agree on 82/918; every single-image entry was explicitly checked to remain In progress. No application code changed, and no commit/push was performed. Interactive UI review remains manual.

### Short manual checklist

1. Close and reopen the editor before saving; with filters cleared, expect 2,120 Verified total.
2. Check Verified `GE Trng X 201`: X front, 1-2-4 / Reduced 1-4, type Training.
3. Check In progress `SU Art III 1309`: front 5-4-6 and generated orange blank back; it must remain In progress after save/reopen.
4. Check `SU Arm Trng III 149TB`: printed designation 194TB, stored mismatch note, In progress. Also inspect an OP pair and a UR pair to confirm their appearances are not labelled Reduced.

### Two-image entries still requiring review (109)

| ID suffix | Imported name | Question |
| --- | --- | --- |
| 236388 | GE Mot RR Eng HQ 3.FB | OP/mobile |
| 236389 | GE Mot RR Eng HQ 4.FB | OP/mobile |
| 236390 | GE Mot RR Eng HQ 5.FB | OP/mobile |
| 236391 | GE Mot RR Eng HQ 6.FB | OP/mobile |
| 236394 | GE ST.FB | OP/mobile |
| 236395 | GE QM 1 PzGrppe.FB | OP/mobile |
| 236396 | GE QM 2 PzGrppe.FB | OP/mobile |
| 236397 | GE QM 3 PzGrppe.FB | OP/mobile |
| 236398 | GE QM 4 PzGrppe.FB | OP/mobile |
| 236399 | GE QM AG Lappland.FB | OP/mobile |
| 236400 | GE QM AG Mitte.FB | OP/mobile |
| 236401 | GE QM AG Nord.FB | OP/mobile |
| 236402 | GE QM AG Sud.FB | OP/mobile |
| 236403 | GE QM Lappland.FB | OP/mobile |
| 236404 | GE QM 20 Mtn A.FB | OP/mobile |
| 237083 | KM Port Eng II I_313.FB | OP/mobile |
| 237084 | KM Port Eng II 321.FB | OP/mobile |
| 237085 | KM Port Eng III 323.FB | OP/mobile |
| 237086 | GE Port Eng II 340.FB | OP/mobile |
| 237315 | GE SP Inf XX 250 Sp.FB | Spanish nationality |
| 237877 | FI ST.FB | OP/mobile |
| 237878 | FI QM SHQ 10SP.FB | OP/mobile |
| 237879 | FI QM SHQ 15SP.FB | OP/mobile |
| 237880 | FI Ldr Mannerheim.FB | Commander fields |
| 237881 | FI Ldr Siilasvuo.FB | Commander fields |
| 237886 | FI RR Eng HQ FR.FB | OP/mobile |
| 238119 | HU Mot AB Eng II SHQ.FB | OP/mobile |
| 238138 | HU ST.FB | OP/mobile |
| 238139 | HU QM 2A HOG.FB | OP/mobile |
| 238147 | HU RR Eng HQ 102.FB | OP/mobile |
| 238332 | IT ST.FB | OP/mobile |
| 238333 | IT QM 8A.FB | OP/mobile |
| 238334 | IT QM CSIR @12SP.FB | OP/mobile |
| 238335 | IT QM CSIR @17SP.FB | OP/mobile |
| 238554 | RO Port Eng III RM.FB | OP/mobile |
| 238555 | RO Mot AB Eng II 1 FARR.FB | OP/mobile |
| 238556 | RO Mot AB Eng II 2 FARR.FB | OP/mobile |
| 238559 | RO ST.FB | OP/mobile |
| 238560 | RO QM 3A.FB | OP/mobile |
| 238561 | RO QM 4A.FB | OP/mobile |
| 238566 | RO RR Eng HQ 1.FB | OP/mobile |
| 238567 | RO RR Eng HQ 2.FB | OP/mobile |
| 238568 | RO RR Eng HQ 4.FB | OP/mobile |
| 238782 | SL ST.FB | OP/mobile |
| 238783 | SL QM SFF.FB | OP/mobile |
| 238798 | SL Sec XX 2 @(1)4.FB | Parenthesized rating |
| 240297 | SU Mot RR Eng HQ 1.FB | OP/mobile |
| 240298 | SU Mot RR Eng HQ 2.FB | OP/mobile |
| 240299 | SU Mot RR Eng HQ 3.FB | OP/mobile |
| 240302 | SU ST.FB | OP/mobile |
| 240303 | SU QM DF 2.FB | OP/mobile |
| 240304 | SU QM LF 1.FB | OP/mobile |
| 240305 | SU QM LF 2.FB | OP/mobile |
| 240306 | SU QM SF 1.FB | OP/mobile |
| 241104 | SU Port Eng X 42sd.FB | OP/mobile |
| 241105 | SU Port Eng X 43sd.FB | OP/mobile |
| 241106 | SU Port Eng X 44sd.FB | OP/mobile |
| 241253 | SU UR 1.FB | UR format |
| 241254 | SU UR 2.FB | UR format |
| 241255 | SU UR 3.FB | UR format |
| 241256 | SU UR 4.FB | UR format |
| 241257 | SU UR 5.FB | UR format |
| 241258 | SU UR 6.FB | UR format |
| 241259 | SU UR 7.FB | UR format |
| 241260 | SU UR 8.FB | UR format |
| 241261 | SU UR 9.FB | UR format |
| 241262 | SU UR 10.FB | UR format |
| 241263 | SU UR 11.FB | UR format |
| 241264 | SU UR 12.FB | UR format |
| 241265 | SU UR 14.FB | UR format |
| 241266 | SU UR 15 L1_2.FB | UR format |
| 241267 | SU UR 15 L1_4.FB | UR format |
| 241268 | SU UR 17.FB | UR format |
| 241269 | SU UR 21.FB | UR format |
| 241270 | SU UR 22.FB | UR format |
| 241271 | SU UR 23.FB | UR format |
| 241272 | SU UR 25.FB | UR format |
| 241273 | SU UR 26.FB | UR format |
| 241274 | SU UR 27.FB | UR format |
| 241275 | SU UR 28.FB | UR format |
| 241276 | SU UR 41.FB | UR format |
| 241277 | SU UR 42.FB | UR format |
| 241278 | SU UR 58.FB | UR format |
| 241279 | SU UR 61.FB | UR format |
| 241280 | SU UR 62.FB | UR format |
| 241281 | SU UR 63.FB | UR format |
| 241282 | SU UR 65.FB | UR format |
| 241283 | SU UR 66.FB | UR format |
| 241284 | SU UR 67.FB | UR format |
| 241285 | SU UR 80.FB | UR format |
| 241286 | SU UR 81.FB | UR format |
| 241287 | SU UR 82.FB | UR format |
| 241288 | SU UR 83.FB | UR format |
| 241289 | SU UR 84.FB | UR format |
| 241290 | SU UR 86.FB | UR format |
| 241291 | SU UR I_29.FB | UR format |
| 241292 | SU UR II_29.FB | UR format |
| 241293 | SU UR 1_44.FB | UR format |
| 241294 | SU UR 2_44.FB | UR format |
| 241295 | SU UR I_51.FB | UR format |
| 241296 | SU UR II_51.FB | UR format |
| 241297 | SU UR I_55.FB | UR format |
| 241298 | SU UR II_55.FB | UR format |
| 241299 | SU UR I_64.FB | UR format |
| 241300 | SU UR II_64.FB | UR format |
| 241301 | SU UR I_68.FB | UR format |
| 241302 | SU UR II_68.FB | UR format |
| 241774 | VMF RR Art II 9.FB | CD fields |
| 241775 | VMF RR Art II Baltic.FB | CD fields |

## Previous batch: 1,000 additional ground counters

Directly inspected both original appearances of 1,000 additional untouched queue entries on 42 artwork sheets. **914 are assistant-Verified; 86 remain In progress with transcribed information and explicit questions.** This batch spans Germany (267), Soviet Union (483), Hungary (108), Romania (104), Italy (17), Finland (16) and Slovakia (5). No existing manual or previously transcribed definitions were replaced.

Current totals: **2,038 Verified / 4,927 In progress / 3 Unreviewed** across 6,968 definitions. **4,637 untranscribed queue placeholders remain.** Older counts below describe earlier checkpoints.

Ratings were visually transcribed independently for each appearance, including separate versus combined formats, zero, printed AA and descriptors. UICFB pp1-3 supplies symbols, size-equivalent brackets, AA placement and national/service colour identifiers. Page 2 explicitly identifies the small number inside/beside the icon as AA; clearly legible values in this batch are stored accordingly. Earlier special-marking drafts remain unchanged. Bracketed sizes are retained literally and use their equivalent size; printed suffixes do not change sovereign nationality by inference. No gameplay effects were added.

Alternate operational/Coastal Defense appearances retain Other/Emplaced statuses rather than Reduced. Level-only CD faces retain unknown short/long fields; OP text is preserved without inventing combat ratings. Ground Para-Rifle icons provisionally follow the Glider symbol in UICFB p1 and stay In progress for classification confirmation.

Recovery copy: `assets/counters/recovery_snapshots/before-review-1000-20261025-063935.zip` (six saved JSON files, SHA-256 manifest and archive integrity verified). Normal exact pre-save backup: `unit-definitions-20261025-065209-774096.json` under `assets/counters/unit_definition_backups/`. All **5,968 other records**, target unknown fields, top-level metadata, mapping/transport files and catalog were compared unchanged. Original artwork and PDFs were untouched. Proposals and per-aspect review evidence: `counter_batches/ground_1000_20261025.json`. Verified requires confidence strictly greater than 95%; these are assistant judgments, not statistical accuracy guarantees.

Validation: all **71 tests passed**; all 1,000 proposals opened against temporary editor data without changing saved statuses or bytes. **28 representative temporary save/reloads** preserved proposal values, unknown fields and metadata, including different face formats, AA, equivalent sizes, CD overrides and OP drafts. Dry-run and applied reports agree on 914/86. No application code changed for this batch; no commit/push performed. Interactive UI review remains manual.

### Short manual checklist

1. Close and reopen the editor before further saves; expect 2,038 Verified total with filters cleared.
2. Spot-check `GE Inf X 702`: [X], full 2-6 / Reduced 1-6; `GE Mech XX 16 @1520`: full 15-20 / Reduced 7-8-20, AA 1 on each face.
3. Check In progress examples `LW Mot AB Eng Afrika` (mobile 0-20 / OP), `GE Hvy Art II 144` (artillery 1-4 / emplaced CD Level 1) and `SU Para-Rifle X 1 AC` (classification question). These should remain saveable as drafts.

### The 86 questions in this batch

- **OP (20)**: Operational/mobile OP appearance: confirm applicable format; not a Reduced face.
- **CD (29)**: Emplaced CD level is transcribed; short/long values need confirmation.
- **PARA (30)**: UICFB p1 Glider icon versus imported Para-Rifle label: confirm ground unit classification.
- **HEAVY (5)**: Confirm Heavy descriptor on the physical armour counter.
- **MARK (1)**: Dovator additional vertical descriptor remains unresolved.
- **PAREN (1)**: Parenthesized (1)-6 needs the correct defense-only interpretation/format.

| ID suffix | Imported name (searchable in editor) | Question |
| --- | --- | --- |
| 237120 | GE Sec III Warschau.FB | PAREN |
| 240151 | SU Cdo Cav XX Dovator.FB | MARK |
| 236150 | GE Hvy Arm II 503 @416.FB | HEAVY |
| 236151 | GE Hvy Arm II 503 @6516.FB | HEAVY |
| 236152 | GE Hvy Arm II 503 @7616.FB | HEAVY |
| 236153 | GE Hvy Arm II 505 @416.FB | HEAVY |
| 236154 | GE Hvy Arm II 505 @6516.FB | HEAVY |
| 237444 | LW Mot AB Eng Afrika.FB | OP |
| 237445 | LW Mot AB Eng Atlantik.FB | OP |
| 237446 | LW Mot AB Eng LMR.FB | OP |
| 237447 | LW Mot AB Eng Nord.FB | OP |
| 237448 | LW Mot AB Eng Norwegen.FB | OP |
| 237449 | LW Mot AB Eng I FK.FB | OP |
| 237450 | LW Mot AB Eng II FK.FB | OP |
| 237451 | LW Mot AB Eng IV FK.FB | OP |
| 237452 | LW Mot AB Eng V FK.FB | OP |
| 237453 | LW Mot AB Eng VIII FK.FB | OP |
| 237454 | LW Mot AB Eng IX FK.FB | OP |
| 237455 | LW Mot AB Eng X FK.FB | OP |
| 237459 | LW QMA TG Sud.FB | OP |
| 237461 | LW QMA X FK.FB | OP |
| 241162 | SU Para-Rifle X 1 AC @346.FB | PARA |
| 241163 | SU Para-Rifle X 1 AC @566.FB | PARA |
| 241164 | SU Para-Rifle X 2 AC @346.FB | PARA |
| 241165 | SU Para-Rifle X 2 AC @566.FB | PARA |
| 241166 | SU Para-Rifle X 3 AC @346.FB | PARA |
| 241167 | SU Para-Rifle X 3 AC @566.FB | PARA |
| 241168 | SU Para-Rifle X 4 AC @346.FB | PARA |
| 241169 | SU Para-Rifle X 4 AC @566.FB | PARA |
| 241170 | SU Para-Rifle X 5 AC @346.FB | PARA |
| 241171 | SU Para-Rifle X 5 AC @566.FB | PARA |
| 241172 | SU Para-Rifle X 6 AC @346.FB | PARA |
| 241173 | SU Para-Rifle X 6 AC @566.FB | PARA |
| 241174 | SU Para-Rifle X 7 AC @346.FB | PARA |
| 241175 | SU Para-Rifle X 7 AC @566.FB | PARA |
| 241176 | SU Para-Rifle X 8 AC @346.FB | PARA |
| 241177 | SU Para-Rifle X 8 AC @566.FB | PARA |
| 241178 | SU Para-Rifle X 9 AC @346.FB | PARA |
| 241179 | SU Para-Rifle X 9 AC @566.FB | PARA |
| 241180 | SU Para-Rifle X 10 AC @346.FB | PARA |
| 241181 | SU Para-Rifle X 10 AC @566.FB | PARA |
| 241562 | SU Gds Para-Rifle XX 1.FB | PARA |
| 241563 | SU Gds Para-Rifle XX 2.FB | PARA |
| 241564 | SU Gds Para-Rifle XX 3.FB | PARA |
| 241565 | SU Gds Para-Rifle XX 4.FB | PARA |
| 241566 | SU Gds Para-Rifle XX 5.FB | PARA |
| 241567 | SU Gds Para-Rifle XX 6.FB | PARA |
| 241568 | SU Gds Para-Rifle XX 7.FB | PARA |
| 241569 | SU Gds Para-Rifle XX 8.FB | PARA |
| 241570 | SU Gds Para-Rifle XX 9.FB | PARA |
| 241571 | SU Gds Para-Rifle XX 10.FB | PARA |
| 235720 | GE Hvy Art II 144.FB | CD |
| 235721 | GE Hvy Art II 145.FB | CD |
| 235722 | GE Hvy Art II 147.FB | CD |
| 235723 | GE Hvy Art II 148.FB | CD |
| 235724 | GE Hvy Art II 149.FB | CD |
| 235725 | GE Hvy Art II 284.FB | CD |
| 235726 | GE Hvy Art II 287.FB | CD |
| 235727 | GE Hvy Art II 289.FB | CD |
| 235728 | GE Hvy Art II 338.FB | CD |
| 235729 | GE Hvy Art II 474.FB | CD |
| 235731 | GE Hvy Art II 498.FB | CD |
| 235732 | GE Hvy Art II 504.FB | CD |
| 235733 | GE Hvy Art II 531.FB | CD |
| 235736 | GE Hvy Art II 707.FB | CD |
| 235737 | GE Hvy Art II 708.FB | CD |
| 235738 | GE Hvy Art II 774.FB | CD |
| 235739 | GE Hvy Art II 799.FB | CD |
| 235740 | GE Hvy Art II 910.FB | CD |
| 235741 | GE Hvy Art II 914.FB | CD |
| 235749 | GE SMot Hvy Art II 772.FB | CD |
| 235750 | GE SMot Hvy Art II 789.FB | CD |
| 235760 | GE SMot Hvy Art II 901.FB | CD |
| 235761 | GE SMot Hvy Art II 903.FB | CD |
| 235762 | GE SMot Hvy Art II 906.FB | CD |
| 235763 | GE SMot Hvy Art II 928.FB | CD |
| 235764 | GE SMot Hvy Art II 929.FB | CD |
| 235765 | GE SMot Hvy Art II 985.FB | CD |
| 235766 | GE SMot Hvy Art II 986.FB | CD |
| 235937 | GE Mot Siege Art II 767.FB | CD |
| 236382 | GE River Eng HQ 2.FB | OP |
| 236383 | GE River Eng HQ 3.FB | OP |
| 236384 | GE River Eng HQ 4.FB | OP |
| 236385 | GE River Eng HQ Wskdo.FB | OP |
| 236386 | GE Mot RR Eng HQ 1.FB | OP |
| 236387 | GE Mot RR Eng HQ 2.FB | OP |

## Previous batch: 500 Soviet infantry entries

Directly inspected both artwork faces of IDs `vassal:133:240307` through `vassal:133:240806` and replaced those 500 queue placeholders with transcribed definitions. **495 are Verified; 5 remain In progress** because an additional printed `1` inside the front infantry symbol needs interpretation:

| ID suffix | Printed division designation | Front / back main ratings |
| --- | --- | --- |
| 240652 | 395 | 7–8–6 / 3–4–6 |
| 240719 | 99 | 10–6 / 5–6 |
| 240725 | 112 | 10–6 / 5–6 |
| 240781 | 14 | 12–6 / 6–6 |
| 240788 | 52 | 12–6 / 6–6 |

The main ratings, designation, infantry symbol, size and front/back status were transcribed for all 500. The extra `1` was recorded in notes rather than guessed as AA or another attribute. Soviet Union / Red Army identity follows the artwork colour key; printed ethnic/place-name and `m` suffixes were retained literally without inferring gameplay effects. Review confidence exceeds 95% on all aspects of the 495 Verified entries; the five unresolved fronts are recorded below threshold. Evidence: `counter_batches/soviet_infantry_500_20261025.json`.

Updated totals: **1,124 Verified / 5,841 In progress / 3 Unreviewed**. **5,637 untranscribed queue entries remain.** The earlier full-catalog-pass figures below are historical, not the current totals.

Fresh recovery archive: `assets/counters/recovery_snapshots/before-review-500-20261025-062350.zip`, with six saved JSON files and a verified SHA-256 manifest. All 6,468 records outside this batch, unknown target fields and top-level metadata were preserved. Exact immediate pre-save definition backup also verified.

All 71 tests passed. All 500 proposed definitions opened against temporary editor fixtures; seven temporary save/reloads preserved transcribed ratings, statuses and unknown fields. Queue replacement now requires an explicit unchanged-record fingerprint and rejects entries with manual ratings, identity, images or changed status. Add-only batches still skip existing records. No commit/push performed.

Restart the editor before saving. Check Verified + `SU Inf XX` for the new entries; spot-check `45 Uzbek` (5–6–6 / 2–3–6), `103m` (6–6 / 3–6), and the five In progress exceptions above. Interactive UI inspection remains a manual check.

## What this pass actually completed

- Visually inspected both original faces of 368 further German infantry-division entries.
- Added 367 as assistant-Verified, with independently transcribed combined/separate face formats, printed designations, infantry symbol and XX/Reduced labels.
- Added the reviewed 78 Sturm entry (vassal:133:236831) as In progress. Its extra printed `1` inside the front symbol needs interpretation. Its visible ratings were transcribed as front 19–6 and back 9–10–6; no meaning was invented for the extra mark.
- Added 6,137 **review-queue entries**, explicitly marked In progress and **not visually transcribed**. These hold catalog category/source-image references and specific missing-review notes, not guessed ratings or inferred front/back assignments. They are not completed counter definitions.
- Preserved every field and review status of all 463 pre-existing definitions, including the user's unfinished aircraft work.

The catalog now has 6,968 saved records: **629 Verified, 6,336 In progress, 3 Unreviewed**. The previous pilot and user-verified counters are included in those totals. The full catalog has **not** been visually verified or fully transcribed. Naval, other ground layouts and the previous aircraft review queue still need work.

## Confidence policy

New automatic Verified status requires confidence **strictly greater than 0.95** for identity, front and back, complete review evidence/fingerprints, no outstanding issues and the editor's metadata completeness checks. Values at 0.95, missing/invalid values and unresolved markings remain In progress. Confidence is recorded assistant judgment, not a calibrated statistical accuracy guarantee. Complete fields alone are insufficient for verification.

Local Windows OCR did not reliably read the test artwork. An exact-template recognizer also failed on small raster differences. Neither experiment was used to verify any saved entry; the recognizer experiment was removed from production code. The new Verified records came from direct artwork inspection. Do not describe this pass as successful unattended OCR or as full-catalog artwork review.

Review proposals/evidence are retained in `counter_batches/full_catalog_20261025.json`; per-entry `batch_review` data retains evidence, confidence and unresolved issues. Source symbol/size/colour reference: UICFB PDF pp1–3. No gameplay rule calculations were added.

## Recovery copy

Before changes, six current saved JSON data files were copied into:

`assets/counters/recovery_snapshots/before-full-counter-review-20261025-060256.zip`

The archive includes the definitions, imported catalog, root saved JSON data and a SHA-256 manifest. Every archived file was compared with its pre-pass bytes, and archive integrity passed. Original artwork/PDFs were not changed. The normal timestamped definition backups also retain the immediate pre-save file.

To restore counter definitions only: close the editor/main app, keep a separate copy of the latest definitions, open the recovery archive and copy its `assets/counters/unit_definitions.json` over the project file at that same relative path. Do not restore terrain/transport files unless those also need rollback. Restart the app afterward. Recovery archives remain local and are not uploaded by Git.

## Checks and manual spot checks

- All 69 tests passed; automated persistence tests used temporary fixtures only.
- Dry-run and final batch reports agreed on 367 Verified / 6,138 In progress.
- All 463 prior records and top-level metadata were compared unchanged; exact pre-save backup verified.
- Restart the editor before saving after external additions. The Verified total should be 629.
- Spot-check division 328 at 10–11–6 / 5–6–6 and division 336 at 12–13–6 / 6–7–6, plus the In progress 78 Sturm exception.
- Interactive UI review remains untested for this full pass. Queue entries deliberately retain Unknowns and require transcription before completeness checks can pass. No commit or push was performed.
