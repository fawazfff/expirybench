# Raw response logs: audit and archive status

## Public log reviewed

The append-only `runs_openai.jsonl` file was reviewed in full before publication in its current sanitized form.

- Original records reviewed: **119**.
- Completed model responses: **80** (40 neutral and 40 temporal-hint).
- Failed API attempts: **38** (API connection errors in the temporal-hint condition).
- Incomplete responses: **1** (neutral condition; the returned response payload was truncated and its inner JSON could not be parsed).
- The 80 completed responses cover all 40 benchmark item IDs once in each of the two conditions.
- All completed records use the same dataset SHA-256: `f38f1d2695a43fc2999363a6b494583e5690843902934d82954c1b90ab07b585`.
- The recorded model identifier is `gpt-6-luna`.

## Integrity check

The completed records were rescored directly from their stored model outputs:

| Condition | Completed n | Correct joint decisions | Joint accuracy |
|---|---:|---:|---:|
| Neutral | 40 | 38 | 95.0% |
| Temporal hint | 40 | 33 | 82.5% |

These values match the corresponding neutral and temporal-hint entries in `results_summary.json`.

The incomplete response and failed API attempts are retained in the append-only log for transparency and are not counted among the 80 completed responses. The failed attempts contain the error label `APIConnectionError: Connection error.`.

## Redaction and security review

A pattern-based scan of all 119 records found no obvious API-key strings, bearer tokens, authorization-header values, private-key markers, or email addresses. This is a practical screening check, not a guarantee that every possible sensitive value has been ruled out.

Provider-generated `response_id` fields were removed from the current public copy because they are not needed to reproduce the scoring. Model outputs, prompt conditions, item IDs, gold labels/actions, dataset hash, timestamps, usage metadata, latency values, and failed/incomplete attempt records were retained.

The original append-only log should be retained by the researcher in private storage. The repository's earlier Git commit contains the previous version with response IDs; those IDs were not identified as credentials. The current file is the sanitized public copy.

## Scope limitation

This file covers only the neutral and temporal-hint conditions. The separate 40-response `balanced_hint` log is not present here. Therefore, this file independently supports the first 80 successful responses, but does not by itself reproduce the full 120-response, three-condition result set.

Do not describe the balanced-hint results as independently verified from this file. Add the balanced-hint log after it has been separately checked and sanitized.
