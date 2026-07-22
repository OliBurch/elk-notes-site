# resp_016 — Claude Opus 4.8 — informed (total 11)

> **Scoring note:** True data set with a very strong response. Recognises its own sampling caveat with path_km due to num_fixes.

## 1. What the data show

**The dominant signal is partial migration — a bimodal split between resident and migratory elk.**

If you sort individuals by `summer_disp_km` (mean summer distance from the winter range) and `days_away`, they don't spread evenly — they clump into two groups with a gap in between:

| Group | summer_disp_km | days_away | Example animals |
|---|---|---|---|
| **Residents** | ~1.5–7 | ~0–20 | OR99, OR54_BL260, YL107, YL120, OR77, OR84 |
| **Migrants** | ~14–60 | ~65–290 | OR78, OR55_OR15, OR56, YL29, YL25, YL168, YL176 |

`summer_disp_km` and `days_away` are tightly, positively correlated: animals that go far stay away long. This is the classic seasonal-migration signature — they leave the winter range for a distant summer range and return.

**A few additional structural findings:**

- **Migrants come in distance classes, not a continuum.** There is a cluster of *short/medium* migrants (~14–20 km) and a separate cluster of *long-distance* migrants (~30–60 km: OR55, OR78, YL25, YL29, YL57, YL93, YL168, YL176). This suggests discrete summer destinations rather than a smooth gradient.

- **Strategy is highly repeatable within individuals.** Animals tracked over multiple years almost always keep the same behavior. OR78 is ~57–60 km every year; OR99 and OR54_BL260 are resident every year. Migratory tactic behaves like an individual trait, not a random annual choice.

- **But some individuals switch/modulate.** YL112_OR38 swings between ~3.5 km and ~24 km across years; OR60_BL288 ranges from ~4 to ~29 km; OR89 declines steadily (18 → 7 → 6 → 5 → 3 km) toward residency. So the trait is repeatable but not perfectly fixed — there is real behavioral plasticity.

- **`max_disp_km` is a poor classifier — beware exploratory forays.** Several clear residents show large single-trip maxima (OR41 = 63.8, OR100 = 36.8, YL30 = 44.2, OR99 = 43.8) despite tiny `summer_disp` and near-zero `days_away`. These are brief excursions, not migrations. Use *seasonal displacement + time away*, not maximum displacement, to define migrants.

- **Migrants tend toward *tighter* winter ranges** (`winter_spread` ~0.5–0.8 for GP2, OR23, OR55, YL123, GR513) — consistent with concentrating on a specific low-elevation valley in winter.

**Important sampling caveat:** `n_fixes` ranges from ~250 to ~17,000, and `path_km` scales strongly with fix count and tracking duration, not just true movement. Short deployments (e.g., 300–500 fixes) systematically under-measure path length. I would **not** interpret `path_km` as tortuosity/activity without standardizing fix rate and duration first.

## 2. Hypotheses

1. **Predation-risk / human-shield trade-off (partial migration).** Residents stay near the Bow Valley / Banff townsite, trading lower forage quality for reduced wolf predation (human presence displaces wolves), while migrants accept higher risk to reach high-quality alpine/backcountry summer forage. This is a well-documented dynamic in this exact system.

2. **Fixed individual strategy set by learning/maternal culture.** High within-individual repeatability suggests migratory tactic is learned from the mother or established early and retained — a "migratory culture" rather than an annual optimization.

3. **Directional shift toward residency over time.** The presence of switchers and declining-migration individuals (OR89, OR60_BL288) may reflect a population-level trend toward residency driven by changing predator numbers, human land use, or forage — a shift reported in Banff elk over recent decades.

## 3. Additional data to test these

- **Spatial coordinates / summer-range polygons** — to confirm discrete destinations and map migrant vs resident ranges (essential; displacement alone hides geography).
- **Predation and cause-specific mortality** (wolf locations, kill sites, survival) — to test the risk trade-off directly.
- **Fitness metrics by tactic**: pregnancy rate, body condition, calf survival — do residents and migrants have equal fitness (the requirement for stable partial migration)?
- **Forage/environment**: NDVI or green-up (forage maturation), snow depth, elevation — to test the forage-quality driver.
- **Distance to roads/townsite/human infrastructure** — to test the human-shield hypothesis.
- **Individual covariates**: age, reproductive status, and **maternal pedigree** — to separate learned vs. condition-dependent strategy.
- **Standardized fix schedules / deployment lengths** — so `path_km` and activity can be compared fairly across animals.
