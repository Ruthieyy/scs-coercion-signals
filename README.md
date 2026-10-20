# Signals vs. Costs of Great-Power Coercion in the South China Sea

> **Status: early research prototype (Oct 2026). All results are preliminary.**

## Research question
When China applies coercion in the South China Sea and around Taiwan, **what is signalled, and what does it actually cost?**
Coercion here means gray-zone incidents (water cannon, ramming, blockades of resupply), large PLA exercises, and official warnings.
1. **Signals.** Can coercive *acts* and *threats* be detected and classified automatically from multilingual text (news events, official statements) in near real time?
2. **Costs.** Do those signals predict measurable economic costs? The costs studied are changes in commercial traffic through nearby chokepoints, measured with AIS-derived IMF PortWatch transits. Later the scope widens to freight/insurance, trade flows and markets.
3. **Gap.** Is there a systematic gap between how loud coercion *sounds* and what it *costs*? If so, which kinds of coercion are "cheap talk" and which carry real costs?

Shipping data is used here as **one measurable lens on costs, not as the topic itself**.

## Why it matters
Gray-zone coercion is designed to stay below the threshold of war, which makes its effects hard to measure. Policy debate often goes by headline intensity. This project asks whether the headlines track real-world costs. That links to the literature on costly signalling (Fearon 1997), geopolitical-risk indices (Caldara & Iacoviello 2022), and text-based conflict forecasting (Mueller & Rauh 2018). See `docs/literature_review.md`.

## Contribution (what ML adds)
- **Signal measurement.** Build a coercion-event classifier for English and Chinese news and MFA/CCG statements, with an *act vs. threat* split in the style of Caldara–Iacoviello GPR. It starts from keyword timelines and moves to a fine-tuned transformer or LLM-assisted labelling with a validated gold set (AI annotators checked against a 40-sentence human spot-check; codebook revised to v1.2).
- **Cost estimation.** Run event studies and local projections against placebo distributions, with weather/typhoon and seasonality controls. Later this moves to synthetic control or causal ML (double ML) for heterogeneous effects by incident type.
- **Forecasting test.** Use walk-forward validation to test whether signal features improve out-of-sample prediction of traffic disruptions beyond weather and seasonality.

## Data
| source | what | access | in repo |
|---|---|---|---|
| IMF PortWatch `Daily_Chokepoints_Data` | daily transits by ship type, 8 SE-Asian chokepoints, 2019–2026 | public ArcGIS REST | `src/fetch_portwatch.py` |
| GDELT DOC 2.0 API | daily article-volume timelines for coercion queries | public, 1 req/5 s | `src/fetch_gdelt_signals.py` |
| GDELT 1.0 events | daily CAMEO-coded events (probe file) | public | probe only |
| Curated event list | 60 verified PRC coercion events 2019–2026 (48 actions / 12 threats), with source URLs | hand-built, see `docs/event_verification.md` | `src/events_master.py` → `data/raw/coercion_events_curated.csv` |
| IBTrACS WP v04r01 | tropical-cyclone tracks → TC proximity per strait | public (NOAA NCEI) | `src/build_weather.py` |
| Open-Meteo marine (ERA5 ocean) | daily max wave height per strait | public, no key | `src/build_weather.py` |
| China MFA regular press conferences (EN + ZH) | ~1,000 transcripts per language, **2022-07 → 2026-10** (the listing does not reach earlier) | public fmprc.gov.cn / mfa.gov.cn | `src/crawl_mfa.py`, `src/segment_mfa.py` |
| Taiwan MND PLA activity reports | 2,015 reports, 2020-09 → 2026-10 (format break 2022-11; counts missing where only a PDF or image was published) | public mnd.gov.tw | `src/crawl_mnd.py` |
| Labelled sentences | 471 MFA sentences, action / threat / neither, AI labels under codebook v1.2 plus a **40-sentence human spot-check hand-labeled by the author** (initial human–AI κ = 0.46; see below) | `docs/codebook.md` | `data/labels/` |
| Not accessible | China Coast Guard (WAF block, HTTP 418) and Philippine Coast Guard (HTTP 403) sites; not circumvented | — | — |
| Planned | AMTI tracker, GPR daily, freight/FX/equities | public | — |

## Repo layout
```
src/                 fetch + build + analysis scripts
data/raw/            downloaded data (large files git-ignored; re-fetch via src/)
data/processed/      aligned daily panel
notebooks/           exploration
reports/             findings notes, figures/
docs/                probe notes, literature review, source URLs
```

