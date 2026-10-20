# Feasibility probe (2026-10-17)
- PortWatch Daily_Chokepoints_Data: public ArcGIS REST, no key. 28 chokepoints. SCS-relevant: Malacca(5), Taiwan(11), Luzon(14), Sunda(19), Lombok(15), Makassar(20), Balabac(25), Mindoro(27).
  fetch_portwatch.py -> data/portwatch_scs_chokepoints.csv (22,728 rows, 2019-01-01..2026-10-11, daily, by ship type).
- Weekly drop >15% vs trailing 8-wk median: Taiwan 3.2% of weeks, Luzon 13.1%, Malacca ~0%. Largest Taiwan drop wk of 2025-10-26 (-36%) coincides with 5-6.5 m waves (Open-Meteo) -> weather dominates. PLA drills (Aug 2022, Apr 2023, May/Oct 2024, Apr 2025, Dec 2025) show no clear transit-count drop.
- GDELT DOC API: works (one call = daily volume 2019-2026 for "Taiwan Strait"); rate limit 1 req / 5 s (got 429 once).
- GDELT 1.0 daily events file over HTTPS works (http timed out). 20251229: 88k events, 2,702 in 0-26N/105-125E bbox (needs sea polygon filter; includes land).
- Open-Meteo marine API: works, no key. IBTrACS WP CSV: works.
