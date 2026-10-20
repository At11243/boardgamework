# Remaining aircraft review batch

The earlier Luftwaffe batch is complete: all 152 Luftwaffe aircraft definitions are user-Verified, including the original manually entered aircraft. Stale assistant review notes have been cleaned without changing ratings, identities or review statuses. Croat/Estonian contingent nationality is Germany, with their respective Luftwaffe service labels; Spanish aircraft remain Spain / Luftwaffe. Gliders use the user-approved reduced Squadron interpretation and blank reverses. The two -1 tug modifiers remain a documented provisional rules interpretation. The obsolete separate Luftwaffe review checklist has been removed.

Added all **284 previously undefined aircraft catalog entries** as **In progress**, with front/back ratings visually transcribed from the original images. All 155 pre-existing definitions, their review statuses, unknown fields and top-level metadata were preserved. No ground/naval definitions or original artwork were changed. No aircraft entries in the catalog's Air palettes remain without a definition; human review is still required.

| Group | Added |
| --- | ---: |
| Soviet Union | 139 |
| Romania | 52 |
| Hungary | 25 |
| Finland | 17 |
| Bulgaria | 13 |
| Royal Air Force | 11 |
| Royal Navy aircraft | 11 |
| Slovakia | 6 |
| Italian Air Force | 4 |
| United States Navy aircraft | 4 |
| United States Army Air Forces | 2 |
| Total | 284 |

Soviet nationality is Soviet Union, with separate VVS, PVO, ADD, Guards and VMF service labels. The imported VVF prefix is preserved in source notes; service wording follows VVS in UICFB p3. British nationality is United Kingdom, with Royal Air Force/Royal Navy services; American nationality is United States, with the respective services. Other national air forces retain their own nationality and service. Existing German/Luftwaffe contingent records were not changed.

Both artwork faces were inspected separately. Printed codes, capacities, zero values and fractional symbols are retained literally, including ratings that differ between nations or do not halve exactly. Ordinary pairs use a Wing front and Squadron back, following v1.6a 5.B.1 (printed p28 / PDF p30); size/status text stays blank where no such text is printed. Type terminology and descriptors follow 5.B.3; colour/service identification uses UICFB p3. This is metadata transcription, not gameplay calculation or an automatic verification feature.

## Review exceptions

These four entries have complete literal ratings/codes but **Unknown general Unit type**. Their compact R combinations need interpretation; no dual-role slash or rocket descriptor was invented:

| ID | Catalog entry | Literal code |
| --- | --- | --- |
| vassal:133:237773 | BU BR KB-6 L.FB | BR |
| vassal:133:237991 | HU RB Mxd R-1.FB | RB |
| vassal:133:237992 | HU RB Mxd R-2.FB | RB |
| vassal:133:238000 | HU RA WM-21 L.FB | RA |

Two entries have the full-strength image **first** in the catalog/review sheet, rather than second: Romanian Me109F2 (238404) and Royal Navy Albacore (242044). Their definitions assign the inspected full-strength artwork as front and the reduced artwork as back. The Romanian Me109F2's missing comma-separated image references were repaired in the existing catalog using the previously fixed importer resolver; all other catalog records and metadata were preserved.

## Manual checklist

1. **Close and reopen the editor before further saves.** An already-running editor holds the pre-batch definitions in memory.
2. Filter to In progress and work through one nation's aircraft at a time. Compare both images, all printed ratings/codes and front/back sizes before marking Verified.
3. Spot-check the Romanian Me109F2 and Royal Navy Albacore face assignments, transport capacities, and differences between Soviet service variants.
4. Resolve the four compact-code general types above before verifying them. Check Definition checks metadata completeness, not historical accuracy or rule interpretation.

## Validation and backups

- All 284 drafts opened as In progress in an offscreen editor against temporary data. Opening did not change persisted records or statuses.
- Completeness checks identified exactly the four expected Unknown general types.
- Eight representative editor saves/reloads against temporary data preserved every transcribed rating, including zero/fractional values, capacities and unusual face order.
- All 61 existing tests passed. Automated persistence checks used temporary definitions and images only.
- The authorized final addition used the existing atomic writer and timestamped backup. Every prior definition and top-level metadata field was compared unchanged; the backup matched the exact pre-write file.
- The catalog image-link repair used an atomic replacement and exact backup check.

Definitions backup: `assets/counters/unit_definition_backups/unit-definitions-20261020-060220-287049.json`.

Catalog backup: `assets/counters/catalog_backups/counter-catalog-20261020-060220-681020.json`.

Temporary manual transcriptions, contact sheets and validation reports were removed after the saved drafts and this review summary were checked. Original artwork and local data backups are retained. Interactive visual review and gameplay behavior remain untested. No application code or artwork was changed for this batch.
