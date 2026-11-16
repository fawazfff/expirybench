# Raw response logs: audit and archive status

## Public logs reviewed

Both public run logs were fetched from the repository and checked in full.

### Neutral and temporal-hint log: `runs_openai.jsonl`

- Original records reviewed: **119**.
- Completed model responses: **80** (40 neutral and 40 temporal-hint).
- Failed API attempts: **38**.
- Incomplete responses: **1**.
- The 80 completed responses cover all 40 benchmark item IDs once in each condition.
- All completed records use dataset SHA-256: `f38f1d2695a43fc2999363a6b494583e5690843902934d82954c1b90ab07b585`.
- Recorded model identifier: `gpt-6-luna`.

### Balanced-hint log: `runs_balanced_hint.jsonl`

- Records reviewed: **40**.
- Completed responses: **40**.
- Failed or incomplete records: **0**.
- All 40 expected item IDs (EB-001 through EB-040) appear exactly once.
- All records use prompt arm `balanced_hint`, model identifier `gpt-6-luna`, and the same dataset SHA-256 as the other conditions.
- Every response payload is valid JSON.
- All 40 predicted status labels match `gold_label`.
- All 40 selected-document actions match `gold_action`.
- Joint accuracy: **40/40 (100%)**, matching `results_summary.json`.

## Recomputed results

| Condition | Completed n | Correct joint decisions | Joint accuracy |
|---|---:|---:|---:|
| Neutral | 40 | 38 | 95.0% |
| Temporal hint | 40 | 33 | 82.5% |
| Balanced hint | 40 | 40 | 100.0% |

The neutral and temporal-hint values were rescored from the completed outputs in `runs_openai.jsonl`. The balanced-hint value was rescored from `runs_balanced_hint.jsonl`. These results match the corresponding entries in `results_summary.json`.

## Redaction and security review

A pattern-based scan of both logs found no obvious API-key strings, bearer tokens, authorization-header values, private-key markers, or email addresses. This is a practical screening check, not a guarantee that every possible sensitive value has been ruled out.

Provider-generated `response_id` fields were removed from both public run logs because they are not needed to reproduce the scoring. Model outputs, prompt conditions, item IDs, gold labels/actions, dataset hash, timestamps, usage metadata, and other experiment fields were retained. The original unmodified logs should be retained by the researcher in private storage.

The earlier Git history may contain versions of the neutral/temporal log with response IDs. Those identifiers were not identified as credentials. The current public files are the sanitized copies.

## Scope and limitations

The public archive now contains the 120 completed responses across all three prompt conditions. The balanced-hint condition was designed after the first two conditions had been inspected, so it remains a post-hoc exploratory condition. The raw-log checks verify record integrity and agreement with the stored gold labels/actions; they do not independently validate the benchmark's underlying gold-label design or establish general model capability.

The latency field in the balanced-hint log is zero for every record. It should not be used to make latency or speed claims.

The pattern-based security scan can miss unknown or obfuscated secrets. The original unmodified append-only logs should remain in private storage.
