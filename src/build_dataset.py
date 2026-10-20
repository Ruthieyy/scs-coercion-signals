"""Assemble aligned daily panel: PortWatch chokepoint transits + GDELT signal volumes + curated events."""
import json, pathlib, pandas as pd, numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW, PROC = ROOT / "data/raw", ROOT / "data/processed"

def load_portwatch():
    df = pd.read_csv(RAW / "portwatch_scs_chokepoints.csv", parse_dates=["date"])
    w = df.pivot_table(index="date", columns="portname", values="n_total", aggfunc="sum")
    w.columns = ["transits_" + c.lower().replace(" ", "_") for c in w.columns]
    return w

def load_gdelt():
    out = {}
    files = sorted(RAW.glob("gdelt_signal_*.json")) + [RAW / "gdelt_doc_hist.json"]
    for f in files:
        if not f.exists(): continue
        name = "taiwan_strait_all" if f.name == "gdelt_doc_hist.json" else f.stem.replace("gdelt_signal_", "")
        tl = json.loads(f.read_text())["timeline"][0]["data"]
        s = pd.DataFrame(tl)
        s["date"] = pd.to_datetime(s["date"].str[:8])
        s = s.set_index("date")
        # share of all monitored articles (per 100k) -> removes GDELT corpus-size drift
        out["gdelt_" + name] = s["value"] / s["norm"].replace(0, np.nan) * 1e5
    return pd.DataFrame(out)

def load_events():
    ev = pd.read_csv(RAW / "coercion_events_curated.csv", parse_dates=["start_date", "end_date"])
    return ev

def main():
    pw, gd, ev = load_portwatch(), load_gdelt(), load_events()
    panel = pw.join(gd, how="left")
    for th in ["taiwan", "scs"]:
        flag = pd.Series(0, index=panel.index)
        for _, r in ev[ev.theater.str.startswith(th)].iterrows():
            flag[(flag.index >= r.start_date) & (flag.index <= r.end_date)] = 1
        panel[f"event_{th}"] = flag
    PROC.mkdir(exist_ok=True, parents=True)
    panel.to_csv(PROC / "daily_panel.csv")
    print(panel.shape, panel.index.min().date(), panel.index.max().date())
    print(panel.notna().sum())
if __name__ == "__main__":
    main()
