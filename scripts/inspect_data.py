import pandas as pd
import os
import openpyxl

def main():
    data_dir = os.path.join('data', 'raw')
    print(f"--- Exploring files in {data_dir} ---\n")
    
    if not os.path.exists(data_dir):
        print(f"Directory {data_dir} does not exist.")
        return
        
    files = [f for f in os.listdir(data_dir) if f.lower().endswith('.xlsx') or f.lower().endswith('.csv')]
    
    if not files:
        print("No .xlsx or .csv files found in the data/raw/ directory.")
        return
        
    for filename in files:
        file_path = os.path.join(data_dir, filename)
        print("="*60)
        print(f"FILE: {filename}")
        print("="*60)
        
        ext = os.path.splitext(filename)[1].lower()
        
        if ext == '.xlsx':
            try:
                wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
                sheet_names = wb.sheetnames
                print(f"-> Sheet names found: {sheet_names}")
                
                df = pd.read_excel(file_path, sheet_name=sheet_names[0], nrows=10, header=None)
                print(f"-> First 3 rows of sheet '{sheet_names[0]}':")
                print(df.head(3).to_string(index=False))
                
                # Heuristic: find the first row with fewer nulls as a potential header
                header_row = -1
                for i in range(len(df)):
                    # Allow up to 10% nulls in header, or look for 0 nulls
                    null_pct = df.iloc[i].isnull().sum() / len(df.columns)
                    if null_pct < 0.2: 
                        header_row = i
                        break
                        
                if header_row > 0:
                    print(f"\n[!] ALERT: Introductory metadata detected. Actual column headers likely start at row index {header_row} (Excel row {header_row+1}).")
                elif header_row == 0:
                    print(f"\n[+] Standard format: Row 0 appears to be the true header.")
                else:
                    print(f"\n[?] Could not confidently determine header. Manual inspection required.")
                    
            except Exception as e:
                print(f"Error reading Excel file: {e}")
                
        elif ext == '.csv':
            try:
                df = pd.read_csv(file_path, nrows=10, header=None)
                print(f"-> First 3 rows:")
                print(df.head(3).to_string(index=False))
                
                header_row = -1
                for i in range(len(df)):
                    null_pct = df.iloc[i].isnull().sum() / len(df.columns)
                    if null_pct < 0.2:
                        header_row = i
                        break
                        
                if header_row > 0:
                    print(f"\n[!] ALERT: Introductory metadata detected. Actual column headers likely start at row {header_row}.")
                elif header_row == 0:
                    print(f"\n[+] Standard format: Row 0 appears to be the true header.")
                else:
                    print(f"\n[?] Could not confidently determine header. Manual inspection required.")
            except Exception as e:
                print(f"Error reading CSV file: {e}")
                
        print("\n")

if __name__ == "__main__":
    main()
