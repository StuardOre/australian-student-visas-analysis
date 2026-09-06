import pandas as pd
import os
import numpy as np
import warnings

# Suppress openpyxl warnings about print area
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

def load_and_melt(file_path, sheet_name, value_name, header_idx=14):
    # Load sheet using the specific row index as header
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=header_idx)
    
    # Rename the first two columns
    cols = list(df.columns)
    cols[0] = 'Applicant_Type'
    cols[1] = 'Sector'
    df.columns = cols
    
    # Forward-fill 'Applicant_Type' to resolve merged cells
    df['Applicant_Type'] = df['Applicant_Type'].ffill()
    
    # Clean up Applicant_Type and Sector string values
    df['Applicant_Type'] = df['Applicant_Type'].astype(str).str.strip()
    df['Sector'] = df['Sector'].astype(str).str.strip()
    
    # Drop summary rows (e.g., 'Primary Total', 'Grand Total', or 'nan')
    df = df[~df['Applicant_Type'].str.contains('Total|nan', case=False, na=False)]
    df = df[~df['Sector'].str.contains('Total|nan', case=False, na=False)]
    
    # Identify financial year columns (exclude Applicant_Type, Sector, and any Total columns)
    id_vars = ['Applicant_Type', 'Sector']
    year_cols = [c for c in df.columns if c not in id_vars and 'Total' not in str(c) and 'Unnamed' not in str(c) and not pd.isna(c)]
    
    # Melt the table from wide to long format
    df_melted = df.melt(id_vars=id_vars, value_vars=year_cols, 
                        var_name='Financial_Year', value_name=value_name)
                        
    # Ensure Financial_Year is cleanly formatted (e.g., strip spaces to fix merge mismatches)
    df_melted['Financial_Year'] = df_melted['Financial_Year'].astype(str).str.strip()
    
    # Clean numeric columns (remove commas, percentage signs, <5 cases, convert to float)
    def clean_numeric(val):
        if pd.isna(val):
            return np.nan
        val_str = str(val).strip().replace(',', '').replace('%', '')
        if val_str == '-' or val_str == '' or val_str == '<5':
            return np.nan # '<5' is commonly used in gov data to obscure small numbers for privacy
        try:
            return float(val_str)
        except ValueError:
            return np.nan
            
    df_melted[value_name] = df_melted[value_name].apply(clean_numeric)
    
    return df_melted

def main():
    data_dir = os.path.join('data', 'raw')
    
    # File Paths
    file_granted = os.path.join(data_dir, 'bp0015l-student-visas-granted-report-locked-at-2026-07-31-v100.xlsx')
    sheet_granted = 'Granted (Month)'
    
    file_lodged = os.path.join(data_dir, 'bp0015l-student-visas-lodged-report-locked-at-2026-07-31-v100.xlsx')
    sheet_lodged = 'Lodged (Month) '
    
    file_rate = os.path.join(data_dir, 'bp0015l-student-visa-grant-rates-locked-at-2026-07-31-v100.xlsx')
    sheet_rate = 'Grant Rate (Month)'
    
    print("Processing Lodged dataset...")
    df_lodged = load_and_melt(file_lodged, sheet_lodged, 'Lodged', header_idx=13)
    
    print("Processing Granted dataset...")
    df_granted = load_and_melt(file_granted, sheet_granted, 'Granted')
    
    print("Processing Grant Rates dataset...")
    df_rate = load_and_melt(file_rate, sheet_rate, 'Grant_Rate', header_idx=13)
    
    print("\nMerging datasets into unified DataFrame...")
    # Merge datasets sequentially
    df_merged = pd.merge(df_lodged, df_granted, on=['Applicant_Type', 'Sector', 'Financial_Year'], how='outer')
    df_merged = pd.merge(df_merged, df_rate, on=['Applicant_Type', 'Sector', 'Financial_Year'], how='outer')
    
    # Sort for cleanliness
    df_merged = df_merged.sort_values(by=['Applicant_Type', 'Sector', 'Financial_Year']).reset_index(drop=True)
    
    # Save the processed dataset
    out_dir = os.path.join('data', 'processed')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'student_visas_summary.csv')
    df_merged.to_csv(out_path, index=False)
    
    print(f"\n[+] Success: Unified dataset saved to {out_path}\n")
    
    print("--- First 5 Rows ---")
    print(df_merged.head(5).to_string())
    
    print("\n--- Summary Statistics ---")
    print(df_merged.describe().to_string())
    
if __name__ == '__main__':
    main()
