# Literature Review: Geopolitical Signals vs. Weather in Forecasting South China Sea Chokepoint Disruptions

**Project question:** Beyond weather and seasonality, do geopolitical signals add predictive power for weekly disruptions in transit counts? The signals are GDELT news and events, gray-zone vessel activity and Chinese official statements. Transit counts come from IMF PortWatch AIS data for the South China Sea, the Taiwan Strait and the Luzon chokepoints.
**Planned model:** XGBoost classifier, walk-forward validation, SHAP.
**Early probe result:** the large transit drops are mostly weather (typhoons and big waves). PLA drills show no clear drop.

Compiled Oct 17, 2026 (CT).

**How each paper was checked:** I confirmed every entry against a publisher page, DOI landing page, RePEc/IDEAS record, PubMed record or official institutional page, using web search or fetch on that date. The "Data" and "Model design" sections stay at the level of detail those abstracts and landing pages support. Where I go beyond the abstract, I say so with "(per paper)" or a caveat. Read the PDFs before you quote specific numbers in your write-up.

---

## A. Measuring geopolitical risk from text, and forecasting conflict with news or event data

### 1. Caldara, D. & Iacoviello, M. (2022). "Measuring Geopolitical Risk." *American Economic Review* 112(4): 1194–1225.
- DOI: https://doi.org/10.1257/aer.20191823 · Data: https://www.matteoiacoviello.com/gpr.htm
- **Venue:** AER, a top-5 economics journal. The authors are Federal Reserve Board economists.
- **Research question:** Can news text measure adverse geopolitical events and risks, and do those risks affect the real economy?
- **Data:** The share of articles in major English-language newspapers that discuss adverse geopolitical events and threats (wars, terrorism, military buildups, nuclear threats and similar). The index runs monthly back to 1900 for the historical series and from 1985 for the recent series. A daily version is published on the website, along with country-specific and firm/industry-level indicators.
- **Model design:** A dictionary-based text index, validated against human audits of articles. Two sub-indices separate **Threats** from **Acts**. Economic effects are estimated with VARs and local projections.
- **Key findings:** GPR spikes around the World Wars, Korea, the Cuban Missile Crisis and 9/11. Higher GPR foreshadows lower investment and employment and fatter downside tails. Both threats and realized acts matter.
- **What Yutong should borrow:**
  - Use the daily GPR, aggregated to weeks, as a ready-made, defensible global geopolitical feature.
  - Use the **Threats vs. Acts split**. It is the theoretical template for separating "rhetoric/official statements" (threats) from "drills/incidents" (acts) in her own features.
  - The country-specific series may include China, Taiwan, the Philippines and others. Check the download file.
  - **Challenge:** GPR is global and English-language. Expect it to capture risk sentiment rather than physical blockages. That makes it a good *baseline geopolitical feature* to beat with her local, Chinese-language signals.

### 2. Mueller, H. & Rauh, C. (2018). "Reading Between the Lines: Prediction of Political Violence Using Newspaper Text." *American Political Science Review* 112(2): 358–375.
- DOI: https://doi.org/10.1017/S0003055417000570 · Open accepted version: https://www.repository.cam.ac.uk/items/56a996a3-ec65-4b2c-97eb-ab495b237f43
- **Research question:** Can newspaper text predict when armed conflict and civil war will break out?
- **Data:** A large corpus of newspaper articles by country and year, reduced with LDA topic models.
- **Model design:** Topic shares go into panel regressions with **country fixed effects**. The fixed effects force the model to use *within-country variation over time* rather than "this country is always violent." Evaluation is out-of-sample (ROC-based).
- **Key findings:** Within-country changes in topics predict when conflict happens. They are most useful exactly where risk rises in places that were previously peaceful. Text works because topics are broad (they include stabilizing factors) and deep (their vocabulary adapts to context).
- **What Yutong should borrow:**
  - Build the news features as **deviations from each chokepoint's own baseline**, such as z-scores against the trailing 52 weeks, not as raw counts.
  - Consider LDA or embeddings on Chinese MFA/CCG text instead of keyword counts only.

