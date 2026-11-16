# ExpiryBench v0.1

**When Evidence Expires: Prompt Sensitivity in Document-Validity Decisions**

ExpiryBench is a 40-item synthetic pilot benchmark for testing whether a language model distinguishes document publication, effective, expiry, and replacement dates, and whether it abstains when the supplied evidence does not establish which document governs.

**Research track:** Apart Research AI x Epistemics Research Sprint, Track 1: Model Epistemics & Decision-Making Evals.

## Research question

Can prompt wording change a model's document-validity classifications and its decision to select a document or abstain when temporal evidence is incomplete?

## Dataset

- 40 fictional document-pair scenarios.
- 10 examples each: CURRENT, EXPIRED, NOT_YET_EFFECTIVE, and INDETERMINATE.
- JSONL SHA-256: `f38f1d2695a43fc2999363a6b494583e5690843902934d82954c1b90ab07b585`.
- No real personal records or live policy documents.
- The deterministic generator was rerun and reproduced the published JSONL byte-for-byte with the same SHA-256.

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

### Research and benchmark
- `paper.md`: current research report in Markdown.
- `expirybench_v0_1.jsonl` and `expirybench_v0_1.csv`: frozen 40-item dataset.
- `DATASET_SHA256.txt`: dataset checksum.
- `PROMPTS.md`: exact prompt-condition descriptions.
- `research_protocol.md`: protocol and deviations.
- `REFERENCES_VERIFIED.md`: bibliographic verification notes.
- `SPRINT_ALIGNMENT.md`: sprint requirement checklist.

### Reproduction code
- `build_benchmark.py`: deterministic dataset generator.
- `run_eval.py`: OpenAI Responses API evaluation runner for all three prompt arms.
- `score_runs.py`: scores status, action, joint accuracy, abstention errors, and exploratory confidence.
- `paired_analysis.py`: deduplicates successful records and calculates paired exact McNemar tests with Holm adjustment.
- `requirements.txt` and `.env.example`: Python dependency and environment template.

### Experiment records and audit
- `runs_openai.jsonl`: append-only neutral and temporal-hint attempts, including failed and incomplete attempts. Provider response IDs have been removed from the public copy.
- `runs_balanced_hint.jsonl`: 40 completed balanced-hint responses. Provider response IDs have been removed.
- `RAW_RUNS_STATUS.md`: record-integrity and redaction audit.
- `results_summary.json`: pilot metrics and paired-comparison results.
- `paired_comparisons.csv`: item-level paired-test summary and Holm-adjusted p-values.

The public run logs contain the 120 successful responses across all three conditions, plus the failed/incomplete attempts retained in the first log for transparency. The balanced-hint log was checked for valid JSON, unique coverage of all 40 item IDs, consistent model and dataset hash, and agreement between each predicted status/action and its gold label/action. The raw-data checks verify record integrity and scoring consistency; they do not independently validate the benchmark's gold-label design.

## Clone the repository and reproduce the pilot

You can download the complete project to your computer and reproduce the published dataset and analysis. You do not need an API key to reproduce the reported pilot scores because the original experiment responses are included in the repository.

### 1. Install the tools

Install:
- Git: https://git-scm.com/downloads
- Python 3.10 or newer: https://www.python.org/downloads/

On Windows, select the option to add Python to PATH during installation if the installer offers it.

### 2. Clone the GitHub repository

Open Terminal, PowerShell, or Command Prompt and run:

```bash
git clone https://github.com/fawazfff/expirybench.git
cd expirybench
```

This downloads the project files and moves your terminal into the project folder.

### 3. Install the Python packages

```bash
python -m pip install -r requirements.txt
```

If your computer uses the Windows Python launcher, you can use `py -3 -m pip install -r requirements.txt` instead.

### 4. Rebuild and verify the benchmark dataset

Run:

```bash
python build_benchmark.py
```

The script generates `expirybench_v0_1.jsonl` and `expirybench_v0_1.csv` in the project folder. Check the JSONL checksum.

macOS/Linux:

```bash
sha256sum expirybench_v0_1.jsonl
```

Windows PowerShell:

```powershell
(Get-FileHash .\expirybench_v0_1.jsonl -Algorithm SHA256).Hash.ToLower()
```

The expected SHA-256 is:

```
f38f1d2695a43fc2999363a6b494583e5690843902934d82954c1b90ab07b585
```

The checksum lets you check whether the generated dataset matches the frozen dataset used for the reported experiment. If the hash differs, do not treat it as the same dataset until the difference has been investigated.

### 5. Reproduce the reported scores from the archived experiment

Run:

```bash
python score_runs.py runs_openai.jsonl
python score_runs.py runs_balanced_hint.jsonl
python paired_analysis.py runs_openai.jsonl runs_balanced_hint.jsonl
```

These commands score the archived model responses and calculate the paired comparisons with Holm correction. They do not call an AI API and do not incur API charges.

