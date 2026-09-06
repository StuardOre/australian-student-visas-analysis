import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

def main():
    data_path = os.path.join('data', 'processed', 'student_visas_summary.csv')
    df = pd.read_csv(data_path)
    
    # 1. Filter for Primary applicants to maintain consistency
    df = df[df['Applicant_Type'] == 'Primary'].copy()
    
    # 2. Calculate Refused_or_Withdrawn (Lodged - Granted)
    # We use a lambda to replace negative values with 0 (due to natural processing lag across months)
    df['Refused_or_Withdrawn'] = df['Lodged'] - df['Granted']
    df['Refused_or_Withdrawn'] = df['Refused_or_Withdrawn'].apply(lambda x: max(x, 0) if pd.notnull(x) else np.nan)
    
    # 3. Filter for specific sectors
    sectors = ['Higher Education Sector', 'Vocational Education and Training Sector']
    df = df[df['Sector'].isin(sectors)]
    
    # 4. Filter for Financial Years from 2018-19 onwards
    df = df[df['Financial_Year'] >= '2018-19']
    
    # Exclude the partial year '2026-27 to 31 July 2026' so it doesn't skew the visual chart
    df = df[~df['Financial_Year'].str.contains('2026-27')]
    
    # 5. Generate Stacked Bar Chart (Subplots for each sector)
    fig, axes = plt.subplots(1, 2, figsize=(16, 7), sharey=True)
    
    for idx, sector in enumerate(sectors):
        df_sector = df[df['Sector'] == sector].copy()
        
        years = df_sector['Financial_Year']
        granted = df_sector['Granted']
        refused = df_sector['Refused_or_Withdrawn']
        
        ax = axes[idx]
        
        # Plot Granted (Green)
        ax.bar(years, granted, label='Granted', color='#2ca02c', alpha=0.85)
        
        # Plot Refused on top of Granted (Red)
        ax.bar(years, refused, bottom=granted, label='Refused or Withdrawn', color='#d62728', alpha=0.85)
        
        ax.set_title(sector, fontsize=14, fontweight='bold')
        ax.set_xlabel('Financial Year', fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(axis='y', linestyle='--', alpha=0.5)
        ax.legend()

    axes[0].set_ylabel('Volume of Primary Applications', fontsize=13)
    plt.suptitle('Student Visa Outcomes: Granted vs Refused/Withdrawn (Since 2018-19)', fontsize=18, fontweight='bold')
    plt.tight_layout()
    
    # Save Image
    os.makedirs('images', exist_ok=True)
    out_img = os.path.join('images', 'refusals_stacked_bar.png')
    plt.savefig(out_img, dpi=300)
    print(f"[+] Stacked bar chart saved successfully to {out_img}\n")
    
    # 6. Calculate exact figures for the recent increase in refusals
    # We compare the last two COMPLETE financial years
    y_prev = '2024-25'
    y_last = '2025-26'
    
    print("--- RECENT REFUSALS SURGE ANALYSIS ---")
    for sector in sectors:
        try:
            ref_prev = df[(df['Sector'] == sector) & (df['Financial_Year'] == y_prev)]['Refused_or_Withdrawn'].values[0]
            ref_last = df[(df['Sector'] == sector) & (df['Financial_Year'] == y_last)]['Refused_or_Withdrawn'].values[0]
            
            diff = ref_last - ref_prev
            pct_diff = (diff / ref_prev) * 100 if ref_prev > 0 else 0
            
            print(f"[{sector}]")
            print(f"  -> Total Refused/Withdrawn in {y_prev}: {ref_prev:,.0f}")
            print(f"  -> Total Refused/Withdrawn in {y_last}: {ref_last:,.0f}")
            print(f"  -> ABSOLUTE INCREASE: +{diff:,.0f} applications (+{pct_diff:.1f}%)\n")
        except Exception as e:
            print(f"[{sector}] Error calculating stats: {e}\n")

if __name__ == '__main__':
    main()
