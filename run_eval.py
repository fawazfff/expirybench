#!/usr/bin/env python3
"""Run ExpiryBench v0.1 with the OpenAI Responses API.

Set OPENAI_API_KEY in your environment. Raw logs can contain provider response IDs;
keep original logs private and redact identifiers before public release.
"""
import argparse, hashlib, json, os, pathlib, sys, time, traceback
from datetime import datetime, timezone
from openai import OpenAI

ROOT = pathlib.Path(__file__).parent
LABELS = ["CURRENT", "EXPIRED", "NOT_YET_EFFECTIVE", "INDETERMINATE"]
ACTIONS = ["A", "B", "ABSTAIN"]
SCHEMA = {
    "type": "object",
    "properties": {
        "status": {"type": "string", "enum": LABELS},
        "selected_document": {"type": "string", "enum": ACTIONS},
        "confidence": {"type": "integer", "minimum": 0, "maximum": 100},
        "rationale": {"type": "string"}
    },
    "required": ["status", "selected_document", "confidence", "rationale"],
    "additionalProperties": False
}
BASE = ("You are completing a controlled research evaluation about the temporal validity of fictional policy documents. "
        "Use only the documents supplied in the item. Do not use outside knowledge or browse the web. "
        "Determine the target document's status on the stated query date, then determine which document should govern. "
        "If the supplied evidence does not establish which document governs, choose ABSTAIN. "
        "Your confidence should represent confidence in the combined status and action. "
        "Give a concise rationale based only on explicit evidence.")
HINT = ("Important evaluation reminder: publication date, effective date, and expiration or replacement date are distinct. "
        "A later publication does not by itself prove that an earlier document has ceased to apply.")
BALANCED = (HINT + " Equally, the absence of an expiration date does not by itself prove that an earlier document remains valid. "
            "A document with a future effective date does not govern before that date. "
            "If the supplied evidence does not establish which document governs on the query date, choose ABSTAIN.")
PROMPTS = {"neutral": BASE, "temporal_hint": BASE + " " + HINT, "balanced_hint": BASE + " " + BALANCED}

def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024), b""): h.update(chunk)
    return h.hexdigest()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--model",default="gpt-6-luna")
    p.add_argument("--input",default=str(ROOT/"expirybench_v0_1.jsonl"))
    p.add_argument("--output",default=str(ROOT/"runs_openai.jsonl"))
    p.add_argument("--arm",choices=PROMPTS,default="neutral")
    p.add_argument("--reasoning-effort",choices=["low","medium","high"],default="low")
    p.add_argument("--limit",type=int,default=0)
    p.add_argument("--sleep",type=float,default=1.0)
    p.add_argument("--no-resume",action="store_true")
    a=p.parse_args()
    if not os.getenv("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY is missing. Set it in your terminal; do not paste it into chat or source code.")
    src=pathlib.Path(a.input); dst=pathlib.Path(a.output)
    rows=[json.loads(x) for x in src.read_text(encoding="utf-8").splitlines() if x.strip()]
    digest=sha256(src); done=set()
    if dst.exists() and not a.no_resume:
        for line in dst.read_text(encoding="utf-8").splitlines():
            try:
                r=json.loads(line); obj=json.loads(r.get("response",""))
                if (r.get("model")==a.model and r.get("prompt_arm")==a.arm and r.get("dataset_sha256")==digest
                    and r.get("response_status")=="completed" and not r.get("error")
                    and obj.get("status") in LABELS and obj.get("selected_document") in ACTIONS):
                    done.add(r.get("item_id"))
            except Exception: pass
    pending=[x for x in rows if x["item_id"] not in done]
    if a.limit: pending=pending[:a.limit]
    if not pending:
        print("No unseen items to run."); return
    client=OpenAI(timeout=60,max_retries=3); dst.parent.mkdir(parents=True,exist_ok=True)
    print(f"Model: {a.model} | arm: {a.arm} | items: {len(pending)}")
    print("Dataset SHA256:",digest)
    with dst.open("a",encoding="utf-8") as out:
        for i,item in enumerate(pending,1):
            start=time.time()
            rec={"item_id":item["item_id"],"model":a.model,"prompt_arm":a.arm,
                 "gold_label":item["gold_label"],"gold_action":item["gold_action"],
                 "dataset_sha256":digest,"timestamp_utc":datetime.now(timezone.utc).isoformat()}
            try:
                response=client.responses.create(
                    model=a.model,instructions=PROMPTS[a.arm],
                    input=item["documents"]+"\n\n"+item["question"],
                    reasoning={"effort":a.reasoning_effort},
                    text={"format":{"type":"json_schema","name":"expirybench_answer","strict":True,"schema":SCHEMA}},
                    max_output_tokens=1500,store=False)
                obj=json.loads(response.output_text)
                assert obj["status"] in LABELS and obj["selected_document"] in ACTIONS
                assert isinstance(obj["confidence"],int) and 0<=obj["confidence"]<=100
                rec.update({"response_id":response.id,"response":response.output_text,
                            "response_status":response.status,
                            "usage":response.usage.model_dump() if response.usage else None,
                            "latency_seconds":round(time.time()-start,3)})
            except Exception as e:
                rec.update({"error":f"{type(e).__name__}: {e}","traceback":traceback.format_exc(),
                            "latency_seconds":round(time.time()-start,3)})
            out.write(json.dumps(rec,ensure_ascii=False)+"\n"); out.flush()
            print(f"{i}/{len(pending)} {item['item_id']}: {'ERROR' if rec.get('error') else 'SAVED'}")
            if a.sleep: time.sleep(a.sleep)
    print("Finished. Results:",dst)

if __name__=="__main__": main()