The reported joint accuracies are:
- Neutral: 38/40 (95%).
- Temporal hint: 33/40 (82.5%).
- Balanced hint: 40/40 (100%).

### 6. Run a new experiment (optional)

This step is different from reproducing the published results. It sends new requests to the OpenAI API, creates new responses, may incur API charges, and will not necessarily produce the same scores.

Set your API key as an environment variable. Do not put it in a Python file or commit it to GitHub.

Windows PowerShell:

```powershell
$env:OPENAI_API_KEY = "YOUR_API_KEY"
```

macOS/Linux:

```bash
export OPENAI_API_KEY="YOUR_API_KEY"
```

Then run each prompt condition:

```bash
python run_eval.py --arm neutral --output new_runs_neutral.jsonl
python run_eval.py --arm temporal_hint --output new_runs_temporal_hint.jsonl
python run_eval.py --arm balanced_hint --output new_runs_balanced_hint.jsonl
```

Keep newly generated run files separate from the archived files. The runner writes provider response IDs to local output records, so do not publish those raw files without reviewing and sanitizing them first.


```bash
python build_benchmark.py
sha256sum expirybench_v0_1.jsonl
```

The generated JSONL should have SHA-256:

```
f38f1d2695a43fc2999363a6b494583e5690843902934d82954c1b90ab07b585
```

## Re-score the archived runs

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Score the first two conditions and the balanced condition:

```bash
python score_runs.py runs_openai.jsonl
python score_runs.py runs_balanced_hint.jsonl
```

Recompute all three conditions and paired tests:

```bash
python paired_analysis.py runs_openai.jsonl runs_balanced_hint.jsonl
```

The paired script uses the latest valid successful response for each model, prompt arm, item, and dataset hash. It applies Holm adjustment across all three pairwise comparisons.

## Run a new evaluation

Set the API key in your terminal, never in source code or a committed file.

PowerShell:

```powershell
$env:OPENAI_API_KEY = "YOUR_API_KEY"
```

macOS/Linux:

```bash
export OPENAI_API_KEY="YOUR_API_KEY"
```

Run one condition at a time, writing to separate output files:

```bash
python run_eval.py --arm neutral --output new_runs_neutral.jsonl
python run_eval.py --arm temporal_hint --output new_runs_temporal_hint.jsonl
python run_eval.py --arm balanced_hint --output new_runs_balanced_hint.jsonl
```

The default model identifier is the one recorded in the pilot. Change it with `--model` if testing another model. The runner resumes completed items by default; use `--no-resume` only when a fresh full run is intended.

**Important:** Running the API evaluation again creates new experimental data and may incur API charges. It is not required to reproduce the reported pilot results. The archived logs are the source for the reported outputs. The runner stores provider response IDs in local raw logs; keep originals private and remove those identifiers before publishing copies. Never publish API keys or credentials.

## Limitations and interpretation

The balanced prompt was created after earlier results were inspected and is exploratory, not a held-out generalization test. The benchmark is small and synthetic, its ten indeterminate items share a repeated structure, and one researcher manually reviewed the gold labels. Only one recorded model identifier and one response per item per condition were evaluated. Confidence values are model self-reports, not calibrated probabilities. The experiment supplied documents directly and did not test retrieval or source authenticity. The proposed Validity-Action Gap was not observed.

Do not use this pilot as a legal, medical, financial, regulatory, or other high-stakes decision system.

## Work provenance and AI assistance

The project package records work completed during the 13-15 November 2026 sprint. The archived working bundle is dated 14 November 2026, but it does not contain full Git history and therefore cannot independently prove creation dates. No pre-sprint source file was identified in the supplied archive. Any known pre-existing code or data must be disclosed explicitly.

AI tools assisted with code drafting/debugging, analysis-script development, and editorial review. The researcher remains responsible for checking the dataset, labels, run records, calculations, references, and final claims.

## Report structure and submission check

The current report is titled **When Evidence Expires: Prompt Sensitivity in Document-Validity Decisions**. Its methodology is Section 4, titled **Method**, with subsections covering the dataset, model and procedure, prompt conditions, metrics and statistical test, and sprint work/code provenance/AI assistance.

The report includes:
- A 150-250 word abstract.
- Introduction, related work, research questions, method, results, discussion, limitations, conclusion, and next study.
- References, excluded from the main-paper page limit.
- Appendix A, titled **Limitations and Dual-Use / Ethical Considerations**, plus public research materials.

The final PDF has been exported by the author. Before submission, check the exported PDF itself to confirm that the main paper is within the required 4-8 pages, excluding references and appendices, and that Appendix A and the public research materials are present.

- [Official report template](https://docs.google.com/document/d/17b3JWki-ZkaqdmqGI5d0gof-HwlGuWU9Mc_1klNZXKs/copy?usp=sharing)
- [Sprint guidelines](https://apartresearch.com/sprints/ai-x-epistemics-research-sprint-2026-11-13-to-2026-11-15#guidelines)
