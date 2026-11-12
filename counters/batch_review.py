"""Apply artwork-reviewed batches, protecting existing manual definitions.

This automates validation, review status, provenance and safe persistence. It
does not extract ratings from filenames or equate OCR confidence/completeness
with accuracy. The assistant supplies visually audited proposals. Existing
IDs are skipped unless an unchanged, untranscribed queue placeholder is
explicitly targeted by a matching record fingerprint.
"""
import argparse
from copy import deepcopy
import hashlib
import json
import math
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace

from counters.unit_storage import write_definitions


def record_fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":")).encode("utf-8")).hexdigest()


def is_queue_placeholder(value):
    """Allow opt-in replacement of untouched inventory records, never real work."""
    if (value.get("review_status") != "In progress"
            or "REVIEW QUEUE ONLY:" not in value.get("notes", "")
            or value.get("front_image") or value.get("back_image")
            or value.get("back_appearance") != "Not yet reviewed"):
        return False
    if any(value.get(key) not in (None, "", "Unknown") for key in
           ("designation", "nationality", "service", "unit_type", "unit_size")):
        return False
    if any(value.get(key) for key in ("ground", "aircraft", "naval", "commander", "faces")):
        return False
    review = value.get("batch_review", {}).get("review", {})
    return all(review.get(aspect, {}).get("checked") is False
               for aspect in ("identity", "front", "back"))


def prepare_batch(root, catalog, current, batch, issues_for):
    """Return a new document and report; inputs are never mutated."""
    if (batch.get("format") != "tsww-counter-review-batch"
            or batch.get("version") != 1 or not isinstance(batch.get("entries"), list)
            or not isinstance(batch.get("source"), str) or not batch["source"].strip()):
        raise ValueError("Invalid artwork review batch.")
    root = Path(root).resolve()
    result = deepcopy(current)
    report = {"verified": [], "in_progress": {}, "skipped_existing": []}
    seen = set()
    for entry in batch["entries"]:
        uid = entry["type_id"]
        if uid in seen or uid not in catalog["counter_types"]:
            raise ValueError(f"Duplicate or unknown counter ID: {uid}")
        seen.add(uid)
        existing = current["definitions"].get(uid)
        if existing is not None:
            expected = entry.get("replace_placeholder_sha256")
            if not expected:
                report["skipped_existing"].append(uid)
                continue
            if not is_queue_placeholder(existing) or record_fingerprint(existing) != expected:
                raise ValueError(f"Queue entry changed or contains reviewed/manual work: {uid}")
        value = deepcopy(existing or {})
        value.update(deepcopy(entry["definition"]))
        if existing:
            # Retain user-added note lines while replacing generated queue text.
            extra_notes = [line for line in existing.get("notes", "").splitlines()
                           if line.strip() and not line.startswith(
                               ("Imported name:", "REVIEW QUEUE ONLY:", "Batch review issues:"))]
            if extra_notes:
                value["notes"] = value.get("notes", "") + "\n" + "\n".join(extra_notes)
        review = entry.get("review", {})
        hashes = entry.get("image_sha256", {})
        problems = list(entry.get("issues", []))
        if not all(isinstance(item, str) for item in problems):
            raise ValueError(f"Invalid review issues: {uid}")
        allowed = set(catalog["counter_types"][uid].get("image_paths", []))
        for face in ("front", "back"):
            if face == "back" and value.get("back_appearance") == "Blank color":
                continue
            name = value.get(face + "_image")
            if not name:
                problems.append(f"{face}: no assigned image")
                continue
            path = (root / name).resolve()
            if not path.is_relative_to(root) or Path(name).is_absolute():
                raise ValueError(f"Image path outside project: {uid}")
            if name not in allowed:
                problems.append(f"{face}: assignment not linked to this catalog entry")
            expected = hashes.get(name)
            if expected:
                if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                    raise ValueError(f"Artwork changed since review: {uid} {face}")
            else:
                problems.append(f"{face}: no artwork fingerprint from review")
        for aspect in ("identity", "front", "back"):
            audit = review.get(aspect, {})
            if (audit.get("checked") is not True or not isinstance(audit.get("evidence"), str)
                    or not audit["evidence"].strip()):
                problems.append(f"{aspect}: artwork review incomplete")
            confidence = audit.get("confidence")
            if (type(confidence) not in (int, float) or not math.isfinite(confidence)
                    or not 0.95 < confidence <= 1):
                problems.append(f"{aspect}: confidence must be greater than 95%")
        # The caller uses the editor's existing completeness checks, not a
        # parallel interpretation of required/optional ratings.
        problems.extend(issues_for(uid, value))
        problems = list(dict.fromkeys(problems))
        value["review_status"] = "In progress" if problems else "Verified"
        value["batch_review"] = {
            "version": 1, "reviewed_by": batch["source"],
            "review": deepcopy(review), "image_sha256": deepcopy(hashes),
            "issues": problems,
        }
        if problems:
            report["in_progress"][uid] = problems
            value["notes"] = value.get("notes", "") + "\nBatch review issues: " + "; ".join(problems)
        else:
            report["verified"].append(uid)
        result["definitions"][uid] = value
    return result, report


def save_batch(path, expected_bytes, document):
    """Refuse a stale plan instead of overwriting a concurrent editor save."""
    path = Path(path)
    if path.read_bytes() != expected_bytes:
        raise ValueError("Definitions changed during review; rerun against the latest file.")
    if json.loads(expected_bytes) != document:
        write_definitions(path, document)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch", type=Path)
    parser.add_argument("--apply", action="store_true", help="Save new definitions; default is dry-run")
    parser.add_argument("--report", type=Path)
    parser.add_argument("--summary", action="store_true", help="Print counts instead of every ID")
    args = parser.parse_args()
    # No visible window; use the real editor's loader and completeness policy.
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from PySide6.QtWidgets import QApplication, QListWidgetItem
    from PySide6.QtCore import Qt
    from counters.unit_editor import UnitEditor, project_dir
    app = QApplication.instance() or QApplication([])
    path = project_dir / "assets/counters/unit_definitions.json"
    original = path.read_bytes()
    current = json.loads(original)
    catalog = json.loads((path.parent / "counter_catalog.json").read_text(encoding="utf-8"))
    batch = json.loads(args.batch.read_text(encoding="utf-8-sig"))
    # Validate proposed schema before instantiating the editor, so malformed
    # proposals cannot trigger blocking error dialogs or be silently normalized.
    candidates = deepcopy(current)
    for entry in batch["entries"]:
        if (entry["type_id"] not in candidates["definitions"]
                or entry.get("replace_placeholder_sha256")):
            prior = candidates["definitions"].get(entry["type_id"], {})
            candidates["definitions"][entry["type_id"]] = dict(prior, **entry["definition"])
    with tempfile.TemporaryDirectory() as folder:
        candidate_path = Path(folder) / "definitions.json"
        candidate_path.write_text(json.dumps(candidates), encoding="utf-8")
        UnitEditor.load_definitions(SimpleNamespace(definitions_path=candidate_path))
    editor = UnitEditor()
    try:
        def issues_for(uid, value):
            editor.dirty = False
            editor.unit_definitions[uid] = deepcopy(value)
            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, uid)
            editor.show_definition(item, None)
            return editor.definition_issues()
        updated, report = prepare_batch(project_dir, catalog, current, batch, issues_for)
        if args.apply:
            save_batch(path, original, updated)
        if args.report:
            args.report.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps({key: len(value) for key, value in report.items()}
                         if args.summary else report, indent=2))
    finally:
        editor.dirty = False
        editor.close()


if __name__ == "__main__":
    main()
