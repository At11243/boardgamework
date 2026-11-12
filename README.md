# TSWW Barbarossa

Native Python/PySide6 companion. Run commands from the project root using the project's virtual environment.

## Set up on another Windows computer

1. Install Git and Python (the current development environment uses Python 3.14). Sign into GitHub with an account that can access the private repository.
2. Clone the project:

   ```powershell
   git clone https://github.com/At11243/TSWW-Barbarossa.git
   cd TSWW-Barbarossa
   ```

3. Copy the **entire `assets` and `reference` folders** from the current computer into this project folder. They contain local artwork, the imported counter catalog, VASSAL source files, reference PDFs and backups that are not downloaded by Git. Keep the cloned `assets/counters/unit_definitions.json` if a copy operation asks about replacing it: Git contains the checkpointed definitions. Transfer any separately saved campaign JSON files too, if you use them.
4. Create a new virtual environment on the destination computer; do not copy the old `.venv`:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   .\.venv\Scripts\python.exe -B -m unittest discover -s tests -q
   .\.venv\Scripts\python.exe -m counters.unit_editor
   # Main map application:
   .\.venv\Scripts\python.exe main.py
   ```

5. In the IDE, select `.venv/Scripts/python.exe` as the interpreter. Check an existing Verified aircraft, its images, and the latest mapped terrain before entering more data.

Close the editor and main application before transferring or pulling data. When switching computers later, commit/push saved definitions and terrain changes on the computer you are leaving, then pull them on the other computer before opening the app. Local artwork/PDFs do not need recopying unless those files change.

```powershell
# Main application
.\.venv\Scripts\python.exe main.py

# Separate unit catalog editor
.\.venv\Scripts\python.exe -m counters.unit_editor
# Or run counters/unit_editor.py directly with your IDE's Run File button.

