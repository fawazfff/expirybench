# ExpiryBench v0.1: final protocol and deviations

## Research question

Can a language model distinguish known expiry from uncertain current validity, and how does temporal guidance in the prompt affect status classification and document-selection decisions?

## Dataset

The frozen dataset contains 40 synthetic document-pair scenarios, 10 in each of four labels: CURRENT, EXPIRED, NOT_YET_EFFECTIVE, and INDETERMINATE. The JSONL SHA-256 is `f38f1d2695a43fc2999363a6b494583e5690843902934d82954c1b90ab07b585`.

A single researcher manually audited the 40 gold labels for date consistency and evidence support. No independent second annotator participated. The ten indeterminate items share a similar template and should not be treated as structurally diverse examples.

## Model and procedure

The model identifier recorded by the runner was `gpt-6-luna`. All 40 items were run once under each of three prompt conditions, with browsing and external tools disabled and reasoning effort set to low. The model returned status, action, confidence, and rationale in a strict JSON schema. There are 120 completed responses in total.

## Prompt conditions

- Neutral: base task instructions only.
- Temporal hint: base instructions plus a reminder that publication date, effective date, and expiry/replacement date are distinct, and that a later publication does not prove replacement.
- Balanced hint: base instructions plus a reminder covering both non-automatic replacement and the fact that a missing expiry date does not prove continued validity, plus the future-effective-date and abstention rules.

**Protocol deviation:** The balanced hint was designed after the neutral and temporal-hint results were inspected. It is a post-hoc exploratory condition, not a preregistered condition. The intervention includes multiple additional statements, so the effect of any one sentence cannot be isolated.

## Outcomes

Primary: status accuracy, action accuracy, and joint accuracy. Secondary: per-class accuracy, false definitive actions on indeterminate cases, and the Validity-Action Gap (wrong action among cases with correct status). Confidence scores are exploratory self-reports, not calibrated probabilities.

## Statistical analysis

The same items were compared pairwise using the exact two-sided McNemar test. Holm adjustment was applied across all three pairwise comparisons. Report discordant-pair counts alongside p-values. The results are exploratory given the sample size and post-hoc prompt design.

## Results snapshot

- Neutral: 38/40 joint correct (95%); indeterminate 8/10.
- Temporal hint: 33/40 joint correct (82.5%); indeterminate 3/10.
- Balanced hint: 40/40 joint correct (100%); indeterminate 10/10.
- Balanced vs temporal hint: 7 items favoured balanced, none favoured temporal hint; exact McNemar p = 0.015625; Holm-adjusted p = 0.046875.
- Balanced vs neutral: 2 items favoured balanced, none favoured neutral; exact p = 0.50.
- Neutral vs temporal hint: 6 items favoured neutral, 1 favoured temporal hint; exact p = 0.125.
- No Validity-Action Gap cases were observed.

## Reproduction and raw records

The public repository contains the 40-item dataset, deterministic generator, evaluation runner, scoring utility, paired-analysis script, and sanitized run logs for all three prompt conditions. The first append-only log contains neutral and temporal-hint attempts, including 38 failed API attempts and one incomplete response, alongside the 80 completed responses. The balanced-hint log contains 40 completed responses. Provider-generated response identifiers were removed from the public copies. The original unmodified logs should be retained privately.

The balanced-hint log has zero latency values throughout. Do not use it for latency or speed claims. Pattern-based security checks found no obvious API keys, bearer tokens, authorization-header values, private-key markers, or email addresses; this screening is not a guarantee that every possible sensitive value has been excluded.

## Sprint provenance and AI assistance

The project was assembled during the 13-15 November 2026 sprint. The archived initial bundle is dated 14 November 2026 and contains the initial dataset, generator, neutral/temporal-hint runner, scorer, protocol draft, and initial paper draft. Later sprint work added the post-hoc balanced prompt, support for that arm, paired McNemar/Holm analysis, and the revised report. No pre-sprint repository or code is identified in the supplied archive; the archive does not preserve complete Git history.

AI tools assisted with code drafting/debugging, analysis-script development, and editorial review. The researcher remains responsible for validating the dataset, labels, experimental records, metrics, references, and final claims.
