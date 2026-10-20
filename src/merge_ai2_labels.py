"""Merge the second AI annotator's labels (data/labels/ai2_labeled_raw.csv, exported from the review spreadsheet;
produced by a second, independent AI model provided by the author, NOT by a human) into
data/labels/for_human_review.csv (columns ai2_label, ai2_note; human_label/human_note stay EMPTY) and
data/labels/agent_labeled.csv. agent_labeled.csv keeps the Grok Bot assistant label in `agent_label`; `label`
becomes the second annotator's label where one exists and `label_source` becomes 'ai2' for those rows."""
import pathlib, pandas as pd
from sklearn.metrics import cohen_kappa_score
ROOT = pathlib.Path(__file__).resolve().parents[1]; D = ROOT / "data/labels"
H = pd.read_csv(D / "ai2_labeled_raw.csv").rename(columns={"编号": "sent_id", "你的标签": "ai2_label", "备注": "ai2_note"})
H["ai2_label"] = H.ai2_label.str.strip().str.lower()
assert H.ai2_label.isin(["action", "threat", "neither"]).all() and H.sent_id.is_unique
H = H.set_index("sent_id")[["ai2_label", "ai2_note"]]
R = pd.read_csv(D / "for_human_review.csv")
assert set(R.sent_id) == set(H.index), "review set and ai2 labels differ"
R["ai2_label"] = R.sent_id.map(H.ai2_label); R["ai2_note"] = R.sent_id.map(H.ai2_note)
R["human_label"] = pd.NA; R["human_note"] = pd.NA  # reserved for a real human check
cols = list(R.columns); cols.remove("ai2_label"); cols.remove("ai2_note"); i = cols.index("human_label")
R = R[cols[:i] + ["ai2_label", "ai2_note"] + cols[i:]]; R.to_csv(D / "for_human_review.csv", index=False)
A = pd.read_csv(D / "agent_labeled.csv")
if "agent_label" not in A: A.insert(A.columns.get_loc("label"), "agent_label", A.label)
A["ai2_label"] = A.sent_id.map(H.ai2_label)
A["label"] = A.ai2_label.fillna(A.agent_label)
A["label_source"] = A.ai2_label.notna().map({True: "ai2", False: "agent"})
A.drop(columns="ai2_label").to_csv(D / "agent_labeled.csv", index=False)
# (the planned human spot-check sample data/labels/human_spotcheck_40.csv is built separately; not regenerated here)
k = cohen_kappa_score(R.ai2_label, R.agent_label)
print(f"ai2 n={len(R)}, agree={(R.ai2_label == R.agent_label).sum()}, kappa(agent,ai2)={k:.3f}")
print(pd.crosstab(R.agent_label, R.ai2_label, margins=True)); print(A.label_source.value_counts())
