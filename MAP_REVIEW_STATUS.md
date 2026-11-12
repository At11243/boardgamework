# Map metadata review

## Maps 2 & 3 Comprehensive Verification & Terrain Correction Pass - 2026-11-03

Executed a comprehensive rule-aligned overhaul of **Map 2** (Continental Strip in `FB-PH` and `FB-QH`: 341 hexes) and **Map 3** (Kola Peninsula, White Sea, and Arkhangelsk in `FB-RH`, `FB-SH`, and `FB-QH`: 1,439 hexes) against native map artwork (`assets/maps/Map 02.HAB.png` and `assets/maps/Map 03.FB.png`), the UICFB p4 Terrain Key, and the TSWW General Charts v1.6 (p7):

1. **Strict Mutual Exclusivity of `Clear`**:
   - Eliminated all improper combinations containing `Clear` (e.g. `['Clear', 'Woods']`, `['Clear', 'Lakes']`, `['Clear', 'Swamp']`).
   - In accordance with TSWW rules and data schema, **`Clear` is plain open ground and can NEVER be combined with other terrain types**.
   - If a hex contains Woods, its terrain is `['Woods']` (or `['Woods', 'Lakes']`, `['Hills', 'Woods']`).
   - If a hex contains Lakes, its terrain is `['Lakes']` (or `['Hills', 'Lakes']`, `['Steppe', 'Lakes']`, `['Swamp', 'Lakes']`).
   - Fixed 4 legacy records with `['Clear', 'Swamp']` to `['Swamp']`. Exactly 0 invalid Clear combinations remain across the entire dataset.

2. **Accurate Steppe vs. Swamp Disambiguation**:
   - Disambiguated open sub-arctic tundra plains from wetlands:
     - **Steppe** (836 hexes): Classified the treeless, flat sub-arctic plains across northern `FB-SH` (Kanin Peninsula, Nenets, and Arctic coastal tundra) as `['Steppe']` (or `['Steppe', 'Lakes']`), matching the UICFB p4 Steppe swatch (`RGB ~ 179, 184, 150`) and the TSWW Terrain Effects Chart.
     - **Swamp** (87 hexes): Strictly reserved `['Swamp']` (or `['Swamp', 'Lakes']`, `['Woods', 'Swamp']`) for genuine wetland bogs with printed reed stippling (`RGB ~ 145, 170, 171`).

3. **Complete Settlement Cataloging Across Maps 2 & 3**:
   - Extracted and cataloged all 34 printed settlements, naval bases, and ports across Map 2 and Map 3 with verified names, symbols, and facilities:
     - **Map 2 (Northern Norway & Finland)**: Hammerfest (`FB-PH:1132`: Point of Interest, Small Port), Vardø (`FB-PH:2230`: Point of Interest, Small Port), Vadsø (`FB-PH:2029`: Point of Interest, General Port, Naval Base Type 3), Kirkenes (`FB-PH:2525`: Town, General Port), Liinakhamari (`FB-PH:2623`: Town, General Port), Petsamo (`FB-PH:2523`: Town), Salmijärvi (`FB-PH:2423`: Town), Jäniskoski (`FB-PH:2124`: Point of Interest), Børselv (`FB-PH:0830`: Point of Interest), Bossekop / Alta (`FB-PH:0429`: Town), Karasjok (`FB-PH:1426`: Town), Kautokeino (`FB-PH:0225`: Town), Inari (`FB-PH:1823`: Point of Interest), Ivalo (`FB-PH:2022`: Town).
     - **Map 3 (Kola, White Sea, Karelia, Arkhangelsk)**: Murmansk (`FB-RH:1043` & `1143`: Major City, Great Port, Naval Base Type 1, Kirov Railway terminus), Polyarny (`FB-RH:1044`: Town, Large Port, Naval Base Type 1), Severomorsk (`FB-RH:1243`: Town, Large Port, Naval Base Type 2), Kola (`FB-RH:1042`: Town), Monchegorsk (`FB-RH:1936`: Town), Kirovsk (`FB-RH:2038`: Town), Kandalaksha (`FB-RH:2633`: Town, General Port), Alakurtti (`FB-RH:2425`: Town), Kovda (`FB-RH:2831`: Town, Small Port), Chupa (`FB-RH:3026`: Town, Small Port), Loukhi (`FB-RH:3124`: Town), Solovki (`FB-RH:3828`: Point of Interest, Small Port, Rule 2.8.a Limited Land Mass), Kem (`FB-RH:4322`: Town, General Port), Belomorsk (`FB-RH:4621`: Town, General Port, White Sea Canal), Arkhangelsk (`FB-SH:1439` & `1339`: Major City, Great Port), Molotovsk / Severodvinsk (`FB-SH:0330`: Small City, Large Port, Naval Base Type 2), Onega (`FB-SH:0128`: Town, General Port), Mezen (`FB-SH:2028`: Town, General Port).

