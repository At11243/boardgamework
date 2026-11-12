"""Native-resolution hex exporter and terrain review preparation (read-only).

No scene rendering or screenshot scaling: all crops come from the original
board PNG and the same hex_center/hex_vertices functions used by the editor.
"""
import argparse,hashlib,json,math,os,random
from collections import Counter,defaultdict
from pathlib import Path
os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
import numpy as np
from PySide6.QtGui import QImage,QImageReader,QPainter,QColor,QFont,QFontDatabase,QPolygonF,QPen
from PySide6.QtCore import Qt,QPointF
from PySide6.QtWidgets import QApplication
from maps.campaign_grid_definitions import barbarossa_grids
from maps.hex_model import hex_center,hex_vertices,printed_hex_number,is_playable_hex

ROOT=Path.cwd()
OUT=Path('audits/20261109/terrain')
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def identifier(key):return '--'.join(str(x).replace(' ','_') for x in key)
def region_for(key):return next(r for r in barbarossa_grids[key[0]]['regions'] if r['name']==key[1])
def crop_hex(image,key,padding=0):
    region=region_for(key);grid=region['grid'];cx,cy=hex_center(grid,key[2],key[3]);vertices=hex_vertices(grid,cx,cy)
    x0=math.floor(min(x for x,y in vertices))-padding;y0=math.floor(min(y for x,y in vertices))-padding
    x1=math.ceil(max(x for x,y in vertices))+padding;y1=math.ceil(max(y for x,y in vertices))+padding
    if x0<0 or y0<0 or x1>image.width() or y1>image.height():return None,None,{'bbox':[x0,y0,x1,y1],'center':[cx,cy],'edge_clipped':True}
    crop=image.copy(x0,y0,x1-x0,y1-y0);yy,xx=np.mgrid[y0:y1,x0:x1];xx=xx+.5;yy=yy+.5
    # Analytic convex-polygon inclusion; 90% inset avoids grid edges and adjacent pixels.
    mask=np.ones(xx.shape,bool)
    for i,(x,y) in enumerate(vertices):
        x=cx+(x-cx)*.90;y=cy+(y-cy)*.90;nx,ny=vertices[(i+1)%6];nx=cx+(nx-cx)*.90;ny=cy+(ny-cy)*.90
        cross=(nx-x)*(yy-y)-(ny-y)*(xx-x)
        # Vertices are in clockwise screen order (positive cross inside).
        mask &= cross>=-1e-7
    return crop,mask,{'bbox':[x0,y0,x1,y1],'center':[cx,cy],'vertices':vertices,'edge_clipped':False}
def rgb_array(im):
    im=im.convertToFormat(QImage.Format.Format_RGB888)
    return np.frombuffer(im.bits(),np.uint8).reshape(im.height(),im.bytesPerLine())[:,:im.width()*3].reshape(im.height(),im.width(),3).copy()
def features(im,mask):
    a=rgb_array(im).astype(float)/255;pix=a[mask];med=np.median(pix,axis=0);gray=a.mean(axis=2);dark=(gray<.42)&mask
    output=[];names=[]
    for i,c in enumerate('rgb'):
        for q in [.1,.5,.9]:names.append(f'{c}_q{int(q*100)}');output.append(float(np.quantile(pix[:,i],q)))
    blue=(a[:,:,2]>a[:,:,0]+.055)&(a[:,:,2]>a[:,:,1]-.015)&mask
    green=(a[:,:,1]>a[:,:,0]+.025)&(a[:,:,1]>a[:,:,2]+.025)&mask
    for name,m in [('dark',dark),('blue',blue),('green',green)]:names.append(name+'_fraction');output.append(float(m.sum()/mask.sum()))
    # Native-pixel gradients at several radii preserve specks and grass-stroke texture.
    for distance in [1,2,4]:
        mm=mask[:,distance:]&mask[:,:-distance];diff=np.abs(gray[:,distance:]-gray[:,:-distance])[mm]
        names.extend([f'gradient_{distance}_mean',f'gradient_{distance}_q90']);output.extend([float(diff.mean()),float(np.quantile(diff,.9))])
    # Short ink runs distinguish fine texture from large solid patches.
    runs=[]
    for row in dark:
        edges=np.diff(np.r_[False,row,False].astype(int));runs.extend((np.where(edges==-1)[0]-np.where(edges==1)[0]).tolist())
    names+=['short_ink_runs','long_ink_runs'];output += [sum(1<=r<=5 for r in runs)/mask.sum()*1000,sum(r>12 for r in runs)/mask.sum()*1000]
    return output,names
