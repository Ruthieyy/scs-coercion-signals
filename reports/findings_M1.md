# M1 findings note — PRELIMINARY (2026-10-19)

**Bottom line:** the news *signal* of coercion is strong and easy to detect. A measurable *cost* in chokepoint traffic is not visible yet. That fits the "loud signal, small cost" hypothesis, but the current design is too weak to claim it.

Figure: `reports/figures/fig01_signals_vs_costs.png`. Full numbers: `reports/preliminary_results.md`.

## Signal side
- GDELT coverage of "Taiwan Strait drills/blockade" spikes at **all 6** curated PLA exercises. The median z-score is about 27 against the trailing 90 days.
- Coverage of Second Thomas, Scarborough and Sabina Shoal spikes (z>3) at **7 of 10** CCG incidents.
- Generic "China warns" rhetoric spikes at only 6 of 16 events. It is a noisy proxy for *threats* and needs a real classifier.

## Cost side (event study, 7-day-smoothed log transits, baseline days −28…−8, placebo = random non-event dates)
- **Taiwan Strait after PLA drills:** +3.9% over days 0–14 (p≈0.19). There is **no drop**, which matches the earlier probe.
- **Luzon after drills:** +8.7% (p≈0.16). Diversion away from the Strait is one possible reading, but the evidence is weak.
- **Balabac Strait after SCS incidents:** −7.0% (p≈0.06). However, **the dip starts about 5 days before the events**, and Balabac carries only about 11 ships a day. This looks more like noise, clustering or seasonality than a causal effect.
- **Mindoro:** about 0%. **Malacca** (distant control): +1.6%. Both are null.
- **Weekly lagged regression** of signal(t) on Δtransits(t+1): no predictive relationship (R² ≈ 0).

## Caveats
- N is small (6 drills and 10 incidents), and there are no weather or typhoon controls yet.
- Event dates are reconstructed from memory of public reporting and are flagged `verify_dates` in the CSV.
- One GDELT query (CCG water cannon / ramming) kept hitting the 429 rate limit and has not been fetched.
- PortWatch counts are AIS-derived, so coverage gaps are possible.
