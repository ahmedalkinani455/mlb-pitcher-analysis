
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# ==================================================
# 1. DATA LOADING
# ==================================================

df = pd.read_csv("/Users/ahmedal-kinani/Desktop/mlb-pitcher-analysis/data/stats.csv")

os.makedirs("/Users/ahmedal-kinani/Desktop/mlb-pitcher-analysis/data/processed", exist_ok=True)
os.makedirs("/Users/ahmedal-kinani/Desktop/mlb-pitcher-analysis/visualizations", exist_ok=True)


# ==================================================
# 2. INITIAL DATA EXPLORATION
# ==================================================

print("\n========== DATASET OVERVIEW ==========")

print("\nFirst five rows:")
print(df.head())

print("\nDataset information:")
df.info()

print("\nColumn names:")
print(df.columns.tolist())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDescriptive statistics:")
print(df.describe())

descriptive_df = df.describe().reset_index()

descriptive_df.to_csv(
    "data/processed/descriptive_stats.csv",
    index=False
)


# ==================================================
# 3. BASIC PITCHER STATISTICS
# ==================================================

print("\n========== BASIC PITCHER STATISTICS ==========")

total_pitchers = df["player_id"].nunique()

avg_strikeout = df["k_percent"].mean()
avg_walk = df["bb_percent"].mean()

highest_strikeout = df.loc[
    df["k_percent"].idxmax(),
    ["last_name, first_name", "k_percent"]
]

highest_whiff = df.loc[
    df["whiff_percent"].idxmax(),
    ["last_name, first_name", "whiff_percent"]
]

lowest_whiff = df.loc[
    df["whiff_percent"].idxmin(),
    ["last_name, first_name", "whiff_percent"]
]

print(f"Total pitchers: {total_pitchers}")
print(f"Average strikeout percentage: {avg_strikeout:.2f}%")
print(f"Average walk percentage: {avg_walk:.2f}%")

print("\nHighest strikeout percentage:")
print(highest_strikeout)

print("\nHighest whiff percentage:")
print(highest_whiff)

print("\nLowest whiff percentage:")
print(lowest_whiff)


# ==================================================
# 4. TOP FIVE PITCHERS BY STRIKEOUT PERCENTAGE
# ==================================================

print("\n========== TOP FIVE STRIKEOUT PITCHERS ==========")

top_strikeout_pitchers = (
    df.sort_values(by="k_percent", ascending=False)
    [["last_name, first_name", "k_percent", "bb_percent"]]
    .head(5)
)

print(top_strikeout_pitchers)


# ==================================================
# 5. ABOVE-AVERAGE STRIKEOUT PITCHERS
# ==================================================

print("\n========== ABOVE-AVERAGE STRIKEOUT PITCHERS ==========")

above_avg_pitchers = df.loc[
    df["k_percent"] > avg_strikeout,
    ["last_name, first_name", "k_percent"]
].sort_values(by="k_percent", ascending=False)

print(above_avg_pitchers)


# ==================================================
# 6. STRIKEOUT AND WALK COMPARISON
# ==================================================

print("\n========== STRIKEOUT AND WALK COMPARISON ==========")

strikeout_walk_comparison = (
    df[["last_name, first_name", "k_percent", "bb_percent"]]
    .sort_values(by="k_percent", ascending=False)
)

print(strikeout_walk_comparison)


# ==================================================
# 7. CORRELATION ANALYSIS
# ==================================================

print("\n========== CORRELATION ANALYSIS ==========")

strikeout_whiff_corr = df["k_percent"].corr(
    df["whiff_percent"]
)

strikeout_walk_corr = df["k_percent"].corr(
    df["bb_percent"]
)

print(f"Strikeout % vs Whiff %: {strikeout_whiff_corr:.3f}")
print(f"Strikeout % vs Walk %: {strikeout_walk_corr:.3f}")


# ==================================================
# 8. WHIFF PERCENTAGE VARIATION
# ==================================================

print("\n========== WHIFF PERCENTAGE ANALYSIS ==========")

avg_whiff = df["whiff_percent"].mean()
std_whiff = df["whiff_percent"].std()

print(f"Average whiff percentage: {avg_whiff:.2f}%")
print(f"Standard deviation: {std_whiff:.2f}")

high_whiff_pitchers = df.loc[
    df["whiff_percent"] > avg_whiff + std_whiff,
    ["last_name, first_name", "whiff_percent"]
].sort_values(by="whiff_percent", ascending=False)

print("\nPitchers more than one standard deviation above the mean:")
print(high_whiff_pitchers)


# ==================================================
# 9. STRIKEOUT PERCENTAGE VS WHIFF PERCENTAGE
# ==================================================

print("\n========== CREATING VISUALIZATION ==========")

x = df["k_percent"]
y = df["whiff_percent"]

plt.figure(figsize=(8, 5))

plt.scatter(x, y, alpha=0.7)

m, b = np.polyfit(x, y, 1)

x_line = np.linspace(x.min(), x.max(), 100)
y_line = m * x_line + b

plt.plot(x_line, y_line)

plt.title("Strikeout Percentage vs Whiff Percentage (2025)")
plt.xlabel("Strikeout Percentage")
plt.ylabel("Whiff Percentage")
plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    "/Users/ahmedal-kinani/Desktop/mlb-pitcher-analysis/visualizations/strikeout_vs_whiff.png",
    dpi=300
)

plt.show()
plt.close()

print("\nExploration completed.")
