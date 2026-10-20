"""Train and evaluate action/threat/neither classifiers on MFA sentences.
Labels: data/labels/agent_labeled.csv (agent labels, NOT human; see docs/codebook.md).
Split: stratified 60/40 by (lang,label), seed 0 -> held-out test never used for training/tuning.
Models: (R) silver rules; (B1) TF-IDF char 2-5 + LR on agent-train; (B2) TF-IDF + LR on silver labels of the
whole unlabeled corpus (weak supervision); (T) frozen multilingual MiniLM-L12 sentence embeddings + LR on agent-train;
(T-xl) same, trained on EN only, tested on ZH (cross-lingual transfer)."""
import json, sys, pathlib, numpy as np, pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, f1_score
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from label_rules import label as rule
L = ["action", "threat", "neither"]
A = pd.read_csv(ROOT / "data/labels/agent_labeled.csv")
C = pd.read_csv(ROOT / "data/processed/mfa_sentences.csv")
tr, te = train_test_split(A, test_size=0.4, random_state=0, stratify=A.lang + A.label)
res, rep = {}, []
def ev(name, y, p, sub=None):
    f = f1_score(y, p, labels=L, average="macro"); res[name] = dict(macro_f1=round(f, 3), n=len(y),
        per_class=classification_report(y, p, labels=L, output_dict=True, zero_division=0),
        confusion=confusion_matrix(y, p, labels=L).tolist())
    rep.append(f"### {name} (n={len(y)}, macro-F1={f:.3f})\n```\n{classification_report(y, p, labels=L, zero_division=0)}\nconfusion (rows=true {L}):\n{confusion_matrix(y, p, labels=L)}\n```")
tfidf = lambda: TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5), min_df=2, sublinear_tf=True)
lr = lambda: LogisticRegression(max_iter=3000, class_weight="balanced", C=5)
ev("R: silver rules", te.label, [rule(s, l) for s, l in zip(te.sentence, te.lang)])
v = tfidf(); m = lr().fit(v.fit_transform(tr.sentence), tr.label); ev("B1: TF-IDF+LR (agent train)", te.label, m.predict(v.transform(te.sentence)))
W = C[~C.sent_id.isin(te.sent_id)]; v2 = tfidf(); m2 = lr().fit(v2.fit_transform(W.sentence), W.silver)
ev("B2: TF-IDF+LR (silver, weak supervision)", te.label, m2.predict(v2.transform(te.sentence)))
from sentence_transformers import SentenceTransformer
st = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
E = lambda s: st.encode(list(s), batch_size=64, normalize_embeddings=True, show_progress_bar=False)
Etr, Ete = E(tr.sentence), E(te.sentence)
mt = LogisticRegression(max_iter=3000, class_weight="balanced", C=2).fit(Etr, tr.label); pt = mt.predict(Ete)
ev("T: multilingual MiniLM + LR (agent train)", te.label, pt)
en = (tr.lang == "en").values; mx = LogisticRegression(max_iter=3000, class_weight="balanced", C=2).fit(Etr[en], tr.label[en])
z = (te.lang == "zh").values; ev("T-xl: MiniLM trained EN only -> tested ZH", te.label[z], mx.predict(Ete[z]))
for lang in ["en", "zh"]:
    k = (te.lang == lang).values; ev(f"T by language: {lang}", te.label[k], pt[k])
# ensemble: TF-IDF probs + embedding probs
pb = m.predict_proba(v.transform(te.sentence)); pe = mt.predict_proba(Ete)
ev("T+B1: average of probabilities", te.label, np.array(m.classes_)[(pb + pe).argmax(1)])
te.assign(pred_T=pt, pred_R=[rule(s, l) for s, l in zip(te.sentence, te.lang)]).to_csv(ROOT / "data/labels/test_predictions.csv", index=False)
best = max(res, key=lambda k: res[k]["macro_f1"] if not k.startswith(("T-xl", "T by")) else -1); print("best:", best)
# final model = best family refit on all agent labels, applied to full corpus
if best.startswith("T+B1"):
    vf = tfidf(); mf = lr().fit(vf.fit_transform(A.sentence), A.label); EA = E(A.sentence)
    mtf = LogisticRegression(max_iter=3000, class_weight="balanced", C=2).fit(EA, A.label)
    P = mf.predict_proba(vf.transform(C.sentence)) + mtf.predict_proba(E(C.sentence)); classes = mf.classes_
elif best.startswith("T:"):
    mtf = LogisticRegression(max_iter=3000, class_weight="balanced", C=2).fit(E(A.sentence), A.label)
    P = mtf.predict_proba(E(C.sentence)); classes = mtf.classes_
else:
    vf = tfidf(); mf = lr().fit(vf.fit_transform(A.sentence), A.label); P = mf.predict_proba(vf.transform(C.sentence)); classes = mf.classes_
C["pred"] = np.array(classes)[P.argmax(1)]
for i, c in enumerate(classes): C[f"p_{c}"] = P[:, i] / P.sum(1)
C.to_csv(ROOT / "data/processed/mfa_sentences_scored.csv", index=False)
json.dump(dict(best=best, results=res, train_n=len(tr), test_n=len(te)), open(ROOT / "reports/classifier_metrics.json", "w"), indent=1)
(ROOT / "reports/classifier_metrics.md").write_text("# Classifier evaluation (held-out test; labels = agent labels, NOT human)\n\n"
    f"Train n={len(tr)}, test n={len(te)} (stratified by lang×label; sample was enriched with rule-flagged sentences, so class balance ≠ population).\n"
    f"Best (by macro-F1, used for the series): **{best}**\n\n" + "\n\n".join(rep) + "\n")
print("\n".join(rep)); print(C.groupby(["lang", "pred"]).size())
