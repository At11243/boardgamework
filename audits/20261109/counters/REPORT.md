# Counter audit — started 2026-11-09, completed 2026-11-10

**Read-only proposals. No catalog, saved definitions, status or artwork changed.**

Current inventory: **6,968 definitions; 5,708 Verified / 1,260 In progress**. Previous prose notes are historical claims, not the current-file inventory.

## Coverage and evidence

- Automated structural/completeness audit: **all 6,968 definitions**, including all 5,708 completed entries. No duplicate JSON keys, no missing catalog IDs, all 9,696 imported artwork paths exist; assigned artwork is readable and recorded hashes agree. All 5,708 completed entries pass existing editor completeness checks. The 33 missing assigned-front flags concern In progress placeholders, not completed entries.
- Fresh original-art OCR: **9,454 face images**, covering every completed front and assigned printed reverse. OCR panels contain original pixels only; expected metadata is never rendered into the OCR inputs. Contrast-normalized strips are a second pixel view, not a second catalog. Windows OCR independently transcribes them before comparison.
- **2,871 / 5,708 (50.3%)** completed entries have a matching front literal printed-factor sequence/code from fresh OCR. This establishes only the named factor field, not a fully verified entry. All failures remain unresolved OCR, not proposed corrections.
- **120 entries (2.1%) manually inspected** in 20 stratified batches, spanning 18 nationalities, all five completed counter categories and 73 nationality/category/ground-format strata. Front and assigned reverse original art compared for visible designation, symbol, size/status and printed factors. Physical crops compared where direct source locators exist. **2,930 unique completed IDs** have at least a manual-art or matching-factor check; these counts overlap.
- **Full independent metadata/physical verification of a majority has NOT been achieved.** Majority coverage here is automated factor corroboration only. Nationality/service for every entry, all tiny modifiers, and correct physical-front/reverse relationships across most entries remain unverified. A prior confidence number or generated review file is not independent evidence.

## Confirmed source-locator errors

These are corroboration/provenance errors: current physical locations point to other counters. They do not by themselves prove that the saved digital ratings are wrong. The nine cases were also re-extracted directly from the original PDF embedded images, using the existing sheet geometry and surrounding cells, rather than relying solely on cached crops. Proposed correction: replace or withdraw the incorrect physical corroboration claim and find the exact cell. Preserve current art/ratings until that review.

| ID | Current claim / source | Observed problem | Proposed correction |
| --- | --- | --- | --- |
| vassal:133:238842 | KIC Document 185.pdf, PDF p1, r12 c4: Printed front/back corroborated | Source crop shows SB-2 and a fighter appearance, not IL-2. | Correct source locator; re-establish physical pair/blank evidence. |
| vassal:133:236047 | KIC Document 199.pdf, PDF p7, r13 c16: Blank confirmed | Source crop shows a black naval/escort appearance, not grey Svolvar Level 24. | Correct source locator; re-establish physical pair/blank evidence. |
| vassal:133:235972 | KIC Document 199.pdf, PDF p9, r2 c16: Blank confirmed | Source crop shows security 668 Rusl (1)-6, not Arko 108 6-4-18. | Correct source locator; re-establish physical pair/blank evidence. |
| vassal:133:242048 | KIC Document 120.pdf, PDF p9, r7 c1: Blank confirmed | Source crop shows Sea Hurricane IC aircraft, not commando 12. | Correct source locator; re-establish physical pair/blank evidence. |
| vassal:133:239486 | KIC Document 132.pdf, PDF p7, r10 c7: Blank confirmed | Source crop shows artillery headquarters 6AD / 12, not 107/3GAD 4-5-12. | Correct source locator; re-establish physical pair/blank evidence. |
| vassal:133:236013 | KIC Document 199.pdf, PDF p11, r10 c19: Blank confirmed | Source crop shows black naval appearance and Spotted marker, not Bergen Level 16. | Correct source locator; re-establish physical pair/blank evidence. |
| vassal:133:236061 | KIC Document 199.pdf, PDF p9, r7 c8: Blank confirmed | Source crop shows training/security appearance (1)-4, not Vestfjord Level 35. | Correct source locator; re-establish physical pair/blank evidence. |
| vassal:133:235682 | KIC Document 199.pdf, PDF p9, r8 c16: Blank confirmed | Source crop shows armour 232, 2-18, not antiaircraft 286, 1-2-20. | Correct source locator; re-establish physical pair/blank evidence. |
| vassal:133:241052 | KIC Document 108.pdf, PDF p7, r1 c5: Blank confirmed | Source crop shows infantry 199, 10-6, not engineer 12, (1)-6. | Correct source locator; re-establish physical pair/blank evidence. |

## Ambiguous or unreadable source evidence

