# resp_025 — Claude Sonnet 5 — informed (total 8)

> **Scoring note:** True data set that correctly groups more than 2 regions but overasserts and proposes labels for specific herd grouping from its own data.

# Elk Movement Data — Interpretation

## 1. Key Patterns in the Data

**A. A strong bimodal (or multimodal) migratory tactic structure**

The population splits clearly into two behavioral clusters, best seen in `summer_disp_km` and `days_away`:

- **Residents**: `summer_disp_km` ≈ 2–6 km, `days_away` ≈ 0, `max_disp_km` typically <15 km (e.g., OR99, YL107, YL120_BL290, YL161–YL164, BL215, BL224). These animals show tight, stable annual home ranges.
- **Long-distance migrants**: `summer_disp_km` 15–60 km, `days_away` often >100–250 days (e.g., OR55_OR15, OR78, OR56_BL251, YL168, YL176, YL93, YL29, YL57, YL25, GR513). These individuals leave a winter core area for months at a time, consistent with classic elk migration to high-elevation/alpine summer ranges.
- A middle group (10–20 km displacement, 30–120 days away) suggests **short-distance or facultative migrants** (e.g., YL154, YL166, OR60_BL288, OR89).

**B. Individual repeatability, with some plasticity across years**

Most animals with multiple years of data repeat their strategy closely (e.g., OR78 is a ~58 km migrant in every year sampled; YL107 is a resident in every year). However, some individuals switch:
- **OR60_BL288** varies from 28.7 km/110 days (2015) to 3.8 km/48 days (2018) to 15.5 km/92 days (2019) — a clear case of **partial/facultative migration**, where the same individual behaves as resident in some years and migrant in others.
- **OR89** trends from migratory (18.2 km, 121 days in 2015) toward resident (3.1 km, 0 days in 2019) — possibly an age- or condition-related behavioral shift.

**C. Winter range fidelity is nearly universal**

`winter_spread_km` stays low (~1–2 km) for almost every animal regardless of summer strategy or displacement distance — even extreme migrants (e.g., OR78: winter_spread ~1.1 km) return to a tightly clustered winter range. This indicates winter aggregation/site fidelity is a fixed trait, decoupled from summer ranging tactic — classic elk ecology (snow-limited winter ranges constrain the population into common areas regardless of where individuals summer).

**D. Path length (`path_km`) is not simply proportional to displacement**

Residents often accumulate very large `path_km` (1300–1800 km/year) despite tiny net displacement — reflecting tortuous, intensive space use within a small home range rather than net directional movement. Migrants don't necessarily have higher path lengths; some (e.g., GR513: 692 km path but 23.7 km displacement) show relatively direct, efficient movement.

**E. A likely sampling/fix-rate artifact**

`n_fixes` varies enormously (250–17,000+) across records, apparently reflecting different collar duty-cycle programming (many individuals show n_fixes crashing to 300–800 in 2018–2019, presumably reduced fix schedules or battery depletion). Lower n_fixes rows systematically show lower `path_km`, an expected artifact since path length is fix-interval dependent — this is a **methodological confound**, not necessarily biological difference in movement rate, and should be corrected for before comparing path lengths across years/individuals.

## 2. Hypotheses

1. **Partial migration driven by individual state/condition** — differences (and within-individual year-to-year switching) in migratory tendency may reflect age, reproductive status (calf presence), body condition, or memory/learning, consistent with well-documented partial migration in elk populations.

2. **Environmental heterogeneity and predation risk shape strategy** — migrants may be avoiding wolf predation risk concentrated in low-elevation valley bottoms (a known driver in this exact system — Banff/Bow Valley elk), or tracking a "green wave" of higher-quality forage at high elevation in summer, while residents exploit human-associated refugia (e.g., townsite, low predation zones) at a fitness cost of lower forage quality.

3. **Distinct sub-herds with traditional migratory routes** — naming patterns (YL, OR, BL, GR prefixes) suggest multiple study cohorts/herds (e.g., Ya Ha Tinda vs. Bow Valley elk), and the extreme long-distance migrants may represent a genetically/behaviorally distinct traditional migratory segment rather than a randomly distributed tactic across the whole population.

4. (Methodological) **Fix-schedule changes across the study confound path-based metrics** — apparent inter-annual "changes" in movement intensity may partly reflect changing GPS collar programming rather than true behavioral change.

## 3. Additional Data to Test These Hypotheses

- **Individual covariates**: age, reproductive status/calf survival, body condition scores — to test the state-dependent migration hypothesis.
- **Predation risk layers**: wolf pack territory maps, kill-site density, human/road density — to test predation-avoidance vs. forage hypotheses.
- **Vegetation/phenology data**: NDVI green-wave surfaces, snow depth/SWE — to test forage-tracking and snow-driven winter range constriction.
- **Herd/genetic origin metadata**: capture location, natal herd assignment, matrilineal group — to test whether migratory tactic is herd-specific/traditional.
- **Standardized fix schedule metadata**: actual fix interval/duty cycle per collar-year, to correct `path_km` (e.g., via time-normalized step-length or net-squared-displacement models) rather than relying on raw path length.
- **Land ownership/human disturbance layers** (e.g., townsite proximity, trail/road density) to test refugia-use by residents.
- **Multi-year survival/fecundity data** to link migratory tactic to fitness outcomes.
