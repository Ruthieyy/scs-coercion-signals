"""Weather controls per chokepoint: IBTrACS tropical-cyclone proximity + ERA5 (Open-Meteo marine) max wave height.
Outputs data/processed/weather_controls.csv (daily, 2019-01-01..)."""
import pathlib, numpy as np, pandas as pd, requests, time
ROOT = pathlib.Path(__file__).resolve().parents[1]; RAW = ROOT / "data/raw"; PROC = ROOT / "data/processed"
# representative open-water points for each PortWatch chokepoint
PTS = {"taiwan_strait": (24.0, 119.5), "luzon_strait": (20.5, 121.0), "balabac_strait": (7.6, 117.0),
       "mindoro_strait": (12.6, 120.3), "malacca_strait": (2.5, 101.5)}
START, END = "2019-01-01", "2026-10-11"
def hav(lat1, lon1, lat2, lon2):
    p = np.pi / 180; a = np.sin((lat2-lat1)*p/2)**2 + np.cos(lat1*p)*np.cos(lat2*p)*np.sin((lon2-lon1)*p/2)**2
    return 12742 * np.arcsin(np.sqrt(a))
def ibtracs():
    f = RAW / "ibtracs_WP.csv"
    if not f.exists():
        url = "https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/ibtracs.WP.list.v04r01.csv"
        f.write_bytes(requests.get(url, timeout=300).content)
    d = pd.read_csv(f, skiprows=[1], usecols=["SID", "ISO_TIME", "LAT", "LON", "USA_WIND", "WMO_WIND"], low_memory=False)
    d["t"] = pd.to_datetime(d.ISO_TIME); d = d[(d.t >= START)]
    for c in ["LAT", "LON", "USA_WIND", "WMO_WIND"]: d[c] = pd.to_numeric(d[c], errors="coerce")
    d["wind"] = d[["USA_WIND", "WMO_WIND"]].max(axis=1).fillna(0); d["date"] = d.t.dt.normalize()
    out = pd.DataFrame(index=pd.date_range(START, END, freq="D"))
    for k, (la, lo) in PTS.items():
        dist = hav(la, lo, d.LAT.values, d.LON.values)
        near = d[(dist <= 300) & (d.wind >= 34)]   # tropical-storm strength within 300 km
        near5 = d.assign(dist=dist)[dist <= 500]
        out[f"tc300_{k}"] = out.index.isin(near.date).astype(int)
        out[f"tcwind500_{k}"] = near5.groupby("date").wind.max().reindex(out.index).fillna(0)
    return out
def waves():
    out = {}
    for k, (la, lo) in PTS.items():
        r = requests.get("https://marine-api.open-meteo.com/v1/marine", params=dict(latitude=la, longitude=lo,
            daily="wave_height_max", start_date=START, end_date=END, models="era5_ocean"), timeout=120).json()
        out[f"wave_{k}"] = pd.Series(r["daily"]["wave_height_max"], index=pd.to_datetime(r["daily"]["time"]), dtype=float)
        time.sleep(1)
    return pd.DataFrame(out)
if __name__ == "__main__":
    w = ibtracs().join(waves()); PROC.mkdir(parents=True, exist_ok=True)
    w.to_csv(PROC / "weather_controls.csv"); print(w.describe().T.round(2))
