"""Editable control roster from UICFB, PDF p3 (National Colour Identifiers).

These are chart force groupings, not date-dependent political allegiance.
Service branches are grouped under their nation. Inter Allied is explicitly
a control grouping, not a sovereign nation. The key supplies no neutral list.
"""
from copy import deepcopy

_ROSTER = [
    ("germany", "Germany", "axis", ["German"]),
    ("italy", "Italy", "axis", ["Italian"]),
    ("slovakia", "Slovakia", "axis", ["Slovak", "Slovakian"]),
    ("hungary", "Hungary", "axis", ["Hungarian"]),
    ("bulgaria", "Bulgaria", "axis", ["Bulgarian"]),
    ("romania", "Romania", "axis", ["Romanian", "Rumania", "Rumanian"]),
    ("spain", "Spain (chart forces)", "axis", ["Spain", "Spanish"]),
    ("finland", "Finland", "axis", ["Finnish"]),
    ("uk", "United Kingdom", "allied", ["British", "Britain", "UK"]),
    ("canada", "Canada", "allied", ["Canadian"]),
    ("australia", "Australia", "allied", ["Australian"]),
    ("new_zealand", "New Zealand", "allied", ["New Zealander"]),
    ("poland", "Poland", "allied", ["Polish", "Free Polish"]),
    ("usa", "United States", "allied", ["American", "United States of America", "USA", "US"]),
    ("norway", "Norway", "allied", ["Norwegian", "Free Norwegian"]),
    ("france", "France (Free French)", "allied", ["France", "French", "Free French"]),
    ("greece", "Greece", "allied", ["Greek", "Free Greek"]),
    ("ussr", "Soviet Union", "allied", ["Soviet", "USSR", "The Soviet Union"]),
    ("inter_allied", "Inter Allied (control group)", "allied", ["Inter Allied", "Inter-Allied"]),
]


def initial_roster():
    return deepcopy([{"nation_id": uid, "name": name, "allegiance": side, "aliases": aliases,
                      "kind": "control_group" if uid == "inter_allied" else "nation",
                      "source": {"document": "UICFB.pdf", "pdf_page": 3}}
                     for uid, name, side, aliases in _ROSTER])
