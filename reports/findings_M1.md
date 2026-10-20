# Findings note — PRELIMINARY (updated 2026-10-19, M2)

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
