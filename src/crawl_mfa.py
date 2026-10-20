"""Crawl PRC MFA regular press conference transcripts (EN: fmprc.gov.cn/eng/xw/fyrbt/lxjzh/, ZH: mfa.gov.cn jzhsl).
Polite: 3 workers, retries. Saves raw HTML to data/raw/mfa_{en,zh}/ (git-ignored) and an index CSV."""
import re, sys, time, pathlib, csv, requests, concurrent.futures as cf
ROOT = pathlib.Path(__file__).resolve().parents[1]
H = {"User-Agent": "Mozilla/5.0 (research; UIUC student project)"}
CFG = {"en": ("https://www.fmprc.gov.cn/eng/xw/fyrbt/lxjzh/", "index_{}.html", ".html"),
       "zh": ("https://www.mfa.gov.cn/web/fyrbt_673021/jzhsl_673025/", "index_{}.shtml", ".shtml")}
def get(u, tries=4):
    for i in range(tries):
        try:
            r = requests.get(u, headers=H, timeout=40)
            if r.status_code == 200: r.encoding = "utf-8"; return r.text
        except Exception: pass
        time.sleep(3 * (i + 1))
    return None
def listing(lang):
    base, pat, ext = CFG[lang]; first = get(base)
    n = int(re.search(r"countPage\s*=\s*(\d+)", first).group(1)); items = []
    for p in range(n):
        t = first if p == 0 else get(base + pat.format(p))
        if not t: continue
        for h, title in re.findall(r'href="\./(\d{6}/t\d{8}_\d+' + re.escape(ext) + r')"[^>]*>([^<]+)<', t):
            items.append((h, title.strip()))
        time.sleep(0.3)
    return base, list(dict.fromkeys(items))
def main(lang):
    base, items = listing(lang); out = ROOT / f"data/raw/mfa_{lang}"
    items = [(h, t) for h, t in items if h[8:12] >= "2019"]
    print(lang, "items since 2019:", len(items), flush=True)
    def dl(it):
        h, t = it; f = out / h.replace("/", "_")
        if f.exists(): return True
        html = get(base + h); time.sleep(0.4)
        if html: f.write_text(html); return True
        return False
    with cf.ThreadPoolExecutor(3) as ex: ok = list(ex.map(dl, items))
    with open(out / "index.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["file", "date", "title", "url", "ok"])
        for (h, t), o in zip(items, ok): w.writerow([h.replace("/", "_"), h[8:16], t, base + h, o])
    print(lang, "downloaded", sum(ok), "/", len(items), flush=True)
if __name__ == "__main__":
    main(sys.argv[1])
