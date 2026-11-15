# Exact prompt conditions used in the pilot

All conditions share the same base instructions. The temporal_hint and balanced_hint conditions append their respective reminders.

## Base instructions

You are completing a controlled research evaluation about the temporal validity of fictional policy documents. Use only the documents supplied in the item. Do not use outside knowledge or browse the web. Determine the target document's status on the stated query date, then determine which document should govern. If the supplied evidence does not establish which document governs, choose ABSTAIN. Your confidence should represent confidence in the combined status and action. Give a concise rationale based only on explicit evidence.

## Neutral

Base instructions only.

## Temporal hint

Important evaluation reminder: publication date, effective date, and expiration or replacement date are distinct. A later publication does not by itself prove that an earlier document has ceased to apply.

## Balanced hint

Important evaluation reminder: publication date, effective date, and expiration or replacement date are distinct. A later publication does not by itself prove that an earlier document has ceased to apply. Equally, the absence of an expiration date does not by itself prove that an earlier document remains valid. A document with a future effective date does not govern before that date. If the supplied evidence does not establish which document governs on the query date, choose ABSTAIN.

## Design note

The balanced hint was added after results from the neutral and temporal-hint conditions were inspected. Treat it as an exploratory follow-up, not a preregistered intervention.
