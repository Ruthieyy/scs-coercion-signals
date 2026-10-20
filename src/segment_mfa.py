"""Turn MFA transcripts into answer-sentence units on the Taiwan/SCS topic set.
Output data/processed/mfa_sentences.csv: sent_id, date, lang, speaker, question, sentence, url."""
import re, html, csv, pathlib, pandas as pd
ROOT = pathlib.Path(__file__).resolve().parents[1]
TOPIC = {"en": re.compile(r"Taiwan|South China Sea|Philippin|Manila|Scarborough|Huangyan|Second Thomas|Ren'?ai|Xianbin|Sabina|Spratly|Nansha|Xisha|Paracel|Vietnam|coast guard|Strait|Kinmen|Lai Ching-te|DPP|arms sale|reunification|separatis", re.I),
         "zh": re.compile(r"台湾|台海|台独|赖清德|民进党|南海|菲律宾|菲方|黄岩岛|仁爱礁|仙宾礁|南沙|西沙|越南|海警|金门|对台军售|统一|分裂")}
QPAT = {"en": re.compile(r"^(Q:|Q：|[A-Z][\w .’'&\-]{1,60}(?:\:|：)\s?.*\?$)"), "zh": re.compile(r"^[^：:]{1,40}记者[：:]|^问[：:]")}
APAT = {"en": re.compile(r"^(Spokesperson|Mao Ning|Lin Jian|Guo Jiakun|Wang Wenbin|Zhao Lijian|Hua Chunying|Wang Yi)\s*[:：]"),
        "zh": re.compile(r"^(毛宁|林剑|郭嘉昆|汪文斌|赵立坚|华春莹|发言人)[：:]")}
# Non-speech website boilerplate scraped from mfa.gov.cn pages (exit-site popup, copyright/ICP footer). Filtered AFTER
# sent_id assignment so existing ids (and the labels keyed on them) stay stable.
JUNK = re.compile(r"即将离开外交部门户网站|版权所有|京ICP备|京公网安备|网站标识码")
def is_junk(s): return bool(JUNK.search(str(s)))
def paras(t):
    t = re.sub(r"<(script|style).*?</\1>", "", t, flags=re.S)
    return [p for p in (html.unescape(re.sub(r"<[^>]+>", "", x)).replace("\xa0", " ").strip() for x in re.findall(r"<p[^>]*>(.*?)</p>", t, re.S)) if p]
def sents(p, lang):
    s = re.split(r"(?<=[。！？])" if lang == "zh" else r"(?<=[.!?])\s+(?=[A-Z“\"])", p)
    return [x.strip() for x in s if len(x.strip()) >= (8 if lang == "zh" else 25)]
def title_date(title, lang, fallback):
    t = re.sub(r"[\u2002\u200b\u3000\xa0]", " ", title)
    m = re.search(r"(\w+ \d{1,2}, \d{4})", t) if lang == "en" else re.search(r"(\d{4})年(\d{1,2})月(\d{1,2})日", t)
    try:
        return pd.to_datetime(m.group(1)) if lang == "en" else pd.Timestamp(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except Exception:
        return pd.to_datetime(fallback)  # URL date; wrong for items bulk-migrated on 2024-05-30
def main():
    rows = []
    for lang in ["en", "zh"]:
        idx = pd.read_csv(ROOT / f"data/raw/mfa_{lang}/index.csv", dtype=str)
        for _, r in idx[idx.ok == "True"].iterrows():
            f = ROOT / f"data/raw/mfa_{lang}" / r.file
            if not f.exists(): continue
            q, speaker, mode = "", "", None
            for p in paras(f.read_text(errors="ignore")):
                if QPAT[lang].search(p) and not APAT[lang].search(p): q, mode = p, "q"; continue
                m = APAT[lang].search(p)
                if m: speaker, mode = m.group(1), "a"; p = p[m.end():].strip()
                if mode != "a": continue
                if not TOPIC[lang].search(q + " " + p): continue
                for s in sents(p, lang):
                    rows.append(dict(date=title_date(r.title, lang, r.date).date(), lang=lang, speaker=speaker, question=q[:400], sentence=s, url=r.url))
    df = pd.DataFrame(rows).drop_duplicates(["date", "lang", "sentence"]).reset_index(drop=True)
    df.insert(0, "sent_id", [f"{l}{i:06d}" for i, l in zip(df.index, df.lang)])
    df = df[~df.sentence.map(is_junk)]
    df.to_csv(ROOT / "data/processed/mfa_sentences.csv", index=False)
    print(df.groupby("lang").agg(n=("sentence", "size"), start=("date", "min"), end=("date", "max"), days=("date", "nunique")))
if __name__ == "__main__":
    main()