### 3. Mueller, H. & Rauh, C. (2022). "The Hard Problem of Prediction for Conflict Prevention." *Journal of the European Economic Association* 20(6): 2440–2467.
- DOI: https://doi.org/10.1093/jeea/jvac025 · RePEc: https://ideas.repec.org/a/oup/jeurec/v20y2022i6p2440-2467..html
- **Research question:** How do we forecast rare outbreaks in peaceful places (the "hard problem"), and is a forecast useful for decisions?
- **Data:** Topic models over more than 4 million newspaper articles.
- **Model design:** Topic shares go into a **random forest** that predicts conflict risk. The risk scores then feed a cost-minimizing decision framework that sets the threshold for intervention.
- **Key findings:** Outbreaks in previously peaceful countries are rare and hard to predict. Even so, text-based forecasts plus a cost-based threshold imply large expected savings: over US$1 trillion even with fairly ineffective interventions.
- **What Yutong should borrow:**
  - Make the "hard problem" split explicit. Evaluate separately on (a) all disruption weeks and (b) **non-weather** disruption weeks, or onsets after calm periods. That is where geopolitical signals would have to prove themselves.
  - Choose the classification threshold by a **cost ratio** (missed disruption vs. false alarm) rather than 0.5. A risk-analytics employer will find this compelling.

### 4. Hegre, H. et al. (2019). "ViEWS: A political violence early-warning system." *Journal of Peace Research* 56(2): 155–174.
- DOI: https://doi.org/10.1177/0022343319823860 (open access)
- **Research question:** Can a transparent, public system produce monthly forecasts of political violence 1–36 months ahead?
- **Data:** UCDP conflict events plus thematic covariates (conflict history, economy, institutions, geography), at country-month and sub-national grid-cell-month level, for Africa.
- **Model design:** An **ensemble** of thematic constituent models and ML models. Out-of-sample evaluation uses separate calibration and test periods. Forecasts are compared against baselines.
- **Key findings:** The system captures persistent conflict well and some diffusion, for example into Cameroon. New conflicts are harder.
- **What Yutong should borrow:**
  - Use ViEWS' **train / calibration / test time partitions** as the template for walk-forward validation.
  - Always report results **against simple baselines** such as persistence and conflict history.
  - Run a separate "thematic" model per signal family (weather, news, gray-zone, statements), then compare and ensemble them. That design answers her research question directly.

### 5. Vesco, P., Hegre, H., Colaresi, M., Jansen, R.B., Lo, A., Reisch, G. & Weidmann, N.B. (2022). "United they stand: Findings from an escalation prediction competition." *International Interactions* 48(4): 860–896.
- DOI: https://doi.org/10.1080/03050629.2022.2029856 · Open PDF: https://viewsforecasting.org/wp-content/uploads/United-they-stand-Findings-from-an-escalation-prediction-competition.pdf
- **Research question:** Which approaches best predict *changes* (escalation or de-escalation) in state-based violence?
- **Data/design:** A forecasting competition on ViEWS data with a common target and true out-of-sample evaluation across many teams' models.
- **Key finding:** A simple **ensemble of diverse models beat the average individual model**.
- **What Yutong should borrow:** Predicting *change* is harder than predicting *levels*. Frame the target as a drop relative to the chokepoint's own recent baseline, which she already plans. Benchmark XGBoost against a logistic regression and a seasonal-naïve model, and report a simple average of the three.

### 6. Bazzi, S., Blair, R.A., Blattman, C., Dube, O., Gudgeon, M. & Peck, R. (2022). "The Promise and Pitfalls of Conflict Prediction: Evidence from Colombia and Indonesia." *Review of Economics and Statistics* 104(4): 764–779.
- DOI: https://doi.org/10.1162/rest_a_01016 · RePEc: https://ideas.repec.org/a/tpr/restat/v104y2022i4p764-779.html
- **Research question:** How feasible is early-warning prediction of violence with unusually rich local data?
- **Data:** Two decades of local violent events plus hundreds of annual risk factors.
- **Model design:** A range of ML methods predicting one year ahead.
- **Key findings:** The models reliably find persistent hot spots, and detailed violence histories perform best. But they **poorly predict new outbreaks or escalations**, even in a best-case setting.
- **How this challenges her design:** It is a sobering prior. Geopolitical features may add little beyond weather and history, which matches her early probe. A well-documented **null or small-gain result is publishable-quality and honest**. Frame the project so that either answer counts as a finding.

### 7. Hammond, J. & Weidmann, N.B. (2014). "Using machine-coded event data for the micro-level study of political violence." *Research & Politics*.
- DOI: https://doi.org/10.1177/2053168014539924 (open access)
- **Research question:** How reliable is GDELT compared with hand-coded conflict data?
- **Data:** GDELT compared with ACLED and UCDP-GED.
- **Design:** Correlations at the grid-cell-month level and the aggregate level.
- **Key findings:** GDELT tracks *temporal* trends reasonably well, but its geography is unreliable. It over-places events near capitals and correlates weakly with ACLED and GED at the cell level. The authors recommend using it as a complement to hand-coded data, not a substitute.
- **What Yutong should borrow:**
  - Use GDELT as a **time series of attention or tone** (weekly counts, Goldstein scores, tone around SCS/Taiwan actor-pairs and keywords), not as a precise map of incidents.
  - Normalize by total GDELT volume, because coverage drifts over time.
  - Use ACLED only for mapping or validation.

