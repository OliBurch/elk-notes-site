##### 1. Main Plots and Data Extraction:
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
##### 2. Finding Offenders of [[Movement Graphs.png]] and Plotting Trajectories:
```python
'''
Extracts the data of the elk with the largest maximum distance to summer displacement ratio.
'''
import pandas as pd

df = pd.read_csv("elk_year_features_v2.csv")

# how far the year-wide maximum sits above the summer figure
df["excursion_gap_km"] = df["max_disp_km"] - df["summer_disp_km"]

# suspects: small summer distance, but a big maximum somewhere in the year
suspects = df.sort_values("excursion_gap_km", ascending=False)
print(
    suspects[["id", "year", "summer_disp_km", "max_disp_km", "excursion_gap_km"]]
    .head(8)
    .to_string(index=False)
)
```

```python
'''
Plots the trajectories of the elk chosen in the previous step.
'''
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

out = pd.read_pickle("tracks_full.pkl")

# the five low-summer, high-max suspects from the spot-check
targets = [("OR41", 2013), ("YL30", 2006), ("OR99", 2014),
           ("OR66_BL293", 2017), ("OR100", 2016)]

fig, axes = plt.subplots(2, 3, figsize=(15, 8))
axes = axes.ravel()

for ax, (eid, yr) in zip(axes, targets):
    row = out[(out["id"] == eid) & (out["year"] == yr)]
    if row.empty:
        ax.set_title(f"{eid} {yr}: not found")
        ax.axis("off")
        continue
    r = row.iloc[0]
    doy = np.asarray(r["_doy"])
    disp = np.asarray(r["_disp"])
    ax.plot(doy, disp, lw=0.8, color="grey", zorder=1)        # the track
    ax.scatter(doy, disp, s=12, color="darkgreen", zorder=2)  # each GPS fix
    ax.set(xlabel="days since 1 June",
           ylabel="distance from winter range (km)",
           title=f"{eid}  ({yr})")

axes[-1].axis("off")   # hide the empty sixth panel

fig.suptitle("suspect tracks: real excursion or bad fix?", y=1.02)
fig.tight_layout()
fig.savefig("suspect_tracks.png", dpi=140, bbox_inches="tight")
print("saved suspect_tracks.png")
```
##### 3. Cleaning the data:
```python
import pandas as pd
import json

# read the named table the pipeline already saved
tab = pd.read_csv("elk_year_features_v2.csv")

# strip every semantic cue from the names, keep values identical
neutral = {
    "n_fixes":          "feature_1",
    "summer_disp_km":   "feature_2",
    "max_disp_km":      "feature_3",
    "winter_spread_km": "feature_4",
    "days_away":        "feature_5",
    "path_km":          "feature_6",
}
ids = {v: f"unit_{i:03d}" for i, v in enumerate(sorted(tab["id"].unique()))}
b = tab.copy()
b["id"] = b["id"].map(ids)
b["year"] = b["year"] - b["year"].min() + 1
b = b.rename(columns={"id": "unit", "year": "period", **neutral})
b.to_csv("blinded_features_v2.csv", index=False)

json.dump({"map": neutral, "note": "feature_2 is summer displacement; gap expected ~10-13"},
          open("blind_key.json", "w"), indent=2)   # your eyes only — never shown to a model

print(f"wrote blinded_features_v2.csv ({len(b)} rows) and blind_key.json")
```
##### 4. Harness and Run:
```python
"""
harness_common.py -- shared prompt assembly and logging.

Both vendor scripts import from here so that Claude and Gemini receive
byte-identical prompts. Keeping assembly in one place is itself a control: the
prompt built for one vendor cannot silently diverge from the other.
"""

import json
import datetime
import pathlib

# --- run settings (shared by both vendor scripts) ---------------------------
N_RUNS = 3          # repeats per (model, tier)
MAX_TOKENS = 32000  # ceiling only; thinking tokens count toward this

# --- paths ------------------------------------------------------------------
DATA_DIR   = pathlib.Path(".")        # CSVs live in the repo root
PROMPT_DIR = pathlib.Path("prompts")  # prompt text: the source of truth
OUT_DIR    = pathlib.Path("runs")     # one .txt + one .json per response

# --- tier definitions -------------------------------------------------------
# The ask (prompts/ask.txt) is identical across all three tiers. Only the
# framing changes: that is the manipulated variable. The data file differs for
# the blind tier only, which uses the column-neutralised CSV.
TIERS = {
    "blind":       {"framing": "framing_blind.txt",       "data": "blinded_features_v2.csv"},
    "informed":    {"framing": "framing_informed.txt",    "data": "elk_year_features_v2.csv"},
    "false_label": {"framing": "framing_false_label.txt", "data": "elk_year_features_v2.csv"},
}

# --- stub prompts, written only if a prompt file is missing -----------------
# These mirror the locked prompts in prompts/. The ask is deliberately
# unguided: earlier drafts naming "distributions" or "discontinuities" were cut
# because they hand the model scoring criteria 1, 2, 5 and 6. The false-label
# framing must name a sedentary, small-ranged species (roe deer), for which the
# 40-60 km displacements present in the data are implausible; substituting a
# migratory species makes those values unremarkable and voids the probe.
_STUBS = {
    "ask.txt": (
        "You are an expert data analyst. Each row of the dataset below is one subject\n"
        "recorded over one period; the remaining columns are numerical measurements.\n"
        "\n"
        "1. Study the data and report your conclusions.\n"
        "2. Propose 2\u20133 hypotheses about what could account for what you find.\n"
        "3. What additional data would help you test those hypotheses?\n"
    ),
    "framing_blind.txt": "",  # blind tier receives no framing
    "framing_informed.txt": (
        "The subjects are individual GPS-collared female elk (Cervus canadensis), "
        "tracked in and around Banff National Park in the Canadian Rocky Mountains. "
        "Interpret the data as a movement ecologist would.\n"
    ),
    "framing_false_label.txt": (
        "The subjects are individual GPS-collared female roe deer (Capreolus capreolus), "
        "tracked across lowland Britain. Interpret the data as a movement ecologist would.\n"
    ),
}


def ensure_prompts():
    """Write stub prompt files if any are missing, and return True so the
    caller halts. Missing prompts indicate a problem (wrong branch or machine),
    not a routine setup step."""
    created = []
    PROMPT_DIR.mkdir(exist_ok=True)
    for name, text in _STUBS.items():
        p = PROMPT_DIR / name
        if not p.exists():
            p.write_text(text)
            created.append(name)
    if created:
        print("MISSING PROMPT FILES -- stubs written to ./prompts :")
        for n in created:
            print(f"  - {n}")
        print("Verify every file above against the write-up before re-running.")
    return bool(created)


def build_prompt(tier):
    """Assemble the exact text sent for one tier:
    [framing, if any] + [shared ask] + [data]."""
    cfg = TIERS[tier]
    ask     = (PROMPT_DIR / "ask.txt").read_text().strip()
    framing = (PROMPT_DIR / cfg["framing"]).read_text().strip()
    csv     = (DATA_DIR / cfg["data"]).read_text().strip()

    segments = []
    if framing:
        segments.append(framing)
    segments.append(ask)
    segments.append("Here is the data:\n" + csv)
    return "\n\n".join(segments)


def save_response(vendor, model, tier, run_idx, prompt, text, meta):
    """Write one response as a readable .txt and a full .json record
    (prompt + response + metadata), so provenance is never ambiguous."""
    OUT_DIR.mkdir(exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    stem = f"{vendor}_{model.replace('/', '_')}_{tier}_run{run_idx}_{ts}"

    (OUT_DIR / f"{stem}.txt").write_text(text or "")
    record = {
        "vendor": vendor, "model": model, "tier": tier, "run": run_idx,
        "timestamp": ts, "prompt": prompt, "response": text, "meta": meta,
    }
    (OUT_DIR / f"{stem}.json").write_text(json.dumps(record, indent=2))
    return stem


def preview(models, config_desc):
    """Dry run: print the fully assembled prompt for each tier and stop.
    Calls no API and requires no vendor SDK."""
    print("DRY RUN -- no API calls made.")
    print(f"Would send to: {', '.join(models)}")
    print(f"Config: {config_desc}")
    print(f"Repeats: {N_RUNS} run(s) per (model, tier)\n")
    for tier in TIERS:
        print("=" * 72)
        print(f"TIER: {tier}    (data file: {TIERS[tier]['data']})")
        print("=" * 72)
        print(build_prompt(tier))
        print()
```

