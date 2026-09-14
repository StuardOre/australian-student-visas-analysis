"""
Sector trend analysis: granted volume and approval rates over time.
Professional charts with finding-based titles, data source, and annotations.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import config
import style
from data_loader import primary_visas, full_years

SOURCE = ("Source: Department of Home Affairs, Subclass 500 student visa "
          "reports (lock date 2026-07-31)")


def main():
    style.apply_theme()

    df = primary_visas()

    sectors_of_interest = [
        config.SECTOR_HIGHER_ED,
        config.SECTOR_VET,
        config.SECTOR_ELICOS,
    ]
    df_major = df[df["Sector"].isin(sectors_of_interest)].copy()
    df_major = full_years(df_major).sort_values("Financial_Year")

    config.IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    # ---- Chart 1: Granted volume by sector ----
    fig, ax = plt.subplots(figsize=(style.FIGWIDTH, style.FIGHEIGHT))
    sns.lineplot(data=df_major, x="Financial_Year", y="Granted",
                 hue="Sector", marker="o", linewidth=2.5, ax=ax)
    ax.set_title("Post-Pandemic Boom: Granted Primary Student Visas by Sector "
                 "(2005-2026)", fontsize=16, fontweight="bold")
    ax.set_xlabel("Financial Year", fontsize=13)
    ax.set_ylabel("Number of Granted Visas", fontsize=13)
    ax.legend(title="Education Sector", loc="upper left")
    style.tidy_x_ticks(ax)

    # Annotate the post-pandemic peak for Higher Education
    he = df_major[df_major["Sector"] == config.SECTOR_HIGHER_ED]
    if not he.empty:
        peak_idx = he["Granted"].idxmax()
        peak_row = he.loc[peak_idx]
        style.annotate_point(
            ax, peak_row["Financial_Year"], peak_row["Granted"],
            f"Peak: {peak_row['Granted']:,.0f}",
        )

    style.save_chart(fig, config.IMAGES_DIR / "visa_grants_by_sector.png", SOURCE)
    print("[+] visa_grants_by_sector.png")

    # ---- Chart 2: Grant rates by sector ----
    fig, ax = plt.subplots(figsize=(style.FIGWIDTH, style.FIGHEIGHT))
    sns.lineplot(data=df_major, x="Financial_Year", y="Grant_Rate",
                 hue="Sector", marker="s", linewidth=2.5, ax=ax)
    ax.set_title("Approval Rate Collapse: Grant Rates by Sector (2005-2026)",
                 fontsize=16, fontweight="bold")
    ax.set_xlabel("Financial Year", fontsize=13)
    ax.set_ylabel("Grant Rate (Approval Ratio)", fontsize=13)
    ax.set_yticklabels(["{:.0f}%".format(x * 100) for x in ax.get_yticks()])
    ax.legend(title="Education Sector", loc="lower left")
    style.tidy_x_ticks(ax)

    # Annotate the VET historic low
    vet = df_major[df_major["Sector"] == config.SECTOR_VET]
    if not vet.empty:
        min_idx = vet["Grant_Rate"].idxmin()
        min_row = vet.loc[min_idx]
        style.annotate_point(
            ax, min_row["Financial_Year"], min_row["Grant_Rate"],
            f"VET low: {min_row['Grant_Rate']:.1%}",
        )

    style.save_chart(fig, config.IMAGES_DIR / "grant_rates_by_sector.png", SOURCE)
    print("[+] grant_rates_by_sector.png")

    # ---- Key statistics (same as before) ----
    print("\n--- KEY MIGRATION POLICY STATISTICS ---\n")

    def get_stat(df, sector, year, column):
        try:
            return df[(df["Sector"] == sector)
                      & (df["Financial_Year"] == year)][column].values[0]
        except IndexError:
            return None

    def pd_notnull(val):
        return val is not None and pd.notnull(val)

    y_pre = "2018-19"
    y_peak = config.YEAR_PEAK
    y_latest = df_major["Financial_Year"].max()

    for sector in [config.SECTOR_HIGHER_ED, config.SECTOR_VET]:
        print(f"[{sector}]")
        v_pre = get_stat(df_major, sector, y_pre, "Granted")
        v_peak = get_stat(df_major, sector, y_peak, "Granted")
        v_latest = get_stat(df_major, sector, y_latest, "Granted")
        r_peak = get_stat(df_major, sector, y_peak, "Grant_Rate")
        r_latest = get_stat(df_major, sector, y_latest, "Grant_Rate")

        if pd_notnull(v_pre) and pd_notnull(v_peak):
            growth_peak = ((v_peak - v_pre) / v_pre) * 100
            print(f"  -> Volume Growth (Pre-Pandemic {y_pre} to Post-Pandemic "
                  f"Peak {y_peak}): {growth_peak:+.1f}% "
                  f"({v_pre:,.0f} to {v_peak:,.0f})")
        if pd_notnull(v_peak) and pd_notnull(v_latest):
            growth_latest = ((v_latest - v_peak) / v_peak) * 100
            print(f"  -> Volume Shift (Peak {y_peak} to Latest {y_latest}): "
                  f"{growth_latest:+.1f}% ({v_peak:,.0f} to {v_latest:,.0f})")
        if pd_notnull(r_peak) and pd_notnull(r_latest):
            rate_drop = (r_latest - r_peak) * 100
            print(f"  -> Approval Rate Shift (Peak {y_peak} to Latest {y_latest}): "
                  f"{rate_drop:+.1f} percentage points "
                  f"({r_peak:.1%} to {r_latest:.1%})\n")

    print("[SUCCESS] Analysis complete. Charts saved to 'images/'.")


if __name__ == "__main__":
    main()