### 8. Drobetz, W., Gavriilidis, K., Krokida, S.-I. & Tsouknidis, D. (2021). "The effects of geopolitical risk and economic policy uncertainty on dry bulk shipping freight rates." *Applied Economics* 53(19): 2218–2229.
- DOI: https://doi.org/10.1080/00036846.2020.1857329 · Open version: https://dspace.stir.ac.uk/bitstream/1893/32035/1/DGKT%20R1%2009-10-2020.pdf
- **Research question:** How do GPR and EPU shocks move dry-bulk freight rates?
- **Data:** The Caldara–Iacoviello GPR index, EPU indices for the US, China and Brazil, and Capesize and Panamax freight rates.
- **Model design:** A Bayesian VAR with impulse responses.
- **Key findings:** GPR shocks **raise** freight rates immediately, and the effect fades gradually. EPU shocks lower rates gradually.
- **What Yutong should borrow:** Geopolitical risk shows up in **prices** (freight and insurance) sooner than in **transit counts**. That may explain why the PLA drills showed no count drop. Ships keep sailing, just at a higher cost or on a slightly different route. Possible extension: add a price-side target or validation, such as a freight index, to show that geopolitics "bites" there even when counts don't move.

---

## B. Shipping and chokepoint disruption measured with AIS

### 9. Cerdeiro, D.A., Komaromi, A., Liu, Y. & Saeed, M. (2020). "World Seaborne Trade in Real Time: A Proof of Concept for Building AIS-based Nowcasts from Scratch." IMF Working Paper WP/20/57.
- DOI: https://doi.org/10.5089/9781513544106.001 · PDF: https://www.imf.org/-/media/files/publications/wp/2020/english/wpiea2020057-print-pdf.pdf
- **Research question:** Can raw AIS messages be turned into policy-relevant trade indicators?
- **Data:** Raw global AIS.
- **Model design:** An end-to-end pipeline. ML identifies port boundaries, voyages are built port to port, and trade volumes are estimated from draft and payload changes. Results are validated against official trade statistics.
- **Key findings:** A good fit with official statistics for many countries and the world aggregate. Event studies (Hurricane Maria, COVID-19 containment) show the data's value for detecting shocks.
- **What Yutong should borrow:**
  - This is the intellectual origin of PortWatch.
  - The Hurricane Maria event study supports her "weather dominates" finding and shows how to run a clean **event-study figure** (counts relative to the pre-event baseline). That figure is a good visual for the write-up.

### 10. Arslanalp, S., Koepke, R. & Verschuur, J. (2021). "Tracking Trade from Space: An Application to Pacific Island Countries." IMF Working Paper WP/21/225.
- DOI: https://doi.org/10.5089/9781513593531.001.a001 · Page: https://www.imf.org/en/publications/wp/issues/2021/08/20/tracking-trade-from-space-an-application-to-pacific-island-countries-464345
- **Research question:** Can AIS produce reliable *daily* port and trade indicators where official data are thin?
- **Data:** UN Global Platform AIS for 30 ports in 11 Pacific island countries.
- **Model design:** Improved cargo-payload estimation, validation of port calls, and port-boundary definition.
- **Key findings:** Daily indicators fill gaps in official data and detect shocks such as COVID-19.
- **What Yutong should borrow:** This is the **methodology paper behind the PortWatch data she downloaded**. Cite it as the data source, and read its section on measurement error before defining "disruption." Small chokepoints have noisy daily counts, which supports her choice of **weekly aggregation**.

### 11. Arslanalp, S., Choi, S.M., Kamali, P., Koepke, R., McKetty, M., Ruta, M., Saraiva, M., Sozzi, A. & Verschuur, J. (2025). "Nowcasting Global Trade from Space." IMF Working Paper WP/25/93.
- DOI: https://doi.org/10.5089/9798229009294.001 · RePEc: https://ideas.repec.org/p/imf/imfwpa/2025-093.html
- **Research question:** Can PortWatch data nowcast monthly maritime trade values and volumes?
- **Data:** IMF PortWatch port calls and **transit volumes for major chokepoints/passages (including Suez)**, together with customs data.
- **Model design:** Estimates customs values, price deflators and volumes from satellite AIS (per search summary; I could not open the full PDF because the fetch timed out).
- **Key findings:** PortWatch-based nowcasts track official trade.
- **What Yutong should borrow:** This is the **most current official documentation** of how PortWatch chokepoint transit numbers are built. Use it to justify the target variable and to note known limitations, such as AIS coverage gaps and vessel-type classification.

