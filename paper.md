# When Evidence Expires: Prompt Sensitivity in Document-Validity Decisions

**Project:** ExpiryBench v0.1  
**Author:** Fawaz Ibrahim  
**Affiliation:** Independent researcher  
**Evaluation date:** 14 November 2026  
**Model identifier recorded by the runner:** `gpt-6-luna`

## Abstract

Language models often see documents issued at different times, but publication, effective, expiry, and replacement dates mean different things. A later publication does not necessarily replace an older document, and the absence of an expiry date does not prove continued validity. We created ExpiryBench, a 40-item synthetic pilot dataset with four labels: CURRENT, EXPIRED, NOT_YET_EFFECTIVE, and INDETERMINATE. Each item asks a model to classify a target document and select the governing document or abstain when the evidence is insufficient.

We evaluated one recorded model identifier on the same 40 items under three prompts: a neutral baseline, a one-sided temporal reminder, and a balanced reminder. Each condition produced 40 completed responses. Joint accuracy was 95%, 82.5%, and 100%, respectively. Indeterminate-case accuracy was 80%, 30%, and 100%. A paired exact McNemar test favoured the balanced prompt over the temporal hint on seven discordant items and none in the opposite direction (p = 0.015625; Holm-adjusted p = 0.046875). The balanced-versus-neutral difference was not significant (p = 0.50).

The balanced prompt was designed after the first two conditions had been inspected, so its perfect score is exploratory and may reflect alignment with the dataset's repeated indeterminate pattern. All errors occurred in indeterminate cases. The pilot suggests prompt wording can affect whether a model abstains when temporal evidence is incomplete, but it does not establish general temporal reasoning ability.

## 1. Introduction

A document's publication date does not necessarily establish when it becomes effective. Nor does the absence of an expiry date establish that a document remains in force. When two documents are supplied, a model may need to distinguish a known replacement from a later publication that has not yet taken effect, or from a record that leaves continued validity unresolved.

The initial project also proposed measuring a **Validity–Action Gap**: a case in which the model's status classification is correct but its document-selection action is wrong. This pilot did not produce such a case. The results instead point to prompt sensitivity in situations where the supplied evidence does not establish whether an older document remains valid.

This project is primarily a Track 1 Model Epistemics and Decision-Making Evaluation. It tests a concrete decision behaviour: whether a model distinguishes evidence of expiry or replacement from evidence that leaves validity unresolved, and whether it abstains when the supplied record is insufficient [8].

## 2. Related Work

Research on temporal reasoning has examined date interpretation and temporal bias in language models. DateLogicQA studies date-related reasoning across past, present, and future contexts [1]. EvolveBench evaluates temporal awareness, including the handling of temporally misaligned evidence [2]. TIDE examines version resolution in evolving official documents [3]. Recent work on stale-document poisoning studies how outdated retrieved evidence can change otherwise correct model answers [4]. ExpiryBench is narrower than these efforts: it tests a small set of explicit document-status distinctions and asks the model to make a corresponding selection or abstention.

The sprint's Track 1 reading list also highlights the problem of models guessing when evidence is weak. Kalai et al. argue that common evaluation incentives can reward guesses over acknowledging uncertainty [5]. The MASK benchmark makes a related but distinct point by separating factual accuracy from honesty under pressure [6]. A broader design sketch for epistemic-virtue evaluations motivates testing whether models communicate uncertainty and avoid misleading claims [7]. ExpiryBench studies only a narrower behaviour: whether a model chooses an evidence-supported document action or abstains in a synthetic temporal-validity task. It does not test deception, lying, or honesty under adversarial pressure.


## 3. Research questions

The study asks:

1. How accurately does the model classify four temporal-validity categories?
2. Does its document-selection action agree with the gold action, including abstention when the evidence is insufficient?
3. Does adding temporal guidance change performance, especially on indeterminate cases?

The initial hypotheses were that indeterminate cases would be harder than cases with explicit validity terms; that a model might mistake a newer publication for proof of replacement; and that status and action could diverge. The prompt comparison was exploratory. In particular, the balanced condition was designed after the first two conditions had been scored.

## 4. Method

### 4.1 Dataset

ExpiryBench v0.1 contains 40 fictional document pairs, with 10 items in each category.

