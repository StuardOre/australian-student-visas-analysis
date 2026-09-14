"""
Policy timeline analysis: overlays major Australian student-visa policy events
on the granted-volume trend to connect policy shifts with observed outcomes.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt
import pandas as pd

import config
import style
from data_loader import primary_visas, full_years

SOURCE = ("Source: Department of Home Affairs, Subclass 500 student visa "
          "reports (lock date 2026-07-31). Policy events: public announcements.")

# Major policy events affecting Subclass 500 student visas (financial-year view)
POLICY_EVENTS = [
    ("2016-17", "SSVF introduced\n(Simplified Student Visa Framework)", style.PALETTE["higher_ed"]),
    ("2019-20", "COVID-19 border\nclosure (Feb 2020)", style.PALETTE["refused"]),
    ("2021-22", "Borders reopen to\nstudents (Dec 2021)", style.PALETTE["granted"]),
    ("2023-24", "Financial requirement raised\n+ MD 107 prioritization", style.PALETTE["vet"]),
    ("2024-25", "Genuine Student (GS)\nrequirement + fee doubling", style.PALETTE["refused"]),
]


def main():
    style.apply_theme()

    df = primary_visas()

    # Aggregate the two major sectors into a single trend line
    major = df[df["Sector"].isin([config.SECTOR_HIGHER_ED, config.SECTOR_VET])]
    major = full_years(major)
    yearly = major.groupby("Financial_Year")["Granted"].sum()

    fig, ax = plt.subplots(figsize=(15, 8))

    ax.plot(yearly.index, yearly.values, marker="o", linewidth=2.5,
            color=style.PALETTE["higher_ed"], label="Granted (Higher Ed + VET, Primary)")
    ax.fill_between(range(len(yearly)), yearly.values, alpha=0.15,
                    color=style.PALETTE["higher_ed"])

    # Vertical policy event lines
    x_positions = {fy: i for i, fy in enumerate(yearly.index)}
    y_max = yearly.max()
    for fy, label, color in POLICY_EVENTS:
        if fy in x_positions:
            x = x_positions[fy]
            ax.axvline(x=x, color=color, linestyle="--", linewidth=1.5, alpha=0.8)
            ax.text(x, y_max * 1.02, label, rotation=0, fontsize=8.5,
                    ha="center", va="bottom", color=color, fontweight="bold")

    ax.set_title("Policy Meets Data: Student Visa Grants vs Major Policy Events "
                 "(2005-2026)", fontsize=17, fontweight="bold", pad=60)
    ax.set_xlabel("Financial Year", fontsize=13)
    ax.set_ylabel("Number of Granted Visas", fontsize=13)
    ax.set_ylim(0, y_max * 1.25)
    style.tidy_x_ticks(ax)
    ax.legend(loc="upper left")

    # Annotate the peak and the post-crackdown trough
    peak_i = yearly.idxmax()
    ax.annotate(f"Peak: {yearly.max():,.0f}",
                xy=(x_positions[peak_i], yearly.max()),
                xytext=(-60, 10), textcoords="offset points",
                arrowprops=dict(arrowstyle="->", color="#333333", lw=0.8),
                fontsize=11, fontweight="bold")
    last_i = yearly.index[-1]
    ax.annotate(f"Latest: {yearly.iloc[-1]:,.0f}",
                xy=(len(yearly) - 1, yearly.iloc[-1]),
                xytext=(-90, -25), textcoords="offset points",
                arrowprops=dict(arrowstyle="->", color="#333333", lw=0.8),
                fontsize=11, fontweight="bold")

    style.save_chart(fig, config.IMAGES_DIR / "policy_timeline.png", SOURCE)
    print(f"[+] policy_timeline.png saved to {config.IMAGES_DIR}\n")

    # Print the narrative summary
    print("--- POLICY TIMELINE SUMMARY ---")
    for fy, label, _ in POLICY_EVENTS:
        v = yearly.get(fy)
        if v is not None:
            print(f"  {fy}: {label.replace(chr(10), ' ')} -> {v:,.0f} granted")
        else:
            print(f"  {fy}: {label.replace(chr(10), ' ')} -> (outside data range)")

    print("\n[Reading]")
    print("The chart connects each policy inflection with the subsequent volume")
    print("response: the SSVF era (2016+) precedes steady growth; the pandemic")
    print("closure (2020) precedes the collapse; reopening (Dec 2021) precedes")
    print("the record 2022-23 peak; the 2023-24 financial-requirement and MD107")
    print("changes precede the sharp contraction and VET-specific collapse.")
    print("Temporal coincidence is noted; causal attribution requires further")
    print("controls (applicants abroad, provider mix, macro conditions).")


if __name__ == "__main__":
    main()