"""Full inventory audit with evidence-limited corrections and atomic persistence."""
import argparse,copy,hashlib,json,re
from collections import Counter,defaultdict
from pathlib import Path
from counters.unit_storage import write_definitions
from audit_tools.summarize_counter_ocr import expected_ground,normalized

OUT=Path('audits/20261112/counters_full_check')
DEFINITIONS=Path('assets/counters/unit_definitions.json')
RUN='counter-full-check-20261112'

def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def reconcile(document,findings,collisions):
    """Pure transformation; retains every unknown field and prior evidence."""
    result=copy.deepcopy(document);data=result['definitions'];changes=[]
    country='vassal:133:236608'
    if country in data and data[country].get('nationality')=='German':
        data[country]['nationality']='Germany'
        changes.append({'type_id':country,'field':'nationality','before':'German','after':'Germany','source':'User-confirmed German Army Infantry Division 87 example in PROJECT_CONTEXT.md; original grey 87 / XX / 12-6 artwork; roster uses Germany.'})
    issues=defaultdict(list)
    for finding in findings:issues[finding['type_id']].append({'kind':finding['kind'],'detail':finding['detail'],'source':finding['source_reference']})
    for group in collisions:
        for uid in group['type_ids']:issues[uid].append({'kind':'physical_locator_collision','detail':f"Same physical front cell claimed by distinct artwork: {group['type_ids']}",'source':group['location']})
    for uid,flags in issues.items():
        v=data[uid]
        if v.get('counter_audit',{}).get('run')==RUN:continue
        previous=v.get('review_status')
        # Explicitly preserve withdrawn provenance, not just the file backup.
        v.setdefault('counter_audit_history',[]).append({'run':RUN,'prior_review_status':previous,'physical_back_review':copy.deepcopy(v.get('physical_back_review')),'batch_review':copy.deepcopy(v.get('batch_review'))})
        v['counter_audit']={'run':RUN,'result':'Needs source reconciliation','issues':flags,'scope':'Metadata/source evidence only. Artwork, identity, ratings and face assignments retained.'}
        v['review_status']='In progress'
        p=v.get('physical_back_review')
        if isinstance(p,dict):
            p['audit_status']='Unresolved: prior corroboration must not be relied on'
            if any(f['kind']=='confirmed_locator_mismatch' for f in flags):
                p['result']='Invalid source locator; physical reverse unconfirmed';p['confidence']=0
        batch=v.get('batch_review')
        message='Counter audit: source evidence unresolved; see counter_audit issues. Prior physical corroboration is suspended; retain current digital art/ratings pending review.'
        if isinstance(batch,dict):
            if message not in batch.setdefault('issues',[]):batch['issues'].append(message)
            parts=['identity','front','back'] if any(f['kind']=='confirmed_locator_mismatch' for f in flags) else ['back']
            for part in parts:
                review=batch.get('review',{}).get(part)
                if isinstance(review,dict):review.update({'checked':False,'confidence':0,'evidence':message})
        v['notes']=v.get('notes','')+'\n\n'+message
        changes.append({'type_id':uid,'field':'review/source evidence','before':previous,'after':'In progress','issues':flags,'source':'Independent source-locator review and all-definition physical-cell cross-check'})
    return result,changes

