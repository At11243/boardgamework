presence = ["Unknown", "Absent", "Present"]

hex_options = {
    "port_fortification" : (
        "Printed port fortification",
        presence,
    ),
    "rocky_coast" : (
        "Rocky coast",
        presence,
    ),
    "reefs" : (
        "Reefs",
        presence,
    ),
    "restricted_waters": (
        "Restricted waters", 
        presence,
    ),
}

hex_text_fields = {
    "weather_zone": "Printed weather zone reference",
    "sea_zone" : "Printed sea zone reference",
}

side_options = {
    "relief": (
        "Hill / mountain hexside",
        [
            "Unknown",
            "None",
            "Hill",
            "Wooded Hill",
            "Mountain",
            "Wooded Mountain",
        ],
    ),
    "higher_ground" : (
        "Higher side of escarpment / cliff",
        [
            "Unknown",
            "Level",
            "This hex",
            "Neighbor hex",
        ],
    ),
    "navigable_straight": (
        "Navigable strait",
        presence,
    ),
}

def validate_extra_fields(properties):
    for field, (_, options) in hex_options.items():
        if properties.get(field, "Unknown") not in options:
            raise ValueError(f"Invalid map field: {field}")

    for field in hex_text_fields:
        if not isinstance(properties.get(field, ""), str):
            raise ValueError(f"Invalid map text field: {field}")

    for values in properties.get("hexsides", {}).values():
        for field, (_, options) in side_options.items():
            if values.get(field, "Unknown") not in options:
                raise ValueError(f"Invalid hexside field: {field}")
                          