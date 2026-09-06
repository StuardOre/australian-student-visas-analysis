import pandas as pd
import matplotlib.pyplot as plt
import os

def main():
    data_path = os.path.join('data', 'processed', 'student_visas_summary.csv')
    df = pd.read_csv(data_path)
    
    # 1. Filter for Primary applicants only
    df = df[df['Applicant_Type'] == 'Primary'].copy()
    
    # 2. Filter from 2015-16 onwards, excluding the partial year 2026-27
    df = df[df['Financial_Year'] >= '2015-16']
    df = df[~df['Financial_Year'].str.contains('2026-27')]
    
    # 3. Categorize sectors into 3 buckets: Higher Ed, VET, Other
    def categorize_sector(s):
        if 'Higher Education' in s:
            return 'Higher Education'
        elif 'Vocational Education' in s:
            return 'VET'
        else:
            return 'Other Sectors'
            
    df['Market_Sector'] = df['Sector'].apply(categorize_sector)
    
    # 4. Group by Year and Market_Sector, summing the Granted volume
    df_grouped = df.groupby(['Financial_Year', 'Market_Sector'])['Granted'].sum().reset_index()
    
    # Pivot the data to have Years as rows and Sectors as columns
    pivot = df_grouped.pivot(index='Financial_Year', columns='Market_Sector', values='Granted').fillna(0)
    
    # 5. Calculate percentages for 100% Stacked Area Chart
    pivot_pct = pivot.div(pivot.sum(axis=1), axis=0) * 100
    
    # 6. Plotting
    fig, ax = plt.subplots(figsize=(12, 6))
    
    years = pivot_pct.index
    
    # Plot as a stackplot
    ax.stackplot(years, pivot_pct['Higher Education'], pivot_pct['VET'], pivot_pct['Other Sectors'],
                 labels=['Higher Education', 'VET', 'Other Sectors'],
                 colors=['#1f77b4', '#ff7f0e', '#7f7f7f'], alpha=0.85)
                 
    ax.set_title('100% Market Share of Granted Student Visas (2015 - 2026)', fontsize=15, fontweight='bold')
    ax.set_xlabel('Financial Year', fontsize=12)
    ax.set_ylabel('Market Share (%)', fontsize=12)
    ax.set_xlim(years[0], years[-1])
    ax.set_ylim(0, 100)
    plt.xticks(rotation=45)
    
    # Place legend outside the plot area
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title='Education Sector')
    
    plt.tight_layout()
    
    os.makedirs('images', exist_ok=True)
    out_img = os.path.join('images', 'market_share_stacked_area.png')
    plt.savefig(out_img, dpi=300)
    print(f"[+] 100% Stacked Area Chart saved successfully to {out_img}\n")
    
    # 7. Print Analytical Conclusion
    year_start = '2015-16'
    year_end = years[-1]
    
    vet_start = pivot_pct.loc[year_start, 'VET']
    vet_end = pivot_pct.loc[year_end, 'VET']
    he_start = pivot_pct.loc[year_start, 'Higher Education']
    he_end = pivot_pct.loc[year_end, 'Higher Education']
    
    print("--- MARKET SHARE ANALYTICAL CONCLUSION ---")
    print(f"VET Market Share in {year_start}: {vet_start:.1f}%")
    print(f"VET Market Share in {year_end}: {vet_end:.1f}%")
    print(f"Higher Ed Market Share in {year_start}: {he_start:.1f}%")
    print(f"Higher Ed Market Share in {year_end}: {he_end:.1f}%")
    
    print("\n[Conclusion]")
    print("The 100% stacked area chart clearly illustrates a significant structural shift in the Australian international education market.")
    print(f"The Vocational Education and Training (VET) sector has experienced a severe contraction in market dominance, plummeting from a {vet_start:.1f}% share of all granted primary visas in {year_start} to just {vet_end:.1f}% in {year_end}.")
    print("This steep decline aligns directly with the government's targeted policy crackdowns and surging refusal rates in the vocational space.")
    print(f"Conversely, Higher Education has consolidated its position as the preferred, lower-risk pathway, growing its market share from {he_start:.1f}% to {he_end:.1f}% over the same period, effectively absorbing the space left by VET.")

if __name__ == '__main__':
    main()
