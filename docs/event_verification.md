# Event verification log (2026-10-19)

How events were checked:
- Every event in `data/raw/coercion_events_curated.csv` has at least one source URL from a credible outlet or an official body. These include Reuters, AP, the Guardian, NYT, USNI News, ABC Australia, Al Jazeera, Philippine Star, GMA, SCMP, RFA, Newsweek citing Taiwan's Ministry of National Defense (MND), and the US State Department.
- The `verify` column records how the date was checked:
  - `search`: the date was confirmed in the article text or snippet returned by web search on 2026-10-19 (25 events).
  - `wiki_cite`: the date and title were confirmed from the outlet citation listed on the relevant Wikipedia article (35 events). This was cross-checked against the Wikipedia event description. The article itself was not opened because Reuters, AP and USNI block automated fetches (HTTP 401/403).
- Two dates per event:
  - `event_date`: when the incident happened.
  - `public_date`: the first public report. Event studies use `public_date`, which matters for delayed disclosures such as the Feb 2023 laser incident (reported 7 days later) and the Whitsun Reef and Vanguard Bank episodes.

## Original 16 events (v1 list), all verified and none dropped
| v1 id | verified date | correction | source |
|---|---|---|---|
| E01 | 2022-08-04..08-10 (announced 08-02) | none | Reuters |
| E02 | 2023-04-08..04-10 | none | Reuters |
| E03 | 2023-08-05 | none | USNI / Guardian |
| E04 | 2023-10-22 | none | AP |
| E05 | 2023-12-09 (Scarborough) + 2023-12-10 (Second Thomas) | split into two events | US State Dept; Reuters |
| E06 | 2024-03-05 | none | Reuters |
| E07 | 2024-03-23 | none | Reuters |
| E08 | 2024-04-30 | none | AP |
| E09 | 2024-05-23..05-24 | none | Al Jazeera |
| E10 | 2024-06-17 | none (blades, knives and axes; one sailor lost a thumb) | Reuters |
| E11 | 2024-08-19, 08-25, 08-31 | split into three events | USNI ×2, AP |
| E12 | 2024-10-14 | none (record 153 aircraft) | Reuters |
| E13 | 2024-12-04 | none | Reuters |
| E14 | 2025-04-01..04-02 | the name "Strait Thunder-2025A" applies to the Apr 2 phase only | Reuters |
| E15 | 2025-08-11 | none | ABC Australia |
| E16 | 2025-12-29..12-30 | the exercise is named "Justice Mission 2025" | Reuters |

## Known limitations
- Coverage is biased toward events that got heavy English-language reporting. The list leans Philippine, because the Philippine Coast Guard has publicised incidents aggressively since 2023.
- AMTI, Taiwan MND daily PLA-activity reports and PRC MFA transcripts were not yet systematically scraped. Planned for M3.
- Threats are under-sampled (12). They need a text classifier rather than hand curation.
