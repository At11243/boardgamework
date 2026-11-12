# Counter audit and terrain prototype

Work started November 9 and completed November 10, 2026. No commits or pushes. Existing application edits were preserved. Counter definitions, imported catalog, terrain and transport hashes match the starting snapshot; see protected_data_check.json.

## Read these first

- [Counter report](counters/REPORT.md): all-record checks, precise independent coverage, nine confirmed incorrect physical-source locators and six ambiguous cases.
- [Terrain report](terrain/REPORT.md): visual audit, 31 proposed texture corrections, geometry exclusions, native crop pipeline, baseline limitations and labeling instructions.

The counter audit is **not complete independent verification of a majority of all metadata**. Of 5,708 Verified counters, 2,871 have fresh OCR corroboration of a literal factor/code field (50.3%); 120 received stratified manual image inspection. These are different levels of evidence. No status or rating was changed. More source images are not required just to continue digital-art inspection; broader manual transcription and reliable physical sheet locators are still required. For physical-only questions, uncropped sheet images with unambiguous sheet/page/front-back orientation would help. Existing nine incorrect locators must be resolved before relying on their blank-back claims.

## Repository inventory

| Purpose | Location / observation |
| --- | --- |
| Instructions / priorities | AGENTS.md, PROJECT_CONTEXT.md; read before work |
| Definitions / import catalog | assets/counters/unit_definitions.json and counter_catalog.json; separate roles |
| Counter artwork | assets/counters/images; 9,696 imported paths present |
| Counter review/import code | counters/unit_editor.py, unit_storage.py, import_counters.py, batch_review.py; existing counter_batches and tmp review helpers |
| Physical scans | Downloads/KIC Document 108, 120, 132, 185, 199 and 2262.pdf; exact hashes in counters/consistency.json |
| Rules and charts | reference and reference/charts; UICFB p4 used for terrain symbols. Production 1.6a and Print 1.6 versions coexist; this pass implements no gameplay rules |
| Board artwork | assets/maps; original PNGs, 18 boards plus supporting images |
| Active campaign boards | Map 2, 3, 5, 6, 8, 9, 11, 12 |
| Actual calibration / stable keys | maps/campaign_grid_definitions.py and maps/hex_model.py; maps/campaign_layout.py handles placement |
| Live map data | map_terrain.json and map_transport.json; read-only this pass |
| Existing map tools | maps/terrain_editor.py, maps/mapping_support.py, maps/map_view.py; prior map_batches are claims, not automatically trusted labels |
| New isolated tools | audit_tools; Python except the small Windows OCR PowerShell bridge |

Git was dirty at entry: modifications to project/reference/readme documents, counter definitions/editor/tests, terrain/transport and map view/editor, plus existing untracked review documents and batches. Those were not reset, cleaned or rewritten. This pass adds audit_tools and audits only.

## Reproduction

Use the project root and `.venv/Scripts/python.exe`. NumPy, PySide6 and PyMuPDF were already installed. No neural framework, remote API, model download or new dependency was needed.

Terrain commands and the 72-example labeling workflow are in its report. Counter preparation:

```powershell
.venv/Scripts/python.exe -m audit_tools.counters
.venv/Scripts/python.exe -m audit_tools.ocr_factors
.venv/Scripts/python.exe -m audit_tools.summarize_counter_ocr
.venv/Scripts/python.exe -m audit_tools.manual_counter_batch
.venv/Scripts/python.exe -m audit_tools.manual_findings
.venv/Scripts/python.exe -m audit_tools.report_counters
```

OCR preparation makes four `jobs-*.json` files. Run each with `audit_tools/ocr_artwork.ps1 -Jobs <job-file>` and similarly the factor-strip jobs before summarizing. The Windows Runtime OCR bridge is needed because that built-in OCR engine has no native Python API here. Cached OCR outputs are reused: archive this dated directory before a fresh audit against changed artwork, otherwise old OCR may be reused. Manual observations are dated findings, not a reusable automatic visual verifier.

## What is needed next

1. Review the nine counter provenance errors and six ambiguous entries together; leave ratings and art unchanged until the evidence is resolved.
2. Confirm the terrain vocabulary: prototype marsh = Swamp, Salt Marsh separate. Blue specks can mean Lakes.
3. Label the 72 isolated crops in the standalone Python window. Map 9 is held out. These answers enable honest per-class performance and model-error examples; currently evaluation counts are zero.
4. Review terrain proposals before any live correction. Classifier outputs are all flagged for human review. A separate randomized batch will be needed to compare correction time with manual labeling time.

Three new focused tests passed and all audit modules compile. No interactive user acceptance test or neural-classifier comparison has been completed. Roads/railways and the application shell remain outside this work.