| Label | Operational meaning |
|---|---|
| CURRENT | The target document is established as governing on the query date. |
| EXPIRED | The target document's stated validity has ended by the query date. |
| NOT_YET_EFFECTIVE | The target document has been published, but its effective date is after the query date. |
| INDETERMINATE | The supplied evidence does not establish whether the target document remains valid or which document governs. |

The available actions are `A`, `B`, and `ABSTAIN`. For NOT_YET_EFFECTIVE items, Document B is the target and Document A remains in force until B becomes effective. The dataset contains synthetic text, dates, questions, gold labels, gold actions, and reference rationales. The researcher manually reviewed all 40 labels for date consistency and whether the supplied evidence supported the gold answer. No second independent annotator was used.

The JSONL dataset SHA-256 is:

`f38f1d2695a43fc2999363a6b494583e5690843902934d82954c1b90ab07b585`

### 4.2 Model and procedure

The recorded model identifier was `gpt-6-luna`. The same 40 items were evaluated once under each prompt condition, giving 120 completed responses. Browsing and external tools were not enabled. The model returned a structured response with a status, selected document, confidence from 0 to 100, and rationale. Reasoning effort was set to low. Failed API attempts were not included in the 120 successful responses. The original unmodified append-only run log should be retained privately. The sanitized public neutral and temporal-hint log is available at `runs_openai.jsonl`; its audit notes are in `RAW_RUNS_STATUS.md`.

The exact model identifier is reported as recorded by the experiment runner. The paper does not infer a public model family or claim that this identifier is independently reproducible outside the account and date of the run. The public repository now includes a sanitized append-only log for the neutral and temporal-hint conditions. That file contains 119 attempt records: 80 completed responses (40 per condition), 38 failed API connection attempts, and one incomplete neutral response. The 80 completed outputs were rescored directly from the stored responses and match the reported joint accuracies of 95% (neutral) and 82.5% (temporal hint). Provider-generated response identifiers were removed from the public copy. The separate 40-response balanced-hint log is not included, so the balanced-hint results and the full 120-response summary cannot yet be independently reproduced from the public raw logs. The audit and redaction details are documented in `RAW_RUNS_STATUS.md`.

### 4.3 Prompt conditions

**Neutral.** The base task instructions asked the model to use only the supplied documents, classify the target document on the query date, choose the governing document, and abstain if the evidence did not establish which document governs.

**Temporal hint.** The same base instructions were followed by this reminder: publication date, effective date, and expiration or replacement date are distinct; a later publication does not by itself prove that an earlier document has ceased to apply.

**Balanced hint.** The base instructions were followed by a longer reminder. It repeated the publication/effective/expiry distinction, added that the absence of an expiration date does not prove continued validity, stated that a future-effective document does not govern before its effective date, and repeated the instruction to abstain when the evidence does not establish which document governs.

The balanced condition was introduced after examining the first two conditions' results. It is an exploratory follow-up, not a preregistered or independently held-out intervention. Because the balanced prompt contains several additional statements, this experiment cannot identify which sentence caused the change.

### 4.4 Metrics and statistical test

Status accuracy and action accuracy are the proportions of correct status labels and actions. Joint accuracy requires both to be correct. Indeterminate false-definitive action counts an A or B selection on an INDETERMINATE item where the gold action is ABSTAIN. The Validity–Action Gap counts an incorrect action among responses with a correct status classification.

We used the exact two-sided McNemar test for paired item-level comparisons. The test is based on discordant pairs, not on treating the two prompt conditions as independent samples. Holm adjustment was calculated across the three pairwise comparisons among the prompt conditions.

### 4.5 Sprint work, code provenance, and AI assistance

ExpiryBench v0.1 was assembled during the 13-15 November 2026 AI x Epistemics Research Sprint. The initial working bundle preserved in the project archive is dated 14 November 2026 and contains the dataset generator, 40-item dataset, initial neutral and temporal-hint evaluation runner, scoring utility, protocol draft, and initial paper draft. Subsequent sprint work added the balanced prompt after the first two conditions had been inspected, extended the runner to support that condition, added paired McNemar and Holm analysis, and revised the report and supporting documentation. No pre-sprint repository or source file is identified in the supplied archive. The archive does not include a complete version-control history, so its timestamps should not be treated as an independent audit of authorship or file creation.

