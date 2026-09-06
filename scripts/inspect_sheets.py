import pandas as pd
import os

def process_sheet(file_path, sheet_name):
    print("=" * 70)
    print(f"Processing File: {os.path.basename(file_path)}")
    print(f"Target Sheet: '{sheet_name}'")
    print("-" * 70)
    
    try:
        # Read a raw slice to understand the pivot layout
        df_raw = pd.read_excel(file_path, sheet_name=sheet_name, header=None, nrows=25)
        
        print("\n-> Raw slice (First 25 rows, first 5 columns):")
        print(df_raw.iloc[:, :5].to_string())
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"Error processing {os.path.basename(file_path)}: {e}")

def main():
    data_dir = os.path.join('data', 'raw')
    
    file_granted = os.path.join(data_dir, 'bp0015l-student-visas-granted-report-locked-at-2026-07-31-v100.xlsx')
    sheet_granted = 'Granted (Month)'
    
    file_lodged = os.path.join(data_dir, 'bp0015l-student-visas-lodged-report-locked-at-2026-07-31-v100.xlsx')
    sheet_lodged = 'Lodged (Month) ' # Note the trailing space
    
    process_sheet(file_granted, sheet_granted)
    process_sheet(file_lodged, sheet_lodged)

if __name__ == '__main__':
    main()
