#!/usr/bin/env python3
"""Deduplicate completed responses and run paired exact McNemar/Holm analysis.

Usage: python paired_analysis.py runs_openai.jsonl runs_balanced_hint.jsonl
Latest valid successful response wins for each model/arm/item/dataset key.
"""
import json, math, sys
from pathlib import Path

ARMS=("neutral","temporal_hint","balanced_hint")
def load(path):
    latest={}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip(): continue
        try:
            r=json.loads(line)
            if r.get("response_status")!="completed" or r.get("error"): continue
            obj=json.loads(r.get("response",""))
            if obj.get("status") not in {"CURRENT","EXPIRED","NOT_YET_EFFECTIVE","INDETERMINATE"}: continue
            if obj.get("selected_document") not in {"A","B","ABSTAIN"}: continue
            key=(r.get("model"),r.get("prompt_arm"),r.get("item_id"),r.get("dataset_sha256"))
            latest[key]=r
        except Exception: continue
    return latest

def exact_mcnemar(b,c):
    n=b+c
    if n==0: return 1.0
    return min(1.0,2*sum(math.comb(n,k) for k in range(min(b,c)+1))/(2**n))

def correct(r):
    obj=json.loads(r["response"])
    return obj["status"]==r["gold_label"] and obj["selected_document"]==r["gold_action"]

if len(sys.argv)<3:
    raise SystemExit("Usage: python paired_analysis.py runs_openai.jsonl runs_balanced_hint.jsonl")
data={}
for f in sys.argv[1:]: data.update(load(f).items())
models=sorted({k[0] for k in data}); hashes=sorted({k[3] for k in data})
print("MODELS:",models); print("DATASET HASHES:",hashes)
for arm in ARMS:
    subset=[r for k,r in data.items() if k[1]==arm]
    print(f"{arm}: {len(subset)} successful unique responses")
    if subset:
        n=sum(correct(r) for r in subset)
        ind=[r for r in subset if r["gold_label"]=="INDETERMINATE"]
        false=sum(json.loads(r["response"])["selected_document"]!="ABSTAIN" for r in ind)
        print(f"  joint accuracy: {n}/{len(subset)} = {n/len(subset):.3f}")
        print(f"  indeterminate false definitive: {false}/{len(ind)}")
lookup={(k[1],k[2]):r for k,r in data.items()}
pairs=[]
for first,second in (("balanced_hint","neutral"),("balanced_hint","temporal_hint"),("neutral","temporal_hint")):
    ids=sorted({k[2] for k in data if k[1]==first}&{k[2] for k in data if k[1]==second})
    both=a_only=b_only=neither=0
    for item in ids:
        x=lookup.get((first,item)); y=lookup.get((second,item))
        if not x or not y: continue
        xc,yc=correct(x),correct(y)
        if xc and yc: both+=1
        elif xc: a_only+=1
        elif yc: b_only+=1
        else: neither+=1
    p=exact_mcnemar(a_only,b_only)
    pairs.append((p,first,second,both,a_only,b_only,neither,len(ids)))
    print(f"\n{first} vs {second}: n={len(ids)}")
    print("  both correct:",both); print(f"  {first} only correct:",a_only)
    print(f"  {second} only correct:",b_only); print("  both wrong:",neither)
    print("  exact two-sided McNemar p:",p)
# Holm step-down across all three pairwise comparisons.
ordered=sorted(enumerate(pairs),key=lambda z:z[1][0])
adjusted=[None]*len(pairs); previous=0.0; m=len(pairs)
for rank,(idx,row) in enumerate(ordered):
    candidate=min(1.0,(m-rank)*row[0]); previous=max(previous,candidate); adjusted[idx]=previous
print("\nHOLM-ADJUSTED P VALUES (all three pairwise comparisons)")
for adj,row in zip(adjusted,pairs):
    print(f"{row[1]} vs {row[2]}: raw={row[0]:.6f}, Holm={adj:.6f}")

