"""
Unit tests for the shared data pipeline (data_loader.py).

Run with: python -m pytest tests/ -v
"""
import pandas as pd

import config
from data_loader import clean_numeric, categorize_sector


def test_clean_numeric_basic():
    assert clean_numeric("1,234") == 1234.0
    assert clean_numeric("12.5%") == 12.5
    assert clean_numeric("42") == 42.0


def test_clean_numeric_privacy_mask():
    # '<5', '-' and '' are all masked/empty values -> NaN
    assert pd.isna(clean_numeric("<5"))
    assert pd.isna(clean_numeric("-"))
    assert pd.isna(clean_numeric(""))


def test_clean_numeric_nan_and_invalid():
    assert pd.isna(clean_numeric(float("nan")))
    assert pd.isna(clean_numeric("not-a-number"))


def test_categorize_sector_higher_ed():
    assert categorize_sector("Higher Education Sector") == "Higher Education"
    assert categorize_sector("Higher Education (Other)") == "Higher Education"


def test_categorize_sector_vet():
    assert categorize_sector("Vocational Education and Training Sector") == "VET"


def test_categorize_sector_other():
    assert categorize_sector("Independent ELICOS Sector") == "Other Sectors"
    assert categorize_sector("Unknown Sector") == "Other Sectors"


def test_config_has_expected_years():
    assert config.YEAR_PEAK == "2022-23"
    assert config.YEAR_NEXT == "2023-24"
    assert config.SPEND_PER_STUDENT_AUD == 40000


def test_config_paths_created():
    assert config.PROCESSED_CSV.name == "student_visas_summary.csv"
    assert "data" in str(config.DATA_RAW_DIR)