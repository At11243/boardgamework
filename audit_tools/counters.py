"""Read-only structural counter audit and independent artwork OCR preparation.

Run from the project root with .venv/Scripts/python.exe -m audit_tools.counters.
OCR inputs contain only original artwork pixels, never expected catalog values.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
import os
from pathlib import Path
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
from PySide6.QtGui import QImage, QImageReader, QTransform, QColor, QPainter
from PySide6.QtWidgets import QApplication, QListWidgetItem
from PySide6.QtCore import Qt


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    duplicates = []
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                duplicates.append(key)
            result[key] = value
        return result
    return json.loads(Path(path).read_text(encoding='utf-8-sig'), object_pairs_hook=pairs), duplicates


def run(out, ocr=True, check_all=False):
    out.mkdir(parents=True, exist_ok=True)
    app = QApplication.instance() or QApplication([])
    root = Path.cwd().resolve()
    definitions, duplicate_def_keys = load('assets/counters/unit_definitions.json')
    catalog, duplicate_catalog_keys = load('assets/counters/counter_catalog.json')
    data = definitions['definitions']
    baseline = {str(p): sha(p) for p in [Path('assets/counters/unit_definitions.json'), Path('assets/counters/counter_catalog.json'), Path('map_terrain.json'), Path('map_transport.json')]}
    issues = []
    image_cache = {}
    front_index = defaultdict(list)
    def issue(uid, field, current, proposed, kind='automated_flag', source='current JSON / artwork references'):
        issues.append(dict(type_id=uid, field=field, current=current, proposed=proposed, kind=kind, source=source))
    from counters import unit_editor
    ed = unit_editor.UnitEditor()
    # Read-only batch navigation never needs an interactive unsaved-edit dialog.
    ed.finish_pending_edits = lambda: True
    ed.setUpdatesEnabled(False)
    editor_issues = {}
    try:
        for index,(uid, v) in enumerate(data.items(),1):
            if index%500==0:print(f'Checked {index}/{len(data)} definitions',flush=True)
            if uid not in catalog['counter_types']:
                issue(uid, 'type_id', uid, 'Review ID absent from imported catalog')
            if v.get('type_id', uid) != uid:
                issue(uid, 'type_id', v.get('type_id'), uid)
            if v.get('front_image'):
                front_index[v['front_image']].append(uid)
            for face in ['front', 'back']:
                image = v.get(face+'_image')
                required = face == 'front' or v.get('back_appearance') == 'Printed image'
                if not image:
                    if required:issue(uid, face+'_image', image, 'Assign reviewed original artwork')
                    continue
                p = (root / image).resolve()
                if not p.is_relative_to(root):
                    issue(uid, face+'_image', image, 'Resolve unsafe path'); continue
                if image not in image_cache:
                    im = QImage(str(p))
                    image_cache[image] = {'readable':not im.isNull(), 'size':[im.width(), im.height()], 'sha256':sha(p) if p.is_file() else None}
                if not image_cache[image]['readable']:
                    issue(uid, face+'_image', image, 'Restore source artwork')
                expected = v.get('batch_review', {}).get('image_sha256', {}).get(image)
                if expected and expected != image_cache[image]['sha256']:
                    issue(uid, face+'_image_sha256', expected, image_cache[image]['sha256'], 'confirmed_integrity_error', image)
            if check_all or v.get('review_status') == 'Verified':
                item = QListWidgetItem(); item.setData(Qt.ItemDataRole.UserRole, uid)
                ed.dirty = False; ed.show_definition(item, None)
                problems = ed.definition_issues()
                if problems:
                    editor_issues[uid] = problems
                    for problem in problems:issue(uid, 'editor_completeness', problem, 'Review before retaining Verified status' if v.get('review_status')=='Verified' else 'Complete the draft when source evidence is available')
            if v.get('back_appearance') == 'Blank color' and v.get('back_image'):
                issue(uid, 'back_appearance', 'Blank color with assigned back image', 'Review whether image or generated blank is intended')
    finally:
        ed.dirty = False; ed.close()
    # Multiple appearances can legitimately share the same front. Report, never merge.
    shared = {image:ids for image,ids in front_index.items() if len(ids)>1}
    nonreciprocal = []
    for uid, v in data.items():
        if not v.get('back_image') or v.get('back_appearance') != 'Printed image':continue
        targets = front_index.get(v['back_image'], [])
        if targets and not any(data[t].get('back_image') == v.get('front_image') for t in targets):
            nonreciprocal.append({'type_id':uid, 'counterpart_candidates':targets, 'note':'May be legitimate multiple physical variants; not automatically an error.'})
    source_inventory=[]
    for p in list(Path('reference').rglob('*.pdf')) + sorted(Path('C:/Users/dt112/Downloads').glob('KIC Document*.pdf')):
        source_inventory.append({'path':str(p), 'bytes':p.stat().st_size, 'sha256':sha(p)})
    result={'definitions':len(data), 'status_counts':dict(Counter(v.get('review_status') for v in data.values())), 'by_nationality':dict(Counter(v.get('nationality') for v in data.values() if v.get('review_status')=='Verified')), 'by_category':dict(Counter(v.get('counter_category') for v in data.values() if v.get('review_status')=='Verified')), 'duplicate_json_keys':{'definitions':duplicate_def_keys,'catalog':duplicate_catalog_keys}, 'issues':issues, 'editor_issues':editor_issues, 'shared_front_art':shared, 'nonreciprocal_links':nonreciprocal, 'images':image_cache, 'sources':source_inventory, 'protected_sha256':baseline}
    (out/'consistency.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps({k:result[k] for k in ['definitions','status_counts','by_category']})+f' flags={len(issues)}',flush=True)
    if ocr:
        folder=out/'ocr_inputs';folder.mkdir(exist_ok=True)
        rows=[]
        # Every completed front; printed reverses are audited separately from fronts.
        for uid,v in data.items():
            if v.get('review_status')!='Verified':continue
            for face in ['front','back']:
                if face=='back' and v.get('back_appearance')!='Printed image':continue
                image=v.get(face+'_image')
                if image and image_cache.get(image,{}).get('readable'):rows.append({'type_id':uid,'face':face,'image':image,'sha256':image_cache[image]['sha256']})
        jobs=[]
        for start in range(0,len(rows),12):
            canvas=QImage(1200,1920,QImage.Format.Format_RGB32);canvas.fill(QColor('white'));p=QPainter(canvas)
            for j,row in enumerate(rows[start:start+12]):
                x=j%2*600;y=j//2*320;im=QImage(row['image']);sw,sh=im.width(),im.height()
                # Four-times-ish magnification aids OCR, but preserves original pixels.
                p.drawImage(x,y+10,im.scaled(270,270,Qt.AspectRatioMode.IgnoreAspectRatio,Qt.TransformationMode.FastTransformation))
                # Rotate the printed left designation for a second OCR view.
                strip=im.copy(0,0,max(1,round(sw*.23)),sh).transformed(QTransform().rotate(90))
                p.drawImage(x+285,y+10,strip.scaled(300,65))
                # Bottom literal ratings only; no expected values painted in this panel.
                bottom=im.copy(0,round(sh*.60),sw,sh-round(sh*.60))
                p.drawImage(x+285,y+100,bottom.scaled(300,150))
                row.update({'job':start//12,'cell':[x,y,600,320]})
            p.end();name=folder/f'{start//12:04}.png';assert canvas.save(str(name));jobs.append({'image':str(name.resolve()),'output':str((out/'ocr_results'/f'{start//12:04}.json').resolve())})
        (out/'ocr_results').mkdir(exist_ok=True)
        (out/'ocr_manifest.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
        for worker in range(4):(out/f'jobs-{worker}.json').write_text(json.dumps(jobs[worker::4]),encoding='utf-8')
        print(f'OCR prepared: {len(rows)} original artwork faces, {len(jobs)} panels, 4 workers',flush=True)
    assert all(sha(p)==h for p,h in baseline.items()),'Audit mutated protected data'


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,default=Path('audits/20261109/counters'));parser.add_argument('--no-ocr',action='store_true');parser.add_argument('--all-definitions',action='store_true');args=parser.parse_args();run(args.out,not args.no_ocr,args.all_definitions)
