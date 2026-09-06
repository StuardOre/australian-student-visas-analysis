# Australian Student Visa Trends: Policy Shift Analysis (Subclass 500)

## 1. Executive Summary & Context
In recent years, Australian media and political discourse have heavily focused on the influx of international students and the perceived tightening of migration policies. This project analyzes official Department of Home Affairs data across +20 years (2005 to 2026) to empirically evaluate these claims regarding student visa crackdowns.

By processing static Excel pivot tables published by the government, this project aims to uncover the true volume and approval rate trends of Subclass 500 Primary Student Visas across major education sectors.

## 2. Key Findings & Data Insights

### The Post-Pandemic Boom (2018-19 to 2022-23)
Following the reopening of international borders, Australia experienced an unprecedented surge in student visa grants:
- **Higher Education Sector:** Experienced a robust volume growth of **+37.9%** (from 189,477 to a peak of 261,317).
- **Vocational Education and Training (VET) Sector:** Surged even faster at **+49.0%** (from 86,121 to 128,334).

### Targeted Policy Tightening
The data confirms a massive recent policy shift resulting in a severe crackdown on approval rates. However, this crackdown is highly targeted:
- **Higher Education** approval rates dropped by **-16.7 percentage points** (down to 70.8%).
- **VET Sector** suffered a dramatic decline, plummeting by **-28.6 percentage points** (down to a historic low of **48.4%**). This clearly indicates that the government's recent visa tightening is disproportionately focused on the vocational education sector.

## 3. Visualizations

### Visa Grants by Sector
![Visa Grants by Sector](images/visa_grants_by_sector.png)

### Grant Rates by Sector
![Grant Rates by Sector](images/grant_rates_by_sector.png)

## 4. Socio-Economic Impact & Market Shift

### Massive Surge in Refusals
The tightening of migration policies led to a massive increase in rejected applications. In the 2025-26 financial year alone, the combined number of refused or withdrawn applications across the two major sectors neared **60,000**, with the VET sector experiencing a **+54.8%** surge in refusals compared to the previous year.
![Refusals](images/refusals_stacked_bar.png)

### Market Restructuring (Flight to Quality)
The targeted policy crackdowns have caused a severe structural shift in the Australian international education market. The **Vocational Education and Training (VET)** sector has lost nearly half its market share, plummeting from 21.7% to just **13.1%**. Meanwhile, the **Higher Education** sector has aggressively absorbed this space, now dominating the landscape with a **67.1%** market share, cementing itself as the preferred, lower-risk pathway for students.
![Market Share](images/market_share_stacked_area.png)

### The $6.72 Billion Economic Deficit
The abrupt drop in approved visas between the peak (2022-23) and the following year (2023-24) resulted in the loss of **167,921 primary students**. Assuming a conservative annual expenditure of $40,000 AUD per student (tuition and living expenses), this policy shift effectively erased approximately **$6.72 Billion AUD** from the Australian economy in just a single year, heavily impacting the retail, education, and real estate sectors.

## 5. Technical Architecture & Data Pipeline
The analysis is built on a robust Python data pipeline that handles complex, real-world government datasets. Key engineering tasks included:
- **Dynamic Header Handling:** The pipeline programmatically detects and bypasses introductory metadata blocks (which varied between row indices 13 and 14 depending on the report).
- **Pivot-Table Reshaping:** Used Pandas `melt` to transform wide-format Excel pivot tables into a tidy, long-format dataset for time-series analysis.
- **Data Cleaning & Consolidation:** Employed forward-filling (`ffill()`) for merged Excel cells, stripped hidden string characters, cleaned privacy-masked numeric values (e.g., `<5`), and sequentially merged three separate reports (Lodged, Granted, Grant Rates) into a unified analytical DataFrame.

## 6. How to Reproduce
Follow these steps to run the pipeline locally:

1. **Clone the repository** and ensure raw government Excel files are in the `data/raw/` directory.
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Data Cleaning Pipeline:**
   ```bash
   python scripts/clean_data.py
   ```
4. **Run the Trend & Economic Analysis:**
   ```bash
   python scripts/sector_trends_analysis.py
   python scripts/refusals_analysis.py
   python scripts/market_share_analysis.py
   python scripts/economic_impact.py
   ```