AI tools assisted with code drafting/debugging and editorial review. The researcher remains responsible for the dataset, labels, experimental outputs, metrics, references, and conclusions.

## 5. Results

### 5.1 Overall and category accuracy

| Metric | Neutral | Temporal hint | Balanced hint |
|---|---:|---:|---:|
| Completed responses | 40/40 | 40/40 | 40/40 |
| Status accuracy | 95% | 82.5% | 100% |
| Action accuracy | 95% | 82.5% | 100% |
| Joint accuracy | 95% | 82.5% | 100% |
| Indeterminate accuracy | 8/10 | 3/10 | 10/10 |
| False definitive actions on indeterminate items | 2/10 | 7/10 | 0/10 |
| Validity–Action Gap | 0/38 | 0/33 | 0/40 |

| Gold category | Neutral | Temporal hint | Balanced hint |
|---|---:|---:|---:|
| CURRENT | 10/10 | 10/10 | 10/10 |
| EXPIRED | 10/10 | 10/10 | 10/10 |
| INDETERMINATE | 8/10 | 3/10 | 10/10 |
| NOT_YET_EFFECTIVE | 10/10 | 10/10 | 10/10 |

All observed errors occurred in the INDETERMINATE category. In this dataset, status accuracy, action accuracy, and joint accuracy were identical because each incorrect status prediction was accompanied by an incorrect action.

### 5.2 Paired comparisons

| Comparison | Both correct | First condition only | Second condition only | Both wrong | Exact McNemar p |
|---|---:|---:|---:|---:|---:|
| Neutral vs temporal hint | 32 | 6 | 1 | 1 | 0.125 |
| Balanced hint vs neutral | 38 | 2 | 0 | 0 | 0.500 |
| Balanced hint vs temporal hint | 33 | 7 | 0 | 0 | 0.015625 |

For balanced hint versus temporal hint, all seven discordant items favoured the balanced condition. Each was an indeterminate case. The exact two-sided McNemar p-value was 0.015625. After Holm adjustment across all three pairwise comparisons, the adjusted p-value was 0.046875.

For balanced hint versus neutral, two items favoured the balanced condition and none favoured neutral. The exact p-value was 0.50, so the observed five-percentage-point difference is not statistically significant in this paired test. The neutral-versus-temporal-hint comparison also did not reach the 0.05 threshold (p = 0.125).

### 5.3 Indeterminate responses

Under the balanced prompt, all ten indeterminate items were classified as INDETERMINATE and assigned ABSTAIN. The model's rationales generally stated that Document A had taken effect but that the supplied text did not establish whether it remained valid. They also noted that Document B had a future effective date and did not explicitly say it replaced A.

For EB-038, the model wrote that A had taken effect, but the documents did not establish whether it remained valid; B was not effective until a later date and did not say it replaced A. The model selected ABSTAIN and assigned 96% confidence. This is an example of the model following the intended rule in this item. It is not evidence that the confidence score is calibrated.

### 5.4 Validity–Action Gap

No response had a correct status classification paired with an incorrect action. The measured gap was therefore zero in all three conditions. This is a null result for the proposed construct in this dataset. It does not show that such a gap cannot occur; the current items may not separate status recognition from action selection strongly enough to expose it.

## 6. Discussion

The main pattern is concentrated in the indeterminate items. The one-sided reminder was associated with lower accuracy than the neutral prompt, while the balanced reminder was associated with higher accuracy than either of the first two conditions. The seven-item difference between balanced and one-sided guidance was statistically significant under the paired test and remained below 0.05 after Holm adjustment across the three pairwise comparisons. The two-item difference between balanced and neutral was not significant.

One plausible reading is that the one-sided reminder made the model less likely to treat a later publication as evidence of replacement, but did not also guard against assuming that an older document remains valid when no expiry date is supplied. The balanced reminder addressed both possibilities and explicitly repeated the abstention rule. The observed outputs are consistent with that explanation, but the design cannot isolate the effect of any one sentence.

The 100% balanced-condition score should be interpreted carefully. The prompt was constructed after the first two sets of errors had been inspected, and its wording directly describes the logic used to create the indeterminate cases. The ten indeterminate items also share a common structure. The result therefore shows that this model followed a closely matched instruction on this pilot dataset. It does not demonstrate general temporal reasoning or establish performance on unseen documents.

