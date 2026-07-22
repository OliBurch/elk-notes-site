# resp_003 — Claude Opus 4.8 — informed (total 9)

> **Scoring note:** True data set which notices three groups and a margin as well as the winter range and weakness in the data. Slight overstep in asserting exploratory movement not bad GPS stamps as data proves. Also cites YL99 which doesn't exist.

## 1. Conclusions

**The dominant signal is partial migration.** The population splits cleanly into behavioral tactics, best seen in `summer_disp_km` (distance of the summer range from the winter range) and `days_away` (time spent off the winter range):

| Tactic | summer_disp_km | days_away | Examples |
|---|---|---|---|
| **Residents** | ~2–6 km | ~0–20 | YL107, OR99, YL120_BL290, YL137_BE13, OR54_BL260 |
| **Medium migrants** | ~9–20 km | ~80–220 | OR89, YL154, YL166, OR81, YL170, YL118_OR8 |
| **Long migrants** | ~28–60 km | ~100–210 | OR78, OR55_OR15, OR56_BL251, YL25, YL29, YL57, GP2 |

Key structural findings:

- **`summer_disp_km` and `days_away` are tightly coupled.** Animals that establish distant summer ranges also stay away for months; residents return (or never leave) within days. These two columns essentially describe one axis: *migratory commitment*.
- **The winter range is shared and consistent.** `winter_spread_km` is remarkably constant (~1.0–1.5 km) across almost all individuals and tactics → the animals aggregate on a common, restricted winter range and diverge only in summer. This is the classic geometry of a migratory ungulate herd wintering on a low-elevation range.
- **Discrete summer destinations, not a continuum.** Long migrants cluster at repeatable distances (~38 km, ~50 km, ~58 km) and individuals return to essentially the *same* distance year after year (OR78: 57–60 km every year; OR55_OR15: ~58–59 km; YL176: ~30–31 km). This points to a few **traditional migratory routes/summer ranges**, not random dispersal.
- **Strong individual repeatability, but real switchers exist.** Most animals keep their tactic across years. A minority are plastic:
  - **OR89**: 18.2 → 7.2 → 6.6 → 5.4 → 3.1 km (progressively *abandoning* migration).
  - **OR60_BL288, YL112_OR38, YL167_OR10, OR65_BL265**: flip between resident-like and migratory years.
- **A population-wide "year" signal in winter_spread.** Across unrelated individuals, `winter_spread_km` is elevated in 2017 (~1.4–1.6) and low in 2016/2019 (~1.1). A synchronous shift across many animals implies a shared environmental driver (e.g., snow/forage conditions), not individual behavior.
- **Occasional long forays by otherwise-resident animals.** Several residents show a large `max_disp_km` spike far exceeding their `summer_disp_km` (OR41: 63.8, YL99: 43.8, YL30: 44.2, OR66: 42.6, OR100: 36.8). These are brief exploratory/excursive movements, not range shifts.
- **Data-quality caveats.** `n_fixes` and `path_km` scale with collar schedule and deployment length, so `path_km` is a fix-rate artifact more than a biological quantity — compare it cautiously. Two winter_spread values are near-zero (GR513: 0.03; YL47 2006: 0.01) and should be flagged (mortality, collar failure, or truncated deployment — note GR513's odd combination of long migration but tiny path).

## 2. Hypotheses

1. **Predation-risk / human-shielding trade-off drives partial migration.** Residents remain year-round near the low-elevation Banff townsite/valley bottom, where wolf predation is suppressed by human presence, trading forage for safety; migrants exploit high-quality, higher-elevation summer forage at the cost of higher predation risk. This would explain the coexistence of stable resident and migrant tactics on one shared winter range.

2. **Migratory tactic is learned/traditional and matrilineal.** The discreteness of summer destinations and their year-to-year fidelity suggest culturally transmitted routes. Switchers (OR89 losing migration; plastic individuals) reflect updating in response to a changing risk/forage landscape rather than genetic determinism.

3. **Environmental conditions modulate range use within and across years.** The synchronous 2017 rise in `winter_spread_km` and the trend toward shorter migrations over time (e.g., OR89) suggest snowpack/green-up phenology and possibly a directional environmental or population change (warming, altered predator numbers, or habituation) are reshaping movement.

## 3. Additional data needed

To test predation/forage trade-offs:
- **Wolf/predator distribution and kill sites**, and distance of each range to the townsite/roads (human-disturbance layer).
- **NDVI / green-up phenology and forage quality** along migratory routes and on summer vs. winter ranges.
- **Snow depth / SWE** by year and elevation (to test the winter_spread year effect and migration timing).
- **Actual coordinates / elevation of summer and winter centroids** (not just distances) to confirm shared winter range and map the discrete summer destinations.

To test learning/tradition and fitness consequences:
- **Individual age, reproductive status (pregnancy/calf survival), and body condition.**
- **Matrilineal/genetic relatedness** among individuals to test cultural inheritance of routes.
- **Survival and cause of mortality** by tactic (to test whether migration carries a predation cost and residency a forage/other cost).

Methodological:
- **Standardized fix schedules** (or explicit modeling of fix rate) so `path_km` and step-based metrics are comparable across years and collars, plus flags for truncated/failed deployments (GR513, YL47).