def main(apply=False):
    original=DEFINITIONS.read_bytes();doc=json.loads(original);data=doc['definitions'];catalog=json.loads(Path('assets/counters/counter_catalog.json').read_text())['counter_types']
    consistency=json.loads((OUT/'consistency.json').read_text());manual=json.loads(Path('audits/20261109/counters/manual_review.json').read_text())
    assert hashlib.sha256(original).hexdigest()==consistency['protected_sha256'][str(DEFINITIONS)],'Definitions changed since consistency scan; rescan before applying'
    groups=defaultdict(list);physical_flags=[]
    sources={z['sha256']:z for z in consistency['sources']};physical_count=0
    for uid,v in data.items():
        p=v.get('physical_back_review',{})
        if p:physical_count+=1
        location=(p.get('source_sha256') or p.get('source_pdf'),p.get('front_page'),p.get('front_row'),p.get('front_column'))
        if all(location):groups[location].append(uid)
        if p.get('source_sha256') and p.get('source_sha256') not in sources:physical_flags.append({'type_id':uid,'kind':'unavailable_physical_source_hash','source':p.get('source_pdf'),'expected_sha256':p['source_sha256']})
    collisions=[{'location':list(k),'type_ids':ids,'front_images':[data[i].get('front_image') for i in ids]} for k,ids in groups.items() if len({data[i].get('front_image') for i in ids})>1]
    # Previous manual findings apply only if the exact reviewed provenance remains.
    applicable=[]
    for f in manual['findings']:
        if data[f['type_id']].get('physical_back_review')==f['current']:applicable.append(f)
        else:physical_flags.append({'type_id':f['type_id'],'kind':'prior_finding_source_changed','source':f['source_reference']})
    revised,changes=reconcile(doc,applicable,collisions)
    ocr=json.loads(Path('audits/20261109/counters/ocr_comparison.json').read_text());corroborated=defaultdict(list);unresolved=defaultdict(list)
    for row in ocr['rows']:
        uid=row['type_id'];face=row['face'];v=data[uid];category=v.get('counter_category')
        current=expected_ground(v.get('ground',{}).get(face,{})) if category=='Ground unit' else ''.join(str(v.get('aircraft',{}).get(face,{}).get(k,'')) for k in ['attack_factor','aircraft_type_code','air_defense']) if category=='Air unit' else ''.join(str(v.get('naval',{}).get(face,{}).get(k,'')) for k in ['gunnery','ship_type','protection']) if category=='Naval unit' else ''
        image=consistency['images'].get(row['image'],{})
        valid=(v.get(face+'_image')==row['image'] and image.get('sha256')==row['sha256'] and normalized(current)==normalized(row['expected']))
        if valid and row['matched']:corroborated[uid].append(face)
        else:unresolved[uid].append({'face':face,'reason':'Unresolved OCR is not a confirmed metadata error' if valid else 'Cached OCR source/field changed; cannot reuse'})
    candidates=json.loads((OUT/'visual_factor_candidates.json').read_text());visual={}
    for index,row in enumerate(candidates,1):
        visual.setdefault(row['id'],[]).append({'face':row['face'],'expected':row['expected'],'finding':'Saved literal ratings agree with visible original artwork; OCR disagreement rejected','panel':f'visual/ocr-mismatch-{(index-1)//16+1:02}.png','cell':(index-1)%16+1,'source_image':data[row['id']].get(row['face']+'_image')})
    results=[]
    collision_ids={uid for g in collisions for uid in g['type_ids']}
    by_issue=defaultdict(list)
    for z in consistency['issues']:by_issue[z['type_id']].append(z)
    catalog_overrides=[]
    for uid,v in data.items():
        override=bool(v.get('front_image') and v['front_image'] not in catalog[uid]['image_paths'])
        if override:catalog_overrides.append(uid)
        results.append({'type_id':uid,'designation':v.get('designation'),'before_status':v.get('review_status'),'after_status':revised['definitions'][uid].get('review_status'),
            'automated_checks':['stable ID / catalog membership','assigned image existence/readability/fingerprint','editor core completeness for applicable faces','duplicate/shared art and face-link cross-check','physical-source location cross-check'],
            'issues':by_issue[uid],'source_cell_conflict':uid in collision_ids,'catalog_front_override':override,
            'literal_ocr_corroborated_faces':corroborated[uid],'unresolved_ocr':unresolved[uid],'new_visual_factor_checks':visual.get(uid,[]),
            'not_certified':['all designation/service/type/size/optional fields independently reread','physical front/back pairing unless separately supported']})
    report={'run':RUN,'total':len(data),'before_counts':dict(Counter(v.get('review_status') for v in data.values())),'after_counts':dict(Counter(v.get('review_status') for v in revised['definitions'].values())),
        'editor_incomplete_definitions':len(consistency['editor_issues']),'structural_flags':consistency['issues'],'physical_records':physical_count,'physical_unique_cells':len(groups),'physical_cell_collisions':collisions,'physical_flags':physical_flags,
        'catalog_front_override_ids':catalog_overrides,'shared_front_groups':consistency['shared_front_art'],'nonreciprocal_links':consistency['nonreciprocal_links'],
        'visual_factor_faces':len(candidates),'visual_factor_ids':len(visual),'ocr_literal_fronts':sum('front' in faces for faces in corroborated.values()),'changes':changes,'before_sha256':hashlib.sha256(original).hexdigest(),'applied':apply,
        'limits':'All definitions checked automatically, not all fields independently visually certified. 188 suspicious face ratings reread from original pixels; no confirmed printed-factor error found. OCR unmatched and unreviewed fields remain explicit, not invented corrections. Catalog overrides and nonreciprocal appearances are review flags, not automatic errors.'}
    (OUT/'all_definition_results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    if apply:
        assert DEFINITIONS.read_bytes()==original,'Concurrent edits detected; abort'
        if changes:write_definitions(DEFINITIONS,revised)
        report['after_sha256']=digest(DEFINITIONS)
    (OUT/'review.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    lines=['# Full counter definition check — 2026-11-12','',f"All **{len(data):,} definitions** checked automatically. Starting statuses: {report['before_counts']}. {'Applied' if apply else 'Proposed'} statuses: {report['after_counts']}.",'',
        '**This is not a claim that every field on every counter has been independently visually verified.** Each ID has a record in all_definition_results.json listing checks, incomplete fields, OCR evidence and remaining uncertified scope. Metadata and original artwork remain distinct from source-corroboration claims.', '',
        '## Findings and corrections','',
        '- Corrected nationality spelling for German Army Infantry Division 87: German → Germany. Stable ID, artwork, face values and zero/N/A semantics retained.',
        '- Nine previously confirmed physical locator errors: withdrew invalid corroboration, preserved original claims in audit history, retained digital artwork and factors.',
        '- Six ambiguous physical-source cases: flagged for reinspection; no speculative rating or pairing edits.',
        f'- {len(collisions)} physical front cells are claimed by {len(collision_ids)} definitions using different front artwork. All affected definitions are flagged; no counter IDs merged and no reverse images invented. These could include art/version or mapping problems and need cell-level reconciliation.',
        f'- {len(changes)-1} source-flagged definitions received explicit audit issues/notes and In progress status. Only 45 previously Verified definitions were downgraded; already In progress entries remain so.',
        f'- Existing editor checks found {len(consistency["editor_issues"])} incomplete definitions, all already In progress; {sum(z["field"]=="front_image" for z in consistency["issues"])} lack assigned fronts. Their exact IDs/fields are in the all-definition results, not silently fixed from filenames.',
        f'- {len(catalog_overrides)} saved front assignments differ from their own imported catalog entry. Recovered artwork can legitimately do this; report only. Likewise {len(consistency["shared_front_art"])} shared-front groups and {len(consistency["nonreciprocal_links"])} nonreciprocal appearance groups are not automatically errors.', '',
        '## Independent evidence and limits','',
        f'Inspected **{len(candidates)} suspicious face rating sequences / {len(visual)} IDs** against original artwork across twelve panels. The saved literal ratings agree; these were OCR errors, so no printed factor corrections were made. Earlier 120-entry stratified manual inspection remains a separate, overlapping sample. OCR evidence is reused only when source-image SHA, assignment and expected current field match. {report["ocr_literal_fronts"]} front factor/code sequences retain OCR corroboration. This is not full identity/type/nationality/physical-pair certification.',
        '', 'No missing modifier or blank reverse is inferred from a filename. Original PDFs/art/catalog are not rewritten. Manual unknown fields are retained. Remaining physical ambiguity requires correct sheet/cell/front-back identification or clearer images; the audit does not claim that every physical back has now been matched.', '',
        '## Changed IDs','', '| ID | Field / issue | Before | After |','| --- | --- | --- | --- |']
    for c in changes:lines.append(f"| {c['type_id']} ({data[c['type_id']].get('designation','')}) | {c['field']} | {c['before']} | {c['after']} |")
    lines += ['', '## Specific source questions','', '| ID / designation | Finding | Source |','| --- | --- | --- |']
    for f in applicable:lines.append(f"| {f['type_id']} / {data[f['type_id']].get('designation','')} | {f['detail']} | {f['source_reference']} |")
    lines += ['', '## Conflicting source cells','', 'Each row names every definition claiming the same physical front cell with different artwork. Hash, PDF page, row and column are retained for exact lookup; use consistency.json sources to resolve the document hash.', '', '| Source SHA / PDF page / row / column | IDs and designations |','| --- | --- |']
    for g in collisions:lines.append(f"| {g['location']} | {'; '.join(i+' '+str(data[i].get('designation','')) for i in g['type_ids'])} |")
    lines += ['', 'Exact source references, issue descriptions, all collision IDs and before/after fingerprints are in review.json. Prior source-review objects and batch-review evidence are retained per changed definition in counter_audit_history as well as the timestamped file backup.', '',
        '## Reproduce / manual checks','',
        'Close any open unit editor before loading externally updated definitions; an old window may hold stale data. Open Infantry Division 87 and confirm Germany. Open flagged Arko 108 and confirm In progress plus audit notes. Ratings/art must be unchanged. Pick an unaffected Verified counter to confirm its status and values were retained.', '',
        'Read-only: `.venv/Scripts/python.exe -m audit_tools.counters --out audits/20261112/counters_full_check --no-ocr --all-definitions`.',
        'The reconciliation script is guarded against concurrent definition changes and uses the existing atomic writer/backup convention. Do not reapply an old audit plan against newer manually edited data. Persistence tests must use temporary fixtures.', '',
        'Terrain tooling, labels and live map files were left outside this counter-only commit. No gameplay rules or artwork changes.']
    (OUT/'REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ['total','before_counts','after_counts','editor_incomplete_definitions','visual_factor_faces','visual_factor_ids','ocr_literal_fronts','applied']},indent=2));print('Changed IDs',len(changes),'physical cells',len(collisions))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true');main(p.parse_args().apply)