The initial Validity–Action Gap hypothesis was not observed. The model's errors linked status and action: when the status was wrong, the action was also wrong. Future benchmark items should include cases where the status is clear but choosing the governing document requires a separate comparison or interpretation.

## 7. Limitations

1. **Synthetic, small dataset.** Forty items cannot represent the range of real policy, legal, medical, software, or administrative document histories.
2. **Repeated indeterminate structure.** The ten indeterminate cases share a similar construction. Their results may reflect recognition of a repeated template.
3. **One model and one run per item.** The study does not estimate variation across models, model versions, or repeated samples.
4. **Post-hoc balanced prompt.** The third condition was designed after inspecting earlier errors, so its result is exploratory and susceptible to overfitting to the benchmark structure.
5. **Single annotator.** The gold labels were manually audited by one researcher. Independent annotation and adjudication are still needed.
6. **No real retrieval or source verification.** Both documents were supplied directly. The study does not test document discovery, authenticity, missing-source retrieval, or external legal validity.
7. **Confidence is not calibrated.** The reported confidence values are model self-reports. The pilot does not establish their probabilistic meaning.
8. **No observed Validity–Action Gap.** The dataset did not produce the failure mode originally proposed, so conclusions about that construct are limited.

## 8. Conclusion

On this 40-item synthetic pilot, prompt wording changed the model's performance on indeterminate document-validity cases. The neutral condition achieved 95% joint accuracy, the one-sided temporal reminder 82.5%, and the balanced reminder 100%. The paired difference between balanced and one-sided guidance was significant after correction for the three pairwise comparisons. The balanced-versus-neutral difference was not significant.

The result is a prompt-sensitivity finding, not evidence that the model has acquired a general ability to resolve document validity. The balanced prompt was developed after earlier results were known and closely matched the structure of the indeterminate items. A stronger follow-up needs a larger, more varied, independently annotated benchmark, multiple models, repeated runs, and prompt conditions frozen before evaluation.

## 9. Next study

A follow-up version should add different forms of uncertainty: missing replacement records, conflicting dates, partial amendment histories, unclear continuity clauses, and documents that refer to unavailable appendices. It should include cases where the status label is correct but selecting the governing document requires a separate reasoning step. At least two annotators should label the items independently before adjudication. Prompt conditions should be fixed in advance, and evaluation should include multiple models and repeated trials. Any real-world examples should be supported by verifiable source histories.


## References

[1] Gagan Bhatia, MingZe Tang, Cristina Mahanta, Madiha Kazi, Maxime Peyrard, and Wei Zhao. 2025. “DateLogicQA: Benchmarking Temporal Biases in Large Language Models.” *Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 4: Student Research Workshop*, 321–332. Association for Computational Linguistics. https://doi.org/10.18653/v1/2025.naacl-srw.32

[2] Zhiyuan Zhu, Yusheng Liao, Zhe Chen, Yuhao Wang, Yunfeng Guan, Yanfeng Wang, and Yu Wang. 2025. “EvolveBench: A Comprehensive Benchmark for Assessing Temporal Awareness in LLMs on Evolving Knowledge.” *Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, 16173–16188. https://doi.org/10.18653/v1/2025.acl-long.788

[3] Mahbub E. Sobhani, Md. Faiyaz Abdullah Sayeedi, Fahmid Hasan Chowdhury, Md Adnan Arefeen, Farig Sadeque, Md. Faizul Bari, and Swakkhar Shatabda. 2026. “Time Present and Time Past: Benchmarking Large Language Models on Temporally Evolving Document Understanding (TIDE).” arXiv:2608.08512. https://arxiv.org/abs/2608.08512

[4] Md Shamim Ahmed, Lukas Galke Poech, and Richard Röttger. 2026. “Stale-Document Poisoning: When Outdated Retrieval Overrides Correct Model Answers.” arXiv:2609.31342. https://arxiv.org/abs/2609.31342

[5] Adam Tauman Kalai, Ofir Nachum, Santosh S. Vempala, and Edwin Zhang. 2025. “Why Language Models Hallucinate.” arXiv:2509.04664. https://arxiv.org/abs/2509.04664