def geometry_samples():
    OUT.mkdir(parents=True,exist_ok=True);records=json.loads(Path('map_terrain.json').read_text(encoding='utf-8'))['hexes'];chosen=[]
    for board in ['Map 2','Map 3','Map 5']:
        candidates=[r for r in records if r['key'][0]==board and r['properties'].get('terrain') not in [None,['Lake/Sea']]]
        chosen.extend(candidates[:2])
    result=[]
    for rec in chosen:
        key=rec['key'];image=QImage('assets/maps/'+barbarossa_grids[key[0]]['filename']);cut,mask,info=crop_hex(image,key)
        if cut is None:continue
        assert mask.sum()>100
        name=identifier(key);cut.save(str(OUT/(name+'.png')))
        cx,cy=info['center'];context=image.copy(round(cx-250),round(cy-230),500,460).convertToFormat(QImage.Format.Format_RGB32);p=QPainter(context);p.setPen(QPen(QColor('magenta'),2));p.drawPolygon(QPolygonF([QPointF(x-round(cx-250),y-round(cy-230)) for x,y in info['vertices']]));p.end();context.save(str(OUT/(name+'-context.png')))
        result.append({'key':key,'live_terrain':rec['properties'].get('terrain'),'geometry':info})
    (OUT/'alignment_samples.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print('Alignment samples',len(result))
def export():
    OUT.mkdir(parents=True,exist_ok=True);folder=OUT/'crops';folder.mkdir(exist_ok=True)
    raw=Path('map_terrain.json').read_bytes();records=json.loads(raw)['hexes'];seen=set();flags=[];rows=[];feature_rows=[];names=[]
    groups=defaultdict(list)
    for rec in records:
        key=tuple(rec['key'])
        if key in seen:flags.append({'key':key,'field':'key','current':key,'proposed':'Review duplicate stable key','kind':'confirmed_structural_error'})
        seen.add(key);groups[key[0]].append(rec)
    for board,recs in groups.items():
        image=QImage('assets/maps/'+barbarossa_grids[board]['filename']);assert not image.isNull(),board
        for rec in recs:
            key=rec['key'];props=rec['properties'];region=region_for(key);number=printed_hex_number(region,key[2],key[3]);verified=props.get('review_status')=='Verified'
            if verified and not props.get('terrain'):flags.append({'key':key,'field':'terrain','current':props.get('terrain'),'proposed':'Review missing terrain; Verified is incomplete','kind':'confirmed_completeness_error'})
            if props.get('printed_number') and props['printed_number']!=number:flags.append({'key':key,'field':'printed_number','current':props['printed_number'],'proposed':number,'kind':'geometry_reference_disagreement'})
            cut,mask,geo=crop_hex(image,key)
            if cut is None or mask.sum()<100:
                flags.append({'key':key,'field':'crop','current':geo,'proposed':'Review clipped/off-board hex; do not train','kind':'crop_geometry_flag'});continue
            f,names=features(cut,mask);feature_rows.append(f);crop_path=folder/(identifier(key)+'.png');assert cut.save(str(crop_path))
            rows.append({'key':key,'board_id':board,'hex_id':f'{key[1]}:{number}','printed_number':number,'geometry':geo,'crop':str(crop_path),'review_status':props.get('review_status'),'live_terrain':props.get('terrain'),'live_surface':props.get('surface'),'label_status':'unreviewed_for_training','features_index':len(feature_rows)-1})
        del image;print('Exported',board,len(recs),flush=True)
    np.savez_compressed(OUT/'features.npz',X=np.asarray(feature_rows,dtype=np.float32),names=np.asarray(names))
    (OUT/'manifest.json').write_text(json.dumps({'source_sha256':hashlib.sha256(raw).hexdigest(),'calibration_sha256':digest('maps/campaign_grid_definitions.py'),'geometry_sha256':digest('maps/hex_model.py'),'feature_names':names,'rows':rows,'flags':flags},indent=2,ensure_ascii=False),encoding='utf-8')
    assert Path('map_terrain.json').read_bytes()==raw
    # Every non-water Verified hex gets a contact sheet; also sample open-water claims.
    land=[z for z in rows if z['review_status']=='Verified' and z['live_terrain']!=['Lake/Sea']]
    rng=random.Random(20261109);water=[z for z in rows if z['review_status']=='Verified' and z['live_terrain']==['Lake/Sea']];rng.shuffle(water)
    review=land+water[:36];(OUT/'visual_selection.json').write_text(json.dumps(review,indent=2),encoding='utf-8')
    QFontDatabase.addApplicationFont('C:/Windows/Fonts/arial.ttf')
    for start in range(0,len(review),12):
        im=QImage(1800,1100,QImage.Format.Format_RGB32);im.fill(QColor('white'));p=QPainter(im);p.setPen(QColor('black'));p.setFont(QFont('Arial',11))
        for j,z in enumerate(review[start:start+12]):
            x=j%4*450;y=j//4*365;p.drawText(x+4,y+18,f'{start+j+1} {z["board_id"]} {z["hex_id"]}');p.drawText(x+4,y+38,str(z['live_terrain']));cut=QImage(z['crop']);p.drawImage(x+4,y+55,cut.scaled(360,290,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.FastTransformation))
        p.end();im.save(str(OUT/f'audit-{start//12+1:02}.png'))
    print('Native crops',len(rows),'verified non-water',len(land),'water sample',min(len(water),36),'flags',len(flags),flush=True)
if __name__=='__main__':
    app=QApplication.instance() or QApplication([]);QImageReader.setAllocationLimit(2048)
    p=argparse.ArgumentParser();p.add_argument('command',choices=['alignment','export']);args=p.parse_args();geometry_samples() if args.command=='alignment' else export()
