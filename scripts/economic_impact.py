import pandas as pd
import os

def main():
    data_path = os.path.join('data', 'processed', 'student_visas_summary.csv')
    df = pd.read_csv(data_path)
    
    # Filter for Primary applicants only
    df_primary = df[df['Applicant_Type'] == 'Primary'].copy()
    
    # Calculate the total Granted volume across ALL sectors per financial year
    yearly_totals = df_primary.groupby('Financial_Year')['Granted'].sum()
    
    year_peak = '2022-23'
    year_next = '2023-24'
    
    vol_peak = yearly_totals.get(year_peak, 0)
    vol_next = yearly_totals.get(year_next, 0)
    
    # Calculate the drop in student volume
    students_lost = vol_peak - vol_next
    
    if students_lost <= 0:
        print(f"Unexpected data: Volume did not drop between {year_peak} and {year_next}.")
        return
        
    # Economic impact parameters
    spend_per_student = 40000  # $40,000 AUD (Tuition + Living Expenses)
    economic_deficit = students_lost * spend_per_student
    
    # Convert to Billions
    deficit_billions = economic_deficit / 1_000_000_000
    
    print("--- ECONOMIC IMPACT OF MIGRATION TIGHTENING ---")
    print(f"Total Granted Visas (Peak {year_peak}): {vol_peak:,.0f}")
    print(f"Total Granted Visas ({year_next}):        {vol_next:,.0f}")
    print(f"Total Primary Students Lost:            {students_lost:,.0f}")
    print(f"\nEstimated Annual Spend per Student:     ${spend_per_student:,.0f} AUD")
    print("=" * 55)
    print(f"ESTIMATED ECONOMIC DEFICIT:             ${deficit_billions:.2f} BILLION AUD")
    print("=" * 55)
    
    print("\n[Analytical Conclusion]")
    print(f"The aggressive tightening of the Australian student visa framework resulted in a sharp contraction of {students_lost:,.0f} primary international students between {year_peak} and {year_next}.")
    print(f"Assuming a conservative annual expenditure of $40,000 AUD per student, this policy shift has effectively erased approximately ${deficit_billions:.2f} Billion AUD from the Australian economy in just one year, heavily impacting the education sector, retail, and real estate markets.")

if __name__ == '__main__':
    main()