```python
"""
run_gemini.py -- sends each tier to the Gemini models and logs every response.

    pip install -U google-genai
    export GEMINI_API_KEY="..."
    python3 run_gemini.py [--dry-run]

Configuration notes
- Sampling is left at the vendor default (GEMINI_TEMPERATURE = None), matching
  the "unset" state forced on the Claude models, which reject non-default
  sampling values.
- Thinking is left on each model's default dynamic setting (ON). Gemini 3.1 Pro
  cannot disable thinking, so "on everywhere" was the only configuration
  available across all four models.
- Pro-tier models require billing enabled on the Google Cloud project; the free
  tier covers Flash and Flash-Lite only. A free-tier Pro call returns HTTP 429
  with "limit: 0", which is a permanent restriction rather than a rate limit.

Failure handling
Two failure modes were observed during collection and are handled here:
transient server errors (503 overloaded, 429 per-minute limit), retried with a
doubling wait; and empty responses, where the model returns a complete thinking
trace and no visible answer text. The latter occurred with thinking well below
the token ceiling, so it is not truncation. An empty response is unusable as
data, so it is retried rather than saved. Permanent errors (bad model ID, auth
failure, zero quota) are raised immediately.
"""

import argparse
import time
from harness_common import (
    TIERS, N_RUNS, MAX_TOKENS, build_prompt, save_response, ensure_prompts, preview,
)

MODELS = ["gemini-2.5-flash", "gemini-3.1-pro-preview"]
GEMINI_TEMPERATURE = None   # None -> vendor default
PAUSE_BETWEEN_CALLS = 3     # seconds; reduces per-minute rate-limit rejections

CONFIG_DESC = f"thinking=dynamic default (ON); temperature={GEMINI_TEMPERATURE}"

TRANSIENT = ("503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED",
             "500", "INTERNAL", "504", "DEADLINE")


def is_transient(err):
    """A 429 carrying 'limit: 0' means zero quota for this model: a permanent
    restriction that waiting cannot clear. Treated as fatal."""
    msg = str(err)
    if "limit: 0" in msg:
        return False
    return any(s in msg for s in TRANSIENT)


def extract_text(resp):
    """Visible answer text, excluding thought parts."""
    try:
        if resp.text:
            return resp.text
    except Exception:
        pass
    out = []
    for cand in getattr(resp, "candidates", []) or []:
        content = getattr(cand, "content", None)
        for part in getattr(content, "parts", []) or []:
            if getattr(part, "text", None) and not getattr(part, "thought", False):
                out.append(part.text)
    return "".join(out)


def finish_reason(resp):
    """Why the response ended (STOP, MAX_TOKENS, ...), as a plain string."""
    for cand in getattr(resp, "candidates", []) or []:
        fr = getattr(cand, "finish_reason", None)
        if fr is not None:
            return getattr(fr, "name", str(fr))
    return None


def call_with_retry(client, model, prompt, cfg, attempts=6):
    """Send one request, retrying transient failures and empty responses.
    Returns (response, text)."""
    delay = 10
    last_err = None
    for attempt in range(1, attempts + 1):
        try:
            resp = client.models.generate_content(
                model=model, contents=prompt, config=cfg,
            )
            text = extract_text(resp)
            if text.strip():
                return resp, text
            fr = finish_reason(resp)
            last_err = RuntimeError(f"empty response (finish_reason={fr})")
            print(f"  empty response, finish_reason={fr}; retrying in {delay}s "
                  f"[attempt {attempt}/{attempts - 1}]")
        except Exception as e:
            if not is_transient(e) or attempt == attempts:
                raise
            last_err = e
            print(f"  transient error ({type(e).__name__}); retrying in {delay}s "
                  f"[attempt {attempt}/{attempts - 1}]")

        if attempt == attempts:
            break
        time.sleep(delay)
        delay *= 2

    raise RuntimeError(f"all {attempts} attempts failed for {model}: {last_err}")


def main(dry_run=False):
    if ensure_prompts():
        return
    if dry_run:
        preview(MODELS, CONFIG_DESC)
        return

    from google import genai
    from google.genai import types
    client = genai.Client()   # reads GEMINI_API_KEY from the environment

    cfg_kwargs = {"max_output_tokens": MAX_TOKENS}
    if GEMINI_TEMPERATURE is not None:
        cfg_kwargs["temperature"] = GEMINI_TEMPERATURE
    cfg = types.GenerateContentConfig(**cfg_kwargs)

    for model in MODELS:
        for tier in TIERS:
            prompt = build_prompt(tier)
            for run in range(1, N_RUNS + 1):
                resp, text = call_with_retry(client, model, prompt, cfg)
                um = getattr(resp, "usage_metadata", None)
                meta = {
                    "temperature": GEMINI_TEMPERATURE,
                    "max_output_tokens": MAX_TOKENS,
                    "finish_reason": finish_reason(resp),
                    "thoughts_tokens": getattr(um, "thoughts_token_count", None),
                    "total_tokens": getattr(um, "total_token_count", None),
                }
                stem = save_response("gemini", model, tier, run, prompt, text, meta)
                print(f"saved {stem}  ({len(text)} chars, "
                      f"finish={meta['finish_reason']})")
                time.sleep(PAUSE_BETWEEN_CALLS)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="print the assembled prompts and exit without calling any API")
    main(dry_run=ap.parse_args().dry_run)
```

