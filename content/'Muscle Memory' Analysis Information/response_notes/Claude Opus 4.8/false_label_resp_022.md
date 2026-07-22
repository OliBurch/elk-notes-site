# resp_022 — Claude Opus 4.8 — false_label (total 7)

> **Scoring note:** False data response insistent on the naming being about structured locational groups. Does outline a very loose margin and catches structure. First response to label excursion cases correclty.

## 1. What the data show

**Setup.** Each row is one deer-year. The informative axis is `summer_disp_km` — how far the animal's summer range sits from its winter range — paired with `days_away`, the time spent at that displaced summer location. `winter_spread_km` is essentially a home-range‑size index; `max_disp_km` is the single farthest point reached; `path_km` and `n_fixes` are effort/sampling terms.

**Finding 1 — This is a classic partial-migration system.**
`summer_disp_km` is strongly bimodal, and the two modes are cleanly separated by `days_away`:

- **Residents** (the majority): `summer_disp` ≈ 2–6 km, `days_away` ≈ 0 (often exactly 0). Winter and summer ranges overlap; the animal never leaves.
- **Migrants** (a substantial minority): `summer_disp` from ~8 up to ~58 km, coupled with `days_away` of tens to >250 days. These animals make a seasonal round-trip to a discrete summer range and return.

`summer_disp_km` and `days_away` are almost perfectly coupled (r ≈ 0.9): displacement without prolonged absence essentially doesn't occur. That is the fingerprint of *seasonal migration*, not permanent dispersal.

**Finding 2 — Migration distance, when it happens, is highly variable but individually stereotyped.** Committed migrants return to the *same* distant summer range year after year with remarkable fidelity:
- OR55_OR15: ~58–59 km every year (2014–2019)
- OR78: ~58 km every year
- OR56_BL251: ~38 km; YL176: ~30 km; YL166: ~15–17 km.
This constancy across years implies memory/tradition — a fixed summer destination, not random wandering.

**Finding 3 — Migratory tactic is plastic in many individuals.** Several deer switch tactic between years:
- OR89: migrant in 2015 (18 km, 121 d) → progressively shorter → resident by 2019 (3 km, 0 d).
- YL112_OR38: alternates (8 → 24 → 5 → 4 → 22 km) year to year.
- OR60_BL288, YL167_OR10, YL170: intermediate and fluctuating.
So migration here is *facultative/conditional*, decided anew each year, not a fixed genetic morph.

**Finding 4 — Don't confuse forays with migration.** Some clear residents show huge `max_disp_km` (e.g., OR41: summer_disp 4.8 km but max_disp 63.8 km, days_away 2.4; OR100 2016: max 36.8, days_away 16; YL30: max 44, resident). These are brief exploratory excursions (or GPS outliers), *not* seasonal relocations. `max_disp` alone would badly overstate migratory behaviour.

**Finding 5 — Winter range size is stable and small.** `winter_spread_km` clusters tightly around ~1 km with little relation to migratory status (a few high values — YL28 2.85, YL93 2.37 — may reflect range establishment or fixes early in tracking). Consistent with small, defended roe-deer ranges.

**A sampling caution.** `path_km` tracks `n_fixes` closely, and `n_fixes` often falls sharply in an animal's later years (collar degradation/battery). Declines in `path_km` are therefore largely an artifact — do not read them as reduced activity. Interpret movement metrics per unit sampling effort.

**Site structure.** The ID prefixes (BL, GR, OR, YL, GP) look like separate study sites, and migratory prevalence differs among them (e.g., BL animals almost all resident; OR/YL contain most of the long-distance migrants). Tactic frequency appears landscape-dependent.

---

## 2. Hypotheses

1. **Conditional (state-dependent) partial migration.** The within-individual switching (OR89 settling down, YL112 flip-flopping) suggests the decision responds to annual state — age/experience, body condition, or reproductive outcome. *Prediction:* younger/lighter animals, or those that failed to reproduce, are more likely to migrate; individuals become more resident as they age and secure a good range.

2. **Environmental tracking / resource escape.** Year-to-year plasticity points to deer responding to environmental cues — tracking forage green-up (green-wave surfing) or escaping seasonal food/thermal stress. *Prediction:* migration probability and `days_away` increase in years with poorer local summer forage, higher temperatures, or greater local density.

3. **Landscape-determined benefit + spatial memory.** The high inter-site variation and the year-to-year destination fidelity of committed migrants suggest migration pays off only where a discrete, high-quality summer patch exists within reach; once found, animals return by memory. *Prediction:* migrant destinations coincide with distinct habitat (woodland/agricultural mosaics, cover), and migration distance is set by landscape configuration, not by the individual per se.

---

## 3. Data needed to test these

- **Individual attributes:** age, body mass/condition, reproductive status and fawning success, parity — to test hypothesis 1.
- **Environmental covariates:** remotely sensed vegetation phenology (NDVI/green-up timing), temperature, precipitation, and (where relevant) forage/crop maps for each deer-year — to test hypothesis 2. Local **population density** and hunting/harvest pressure would add competition/disturbance mechanisms.
- **Habitat and land-cover maps** for winter and summer ranges and the intervening corridor, plus human-disturbance layers — to test hypothesis 3.
- **Finer temporal detail:** explicit departure/return dates, so seasonal migration can be cleanly separated from short exploratory **forays** (the big `max_disp` cases) and so timing can be linked to phenology.
- **Natal origin / genetics / age at collaring:** to distinguish one-way natal *dispersal* from repeated seasonal *migration*, and to test relatedness in destination choice.
- **Standardized fix schedules or effort-corrected metrics**, so `path_km` and range indices are comparable across years and collars.

**Bottom line:** These lowland British roe deer are a *partial-migration* system — most individuals are sedentary, but a consistent minority make long, faithful seasonal round-trips, and a notable number switch tactics between years, indicating a flexible, condition-/environment-dependent decision rather than a fixed morph.
