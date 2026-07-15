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