# All local tests (temporary fixtures, no real saved data)
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -v
```

## Code layout

```text
main.py                 Application entry point, docks and menus
maps/                   Map view, terrain editor, geometry, grids and mapping helpers
counters/               Counter browser/editor, instance state, face rendering, stack inspector
game/                   Action history, history panel and dice dialog
rules/                  UI-independent rules: DiceService and combat-result records
tests/                  Automated tests
assets/                 Original map/counter artwork and imported counter data
reference/              Rulebooks, charts and orders of battle
```

Terrain and transport JSON remain in the project root. Counter catalog, reviewed definitions and their backups remain under `assets/counters/`. Campaign-save formats and relative artwork paths are unchanged. `main.py` is the application entry point; the older root `rules.py` is retained, while active rules imports use the `rules/` package. The unit editor supports both direct-file and `-m` launching.

Reviewed/draft unit definitions are versioned. Original artwork, imported catalogs, reference PDFs, local backups, the virtual environment and temporary review artifacts stay local and are excluded from Git. Import the original counter module with `.\.venv\Scripts\python.exe -m counters.import_counters` when setting up a new checkout. Keep reference PDFs at the paths documented in `REFERENCE_SOURCES.md`.

Aircraft entry is complete: all 152 Luftwaffe aircraft have been user-verified; 284 additional aircraft have draft definitions awaiting review. See `AIRCRAFT_REVIEW_BATCH.md` for the remaining batch and unresolved compact type codes. Naval and ground transcription follows aircraft review.

Game > Players and Nations configures local teams (Axis × Allied), names and whole-nation assignments. Suggest Balanced Split counts placed instances with Verified nationality metadata; hover over the report for unknown/unreviewed IDs. The chart-derived roster is editable, including Neutral and added nations. Save the setup dialog, then save the campaign to persist it. Online/PBEM choices and AI mode configure assignments only; multiplayer transport, AI opponents, and control permissions are future work.


## Artwork-reviewed counter batches

The user has authorized assistant verification of clear entries. `counters.batch_review` automates validation, review status and safe addition of visually reviewed proposals. It does not perform unattended OCR or infer ratings from filenames. Existing manual and completed definitions remain protected; only unchanged, explicitly fingerprinted inventory placeholders may be promoted.

```powershell
# Preview only
.\.venv\Scripts\python.exe -m counters.batch_review counter_batches/german_infantry_01.json
# Apply the reviewed batch with atomic saves and timestamped backups
.\.venv\Scripts\python.exe -m counters.batch_review counter_batches/german_infantry_01.json --apply
```

Each proposal records identity/front/back review evidence and artwork SHA-256 fingerprints. New entries become Verified only when these reviews are complete, all assigned artwork is fingerprinted and linked to that catalog entry, no issues remain, and the real editor's completeness checks pass. Other new entries stay In progress with reasons in notes and `batch_review` metadata. Changed artwork aborts the batch; concurrent definition changes abort the write. This verifies counter metadata, not gameplay legality.

The first pilot added 24 German infantry divisions (IDs 236439-236462) as assistant-Verified. Per-face combined/separate ratings were inspected independently. All 439 existing definitions were preserved. Restart an open editor before saving after batch additions. Reapplying a batch skips existing IDs. Evidence is retained in `counter_batches/german_infantry_01.json`.


Full-catalog follow-up: see `COUNTER_REVIEW_STATUS.md` for exact scope and recovery instructions. Another 367 infantry entries are assistant-Verified; one reviewed Sturm exception and 6,137 explicitly untranscribed catalog queue entries are In progress. This is not full-catalog OCR or completed transcription. The latest batch policy requires identity/front/back confidence strictly greater than 95%; confidence is recorded review judgment, not a calibrated statistical guarantee. Existing manual/completed definitions remain protected, and opening the editor does not change review statuses.


The subsequent 500-counter Soviet infantry batch is fully transcribed: 495 Verified and five specific printed-marking questions In progress. Current totals and recovery details are at the top of `COUNTER_REVIEW_STATUS.md`. Queue-placeholder replacement is now supported only with an explicit matching record fingerprint and checks that no manual ratings, identity or artwork assignments have been added. Manual and Verified records remain protected. Such queue-promotion proposals are single-use and refuse reapplication after the records have changed; the original add-only pilot still skips existing IDs. Evidence is retained in `counter_batches/soviet_infantry_500_20261025.json`.


Previous 1,000-counter ground batch: 914 assistant-Verified and 86 transcribed drafts with specific questions. Current totals are 2,038 Verified, 4,927 In progress and 3 Unreviewed; 4,637 records remain untranscribed queue placeholders. See the top of `COUNTER_REVIEW_STATUS.md` for the recovery archive, exact review questions and manual checks. Evidence: `counter_batches/ground_1000_20261025.json`. Restart an open editor before saving.


Previous batch (1000b) transcribed another 1,000 entries: 82 assistant-Verified and 918 In progress. At the user's request, all 809 single-image entries use generated blank reverses by default and stay In progress; physical backs are unconfirmed.

Previous batch (1000c) transcribed 156 naval pairs, three aircraft pairs and 841 single-image ground fronts: 86 assistant-Verified and 914 In progress. All single-image entries retain In progress. Submarine patrol-range and unresolved FAS numbers remain separate from tactical speed.

The remaining-queue pass assessed 2,637 entries: seven aircraft-factory markers Verified and 2,630 In progress. Current totals: **2,213 Verified / 4,752 In progress / 3 Unreviewed**. Available artwork was transcribed for 2,604 entries; **33 unresolved-artwork records** remain untranscribed. All 2,512 single-image records retain In progress with generated blank defaults. Another 85 records have recovered original appearance references stored as provisional fronts and `appearance_candidates`; catalog-link/multi-appearance review remains necessary. See the top of `COUNTER_REVIEW_STATUS.md` for recovery details, exceptions and manual checks. Restart an open editor before saving.
