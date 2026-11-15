# Raw response logs: archive status

The experiment produced 120 successful responses. The researcher reported that the local working folder contains:

- `runs_openai.jsonl` (append-only original log, including retries and failed attempts)
- `runs_deduplicated.jsonl` (80 successful unique responses for neutral and temporal_hint)
- `runs_balanced_hint.jsonl` (40 successful responses)

These three files were not present in the working package available when this repository was populated. They are therefore **not included**. The results in `results_summary.json` and `paper.md` have not been freshly recomputed from those raw response records in this repository.

Before public release, add the three local files only after checking for API keys, authorization headers, personal information, or other secrets. Preserve the original append-only log. Publish checksums for each raw file and document any redaction. Never commit an API key.
