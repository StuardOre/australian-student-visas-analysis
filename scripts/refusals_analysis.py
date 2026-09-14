"""
Refusals analysis: granted vs refused/withdrawn stacked bars by sector.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt
import numpy as np

import config
from data_loader import primary_visas


def main():
    df = primary_visas()

    # Refused/Withdrawn = Lodged - Granted (floor at 0 due to processing lag)
    df["Refused_or_Withdrawn"] = df["Lodged"] - df["Granted"]
    df["Refused_or_Withdrawn"] = df["Refused_or_Withdrawn"].apply(
        lambda x: max(x, 0) if pd_notnull(x) else np.nan
    )

    # Focus on the two major sectors, complete years from 2018-19
    sectors = [config.SECTOR_HIGHER_ED, config.SECTOR_VET]
    df = df[df["Sector"].isin(sectors)]
    df = df[df["Financial_Year"] >= "2018-19"]
    df = df[~df["Financial_Year"].astype(str).str.contains(config.PARTIAL_YEAR)]

    # Stacked bar chart (one subplot per sector)
    fig, axes = plt.subplots(1, 2, figsize=(16, 7), sharey=True)

    for idx, sector in enumerate(sectors):
        df_sector = df[df["Sector"] == sector].copy()
        years = df_sector["Financial_Year"]
        granted = df_sector["Granted"]
        refused = df_sector["Refused_or_Withdrawn"]

        ax = axes[idx]
        ax.bar(years, granted, label="Granted", color="#2ca02c", alpha=0.85)
        ax.bar(years, refused, bottom=granted, label="Refused or Withdrawn",
               color="#d62728", alpha=0.85)
        ax.set_title(sector, fontsize=14, fontweight="bold")
        ax.set_xlabel("Financial Year", fontsize=12)
        ax.tick_params(axis="x", rotation=45)
        ax.grid(axis="y", linestyle="--", alpha=0.5)
        ax.legend()

    axes[0].set_ylabel("Volume of Primary Applications", fontsize=13)
    plt.suptitle("Student Visa Outcomes: Granted vs Refused/Withdrawn "
                 "(Since 2018-19)", fontsize=18, fontweight="bold")
    plt.tight_layout()

    config.IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    out_img = config.IMAGES_DIR / "refusals_stacked_bar.png"
    plt.savefig(out_img, dpi=300)
    print(f"[+] Stacked bar chart saved to {out_img}\n")

    # Recent refusals surge (last two complete years)
    print("--- RECENT REFUSALS SURGE ANALYSIS ---")
    for sector in sectors:
        try:
            ref_prev = df[(df["Sector"] == sector)
                          & (df["Financial_Year"] == config.YEAR_REFUSALS_PREV)][
                "Refused_or_Withdrawn"].values[0]
            ref_last = df[(df["Sector"] == sector)
                          & (df["Financial_Year"] == config.YEAR_REFUSALS_LAST)][
                "Refused_or_Withdrawn"].values[0]
            diff = ref_last - ref_prev
            pct_diff = (diff / ref_prev) * 100 if ref_prev > 0 else 0
            print(f"[{sector}]")
            print(f"  -> Total Refused/Withdrawn in {config.YEAR_REFUSALS_PREV}: {ref_prev:,.0f}")
            print(f"  -> Total Refused/Withdrawn in {config.YEAR_REFUSALS_LAST}: {ref_last:,.0f}")
            print(f"  -> ABSOLUTE INCREASE: +{diff:,.0f} applications (+{pct_diff:.1f}%)\n")
        except Exception as e:
            print(f"[{sector}] Error calculating stats: {e}\n")


def pd_notnull(val):
    import pandas as pd
    return val is not None and pd.notnull(val)


if __name__ == "__main__":
    main()