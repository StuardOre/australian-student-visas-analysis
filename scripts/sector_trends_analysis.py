"""
Sector trend analysis: granted volume and approval rates over time.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt
import seaborn as sns

import config
from data_loader import primary_visas, full_years


def main():
    df = primary_visas()

    sectors_of_interest = [
        config.SECTOR_HIGHER_ED,
        config.SECTOR_VET,
        config.SECTOR_ELICOS,
    ]
    df_major = df[df["Sector"].isin(sectors_of_interest)].copy()
    df_major = full_years(df_major).sort_values("Financial_Year")

    config.IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    # Line plot: granted volume by sector
    plt.figure(figsize=(14, 7))
    sns.lineplot(data=df_major, x="Financial_Year", y="Granted",
                 hue="Sector", marker="o", linewidth=2.5)
    plt.title("Volume of Primary Student Visas Granted Over Time (By Sector)",
              fontsize=16, fontweight="bold")
    plt.xlabel("Financial Year", fontsize=13)
    plt.ylabel("Number of Granted Visas", fontsize=13)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend(title="Education Sector", loc="upper left")
    plt.tight_layout()
    plt.savefig(config.IMAGES_DIR / "visa_grants_by_sector.png", dpi=300)
    plt.close()

    # Line plot: grant rates by sector
    plt.figure(figsize=(14, 7))
    sns.lineplot(data=df_major, x="Financial_Year", y="Grant_Rate",
                 hue="Sector", marker="s", linewidth=2.5)
    plt.title("Primary Student Visa Approval Rates Over Time (By Sector)",
              fontsize=16, fontweight="bold")
    plt.xlabel("Financial Year", fontsize=13)
    plt.ylabel("Grant Rate (Approval Ratio)", fontsize=13)
    plt.gca().set_yticklabels(
        ["{:.0f}%".format(x * 100) for x in plt.gca().get_yticks()])
    plt.xticks(rotation=45)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend(title="Education Sector", loc="lower left")
    plt.tight_layout()
    plt.savefig(config.IMAGES_DIR / "grant_rates_by_sector.png", dpi=300)
    plt.close()

    # Key statistics
    print("--- KEY MIGRATION POLICY STATISTICS ---\n")

    def get_stat(df, sector, year, column):
        try:
            return df[(df["Sector"] == sector)
                      & (df["Financial_Year"] == year)][column].values[0]
        except IndexError:
            return None

    y_pre = "2018-19"
    y_peak = config.YEAR_PEAK
    y_latest = df_major["Financial_Year"].max()

    for sector in [config.SECTOR_HIGHER_ED, config.SECTOR_VET]:
        print(f"[{sector}]")

        v_pre = get_stat(df_major, sector, y_pre, "Granted")
        v_peak = get_stat(df_major, sector, y_peak, "Granted")
        v_latest = get_stat(df_major, sector, y_latest, "Granted")
        r_pre = get_stat(df_major, sector, y_pre, "Grant_Rate")
        r_peak = get_stat(df_major, sector, y_peak, "Grant_Rate")
        r_latest = get_stat(df_major, sector, y_latest, "Grant_Rate")

        if pd_notnull(v_pre) and pd_notnull(v_peak):
            growth_peak = ((v_peak - v_pre) / v_pre) * 100
            print(f"  -> Volume Growth (Pre-Pandemic {y_pre} to Post-Pandemic "
                  f"Peak {y_peak}): {growth_peak:+.1f}% ({v_pre:,.0f} to {v_peak:,.0f})")
        if pd_notnull(v_peak) and pd_notnull(v_latest):
            growth_latest = ((v_latest - v_peak) / v_peak) * 100
            print(f"  -> Volume Shift (Peak {y_peak} to Latest {y_latest}): "
                  f"{growth_latest:+.1f}% ({v_peak:,.0f} to {v_latest:,.0f})")
        if pd_notnull(r_peak) and pd_notnull(r_latest):
            rate_drop = (r_latest - r_peak) * 100
            print(f"  -> Approval Rate Shift (Peak {y_peak} to Latest {y_latest}): "
                  f"{rate_drop:+.1f} percentage points "
                  f"({r_peak:.1%} to {r_latest:.1%})\n")

    print("[SUCCESS] Analysis complete. High-resolution charts saved to the "
          "'images/' folder.")


def pd_notnull(val):
    import pandas as pd
    return val is not None and pd.notnull(val)


if __name__ == "__main__":
    main()