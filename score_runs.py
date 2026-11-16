#!/usr/bin/env python3
"""Score ExpiryBench JSONL run records. Invalid or failed records count as incorrect."""
import argparse, collections, json
LABELS={"CURRENT","EXPIRED","NOT_YET_EFFECTIVE","INDETERMINATE"}
ACTIONS={"A","B","ABSTAIN"}
p=argparse.ArgumentParser(description=__doc__); p.add_argument("runs"); a=p.parse_args()
rows=[json.loads(x) for x in open(a.runs,encoding="utf-8") if x.strip()]
by=collections.defaultdict(list)
for r in rows:
    try:
        obj=json.loads(r.get("response",""))
        status=str(obj.get("status","")).upper().strip()
        action=str(obj.get("selected_document","")).upper().strip()
        conf=int(obj.get("confidence"))
        valid=(not r.get("error") and r.get("response_status","completed")=="completed"
               and status in LABELS and action in ACTIONS and 0<=conf<=100)
    except Exception:
        status=action=None; conf=None; valid=False
    by[(r.get("model","unknown"),r.get("prompt_arm","unspecified"))].append(
        (r.get("gold_label"),r.get("gold_action"),status,action,conf,valid))
for (model,arm),vals in sorted(by.items()):
    n=len(vals); valid=sum(x[5] for x in vals)
    sc=sum(x[0]==x[2] for x in vals if x[5])
    ac=sum(x[1]==x[3] for x in vals if x[5])
    jc=sum(x[0]==x[2] and x[1]==x[3] for x in vals if x[5])
    right_status=[x for x in vals if x[5] and x[0]==x[2]]
    gap=sum(x[1]!=x[3] for x in right_status)
    ind=[x for x in vals if x[0]=="INDETERMINATE"]
    false=sum(x[5] and x[3]!="ABSTAIN" for x in ind)
    brier=sum((x[4]/100-(1 if x[0]==x[2] and x[1]==x[3] else 0))**2 for x in vals if x[5])/valid if valid else float("nan")
    print(f"\nMODEL: {model} | ARM: {arm} | records={n} | valid={valid}")
    print(f"Status accuracy: {sc}/{n} = {sc/n:.3f}")
    print(f"Action accuracy: {ac}/{n} = {ac/n:.3f}")
    print(f"Joint accuracy: {jc}/{n} = {jc/n:.3f}")
    print(f"Validity-Action Gap: {gap}/{len(right_status)}")
    print(f"Indeterminate false definitive: {false}/{len(ind)}")
    print(f"Joint-confidence Brier score (valid outputs): {brier:.4f}")
    for label in sorted(LABELS):
        sub=[x for x in vals if x[0]==label]
        correct=sum(x[5] and x[2]==label for x in sub)
        print(f"{label}: {correct}/{len(sub)}")
