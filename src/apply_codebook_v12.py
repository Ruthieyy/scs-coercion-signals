"""Codebook v1.2 (decided by the author after the 40-sentence human spot-check; see docs/codebook.md).
1) Human gold: merges the author's hand labels for data/labels/human_spotcheck_40.csv (initial labels from
   data/labels/human_spotcheck_40_results.csv; final adjudicated labels for the 14 disagreements are in FINAL below,
   which override the spreadsheet's 最终标签 column) -> human_spotcheck_40.csv, for_human_review.csv (human_label),
   agent_labeled.csv (human_label, label_source='human').
2) Re-applies revised rule 5 and new rule 10 to all 471 AI-labeled sentences. Candidates were every sentence with a
   fatalistic phrase (注定/死路/自取灭亡/没有出路/doomed/dead end/perish/...), every 正告/警告/warn/beware sentence and every
   action-labeled sentence; each was read individually by the AI assistant and relabeled only where v1.2 changes the
   outcome (V12 below, with reasons). Changed rows get label_source='agent_v1.2'; previous labels stay in
   `label_v1_1` (pre-revision gold) / `agent_label` (original assistant) / `ai2_label` (second AI annotator).
Idempotent: always rebuilds from the stored previous-label columns."""
import pathlib, pandas as pd
ROOT = pathlib.Path(__file__).resolve().parents[1]; D = ROOT / "data/labels"
FINAL = dict(en008910="neither", en003321="neither", en003769="threat", en001298="neither", zh015366="threat",
             en007463="neither", zh010234="neither", zh009871="action", en002848="neither", zh016514="neither",
             en001361="neither", zh011423="neither", en003687="action", en002903="threat")
BORDERLINE = {"zh011423": "borderline (author): mostly stance about the drills, slight warning"}
J = "rule 10: justifies / restates the purpose or legitimacy of a measure already taken -> neither"
T5 = "rule 5 (v1.2): explicit addressee + targeted behaviour + adverse outcome -> threat even if phrased fatalistically"
V12 = {  # sent_id: (new label, reason)
    "en006129": ("neither", "rule 10: generic 'CCG takes necessary measures to safeguard sovereignty', no specific measure announced (borderline)"),
    "zh016788": ("neither", J), "en008501": ("neither", J), "zh016770": ("neither", J), "zh012805": ("neither", J),
    "zh016986": ("neither", J), "zh012860": ("neither", J + " ('我愿再次重申')"), "en008712": ("neither", J),
    "en001298": ("neither", J + " ('with the aim of ... fully legitimate')"), "zh015247": ("neither", J),
    "zh011423": ("neither", J + " (drills described as punishment/warning)"), "zh016604": ("neither", J),
    "zh016514": ("neither", J + " ('我们已经清楚地阐明 ... 正当、合理、合法')"), "en008279": ("neither", J),
    "en002903": ("neither", J + "; 'a warning to separatists' has no adverse outcome, so not threat under rule 5"),
    "zh011019": ("neither", "not a PRC measure: describes other states' joint patrol (correction under base definition)"),
    "en007784": ("threat", T5 + " ('Taiwan authorities should beware ... doomed to fail')"),
    "zh015440": ("threat", T5 + " ('再次正告台湾当局 ... 注定以失败告终')"),
    "zh015366": ("threat", T5 + " ('正告台湾当局，台独是死路一条')"),
    "en009372": ("threat", T5 + " ('make it clear to the Taiwan authorities ... dead end'; borderline: 'make it clear to' rather than 'warn')"),
    "en001361": ("neither", "rule 5 (v1.2): no explicit addressee/adverse outcome for an addressed party; resolve statement (rule 6)"),
    "en001878": ("threat", "rule 7 consistency: 'Those who play with fire will perish by it' -> threat (identical sentences were already threat)"),
}
A = pd.read_csv(D / "agent_labeled.csv")
if "label_v1_1" not in A:
    rv = pd.read_csv(D / "for_human_review.csv").set_index("sent_id")
    A.insert(A.columns.get_loc("label"), "ai2_label", A.sent_id.map(rv.ai2_label))
    A.insert(A.columns.get_loc("label"), "label_v1_1", A.label)
    A.insert(A.columns.get_loc("label"), "source_v1_1", A.label_source)
assert set(V12) <= set(A.sent_id)
A["agent_v12_label"] = A.label_v1_1
A["v12_reason"] = ""
for k, (lab, why) in V12.items():
    i = A.sent_id == k; A.loc[i, "agent_v12_label"] = lab; A.loc[i, "v12_reason"] = why
changed = A.agent_v12_label != A.label_v1_1
# human spot-check
R = pd.read_csv(D / "human_spotcheck_40_results.csv").set_index("sent_id")
S = pd.read_csv(D / "human_spotcheck_40.csv")
assert set(S.sent_id) == set(R.index) and set(FINAL) <= set(S.sent_id)
S["initial_human"] = S.sent_id.map(R.human.str.strip().str.lower())
S["final_human"] = [FINAL.get(s, ih) for s, ih in zip(S.sent_id, S.initial_human)]
S["adjudicated"] = S.sent_id.isin(FINAL)
S["borderline"] = S.sent_id.isin(BORDERLINE)
S["human_label"] = S.final_human
S["human_note"] = [BORDERLINE.get(s, "" if pd.isna(n) else n) for s, n in zip(S.sent_id, S.sent_id.map(R.note))]
S.to_csv(D / "human_spotcheck_40.csv", index=False)
H = S.set_index("sent_id")
rv = pd.read_csv(D / "for_human_review.csv")
rv["human_label"] = rv.sent_id.map(H.human_label); rv["human_note"] = rv.sent_id.map(H.human_note)
rv.to_csv(D / "for_human_review.csv", index=False)
A["human_label"] = A.sent_id.map(H.human_label)
A["label"] = A.human_label.fillna(A.agent_v12_label)
A["label_source"] = A.source_v1_1.where(~changed, "agent_v1.2").where(A.human_label.isna(), "human")
A.to_csv(D / "agent_labeled.csv", index=False)
print(f"v1.2 relabels: {changed.sum()} of {len(A)} (train/agent: {(changed & (A.source_v1_1=='agent')).sum()}, test/ai2: {(changed & (A.source_v1_1=='ai2')).sum()})")
print(pd.crosstab(A.label_v1_1[changed], A.agent_v12_label[changed]))
print(A.label_source.value_counts())
