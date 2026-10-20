# Classifier evaluation (held-out test; labels = agent labels, NOT human)

Train n=283, test n=190 (stratified by lang×label; sample was enriched with rule-flagged sentences, so class balance ≠ population).
Best (by macro-F1, used for the series): **T+B1: average of probabilities**

### R: silver rules (n=190, macro-F1=0.757)
```
              precision    recall  f1-score   support

      action       0.64      0.91      0.75        23
      threat       0.57      0.93      0.71        42
     neither       0.98      0.70      0.81       125

    accuracy                           0.77       190
   macro avg       0.73      0.85      0.76       190
weighted avg       0.85      0.77      0.78       190

confusion (rows=true ['action', 'threat', 'neither']):
[[21  2  0]
 [ 1 39  2]
 [11 27 87]]
```

### B1: TF-IDF+LR (agent train) (n=190, macro-F1=0.834)
```
              precision    recall  f1-score   support

      action       0.83      0.83      0.83        23
      threat       0.79      0.74      0.77        42
     neither       0.90      0.92      0.91       125

    accuracy                           0.87       190
   macro avg       0.84      0.83      0.83       190
weighted avg       0.87      0.87      0.87       190

confusion (rows=true ['action', 'threat', 'neither']):
[[ 19   2   2]
 [  0  31  11]
 [  4   6 115]]
```

### B2: TF-IDF+LR (silver, weak supervision) (n=190, macro-F1=0.752)
```
              precision    recall  f1-score   support

      action       0.73      0.70      0.71        23
      threat       0.63      0.81      0.71        42
     neither       0.88      0.80      0.84       125

    accuracy                           0.79       190
   macro avg       0.74      0.77      0.75       190
weighted avg       0.80      0.79      0.79       190

confusion (rows=true ['action', 'threat', 'neither']):
[[ 16   0   7]
 [  1  34   7]
 [  5  20 100]]
```

### T: multilingual MiniLM + LR (agent train) (n=190, macro-F1=0.803)
```
              precision    recall  f1-score   support

      action       0.71      0.87      0.78        23
      threat       0.76      0.74      0.75        42
     neither       0.89      0.86      0.88       125

    accuracy                           0.84       190
   macro avg       0.79      0.82      0.80       190
weighted avg       0.84      0.84      0.84       190

confusion (rows=true ['action', 'threat', 'neither']):
[[ 20   1   2]
 [  0  31  11]
 [  8   9 108]]
```

### T-xl: MiniLM trained EN only -> tested ZH (n=78, macro-F1=0.772)
```
              precision    recall  f1-score   support

      action       0.67      0.73      0.70        11
      threat       0.75      0.79      0.77        19
     neither       0.87      0.83      0.85        48

    accuracy                           0.81        78
   macro avg       0.76      0.78      0.77        78
weighted avg       0.81      0.81      0.81        78

confusion (rows=true ['action', 'threat', 'neither']):
[[ 8  1  2]
 [ 0 15  4]
 [ 4  4 40]]
```

### T by language: en (n=112, macro-F1=0.815)
```
              precision    recall  f1-score   support

      action       0.83      0.83      0.83        12
      threat       0.79      0.65      0.71        23
     neither       0.88      0.92      0.90        77

    accuracy                           0.86       112
   macro avg       0.83      0.80      0.82       112
weighted avg       0.85      0.86      0.85       112

confusion (rows=true ['action', 'threat', 'neither']):
[[10  0  2]
 [ 0 15  8]
 [ 2  4 71]]
```

### T by language: zh (n=78, macro-F1=0.787)
```
              precision    recall  f1-score   support

      action       0.62      0.91      0.74        11
      threat       0.73      0.84      0.78        19
     neither       0.93      0.77      0.84        48

    accuracy                           0.81        78
   macro avg       0.76      0.84      0.79        78
weighted avg       0.83      0.81      0.81        78

confusion (rows=true ['action', 'threat', 'neither']):
[[10  1  0]
 [ 0 16  3]
 [ 6  5 37]]
```

### T+B1: average of probabilities (n=190, macro-F1=0.864)
```
              precision    recall  f1-score   support

      action       0.87      0.87      0.87        23
      threat       0.84      0.76      0.80        42
     neither       0.91      0.94      0.92       125

    accuracy                           0.89       190
   macro avg       0.87      0.86      0.86       190
weighted avg       0.89      0.89      0.89       190

confusion (rows=true ['action', 'threat', 'neither']):
[[ 20   1   2]
 [  0  32  10]
 [  3   5 117]]
```

## Caveats on label quality (read before citing any number above)
- **Labels are agent labels.** The AI assistant applied all 473 labels blind to the rule label, following `docs/codebook.md`. No human has checked them yet. There was a single annotator, so there is no inter-annotator agreement measure. Every metric here therefore measures agreement with one annotator's reading of the codebook.
- **Enriched test set.** Rule-flagged action and threat sentences were oversampled, so the test set has about 12% action, 22% threat and 66% neither. In the full corpus, about 91% of topic sentences are predicted neither. Precision for action and threat in the population is therefore likely lower than reported.
- **Selection bias.** The ensemble was chosen by macro-F1 on the same test set, so its 0.864 is slightly optimistic.
- **No fine-tuning.** The box has no GPU and little RAM, so the transformer is frozen multilingual MiniLM embeddings with logistic regression, not a fine-tuned model.
- **Human validation.** The file to check is `data/labels/for_human_review.csv`: the 190 test sentences with blank `human_label` and `human_note` columns. Once it is filled in, agent-vs-human agreement (Cohen's κ) can be computed and the metrics recomputed against human labels.
