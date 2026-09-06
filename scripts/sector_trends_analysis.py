import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def main():
    data_path = os.path.join('data', 'processed', 'student_visas_summary.csv')
    df = pd.read_csv(data_path)
    
    # 1. Filter for Primary applicants (main visa holders)
    df_primary = df[df['Applicant_Type'] == 'Primary'].copy()
    
    # 2. Focus on top major education sectors
    sectors_of_interest = [
        'Higher Education Sector', 
        'Vocational Education and Training Sector',
        'Independent ELICOS Sector'
    ]
    df_major = df_primary[df_primary['Sector'].isin(sectors_of_interest)].copy()
    
    # 3. Sort chronologically by Financial Year
    df_major = df_major.sort_values(by='Financial_Year')
    
    # Create images directory if it doesn't exist
    os.makedirs('images', exist_ok=True)
    
    # 4. Generate Line Plot for Granted Visas Volume
    plt.figure(figsize=(14, 7))
    sns.lineplot(data=df_major, x='Financial_Year', y='Granted', hue='Sector', marker='o', linewidth=2.5)
    plt.title('Volume of Primary Student Visas Granted Over Time (By Sector)', fontsize=16, fontweight='bold')
    plt.xlabel('Financial Year', fontsize=13)
    plt.ylabel('Number of Granted Visas', fontsize=13)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(title='Education Sector', loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join('images', 'visa_grants_by_sector.png'), dpi=300)
    plt.close()
    
    # 5. Generate Line Plot for Grant Rates
    plt.figure(figsize=(14, 7))
    sns.lineplot(data=df_major, x='Financial_Year', y='Grant_Rate', hue='Sector', marker='s', linewidth=2.5)
    plt.title('Primary Student Visa Approval Rates Over Time (By Sector)', fontsize=16, fontweight='bold')
    plt.xlabel('Financial Year', fontsize=13)
    plt.ylabel('Grant Rate (Approval Ratio)', fontsize=13)
    
    # Convert y-axis to percentage
    plt.gca().set_yticklabels(['{:.0f}%'.format(x*100) for x in plt.gca().get_yticks()])
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(title='Education Sector', loc='lower left')
    plt.tight_layout()
    plt.savefig(os.path.join('images', 'grant_rates_by_sector.png'), dpi=300)
    plt.close()
    
    # 6. Compute and print key statistics
    print("--- KEY MIGRATION POLICY STATISTICS ---\n")
    
    def get_stat(df, sector, year, column):
        try:
            return df[(df['Sector'] == sector) & (df['Financial_Year'] == year)][column].values[0]
        except IndexError:
            return None

    # Years to compare
    y_pre = '2018-19'
    y_peak = '2022-23'
    y_latest = df_major['Financial_Year'].max()
    
    for sector in ['Higher Education Sector', 'Vocational Education and Training Sector']:
        print(f"[{sector}]")
        
        # Volumes
        v_pre = get_stat(df_major, sector, y_pre, 'Granted')
        v_peak = get_stat(df_major, sector, y_peak, 'Granted')
        v_latest = get_stat(df_major, sector, y_latest, 'Granted')
        
        # Rates
        r_pre = get_stat(df_major, sector, y_pre, 'Grant_Rate')
        r_peak = get_stat(df_major, sector, y_peak, 'Grant_Rate')
        r_latest = get_stat(df_major, sector, y_latest, 'Grant_Rate')
        
        if pd.notnull(v_pre) and pd.notnull(v_peak):
            growth_peak = ((v_peak - v_pre) / v_pre) * 100
            print(f"  -> Volume Growth (Pre-Pandemic {y_pre} to Post-Pandemic Peak {y_peak}): {growth_peak:+.1f}% ({v_pre:,.0f} to {v_peak:,.0f})")
            
        if pd.notnull(v_peak) and pd.notnull(v_latest):
            growth_latest = ((v_latest - v_peak) / v_peak) * 100
            print(f"  -> Volume Shift (Peak {y_peak} to Latest {y_latest}): {growth_latest:+.1f}% ({v_peak:,.0f} to {v_latest:,.0f})")
            
        if pd.notnull(r_peak) and pd.notnull(r_latest):
            rate_drop = (r_latest - r_peak) * 100
            print(f"  -> Approval Rate Shift (Peak {y_peak} to Latest {y_latest}): {rate_drop:+.1f} percentage points ({r_peak:.1%} to {r_latest:.1%})\n")

    print("[SUCCESS] Analysis complete. High-resolution charts saved to the 'images/' folder.")

if __name__ == '__main__':
    main()
