"""Crawl Taiwan MND daily 'PLA activities around Taiwan' reports (Chinese site, www.mnd.gov.tw/news/plaact/<id>)
and parse counts: aircraft sorties, sorties crossing median line/entering ADIZ, PLAN ships, official (CCG etc.) ships, balloons.
Output data/processed/mnd_pla_daily.csv. Raw HTML text kept in data/raw/mnd/ (git-ignored)."""
import re, time, html as H, pathlib, requests, pandas as pd, concurrent.futures as cf
ROOT = pathlib.Path(__file__).resolve().parents[1]; RAW = ROOT / "data/raw/mnd"; RAW.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (research; UIUC student project)"}
def get(u):
    for i in range(4):
        try:
            r = requests.get(u, headers=UA, timeout=40)
            if r.status_code == 200: r.encoding = "utf-8"; return r.text
        except Exception: pass
        time.sleep(3 * (i + 1))
def clean(t):
    t = re.sub(r"<(script|style).*?</\1>", "", t, flags=re.S); return H.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t)))
def ids():
    first = get("https://www.mnd.gov.tw/news/plaactlist")
    n = max(int(x) for x in re.findall(r"/news/plaactlist/(\d+)", first)); out = []
    for p in range(1, n + 1):
        t = first if p == 1 else get(f"https://www.mnd.gov.tw/news/plaactlist/{p}")
        if t: out += re.findall(r"news/plaact/(\d+)", t)
        time.sleep(0.3)
    return sorted(set(out), key=int)
def fetch(i):
    f = RAW / f"{i}.txt"
    if f.exists(): return f.read_text()
    t = get(f"https://www.mnd.gov.tw/news/plaact/{i}"); time.sleep(0.3)
    if not t: return None
    c = clean(t); s = c.find("一、日期"); c = c[s: s + 1500] if s >= 0 else c[:3000]
    f.write_text(c); return c
def num(p, s):
    m = re.search(p, s); return int(m.group(1)) if m else None
def parse(i, c):
    """Two formats: (old, 2020-09..~2022-01) one report per day with PLA aircraft entering Taiwan's SW ADIZ, aircraft listed by type;
    (attachment_only) some periods (e.g. 2024-01..06) publish counts only in a PDF/image attachment -> counts left missing, NOT zero;
    (new) daily 0600-0600 report on all PLA aircraft/ships/official ships around Taiwan. Old format has no zero-days and no ships."""
    ds = re.findall(r"(\d{2,3})年(\d{1,2})月(\d{1,2})日", c)
    if not ds: return None
    y, m, dd = ds[1] if "至" in c[:120] and len(ds) > 1 else ds[0]
    new = "共機" in c or "共艦" in c
    air = num(r"共機(\d+)架次", c)
    if air is None:
        sec = c[c.find("二、"): c.find("三、") if "三、" in c else None]
        air = sum(int(x) for x in re.findall(r"(\d+)\s*架次", sec)) or None
    return dict(id=int(i), date=f"{int(y)+1911}-{int(m):02d}-{int(dd):02d}", fmt=("daily_all" if new else "adiz_only") if (air is not None or new) else "attachment_only",
        aircraft=air, aircraft_cross=num(r"共機\d+架次[（(][^）)]*?(\d+)架次", c),
        ships=num(r"共艦(\d+)艘", c), official_ships=num(r"公務船(\d+)艘", c), balloons=num(r"空飄氣球(\d+)", c),
        joint_patrol=int("聯合戰備警巡" in c), text=c[:600])
if __name__ == "__main__":
    import sys
    L = sorted([f.stem for f in (ROOT / "data/raw/mnd").glob("*.txt")], key=int) if "--cached" in sys.argv else ids(); print("ids", len(L), L[:2], L[-2:], flush=True)
    with cf.ThreadPoolExecutor(3) as ex: txt = list(ex.map(fetch, L))
    rows = [r for i, c in zip(L, txt) if c and (r := parse(i, c))]
    df = pd.DataFrame(rows).sort_values(["date", "id"]).groupby("date", as_index=False).agg({"id": "last", "fmt": "last", "aircraft": ["sum", "max"], "aircraft_cross": "max", "ships": "max", "official_ships": "max", "balloons": "max", "joint_patrol": "max", "text": "last"})
    df.columns = ["_".join(c).rstrip("_") if isinstance(c, tuple) else c for c in df.columns]
    df = df.rename(columns={k: k.replace("_last", "").replace("_max", "") for k in df.columns if k not in ("aircraft_sum", "aircraft_max")})
    df["aircraft"] = df.aircraft_max.where(df.fmt == "daily_all", df.aircraft_sum)  # new format: 1 report/day; old: several
    df.loc[df.fmt == "attachment_only", ["aircraft", "aircraft_sum"]] = float("nan")
    (ROOT / "data/processed").mkdir(exist_ok=True); df.to_csv(ROOT / "data/processed/mnd_pla_daily.csv", index=False)
    print(len(df), df.date.min(), df.date.max()); print(df.describe().round(1))
