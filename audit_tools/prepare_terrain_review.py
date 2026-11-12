"""Isolated labels, geometry flags, first labeling queue and new board crops."""
import os,json,random,hashlib
os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
from pathlib import Path
from collections import Counter
import numpy as np
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QImage,QImageReader,QPolygonF,QPainter,QColor,QFont,QFontDatabase
from PySide6.QtCore import QPointF,Qt
from audit_tools.terrain import OUT,region_for,crop_hex,features,identifier,digest
from maps.campaign_grid_definitions import barbarossa_grids
from maps.hex_model import hex_center,printed_hex_number,is_playable_hex

def main():
 app=QApplication.instance() or QApplication([]);QImageReader.setAllocationLimit(2048);QFontDatabase.addApplicationFont('C:/Windows/Fonts/arial.ttf')
 manifest=json.loads((OUT/'manifest.json').read_text(encoding='utf-8'));rows=manifest['rows'];vis=json.loads((OUT/'visual_selection.json').read_text(encoding='utf-8'));X=np.load(OUT/'features.npz')['X'];extra=[];flags=manifest['flags'];rng=random.Random(20261109)
 flags[:]=[z for z in flags if z.get('kind')!='region_geometry_flag']
 for z in rows:
  region=region_for(z['key']);inside=QPolygonF([QPointF(x,y) for x,y in region['boundary']]).containsPoint(QPointF(*z['geometry']['center']),Qt.FillRule.OddEvenFill)
  z['geometry_eligible']=inside and is_playable_hex(*z['key'])
  if not z['geometry_eligible']:flags.append({'key':z['key'],'field':'region/playability','current':z['hex_id'],'proposed':'Review region key/canonical geometry; exclude from training','kind':'region_geometry_flag'})
 eligibility={tuple(z['key']):z['geometry_eligible'] for z in rows}
 for z in vis:z['geometry_eligible']=eligibility.get(tuple(z['key']),False)
 # Independent visual proposals. Never write live terrain or reuse all Verified as labels.
 steppe=[1,3,4,11,41,44,45,46,51,52,53,54,58,61,62,63,64,65,66,67,69,70,71,72,73,78]
 lakes=[6,7,8];swamp=[2,5]
 proposals=[]
 for indices,label in [(steppe,'Steppe'),(lakes,'Lakes'),(swamp,'Swamp')]:
  for i in indices:
   z=vis[i-1];proposals.append({'key':z['key'],'reference':z['hex_id'],'field':'terrain','current':z['live_terrain'],'proposed':[label],'source':z['crop'],'rule_reference':'UICFB p4 Terrain Key','kind':'confirmed_visible_symbol_disagreement' if z['live_terrain'] else 'missing_label_proposal','detail':'Grass tufts = Steppe; larger reeds/horizontal strokes = Swamp; blue lake specks = Lakes. Land component only; coastline and other fields need separate review.'})
 # Small manually inspected seed set. Domain limited and too small for performance claims.
 seeds=[]
 for indices,label in [([99,151,156,163,212,213,216,217],'Clear'),([1,4,46,54,61,62,63,66,71,72,78],'Steppe'),([5],'Swamp')]:
  for i in indices:
   z=vis[i-1]
   if z['geometry_eligible']:seeds.append({'key':z['key'],'label':label,'status':'confirmed','reviewer':'assistant visual audit','source':z['crop'],'basis':'Native map artwork and UICFB p4; primary land texture. Not a live-data update.'})
 # Native neighbouring swamp examples, inspected separately before using as seeds.
 board='Map 3';image=QImage('assets/maps/'+barbarossa_grids[board]['filename'])
 for col,row in [(74,15),(74,16),(73,15),(73,16),(72,15),(72,16)]:
  key=[board,'FB-RH',col,row];cut,mask,geo=crop_hex(image,key)
  if cut is None:continue
  f,names=features(cut,mask);p=OUT/'crops'/(identifier(key)+'.png');cut.save(str(p));extra.append({'key':key,'board_id':board,'hex_id':f'FB-RH:{printed_hex_number(region_for(key),col,row)}','geometry':geo,'crop':str(p),'review_status':None,'live_terrain':None,'live_surface':None,'label_status':'unreviewed_for_training','geometry_eligible':True,'features':f,'seed_candidate':True})
 del image
 # Map 9 is locked evaluation BEFORE label collection or tuning. Use interiors only.
 queue_new=[]
 for board in ['Map 6','Map 9']:
  image=QImage('assets/maps/'+barbarossa_grids[board]['filename']);candidates=[]
  for region in barbarossa_grids[board]['regions']:
   poly=QPolygonF([QPointF(x,y) for x,y in region['boundary']])
   for col in range(5,85,4):
    for row in range(5,105,4):
     key=[board,region['name'],col,row];cx,cy=hex_center(region['grid'],col,row)
     if not(500<cx<image.width()-500 and 500<cy<image.height()-500 and poly.containsPoint(QPointF(cx,cy),Qt.FillRule.OddEvenFill) and is_playable_hex(*key)):continue
     cut,mask,geo=crop_hex(image,key)
     if cut is None:continue
     f,names=features(cut,mask)
     if f[10]>.10:continue # exclude obvious water/mixed blue; no terrain class inferred
     candidates.append((key,geo,f))
  assert len(candidates)>=24,(board,len(candidates))
  arr=np.asarray([z[2] for z in candidates]);scale=arr.std(axis=0)+.01;scaled=(arr-arr.mean(axis=0))/scale;chosen=[int(np.argmin(np.linalg.norm(scaled,axis=1)))];dist=np.sum((scaled-scaled[chosen[0]])**2,axis=1)
  for _ in range(23):
   idx=int(np.argmax(dist));chosen.append(idx);dist=np.minimum(dist,np.sum((scaled-scaled[idx])**2,axis=1))
  for idx in chosen:
   key,geo,f=candidates[idx];cut,mask,_=crop_hex(image,key);p=OUT/'crops'/(identifier(key)+'.png');cut.save(str(p));z={'key':key,'board_id':board,'hex_id':f'{key[1]}:{printed_hex_number(region_for(key),key[2],key[3])}','geometry':geo,'crop':str(p),'review_status':None,'live_terrain':None,'live_surface':None,'label_status':'unreviewed_for_training','geometry_eligible':True,'features':f};extra.append(z);queue_new.append(z)
  del image;print('New-board review crops',board,24,flush=True)
 # Twenty-four existing informative land cases plus forty-eight fresh mainland crops.
 first=[vis[i-1] for i in [1,2,3,4,5,6,7,8,11,41,44,45,46,51,54,61,63,66,67,78,99,151,212,216]]
 queue=[]
 for i,z in enumerate(first+queue_new):queue.append({**z,'queue_id':f'T{i+1:03}','split':'evaluation' if z['board_id']=='Map 9' else 'training','label':'','status':'unreviewed','timing_mode':'manual' if i%2 else 'suggestion'})
 (OUT/'review_queue.json').write_text(json.dumps(queue,indent=2),encoding='utf-8');(OUT/'extra_crops.json').write_text(json.dumps(extra,indent=2),encoding='utf-8')
 (OUT/'seed_labels_pending_swamp.json').write_text(json.dumps(seeds,indent=2),encoding='utf-8')
 (OUT/'audit_proposals.json').write_text(json.dumps({'flags':flags,'terrain_proposals':proposals,'visual_land_count':220,'visual_water_sample':36,'limits':'Terrain textures and geometry only. Not an audit of all settlements, facilities, hexsides, weather labels or transport. Tiny coastal land fractions/combined reliefs need separate adjudication.'},indent=2),encoding='utf-8')
 (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
 for start in range(0,len(queue),12):
  im=QImage(1800,1100,QImage.Format.Format_RGB32);im.fill(QColor('white'));p=QPainter(im);p.setPen(QColor('black'));p.setFont(QFont('Arial',12))
  for j,z in enumerate(queue[start:start+12]):
   x=j%4*450;y=j//4*365;p.drawText(x+5,y+22,f'{z["queue_id"]} {z["board_id"]} {z["hex_id"]}');p.drawText(x+5,y+44,z['split']);p.drawImage(x+5,y+55,QImage(z['crop']).scaled(360,290,Qt.AspectRatioMode.KeepAspectRatio))
  p.end();im.save(str(OUT/f'label-batch-{start//12+1:02}.png'))
 im=QImage(1500,600,QImage.Format.Format_RGB32);im.fill(QColor('white'));p=QPainter(im);p.setFont(QFont('Arial',14))
 for i,z in enumerate([z for z in extra if z.get('seed_candidate')]):
  x=i%3*500;y=i//3*300;p.drawText(x+5,y+22,str(z['key']));p.drawImage(x+5,y+40,QImage(z['crop']).scaled(230,250,Qt.AspectRatioMode.KeepAspectRatio))
 p.end();im.save(str(OUT/'swamp-seed-candidates.png'));print('Queue',len(queue),'seeds pending',len(seeds),'proposals',len(proposals),'flags',len(flags))
if __name__=='__main__':main()

