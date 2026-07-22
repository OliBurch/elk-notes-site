# resp_023 — Claude Opus 4.8 — false_label (total 11)

> **Scoring note:** Very strong false data response that although suggests labels are distinct areas doesn't assert anything that the data cannot support. Still doesn't question the large displacements for roe deer but captures everything else needed for a strong response.

## 1. What the data show

I read the six measurements as a movement "fingerprint" for each animal‑year: how far the summer range sits from the winter range (`summer_disp_km`), the single farthest point reached (`max_disp_km`), how compact the winter range is (`winter_spread_km`), how long the animal was absent from its normal range (`days_away`), and total distance travelled (`path_km`).

**a) The population is a textbook case of partial migration.**
`summer_disp_km` is strongly bimodal. Most animal‑years cluster at **2–6 km with ~0 days away** (residents), and a distinct minority sit at **~15–60 km with 60–290 days away** (migrants). There is very little in between at the population level. `days_away` and `summer_disp_km` are tightly coupled — animals that go far, stay away for months and then return to a wintering ground.

**b) Migration distance itself is multimodal.**
Among migrants I see loose clusters around **~15–20 km, ~28–40 km, and ~58–60 km** (e.g., OR55/OR78/YL29 all sit near 58–60 km across multiple years). This hints at discrete summer destinations rather than a continuous gradient.

**c) The tactic is highly repeatable within individuals.**
Where the same ID appears across years, behaviour is usually consistent:
- Committed migrants repeat almost identically: **OR55_OR15** (58.0, 59.4, 58.5, 58.6 km over four years), **OR78** (~57–60 km), **OR56_BL251** (~38 km), **YL166**, **YL176**.
- Committed residents repeat too: **OR99, YL107, YL120, YL124, YL161, OR100** stay at 2–5 km year after year.

This individual‑level fidelity is a real biological signal, not noise.

**d) But a subset are *facultative* switchers.**
Some animals flip between tactics: **YL112_OR38** (8.5 → 23.8 → 5.0 → 3.6 → 22.3 km), **OR60_BL288** (28.7 → 9.3 → 19.5 → 3.8 → 15.5), **OR65_BL265** (resident year then 213 days away the next), and **OR89**, which *decays* from migratory to resident over five years (18 → 3 km). These are the most interesting individuals ecologically.

**e) Winter ranges are compact and stable regardless of tactic.**
`winter_spread_km` is ~1 km for almost everyone, migrant or resident, consistent with strong winter site fidelity to a shared wintering area. A few extreme values (0.01–0.03, or 2.4–2.9) look like tracking artefacts (very short winter coverage) rather than biology.

**f) `max_disp` separates migration from exploratory forays.**
For true migrants `summer_disp ≈ max_disp` (they go and stay). Several *residents* have a large `max_disp` but small `summer_disp` and ~0 days away — e.g., **OR41** (summer 4.8, max **63.8**, 2.4 days), **OR99 2014** (4.1 vs **43.8**), **YL30** (3.5 vs 44.2). These are brief exploratory excursions/forays, not seasonal migration.

**g) A caveat: `path_km` is largely a sampling artefact.**
Path length tracks `n_fixes` almost mechanically (more fixes → more recorded path, and years with 300–800 fixes have short paths). I would **not** interpret `path_km` as true activity without correcting for fix number/schedule.

## 2. Hypotheses

1. **Resource/phenology-driven partial migration.** In this fragmented lowland landscape, some individuals track spring green-up or move to specific summer forage patches (e.g., woodland edge, crops), then return to reliable winter cover. The discrete distance clusters would then reflect the geography of good summer patches.

2. **Condition-, state- or density-dependent tactic choice.** Facultative switchers (YL112, OR60, OR65) and the OR89 "settling down" trajectory suggest the decision depends on a changing internal or external state — reproductive status, age, body condition, or local density/competition. Subordinate or younger animals may be displaced further.

3. **Fixed intrinsic/heritable tactic ("migratory syndrome").** The strong year-to-year repeatability of committed migrants and residents points to a partly genetic, maternally inherited, or early-life-imprinted strategy, with only a plastic subset responding to conditions.

## 3. Data that would test these

- **Individual state**: age, body mass/condition, reproductive status and parturition dates, and sex (all female here, so within-sex variation in condition/age matters).
- **Environmental drivers**: NDVI/vegetation phenology, land-cover maps, crop calendars, and winter severity (snow, temperature) to test resource- and weather-driven switching, especially against the facultative animals' year-to-year flips.
- **Spatial context**: capture-site coordinates and the actual summer/winter range locations, to test whether distance clusters correspond to shared destinations and whether tactic clusters by site (the ID prefixes BL/GR/OR/YL/BE suggest distinct capture areas).
- **Population/social data**: local density, culling/mortality, sex ratio — to test density-dependent displacement.
- **Relatedness/genetics**: pedigree or genetic sampling to test heritability/maternal inheritance of the migratory syndrome.
- **Finer temporal resolution and standardised fix schedules**: to date migration timing precisely, distinguish forays from migration objectively, and make `path_km`/activity comparable across years (correct for `n_fixes`).
- **Longer individual time series**: to see whether OR89-type transitions reflect ageing/maturation versus one-off responses.

**Bottom line:** this is a partially migratory roe deer population with a strongly repeatable, individually-fixed migratory tactic in most animals, a compact shared wintering strategy, and a small but ecologically informative set of facultative switchers — the latter being the best natural experiment for identifying what drives the decision to migrate.
