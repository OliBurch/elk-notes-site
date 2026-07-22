# resp_005 — Claude Sonnet 5 — informed (total 7)

> **Scoring note:** True data set which makes assertions about the local town that the data cannot back up. It does notice grouping but alike repo_003 it notices the weakness in the data and then tries to draw it out. Raises sampling effort and detection bias for the extreme max-displacement cases.

# Movement Ecology Analysis: GPS-Collared Female Elk (Banff Area)

## 1. Key Patterns in the Data

**A. Clear partial migration signature (bimodal displacement)**
When individuals are ranked by `summer_disp_km` and `days_away`, the population splits into two clusters:
- **Residents**: summer_disp_km ≈ 2–6 km, days_away ≈ 0–20 days, max_disp_km typically <15 km (e.g., BL215, YL107, YL137_BE13, OR99 in most years).
- **Long-distance migrants**: summer_disp_km ≈ 15–60 km, days_away often >100–280 days, max_disp_km often >20–65 km (e.g., OR55_OR15, OR78, YL168, YL176, GR513, YL29, YL25, YL93).

This is the classic Banff elk "partial migration" pattern well documented in the literature — some cow elk migrate seasonally out of the park (often toward provincial land), others remain resident year-round near town/valley-bottom ranges.

**B. Individual plasticity / tactic-switching across years**
Several repeatedly-collared individuals switch strategy between years rather than showing a fixed tactic:
- **OR60_BL288**: summer_disp swings from 3.8 km (2018) to 28.7 km (2015); days_away from 47.9 to 175.7.
- **YL154, YL166, YL170, YL112_OR38**: fluctuate between "moderate migrant" and near-resident behavior across consecutive years.
- **OR99, OR97**: mostly resident, but with occasional years of elevated max_disp.

This suggests migratory tendency is not a fixed individual trait for all elk—facultative switching is common, distinct from individuals like OR55_OR15 or OR78 that are consistently extreme migrants every year (fixed strategists).

**C. Decoupling of “max_disp” from “typical range use”**
Some individuals show a large max_disp_km despite very low summer_disp_km and near-zero days_away (e.g., OR41 2013: summer_disp 4.78 km but max_disp 63.77 km, days_away only 2.4; BL234 2011: summer_disp 2.58, max_disp 25.17; YL30 2006: summer_disp 3.46, max_disp 44.21). These look like **brief exploratory forays or single dispersal-like excursions** rather than sustained seasonal migrations.

**D. Winter range fidelity is far more homogeneous than summer behavior**
`winter_spread_km` clusters tightly around 1–1.8 km for nearly every individual regardless of migratory status (residents and long-distance migrants alike). Only a handful of outliers deviate (GR513 2015 = 0.03 km — extremely tight; YL28 2005 = 2.85; YL93 = 2.37). This implies winter aggregation behavior (likely driven by snow, forage limitation, or predator-defense herding) is a strong, conserved population-level constraint, while summer range strategy is the primary axis of individual variation.

**E. Total path length is roughly independent of migratory strategy**
`path_km` (annual cumulative distance moved) stays broadly similar (~700–1800 km/yr) for both residents and migrants. Migrants aren't necessarily "moving more" overall—they're organizing similar total movement into a directed seasonal shift rather than local, tortuous foraging loops. This points to a redistribution of movement in space, not a change in overall activity/energy expenditure.

**F. Sampling effort varies enormously (n_fixes: 234–17,196)**
This reflects differing collar duty cycles, deployment length, or partial-year tracking (note many low-n_fixes records occur in first/last year of collar life, e.g., 234–500 fixes). This is a potential confound: short deployments could undersample rare long excursions, potentially underestimating true max_disp/days_away for some animals.

---

## 2. Candidate Hypotheses

**H1 — Partial migration driven by individual/maternal or spatial factors.**
Distinct "resident" vs "migrant" elk reflect stable individual tactics, potentially linked to matrilineal learning (calves adopt mother's migratory route), natal range location relative to migration corridors, age, or reproductive costs (residents may be older/less able to migrate, or migrants gain better forage/predator-avoidance tradeoffs).

**H2 — Facultative switching driven by interannual environmental variability.**
Individuals like OR60_BL288 and YL154 that alternate strategies year to year may be responding to variable snowpack, spring green-up timing/NDVI phenology, forage abundance, or human/wolf disturbance pressure — migrating in years when conditions favor movement and staying resident when they don't (e.g., pregnancy/lactation constraints or poor body condition may favor staying resident).

**H3 — Predation risk (wolves/human hunting) drives winter aggregation regardless of summer strategy.**
The consistently tight winter_spread across all individuals suggests a fitness-driven convergence on shared secure winter range (e.g., near town, or low-snow valley bottoms) that overrides individual summer strategy differences — consistent with known wolf-predation refuge use by elk in Banff townsite areas.

**H4 (secondary/methodological) — Sampling effort artifacts.**
Extreme max_disp/low-days-away combinations (e.g., OR41, BL234-2011) could partly reflect brief GPS-tracked exploratory or dispersal movements rather than true behavioral shifts, and variation in n_fixes/deployment duration could bias detection of rare extreme movements across individuals.

---

## 3. Additional Data to Test These Hypotheses

1. **Individual biological covariates**: age, pregnancy/lactation status, body condition score, and mother-offspring/matriline identity — to test maternal transmission of migratory tactic (H1).
2. **Environmental/phenological data**: snow water equivalent (SWE), NDVI green-up curves, and spring green-wave timing across summer/winter ranges — to test whether switching (H2) tracks environmental variability.
3. **Predator/human-risk layers**: wolf pack territories/kill site data, cougar density, hunting-zone boundaries outside the park, and human recreational trail/road density — to test winter aggregation and refuge hypotheses (H3).
4. **Fine-scale telemetry metadata**: GPS fix schedule/duty cycle and deployment start/end dates per collar-year, to properly normalize path_km, max_disp, and days_away for sampling effort (H4).
5. **Land cover/elevation/distance-to-park-boundary** data to classify likely migratory corridors and destination ranges (e.g., differentiate a true seasonal migration from a short exploratory foray).
6. **Survival/reproductive outcome data** (calf survival, adult mortality cause) linked to each elk-year, to assess fitness consequences of resident vs. migrant vs. switching tactics — critical for turning these descriptive patterns into an adaptive/ecological explanation.
7. **Multi-year continuous tracking** for more individuals (many here have gaps) to better quantify the frequency and triggers of strategy-switching over an individual's lifetime.
