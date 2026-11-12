"""Compare fresh pixel OCR to literal saved values; failures are NOT corrections.

This checks printed factors only. It cannot verify nationality, symbols, or the
physical relationship of two faces. Expected values never enter the OCR images.
"""
import json,re
from collections import Counter
from pathlib import Path

def normalized(text):
    return re.sub(r'\s+','',text).replace('–','-').replace('−','-').replace('—','-').upper()

def expected_ground(r):
    f=r.get('format','')
    if not f:
        if r.get('combat_strength') is not None and r.get('movement') is not None:f='Combined combat strength / movement'
        elif all(r.get(k) is not None for k in ['attack','defense','movement']):f='Separate attack / defense / movement'
    if f=='Combined combat strength / movement':return '-'.join(str(r.get(k,'')) for k in ['combat_strength','movement'])
    if f=='Separate attack / defense / movement':return '-'.join(str(r.get(k,'')) for k in ['attack','defense','movement'])
    if f=='Antiaircraft':return '-'.join(str(r.get(k,'')) for k in ['attack','defense','movement'] if r.get(k) not in [None,''])
    if f in ['Coastal defense','Fortification level']:return 'Level'+str(r.get('cd_level') if f=='Coastal defense' else r.get('fortification_level'))
    return str(r.get('printed_rating') or r.get('movement') or '')

def main():
    out=Path('audits/20261109/counters');d=json.loads(Path('assets/counters/unit_definitions.json').read_text(encoding='utf-8'))['definitions'];rows=json.loads((out/'ocr_manifest.json').read_text());results=[];cache={}
    for row in rows:
        job=row['job'];p=out/'ocr_results'/f'{job:04}.json'
        if not p.exists():continue
        if job not in cache:cache[job]=json.loads(p.read_text(encoding='utf-8-sig'))['words']
        x,y,_,_=row['cell'];words=cache[job]
        def region(x0,y0,x1,y1):
            subset=[w for w in words if x+x0<=w['x']+w['w']/2<x+x1 and y+y0<=w['y']+w['h']/2<y+y1]
            return ' '.join(w['text'] for w in sorted(subset,key=lambda a:(round((a['y']-y)/15),a['x'])))
        bottom=region(0,160,275,285);enlarged_bottom=region(280,95,600,260);top=region(0,0,275,110);desig=region(280,0,600,85);v=d[row['type_id']];face=row['face'];category=v['counter_category'];expected='';field='';observed=bottom
        if category=='Ground unit':expected=expected_ground(v.get('ground',{}).get(face,{}));field='literal bottom rating / level'
        elif category=='Air unit':
            r=v.get('aircraft',{}).get(face,{});expected=str(r.get('attack_factor',''))+str(r.get('aircraft_type_code',''))+str(r.get('air_defense',''));field='printed top attack / code / defense';observed=top
        elif category=='Naval unit':
            r=v.get('naval',{}).get(face,{});expected=str(r.get('gunnery',''))+str(r.get('ship_type',''))+str(r.get('protection',''));field='printed top gunnery / code / protection';observed=top
        clean=normalized(expected);text=normalized(observed)
        alternatives=[text]+([normalized(enlarged_bottom)] if category=='Ground unit' else [])
        matched=bool(clean and clean not in ['NONE','N/A','UNKNOWN'] and any(re.search(r'(?<![0-9])'+re.escape(clean)+r'(?![0-9])',t) for t in alternatives))
        results.append({**row,'field':field,'expected':expected,'observed':observed,'designation_ocr':desig,'matched':matched,'status':'literal OCR corroboration only' if matched else 'unresolved OCR; needs visual reading, not a confirmed error'})
    factor_manifest=out/'factor_manifest.json'
    if factor_manifest.exists():
        factors={};fcache={}
        for row in json.loads(factor_manifest.read_text()):
            job=row['job'];p=out/'factor_results'/f'{job:04}.json'
            if not p.exists():continue
            if job not in fcache:fcache[job]=json.loads(p.read_text(encoding='utf-8-sig'))['words']
            x,y,ww,hh=row['cell'];ws=[z for z in fcache[job] if x<=z['x']+z['w']/2<x+ww and y<=z['y']+z['h']/2<y+hh]
            text=' '.join(z['text'] for z in sorted(ws,key=lambda z:z['x']));factors[row['type_id']]=text
        for row in results:
            if row['face']!='front' or d[row['type_id']]['counter_category']!='Ground unit':continue
            text=factors.get(row['type_id'],'');clean=normalized(row['expected'])
            row['contrast_strip_ocr']=text
            if clean and clean not in ['NONE','N/A','UNKNOWN'] and re.search(r'(?<![0-9])'+re.escape(clean)+r'(?![0-9])',normalized(text)):
                row['matched']=True;row['status']='literal OCR corroboration only'
    fronts=[r for r in results if r['face']=='front'];matched={r['type_id'] for r in fronts if r['matched']}
    report={'completed':sum(v.get('review_status')=='Verified' for v in d.values()),'faces_attempted':len(results),'fronts_attempted':len(fronts),'fronts_literal_factor_matched':len(matched),'front_factor_coverage':len(matched)/5708,'categories':{c:{'fronts_attempted':sum(d[r['type_id']]['counter_category']==c for r in fronts),'fronts_matched':sum(d[r['type_id']]['counter_category']==c and r['matched'] for r in fronts)} for c in sorted({v['counter_category'] for v in d.values()})},'rows':results,'scope':'Independent machine reading of original artwork pixels; factor/code corroboration only. Not a complete metadata/physical-pair audit. No confidence score or identity/nationality claim. Unmatched OCR must not become a proposed correction without visual evidence.'}
    (out/'ocr_comparison.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8');print({k:v for k,v in report.items() if k not in ['rows']})
if __name__=='__main__':main()
