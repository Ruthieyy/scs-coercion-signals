"""Fetch daily GDELT DOC 2.0 article-volume timelines for coercion-signal queries.
Rate limit: ~1 request / 5 s. Output: data/raw/gdelt_signal_<name>.json
"""
import json, time, sys, pathlib, requests
API = "https://api.gdeltproject.org/api/v2/doc/doc"
QUERIES = {
    # 'acts' (Caldara-Iacoviello style): physical coercive actions
    "taiwan_drills": '"Taiwan Strait" (drills OR exercise OR blockade)',
    "ccg_water_cannon": '("coast guard" OR "China Coast Guard") ("water cannon" OR rammed OR collision)',
    "shoal_standoff": '("Second Thomas Shoal" OR "Scarborough Shoal" OR "Sabina Shoal")',
    # 'threats': rhetoric / warnings
    "china_warns_scs": '("South China Sea" OR Taiwan) China (warns OR warning OR "red line")',
}
OUT = pathlib.Path(__file__).resolve().parents[1] / "data/raw"
def fetch(name, q):
    p = dict(query=q, mode="timelinevolraw", format="json",
             startdatetime="20190101000000", enddatetime="20261015000000")
    for attempt in range(4):
        r = requests.get(API, params=p, timeout=90)
        if r.status_code == 200 and r.text.strip().startswith("{"):
            (OUT / f"gdelt_signal_{name}.json").write_text(r.text); return True
        print(name, r.status_code, r.text[:120]); time.sleep(10 * (attempt + 1))
    return False
if __name__ == "__main__":
    for n, q in QUERIES.items():
        ok = fetch(n, q); print(n, ok); time.sleep(6)