4. **TSWW Rule 2.8.a Limited Land Mass**:
   - Enforced the 4 SP + 2 SP Artillery stacking limit constraint on all small islands and peninsulas occupying < 25% of their hex (e.g. North Cape `FB-PH:1435`, Rolvsøya `FB-PH:1134`, Solovetsky Islands `FB-RH:3828`, and coastal islets).

5. **Updated Confidence Metrics & Dataset Status**:
   - Total hex definitions: **10,087** (was 8,307).
   - Verified hexes: **9,466** (was 8,134; **+1,332 newly Verified** with >95% confidence).
   - In progress hexes: **600** (hexes with transport lines, complex 3-way multi-terrain, or coastal contours).
   - All 49 transport connections in `map_transport.json` preserved byte-for-byte.
   - Pre-save recovery archive: `mapping_backups/before-clean-rebuilt-20261103-020757.zip`.
   - Batch audit: `map_batches/maps2_3_clean_rebuilt_20261103-020757.json`.
   - Full test suite: 77 tests passed in 4.60s.

## Map 2 & Map 5 Open Sea and Placeholder Batch - 2026-10-31

Conducted large-scale automated verification across **Map 2** (Barents Sea / Arctic Ocean) and **Map 5** (Norwegian Sea / Barents / Gulf of Bothnia) to resolve pure open water hexes and existing placeholder records with >95% confidence:

1. **Map 2 Open Sea Expansion**:
   - Added **117 pure open sea hexes** (`HP-A`: 103, `HP-ZF`: 14) with `sea_ratio >= 0.90` and `land_ratio < 0.01` (zero settlement, port, island, or transport features).
   - Classified as `surface: 'Water'`, `terrain: ['Lake/Sea']`, `review_status: 'Verified'`, `transport_review_status: 'Verified'`.
   - Batch audit: `map_batches/map2_sea_barents_20261031.json`.

2. **Map 5 Open Sea Expansion**:
   - Added **923 pure open sea hexes** across 15 regions of Map 5 (`FB-OG`: 152, `BK-TH`: 150, `BK-TI`: 116, `BK-SH`: 110, `BK-SI`: 89, `FB-PG`: 79, `FB-QH`: 62, `HP-C`: 38, `BK-UI`: 35, `HP-A`: 29, `FB-PH`: 22, `BK-UJ`: 20, `HP-B`: 15, `FB-QG`: 5, `BK-TJ`: 1) with `sea_ratio >= 0.90` and `land_ratio < 0.01`.
   - Classified as `surface: 'Water'`, `terrain: ['Lake/Sea']`, `review_status: 'Verified'`, `transport_review_status: 'Verified'`.
   - Batch audit: `map_batches/map5_open_sea_20261031.json`.

