"""Daily text/activity signals:
- MFA (classifier output, data/processed/mfa_sentences_scored.csv): per press-conference day, share and count of
  predicted threat / action sentences on the Taiwan/SCS topic set; EN and ZH averaged where both exist.
  'threat_novel' excludes boilerplate formulas (red-line formula, 'do not underestimate', 'play with fire').
- Taiwan MND daily PLA activity (data/processed/mnd_pla_daily.csv): aircraft, ships, official ships.
Output data/processed/text_signals_daily.csv (NaN on days without a press conference / report)."""
import re, pathlib, pandas as pd, numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[1]
BOIL = re.compile(r"red line|underestimate|play(ing)? with fire|红线|低估|玩火|自焚|core of China’s core|核心利益中的核心", re.I)
C = pd.read_csv(ROOT / "data/processed/mfa_sentences_scored.csv", parse_dates=["date"])
C["threat_novel"] = (C.pred == "threat") & ~C.sentence.str.contains(BOIL)
g = C.groupby(["date", "lang"]).agg(n=("pred", "size"), threat=("pred", lambda s: (s == "threat").sum()),
        action=("pred", lambda s: (s == "action").sum()), threat_novel=("threat_novel", "sum"))
for k in ["threat", "action", "threat_novel"]: g[f"{k}_share"] = g[k] / g.n
D = g.groupby("date").mean(numeric_only=True)
D = D.rename(columns=lambda c: "mfa_" + c)
M = pd.read_csv(ROOT / "data/processed/mnd_pla_daily.csv", parse_dates=["date"]).set_index("date")
M = M[["fmt", "aircraft", "aircraft_cross", "ships", "official_ships", "joint_patrol"]].add_prefix("mnd_")
out = D.join(M, how="outer").sort_index(); out.to_csv(ROOT / "data/processed/text_signals_daily.csv")
print(out.describe().T.round(2)); print(out.index.min(), out.index.max())
