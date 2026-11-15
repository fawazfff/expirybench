# ExpiryBench v0.1

**When Evidence Expires: Prompt Sensitivity in Document-Validity Decisions**

ExpiryBench is a small synthetic pilot benchmark for evaluating whether a language model can distinguish document publication, effective, expiry, and replacement dates, and whether it abstains when the supplied evidence does not establish which document governs.

**Research track:** Apart Research AI x Epistemics Sprint, Track 1: Model Epistemics & Decision-Making Evals.

## Research question

Can prompt wording change a model's document-validity classifications and its decision to select a document or abstain when temporal evidence is incomplete?

## Dataset

- 40 fictional document-pair scenarios.
- 10 examples each: CURRENT, EXPIRED, NOT_YET_EFFECTIVE, and INDETERMINATE.
- JSONL SHA-256: `f38f1d2695a43fc2999363a6b494583e5690843902934d82954c1b90ab07b585`.
- No real personal records or live policy documents.

## Pilot results

One recorded model identifier (`gpt-6-luna`) was evaluated once on each item under three prompt conditions, for 120 successful responses.

| Metric | Neutral | Temporal hint | Balanced hint |
|---|---:|---:|---:|
| Joint accuracy | 95% | 82.5% | 100% |
| Indeterminate accuracy | 8/10 | 3/10 | 10/10 |
| False definitive actions on indeterminate | 2/10 | 7/10 | 0/10 |

The balanced prompt was designed after the first two conditions had been inspected. It is a post-hoc exploratory follow-up, not a preregistered intervention. Its perfect score may reflect close alignment with the repeated structure of the indeterminate items. The balanced-versus-neutral comparison was not significant (exact paired McNemar p = 0.50). The balanced-versus-temporal-hint comparison was significant after Holm correction (adjusted p = 0.046875).

These results do not establish general temporal reasoning ability, performance on unseen documents, or safety for real-world legal, medical, financial, or regulatory decisions. All errors occurred in indeterminate cases. No Validity-Action Gap cases were observed.

## Repository contents

- `paper.md`: research report draft.
- `ExpiryBench_paper.docx` and `ExpiryBench_paper.pdf`: working report exports. These are not yet verified exports from the official sprint template.
- `expirybench_v0_1.jsonl` and `expirybench_v0_1.csv`: synthetic benchmark items.
- `PROMPTS.md`: exact prompt conditions.
- `research_protocol.md`: protocol and design notes.
- `run_eval.py`, `score_runs.py`, `paired_analysis.py`: evaluation and analysis scripts.
- `results_summary.json`: reported pilot metrics.
- `RAW_RUNS_STATUS.md`: status of original response logs.

## Reproducibility and raw logs

The original response logs are not included in this repository yet. The reported metrics were transcribed from the scoring and paired-analysis outputs supplied during the research process, not freshly recomputed from raw response records in this package. Do not treat the results as independently reproduced until the logs have been audited and the scoring scripts rerun.

Before publishing raw logs, check for API keys, authorization headers, personal information, or other secrets. Never commit an API key. Keep keys in local environment variables.

## Work provenance and AI assistance

The project package records the work completed during the 13–15 November 2026 sprint and notes that no pre-sprint source file was identified in the supplied archive. The archive does not contain full Git history, so this is not independent proof of creation dates. If any code or data predates the sprint, it must be disclosed in the report and here.

AI tools assisted with code drafting and debugging, analysis-script development, and editorial review. The researcher remains responsible for checking the dataset, labels, experiment records, calculations, references, and final claims.

## Sprint submission status

The working report contains a 150–250 word abstract and the required appendix titled **Limitations and Dual-Use / Ethical Considerations**. The exact official Google Docs template still needs to be applied and the final page count checked. The sprint's official template and guidelines are linked below.

- [Official report template](https://docs.google.com/document/d/17b3JWki-ZkaqdmqGI5d0gof-HwlGuWU9Mc_1klNZXKs/copy?usp=sharing)
- [Sprint guidelines](https://apartresearch.com/sprints/ai-x-epistemics-research-sprint-2026-11-13-to-2026-11-15#guidelines)