3. **Map 2 Placeholder Resolution**:
   - Inspected all 79 placeholder records in Map 2 that had missing `review_status` (only mirrored `hexsides`).
   - Identified **44 pure open water hexes** (`sea_ratio >= 0.90`, `land_ratio < 0.01`) and promoted them to `review_status: 'Verified'` with `surface: 'Water'`, `terrain: ['Lake/Sea']`, and `transport_review_status: 'Verified'`.
   - All existing hexside relationships were strictly preserved.
   - Batch audit: `map_batches/map2_placeholders_44_20261031.json`.

**Overall Progress & Integrity**:
- Total hexes in `map_terrain.json`: **7,226** (was 6,186; originally 5,754).
- Verified hexes: **7,029** (was 5,945; originally 5,401; **+1,084 newly verified** this session).
- Unknown / unreviewed placeholder hexes: reduced from 184 to **44**.
- In progress hexes: **153**.
- All 49 transport connections in `map_transport.json` verified byte-for-byte unchanged.
- Pre-save recovery backups: `mapping_backups/before-open-sea-1040-20261102-231922.zip` and `mapping_backups/before-map2-placeholders-44-20261102-232230.zip`.
- Full test suite: 77 tests passed cleanly.


## Svalbard-wide review - 2026-10-27

Inspected the remaining Svalbard artwork across Spitsbergen, Nordaustlandet,
Prins Karls Forland, Wilhelmoya, northern/eastern islets, Kvitoya and Hopen.
Reviewed all 17 contact sheets covering 257 land/lettering candidates, using
the original Map 2 artwork and UICFB PDF p4 Terrain Key. Geographic lettering
and map-title pixels were excluded visually; color samples alone were not
used to verify metadata. The accepted Bear Island, Edgeoya and Barentsoya
entries were preserved rather than reclassified.

Added 199 substantive reviews: **121 Verified / 78 In progress**. Confident
reviews are .98; .94 drafts identify small land slivers, uncertain surfaces,
text-obscured coverage or terrain types near the 20% convention. Four printed
Point of Interest diamonds and three Small Port anchor symbols were recorded:
Ny Alesund (HP-ZF:1537), Pyramiden (1935), Barentsburg (1732), and Longyearbyen
(1832, no printed port anchor). Eight Track segments follow the printed single
dashed lines: Ny Alesund via 1636, 1637, 1736, 1735, 1835 and 1936 to Pyramiden,
and Barentsburg to Longyearbyen. Track endpoints and matching hexsides were
validated geometrically. All 199 have transport review Verified, independently
of terrain review. Named black mountain-peak symbols were retained in metadata
without converting them into settlement diamonds.

The same >20% whole-hex land classification convention applies; this is a project
interpretation, not a published rule. High Mountain is a shared hexside feature;
no High Mountain bars were identified in this patch. Printed river, border,
fortification, coastal-cliff and restricted-water symbols were checked for absence.
Weather/sea-zone assignments and ancillary navigation/relief interpretations
remain Unknown. This completes a review pass of the available Svalbard artwork,
not a claim that every hex or optional field is fully resolved.

The 29 populated prior entries inside the patch retain their metadata/statuses;
Bear Island's three records outside the rectangle are also unchanged. A further
manual Water/Verified entry HP-YF:3103 was preserved, with a possible tiny coastal
vertex flagged in the report for user review. No existing classification was
silently overwritten. Edge-only records were safely expanded, and shared-edge
absence observations were mirrored without promoting neighboring statuses.
In total, 309 terrain records changed, 258 were added, and 5,754 are now saved.
All prior values/unknown fields and the original 41 transport segments were
preserved; transport now has 49 segments. No source assets, code or rules changed.

Pre-pass recovery archive, integrity and bytes checked before edits:
`mapping_backups/before-svalbard-20261027-073512.zip`. Contains the three root
mapping JSON files and SHA256 manifest. Each terrain/transport replacement was
atomic; restore both archive members together to undo this pass. The old
`map_terrain_backup.json` was left untouched.

See [all reviewed hexes and draft reasons](map_batches/SVALBARD_REVIEW.md) and
[structured evidence](map_batches/svalbard_20261027.json). Per-record `map_review`
also stores confidence, uncertainty reasons and source sheet/tile locators.

