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
- **Signal measurement.** Build a coercion-event classifier for English and Chinese news and MFA/CCG statements, with an *act vs. threat* split in the style of Caldara–Iacoviello GPR. It starts from keyword timelines and moves to a fine-tuned transformer or LLM-assisted labelling with a human-validated gold set.
- **Cost estimation.** Run event studies and local projections against placebo distributions, with weather/typhoon and seasonality controls. Later this moves to synthetic control or causal ML (double ML) for heterogeneous effects by incident type.
- **Forecasting test.** Use walk-forward validation to test whether signal features improve out-of-sample prediction of traffic disruptions beyond weather and seasonality.

## Data
| source | what | access | in repo |
|---|---|---|---|
| IMF PortWatch `Daily_Chokepoints_Data` | daily transits by ship type, 8 SE-Asian chokepoints, 2019–2026 | public ArcGIS REST | `src/fetch_portwatch.py` |
| GDELT DOC 2.0 API | daily article-volume timelines for coercion queries | public, 1 req/5 s | `src/fetch_gdelt_signals.py` |
| GDELT 1.0 events | daily CAMEO-coded events (probe file) | public | probe only |
| Curated incident list | 16 major PLA/CCG coercive episodes, 2022–2025 | hand-built, **dates need source verification** | `data/raw/coercion_events_curated.csv` |
| Planned | Open-Meteo marine, IBTrACS typhoons, AMTI tracker, MFA press conferences, GPR daily | public | — |

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
.venv/bin/python src/build_dataset.py
.venv/bin/python src/event_study.py              # -> reports/preliminary_results.md, reports/figures/
```

## Roadmap
- [x] M0: feasibility probe + literature review
- [x] M1: aligned daily panel (PortWatch × GDELT × curated events), first event study + figure
- [ ] M2: verify event dates against primary sources; expand to ~50+ incidents (AMTI, PCG statements); add weather/typhoon controls
- [ ] M3: text classifier for coercion acts vs. threats (EN + ZH, incl. MFA/CCG statements); gold-labelled validation set
- [ ] M4: cost estimation — local projections/synthetic control; extend costs beyond transits (freight rates, TWD/PHP FX, Taiwan equities)
- [ ] M5: walk-forward forecasting test; write-up (blog post + short paper)
