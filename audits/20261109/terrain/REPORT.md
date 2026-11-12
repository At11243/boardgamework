# Terrain audit and local prototype

Read-only review, 2026-11-10. Saved labels and calibration were not corrected.

## Coverage

- Current saved file: 8,307 records; 8,134 Verified. The current-file inventory supersedes historical prose counts.
- Export attempted for every saved record: 8,121 native crops; 186 clipped/off-board records excluded. Original pixels are retained, with a 90% inset polygon used for feature measurement, not image resizing.
- Four alignment overlays were inspected against source board pixels. All 220 exportable non-water Verified hexes and a 36-hex water sample were visually inspected. This is not visual verification of all 8,134 Verified hexes.
- All exported Verified water claims received a coarse blue-pixel screening. 47 fall below 90% blue and require inspection; this is an anomaly screen, not a rule or a confirmed error.
- Scope: primary printed terrain texture, missing terrain and crop geometry. Settlements, facilities, hexsides, roads, railways and every compound terrain combination were not independently audited.
- Geometry/completeness flag counts: `{"crop_geometry_flag": 186, "confirmed_completeness_error": 2, "region_geometry_flag": 155}`. Region/playability flags are exclusions for training, not automatic evidence that a saved hex is invalid. Some derived references disagree with the printed number; retain stable keys and review canonical region assignment.

## Proposed terrain corrections

UICFB p4 Terrain Key distinguishes small Steppe grass tufts, Swamp reeds/horizontal strokes, and blue Lakes specks. Blue alone is not sufficient evidence of Swamp. For the prototype, “marsh” is treated as editor Swamp; Salt Marsh remains separate pending confirmation. Coastal land components and the project’s >20% convention need human adjudication where marginal.

| Stable key | Derived reference | Current | Proposed land texture | Original-pixel crop |
| --- | --- | --- | --- | --- |
| ['Map 3', 'FB-RH', 74, 14] | FB-RH:0123 | ['Clear'] | ['Steppe'] | [crop](crops/Map_3--FB-RH--74--14.png) |
| ['Map 3', 'FB-QH', 71, 12] | FB-QH:3126 | ['Clear'] | ['Steppe'] | [crop](crops/Map_3--FB-QH--71--12.png) |
| ['Map 3', 'FB-QH', 73, 12] | FB-QH:3124 | ['Clear'] | ['Steppe'] | [crop](crops/Map_3--FB-QH--73--12.png) |
| ['Map 3', 'FB-QH', 56, 6] | FB-QH:2441 | ['Clear'] | ['Steppe'] | [crop](crops/Map_3--FB-QH--56--6.png) |
| ['Map 3', 'FB-QH', 53, 11] | FB-QH:3044 | ['Clear'] | ['Steppe'] | [crop](crops/Map_3--FB-QH--53--11.png) |
| ['Map 3', 'FB-QH', 53, 5] | FB-QH:2444 | ['Clear'] | ['Steppe'] | [crop](crops/Map_3--FB-QH--53--5.png) |
| ['Map 3', 'FB-QH', 54, 5] | FB-QH:2343 | ['Clear'] | ['Steppe'] | [crop](crops/Map_3--FB-QH--54--5.png) |
| ['Map 3', 'FB-QH', 54, 6] | FB-QH:2443 | ['Clear'] | ['Steppe'] | [crop](crops/Map_3--FB-QH--54--6.png) |
| ['Map 3', 'FB-QH', 54, 11] | FB-QH:2943 | ['Clear'] | ['Steppe'] | [crop](crops/Map_3--FB-QH--54--11.png) |
| ['Map 3', 'FB-QH', 54, 12] | FB-QH:3043 | ['Clear'] | ['Steppe'] | [crop](crops/Map_3--FB-QH--54--12.png) |
| ['Map 3', 'FB-QH', 55, 12] | FB-QH:3142 | ['Clear'] | ['Steppe'] | [crop](crops/Map_3--FB-QH--55--12.png) |
| ['Map 3', 'FB-QH', 55, 11] | FB-QH:3042 | ['Clear'] | ['Steppe'] | [crop](crops/Map_3--FB-QH--55--11.png) |
| ['Map 3', 'FB-QH', 55, 5] | FB-QH:2442 | ['Clear'] | ['Steppe'] | [crop](crops/Map_3--FB-QH--55--5.png) |
| ['Map 3', 'FB-QH', 56, 11] | FB-QH:2941 | ['Clear'] | ['Steppe'] | [crop](crops/Map_3--FB-QH--56--11.png) |
| ['Map 3', 'FB-QH', 56, 12] | FB-QH:3041 | ['Clear'] | ['Steppe'] | [crop](crops/Map_3--FB-QH--56--12.png) |
| ['Map 3', 'FB-RH', 56, 14] | FB-RH:0141 | ['Clear'] | ['Steppe'] | [crop](crops/Map_3--FB-RH--56--14.png) |
| ['Map 3', 'FB-RH', 56, 15] | FB-RH:0241 | ['Clear'] | ['Steppe'] | [crop](crops/Map_3--FB-RH--56--15.png) |
| ['Map 3', 'FB-RH', 57, 16] | FB-RH:0440 | ['Clear'] | ['Steppe'] | [crop](crops/Map_3--FB-RH--57--16.png) |
| ['Map 3', 'FB-RH', 57, 15] | FB-RH:0340 | ['Clear'] | ['Steppe'] | [crop](crops/Map_3--FB-RH--57--15.png) |
| ['Map 3', 'FB-RH', 57, 14] | FB-RH:0240 | ['Clear', 'Swamp'] | ['Steppe'] | [crop](crops/Map_3--FB-RH--57--14.png) |
| ['Map 3', 'FB-QH', 57, 7] | FB-QH:2640 | ['Clear'] | ['Steppe'] | [crop](crops/Map_3--FB-QH--57--7.png) |
| ['Map 3', 'FB-QH', 58, 10] | FB-QH:2839 | ['Clear'] | ['Steppe'] | [crop](crops/Map_3--FB-QH--58--10.png) |
| ['Map 3', 'FB-QH', 58, 11] | FB-QH:2939 | ['Clear'] | ['Steppe'] | [crop](crops/Map_3--FB-QH--58--11.png) |
| ['Map 3', 'FB-QH', 58, 12] | FB-QH:3039 | ['Clear'] | ['Steppe'] | [crop](crops/Map_3--FB-QH--58--12.png) |
| ['Map 3', 'FB-RH', 58, 14] | FB-RH:0139 | ['Clear'] | ['Steppe'] | [crop](crops/Map_3--FB-RH--58--14.png) |
| ['Map 3', 'FB-QH', 55, 6] | FB-QH:2542 | ['Clear'] | ['Steppe'] | [crop](crops/Map_3--FB-QH--55--6.png) |
| ['Map 3', 'FB-RH', 71, 14] | FB-RH:0226 | ['Clear'] | ['Lakes'] | [crop](crops/Map_3--FB-RH--71--14.png) |
| ['Map 3', 'FB-RH', 71, 15] | FB-RH:0326 | ['Clear'] | ['Lakes'] | [crop](crops/Map_3--FB-RH--71--15.png) |
| ['Map 3', 'FB-RH', 69, 14] | FB-RH:0228 | ['Clear'] | ['Lakes'] | [crop](crops/Map_3--FB-RH--69--14.png) |
| ['Map 3', 'FB-QH', 72, 12] | FB-QH:3025 | ['Clear'] | ['Swamp'] | [crop](crops/Map_3--FB-QH--72--12.png) |
| ['Map 3', 'FB-RH', 72, 14] | FB-RH:0125 | None | ['Swamp'] | [crop](crops/Map_3--FB-RH--72--14.png) |

