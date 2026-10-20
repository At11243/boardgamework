"""Atomic unit-definition writes with the existing timestamped backup convention."""
import json
import shutil
from datetime import datetime
from pathlib import Path


def write_definitions(path, data):
    path = Path(path)
    temporary = path.with_name(path.name + ".tmp")
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        temporary.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        if path.is_file():
            backup_dir = path.parent / "unit_definition_backups"
            backup_dir.mkdir(parents=True, exist_ok=True)
            stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            shutil.copy2(path, backup_dir / f"unit-definitions-{stamp}.json")
        temporary.replace(path)
    finally:
        if temporary.exists():
            temporary.unlink()
