"""
Market-share analysis: 100% stacked area chart of granted visas by sector.
Professional chart with finding-based title, data source, and annotations.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt

import config
import style
from data_loader import primary_visas, full_years, categorize_sector

SOURCE = ("Source: Department of Home Affairs, Subclass 500 student visa "
          "reports (lock date 2026-07-31)")


def main():
    style.apply_theme()

    df = primary_visas()

    # Market-share window, excluding the partial year
    df = full_years(df, start=config.MARKET_SHARE_START)

    # Categorize sectors into Higher Education / VET / Other
    df["Market_Sector"] = df["Sector"].apply(categorize_sector)

    # Group by year + market sector, summing Granted volume
    df_grouped = df.groupby(["Financial_Year", "Market_Sector"])["Granted"].sum().reset_index()
    pivot = df_grouped.pivot(index="Financial_Year", columns="Market_Sector",
                             values="Granted").fillna(0)

    # Percentages for the 100% stacked area chart
    pivot_pct = pivot.div(pivot.sum(axis=1), axis=0) * 100

    # Plot
    fig, ax = plt.subplots(figsize=(style.FIGWIDTH, style.FIGHEIGHT))
    years = pivot_pct.index
    ax.stackplot(
        years,
        pivot_pct["Higher Education"],
        pivot_pct["VET"],
        pivot_pct["Other Sectors"],
        labels=["Higher Education", "VET", "Other Sectors"],
        colors=[style.PALETTE["higher_ed"], style.PALETTE["vet"], style.PALETTE["other"]],
        alpha=0.85,
    )
    ax.set_title("Market Restructuring: VET Share Nearly Halved (2015-2026)",
                 fontsize=16, fontweight="bold")
    ax.set_xlabel("Financial Year", fontsize=12)
    ax.set_ylabel("Market Share (%)", fontsize=12)
    ax.set_xlim(years[0], years[-1])
    ax.set_ylim(0, 100)
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5), title="Education Sector")
    style.tidy_x_ticks(ax)

    # Annotate the VET share collapse
    vet_start = pivot_pct.loc[config.MARKET_SHARE_START, "VET"]
    vet_end = pivot_pct.loc[years[-1], "VET"]
    style.annotate_point(
        ax, config.MARKET_SHARE_START, vet_start,
        f"VET start: {vet_start:.1f}%",
    )
    style.annotate_point(
        ax, years[-1], vet_end,
        f"VET end: {vet_end:.1f}%",
    )

    config.IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    out_img = config.IMAGES_DIR / "market_share_stacked_area.png"
    style.save_chart(fig, out_img, SOURCE)
    print(f"[+] Market share chart saved to {out_img}\n")

    # Analytical conclusion
    year_start = config.MARKET_SHARE_START
    year_end = years[-1]
    he_start = pivot_pct.loc[year_start, "Higher Education"]
    he_end = pivot_pct.loc[year_end, "Higher Education"]

    print("--- MARKET SHARE ANALYTICAL CONCLUSION ---")
    print(f"VET Market Share in {year_start}: {vet_start:.1f}%")
    print(f"VET Market Share in {year_end}: {vet_end:.1f}%")
    print(f"Higher Ed Market Share in {year_start}: {he_start:.1f}%")
    print(f"Higher Ed Market Share in {year_end}: {he_end:.1f}%")

    print("\n[Conclusion]")
    print("The 100% stacked area chart clearly illustrates a significant "
          "structural shift in the Australian international education market.")
    print(f"The Vocational Education and Training (VET) sector has experienced "
          f"a severe contraction in market dominance, plummeting from a "
          f"{vet_start:.1f}% share in {year_start} to just {vet_end:.1f}% in "
          f"{year_end}.")
    print("This steep decline aligns directly with the government's targeted "
          "policy crackdowns and surging refusal rates in the vocational space.")
    print(f"Conversely, Higher Education has consolidated its position as the "
          f"preferred, lower-risk pathway, growing its market share from "
          f"{he_start:.1f}% to {he_end:.1f}% over the same period, effectively "
          f"absorbing the space left by VET.")


if __name__ == "__main__":
    main()