These 31 proposals include 26 Steppe, three Lakes and two Swamp cases. They are saved-label/source disagreements, not measured model errors. Inspect audit-01.png (Clear/Steppe and Lakes examples) and swamp-seed-candidates.png (Swamp detail). No proposals have been applied.

## Prototype and results

- Python/PySide6 reads original boards through the existing hex geometry. Twenty NumPy features describe RGB quantiles, blue/green/dark coverage, native-pixel gradients at 1/2/4 pixels and short/long ink runs. This preserves fine printed marks and is easier to inspect than a large learned model.
- Standardized nearest-class centroids were fitted to 8 Clear, 11 Steppe and 7 Swamp visually reviewed seed crops. These labels are isolated from live Verified statuses. The seeds are geographically narrow and may miss other board palettes.
- Map 9 is reserved for evaluation before label collection/tuning; fresh Map 6 and Map 9 crops use a 500-pixel board-edge margin. No augmentations. Neighboring hexes from the evaluation board cannot enter training. Existing seed crops are from other boards.
- Per-class held-out counts: Clear 0, Steppe 0, Swamp 0. Recall/precision and model error examples are **not yet available**. No training accuracy is offered as a substitute. A neural classifier is deferred until sufficient reviewed training and held-out examples exist.
- suggestions.json contains stable board/region/column/row keys, derived printed references, relative centroid scores and review flags. All suggestions require review. Water, geometry and feature-distance exclusions can produce no suggestion. Scores are not calibrated correctness probabilities and must not be compared with the counter 95% threshold.
- A 72-crop human queue includes 24 existing informative cases and 24 fresh cases on each of Map 6 and Map 9. Use Other/Mixed/Unsure rather than forcing forest, relief, lakes or ambiguous coastlines into the three classes.
- Human labeling time is recorded, but this first workflow shows no predictions to avoid anchoring initial labels. Suggestion-correction versus manual timing has not been measured; an equivalent randomized follow-up batch is required.

## Run from the project root

```powershell
.venv/Scripts/python.exe -m audit_tools.terrain alignment
.venv/Scripts/python.exe -m audit_tools.terrain export
.venv/Scripts/python.exe -m audit_tools.prepare_terrain_review
.venv/Scripts/python.exe -m audit_tools.terrain_baseline
.venv/Scripts/python.exe -m audit_tools.terrain_labeler
.venv/Scripts/python.exe -m audit_tools.report_terrain
.venv/Scripts/python.exe -m unittest audit_tools.test_terrain_tools
```

Export/preparation regenerate derived audit files in this dated directory; archive the directory before refreshing against edited source maps. Human answers are kept separately in human_labels.json and are not reset by preparation. Baseline reruns consume those answers; Map 9 answers remain evaluation-only.

## Manual checks / needed input

1. Launch the labeler; compare a few crops with the matching original board, then answer the 72 examples. Pixelated 4× display is intentional: no smoothing hides tiny marks.
2. Close/reopen to confirm answers persist. Labels are in the audit directory, not map_terrain.json.
3. Confirm that “marsh” should mean Swamp, with Salt Marsh separate, and review the 31 proposed corrections before applying anything.
4. Rerun the baseline after labeling. Inspect held-out confusion/errors before collecting additional examples or selecting a neural model.

Tests: three focused tests passed (finite/separable baseline scores, temporary-file atomic persistence/backup, evaluation-board seed exclusion); all audit Python modules compile. Interactive labeling behavior has not been user-tested. No gameplay or transport rules implemented.
