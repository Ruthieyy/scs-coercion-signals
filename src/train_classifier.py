"""Train and evaluate action/threat/neither classifiers on MFA sentences (codebook v1.2).
Labels: data/labels/agent_labeled.csv (built by src/merge_ai2_labels.py, then src/apply_codebook_v12.py).
  `label` = final label: human (40 spot-checked sentences, hand-labeled by the author, no AI) else AI label under v1.2.
  `agent_v12_label` = AI label under codebook v1.2 for every sentence; `source_v1_1` = 'agent' (Grok Bot assistant) or
  'ai2' (second, independent AI model provided by the author) and defines the split.
Split (no leakage): TRAIN = 282 sentences originally labeled by the assistant (v1.2 labels); TEST = the other 189
  held-out sentences. Two evaluations of the SAME held-out predictions:
  (a) HEADLINE: the 40-sentence human spot-check (subset of TEST), gold = author's adjudicated hand labels;
  (b) all 189 TEST sentences, reference = AI labels re-applied under v1.2 (`agent_v12_label`).
  Website-boilerplate rows are dropped (segment_mfa.is_junk).
Model selection: 5-fold stratified CV on TRAIN only.
Models: (R) silver rules; (B1) TF-IDF char 2-5 + LR; (B2) TF-IDF + LR on silver labels of the whole unlabeled
corpus minus test (weak supervision); (T) frozen multilingual MiniLM-L12 embeddings + LR; (T+B1) average of
probabilities; (T-xl) MiniLM trained EN only, tested ZH.
Final series: chosen family refit on all 471 labels (`label`) and applied to the full corpus."""
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
tr = A[A.source_v1_1 == "agent"].reset_index(drop=True); te = A[A.source_v1_1 == "ai2"].reset_index(drop=True)
te["label"] = te.agent_v12_label  # (b) reference: AI labels under v1.2
hm = te.human_label.notna().values  # (a) human spot-check subset
assert len(te) == 189 and hm.sum() == 40 and not set(tr.sent_id) & set(te.sent_id) and tr.human_label.isna().all()
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
# ---- held-out predictions (model trained on TRAIN only)
preds = {f: fit_predict(f, tr, Etr, te, Ete) for f in NAMES}
yh = te.human_label[hm].values
for f in NAMES: ev(f"(a) human-40 | {NAMES[f]}", yh, preds[f][hm])
for f in NAMES: ev(f"(b) AI-189 v1.2 | {NAMES[f]}", te.label, preds[f])
en = (tr.lang == "en").values; z = (te.lang == "zh").values
ev("(b) AI-189 v1.2 | T-xl: MiniLM trained EN only -> tested ZH", te.label[z], lre().fit(Etr[en], tr.label[en]).predict(Ete[z]))
for lang in ["en", "zh"]:
    q = (te.lang == lang).values; ev(f"(b) AI-189 v1.2 | {best} by language: {lang}", te.label[q], preds[best_f][q])
# annotator agreement on the 40
H = pd.read_csv(ROOT / "data/labels/human_spotcheck_40.csv").set_index("sent_id").join(A.set_index("sent_id")[["ai2_label", "agent_label", "agent_v12_label"]])
def agr(a, b): return dict(agree=int((H[a] == H[b]).sum()), n=len(H), kappa=round(cohen_kappa_score(H[a], H[b]), 3))
ann = {"initial_human vs ai2 (v1.1)": agr("initial_human", "ai2_label"), "initial_human vs assistant (v1.1)": agr("initial_human", "agent_label"),
       "final_human vs ai2 (v1.1)": agr("final_human", "ai2_label"), "final_human vs AI relabeled under v1.2": agr("final_human", "agent_v12_label"),
       "initial_human vs final_human": agr("initial_human", "final_human")}
OLD = ROOT / "data/labels/test_predictions_v1_1.csv"  # frozen held-out predictions of the v1.1 model
old = pd.read_csv(OLD).set_index("sent_id") if OLD.exists() else None
if old is not None and "pred_best" in old:
    o = H.join(old[["pred_best"]]); ann["previous v1.1 ensemble vs initial_human"] = dict(macro_f1=round(f1_score(o.initial_human, o.pred_best, labels=L, average="macro"), 3), kappa=round(cohen_kappa_score(o.initial_human, o.pred_best), 3), n=len(o))
    ann["previous v1.1 ensemble vs final_human"] = dict(macro_f1=round(f1_score(o.final_human, o.pred_best, labels=L, average="macro"), 3), kappa=round(cohen_kappa_score(o.final_human, o.pred_best), 3), n=len(o))
print(json.dumps(ann, indent=1, ensure_ascii=False))
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
json.dump(dict(codebook="v1.2", best=best, selection="5-fold CV macro-F1 on train only", cv_macro_f1=cv,
               annotator_agreement_40=ann, results=res, train_n=len(tr), test_n=len(te), human_n=int(hm.sum())),
          open(ROOT / "reports/classifier_metrics.json", "w"), indent=1, ensure_ascii=False)