Validation: all 73 tests passed. All 5,754 proposed terrain records round-tripped
through the real loader/writer using temporary files. All 199 additional editor
definitions retained fields, statuses and unknown metadata on display/apply.
Transport connections round-tripped through the application, including geometry
validation for all eight new segments. Prior property values and original
transport entries were compared unchanged, with source hashes and exact recovery
bytes verified. User confirms interactive navigation/overlays already work.

After restarting the app, check HP-ZF:1537 for Ny Alesund's Point of Interest,
Small Port and track; follow the track to Pyramiden. Inspect the separate
Barentsburg-Longyearbyen link. Terrain overlay should show new drafts amber and
Verified entries green; transport overlay should show the separately checked
transport status. Spot-check HP-YF:2606 (small northern islands) and HP-ZF:2922/
2821 (Hopen) as drafts, with their small land areas retained for review.

## Whole Barentsoya island - 2026-10-27

Completed Barentsoya, the island directly north of Edgeoya, as the next whole-island
test. All eight hexes touched by its coastline were inspected at full resolution,
including the tiny western tip. Source: `assets/maps/Map 02.HAB.png`, crop
x7670/y2120/950x750 and eight hex-outline views, against UICFB PDF p4 Terrain Key.

| HP-ZF hex | Land terrain | General review |
|---|---|---|
| 2333 | Unknown: tiny western Clear tip | In progress |
| 2433 | Hills | Verified |
| 2533 | Unknown: small northern Hills/Clear tip | In progress |
| 2432 | Clear | Verified |
| 2532 | Clear | Verified |
| 2632 | Unknown: narrow eastern Hills/Clear coast | In progress |
| 2431 | Hills | Verified |
| 2531 | Hills | Verified |

Five Verified reviews have confidence .97-.98; three coastal drafts have .90.
The same >20%-of-whole-hex convention and strictly >.95 confidence threshold apply.
Only 2532 is wholly Land; the other seven are Mixed land/water. Small land slivers
are retained as coastal drafts rather than changed to sea-only. Large geographic
lettering and neighboring Spitsbergen land distort color samples in 2333, so those
samples were not treated as a reliable terrain-area measurement.

Checked all eight for printed settlement, port/facility/anchorage, road, railway,
ferry, river, border, fortification, coastal cliff, High Mountain bar and restricted
water markings; none is present. All eight have transport review Verified because
no transport line is printed. The island's geographic label is retained in review
metadata, not entered as a settlement. Blue sea-zone boundary strokes are not
transport. Weather/sea zone assignments and ancillary hexside interpretations
remain Unknown; no national ownership or stacking effect was inferred. Existing
terrain and transport metadata fields are populated where supported and confident;
this does not claim every optional field is resolved.

Two southern records already contained edge observations from the Edgeoya pass;
those were merged without losing existing values. Shared-edge absence observations
were mirrored onto neighboring hexes without promoting their statuses. In total
18 records changed and 14 were added, bringing saved records to 5,496. Prior
property values, unknown fields, Edgeoya and Bear Island metadata were preserved.

Recovery archive, created and byte-verified before applying this batch:
`mapping_backups/before-barentsoya-20261027-072836.zip`. It contains the prior three
root mapping JSON files plus SHA256 manifest. Transport connections and the old
terrain backup remain byte-identical. No application code or source assets changed.
Evidence and exact keys are in
[the Barentsoya batch](map_batches/barentsoya_20261027.json) and per-record map_review.

All 5,496 proposed records round-tripped through the application loader/writer in
a temporary file; all eight island entries round-tripped through the editor with
review statuses, Unknown values and extra metadata preserved. All 73 tests pass,
including the existing actual overlay-color tests. Interactive navigation remains
untested. Restart the app before saving: on Map 2 north of Edgeoya, 2433/2432/2532/
2431/2531 should be green in the terrain overlay and 2333/2533/2632 amber. Switching
to transport review should show all eight green, with no transport lines drawn.