## Reproduce
```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python src/fetch_portwatch.py
.venv/bin/python src/fetch_gdelt_signals.py      # slow: rate-limited
.venv/bin/python src/events_master.py            # writes curated event CSV
.venv/bin/python src/build_weather.py            # IBTrACS + ERA5 waves
.venv/bin/python src/build_dataset.py
.venv/bin/python src/event_study.py              # -> reports/preliminary_results.md, reports/figures/
# M3 text signals
.venv/bin/python src/crawl_mfa.py && .venv/bin/python src/segment_mfa.py   # MFA EN+ZH -> data/processed/mfa_sentences.csv
.venv/bin/python src/crawl_mnd.py                # (--cached to reparse) -> data/processed/mnd_pla_daily.csv
.venv/bin/python src/merge_ai2_labels.py         # second-annotator labels -> for_human_review.csv (ai2_label) + agent_labeled.csv
.venv/bin/python src/apply_codebook_v12.py       # human spot-check (40) + codebook v1.2 relabels -> agent_labeled.csv
.venv/bin/python src/train_classifier.py         # train = agent labels, test = ai2 labels -> reports/classifier_metrics.md
.venv/bin/python src/build_text_signals.py       # -> data/processed/text_signals_daily.csv
.venv/bin/python src/event_study_text.py         # -> reports/results_M3_text_signals.md, figures/fig02_text_signals.png
```

## Classifier at a glance
- Test set: 189 held-out MFA sentences (EN 112, ZH 77). Training: 282 other sentences. Model chosen by 5-fold CV on the training set only.
**Iterative codebook validation (v1.1 → human spot-check → v1.2).**
1. Two independent AI annotators (the Grok Bot assistant on all 471 sentences; a second AI model provided by the author on the 189 held-out ones) agreed closely: κ = 0.935.
2. The author then hand-labeled (no AI) a stratified random 40-sentence subset. Initial human vs. AI agreement was only 26/40, **κ = 0.46**, so the AI–AI agreement had overstated label quality.
3. The author adjudicated the 14 disagreements (7 to the AI label, 6 kept, 1 third label flagged borderline) and revised the codebook to **v1.2**: rule 5 (threat needs addressee + targeted behaviour + adverse outcome, even if fatalistic) and new rule 10 (action only when a measure is announced or reported; justifying one already taken is neither).
4. The assistant re-applied v1.2 to all 471 sentences: 22 relabeled (16 action → neither, 5 neither → threat, 1 threat → neither). Final human vs. v1.2 AI labels on the 40: 38/40, κ = 0.92. This is optimistic, because v1.2 was written from these 40 sentences.

- **Headline, TF-IDF + MiniLM ensemble vs. the author's hand labels (n = 40):** macro-F1 **0.88**, κ 0.79 (F1 action 0.92, threat 0.83, neither 0.88). The previous v1.1 model scored 0.64 against the author's initial labels on the same 40 and 0.82 against the adjudicated ones, so most of the gain is the label revision, not the model.
- **vs. AI labels under v1.2 on all 189 held-out sentences:** macro-F1 0.845, κ 0.73 (F1 action 0.85, threat 0.77, neither 0.92). MiniLM alone 0.784; keyword rules 0.684. Details: `reports/classifier_metrics.md`.

**Limitations.** Only 40 sentences are human-labeled, by one annotator, and v1.2 was derived from those same sentences, so the headline is a small-sample, optimistic sanity check (one sentence moves macro-F1 by about 0.02–0.05). The training labels are AI labels. A fresh human-labeled sample is the next validation step.

## Roadmap
- [x] M0: feasibility probe + literature review
- [x] M1: aligned daily panel (PortWatch × GDELT × curated events), first event study + figure
- [x] M2: 60 verified events with sources; weather/typhoon controls; event study v2
- [x] M3: MFA EN/ZH and MND corpora; codebook; action/threat classifier (codebook v1.2 after a 40-sentence human spot-check; macro-F1 0.88 on the 40, 0.845 on 189 held-out AI labels); daily threat signal in the event study. **Still open:** a fresh human-labeled validation sample, CCG/PCG statements, MFA before 2022-07
- [ ] M4: cost estimation — local projections/synthetic control; extend costs beyond transits (freight rates, TWD/PHP FX, Taiwan equities)
- [ ] M5: walk-forward forecasting test; write-up (blog post + short paper)
