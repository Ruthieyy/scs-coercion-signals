# Classifier evaluation (codebook v1.2; headline = 40-sentence human spot-check)

## Iterative codebook validation
1. **v1.1, AI annotators only.** The Grok Bot assistant labeled 471 sentences; a second, independent AI model provided by the author labeled the 189 held-out ones. AI–AI agreement: κ = 0.935.
2. **Human spot-check.** The author hand-labeled (no AI) a stratified random 40-sentence subset of the held-out set. Initial agreement with the AI labels was low: 26/40, κ = 0.457 (same vs. the assistant). High AI–AI agreement therefore did not mean the labels matched a human reading.
3. **Adjudication.** The author re-examined the 14 disagreements against the codebook: 7 resolved to the AI label, 6 kept the author's initial label, and 1 got a third label (zh011423, flagged borderline). Final human labels vs. v1.1 AI labels: 33/40, κ = 0.723.
4. **Codebook v1.2** (decided by the author): revised rule 5 (threat needs addressee + targeted behaviour + adverse outcome, even if fatalistic) and new rule 10 (action only when a measure is announced/reported; justifying a measure already taken is neither). The assistant re-applied v1.2 to all 471 sentences (22 relabeled; see `src/apply_codebook_v12.py`). Final human vs. v1.2 AI labels on the 40: 38/40, κ = 0.916. **Caveat:** this agreement is optimistic, because v1.2 was written from these 40 disagreements and the assistant relabeled knowing the adjudicated labels; only a fresh human sample can confirm it.

## Setup
- Train: 282 assistant-labeled sentences (v1.2 labels). Held-out: 189 sentences, never used for training or model selection.
- Model selection: 5-fold stratified CV on the training set only. CV macro-F1: R 0.729, B1 0.776, B2 0.734, T 0.809, T+B1 0.840. Chosen: **T+B1: average of probabilities**.

## Results
- **(a) Headline, vs. human labels (n = 40):** macro-F1 **0.880**, κ 0.791; F1 action 0.92, threat 0.83, neither 0.88.
- **(b) vs. AI labels under v1.2 (n = 189):** macro-F1 **0.845**, κ 0.734; F1 action 0.85, threat 0.77, neither 0.92.
- Before the revision, the v1.1 ensemble scored macro-F1 0.644 (κ 0.455) against the author's initial labels on the same 40, and 0.821 (κ 0.716) against the final adjudicated labels. Most of the gain therefore comes from the adjudication/rule revision, not from the retrained model.
- **n = 40 is small:** one sentence moves macro-F1 by roughly 0.02–0.05, and per-class F1 rests on 6 action / 14 threat / 20 neither. Read (a) as a sanity check, not a precise estimate.

| model | macro-F1 (a) human-40 | κ (a) | macro-F1 (b) AI-189 v1.2 | κ (b) |
|---|---|---|---|---|
| R: silver rules | 0.750 | 0.618 | 0.684 | 0.515 |
| B1: TF-IDF+LR | 0.875 | 0.749 | 0.829 | 0.688 |
| B2: TF-IDF+LR (silver, weak supervision) | 0.900 | 0.795 | 0.779 | 0.638 |
| T: multilingual MiniLM + LR | 0.829 | 0.714 | 0.784 | 0.649 |
| T+B1: average of probabilities | 0.880 | 0.791 | 0.845 | 0.734 |

## Detailed reports

### (a) human-40 | R: silver rules (n=40, macro-F1=0.750, κ=0.618)
```
              precision    recall  f1-score   support

      action       0.60      1.00      0.75         6
      threat       0.72      0.93      0.81        14
     neither       0.92      0.55      0.69        20

    accuracy                           0.75        40
   macro avg       0.75      0.83      0.75        40
weighted avg       0.80      0.75      0.74        40

confusion (rows=true ['action', 'threat', 'neither']):
[[ 6  0  0]
 [ 0 13  1]
 [ 4  5 11]]
```

### (a) human-40 | B1: TF-IDF+LR (n=40, macro-F1=0.875, κ=0.749)
```
              precision    recall  f1-score   support

      action       1.00      1.00      1.00         6
      threat       0.83      0.71      0.77        14
     neither       0.82      0.90      0.86        20

    accuracy                           0.85        40
   macro avg       0.88      0.87      0.88        40
weighted avg       0.85      0.85      0.85        40

confusion (rows=true ['action', 'threat', 'neither']):
[[ 6  0  0]
 [ 0 10  4]
 [ 0  2 18]]
```

### (a) human-40 | B2: TF-IDF+LR (silver, weak supervision) (n=40, macro-F1=0.900, κ=0.795)
```
              precision    recall  f1-score   support

      action       1.00      1.00      1.00         6
      threat       0.80      0.86      0.83        14
     neither       0.89      0.85      0.87        20

    accuracy                           0.88        40
   macro avg       0.90      0.90      0.90        40
weighted avg       0.88      0.88      0.88        40

confusion (rows=true ['action', 'threat', 'neither']):
[[ 6  0  0]
 [ 0 12  2]
 [ 0  3 17]]
```

### (a) human-40 | T: multilingual MiniLM + LR (n=40, macro-F1=0.829, κ=0.714)
```
              precision    recall  f1-score   support

      action       0.75      1.00      0.86         6
      threat       0.91      0.71      0.80        14
     neither       0.81      0.85      0.83        20

    accuracy                           0.82        40
   macro avg       0.82      0.85      0.83        40
weighted avg       0.84      0.82      0.82        40

confusion (rows=true ['action', 'threat', 'neither']):
[[ 6  0  0]
 [ 0 10  4]
 [ 2  1 17]]
```