### 12. Verschuur, J., Koks, E.E. & Hall, J.W. (2020). "Port disruptions due to natural disasters: Insights into port and logistics resilience." *Transportation Research Part D* 85: 102393.
- DOI: https://doi.org/10.1016/j.trd.2020.102393 · Open version: https://ora.ox.ac.uk/objects/uuid:5f339482-629f-4e2f-8580-a8c083e3bce6 · Disruption database: https://github.com/jasperverschuur/Port_Disruption_database
- **Research question:** What do AIS data reveal about how long natural-hazard port disruptions last, and how ports recover?
- **Data:**
  - AIS: US MarineCadastre, Australian AMSA, and global UN Global Platform AIS (Apr–Dec 2019).
  - Hazard data: storm surge and wind from EM-DAT, NOAA and BoM.
- **Model design:** Disruption is identified from daily vessel activity against a normal baseline. Duration is regressed on hazard intensity (a fragility curve).
- **Key findings:**
  - 141 disruptions across 74 ports and 27 events.
  - **Median disruption is 6 days**, with a 95th percentile of 22.2 days.
  - Multiple ports are hit at the same time.
  - Each +1 m of surge or +10 m/s of wind adds about **2 days** of disruption.
  - Ships rarely substitute other ports, and lost production is often recaptured later.
- **What Yutong should borrow:**
  - This is **the closest methodological template** for her target definition.
  - A 6-day median means many weather disruptions **fit inside a single week**. Weekly aggregation can blur them, and she should test daily-to-weekly sensitivity.
  - Use **wind speed and wave height as continuous intensity features**, not just a "typhoon present" flag.
  - "Recapture" implies a **post-disruption rebound week**. She should exclude it or model it, so it isn't mistaken for a normal week.

### 13. Verschuur, J., Koks, E.E. & Hall, J.W. (2023). "Systemic risks from climate-related disruptions at ports." *Nature Climate Change* 13 (Brief Communication).
- DOI: https://doi.org/10.1038/s41558-023-01754-w · Open version: https://ora.ox.ac.uk/objects/uuid:8a330128-3840-4c35-a2f7-d36c62f9a97d
- **Research question:** How much trade and economic activity is at risk from climate-related port downtime worldwide?
- **Data/design:** Modeled downtime for about 1,320 ports, combined with maritime transport, trade-flow and supply-chain models.
- **Key findings:** About **US$81 billion of trade** and at least **US$122 billion of economic activity** are at risk each year. Knock-on effects are concentrated in small island states and economies whose ports and trade are poorly diversified.
- **What Yutong should borrow:** Use it to motivate why weather is the *dominant* baseline in maritime disruption, and to frame a dollar-at-risk translation of her forecasts in the write-up.

### 14. Notteboom, T., Haralambides, H. & Cullinane, K. (2024). "The Red Sea Crisis: ramifications for vessel operations, shipping networks, and maritime supply chains." *Maritime Economics & Logistics* 26(1): 1–20.
- DOI: https://doi.org/10.1057/s41278-024-00287-z (open access)
- **Research question:** What were the early operational and network effects of the 2023–24 Houthi attacks?
- **Data/design:** Descriptive and analytical. Covers rerouting via the Cape, fleet capacity absorption, schedules, freight rates and surcharges, and container imbalances.
- **Key findings:** A credible, *kinetic* threat to ships caused large, persistent diversion away from Suez and Bab el-Mandeb. PortWatch transit data show this clearly. Costs passed through freight rates and supply chains.
- **How this challenges her design:**
  - This is the **positive control**. When geopolitics truly disrupts transits, the drop is large, persistent and obvious in PortWatch.
  - She should **include Bab el-Mandeb/Suez as an out-of-region sanity check**: her pipeline should flag it. If her SCS signals show nothing comparable, that is evidence that SCS gray-zone pressure has *not yet* reached the threshold that diverts ships. This is a substantive geopolitical finding, not a failure.
  - Weather-driven drops are V-shaped, while threat-driven diversions are persistent. That difference suggests a second target: **disruption persistence**.

---

