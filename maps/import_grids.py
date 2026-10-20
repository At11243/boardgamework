from pathlib import Path
from pprint import pformat
from zipfile import ZipFile
import xml.etree.ElementTree as ET

from PySide6.QtWidgets import QApplication, QFileDialog

from maps.campaign_layout import barbarossa_boards 

def extract_grids(module_path):
    with ZipFile(module_path) as archive:
        root = ET.fromstring(archive.read("buildFile.xml"))

        expected_boards = {
            board_id : filename
            for board_id, filename, *_ in barbarossa_boards
        }

        grids = {}

        for board in root.iter():
            if not board.tag.endswith(".Board"):
                continue

            board_id = board.get("name")

            if board_id not in expected_boards:
                continue

            if board.get("image") != expected_boards[board_id]:
                raise ValueError(f"Unexpected image for {board_id}")

            regions = []

            for zone in board.iter():
                if not zone.tag.endswith(".Zone"):
                    continue

                hex_grid = next(
                    (
                        child for child in zone 
                        if child.tag.endswith(".HexGrid")
                    ),
                    None,
                )

                if hex_grid is None:
                    continue

                numbering = next(
                    (
                        child for child in hex_grid
                        if child.tag.endswith(".HexGridNumbering")
                    ),
                    None,
                )

                if numbering is None:
                    raise ValueError(
                        f"Missing numbering for {zone.get('name')}"
                    )

                boundary = [
                    tuple(map(int, vertex.split(",")))
                    for vertex in zone.get("path").split(";")
                ]

                regions.append({
                    "name" : zone.get("name"),
                    "boundary" : boundary,
                    "grid" : {
                        "dx" : float(hex_grid.get("dx")),
                        "dy" : float(hex_grid.get("dy")),
                        "x0" : float(hex_grid.get("x0")),
                        "y0" : float(hex_grid.get("y0")),
                        "sideways" : hex_grid.get("sideways") == "true",
                    },
                    "numbering" : dict(numbering.attrib),
                })

                grids[board_id] = {
                    "filename" : board.get("image"),
                    "regions" : regions, 
                }

        if set(grids) != set(expected_boards):
            raise ValueError("The extension does not contain all campaign boards.")

        return grids

if __name__ == "__main__":
    app = QApplication([])

    project_dir = Path(__file__).resolve().parents[1]

    filename, _ = QFileDialog.getOpenFileName(
        None,
        "Choose the Barbarossa maps extension",
        str(project_dir / "assets"),
        "VASSAL extensions (*.vmdx)",
        )

    if filename:
        grids = extract_grids(filename)

        #Use a separate output while we check the extraction.
        output_path = project_dir / "maps" / "campaign_grid_definitions.py"

        output_path.write_text(
            "# Extracted from the Barbarossa VASSAL maps extension.\n\n" + 
            "barbarossa_grids = "
            + pformat(grids, width = 100, sort_dicts = False)
            + "\n",
            encoding = "utf-8",
        )

        for board_id, data in grids.items():
            print(f"{board_id}: {len(data['regions'])} regions")

        print(f"Saved: {output_path}")

