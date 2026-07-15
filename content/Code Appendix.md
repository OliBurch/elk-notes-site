```python
"""
Anchors each elk to its winter range: the median position it occupies
in Dec-Mar. Then it asks how far away the elk was in mid-summer (Jul-Aug).

That is the definition of migration - summer somewhere else, winter
back home - so it is the best possible single measurement. If the herd
splits, it splits on `summer_disp_km`.

Biological year runs 1 June (year Y) to 31 May (year Y+1), so the Dec-Mar winter
that falls inside it is the winter the elk RETURNS to after its summer.

An animal-year is only kept if it has fixes in BOTH windows - otherwise there
is no anchor and no summer to measure.

FEATURES
  summer_disp_km   median distance from its winter range during Jul-Aug   <-- the key one
  max_disp_km      furthest it ever got from its winter range
  winter_spread_km how tightly it holds the winter range (sanity check)
  days_away        days spent >10 km from the winter range
  path_km          total distance walked

RUN
    python build_features_v2.py Ya Ha Tinda elk project Banff National Park 2001-2020 (females).csv
"""

import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

COL_ID = "individual-local-identifier"
COL_TIME = "timestamp"
COL_LAT = "location-lat"
COL_LON = "location-long"

WINTER_MONTHS = [12, 1, 2, 3]     # the anchor
SUMMER_MONTHS = [7, 8]            # peak summer range occupancy
MIN_WINTER_FIX = 30
MIN_SUMMER_FIX = 30
AWAY_KM = 10.0

R = 6371000.0
LAT0 = 51.7                        # study area centre; fixed so all elk share one grid


def to_km(lat, lon):
    x = np.radians(lon) * R * np.cos(np.radians(LAT0)) / 1000.0
    y = np.radians(lat) * R / 1000.0
    return x, y


def bio_year(ts):
    return np.where(ts.dt.month >= 6, ts.dt.year, ts.dt.year - 1)


def features(g):
    x, y = to_km(g["lat"].values, g["lon"].values)
    m = g["time"].dt.month.values

    win = np.isin(m, WINTER_MONTHS)
    sm = np.isin(m, SUMMER_MONTHS)
    if win.sum() < MIN_WINTER_FIX or sm.sum() < MIN_SUMMER_FIX:
        return None

    # the anchor: this elk's own winter range
    wx, wy = np.median(x[win]), np.median(y[win])
    disp = np.sqrt((x - wx) ** 2 + (y - wy) ** 2)

    steps = np.sqrt(np.diff(x) ** 2 + np.diff(y) ** 2)
    days = (g["time"].iloc[-1] - g["time"].iloc[0]).total_seconds() / 86400.0

    return pd.Series({
        "n_fixes": len(g),
        "summer_disp_km": round(float(np.median(disp[sm])), 2),
        "max_disp_km": round(float(disp.max()), 2),
        "winter_spread_km": round(float(np.median(disp[win])), 2),
        "days_away": round(float((disp > AWAY_KM).mean() * days), 1),
        "path_km": round(float(steps.sum()), 1),
        "_disp": disp,
        "_doy": (g["time"] - g["time"].iloc[0]).dt.total_seconds().values / 86400.0,
    })


def main():
    print(">>> RUNNING:", __file__)
    raw = pd.read_csv(sys.argv[1], low_memory=False,
                      usecols=[COL_ID, COL_TIME, COL_LAT, COL_LON])
    df = pd.DataFrame({
        "id": raw[COL_ID].astype(str),
        "time": pd.to_datetime(raw[COL_TIME]),
        "lat": pd.to_numeric(raw[COL_LAT], errors="coerce"),
        "lon": pd.to_numeric(raw[COL_LON], errors="coerce"),
    }).dropna().sort_values(["id", "time"])
    df["year"] = bio_year(df["time"])
    print(f"loaded {len(df):,} fixes")

    rows = []
    for (i, yr), g in df.groupby(["id", "year"]):
        f = features(g)
        if f is not None:
            f["id"], f["year"] = i, yr
            rows.append(f)
    out = pd.DataFrame(rows)
    print(f"{out['id'].nunique()} elk, {len(out)} animal-years with both a winter "
          f"anchor and a summer window")

    fig, ax = plt.subplots(1, 3, figsize=(17, 4.6))
    for _, r in out.iterrows():
        ax[0].plot(r["_doy"], r["_disp"], lw=0.5, alpha=0.3, color="steelblue")
    ax[0].set(xlabel="days since 1 June", ylabel="distance from winter range (km)",
              title="every animal-year, anchored on winter range")

    ax[1].hist(out["summer_disp_km"], bins=np.arange(0, 80, 2.5),
               color="firebrick", alpha=0.8)
    ax[1].set(xlabel="summer distance from winter range (km)", ylabel="animal-years",
              title="THE KEY PLOT: one clump or several?")

    ax[2].scatter(out["summer_disp_km"], out["max_disp_km"], s=20, alpha=0.7,
                  color="darkgreen", edgecolor="none")
    ax[2].set(xlabel="summer distance (km)", ylabel="max distance (km)",
              title="summer vs max")
    fig.tight_layout()
    fig.savefig("nsd_plots_v2.png", dpi=140)

    tab = out.drop(columns=["_disp", "_doy"])
    tab = tab[["id", "year", "n_fixes", "summer_disp_km", "max_disp_km",
               "winter_spread_km", "days_away", "path_km"]]
    tab.to_csv("elk_year_features_v2.csv", index=False)

    def bin_width_check(out):
        """Robustness check on the histogram bin width.

        The gap at ~10-12 km is the evidence for discrete strategies rather than a
        continuum, so it must not be an artefact of the binning. Re-plot the same
        data at 1 km and 5 km. If the gap survives both, it is structure. If it only
        appears at 2.5 km, it is not.
        """
        d = out["summer_disp_km"].values

        fig, ax = plt.subplots(1, 2, figsize=(12, 4.2), sharey=False)

        for a, w in zip(ax, [1.0, 5.0]):
            a.hist(d, bins=np.arange(0, d.max() + w, w),
                color="firebrick", alpha=0.8)
            a.axvspan(10, 12.5, color="grey", alpha=0.25, zorder=0)   # the claimed gap
            a.set(xlabel="summer distance from winter range (km)",
                ylabel="animal-years",
                title=f"bin width = {w:g} km")

        fig.suptitle("Bin-width robustness check (shaded band = the claimed gap)")
        fig.tight_layout()
        fig.savefig("bin_width_check.png", dpi=140)

        # counts falling inside the gap, at each binning
        n_gap = ((d >= 10) & (d < 12.5)).sum()
        print(f"animal-years in the 10-12.5 km band: {n_gap} of {len(d)}")

    ids = {v: f"unit_{i:03d}" for i, v in enumerate(sorted(tab["id"].unique()))}
    b = tab.copy()
    b["id"] = b["id"].map(ids)
    b["year"] = b["year"] - b["year"].min() + 1
    b.rename(columns={"id": "unit", "year": "period"}).to_csv(
        "blinded_features_v2.csv", index=False)
    bin_width_check(out)
    print("wrote elk_year_features_v2.csv, blinded_features_v2.csv, nsd_plots_v2.png")


if __name__ == "__main__" and len(sys.argv) > 1:
    main()
```