| ID | Current value | Uncertainty | Proposed action |
| --- | --- | --- | --- |
| vassal:133:238452 | Printed reverse confirmed | Physical front mostly cut off; cell crop does not fully establish original regiment 53. | Inspect uncropped physical front/back with neighboring context; no automatic correction. |
| vassal:133:242434 | Blank confirmed | Front name/cell boundary truncated and proposed back contains green infantry. Recheck alignment before claiming blank reverse. | Inspect uncropped physical front/back with neighboring context; no automatic correction. |
| vassal:133:238152 | Blank confirmed | Physical source looks like IV headquarters while saved front is V; inspect the uncropped sheet to distinguish orientation and column offset. | Inspect uncropped physical front/back with neighboring context; no automatic correction. |
| vassal:133:240304 | Existing printed reverse corroborated | Physical reverse capacity appears 10 SP whereas digital pair has 20 SP. Candidate alignment/version needs examination. | Inspect uncropped physical front/back with neighboring context; no automatic correction. |
| vassal:133:237632 | Blank confirmed | Blank-looking reverse contains faint rectangle; cannot distinguish bleed-through from printed marks here. | Inspect uncropped physical front/back with neighboring context; no automatic correction. |
| vassal:133:242083 | Printed reverse confirmed | Physical front/reverse crop boundaries cut through neighbouring submarine/ship cells; require source-context alignment. | Inspect uncropped physical front/back with neighboring context; no automatic correction. |

No confirmed numeric-factor transcription error was found in the manual sample. OCR mismatches are exported individually with expected and observed text in `ocr_comparison.json`; they are NOT confirmed data errors. Seven shared front-art groups and eleven nonreciprocal link groups are listed in `consistency.json`; duplicated appearances and physical variants can make these legitimate. No ID merge or reciprocal rewrite is proposed solely from this check.

## Fields checked by automated artwork reading

| Category | Completed fronts attempted | Matching printed field | Field scope |
| --- | --- | --- | --- |
| Air unit | 439 | 58 | top attack/code/defense |
| Commander | 2 | 0 | manual sample only; automated text not counted as corroborated |
| Ground unit | 4584 | 2723 | core bottom ratings or printed level/code |
| Marker | 7 | 0 | manual sample only; automated text not counted as corroborated |
| Naval unit | 676 | 90 | top gunnery/code/protection |

A single movement/level field is weaker evidence than a full three-factor line. Per-entry `field`, `expected`, `observed`, image path and image SHA-256 make that distinction reviewable. No OCR score is treated as >95% certainty.

## Available references and what is still needed

- Six KIC PDFs are locally accessible: Documents **108 (10 pages), 120 (10), 132 (10), 185 (10), 199 (12), 2262 (3)**. Source hashes and paths are recorded in consistency.json. No new LW sheet photos were supplied; original digital LW artwork remains available, but physical-sheet corroboration needs those front/back scans.
- UICFB (both copies), General Charts v1.6, production rules 1.6a/1.6 and six order-of-battle/reference PDFs are locally available. UICFB pp1–3 supplies symbol/size/palette references; source scans supersede prior generated audit prose as physical evidence.
- To resolve locator failures, the existing scans need exact sheet/cell re-identification with uncropped front/back context; no additional photo is necessarily needed. Where the sheet/version is genuinely missing or unreadable, ask for a clearer front/back image with sheet identity.
- All-entry historical nationality/organization verification would additionally need applicable scenario/order-of-battle references, rather than inferring it from art names. Counter metadata and gameplay rules remain distinct.

## Reproduce

From the repository root, using the existing virtual environment:

```powershell
.venv/Scripts/python.exe -m audit_tools.counters
0..3 | ForEach-Object { powershell -NoProfile -File audit_tools/ocr_artwork.ps1 -Jobs "audits/20261109/counters/jobs-$_.json" }
.venv/Scripts/python.exe -m audit_tools.ocr_factors
0..3 | ForEach-Object { powershell -NoProfile -File audit_tools/ocr_artwork.ps1 -Jobs "audits/20261109/counters/factor-jobs-$_.json" }
.venv/Scripts/python.exe -m audit_tools.summarize_counter_ocr
```

The Python scripts prepare and compare original-pixel inputs. The small PowerShell helper only calls Windows’ built-in OCR API because no Python OCR library is installed; training and analysis remain Python. It does not download a model or change catalog data. OCR output is cached per image panel; use a fresh output directory when source inputs change (the default folder records this run). Manual findings are dated review observations, not automatically repeatable judgments.

Evidence: [manual selection and findings](manual_review.json), [fresh OCR comparison](ocr_comparison.json), [consistency checks](consistency.json). Contact sheets: manual/batch-01.png through batch-20.png; direct PDF locator proof: manual/direct-pdf-locator-checks.png.
