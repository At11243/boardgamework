import hashlib
import json
import re
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMessageBox,
)

def clean_label(value): 
    return re.sub(r",[^>]*>", "", value or "").strip()


def referenced_image_names(definition, images):
    """Resolve single images and comma-separated VASSAL appearance lists."""
    possible = re.findall(
        r"[^;\\\t\r\n]+\.(?:png|jpg|jpeg|gif|bmp)",
        definition, flags=re.IGNORECASE,
    )
    names = []
    for value in possible:
        # Prefer exact names so filenames containing commas still work.
        candidates = [value] if value in images else value.split(",")
        for name in candidates:
            if name in images and name not in names:
                names.append(name)
    return names


def extract_counters(module_path, project_dir):
    output_dir = project_dir / "assets" / "counters" 
    image_dir = output_dir / "images"
    image_dir.mkdir(parents=True, exist_ok = True)

    with ZipFile(module_path) as archive:
        root = ET.fromstring(archive.read("buildFile.xml"))

        image_members = {
            name.removeprefix("images/"): name
            for name in archive.namelist()
            if name.startswith("images/")
            and not name.endswith("/")
            and Path(name).suffix.lower() in (
                ".png", ".jpg", ".jpeg", ".gif", ".bmp"
            ) 
        }

        images = {}

        for original_name, member in image_members.items():
            #Safe filenames, independent of archive paths. 
            image_id = hashlib.sha256(
                original_name.encode("utf-8")
            ).hexdigest()[:20]

            extension = Path(original_name).suffix.lower()
            destination = image_dir / f"{image_id}{extension}"

            destination.write_bytes(archive.read(member))

            images[original_name] = (
                destination.relative_to(project_dir).as_posix()
            )

        counter_types = {}
        unresolved = []

        def visit(element, palette):
            current_pallete = list(palette)

            if element.tag.endswith((
                ".TabWidget",
                ".PanelWidget",
                ".ListWidget",
            )):
                label = clean_label(element.get("entryName"))

                if label:
                    current_pallete.append(label)

            if element.tag.endswith(".PieceSlot"):
                piece_id = element.get("gpid")

                if not piece_id:
                    raise ValueError(
                        "A counter definitoin is missing its VASSAL ID."
                    )

                type_id = f"vassal:{piece_id}"

                if type_id in counter_types:
                    raise ValueError(
                        f"Duplicate counter definition: {type_id}"
                    )

                definition = element.text or ""

                image_names = referenced_image_names(definition, images)

                counter_types[type_id] = {
                    "type_id" : type_id,
                    "vassal_piece_id" : piece_id,
                    "name" : clean_label(element.get("entryName")),
                    "palette" : current_pallete,
                    "image_names" : image_names,
                    "image_paths" : [
                        images[name] for name in image_names
                    ],
                    "vassal_definition" : definition,
                    "identification_status" : "Unreviewed",
                }

                if not image_names:
                    unresolved.append(type_id)

            for child in element:
                visit(child, current_pallete)

        visit(root, [])

    catalog = {
        "format" : "tsww-barbarossa-counter-catalog",
        "version" : 1,
        "source_module" : Path(module_path).name,
        "images" : images,
        "counter_types" : counter_types, 
        "unresolved_image_references": unresolved,
    }

    catalog_path = output_dir / "counter_catalog.json"
    temporary = catalog_path.with_name(
        catalog_path.name + ".tmp"
    )                

    try:
        temporary.write_text(
            json.dumps(catalog, indent = 2, ensure_ascii = False),
            encoding = "utf-8",
        )
        temporary.replace(catalog_path)
    finally:
        if temporary.exists():
            temporary.unlink()

    return catalog_path, catalog

def main():
    app = QApplication([])
    project_dir = Path(__file__).resolve().parents[1]

    filename, _ = QFileDialog.getOpenFileName(
        None,
        "Choose the Barbarossa counters extension",
        str(project_dir / "assets"),
        "VASSAL extensions (*.vmdx)",
    )

    if not filename:
        return 

    try: 
        path, catalog = extract_counters(
            filename, project_dir
        )
    except Exception as error:
        QMessageBox.critical(
            None,
            "Counter import failed",
            str(error)
        )
        return 

    message = (
        f"Images: {len(catalog['images'])}\n"
        f"Counter definitions: {len(catalog['counter_types'])}\n"
        "Definitions needing image review: "
        f"{len(catalog['unresolved_image_references'])}\n\n"
        f"Saved: {path}"
    )

    print(message, flush = True)
    QMessageBox.information(
        None,
        "Counter import complete",
        message,
    )


if __name__ == "__main__" : 
    main() 