## C. Typhoons and port operations

### 15. "Economic impact of typhoon-induced wind disasters on port operations: A case study of ports in China." *International Journal of Disaster Risk Reduction* (2020), 101719.
- DOI: https://doi.org/10.1016/j.ijdrr.2020.101719
- **Citation note:** I could not confirm the author list from the abstract page I fetched. Fill it in from the DOI page before citing.
- **Research question:** How large are typhoon-wind losses at major Chinese ports?
- **Data:** Typhoon tracks and throughput for Shanghai, Ningbo, Shenzhen and Guangzhou, 2007–2017.
- **Model design:**
  1. Simulate typhoon wind fields to work out **port disruption days**, based on wind thresholds.
  2. Estimate daily cargo throughput.
  3. Calculate losses from the port, carrier, shipper and reputational perspectives.
- **Key findings:** Time-critical losses, mostly borne by shippers, dominate total losses.
- **What Yutong should borrow:** Use **wind-speed thresholds derived from simulated wind fields** (or Open-Meteo/ERA5 wind) at each chokepoint as features. Treat the "port closure wind threshold" as a physically motivated feature, such as hours above Beaufort 8 within the chokepoint polygon that week.

---

## D. Gray-zone activity, dark vessels and maritime militia

### 16. Park, J. et al. (2020). "Illuminating dark fishing fleets in North Korea." *Science Advances* 6(30): eabb1197.
- DOI: https://doi.org/10.1126/sciadv.abb1197 · PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC7455503/ · Code: https://github.com/GlobalFishingWatch/paper-dark-fishing-fleets-in-north-korea
- **Citation note:** Copy the full author list from the PMC page. The journal, volume, article ID and DOI are verified.
- **Research question:** Can fleets that don't broadcast AIS be detected and counted?
- **Data:** Four sensors fused together: AIS, Sentinel-1 SAR, VIIRS night-lights and high-resolution optical imagery.
- **Model design:** Satellite detections are matched against AIS, and unmatched detections are counted as "dark" vessels. Vessels are classified from imagery.
- **Key findings:** More than **900 Chinese-origin vessels** were fishing in North Korean waters in 2017 and more than 700 in 2018, plus about 3,000 North Korean vessels in Russian waters in 2018. All of this was largely invisible to AIS.
- **What Yutong should borrow:**
  - **AIS-only counts undercount gray-zone activity.** A feature built from GFW's AIS will miss militia vessels that switch transponders off.
  - Use GFW's **SAR vessel detections** (available through GFW APIs/data) for Scarborough Shoal and Second Thomas Shoal where possible, or explicitly note this limitation.
  - The methodology here is the model for a credible "dark activity index."

### 17. Paolo, F.S. et al. (2024). "Satellite mapping reveals extensive industrial activity at sea." *Nature* 625.
- DOI: https://doi.org/10.1038/s41586-023-06825-8 · PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC10764273/
- **Research question:** How much industrial maritime activity is missing from public tracking systems?
- **Data:** Sentinel-1 SAR and Sentinel-2 optical imagery (2017–2021), matched against AIS.
- **Model design:** Deep-learning detection and classification of vessels and offshore infrastructure.
- **Key findings:** **72–76% of industrial fishing vessels** and **21–30% of transport and energy vessels** are not publicly tracked. Untracked activity is concentrated in South and Southeast Asia and Africa.
- **What Yutong should borrow:**
  - Gives a quantitative basis for her limitations section: commercial cargo and tankers (her PortWatch target) are mostly visible, but the *gray-zone fleet* is mostly not.
  - This asymmetry is a key argument. It explains why the *target* is measurable while the *geopolitical driver* is undermeasured.
  - GFW's public SAR detections come from this pipeline.

### 18. Poling, G.B., Mallory, T.G. & Prétat, H. (2021). "Pulling Back the Curtain on China's Maritime Militia." CSIS Asia Maritime Transparency Initiative & C4ADS, November 2021.
- URL: https://www.csis.org/analysis/pulling-back-curtain-chinas-maritime-militia · PDF: https://csis-website-prod.s3.amazonaws.com/s3fs-public/publication/211118_Poling_Maritime_Militia.pdf
- **Research question:** Who makes up China's South China Sea maritime militia, and how can their vessels be identified?
- **Data:** Chinese-language government and company documents, AIS, remote sensing and on-site reporting.
- **Design:** Open-source investigation and vessel-level identification.
- **Key findings:** Identifies **122 confirmed and 52 likely militia vessels**, and documents the methods for identifying them.
- **What Yutong should borrow:**
  - **This is the bridge to her Mandarin skill.** Use the report's vessel list (names, MMSIs where published) to **tag militia vessels in GFW data**, then build a weekly "militia presence" feature near Scarborough Shoal, Second Thomas Shoal and Whitsun Reef.
  - Combining Chinese-source OSINT with AIS is exactly the workflow Everstream, Kpler and Sayari value.

