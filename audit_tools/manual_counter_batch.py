"""Prepare a reproducible stratified visual review, without catalog mutations."""
import os
os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
import json,random,re
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QImage,QPainter,QColor,QFont,QFontDatabase
from PySide6.QtCore import Qt

def main():
    app=QApplication.instance() or QApplication([]);QFontDatabase.addApplicationFont('C:/Windows/Fonts/arial.ttf')
    out=Path('audits/20261109/counters/manual');out.mkdir(parents=True,exist_ok=True)
    d=json.loads(Path('assets/counters/unit_definitions.json').read_text(encoding='utf-8'))['definitions'];verified={u:v for u,v in d.items() if v.get('review_status')=='Verified'}
    rng=random.Random(20261109);order=list(verified);rng.shuffle(order);groups={};selection=[]
    for u in order:
        v=d[u];key=(v.get('nationality'),v.get('counter_category'),v.get('ground',{}).get('front',{}).get('format'))
        if key not in groups:groups[key]=u;selection.append(u)
    for u in order:
        if len(selection)>=120:break
        if u not in selection:selection.append(u)
    # Use only direct sheet locators for illustrated physical checks. Old claims are not accepted automatically.
    from audit_tools.sheet_helpers import photo,geom
    for start in range(0,len(selection),6):
        canvas=QImage(2000,1800,QImage.Format.Format_RGB32);canvas.fill(QColor('white'));p=QPainter(canvas);p.setPen(QColor('black'));p.setFont(QFont('Arial',13))
        for j,u in enumerate(selection[start:start+6]):
            v=d[u];y=j*300;p.drawText(5,y+22,f'{start+j+1}: {u} | {v.get("nationality")} | {v.get("unit_type")} | {v.get("designation")}')
            for k,face in enumerate(['front','back']):
                image=v.get(face+'_image');im=QImage(image or '')
                if not im.isNull():p.drawImage(5+k*230,y+40,im.scaled(220,220))
            evidence=v.get('physical_back_review',{});source=evidence.get('source_pdf','');m=re.search(r'(\d+)\.pdf$',source)
            loc=None
            if m and 'front_page' in evidence:
                n=int(m.group(1));loc=[n,evidence['front_page'],evidence['front_row'],evidence['front_column']]
                for k,face in enumerate(['front','back']):
                    pg=evidence.get(face+'_page');r=evidence.get(face+'_row');c=evidence.get(face+'_column')
                    if pg is None:continue
                    im=photo(n,pg);x,yy,s=geom(n,pg,r,c);cut=im.copy(round(x-s/2),round(yy-s/2),round(s),round(s));p.drawImage(475+k*230,y+40,cut.scaled(220,220))
            facts={key:v.get(key) for key in ['service','unit_size','back_appearance','ground','aircraft','naval','faces'] if v.get(key)}
            p.drawText(950,y+40,1040,250,Qt.TextFlag.TextWordWrap,str(facts))
            vloc={'type_id':u,'art_front':v.get('front_image'),'art_back':v.get('back_image'),'physical_front_location':loc}
            if start==0 and j==0:pass
        p.end();assert canvas.save(str(out/f'batch-{start//6+1:02}.png'))
    (out/'selection.json').write_text(json.dumps(selection,indent=2),encoding='utf-8');print('Manual selection',len(selection), 'strata',len(groups),flush=True)
if __name__=='__main__':main()