### (a) human-40 | T+B1: average of probabilities (n=40, macro-F1=0.880, κ=0.791)
```
              precision    recall  f1-score   support

      action       0.86      1.00      0.92         6
      threat       1.00      0.71      0.83        14
     neither       0.83      0.95      0.88        20

    accuracy                           0.88        40
   macro avg       0.89      0.89      0.88        40
weighted avg       0.89      0.88      0.87        40

confusion (rows=true ['action', 'threat', 'neither']):
[[ 6  0  0]
 [ 0 10  4]
 [ 1  0 19]]
```

### (b) AI-189 v1.2 | R: silver rules (n=189, macro-F1=0.684, κ=0.515)
```
              precision    recall  f1-score   support

      action       0.45      1.00      0.62        15
      threat       0.51      0.92      0.66        38
     neither       0.98      0.63      0.77       136

    accuracy                           0.72       189
   macro avg       0.65      0.85      0.68       189
weighted avg       0.84      0.72      0.73       189

confusion (rows=true ['action', 'threat', 'neither']):
[[15  0  0]
 [ 1 35  2]
 [17 33 86]]
```

### (b) AI-189 v1.2 | B1: TF-IDF+LR (n=189, macro-F1=0.829, κ=0.688)
```
              precision    recall  f1-score   support

      action       0.87      0.87      0.87        15
      threat       0.70      0.74      0.72        38
     neither       0.91      0.90      0.90       136

    accuracy                           0.86       189
   macro avg       0.83      0.83      0.83       189
weighted avg       0.86      0.86      0.86       189

confusion (rows=true ['action', 'threat', 'neither']):
[[ 13   0   2]
 [  0  28  10]
 [  2  12 122]]
```

### (b) AI-189 v1.2 | B2: TF-IDF+LR (silver, weak supervision) (n=189, macro-F1=0.779, κ=0.638)
```
              precision    recall  f1-score   support

      action       0.64      0.93      0.76        15
      threat       0.62      0.84      0.71        38
     neither       0.95      0.80      0.87       136

    accuracy                           0.82       189
   macro avg       0.73      0.86      0.78       189
weighted avg       0.86      0.82      0.83       189

confusion (rows=true ['action', 'threat', 'neither']):
[[ 14   0   1]
 [  1  32   5]
 [  7  20 109]]
```

### (b) AI-189 v1.2 | T: multilingual MiniLM + LR (n=189, macro-F1=0.784, κ=0.649)
```
              precision    recall  f1-score   support

      action       0.64      0.93      0.76        15
      threat       0.68      0.74      0.71        38
     neither       0.92      0.85      0.89       136

    accuracy                           0.84       189
   macro avg       0.75      0.84      0.78       189
weighted avg       0.85      0.84      0.84       189

confusion (rows=true ['action', 'threat', 'neither']):
[[ 14   0   1]
 [  1  28   9]
 [  7  13 116]]
```

### (b) AI-189 v1.2 | T+B1: average of probabilities (n=189, macro-F1=0.845, κ=0.734)
```
              precision    recall  f1-score   support

      action       0.78      0.93      0.85        15
      threat       0.80      0.74      0.77        38
     neither       0.92      0.92      0.92       136

    accuracy                           0.88       189
   macro avg       0.83      0.86      0.84       189
weighted avg       0.88      0.88      0.88       189

confusion (rows=true ['action', 'threat', 'neither']):
[[ 14   0   1]
 [  0  28  10]
 [  4   7 125]]
```

### (b) AI-189 v1.2 | T-xl: MiniLM trained EN only -> tested ZH (n=77, macro-F1=0.785, κ=0.661)
```
              precision    recall  f1-score   support

      action       0.60      1.00      0.75         6
      threat       0.68      0.76      0.72        17
     neither       0.94      0.83      0.88        54

    accuracy                           0.83        77
   macro avg       0.74      0.87      0.78        77
weighted avg       0.86      0.83      0.84        77

confusion (rows=true ['action', 'threat', 'neither']):
[[ 6  0  0]
 [ 1 13  3]
 [ 3  6 45]]
```

### (b) AI-189 v1.2 | T+B1: average of probabilities by language: en (n=112, macro-F1=0.879, κ=0.808)
```
              precision    recall  f1-score   support

      action       0.80      0.89      0.84         9
      threat       0.89      0.81      0.85        21
     neither       0.94      0.95      0.95        82

    accuracy                           0.92       112
   macro avg       0.88      0.88      0.88       112
weighted avg       0.92      0.92      0.92       112

confusion (rows=true ['action', 'threat', 'neither']):
[[ 8  0  1]
 [ 0 17  4]
 [ 2  2 78]]
```

### (b) AI-189 v1.2 | T+B1: average of probabilities by language: zh (n=77, macro-F1=0.801, κ=0.636)
```
              precision    recall  f1-score   support

      action       0.75      1.00      0.86         6
      threat       0.69      0.65      0.67        17
     neither       0.89      0.87      0.88        54

    accuracy                           0.83        77
   macro avg       0.77      0.84      0.80        77
weighted avg       0.83      0.83      0.83        77

confusion (rows=true ['action', 'threat', 'neither']):
[[ 6  0  0]
 [ 0 11  6]
 [ 2  5 47]]
```

## Limitations
- **Human validation is limited to 40 sentences** by a single human annotator (the author). Training labels (282) and the (b) reference are AI labels under codebook v1.2.
- **v1.2 was derived from the same 40 sentences** used for the headline, so (a) and the human–AI agreement after revision are optimistic. A fresh human-labeled sample is needed for an unbiased estimate.
- **Enriched test set.** Rule-flagged sentences were oversampled. About 9 in 10 topic sentences in the full corpus are predicted neither, so population precision for action/threat is likely lower than reported.
- **No fine-tuning.** Frozen multilingual MiniLM embeddings + logistic regression (no GPU on the box).
