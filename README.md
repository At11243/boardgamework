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
