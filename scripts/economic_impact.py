"""
Estimate the economic impact of the visa tightening between the peak and the
following financial year.
"""
import sys
from pathlib import Path

# Allow running from repo root: python scripts/economic_impact.py
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import config
from data_loader import primary_visas


def main():
    df = primary_visas()

    # Total Granted volume across ALL sectors per financial year
    yearly_totals = df.groupby("Financial_Year")["Granted"].sum()

    vol_peak = yearly_totals.get(config.YEAR_PEAK, 0)
    vol_next = yearly_totals.get(config.YEAR_NEXT, 0)

    students_lost = vol_peak - vol_next

    if students_lost <= 0:
        print(f"Unexpected data: Volume did not drop between {config.YEAR_PEAK} "
              f"and {config.YEAR_NEXT}.")
        return

    economic_deficit = students_lost * config.SPEND_PER_STUDENT_AUD
    deficit_billions = economic_deficit / 1_000_000_000

    print("--- ECONOMIC IMPACT OF MIGRATION TIGHTENING ---")
    print(f"Total Granted Visas (Peak {config.YEAR_PEAK}): {vol_peak:,.0f}")
    print(f"Total Granted Visas ({config.YEAR_NEXT}):        {vol_next:,.0f}")
    print(f"Total Primary Students Lost:            {students_lost:,.0f}")
    print(f"\nEstimated Annual Spend per Student:     "
          f"${config.SPEND_PER_STUDENT_AUD:,.0f} AUD")
    print("=" * 55)
    print(f"ESTIMATED ECONOMIC DEFICIT:             ${deficit_billions:.2f} BILLION AUD")
    print("=" * 55)

    print("\n[Analytical Conclusion]")
    print(f"The aggressive tightening of the Australian student visa framework "
          f"resulted in a sharp contraction of {students_lost:,.0f} primary "
          f"international students between {config.YEAR_PEAK} and {config.YEAR_NEXT}.")
    print(f"Assuming a conservative annual expenditure of "
          f"${config.SPEND_PER_STUDENT_AUD:,} AUD per student, this policy shift "
          f"has effectively erased approximately ${deficit_billions:.2f} Billion "
          f"AUD from the Australian economy in just one year, heavily impacting "
          f"the education sector, retail, and real estate markets.")


if __name__ == "__main__":
    main()