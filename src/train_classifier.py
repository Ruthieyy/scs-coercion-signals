"""Train and evaluate action/threat/neither classifiers on MFA sentences.
Labels: data/labels/agent_labeled.csv. `label_source` = 'agent' (Grok Bot research assistant, 283 sentences)
or 'ai2' (a second, independent AI model provided by the author, 190 sentences; see src/merge_ai2_labels.py).
NO human labels exist yet (see docs/codebook.md).
Split (no leakage): TRAIN = the agent-labeled sentences (282); TEST = the ai2-labeled sentences (189; the same held-out
split as before). One website-boilerplate row is dropped from each (segment_mfa.is_junk). Evaluation reference = second-annotator (ai2) labels; agent/ai2 disagreements resolved to ai2.
Model selection: 5-fold stratified CV on TRAIN only (the test set is never used to pick a model).
Models: (R) silver rules; (B1) TF-IDF char 2-5 + LR; (B2) TF-IDF + LR on silver labels of the whole unlabeled
corpus minus test (weak supervision); (T) frozen multilingual MiniLM-L12 embeddings + LR; (T+B1) average of
probabilities; (T-xl) MiniLM trained EN only, tested ZH.
Final series: chosen family refit on all 471 labels (ai2 labels where available) and applied to the full corpus."""
import json, sys, pathlib, numpy as np, pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, f1_score, cohen_kappa_score
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from label_rules import label as rule
L = ["action", "threat", "neither"]
from segment_mfa import is_junk
A = pd.read_csv(ROOT / "data/labels/agent_labeled.csv"); A = A[~A.sentence.map(is_junk)]  # drop website boilerplate (2 rows)
C = pd.read_csv(ROOT / "data/processed/mfa_sentences.csv")
tr = A[A.label_source == "agent"].reset_index(drop=True); te = A[A.label_source == "ai2"].reset_index(drop=True)
assert len(te) == 189 and not set(tr.sent_id) & set(te.sent_id)
res, rep = {}, []
def ev(name, y, p, store=True):
    f = f1_score(y, p, labels=L, average="macro"); k = cohen_kappa_score(y, p)
    if store: res[name] = dict(macro_f1=round(f, 3), kappa=round(k, 3), n=len(y),
        per_class=classification_report(y, p, labels=L, output_dict=True, zero_division=0),
        confusion=confusion_matrix(y, p, labels=L).tolist())
    rep.append(f"### {name} (n={len(y)}, macro-F1={f:.3f}, κ={k:.3f})\n```\n{classification_report(y, p, labels=L, zero_division=0)}\nconfusion (rows=true {L}):\n{confusion_matrix(y, p, labels=L)}\n```")
tfidf = lambda: TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), min_df=2, sublinear_tf=True)
lr = lambda: LogisticRegression(max_iter=3000, class_weight="balanced", C=5)
lre = lambda: LogisticRegression(max_iter=3000, class_weight="balanced", C=2)
from sentence_transformers import SentenceTransformer
st = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
E = lambda s: st.encode(list(s), batch_size=64, normalize_embeddings=True, show_progress_bar=False)
Etr, Ete = E(tr.sentence), E(te.sentence)
def fit_predict(fam, a, Ea, b, Eb):
    """fit family on frame a (labels a.label), predict frame b."""
    if fam == "R": return np.array([rule(s, l) for s, l in zip(b.sentence, b.lang)])
    if fam == "B2":
        W = C[~C.sent_id.isin(set(te.sent_id) | set(b.sent_id))]; v = tfidf()
        return lr().fit(v.fit_transform(W.sentence), W.silver).predict(v.transform(b.sentence))
    v = tfidf(); m = lr().fit(v.fit_transform(a.sentence), a.label); pb = m.predict_proba(v.transform(b.sentence))
    if fam == "B1": return m.classes_[pb.argmax(1)]
    mt = lre().fit(Ea, a.label); pe = mt.predict_proba(Eb)
    if fam == "T": return mt.classes_[pe.argmax(1)]
    return m.classes_[(pb + pe).argmax(1)]  # T+B1
NAMES = {"R": "R: silver rules", "B1": "B1: TF-IDF+LR", "B2": "B2: TF-IDF+LR (silver, weak supervision)",
         "T": "T: multilingual MiniLM + LR", "T+B1": "T+B1: average of probabilities"}
# ---- model selection by CV on TRAIN only
cv = {f: [] for f in NAMES}
for a_i, b_i in StratifiedKFold(5, shuffle=True, random_state=0).split(tr, tr.lang + tr.label):
    a, b = tr.iloc[a_i], tr.iloc[b_i]
    for f in NAMES: cv[f].append(f1_score(b.label, fit_predict(f, a, Etr[a_i], b, Etr[b_i]), labels=L, average="macro"))
cv = {f: round(float(np.mean(v)), 3) for f, v in cv.items()}
best_f = max([f for f in NAMES if f != "R"], key=lambda f: cv[f]); best = NAMES[best_f]; print("CV:", cv, "best:", best)
# ---- held-out evaluation vs second-annotator (ai2) labels
preds = {f: fit_predict(f, tr, Etr, te, Ete) for f in NAMES}
for f in NAMES: ev(NAMES[f], te.label, preds[f])
en = (tr.lang == "en").values; z = (te.lang == "zh").values
ev("T-xl: MiniLM trained EN only -> tested ZH", te.label[z], lre().fit(Etr[en], tr.label[en]).predict(Ete[z]))
for lang in ["en", "zh"]:
    k = (te.lang == lang).values; ev(f"{best} by language: {lang}", te.label[k], preds[best_f][k])
