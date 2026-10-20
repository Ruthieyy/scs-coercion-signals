# Classifier evaluation (reference = second AI annotator; no human validation yet)

> **No human-annotated validation exists yet.** All labels come from two AI annotators. Every number below is agreement with an AI annotator's reading of `docs/codebook.md`, not accuracy against human judgment. A human spot-check of a stratified random 40-sentence subset (`data/labels/human_spotcheck_40.csv`) is planned.

- **Test set:** 189 held-out sentences labeled by a second, independent AI model provided by the author (`ai2_label` in `data/labels/for_human_review.csv`). They were never used for training or model selection.
- **Training set:** the other 282 sentences, labeled by the Grok Bot research assistant (agent labels).
- **Inter-annotator agreement (AI vs. AI) on the test set:** Cohen's κ = 0.935 (183/189 identical). The 6 disagreements were resolved per codebook rules 5 and 8 (and rules 2–4 for one asserted right to countermeasures), using the second annotator's labels.
- **Model selection:** 5-fold stratified CV on the training set only. CV macro-F1: R 0.767, B1 0.801, B2 0.784, T 0.821, T+B1 0.864. Chosen: **T+B1: average of probabilities**.
- **Headline (chosen model vs. second-annotator labels):** macro-F1 **0.859**, κ 0.758; F1 action 0.89, threat 0.77, neither 0.91.

| model | macro-F1 vs ai2 | κ vs ai2 | macro-F1 vs agent labels |
|---|---|---|---|
| R: silver rules | 0.733 | 0.569 | 0.757 |
| B1: TF-IDF+LR | 0.828 | 0.715 | 0.833 |
| B2: TF-IDF+LR (silver, weak supervision) | 0.747 | 0.588 | 0.760 |
| T: multilingual MiniLM + LR | 0.797 | 0.664 | 0.803 |
| T+B1: average of probabilities | 0.859 | 0.758 | 0.863 |

The last column scores the same predictions against the assistant's own labels of the test set, shown only for comparison with the earlier report (which quoted 0.864 for T+B1, with the model chosen on the test set). Cite the ai2 column.

### R: silver rules (n=189, macro-F1=0.733, κ=0.569)
```
              precision    recall  f1-score   support

      action       0.64      0.95      0.76        22
      threat       0.50      0.92      0.65        37
     neither       0.98      0.66      0.79       130

    accuracy                           0.75       189
   macro avg       0.70      0.85      0.73       189
weighted avg       0.84      0.75      0.76       189

confusion (rows=true ['action', 'threat', 'neither']):
[[21  1  0]
 [ 1 34  2]
 [11 33 86]]
```

### B1: TF-IDF+LR (n=189, macro-F1=0.828, κ=0.715)
```
              precision    recall  f1-score   support

      action       0.83      0.86      0.84        22
      threat       0.72      0.76      0.74        37
     neither       0.91      0.89      0.90       130

    accuracy                           0.86       189
   macro avg       0.82      0.84      0.83       189
weighted avg       0.86      0.86      0.86       189

confusion (rows=true ['action', 'threat', 'neither']):
[[ 19   1   2]
 [  0  28   9]
 [  4  10 116]]
```

### B2: TF-IDF+LR (silver, weak supervision) (n=189, macro-F1=0.747, κ=0.588)
```
              precision    recall  f1-score   support

      action       0.73      0.73      0.73        22
      threat       0.58      0.81      0.67        37
     neither       0.90      0.79      0.84       130

    accuracy                           0.79       189
   macro avg       0.73      0.78      0.75       189
weighted avg       0.81      0.79      0.79       189

confusion (rows=true ['action', 'threat', 'neither']):
[[ 16   0   6]
 [  1  30   6]
 [  5  22 103]]
```

### T: multilingual MiniLM + LR (n=189, macro-F1=0.797, κ=0.664)
```
              precision    recall  f1-score   support

      action       0.71      0.91      0.80        22
      threat       0.68      0.76      0.72        37
     neither       0.91      0.84      0.87       130

    accuracy                           0.83       189
   macro avg       0.77      0.83      0.80       189
weighted avg       0.84      0.83      0.83       189

confusion (rows=true ['action', 'threat', 'neither']):
[[ 20   0   2]
 [  0  28   9]
 [  8  13 109]]
```

### T+B1: average of probabilities (n=189, macro-F1=0.859, κ=0.758)
```
              precision    recall  f1-score   support

      action       0.87      0.91      0.89        22
      threat       0.76      0.78      0.77        37
     neither       0.92      0.91      0.91       130

    accuracy                           0.88       189
   macro avg       0.85      0.87      0.86       189
weighted avg       0.88      0.88      0.88       189

confusion (rows=true ['action', 'threat', 'neither']):
[[ 20   0   2]
 [  0  29   8]
 [  3   9 118]]
```

### T-xl: MiniLM trained EN only -> tested ZH (n=77, macro-F1=0.761, κ=0.614)
```
              precision    recall  f1-score   support

      action       0.67      0.80      0.73        10
      threat       0.65      0.81      0.72        16
     neither       0.89      0.78      0.83        51

    accuracy                           0.79        77
   macro avg       0.74      0.80      0.76        77
weighted avg       0.81      0.79      0.80        77

confusion (rows=true ['action', 'threat', 'neither']):
[[ 8  0  2]
 [ 0 13  3]
 [ 4  7 40]]
```

### T+B1: average of probabilities by language: en (n=112, macro-F1=0.903, κ=0.836)
```
              precision    recall  f1-score   support

      action       1.00      0.83      0.91        12
      threat       0.89      0.81      0.85        21
     neither       0.93      0.97      0.95        79

    accuracy                           0.93       112
   macro avg       0.94      0.87      0.90       112
weighted avg       0.93      0.93      0.93       112

confusion (rows=true ['action', 'threat', 'neither']):
[[10  0  2]
 [ 0 17  4]
 [ 0  2 77]]
```

### T+B1: average of probabilities by language: zh (n=77, macro-F1=0.803, κ=0.663)
```
              precision    recall  f1-score   support

      action       0.77      1.00      0.87        10
      threat       0.63      0.75      0.69        16
     neither       0.91      0.80      0.85        51

    accuracy                           0.82        77
   macro avg       0.77      0.85      0.80        77
weighted avg       0.83      0.82      0.82        77

confusion (rows=true ['action', 'threat', 'neither']):
[[10  0  0]
 [ 0 12  4]
 [ 3  7 41]]
```

## Limitations
- **No human-annotated validation.** Labels come from two independent AI annotators (Grok Bot assistant: all train + test sentences; a second AI model provided by the author: the test sentences). κ = 0.935 is AI–AI agreement; both may share the same blind spots. Planned: a human spot-check of a stratified random 40-sentence subset (`data/labels/human_spotcheck_40.csv`).
- **Enriched test set.** Rule-flagged sentences were oversampled (test: 22 action, 37 threat, 130 neither). About 9 in 10 topic sentences in the full corpus are predicted neither, so population precision for action/threat is likely lower than reported.
- **Small classes.** With ~20–40 positives per class, per-class F1 has wide uncertainty (roughly ±0.1).
- **No fine-tuning.** Frozen multilingual MiniLM embeddings + logistic regression (no GPU on the box).
