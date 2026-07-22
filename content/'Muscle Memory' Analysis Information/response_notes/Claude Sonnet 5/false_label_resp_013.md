# resp_013 — Claude Sonnet 5 — false_label (total 7)

> **Scoring note:** False data set that overclaims in many places but does correctly identify structure and grouping. It is sophisticated at answering about artifacts but terrible at infering (uses GR513 incorrectly twice).

## 1. Patterns in the Data

**a) A clear bimodal movement‑strategy structure**

Most animal‑years cluster into two groups:

- **Resident/philopatric majority** (~70% of records): `summer_disp_km` 2–8 km, `max_disp_km` 8–20 km, `days_away` mostly 0–5 d, `winter_spread_km` ~1–1.5 km. E.g. YL107, YL120_BL290, YL161, YL174, OR77/79/84/85/88/93/98 — classic small, stable, year‑round home ranges typical of central‑European/British roe deer.

- **Long‑distance excursive/migratory minority**: `summer_disp_km` 15–60 km, `days_away` 50–280 d, `max_disp_km` often >25 km (up to 64 km in OR78/OR41). Examples: OR55_OR15, OR78, OR56_BL251, GR513, YL25, YL29, YL57, YL74, YL93, YL168, YL176, YL180, YL166, YL170.

**b) The excursive behaviour is repeatable within individuals, not a one‑off event**

Where the same ID is tracked over multiple years, the strategy is highly consistent:
- OR55_OR15: 58–59 km displacement, 103–171 days away, in **every one of 4 tracked years** (2014–2019).
- OR78: 57–60 km, 79–215 days away, across 4 years.
- OR56_BL251: ~38 km, 108–202 days away, 3 consecutive years.
- YL166/YL170: ~15 km, 120–225 days away, repeated 3–4 years.

This repeatability argues against a single "natal dispersal" event (which should occur once, typically at 1–2 years of age) and instead looks like **recurring seasonal migration or long-distance excursions** that persist across the animal's tracked lifetime.

**c) Winter ranges stay compact regardless of summer behaviour**

`winter_spread_km` is almost uniformly low (mostly 1–1.5 km) even for animals with enormous summer displacement (e.g. GR513: winter_spread 0.03 km but max_disp 39.5 km; OR55_OR15: winter_spread ~0.7–1.5 km but max_disp ~60 km). This suggests migrants **return to and reoccupy a small, discrete winter core area** rather than simply expanding their range — consistent with true two-range partial migration rather than nomadism.

**d) Path length (total distance travelled) does not scale simply with displacement**

Some low-displacement residents rack up very high `path_km` per fix count (e.g., GR154, GR122, YL107 — dense, tortuous local movement), while some big migrants show relatively *modest* path length for their fix count (e.g. GR513: 9,376 fixes but only 692 km; OR23: 4,263 fixes, 824 km). This implies migrants often sit still for long periods within each seasonal range and undertake one or two rapid transit bouts, rather than moving further every day.

**e) Population/site clustering**

The excursive/migratory phenotype is concentrated in certain site-ID prefixes (OR, YL, GR) and essentially absent in others (most BL- and pure GR-coded animals are residents). This points to **landscape or study-area effects** rather than a trait randomly distributed across the whole population.

**f) Sampling artefacts to flag**

Several very low `n_fixes` rows (e.g., OR100 2013/2019 ~350–480 fixes; YL153, YL173 ~500–800 fixes) reflect partial-year deployments (collar fitted late, failed early, or animal died), not true low mobility — these low-effort years generally also show reduced `days_away`/`max_disp`, which is at least partly a truncation artifact and should be treated cautiously in comparative analyses.

## 2. Candidate Hypotheses

1. **Partial migration driven by resource seasonality**: A genetically or environmentally determined subset of females migrates tens of km between distinct summer and winter ranges to track seasonal food resources (e.g., agricultural crops in summer vs. woodland/shelter in winter), while the majority remain year-round residents in stable, resource-rich habitat patches.

2. **Individual specialization / repeatable personality or early-life imprinting**: Because the same individuals show the same extreme displacement pattern across multiple years, migratory tendency may be a fixed individual trait (heritable or set by natal-habitat experience) rather than a flexible annual response to conditions — similar to partial migration syndromes documented in other deer/ungulate systems.

3. **Landscape structure / fragmentation effect**: Sites where migratory behaviour is common (OR, YL) may have more fragmented or patchy habitat, forcing individuals to commute between separated resource patches, whereas BL/GR sites may offer contiguous habitat sufficient for full-time residency. Alternatively, differences could reflect local population density (density-dependent dispersal from crowded natal ranges).

## 3. Additional Data to Test These Hypotheses

- **Fine-scale temporal data (fix timestamps/dates)** to precisely map excursions to season, and check if migration timing aligns with crop harvest, rut, or parturition.
- **Land-cover/habitat maps** (forest cover, crop type, urban/road density) at each site to test whether migratory individuals link two specific habitat types and whether site-level fragmentation predicts prevalence of migration.
- **Age, reproductive status, and capture history** for each individual — to test whether migration is linked to age class (post-dispersal subadults vs. adults) or reproductive state (e.g., non-lactating females ranging further).
- **Population density estimates** per site/year to test the density-dependent dispersal hypothesis.
- **Genetic/pedigree or maternal-lineage data** to assess heritability of migratory tendency across dams and offspring.
- **Weather/snow-cover data**, especially winter severity, to test if migration correlates with harsher conditions in the "away" range.
- **Deployment/collar metadata** (fit date, fault/mortality date) to properly correct for partial-year sampling artifacts before any further quantitative modeling.
- **Habitat-selection (step-selection) analysis** using the raw fix data to confirm that "days away" correspond to a genuine second core-use area rather than exploratory wandering.