# same predictions scored against the AI-assistant labels of the test set (comparability with the earlier report)
vs_agent = {NAMES[f]: dict(macro_f1=round(f1_score(te.agent_label, preds[f], labels=L, average="macro"), 3),
                           kappa=round(cohen_kappa_score(te.agent_label, preds[f]), 3)) for f in NAMES}
k_ah = cohen_kappa_score(te.label, te.agent_label); agree = int((te.label == te.agent_label).sum())
te.assign(pred_best=preds[best_f], pred_T=preds["T"], pred_R=preds["R"]).to_csv(ROOT / "data/labels/test_predictions.csv", index=False)
# ---- final model: best family refit on all labels (ai2 where available), applied to full corpus
EA, EC = E(A.sentence), E(C.sentence)
if best_f in ("T+B1", "B1"):
    vf = tfidf(); mf = lr().fit(vf.fit_transform(A.sentence), A.label); P = mf.predict_proba(vf.transform(C.sentence)); classes = mf.classes_
    if best_f == "T+B1": P = P + lre().fit(EA, A.label).predict_proba(EC)
elif best_f == "T":
    mtf = lre().fit(EA, A.label); P = mtf.predict_proba(EC); classes = mtf.classes_
else:  # B2
    vf = tfidf(); mf = lr().fit(vf.fit_transform(C.sentence), C.silver); P = mf.predict_proba(vf.transform(C.sentence)); classes = mf.classes_
C["pred"] = np.array(classes)[P.argmax(1)]
for i, c in enumerate(classes): C[f"p_{c}"] = P[:, i] / P.sum(1)
C.to_csv(ROOT / "data/processed/mfa_sentences_scored.csv", index=False)
json.dump(dict(gold="ai2 (second independent AI annotator); no human validation", best=best, selection="5-fold CV macro-F1 on train (agent labels)", cv_macro_f1=cv,
               agent_vs_ai2=dict(kappa=round(k_ah, 3), agree=agree, n=len(te)), results=res,
               test_vs_agent_labels=vs_agent, train_n=len(tr), test_n=len(te)),
          open(ROOT / "reports/classifier_metrics.json", "w"), indent=1)
b = res[best]; pc = b["per_class"]
hdr = ("# Classifier evaluation (reference = second AI annotator; no human validation yet)\n\n"
    "> **No human-annotated validation exists yet.** All labels come from two AI annotators. Every number below is "
    "agreement with an AI annotator's reading of `docs/codebook.md`, not accuracy against human judgment. "
    "A human spot-check of a stratified random 40-sentence subset (`data/labels/human_spotcheck_40.csv`) is planned.\n\n"
    f"- **Test set:** {len(te)} held-out sentences labeled by a second, independent AI model provided by the author (`ai2_label` in "
    "`data/labels/for_human_review.csv`). They were never used for training or model selection.\n"
    f"- **Training set:** the other {len(tr)} sentences, labeled by the Grok Bot research assistant (agent labels).\n"
    f"- **Inter-annotator agreement (AI vs. AI) on the test set:** Cohen's κ = {k_ah:.3f} ({agree}/{len(te)} identical). "
    "The 6 disagreements were resolved per codebook rules 5 and 8 (and rules 2–4 for one asserted right to countermeasures), "
    "using the second annotator's labels.\n"
    f"- **Model selection:** 5-fold stratified CV on the training set only. CV macro-F1: "
    + ", ".join(f"{k} {v:.3f}" for k, v in cv.items()) + f". Chosen: **{best}**.\n"
    f"- **Headline (chosen model vs. second-annotator labels):** macro-F1 **{b['macro_f1']:.3f}**, κ {b['kappa']:.3f}; "
    f"F1 action {pc['action']['f1-score']:.2f}, threat {pc['threat']['f1-score']:.2f}, neither {pc['neither']['f1-score']:.2f}.\n\n"
    "| model | macro-F1 vs ai2 | κ vs ai2 | macro-F1 vs agent labels |\n|---|---|---|---|\n"
    + "\n".join(f"| {NAMES[f]} | {res[NAMES[f]]['macro_f1']:.3f} | {res[NAMES[f]]['kappa']:.3f} | {vs_agent[NAMES[f]]['macro_f1']:.3f} |" for f in NAMES)
    + "\n\nThe last column scores the same predictions against the assistant's own labels of the test set, shown only for "
    "comparison with the earlier report (which quoted 0.864 for T+B1, with the model chosen on the test set). "
    "Cite the ai2 column.\n\n")
cav = ("\n\n## Limitations\n"
    "- **No human-annotated validation.** Labels come from two independent AI annotators (Grok Bot assistant: all train + test sentences; "
    "a second AI model provided by the author: the test sentences). κ = %.3f is AI–AI agreement; both may share the same blind spots. "
    "Planned: a human spot-check of a stratified random 40-sentence subset (`data/labels/human_spotcheck_40.csv`).\n"
    "- **Enriched test set.** Rule-flagged sentences were oversampled (test: %d action, %d threat, %d neither). About 9 in 10 topic "
    "sentences in the full corpus are predicted neither, so population precision for action/threat is likely lower than reported.\n"
    "- **Small classes.** With ~20–40 positives per class, per-class F1 has wide uncertainty (roughly ±0.1).\n"
    "- **No fine-tuning.** Frozen multilingual MiniLM embeddings + logistic regression (no GPU on the box).\n") % (
    k_ah, (te.label == "action").sum(), (te.label == "threat").sum(), (te.label == "neither").sum())
(ROOT / "reports/classifier_metrics.md").write_text(hdr + "\n\n".join(rep) + cav)
print(hdr); print("\n".join(rep)); print(C.groupby(["lang", "pred"]).size())