---

## E. Taiwan Strait, PLA exercises and shipping

### 19. Tu, M.-R., Chen, S.-T., Hsu, H.-K. & Huang, K.-C. (2023). "Assessment of Impact on Navigation Safety in the Taiwan Strait during China's Naval Blockade Exercise." *2023 6th IEEE International Conference on Knowledge Innovation and Invention (ICKII)*.
- DOI: https://doi.org/10.1109/ICKII58656.2023.10332637 · IEEE Xplore: https://ieeexplore.ieee.org/document/10332637/
- **Weight:** A regional IEEE conference paper, much lighter than the other entries. It is included because it is the only verified peer-reviewed AIS study of a PLA exercise I found.
- **Research question:** How did the August 2022 PLA exercises change ship routing and collision risk in the Taiwan Strait?
- **Data:** AIS before and during the exercise, plus GIS/ENC chart data.
- **Design:** Compares traffic density across gate lines and simulates collision risk for rerouted vessels.
- **Key findings:** Ships **rerouted around the exercise zones instead of stopping**, and navigation risk in the remaining corridors rose significantly.
- **What Yutong should borrow:** This **directly explains her null finding on PLA drills**. Drills redistribute traffic *spatially* inside or around the chokepoint without reducing the *aggregate* count PortWatch measures. Better targets for drills would be:
  - route deviation or detour distance
  - traffic density in sub-corridors
  - speed changes
  - transit time

  (These are available from GFW tracks.)

### 20. CSIS ChinaPower Project (2024). "How China Could Quarantine Taiwan: Mapping Out Two Possible Scenarios." Center for Strategic and International Studies, June 2024.
- URL: https://www.csis.org/analysis/how-china-could-quarantine-taiwan-mapping-out-two-possible-scenarios · Interactive: https://features.csis.org/chinapower/china-quarantine-taiwan/
- **Citation note:** Check the author byline on the CSIS page. The publisher and date are verified.
- **Research question:** What would a law-enforcement-led "quarantine" of Taiwan look like, as distinct from a military blockade?
- **Design:** Scenario analysis using open-source data on CCG and MSA vessels and the maritime militia.
- **Key findings:**
  - A quarantine led by the China Coast Guard and Maritime Safety Administration (inspections and boarding of Taiwan-bound ships), backed by PLA forces and militia, could pressure Taiwan without closing the strait.
  - Two scenarios: a limited port-focused operation, and a full quarantine extending 24 nm around Taiwan with 30+ CCG/MSA vessels and about 40 militia vessels.
- **What Yutong should borrow:**
  - Gives a **theory of which signals should matter**. The gray-zone escalation ladder runs from CCG presence to MSA announcements to inspections. Counts of PLA aircraft or ships alone don't capture it.
  - Suggests **port calls at Kaohsiung and Keelung** (also in PortWatch) as a more sensitive target than strait transits.
  - Supports adding **CCG/MSA official announcements** (Chinese-language) as features.

---

## F. Methods for rare-event forecasting, validation and explanation

### 21. Chen, T. & Guestrin, C. (2016). "XGBoost: A Scalable Tree Boosting System." *Proceedings of KDD 2016*: 785–794.
- DOI: https://doi.org/10.1145/2939672.2939785 · arXiv: https://arxiv.org/abs/1603.02754
- **Contribution:** Regularized gradient-boosted trees with sparsity-aware split finding, weighted quantile sketch and cache-aware computation.
- **What Yutong should borrow:**
  - Cite it as the model.
  - Use `scale_pos_weight` (roughly negatives/positives) or sample weights for imbalance.
  - Keep `max_depth` small (2–4), use strong regularization and early stopping on a *time-ordered* validation fold. With about 8 chokepoints × about 400 weeks, the dataset is small, so overfitting is the main risk.