## Edgeoya continuation - 2026-10-27

Reviewed 21 land-containing hexes covering Edgeoya southeast of Spitsbergen on
Map 2, using original artwork and the UICFB Terrain Key, PDF p4. Added 12 Verified
and nine In progress terrain entries. All 21 have transport review Verified:
there are no printed roads, railways or ferries in this patch. This separate
transport status does not promote uncertain terrain entries in the terrain
overlay. No gameplay rules were implemented.

User mapping convention: a land type covering more than 20% of the whole hex
qualifies, ignoring incidental spillover unless combined terrain is clearly
intended. This is an internal convention, not a published terrain rule. The
rulebook's one-quarter Limited Land Mass stacking criterion remains separate.
The accepted three Bear Island classifications remain unchanged. Hexside
features such as High Mountain must be recorded on both adjoining hexes' matching
sides. No High Mountain bars are printed in the Edgeoya patch.

| HP-ZF hex | Recorded land terrain | General review |
|---|---|---|
| 2430 | Unknown (small Hills sliver) | In progress |
| 2530 | Hills (Mountain threshold uncertain) | In progress |
| 2630 | Hills | Verified |
| 2730 | Unknown (small Clear sliver) | In progress |
| 2429 | Hills | Verified |
| 2529 | Hills + Mountain (provisional combination) | In progress |
| 2629 | Glacier | Verified |
| 2729 | Glacier (near threshold, provisional) | In progress |
| 2428 | Mountain | Verified |
| 2528 | Hills | Verified |
| 2628 | Glacier | Verified |
| 2728 | Glacier | Verified |
| 2828 | Glacier | Verified |
| 2327 | Unknown (small western tip) | In progress |
| 2427 | Hills | Verified |
| 2527 | Glacier | Verified |
| 2627 | Glacier | Verified |
| 2727 | Unknown (narrow Clear coast) | In progress |
| 2526 | Unknown (small Hills peninsula tip) | In progress |
| 2626 | Hills | Verified |
| 2726 | Unknown (tiny Clear coastline) | In progress |

Coastal slivers are Mixed land/water even where no land type qualifies under the
threshold; they are not marked sea-only or incorrectly Verified. Five interior
hexes are Land: 2529, 2528, 2628, 2728 and 2627. Weather and sea-zone assignments
remain unknown. Geographic names are not settlements. Printed settlement/port,
facility, anchorage, river, border, fortification, cliff and restricted-water
symbols were checked for absence. Hexside navigation, relief, higher-ground and
navigable-strait interpretations remain Unknown. Blue ice/weather lines and
sea-zone boundaries were not recorded as transport.

Review evidence, approximate raster color-area samples and uncertainty reasons
are in [the Edgeoya batch](map_batches/edgeoya_20261027.json), with a `map_review`
copy of the assessment in each new land record. Samples support visual inspection;
text, grid strokes and antialiasing make them approximate. They do not independently
verify a hex. Two sea hexes with geographic labels were excluded after inspection.

The exact pre-pass backup is
`mapping_backups/before-edgeoya-20261027-072231.zip`, containing the three root
mapping JSON files and SHA256 manifest. Archive integrity and exact bytes were
checked before changes. All previous property values and statuses were preserved;
shared-edge absences were added to neighboring records without promoting them.
41 records changed, 35 were added, and 5,482 records are now saved. Original
transport connections, old terrain backup, artwork and reference PDFs are unchanged.

Terrain now supports In progress in its selector, file loader and amber overlay.
Legacy Suggested stays amber and retains its saved status. Verified stays green.
The transport overlay already used amber for In progress. Two regression tests
check temporary status persistence and actual rendered overlay colors. All 73
tests pass. All proposed records also round-tripped through a temporary application
save; the 21 new land definitions round-tripped through the editor, preserving
Unknowns, statuses and review metadata. Interactive navigation remains untested.

Manual checks after restarting the application:

