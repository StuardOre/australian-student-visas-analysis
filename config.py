"""
Centralized configuration for the Australian Student Visa analysis pipeline.

All tunable parameters (file paths, financial years of interest, sectors,
economic assumptions) live here so scripts stay in sync and the analysis is
easy to reproduce or update.
"""
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
IMAGES_DIR = PROJECT_ROOT / "images"

# Source Excel files (official Department of Home Affairs reports)
FILE_GRANTED = DATA_RAW_DIR / "bp0015l-student-visas-granted-report-locked-at-2026-07-31-v100.xlsx"
FILE_LODGED = DATA_RAW_DIR / "bp0015l-student-visas-lodged-report-locked-at-2026-07-31-v100.xlsx"
FILE_RATE = DATA_RAW_DIR / "bp0015l-student-visa-grant-rates-locked-at-2026-07-31-v100.xlsx"

# Sheet names (note: 'Lodged (Month) ' has a trailing space in the source file)
SHEET_GRANTED = "Granted (Month)"
SHEET_LODGED = "Lodged (Month) "
SHEET_RATE = "Grant Rate (Month)"

# Header row index for each file. The government reports embed introductory
# metadata rows that shift the true header; these values are detected by
# inspect_data.py and set here once.
HEADER_IDX_LODGED = 13
HEADER_IDX_GRANTED = 14
HEADER_IDX_RATE = 13

# Processed output
PROCESSED_CSV = DATA_PROCESSED_DIR / "student_visas_summary.csv"

# ---------------------------------------------------------------------------
# Analysis parameters
# ---------------------------------------------------------------------------
# Applicant type of interest (Primary visa holders)
APPLICANT_TYPE = "Primary"

# Financial years for the economic-impact comparison
YEAR_PEAK = "2022-23"
YEAR_NEXT = "2023-24"

# Financial years for the refusals-surge comparison (last two COMPLETE years)
YEAR_REFUSALS_PREV = "2024-25"
YEAR_REFUSALS_LAST = "2025-26"

# Market-share analysis window
MARKET_SHARE_START = "2015-16"
# Partial year to exclude from charts (data only runs to 31 July)
PARTIAL_YEAR = "2026-27"

# Sectors of interest
SECTOR_HIGHER_ED = "Higher Education Sector"
SECTOR_VET = "Vocational Education and Training Sector"
SECTOR_ELICOS = "Independent ELICOS Sector"

# Economic assumption: estimated annual spend per student (tuition + living)
SPEND_PER_STUDENT_AUD = 40_000