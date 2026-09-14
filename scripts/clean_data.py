"""
Build the unified student-visa dataset from the raw government Excel reports.

This is now a thin wrapper around the shared pipeline in data_loader.py.
Run this first to (re)generate data/processed/student_visas_summary.csv.
"""
import warnings

import pandas as pd

# Suppress openpyxl print-area warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

import config
from data_loader import load_visas_summary


def main():
    print("Building unified student visa dataset...")
    df = load_visas_summary()

    print(f"\n[+] Success: Unified dataset saved to {config.PROCESSED_CSV}\n")
    print("--- First 5 Rows ---")
    print(df.head(5).to_string())
    print("\n--- Summary Statistics ---")
    print(df.describe().to_string())


if __name__ == "__main__":
    main()