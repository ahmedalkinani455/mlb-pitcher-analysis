import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm


# ==================================================
# 1. DATA LOADING
# ==================================================

df = pd.read_csv("/Users/ahmedal-kinani/Desktop/mlb-pitcher-analysis/data/stats.csv")

os.makedirs("/Users/ahmedal-kinani/Desktop/mlb-pitcher-analysis/data/processed", exist_ok=True)
os.makedirs("/Users/ahmedal-kinani/Desktop/mlb-pitcher-analysis/visualizations", exist_ok=True)


# ==================================================
# 2. CONTACT QUALITY: CORRELATION ANALYSIS
# ==================================================

print("\n========== CONTACT QUALITY ANALYSIS ==========")

contact_metrics = [
    "woba",
    "hard_hit_percent",
    "barrel_batted_rate"
]

correlation = df[contact_metrics].corr()

print("\nCorrelation matrix:")
print(correlation)

hard_hit_barrel_corr = df["hard_hit_percent"].corr(
    df["barrel_batted_rate"]
)

print(f"\nHard Hit % vs Barrel Rate: {hard_hit_barrel_corr:.3f}")


# ==================================================
# 3. HARD-HIT PERCENTAGE VS WOBA
# ==================================================

print("\n========== HARD HIT % VS WOBA ==========")

x = df["hard_hit_percent"]
y = df["woba"]

m, b = np.polyfit(x, y, 1)

x_line = np.linspace(x.min(), x.max(), 100)
y_line = m * x_line + b

plt.figure(figsize=(8, 5))

plt.scatter(x, y, alpha=0.7)
plt.plot(x_line, y_line)

plt.xlabel("Hard Hit Percentage")
plt.ylabel("wOBA")
plt.title("Hard Hit % vs wOBA (2025)")
plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    "/Users/ahmedal-kinani/Desktop/mlb-pitcher-analysis/visualizations/hard_hit_vs_woba.png",
    dpi=300
)

plt.show()
plt.close()


# ==================================================
# 4. BARREL RATE VS WOBA
# ==================================================

print("\n========== BARREL RATE VS WOBA ==========")

x = df["barrel_batted_rate"]
y = df["woba"]

m, b = np.polyfit(x, y, 1)

x_line = np.linspace(x.min(), x.max(), 100)
y_line = m * x_line + b

plt.figure(figsize=(8, 5))

plt.scatter(x, y, alpha=0.7)
plt.plot(x_line, y_line)

plt.xlabel("Barrel Batted Rate")
plt.ylabel("wOBA")
plt.title("Barrel Rate vs wOBA (2025)")
plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    "/Users/ahmedal-kinani/Desktop/mlb-pitcher-analysis/visualizations/barrel_rate_vs_woba.png",
    dpi=300
)

plt.show()
plt.close()


# ==================================================
# 5. MULTIPLE LINEAR REGRESSION
# ==================================================

print("\n========== MULTIPLE LINEAR REGRESSION ==========")

X = df[["hard_hit_percent", "barrel_batted_rate"]]
y = df["woba"]

X = sm.add_constant(X)

model = sm.OLS(y, X).fit()

print(model.summary())


# ==================================================
# 6. REGRESSION RESIDUAL DIAGNOSTICS
# ==================================================

print("\n========== RESIDUAL ANALYSIS ==========")

predictions = model.predict(X)
residuals = model.resid

plt.figure(figsize=(8, 5))

plt.scatter(predictions, residuals, alpha=0.7)
plt.axhline(y=0, linestyle="--")

plt.xlabel("Predicted wOBA")
plt.ylabel("Residuals")
plt.title("Predicted wOBA vs Residuals")
plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    "/Users/ahmedal-kinani/Desktop/mlb-pitcher-analysis/visualizations/regression_residuals.png",
    dpi=300
)

plt.show()
plt.close()


# ==================================================
# 7. ACTUAL WOBA VS EXPECTED WOBA
# ==================================================

print("\n========== WOBA VS XWOBA ANALYSIS ==========")

df["woba_difference"] = df["woba"] - df["xwoba"]

woba_xwoba_corr = df["woba"].corr(df["xwoba"])

avg_woba = df["woba"].mean()
avg_xwoba = df["xwoba"].mean()
avg_difference = df["woba_difference"].mean()

print(f"Correlation: {woba_xwoba_corr:.3f}")
print(f"Average wOBA: {avg_woba:.3f}")
print(f"Average xwOBA: {avg_xwoba:.3f}")
print(f"Average difference: {avg_difference:.3f}")


# ==================================================
# 8. LARGEST POSITIVE AND NEGATIVE DIFFERENCES
# ==================================================

print("\n========== LARGEST POSITIVE DIFFERENCES ==========")

largest_positive_diff = (
    df[df["woba_difference"] > 0]
    .sort_values(by="woba_difference", ascending=False)
)

print(
    largest_positive_diff[
        [
            "last_name, first_name",
            "pa",
            "woba",
            "xwoba",
            "woba_difference"
        ]
    ].head(5)
)


print("\n========== LARGEST NEGATIVE DIFFERENCES ==========")

largest_negative_diff = (
    df[df["woba_difference"] < 0]
    .sort_values(by="woba_difference", ascending=True)
)

print(
    largest_negative_diff[
        [
            "last_name, first_name",
            "pa",
            "woba",
            "xwoba",
            "woba_difference"
        ]
    ].head(5)
)


# ==================================================
# 9. STRIKEOUT PERCENTAGE VS WOBA
# ==================================================

print("\n========== STRIKEOUT % VS WOBA ==========")

strikeout_woba_corr = df["k_percent"].corr(df["woba"])

print(f"Correlation: {strikeout_woba_corr:.3f}")


# ==================================================
# 10. EXPORT PROCESSED DATA
# ==================================================

df.to_csv(
    "/Users/ahmedal-kinani/Desktop/mlb-pitcher-analysis/data/processed/cleaned_stats.csv",
    index=False
)

print("\nAnalysis completed.")
print("Processed dataset exported.")
print("Visualizations saved.")
