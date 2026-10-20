"""Assemble aligned daily panel: PortWatch chokepoint transits + GDELT signal volumes
+ weather controls (IBTrACS, ERA5 waves) + curated event flags (by public_date)."""
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
    for f in sorted(RAW.glob("gdelt_signal_*.json")) + [RAW / "gdelt_doc_hist.json"]:
        if not f.exists(): continue
        name = "taiwan_strait_all" if f.name == "gdelt_doc_hist.json" else f.stem.replace("gdelt_signal_", "")
        s = pd.DataFrame(json.loads(f.read_text())["timeline"][0]["data"])
        s["date"] = pd.to_datetime(s["date"].str[:8]); s = s.set_index("date")
        out["gdelt_" + name] = s["value"] / s["norm"].replace(0, np.nan) * 1e5  # per 100k articles
    return pd.DataFrame(out)

def main():
    ev = pd.read_csv(RAW / "coercion_events_curated.csv", parse_dates=["event_date", "end_date", "public_date"])
    panel = load_portwatch().join(load_gdelt(), how="left")
    wx = PROC / "weather_controls.csv"
    if wx.exists(): panel = panel.join(pd.read_csv(wx, index_col=0, parse_dates=True), how="left")
    for th in ["taiwan", "scs_ph", "scs_other"]:
        sub = ev[ev.theater.eq(th)] if th != "scs_other" else ev[~ev.theater.isin(["taiwan", "scs_ph"])]
        for cat in ["action", "threat"]:
            flag = pd.Series(0, index=panel.index)
            for _, r in sub[sub.category.eq(cat)].iterrows():
                flag[(flag.index >= r.public_date) & (flag.index <= max(r.end_date, r.public_date))] = 1
            panel[f"event_{th}_{cat}"] = flag
    PROC.mkdir(exist_ok=True, parents=True); panel.to_csv(PROC / "daily_panel.csv")
    print(panel.shape, panel.index.min().date(), panel.index.max().date())
if __name__ == "__main__":
    main()
