"""Prepare simple contrast-normalized source-pixel strips for a second OCR view."""
import json,os
os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
from pathlib import Path
import numpy as np
from PySide6.QtGui import QImage,QColor,QPainter
from PySide6.QtWidgets import QApplication

def main():
 app=QApplication.instance() or QApplication([]);out=Path('audits/20261109/counters');folder=out/'factor_inputs';folder.mkdir(exist_ok=True);(out/'factor_results').mkdir(exist_ok=True)
 d=json.loads(Path('assets/counters/unit_definitions.json').read_text(encoding='utf-8'))['definitions'];rows=[];jobs=[]
 for u,v in d.items():
  if v.get('review_status')=='Verified' and v.get('front_image'):rows.append({'type_id':u,'image':v['front_image'],'face':'front'})
 for start in range(0,len(rows),80):
  canvas=QImage(1000,2000,QImage.Format.Format_RGB32);canvas.fill(QColor('white'));p=QPainter(canvas)
  for j,row in enumerate(rows[start:start+80]):
   im=QImage(row['image']).convertToFormat(QImage.Format.Format_RGB888);h,ww=im.height(),im.width();a=np.frombuffer(im.bits(),np.uint8).reshape(h,im.bytesPerLine())[:,:ww*3].reshape(h,ww,3).astype(float)
   # Absolute color difference preserves light ink on dark counters and dark ink on light ones.
   bg=np.median(a[3:-3,3:-3],axis=(0,1));contrast=np.max(np.abs(a-bg),axis=2);gray=np.uint8(255-np.clip(contrast/(np.percentile(contrast,98)+1e-6)*255,0,255));gray[:2]=255;gray[-2:]=255;gray[:,:2]=255;gray[:,-2:]=255
   norm=QImage(gray.data,ww,h,ww,QImage.Format.Format_Grayscale8).copy();cut=norm.copy(2,round(h*.68),ww-4,max(1,round(h*.28)))
   x=j%4*250;y=j//4*100;p.drawImage(x+10,y+10,cut.scaled(220,70));row.update({'job':start//80,'cell':[x,y,250,100]})
  p.end();name=folder/f'{start//80:04}.png';assert canvas.save(str(name));jobs.append({'image':str(name.resolve()),'output':str((out/'factor_results'/name.with_suffix('.json').name).resolve())})
 (out/'factor_manifest.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
 for k in range(4):(out/f'factor-jobs-{k}.json').write_text(json.dumps(jobs[k::4]),encoding='utf-8')
 print('Contrast factor panels',len(jobs),flush=True)
if __name__=='__main__':main()