### 22. Muchlinski, D., Siroky, D., He, J. & Kocher, M. (2016). "Comparing Random Forest with Logistic Regression for Predicting Class-Imbalanced Civil War Onset Data." *Political Analysis* 24(1): 87–103.
- DOI: https://doi.org/10.1093/pan/mpv024 · RePEc: https://ideas.repec.org/a/cup/polals/v24y2016i1p87-103_9.html
- **Research question:** Do tree ensembles beat (rare-event / penalized) logistic regression on rare-onset data?
- **Design:** Random forests vs. standard, Firth rare-event and L1-penalized logit, evaluated out of sample with AUC and F1.
- **Key findings:** Random forests predicted onsets that the logit models missed.
- **Caveat:** A published critique and the authors' 2018 reply ("Seeing the Forest through the Trees," *Political Analysis*, https://doi.org/10.1017/pan.2018.45) acknowledged implementation errors and higher false-positive rates, though they argued the core result holds.
- **What Yutong should borrow:** Always include a **regularized logistic regression baseline**. The debate shows that apparent ML gains can come from evaluation choices, so pre-register the metric and the validation scheme.

### 23. Cerqueira, V., Torgo, L. & Mozetič, I. (2020). "Evaluating time series forecasting models: an empirical study on performance estimation methods." *Machine Learning* 109(11): 1997–2028.
- DOI: https://doi.org/10.1007/s10994-020-05910-7 (open access)
- **Research question:** Which performance-estimation scheme gives the most accurate estimates of true forecasting error?
- **Design:** Compares 11 methods (CV variants, holdout, prequential/rolling-origin) on 174 real series plus synthetic ones.
- **Key findings:**
  - Blocked CV works well for **stationary** series.
  - For **non-stationary** real-world series, out-of-sample or holdout-style schemes (repeated holdout performed best) give more accurate estimates.
- **What Yutong should borrow:**
  - Shipping series are non-stationary (COVID-19, the Red Sea, the trend in fleet growth), so **use walk-forward (rolling or expanding origin) evaluation**, as planned.
  - Add a **gap/embargo** between train and test equal to the label's look-back window (e.g., 8 weeks), so the rolling-median baseline in the target doesn't leak.

### 24. Saito, T. & Rehmsmeier, M. (2015). "The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets." *PLOS ONE* 10(3): e0118432.
- DOI: https://doi.org/10.1371/journal.pone.0118432 (open access)
- **Key finding:** On imbalanced data, ROC-AUC can look good while false positives explode. PR curves show precision among flagged cases directly.
- **What Yutong should borrow:** Report **PR-AUC (average precision)** as the main metric, with the no-skill line equal to the base rate. Also report the **Brier score** and a calibration plot. Keep ROC-AUC as secondary.

### 25. Lundberg, S.M. et al. (2020). "From local explanations to global understanding with explainable AI for trees." *Nature Machine Intelligence* 2: 56–67.
- DOI: https://doi.org/10.1038/s42256-019-0138-9 · PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC7326367/
- **Citation note:** Check the author list on the PMC page. The title, venue and DOI are verified.
- **Contribution:** TreeExplainer computes exact Shapley values for tree ensembles in polynomial time. It adds SHAP interaction values and global summaries (summary and dependence plots).
- **What Yutong should borrow:**
  - Use TreeSHAP on the XGBoost model.
  - **Group SHAP values by feature family** (weather / season / news / gray-zone / statements) to answer "how much does geopolitics contribute?"
  - Use **interaction values** to test whether geopolitical signals matter *only when weather is calm*.
  - **Caveat:** SHAP explains the model, not causation. Correlated features (e.g., GDELT volume and typhoon-related news) split credit between them. The *predictive-gain test* (synthesis point 2) is the primary evidence; SHAP is supporting.

---

## Excluded or unverified
- Typhoon/port papers by Zhang & Lam and Cao & Lam: I didn't verify a specific citation, so they are omitted. Cao & Lam (2019) is referenced inside Verschuur et al. (2020) on short-duration weather effects; Yutong can get the citation from there.
- Satellite-imagery "When the Strait came to a halt" (facostarainis.github.io): a blog, not peer-reviewed. Not included.
- Reuters and Lloyd's List (Aug 2022) reports of about 200+ vessels rerouting during the drills: useful journalism, consistent with #19, but not papers.
- Other relevant work I saw but didn't fully verify:
  - Michelini et al. (2023), "Extreme weather impacts do not improve conflict predictions in Africa" (*Humanities & Social Sciences Communications*). It is the mirror image of her question: weather adding nothing to conflict forecasts.
  - Mueller & Rauh (2022), "Using past violence and current news to predict changes in violence" (*International Interactions* 48(4)).
  - Both appear in RePEc listings. Read them before citing.

---

## Synthesis: design implications for the project

