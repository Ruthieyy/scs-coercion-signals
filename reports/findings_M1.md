# Findings note — PRELIMINARY (updated 2026-10-19, M3)

**Bottom line (unchanged, now on firmer footing):** the news *signal* of coercion is clear for major military exercises and weaker for coast-guard incidents. After weather adjustment and with 60 verified events, there is **still no credible evidence of a traffic *cost*** at nearby chokepoints. The one "significant" result (Luzon) is a pre-trend, not an effect. The M1 Balabac −7% result **did not survive** the larger sample.

Figure: `reports/figures/fig01_signals_vs_costs.png`. Numbers: `reports/preliminary_results.md`. Event sourcing: `docs/event_verification.md`.

## What changed since M1
- **Events:** went from 16 (4 with unverified dates) to **60 verified events** for 2019–2026: 48 actions and 12 threats, each with a source URL. All 16 originals were confirmed. Two were split into separate events (Dec 2023, and the three Aug 2024 Sabina incidents).
- **Event timing:** day 0 is now the *public report date*, not the incident date.
- **Weather controls:** added IBTrACS tropical cyclones (within 300 km, lags 0–3; max wind within 500 km) and ERA5 maximum wave height (lags 0–2) at each strait. Fixed effects for day of week, month and year are included too.
- **Weather model fit:** R² rises from 0.11 to 0.26 (Taiwan Strait) and from 0.15 to 0.38 (Luzon), so weather is a first-order driver of daily traffic, as the probe suggested.

## Signal side
- **PLA exercises around Taiwan:** GDELT "drills/blockade" coverage spikes at 10 of 14 events. The median z is 12.
- **Philippines/SCS coast-guard incidents:** shoal-name coverage spikes at 13 of 23 (median z 3.3). Smaller incidents are weak in English news volume.
- **"China warns" rhetoric:** spikes at only 2 of 10 *threat* events. Generic keyword volume does **not** capture threats, which is the main motivation for a dedicated act/threat classifier (M3).

## Cost side (abnormal log transits, weather-adjusted, days 0–14 after the public report)
| chokepoint | events | effect | placebo p | pre-trend (days −7…−1) |
|---|---|---|---|---|
| Taiwan Strait | Taiwan actions (14) | +2.1% | 0.15 | +2.3% |
| Luzon | Taiwan actions (14) | +9.5% | **0.02** | **+9.1%** |
| Taiwan Strait | all threats (10) | −1.3% | 0.45 | +2.2% |
| Balabac | Philippines/SCS actions (23) | +0.7% | 0.79 | −7.3% |
| Mindoro | Philippines/SCS actions (23) | +3.6% | 0.13 | −0.5% |
| Malacca (distant control) | all SCS actions (30) | +1.2% | 0.21 | +1.2% |

How to read these:
- **Luzon** is the only p<0.05 result, but traffic is already +9% in the week *before* the public report. The rise begins about 10 days earlier. That pattern does not fit a causal response to the drills. Likely explanations are residual seasonality, or that drills follow predictable political triggers (inaugurations, US visits) that fall in particular seasons. This is not evidence of rerouting.
- **No negative traffic effect** appears anywhere. Commercial shipping does not visibly pay for gray-zone coercion at the daily chokepoint level.
- **Weekly predictive regressions** of news signal on next week's abnormal transits show R² ≈ 0 everywhere.

## Interpretation (hypothesis, not a conclusion)
The results are consistent with coercion being **calibrated to be loud but cheap**. It is high-visibility signalling that stays below the threshold that would disrupt commercial traffic, which is the point of gray-zone tactics. To test this properly, costs have to be measured where they are more likely to show up:
- war-risk insurance and freight rates,
- TWD and PHP exchange rates and Taiwan equities,
- fishing activity (Global Fishing Watch),
- Philippine resupply success.

## Caveats
- N is still modest. Many events cluster in 2023–2025 and at Second Thomas Shoal.
- Chokepoint counts are coarse. A drill zone can be avoided within a strait without changing the transit count.
- AIS coverage gaps are possible.
- The CCG water-cannon GDELT query is still missing because the API kept rate-limiting it.
- The list over-represents English-language and Philippine-publicised events.

---
## M3: text-derived signals (details: `reports/results_M3_text_signals.md`, `reports/classifier_metrics.md`, `reports/figures/fig02_text_signals.png`)

**Data.**
- MFA press conferences: EN 1,000 and ZH 998 transcripts. Coverage starts 2022-07, because the public listing does not reach earlier. Segmentation gives 9,482 EN and 7,341 ZH spokesperson-answer sentences on the Taiwan/SCS topic set (after dropping 288 rows of mfa.gov.cn website boilerplate: the exit-site popup and the copyright footer).
- Taiwan MND PLA reports: 2,015 reports, 2020-09 → 2026-10, of which 1,368 days have aircraft counts.
- China Coast Guard and Philippine Coast Guard sites block automated access. They were not collected.

