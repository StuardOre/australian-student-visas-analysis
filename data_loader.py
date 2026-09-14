"""
Shared data-loading and cleaning helpers for the visa analysis pipeline.

Centralizes the fragile bits (Excel header detection, pivot reshaping, numeric
cleaning, sector categorization) so every analysis script uses the same logic.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import config


# ---------------------------------------------------------------------------
# Numeric cleaning
# ---------------------------------------------------------------------------
def clean_numeric(val):
    """Clean a raw government cell into a float.

    Handles commas, percent signs, privacy-masked values ('<5'), and dashes.
    """
    if pd.isna(val):
        return np.nan
    val_str = str(val).strip().replace(",", "").replace("%", "")
    if val_str in {"-", "", "<5"}:
        return np.nan  # '<5' masks small numbers for privacy
    try:
        return float(val_str)
    except ValueError:
        return np.nan


# ---------------------------------------------------------------------------
# Excel loading (the fragile part)
# ---------------------------------------------------------------------------
def load_and_melt(file_path, sheet_name, value_name, header_idx=14):
    """Load a government pivot-table Excel sheet into tidy long format.

    Parameters
    ----------
    file_path : str | Path
        Path to the .xlsx report.
    sheet_name : str
        Sheet containing the pivot table.
    value_name : str
        Name for the melted value column.
    header_idx : int
        Row index where the true column headers live (introductory metadata
        rows shift this; see inspect_data.py).
    """
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=header_idx)

    # Rename the first two identifier columns
    cols = list(df.columns)
    cols[0] = "Applicant_Type"
    cols[1] = "Sector"
    df.columns = cols

    # Forward-fill merged cells and strip strings
    df["Applicant_Type"] = df["Applicant_Type"].ffill()
    df["Applicant_Type"] = df["Applicant_Type"].astype(str).str.strip()
    df["Sector"] = df["Sector"].astype(str).str.strip()

    # Drop summary rows
    df = df[~df["Applicant_Type"].str.contains("Total|nan", case=False, na=False)]
    df = df[~df["Sector"].str.contains("Total|nan", case=False, na=False)]

    # Identify financial-year columns
    id_vars = ["Applicant_Type", "Sector"]
    year_cols = [
        c for c in df.columns
        if c not in id_vars
        and "Total" not in str(c)
        and "Unnamed" not in str(c)
        and not pd.isna(c)
    ]

    df_melted = df.melt(
        id_vars=id_vars, value_vars=year_cols,
        var_name="Financial_Year", value_name=value_name,
    )
    df_melted["Financial_Year"] = df_melted["Financial_Year"].astype(str).str.strip()
    df_melted[value_name] = df_melted[value_name].apply(clean_numeric)
    return df_melted


# ---------------------------------------------------------------------------
# Pipeline entry points
# ---------------------------------------------------------------------------
def load_visas_summary() -> pd.DataFrame:
    """Build (or reload) the unified merged dataset."""
    if config.PROCESSED_CSV.exists():
        return pd.read_csv(config.PROCESSED_CSV)

    df_lodged = load_and_melt(
        config.FILE_LODGED, config.SHEET_LODGED, "Lodged",
        header_idx=config.HEADER_IDX_LODGED,
    )
    df_granted = load_and_melt(
        config.FILE_GRANTED, config.SHEET_GRANTED, "Granted",
        header_idx=config.HEADER_IDX_GRANTED,
    )
    df_rate = load_and_melt(
        config.FILE_RATE, config.SHEET_RATE, "Grant_Rate",
        header_idx=config.HEADER_IDX_RATE,
    )

    df = df_lodged.merge(df_granted, on=["Applicant_Type", "Sector", "Financial_Year"], how="outer")
    df = df.merge(df_rate, on=["Applicant_Type", "Sector", "Financial_Year"], how="outer")
    df = df.sort_values(["Applicant_Type", "Sector", "Financial_Year"]).reset_index(drop=True)

    config.DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(config.PROCESSED_CSV, index=False)
    return df


def primary_visas(df: pd.DataFrame | None = None) -> pd.DataFrame:
    """Return only Primary applicants."""
    if df is None:
        df = load_visas_summary()
    return df[df["Applicant_Type"] == config.APPLICANT_TYPE].copy()


def categorize_sector(s: str) -> str:
    """Bucket granular sectors into Higher Education / VET / Other."""
    if "Higher Education" in s:
        return "Higher Education"
    if "Vocational Education" in s:
        return "VET"
    return "Other Sectors"


def full_years(df: pd.DataFrame, start: str | None = None) -> pd.DataFrame:
    """Filter to complete financial years, optionally from a start year."""
    if start is not None:
        df = df[df["Financial_Year"] >= start]
    return df[~df["Financial_Year"].astype(str).str.contains(config.PARTIAL_YEAR)]