[6] Richard Ren, Arunim Agarwal, Mantas Mazeika, Cristina Menghini, Robert Vacareanu, Brad Kenstler, Mick Yang, Isabelle Barrass, Alice Gatti, Xuwang Yin, Eduardo Trevino, Matias Geralnik, Adam Khoja, Dean Lee, Summer Yue, and Dan Hendrycks. 2025, revised 2026. “The MASK Benchmark: Disentangling Honesty From Accuracy in AI Systems.” arXiv:2503.03750. https://arxiv.org/abs/2503.03750

[7] Owen Cotton-Barratt, Lizka Vaintrob, and Oly Sourbut. 2025. “Design Sketches: Collective Epistemics.” Forethought, 25 December 2025. https://www.forethought.org/research/design-sketches-collective-epistemics

[8] Apart Research. 2026. “AI x Epistemics Research Sprint: Guidelines and Resources.” https://apartresearch.com/sprints/ai-x-epistemics-research-sprint-2026-11-13-to-2026-11-15#guidelines


## Appendix A. Limitations and Dual-Use / Ethical Considerations

### What the results establish

The results describe one recorded model identifier, `gpt-6-luna`, evaluated once on each of 40 synthetic scenarios under three prompt conditions. They show that, on this particular dataset, the model's status/action decisions on indeterminate cases varied with prompt wording. The paired comparison between the balanced and temporal-hint conditions favoured the balanced condition on seven discordant items and on none in the opposite direction. The balanced-versus-neutral comparison was not statistically significant.

### What the results do not establish

The results do not establish general temporal reasoning ability, reliable performance on unseen documents, or safety for high-stakes use. The balanced prompt was designed after earlier outputs had been examined and closely mirrors the construction of the indeterminate cases. The dataset is small, synthetic, and manually labelled by one researcher. Only one model identifier and one run per item were tested. Confidence values are self-reports, not calibrated probabilities. Documents were supplied directly, so the experiment did not test retrieval, document authenticity, provenance, or external legal validity. The proposed Validity-Action Gap was not observed, and the current items may not separate classification from document selection sufficiently to measure it.

### Dual-use and misuse risks

A temporal-validity evaluator could be used constructively to flag uncertainty before people rely on outdated or prematurely effective documents. The same capability could also be misused to give selective or misleading support to a preferred document: for example, by presenting incomplete date metadata as proof that a rule has expired, by implying that a newly published document has already replaced an existing one, or by treating the absence of an expiry date as proof of continued validity. A user could also cite a high benchmark score as false reassurance that an AI system can make legal, regulatory, employment, financial, or medical determinations.

We reduced these risks in this pilot by using entirely fictional documents, avoiding live policy or personal records, reporting abstention as a valid action, and describing the benchmark as exploratory rather than as a certification or deployment-ready decision system. The dataset and scores should not be used to settle real disputes or to authoritatively decide which real-world document governs. Any future real-world application would require verifiable primary sources, complete amendment histories, independent expert review, human decision authority, and evaluation on representative held-out cases.

### Privacy, data handling, and human review

The v0.1 dataset contains fictional text and dates and no personal data. No human-subject data were collected. The gold labels were reviewed by one researcher; independent annotation and adjudication remain future work. The public neutral and temporal-hint log was screened for obvious API keys, bearer tokens, authorization-header values, private-key markers, and email addresses. No matches were found by that pattern-based screening, which is not a guarantee that every possible sensitive value has been ruled out. Provider-generated response identifiers were removed from the public copy, while experimental outputs and relevant metadata were retained. The original unmodified append-only log should be kept in private storage. The balanced-hint raw log is not included in the public repository.

### AI assistance and accountability

AI tools were used to assist with code drafting and debugging, analysis-script development, and editorial review. The researcher is responsible for checking the underlying records, confirming the metrics and bibliographic details, and approving every claim in the report. The use of AI assistance does not transfer responsibility for the accuracy of the submission.

## Public research materials

The public repository contains the prompt descriptions, results summary, sanitized neutral and temporal-hint run log, and raw-log audit notes: https://github.com/fawazfff/expirybench. The balanced-hint raw response log is not included, so the public repository does not yet provide a complete raw-data reproduction of all three conditions.
