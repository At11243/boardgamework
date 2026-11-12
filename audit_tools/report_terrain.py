"""Generate audit report and all-record water screening, without changing maps."""
import json, hashlib
from pathlib import Path
from collections import Counter
from audit_tools.terrain_labeler import ROOT

def main():
    manifest=json.loads((ROOT/'manifest.json').read_text()); audit=json.loads((ROOT/'audit_proposals.json').read_text())
    import numpy as np
    x=np.load(ROOT/'features.npz')['X']
    water=[{'key':z['key'],'hex_id':z['hex_id'],'blue_fraction':float(x[z['features_index'],10]),'source':z['crop']} for z in manifest['rows'] if z['review_status']=='Verified' and z['live_terrain']==['Lake/Sea'] and x[z['features_index'],10]<.90]
    (ROOT/'water_screening_flags.json').write_text(json.dumps(water,indent=2))
    flags=Counter(z['kind'] for z in audit['flags'])
    lines=['# Terrain audit and local prototype', '',
    'Read-only review, 2026-11-10. Saved labels and calibration were not corrected.', '',
    '## Coverage', '',
    '- Current saved file: 8,307 records; 8,134 Verified. The current-file inventory supersedes historical prose counts.',
    '- Export attempted for every saved record: 8,121 native crops; 186 clipped/off-board records excluded. Original pixels are retained, with a 90% inset polygon used for feature measurement, not image resizing.',
    '- Four alignment overlays were inspected against source board pixels. All 220 exportable non-water Verified hexes and a 36-hex water sample were visually inspected. This is not visual verification of all 8,134 Verified hexes.',
    '- All exported Verified water claims received a coarse blue-pixel screening. '+str(len(water))+' fall below 90% blue and require inspection; this is an anomaly screen, not a rule or a confirmed error.',
    '- Scope: primary printed terrain texture, missing terrain and crop geometry. Settlements, facilities, hexsides, roads, railways and every compound terrain combination were not independently audited.',
    '- Geometry/completeness flag counts: `'+json.dumps(dict(flags))+'`. Region/playability flags are exclusions for training, not automatic evidence that a saved hex is invalid. Some derived references disagree with the printed number; retain stable keys and review canonical region assignment.', '',
    '## Proposed terrain corrections', '',
    'UICFB p4 Terrain Key distinguishes small Steppe grass tufts, Swamp reeds/horizontal strokes, and blue Lakes specks. Blue alone is not sufficient evidence of Swamp. For the prototype, “marsh” is treated as editor Swamp; Salt Marsh remains separate pending confirmation. Coastal land components and the project’s >20% convention need human adjudication where marginal.', '',
    '| Stable key | Derived reference | Current | Proposed land texture | Original-pixel crop |',
    '| --- | --- | --- | --- | --- |']
    for z in audit['terrain_proposals']:
        crop=Path(z['source']).name
        lines.append(f"| {z['key']} | {z['reference']} | {z['current']} | {z['proposed']} | [crop](crops/{crop}) |")
    lines += ['', 'These 31 proposals include 26 Steppe, three Lakes and two Swamp cases. They are saved-label/source disagreements, not measured model errors. Inspect audit-01.png (Clear/Steppe and Lakes examples) and swamp-seed-candidates.png (Swamp detail). No proposals have been applied.', '',
    '## Prototype and results', '',
    '- Python/PySide6 reads original boards through the existing hex geometry. Twenty NumPy features describe RGB quantiles, blue/green/dark coverage, native-pixel gradients at 1/2/4 pixels and short/long ink runs. This preserves fine printed marks and is easier to inspect than a large learned model.',
    '- Standardized nearest-class centroids were fitted to 8 Clear, 11 Steppe and 7 Swamp visually reviewed seed crops. These labels are isolated from live Verified statuses. The seeds are geographically narrow and may miss other board palettes.',
    '- Map 9 is reserved for evaluation before label collection/tuning; fresh Map 6 and Map 9 crops use a 500-pixel board-edge margin. No augmentations. Neighboring hexes from the evaluation board cannot enter training. Existing seed crops are from other boards.',
    '- Per-class held-out counts: Clear 0, Steppe 0, Swamp 0. Recall/precision and model error examples are **not yet available**. No training accuracy is offered as a substitute. A neural classifier is deferred until sufficient reviewed training and held-out examples exist.',
    '- suggestions.json contains stable board/region/column/row keys, derived printed references, relative centroid scores and review flags. All suggestions require review. Water, geometry and feature-distance exclusions can produce no suggestion. Scores are not calibrated correctness probabilities and must not be compared with the counter 95% threshold.',
    '- A 72-crop human queue includes 24 existing informative cases and 24 fresh cases on each of Map 6 and Map 9. Use Other/Mixed/Unsure rather than forcing forest, relief, lakes or ambiguous coastlines into the three classes.',
    '- Human labeling time is recorded, but this first workflow shows no predictions to avoid anchoring initial labels. Suggestion-correction versus manual timing has not been measured; an equivalent randomized follow-up batch is required.', '',
    '## Run from the project root', '',
    '```powershell',
    '.venv/Scripts/python.exe -m audit_tools.terrain alignment',
    '.venv/Scripts/python.exe -m audit_tools.terrain export',
    '.venv/Scripts/python.exe -m audit_tools.prepare_terrain_review',
    '.venv/Scripts/python.exe -m audit_tools.terrain_baseline',
    '.venv/Scripts/python.exe -m audit_tools.terrain_labeler',
    '.venv/Scripts/python.exe -m audit_tools.report_terrain',
    '.venv/Scripts/python.exe -m unittest audit_tools.test_terrain_tools',
    '```', '',
    'Export/preparation regenerate derived audit files in this dated directory; archive the directory before refreshing against edited source maps. Human answers are kept separately in human_labels.json and are not reset by preparation. Baseline reruns consume those answers; Map 9 answers remain evaluation-only.', '',
    '## Manual checks / needed input', '',
    '1. Launch the labeler; compare a few crops with the matching original board, then answer the 72 examples. Pixelated 4× display is intentional: no smoothing hides tiny marks.',
    '2. Close/reopen to confirm answers persist. Labels are in the audit directory, not map_terrain.json.',
    '3. Confirm that “marsh” should mean Swamp, with Salt Marsh separate, and review the 31 proposed corrections before applying anything.',
    '4. Rerun the baseline after labeling. Inspect held-out confusion/errors before collecting additional examples or selecting a neural model.',
    '', 'Tests: three focused tests passed (finite/separable baseline scores, temporary-file atomic persistence/backup, evaluation-board seed exclusion); all audit Python modules compile. Interactive labeling behavior has not been user-tested. No gameplay or transport rules implemented.']
    (ROOT/'REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    baseline=json.loads(Path('audits/20261109/counters/consistency.json').read_text())['protected_sha256']
    comparison={p:hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in baseline.items()}
    Path('audits/20261109/protected_data_check.json').write_text(json.dumps(comparison,indent=2))
    assert all(comparison.values()),comparison
    print('Protected data unchanged',comparison, 'water screen flags',len(water))
if __name__=='__main__': main()