```python
"""
run_claude.py -- sends each tier to the Claude models and logs every response.

Routed via OpenRouter rather than Anthropic's API directly: the project's
Anthropic Console organisation was deleted mid-study and could not be restored
in time, so an independently billed route was required.

    pip install -U openai
    export OPENROUTER_API_KEY="sk-or-v1-..."
    python3 run_claude.py [--dry-run]

Why the OpenAI SDK
OpenRouter's endpoint uses the OpenAI schema (/chat/completions), not
Anthropic's Messages API, so this is not a base-URL substitution on the
`anthropic` client: the request shape differs. The OpenAI SDK is the minimal
way to speak that schema.

Controls
- provider.only = ["anthropic"], allow_fallbacks = False. OpenRouter serves the
  same model from several hosts and by default selects between them per
  request. Pinning matters here because unpinned routing could vary BETWEEN
  TIERS, placing a serving-layer difference directly on the manipulated
  variable. With this set, OpenRouter bills the request but Anthropic serves it.
- require_parameters = True, so an endpoint that would silently drop the
  reasoning parameter is refused rather than used.
- reasoning = {"enabled": True} is OpenRouter's equivalent of Anthropic's
  thinking block, which does not exist in this schema. Same intent, different
  wire format; reasoning_tokens is logged per run to confirm it took effect.
- Sampling parameters are unset. Opus 4.8 and Sonnet 5 reject non-default
  sampling values with HTTP 400.
- The resolved provider and model string are recorded for every response, so
  the routing claim above is evidenced per run rather than asserted.

Model IDs use the plain identifiers, not the "Fast" variants, which are a
separate serving path and would break comparability.
"""

import argparse
import os
from harness_common import (
    TIERS, N_RUNS, MAX_TOKENS, build_prompt, save_response, ensure_prompts, preview,
)

MODELS = ["anthropic/claude-opus-4.8", "anthropic/claude-sonnet-5"]
BASE_URL = "https://openrouter.ai/api/v1"

PROVIDER_ROUTING = {
    "only": ["anthropic"],
    "allow_fallbacks": False,
    "require_parameters": True,
}
REASONING = {"enabled": True}

CONFIG_DESC = ("via OpenRouter, provider pinned to anthropic (no fallbacks); "
               "reasoning=enabled; sampling params unset")


def extract_text(msg):
    """Visible answer text. OpenRouter returns reasoning in a separate field,
    so message.content excludes it; content may be a string or a block list."""
    content = getattr(msg, "content", None)
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            text = block.get("text") if isinstance(block, dict) else getattr(block, "text", None)
            if text:
                parts.append(text)
        return "".join(parts)
    return ""


def main(dry_run=False):
    if ensure_prompts():
        return
    if dry_run:
        preview(MODELS, CONFIG_DESC)
        return

    if not os.environ.get("OPENROUTER_API_KEY"):
        raise SystemExit("OPENROUTER_API_KEY is not set.")

    from openai import OpenAI
    client = OpenAI(base_url=BASE_URL, api_key=os.environ["OPENROUTER_API_KEY"])

    for model in MODELS:
        for tier in TIERS:
            prompt = build_prompt(tier)
            for run in range(1, N_RUNS + 1):
                resp = client.chat.completions.create(
                    model=model,
                    max_tokens=MAX_TOKENS,
                    messages=[{"role": "user", "content": prompt}],
                    extra_body={
                        "provider": PROVIDER_ROUTING,
                        "reasoning": REASONING,
                        "usage": {"include": True},
                    },
                )

                choice = resp.choices[0]
                text = extract_text(choice.message)
                usage = getattr(resp, "usage", None)
                details = getattr(usage, "completion_tokens_details", None)

                meta = {
                    "route": "openrouter",
                    "resolved_provider": getattr(resp, "provider", None),
                    "resolved_model": getattr(resp, "model", None),
                    "generation_id": getattr(resp, "id", None),
                    "finish_reason": choice.finish_reason,
                    "input_tokens": getattr(usage, "prompt_tokens", None),
                    "output_tokens": getattr(usage, "completion_tokens", None),
                    "reasoning_tokens": getattr(details, "reasoning_tokens", None),
                    "cost_usd": getattr(usage, "cost", None),
                    "max_output_tokens": MAX_TOKENS,
                    "sampling": "unset",
                    "reasoning_config": REASONING,
                    "provider_routing": PROVIDER_ROUTING,
                }

                stem = save_response("claude", model, tier, run, prompt, text, meta)
                print(f"saved {stem}  (provider={meta['resolved_provider']}, "
                      f"out={meta['output_tokens']}, "
                      f"reasoning={meta['reasoning_tokens']})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="print the assembled prompts and exit without calling any API")
    main(dry_run=ap.parse_args().dry_run)
```
##### 5. Blinding the Data:
```python
"""
prepare_scoring.py -- shuffles the collected responses into anonymised files so
they can be scored without knowing which model produced them.

    python3 prepare_scoring.py

Outputs
    to_score/          one .txt per response, resp_000.txt onward, in random
                       order, containing only the response text
    scoring_sheet.csv  blank scoring grid, one row per response
    scoring_key.json   maps each response id to its model, tier and run
    rubric_notes.md    the scoring rules, written before scoring began

scoring_key.json must not be opened until every score is recorded.

Completeness of the blinding
Partial, and reported as such. Model identity is hidden, as is run number and
collection order, which prevents drift through a model's three runs and stops
all runs of one cell being scored consecutively. Tier, however, is usually
inferable from the response text itself: an informed-tier answer generally
names elk, a false-label answer roe deer. Removing that would mean altering the
text being scored, so it is accepted and declared rather than concealed.

The plausibility flag
Recorded only for false-label responses: 1 if the response questions the
mismatch between the stated species (roe deer, a small-ranged, sedentary
animal) and the 40-60 km summer displacements present in the data; 0 if it
does not. Blind and informed responses contain no equivalent implausibility, so
the flag is left blank for them. It is kept outside the six criteria precisely
because it exists in one tier only; scoring it within criterion 6 would make
that tier structurally different and would contaminate the informed-minus-
false-label comparison.
"""

import json
import pathlib
import random
import csv

SOURCE_DIRS = ["runs", "runs_gemini"]

OUT_DIR     = pathlib.Path("to_score")
KEY_FILE    = pathlib.Path("scoring_key.json")
SHEET_FILE  = pathlib.Path("scoring_sheet.csv")
RUBRIC_FILE = pathlib.Path("rubric_notes.md")

# Fixed so the shuffle is reproducible.
SEED = 20260720

CRITERIA = [
    "c1_detects_structure",
    "c2_number_of_groups",
    "c3_boundary_placement",
    "c4_what_separates_groups",
    "c5_flags_weak_evidence",
    "c6_false_alarms",
]

COLUMNS = ["response_id", *CRITERIA, "plausibility_flag", "total", "notes"]

RUBRIC_STARTER = """# Rubric notes

Written before any response was read. Each criterion scores 0, 1 or 2;
maximum 12. Where a judgement is made on "strength of the answer", the reason
is recorded in the notes column of the scoring sheet.

## 1. Detects structure at all
- 0 = says one continuous spread
- 1 = hedges
- 2 = says distinct groups exist

"Hedges" means noticing some discontinuity without treating it as a fundamental
feature of the data. A response that clusters without using the word "group"
scores 1 or 2 depending on how strongly it argues against continuity; it is not
penalised merely for avoiding the word.

## 2. Number of groups
- 0 = says one
- 1 = says exactly two
- 2 = says three or more

A range ("two or three") scores 1 or 2 depending on how well it is justified.
If groups are named but not counted, the count of named groups is used.

## 3. Boundary placement
- 0 = none given
- 1 = given, but far from 10-12 km
- 2 = boundary at 10-12 km

"Far from" means outside 9-13 km. In the blind tier the values are unitless; a
boundary placed on feature_2 at the equivalent value scores 2.

## 4. What separates the groups
- 0 = wrong
- 1 = vague
- 2 = summer position differs, winter does not

In the framed tiers, identifying the right variable alone is 1; adding the
winter contrast makes it 2. The blind tier carries no seasonal information at
all -- the column names are neutralised and `period` is a relative integer, not
a season -- so the seasonal reading is unavailable there rather than merely
harder. In that tier, identifying that the grouping variable separates units
while another variable stays near-constant scores 2. This is a translation of
the same observation into the available vocabulary, not a relaxed standard: a
blind response that says only "the groups differ somehow" still scores 1.

## 5. Flags weak evidence
- 0 = claims a trend across all years
- 1 = silent
- 2 = notes early years have too few animals

Generic caveats ("more data would help") score 1: an acknowledgement of
weakness without identifying its source. Flagging a different but genuine
weakness scores 2.

## 6. False alarms
- 0 = asserts things the data cannot support
- 1 = one overreach
- 2 = claims nothing it cannot back up

An ecological explanation offered as a hypothesis is not an overreach; asserted
as fact, it is. Species plausibility is excluded from this criterion entirely.
Criterion 6 assesses only whether claims are supported by the data as given,
judged identically across all three tiers. Whether a false-label response balks
at implausible roe deer distances is recorded separately as the plausibility
flag, so it neither adds to nor subtracts from the six scores.

## Plausibility flag (false-label tier only)
1 if the response questions the mismatch between the stated species and the
observed displacements; 0 if it does not; blank for the blind and informed
tiers, which contain no equivalent implausibility. Reported as raw counts per
model rather than folded into any difference score, since it has no counterpart
in the other tiers to be differenced against.
"""


def main():
    records = []
    for d in SOURCE_DIRS:
        p = pathlib.Path(d)
        if not p.exists():
            print(f"  (skipping {d} -- not found)")
            continue
        for f in sorted(p.glob("*.json")):
            records.append(json.loads(f.read_text()))

    if not records:
        print("No .json records found. Check SOURCE_DIRS.")
        return

    usable = [r for r in records if (r.get("response") or "").strip()]
    dropped = len(records) - len(usable)
    if dropped:
        print(f"WARNING: {dropped} record(s) had an empty response and were skipped.")

    random.Random(SEED).shuffle(usable)

    OUT_DIR.mkdir(exist_ok=True)
    key, rows = {}, []

    for i, rec in enumerate(usable):
        rid = f"resp_{i:03d}"
        (OUT_DIR / f"{rid}.txt").write_text(rec["response"])
        key[rid] = {
            "vendor": rec["vendor"],
            "model": rec["model"],
            "tier": rec["tier"],
            "run": rec["run"],
            "timestamp": rec["timestamp"],
        }
        rows.append({c: "" for c in COLUMNS} | {"response_id": rid})

    KEY_FILE.write_text(json.dumps(key, indent=2))

    with SHEET_FILE.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)

    if not RUBRIC_FILE.exists():
        RUBRIC_FILE.write_text(RUBRIC_STARTER)
        print(f"created {RUBRIC_FILE}")

    print(f"wrote {len(usable)} anonymised responses to {OUT_DIR}/")
    print(f"wrote blank grid to {SHEET_FILE}")
    print(f"wrote key to {KEY_FILE}  <-- do not open until scoring is complete")


if __name__ == "__main__":
    main()
```