bh = res[f"(a) human-40 | {best}"]; ba = res[f"(b) AI-189 v1.2 | {best}"]
F = lambda r, c: r["per_class"][c]["f1-score"]
hl = lambda r: f"macro-F1 **{r['macro_f1']:.3f}**, κ {r['kappa']:.3f}; F1 action {F(r,'action'):.2f}, threat {F(r,'threat'):.2f}, neither {F(r,'neither'):.2f}"
A2 = lambda k: f"{ann[k]['agree']}/{ann[k]['n']}, κ = {ann[k]['kappa']:.3f}"
hdr = ("# Classifier evaluation (codebook v1.2; headline = 40-sentence human spot-check)\n\n"
    "## Iterative codebook validation\n"
    "1. **v1.1, AI annotators only.** The Grok Bot assistant labeled 471 sentences; a second, independent AI model provided by the author "
    "labeled the 189 held-out ones. AI–AI agreement: κ = 0.935.\n"
    f"2. **Human spot-check.** The author hand-labeled (no AI) a stratified random 40-sentence subset of the held-out set. Initial agreement "
    f"with the AI labels was low: {A2('initial_human vs ai2 (v1.1)')} (same vs. the assistant). High AI–AI agreement therefore did not mean the labels matched a human reading.\n"
    f"3. **Adjudication.** The author re-examined the 14 disagreements against the codebook: 7 resolved to the AI label, 6 kept the "
    f"author's initial label, and 1 got a third label (zh011423, flagged borderline). Final human labels vs. v1.1 AI labels: {A2('final_human vs ai2 (v1.1)')}.\n"
    "4. **Codebook v1.2** (decided by the author): revised rule 5 (threat needs addressee + targeted behaviour + adverse outcome, even if "
    "fatalistic) and new rule 10 (action only when a measure is announced/reported; justifying a measure already taken is neither). "
    "The assistant re-applied v1.2 to all 471 sentences (22 relabeled; see `src/apply_codebook_v12.py`). "
    f"Final human vs. v1.2 AI labels on the 40: {A2('final_human vs AI relabeled under v1.2')}. "
    "**Caveat:** this agreement is optimistic, because v1.2 was written from these 40 disagreements and the assistant relabeled knowing the "
    "adjudicated labels; only a fresh human sample can confirm it.\n\n"
    "## Setup\n"
    f"- Train: {len(tr)} assistant-labeled sentences (v1.2 labels). Held-out: {len(te)} sentences, never used for training or model selection.\n"
    "- Model selection: 5-fold stratified CV on the training set only. CV macro-F1: " + ", ".join(f"{k} {v:.3f}" for k, v in cv.items()) + f". Chosen: **{best}**.\n\n"
    "## Results\n"
    f"- **(a) Headline, vs. human labels (n = {int(hm.sum())}):** {hl(bh)}.\n"
    f"- **(b) vs. AI labels under v1.2 (n = {len(te)}):** {hl(ba)}.\n"
    + (f"- Before the revision, the v1.1 ensemble scored macro-F1 {ann['previous v1.1 ensemble vs initial_human']['macro_f1']:.3f} "
       f"(κ {ann['previous v1.1 ensemble vs initial_human']['kappa']:.3f}) against the author's initial labels on the same 40, and "
       f"{ann['previous v1.1 ensemble vs final_human']['macro_f1']:.3f} (κ {ann['previous v1.1 ensemble vs final_human']['kappa']:.3f}) against the final adjudicated labels. "
       "Most of the gain therefore comes from the adjudication/rule revision, not from the retrained model.\n" if "previous v1.1 ensemble vs initial_human" in ann else "")
    + "- **n = 40 is small:** one sentence moves macro-F1 by roughly 0.02–0.05, and per-class F1 rests on 6 action / 14 threat / 20 neither. Read (a) as a sanity check, not a precise estimate.\n\n"
    "| model | macro-F1 (a) human-40 | κ (a) | macro-F1 (b) AI-189 v1.2 | κ (b) |\n|---|---|---|---|---|\n"
    + "\n".join(f"| {NAMES[f]} | {res['(a) human-40 | '+NAMES[f]]['macro_f1']:.3f} | {res['(a) human-40 | '+NAMES[f]]['kappa']:.3f} | {res['(b) AI-189 v1.2 | '+NAMES[f]]['macro_f1']:.3f} | {res['(b) AI-189 v1.2 | '+NAMES[f]]['kappa']:.3f} |" for f in NAMES)
    + "\n\n## Detailed reports\n\n")
cav = ("\n\n## Limitations\n"
    "- **Human validation is limited to 40 sentences** by a single human annotator (the author). Training labels (282) and the (b) reference are AI labels "
    "under codebook v1.2.\n"
    "- **v1.2 was derived from the same 40 sentences** used for the headline, so (a) and the human–AI agreement after revision are optimistic. "
    "A fresh human-labeled sample is needed for an unbiased estimate.\n"
    "- **Enriched test set.** Rule-flagged sentences were oversampled. About 9 in 10 topic sentences in the full corpus are predicted neither, so "
    "population precision for action/threat is likely lower than reported.\n"
    "- **No fine-tuning.** Frozen multilingual MiniLM embeddings + logistic regression (no GPU on the box).\n")
(ROOT / "reports/classifier_metrics.md").write_text(hdr + "\n\n".join(rep) + cav)
print(hdr); print("\n".join(rep)); print(C.groupby(["lang", "pred"]).size())
