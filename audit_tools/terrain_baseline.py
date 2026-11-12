"""Numpy color/texture baseline. Scores are NOT calibrated probabilities."""
import json, hashlib
from collections import Counter
import numpy as np
from audit_tools.terrain_labeler import ROOT

CLASSES = ['Clear', 'Steppe', 'Swamp']

def fit(x, y):
    mean = x.mean(axis=0); scale = np.maximum(x.std(axis=0), .01)
    standardized = (x-mean)/scale
    centers = np.array([standardized[np.array(y)==c].mean(axis=0) for c in CLASSES])
    return mean, scale, centers

def predict(x, model):
    mean, scale, centers = model
    distance = np.mean((((x-mean)/scale)[:, None, :]-centers[None, :, :])**2, axis=2)
    logits = -distance; logits -= logits.max(axis=1, keepdims=True)
    score = np.exp(logits); score /= score.sum(axis=1, keepdims=True)
    return score, distance

def main():
    manifest = json.loads((ROOT/'manifest.json').read_text()); rows = manifest['rows']
    x = np.load(ROOT/'features.npz')['X']; extras = json.loads((ROOT/'extra_crops.json').read_text())
    features = {tuple(z['key']): x[z['features_index']] for z in rows}
    features.update({tuple(z['key']): np.array(z['features']) for z in extras})
    labels = json.loads((ROOT/'seed_labels_pending_swamp.json').read_text())
    # These six native crops were independently visually inspected against UICFB p4.
    for z in extras:
        if z.get('seed_candidate'):
            labels.append({'key':z['key'], 'label':'Swamp', 'status':'confirmed', 'source':z['crop']})
    human = ROOT/'human_labels.json'
    if human.exists():
        by_key = {tuple(z['key']):z for z in labels}
        for z in json.loads(human.read_text()).values(): by_key[tuple(z['key'])] = z
        labels = list(by_key.values())
    labels = [z for z in labels if z.get('status')=='confirmed' and z['label'] in CLASSES]
    train = [z for z in labels if z['key'][0]!='Map 9']; evaluation = [z for z in labels if z['key'][0]=='Map 9']
    assert not {tuple(z['key']) for z in train} & {tuple(z['key']) for z in evaluation}
    counts = Counter(z['label'] for z in train)
    if any(counts[c]<3 for c in CLASSES): raise ValueError(f'Need three reviewed seeds per class: {counts}')
    model = fit(np.array([features[tuple(z['key'])] for z in train]), [z['label'] for z in train])
    np.savez_compressed(ROOT/'baseline.npz', mean=model[0], scale=model[1], centers=model[2])
    model_hash = hashlib.sha256((ROOT/'baseline.npz').read_bytes()).hexdigest()
    suggestions = []
    for z in rows+extras:
        f = features[tuple(z['key'])]; scores, distances = predict(f[None,:], model); j=int(scores[0].argmax())
        excluded = not z.get('geometry_eligible',False) or f[10]>.10
        outside = distances[0,j]>4
        suggestions.append({'key':z['key'], 'hex_id':z['hex_id'], 'suggested_terrain':None if excluded or outside else CLASSES[j],
            'score':float(scores[0,j]), 'score_meaning':'uncalibrated relative centroid preference, not correctness probability',
            'review_required':True, 'reason':'geometry/water exclusion' if excluded else 'outside seed distribution' if outside else 'prototype requires human review', 'model_sha256':model_hash})
    (ROOT/'suggestions.json').write_text(json.dumps(suggestions,indent=2))
    results = {}
    for c in CLASSES:
        subset = [z for z in evaluation if z['label']==c]
        correct = sum(CLASSES[int(predict(features[tuple(z['key'])][None,:], model)[0][0].argmax())]==c for z in subset)
        results[c]={'training_count':counts[c], 'evaluation_count':len(subset), 'recall':correct/len(subset) if subset else None}
    (ROOT/'metrics.json').write_text(json.dumps({'per_class':results, 'evaluation_board':'Map 9', 'suggestions':len(suggestions), 'limits':'No accuracy claim without held-out human labels. No CNN or timing comparison justified yet.'},indent=2))
    print(json.dumps(results,indent=2))
if __name__=='__main__': main()
