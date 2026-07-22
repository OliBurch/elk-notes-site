# resp_029 — Claude Sonnet 5 — false_label (total 9)

> **Scoring note:** False tier response which actively names the margin and winter ranges in a cleanly articulated manner. Overclaims in some places.

# Movement Ecology Interpretation: GPS-Collared Female Roe Deer

## 1. Key Patterns in the Data

**A. Two distinct movement tactics — clear bimodality**

`summer_disp_km` shows a strong gap in the distribution: most individual-years cluster below ~9 km (the classic sedentary, small-home-range roe deer pattern), while a discrete subset ranges from ~13 km up to 60 km. There is essentially no continuum between these groups — animals are either "residents" or "long-distance movers," not evenly spread across the range. Roughly a quarter to a third of individual-years fall into the high-displacement group (e.g., OR55_OR15, OR78, YL25, YL29, YL57, YL74, YL93, OR56_BL251, YL168, YL176, GR513, YL114_BL274, etc.).

**B. Days away from range tracks displacement almost linearly**

`days_away` is near zero for the low-displacement group (many rows = 0.0), but reaches 100–280 days for the high-displacement group. This is not a brief exploratory sortie — for several individuals the animal spends a third to over half the year away from its core range, which is more consistent with **seasonal migration between two ranges** than with occasional excursions.

**C. Winter range stays tight regardless of tactic**

`winter_spread_km` is compressed (mostly 0.5–1.6 km) for both residents and long-distance movers. This is important: if these deer were simply nomadic or ranging unpredictably, we'd expect winter spread to scale with summer displacement. Instead, migrants appear to settle into a **stable, compact winter range**, just one that is geographically distant from the summer range — the signature of true seasonal migration rather than nomadism.

**D. Strong individual repeatability, but some plasticity**

Where multiple years exist for the same ID, behavior is often highly consistent:
- Stable residents: OR99, YL107, YL120_BL290, YL124, YL163 — low displacement and 0 days away across 4–6 years.
- Stable migrants: OR55_OR15 (~58–60 km displacement, every year sampled), OR78, YL168, YL176 — very consistent high displacement/days-away across years.

But some individuals switch dramatically between years — OR60_BL288 (3.8–28.7 km across 5 years), GR513 (single huge spike: 150 days away, only sampled once), YL154 and YL166 (declining/variable displacement over time). This suggests movement tactic is not fixed for all animals — some show **condition- or context-dependent switching**, distinct from the "hard-wired migrant" individuals.

**E. Confounding by deployment duration**

`n_fixes` ranges from 234 to over 17,000, indicating highly variable tracking duration (from a few months to multiple years of near-continuous fixes). Cumulative metrics like `path_km` and `days_away` are partly driven by how long the collar operated, not just by behavior — shorter deployments (common from 2018–2019 in the "YL" series) will show lower cumulative values by default and must be interpreted per unit time, not as raw totals.

## 2. Hypotheses

**H1 — Facultative partial migration for resource tracking.** A subset of the population migrates seasonally between summer and winter ranges (likely tracking crop phenology in agricultural mosaics — e.g., forage in oilseed rape/cereals in summer vs. woodland cover in winter), while the remainder are habitat generalists/residents with year-round access to adequate resources in one place.

**H2 — Individual-level behavioral syndrome ("personality") with density- or condition-dependent plasticity.** Most migrant/resident status is a stable individual trait (strong within-individual repeatability across years), but body condition, age, or local population density in a given year can push some individuals to switch tactics (explaining cases like OR60_BL288 or GR513).

**H3 — Site-specific landscape effects.** Since ID prefixes likely correspond to distinct study sites/populations, the strong clustering of migratory behavior among certain prefixes (many OR/YL codes) versus near-total residency in others (many BL/GR codes) suggests that landscape configuration — fragmentation, distance between seasonal resource patches, or human land-use pattern — determines the *prevalence* of migration in a population, rather than migration being an individual quirk.

**H4 (alternative to H1)** — Some single-year displacement spikes (e.g., GR513, single-record IDs with huge days_away) may reflect **natal or breeding dispersal events** rather than repeated seasonal migration, and should be distinguished from the multi-year, repeatable migrants.

## 3. Additional Data to Test These Hypotheses

- **Site coordinates and land-cover/habitat maps** (agricultural type, woodland %, fragmentation) per study area, to link tactic prevalence to landscape structure (tests H1, H3).
- **NDVI/vegetation phenology data** by season and site, to test whether migration timing tracks green-up/harvest cycles.
- **Age, body mass/condition, and reproductive status** at capture and annually, to test age- or condition-dependent switching (H2, H4) and to separate natal dispersal from repeat migration.
- **Local population density estimates** per site/year, to test density-dependent partial migration.
- **Collar deployment start/end dates and fix schedule**, to normalize `path_km`, `days_away`, and `n_fixes` properly (days tracked, fix interval) rather than comparing raw cumulative totals.
- **Genetic/kinship data**, to test whether migratory tendency clusters within related individuals (heritability of tactic).
- **Weather/snow cover and hunting-season/harvest calendars**, since roe deer movements in agricultural landscapes are often tied to human disturbance and crop cycles.
- **Cause of collar end (mortality vs. failure vs. still active)**, to check if short-duration records reflect increased mortality risk associated with long-distance movement (a fitness cost/benefit angle on the two tactics).
