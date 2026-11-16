import json, csv, random, pathlib
from datetime import date, timedelta

OUT = pathlib.Path(__file__).parent
random.seed(20261114)
query_dates = ["2026-06-01", "2026-07-15", "2026-09-01", "2027-01-10", "2026-11-20"]
topics = [
    ("Remote Work Allowance", "Employees may claim a monthly remote-work allowance of {amount} credits."),
    ("Vendor Onboarding", "New vendors must complete {requirement} before receiving purchase orders."),
    ("Data Retention", "Routine project records must be retained for {period} months."),
    ("Travel Reimbursement", "Domestic travel may be reimbursed up to {amount} credits per day."),
    ("Research Grant Eligibility", "Applicants must have at least {requirement} to qualify for the internal research grant."),
    ("Equipment Lending", "Staff may borrow standard equipment for {period} days."),
    ("Incident Reporting", "Incidents must be reported within {period} hours of discovery."),
    ("Training Requirement", "New staff must complete {requirement} before independent work."),
    ("Cloud Storage", "Project teams may use up to {amount} GB of approved cloud storage."),
    ("Procurement Approval", "Purchases above {amount} credits require director approval."),
]
amounts = ["40", "60", "75", "90", "120", "150", "200", "250", "300", "500"]
requirements = ["two references", "a security review", "manager approval", "a completed induction", "a risk assessment", "three months of service"]
periods = ["3", "6", "9", "12", "18", "24", "48", "72"]

def add_months(d, n):
    y = d.year + (d.month - 1 + n)//12
    m = (d.month - 1 + n)%12 + 1
    day = min(d.day, [31,29 if y%4==0 and (y%100!=0 or y%400==0) else 28,31,30,31,30,31,31,30,31,30,31][m-1])
    return date(y,m,day)

def fmt(d): return d.isoformat()

items=[]
for i in range(40):
    category = ["CURRENT", "EXPIRED", "NOT_YET_EFFECTIVE", "INDETERMINATE"][i//10]
    q = date.fromisoformat(query_dates[i%len(query_dates)])
    title, template = topics[i%len(topics)]
    old_pub = date(2024 + (i%2), 1 + (i%6), 1 + (i%20))
    old_eff = add_months(old_pub, 1 + (i%3))
    new_pub = date(2025 + (i%2), 1 + ((i*3)%10), 1 + ((i*7)%20))
    new_eff = add_months(new_pub, 1 + (i%5))
    old_text = template.format(amount=amounts[i%len(amounts)], requirement=requirements[i%len(requirements)], period=periods[i%len(periods)])
    new_text = template.format(amount=amounts[(i+3)%len(amounts)], requirement=requirements[(i+2)%len(requirements)], period=periods[(i+2)%len(periods)])
    if category == "CURRENT":
        old_pub=date(2024,1+(i%6),5+(i%20)); old_eff=add_months(old_pub,1)
        new_pub=add_months(q,1+(i%3)); new_eff=add_months(new_pub,2)
        old_status="Document A remains in force until it is replaced by a later document that has taken effect."
        doc_a=f"DOCUMENT A — {title}\nPublished: {fmt(old_pub)}\nEffective from: {fmt(old_eff)}\nValidity statement: {old_status}\nProvision: {old_text}"
        doc_b=f"DOCUMENT B — {title} (revision)\nPublished: {fmt(new_pub)}\nEffective from: {fmt(new_eff)}\nExplicitly replaces Document A from its effective date.\nProvision: {new_text}"
        rationale="A is effective on the query date and remains in force until a later document takes effect. B is not yet effective."
    elif category == "EXPIRED":
        old_pub=date(2024,1+(i%6),5+(i%20)); old_eff=add_months(old_pub,1)
        end=add_months(q,-(1+(i%4)))
        new_pub=add_months(end,-1); new_eff=end + timedelta(days=1)
        doc_a=f"DOCUMENT A — {title}\nPublished: {fmt(old_pub)}\nEffective from: {fmt(old_eff)}\nValid through: {fmt(end)}\nProvision: {old_text}"
        doc_b=f"DOCUMENT B — {title} (replacement)\nPublished: {fmt(new_pub)}\nEffective from: {fmt(new_eff)}\nExplicitly replaces Document A from its effective date.\nProvision: {new_text}"
        rationale="A's stated validity ended before the query date; B replaced it from its effective date."
    elif category == "NOT_YET_EFFECTIVE":
        old_pub=date(2024,1+(i%6),5+(i%20)); old_eff=add_months(old_pub,1)
        new_pub=add_months(q,-(1+(i%3))); new_eff=add_months(q,1+(i%4))
        doc_a=f"DOCUMENT A — {title}\nPublished: {fmt(old_pub)}\nEffective from: {fmt(old_eff)}\nValidity statement: Document A remains in force until a replacement takes effect.\nProvision: {old_text}"
        doc_b=f"DOCUMENT B — {title} (announced revision)\nPublished: {fmt(new_pub)}\nEffective from: {fmt(new_eff)}\nExplicitly replaces Document A only from the effective date above.\nProvision: {new_text}"
        rationale="B is already published but its effective date is after the query date; A remains in force until then."
    else:
        old_pub=date(2024,1+(i%6),5+(i%20)); old_eff=add_months(old_pub,1)
        new_pub=add_months(q,-(1+(i%3))); new_eff=add_months(q,1+(i%4))
        doc_a=f"DOCUMENT A — {title}\nPublished: {fmt(old_pub)}\nEffective from: {fmt(old_eff)}\nNo expiration date, replacement clause, or statement about continued validity is provided.\nProvision: {old_text}"
        doc_b=f"DOCUMENT B — {title} (later publication)\nPublished: {fmt(new_pub)}\nEffective from: {fmt(new_eff)}\nNo statement says whether Document B replaces Document A, or what happens to A.\nProvision: {new_text}"
        rationale="The available metadata does not establish whether A remains valid or was separately withdrawn; B's publication and future effective date do not resolve that."
    target = "B" if category == "NOT_YET_EFFECTIVE" else "A"
    action = {"CURRENT":"A", "EXPIRED":"B", "NOT_YET_EFFECTIVE":"A", "INDETERMINATE":"ABSTAIN"}[category]
    items.append({
        "item_id": f"EB-{i+1:03d}", "query_date": fmt(q), "target_document": target,
        "gold_label": category, "gold_action": action, "documents": doc_a+"\n\n"+doc_b,
        "question": f"As of {fmt(q)}, classify the status of target Document {target}. Choose exactly one label: CURRENT, EXPIRED, NOT_YET_EFFECTIVE, or INDETERMINATE. Then choose which document should govern the decision on that date: A, B, or ABSTAIN if the evidence does not establish which applies. Use only the supplied documents. Return confidence from 0 to 100 for your combined judgment.",
        "gold_rationale": rationale, "topic": title,
        "condition": ["explicit_continuity", "explicit_expiry_and_replacement", "published_but_future_effective", "validity_not_established"][i//10]
    })

random.shuffle(items)
with (OUT/"expirybench_v0_1.jsonl").open("w",encoding="utf-8") as f:
    for x in items: f.write(json.dumps(x,ensure_ascii=False)+"\n")
with (OUT/"expirybench_v0_1.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=["item_id","query_date","topic","condition","target_document","gold_label","gold_action","question","documents","gold_rationale"])
    w.writeheader()
    for x in items: w.writerow({k:x[k] for k in w.fieldnames})
print(f"Created {len(items)} items at {OUT}")
