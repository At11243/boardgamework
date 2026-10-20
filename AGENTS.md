# Development instructions

- You may edit project code and run relevant local checks. Use `.venv/Scripts/python.exe`.
- Make focused, incremental changes, explain their purpose, and provide concrete manual tests. Development is collaborative; clear explanations matter while learning TSWW.
- Preserve manually entered terrain, transport, and unit data, stable `type_id` identifiers, existing entries, and unknown fields.
- Use atomic saves and retain existing backup behavior.
- Do not rewrite reference PDFs, original artwork, or imported assets unless explicitly requested.
- Treat reference PDFs as sources. Cite page/rule numbers when implementing rules, and identify conflicting versions rather than silently choosing one.
- Distinguish implemented checks from rules still handled manually. Do not infer rules or ratings solely from filenames or assume mapped hexes/imported counters are verified.
- Blank ratings mean unknown; zero is a real value; N/A explicitly means not applicable. Alternate faces need not mean reduced strength. Older shared ground formats must load into both faces.
- Keep counter definitions separate from changing campaign-instance state. Generate blank reverses in code from stored color and front-image dimensions.
- Do not commit, push, or publish unless requested.
- Report what was tested and what remains untested. Automated persistence tests must use temporary data, never real saved definitions.
- Read PROJECT_CONTEXT.md for project priorities and confirmed examples. Keep gameplay, themes, and counter integration outside the focused unit-editor validation task.