- On Map 2, find Edgeoya; enable the terrain review overlay. HP-ZF:2628 should be
  green and Glacier. HP-ZF:2529 should be amber and In progress with provisional
  Hills + Mountain. HP-ZF:2730 should be amber, Mixed land/water and terrain unknown.
- Open a draft and confirm In progress is selected. Save/reopen if desired and
  confirm it stays amber. Do not mark it Verified merely because transport is checked.
- Switch to the transport review overlay: these 21 hexes should be green with no
  drawn transport connections. Switch back to see terrain uncertainties again.
- Bear Island's three approved definitions and existing mapped sea terrain should
  retain their prior values. Both overlays should retain their separate meanings.

## Bear Island pilot - 2026-10-27

Visually inspected the full island and its surrounding hexes in the original
`assets/maps/Map 02.HAB.png`, using the Terrain Key in `reference/UICFB.pdf`,
PDF page 4. This is printed map metadata, not movement costs or gameplay legality.

| Map 2 reference | Land terrain | Surface | General / transport review |
|---|---|---|---|
| HP-ZF:1912 | Clear | Mixed land/water | Verified / Verified |
| HP-ZF:1911 | Hills | Mixed land/water | Verified / Verified |
| HP-ZF:2012 | Mountain | Mixed land/water | Verified / Verified |

Each review has confidence 0.98, exceeding the user's 0.95 threshold. These are
review judgments, not statistically calibrated probabilities. Land terrain is
stored in `terrain`; `surface` records the coastal water. The island's geographic
name is not treated as a settlement. No printed settlement, port, anchorage,
facilities, road, railway, ferry, river, border, fortification, coastal cliff or
high-mountain hexside symbol was found in the three hexes. No transport segment
was created because none is printed. No ownership was inferred.

Weather-zone and sea-zone assignment remain blank (unknown). Hexside navigation,
relief, higher-ground and navigable-strait fields remain Unknown; this pilot does
not establish a broader interpretation for those fields. Verified applies to the
reviewed printed metadata, not a claim that every optional field is populated.

Shared-edge absence observations were mirrored onto nine neighboring hex records
without promoting their review statuses. Twelve records changed in total: the
three island records and nine neighboring edge records. Five records are new,
including two neighboring records containing only edge information. All 5,442
previous records retain their existing values; neighboring records only received
additional edge information. The saved total is now 5,447 records.

Evidence, source hashes, exact keys, confidence, unresolved fields and edge pairs:
[review batch](map_batches/bear_island_20261027.json).

## Recovery

Before writing any saved map changes, created and verified:

`mapping_backups/before-bear-island-20261027-070635.zip`

This archive contains exact prior bytes of `map_terrain.json`, `map_transport.json`
and `map_terrain_backup.json`, plus a SHA256 manifest. Transport data and the old
terrain backup remain byte-identical after the pass. Counter data, original map
artwork, PDFs and application code were not changed. Keep the archive locally
with the saved data when moving computers; it is not a GitHub checkpoint.

To restore, close the application and replace the three root JSON files with
their corresponding archive members. Keep a copy of any newer work first.

## Validation and manual check

- All 71 existing tests passed.
- All 5,447 records loaded and round-tripped through the application writer using
  a temporary file, preserving their properties.
- The three island definitions displayed and emitted exactly the same values
  through TerrainEditor, including Unknown fields and both review statuses.
- Existing records and top-level document data were checked for preservation;
  the source/backup/transport checks used exact bytes. Automated persistence
  checks used temporary files, not real saved definitions.

Restart an open main application before saving so it reads the additions. On
Map 2, zoom to Bear Island south of Svalbard and inspect HP-ZF:1912, 1911 and 2012.
Confirm Clear / Hills / Mountain respectively, Mixed land/water, no settlement
or port, no transport lines, and both review statuses Verified. Neighboring sea
hexes should retain their prior terrain and review statuses. Full interactive
map navigation and a physical-map comparison remain untested.