1. **Reframe the target. Separate "volume drop" from "rerouting" and "persistence."**
   - Verschuur et al. (#12) show weather disruptions are short (median 6 days), V-shaped and followed by recapture.
   - The Red Sea (#14) shows geopolitical disruption looks different: persistent diversion.
   - The Taiwan Strait study (#19) shows drills cause **spatial rerouting, not aggregate drops**.

   So:
   - (a) Keep the main binary target: weekly transits more than 15% below the trailing 8-week median. Test sensitivity at 10%, 20% and 25%, and also run a daily version.
   - (b) Add a **persistence target**: disruption lasting 2+ or 3+ consecutive weeks. Weather rarely does this; geopolitics might.
   - (c) Optionally add a **rerouting/route-deviation target** from GFW tracks for the Taiwan Strait.
   - (d) Consider **Kaohsiung and Keelung port calls** as a more sensitive target for quarantine-style pressure (#20).

2. **Make the incremental-value test the headline, with strong baselines.** Following ViEWS (#4, #5), Mueller & Rauh (#2, #3) and Bazzi et al. (#6), compare nested models under the *same* walk-forward splits:
   - **M0:** seasonal-naïve or climatology (base rate by chokepoint × week-of-year)
   - **M1:** weather + season + lagged transits (persistence)
   - **M2:** M1 + global GPR, Threats and Acts (#1)
   - **M3:** M2 + local GDELT tone and volume (as within-chokepoint z-scores, #2, #7)
   - **M4:** M3 + gray-zone (GFW AIS + SAR dark detections, militia tags from #18) + Chinese MFA/CCG/MSA statement counts

   Report ΔPR-AUC and ΔBrier with **block-bootstrap confidence intervals** across test weeks. Add a regularized logistic regression version of each model (#22). Run a simple ensemble as a check (#5).

   A small or zero gain is a legitimate, interesting result: "SCS gray-zone pressure has not yet reached a threshold that changes commercial transit volume." Prior literature predicts exactly this (#6, #8, #19).

3. **Use GPR the way it was designed: as a global baseline, split into threats and acts.**
   - Aggregate the daily GPR to weeks and include both the **level and the change** (Δ, or a z-score against the trailing 52 weeks).
   - Include **Threats and Acts separately**, plus country-specific GPR for China/Taiwan/Philippines if they're in the download.
   - Lag every geopolitical feature by at least one week so the forecast is genuinely ex-ante.
   - The research claim then becomes sharper: *do local, Chinese-language and vessel-level signals add value beyond the standard Fed GPR index?* That framing is legible to economists and risk teams alike.

4. **Evaluate like a rare-event forecaster.**
   - Use walk-forward with an expanding window plus an **embargo gap** at least as long as the label look-back (8 weeks), so the rolling-median baseline doesn't leak (#23).
   - Use **PR-AUC as the primary metric**, plus Brier/calibration (#24).
   - Handle imbalance with `scale_pos_weight` rather than SMOTE, which can create unrealistic synthetic time-series points.
   - Choose the alert threshold by an explicit **cost ratio** (#3).
   - Use **stratified evaluation**:
     - all disruptions vs. **non-weather disruptions**, meaning weeks with no typhoon within X km and wave height below Y m (the "hard problem")
     - calm-weather weeks only
   - Run a **Red Sea / Bab el-Mandeb positive control** (#14) to show the pipeline *can* detect geopolitics when it's real.

5. **Engineer weather as physical intensity, not just presence.** Following #12 and #15, use:
   - max wind and hours above a closure threshold
   - max significant wave height
   - typhoon distance to the chokepoint polygon from IBTrACS/NOAA
   - a **rebound-week indicator**, since recapture follows disruption (#12)

   Strong weather features matter for two reasons. They make the incremental geopolitical test fair. They also stop SHAP from misattributing weather-correlated news spikes (typhoon coverage in GDELT) to "geopolitics." Filter GDELT to CAMEO codes and actors tied to political or military events.

6. **Be explicit about measurement asymmetry in the limitations section, and turn it into a selling point.**
   - Commercial cargo is mostly AIS-visible; the gray-zone fleet is mostly dark (#16, #17).
   - GDELT geography is unreliable (#7).
   - SHAP is associational (#25).

   Mitigate:
   - Use GFW SAR detections and the CSIS militia vessel list (#18).
   - Use GDELT only as a time series of attention.
   - Group SHAP by feature family and test interactions with calm weather.

   Saying this clearly in the write-up shows analytical maturity. Combined with Chinese-language sources, it is the differentiator for Everstream, Kpler and Sayari-type roles.
