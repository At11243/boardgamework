# TSWW Barbarossa

Native Python/PySide6 companion. Run commands from the project root using the project's virtual environment.

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