**Classifier.**
- Iterative codebook validation:
  1. Two independent AI annotators (the Grok Bot assistant on all 471 sentences; a second AI model provided by the author on the 189 held-out ones) agreed closely: κ = 0.935.
  2. The author then hand-labeled (no AI) a stratified random 40-sentence subset. Initial human vs. AI agreement was only 26/40, **κ = 0.46**, so the AI–AI agreement had overstated label quality.
  3. The author adjudicated the 14 disagreements (7 to the AI label, 6 kept, 1 third label flagged borderline) and revised the codebook to **v1.2**: rule 5 (threat needs addressee + targeted behaviour + adverse outcome, even if fatalistic) and new rule 10 (action only when a measure is announced or reported; justifying one already taken is neither).
  4. The assistant re-applied v1.2 to all 471 sentences: 22 relabeled (16 action → neither, 5 neither → threat, 1 threat → neither). Final human vs. v1.2 AI labels on the 40: 38/40, κ = 0.92. This is optimistic, because v1.2 was written from these 40 sentences.
- Against the author's hand labels on the 40 (model chosen by CV on the training set only), the TF-IDF + MiniLM ensemble reaches macro-F1 0.88 (κ 0.79): action F1 0.92, threat 0.83, neither 0.88. Small n and optimistic (see caveats).
- Against v1.2 AI labels on all 189 held-out sentences: macro-F1 0.845 (κ 0.73); MiniLM alone 0.784; keyword rules 0.684; a model trained only on rule (silver) labels 0.779.
- Cross-lingual transfer works: trained on EN only and tested on ZH, macro-F1 is 0.79.

**Signal validation (does the series move when it should?).**
- MND aircraft counts are a strong signal for Taiwan military actions: the median z-score is 5.3 and 89% of events exceed z>2. They do not move for SCS events or for verbal threats.
- MFA action-share rises around SCS actions (46% exceed z>2) but, under codebook v1.2, **no longer around Taiwan actions** (9%, median z 0.1; it was 45% under v1.1). Around Taiwan drills the spokesperson mostly *justifies* drills that the PLA Eastern Theater Command announced ("a firm punishment of…"), which v1.2 codes as neither. For SCS incidents the MFA itself reports the CCG measures. MND counts remain the action signal for Taiwan.
- MFA threat-share responds only weakly to the curated threat events. Median z is 0.6, and z>2 occurs for 0 of 9 (also 0 of 9 for novel threats). Threat language peaks around Taiwan actions instead. The largest 10-presser peak is 2024-12-11, the period of Lai Ching-te's Hawaii/Guam transit and the large PLA maritime deployment in early December 2024. In this channel, threats accompany actions; they do not precede them as separate "warning" signals.
- Caveat: there are only 9 curated threat events inside the MFA coverage window.

**Cost side.**
- Using signal-spike days (z>3, merged within 10 days) as events: MFA threat 22 spikes, novel threat 25, action 32, MND aircraft 29.
- Abnormal weather-adjusted transits over days 0–14 lie between −3.0% and +2.2% at every chokepoint, with every placebo p ≥ 0.14.
- Weekly lagged regressions of abnormal transits on the signal z-scores are also null: |β| ≤ 0.9% per SD and every p ≥ 0.25. MND aircraft vs. Taiwan Strait gave p = 0.35.
- This is consistent with M2: neither actions nor threats measurably reduce transits. The new text signals do not change that.

**Interpretation (hypothesis).**
- The text signals measure the signal side much better than GDELT volume. MND tracks actions and the MFA classifier separates action talk from threat talk.
- On the cost side, the null result is now robust across three signal definitions.
- Two readings remain:
  - transits are the wrong cost measure (try freight rates, insurance, FX or equities in M4);
  - coercion in this period was calibrated to stay below the level that disrupts commerce.

**New caveats.**
- Human validation covers only 40 sentences by one annotator (the author), and codebook v1.2 was revised from those same 40, so the human-label metrics are optimistic. Training labels are AI labels under v1.2. A fresh human sample is needed.
- Enriched test set (rule-flagged sentences oversampled). The model is now selected by CV on the training set, not on the test set.
- The threat series is dominated by boilerplate formulas ("red line", "play with fire"). A version excluding them is reported as well.
- No MFA data before 2022-07.
- The MND format changes at 2022-11 (before that, SW-ADIZ incursions only). Counts are missing for 2024-01 to 2025-02, when they were published only as PDF or image attachments or the reports are missing.
- No transformer fine-tuning.
