# Counter editor format review — 2026-10-30

Added the missing printed-metadata layouts and completed the existing transcriptions where supported. **706 definitions updated: 452 newly Verified and 254 still In progress.** Overall: **4,983 Verified / 1,985 In progress / 0 Unreviewed**. All **6,262 other definitions** remain unchanged, including every previously Verified definition.

## Editor changes and references

| Layout or field | Behavior and reference |
|---|---|
| Movement only | Records a printed movement value without requiring invented combat strength or HQ capacity. UICFB PDF p2. |
| Operational / code | Records OP/ST and any printed capacity/radius. Does not require movement or label an alternate Reduced. R16a 14.B.8, printed p102 / PDF104; 15, printed pp113-116 / PDF115-118. |
| Fortification level | Records the actual printed UR level. R16a 4.A.5, printed p20 / PDF22. |
| Coastal defense | Level is the core field; short/long components are optional when unprinted. In 3/2, level=3, printed short component=3, long component=2. Preserve the full slash string as printed_rating. Effective short-range strength (3+2) and doubling are not calculated by this editor. R16a 4.A.3.a.i-ii, printed p19 / PDF21; UICFB PDF p2. |
| CD additional code | Exposes the stored code. Rechecked V symbols recorded as torpedoes Present. R16a 4.A.3.a.iv, printed p19 / PDF21; UICFB PDF p2. |
| Submarine patrol range | SSF requires patrol range rather than printed tactical speed. No rule-defined speed is inserted into counter artwork metadata. R16a 5.C.2.e.ii-iii, printed p32 / PDF34. |
| FAS printed bottom-right | Requires the literal printed value, without assigning an unsupported gameplay meaning or requiring tactical speed. R16a 5.C.4, printed p33 / PDF35. |
| Commander header/lower line | Exposes stored literal markings. Unprinted optional modifiers can remain blank; the key says they have no effect. UICFB PDF p2. |
| Other printed markings | Exposes literal ground ratings/codes and additional values inside symbols. Unresolved markings do not become interpreted automatically. |

**Source conflict retained:** R16a 4.A.3.a.i describes CD levels 1–8, while VASSAL artwork includes higher values. The user selected VASSAL as the working artwork reference. Printed values are preserved; no range cap or gameplay ruling was added.

R16a 5.A.2, printed p25 / PDF27 also explains parenthesized combat values. The editor keeps `(1)` literally; it is not reclassified automatically as defense-only. No arithmetic or gameplay effects were implemented.

## Data review

Applied dedicated layouts to **404 movement-only faces**, **80 OP/ST faces** and **100 fortified-region faces**. Exposed already-transcribed submarine ranges, FAS literal values and commander markings. Revisited **195 CD faces**; **34 slash-value faces** now have separate level/printed components with the original complete text preserved. Existing values, unknown fields, IDs, face artwork, shared identification and physical-review evidence were retained. No new counter pairing, blank-back inference, catalog repair or artwork modification occurred.

Rechecked **652 artwork faces for 452 eligible counters** on 16 labeled contact sheets. Those counters already had accepted physical pairing/blank evidence; their remaining layout blockers were resolved by the references and artwork. Newly Verified: **379 ground, 71 naval, 2 commanders**. Confidence remains a review judgment, not a measured probability.

The other **254 changed profiles** retain physical matching/variant, identification or other issues and remain In progress. Their layout edits reuse existing literal transcriptions and do not claim a new visual/physical verification. The isolated static-AA value on **Baku (239005)** was excluded from migration because its meaning remains uncertain. Photo-question discrepancies remain in [COUNTER_VASSAL_DISCREPANCIES.md](COUNTER_VASSAL_DISCREPANCIES.md).

Historical notes/issues and the preceding batch review are preserved in each changed definition's `editor_format_review`. Current displayed issue lists were refreshed. The per-entry audit, artwork/reference fingerprints and validation are in [the batch report](counter_batches/editor_formats_20261030.json).

## Recovery and validation

Recovery copy: `assets/counters/recovery_snapshots/before-editor-formats-20261030.zip`. Its definition bytes were checked against the input. The normal timestamped backup was also checked after the atomic save.

**77 project tests passed**, with **53 relevant tests repeated after final changes**. **706 temporary editor save/reload checks** verified persistence, extra/unknown-field retention, statuses and backup behavior. All **6,968 staged definitions** also loaded in an isolated fixture without changing the file or statuses. Existing older shared ground-format compatibility tests pass. Automated persistence checks never saved to live data; the final authorized application used the existing atomic writer. Source PDF/artwork hashes and protected catalog/map/main files were checked unchanged. Interactive GUI testing remains for the user. No commit/push.

## Short manual checklist

Restart the editor before saving, so an old session cannot overwrite the updated data. Clear review/search filters.

1. **Artillery HQ 301 (235689):** Verified, Movement only, movement 20; confirmed blank back.
2. **Supply Terminal ST (237877):** Verified, front ST / back OP, using Operational / code; no invented movement ratings.
3. **Trondheim (236052):** Verified, front level 18, printed components 18 / 2, full text `Level 18/2`, torpedoes Present; printed alternate retained.
4. **Type IIB/1 (237742):** Verified, patrol range 12 on both faces; tactical-speed field hidden. **R-1 (237706):** Verified, literal bottom-right 4; no tactical speed inferred.
5. **Mannerheim (237880):** Verified; header/lower-line text visible and existing numeric modifiers preserved. **Fortified Region 1 (241253):** level fields 1 / 3 visible; remains In progress for its unresolved physical match.

Use Check Definition on these examples. If you choose to edit an example, save/reopen it and confirm the selected face format, literal values and status persist. Unknown images/pairings must still prevent Verified saving and offer Return to Editing or Save as In Progress.
