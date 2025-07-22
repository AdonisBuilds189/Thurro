import pandas as pd

# === Step 1: Load Excel File as DataFrame ===
EXCEL_FILE = "converted_report.xlsx"

try:
    df_raw = pd.read_excel(EXCEL_FILE, dtype=str)
    print(f"✅ Loaded: {EXCEL_FILE}")

    # === Step 2: Clean it up ===
    df_raw = df_raw.fillna("")  # Replace NaN with empty string
    df_raw = df_raw.applymap(lambda x: str(x).strip())  # Trim every cell

    # === Step 3: Drop rows that are completely blank (all empty or whitespace-only) ===
    def is_empty_row(row):
        # True if ALL cells in row are ""
        return all(cell == "" for cell in row)

    df_cleaned = df_raw[~df_raw.apply(is_empty_row, axis=1)]  # Invert mask

    print(f"📊 After dropping blank rows: {df_cleaned.shape}")

    # === Step 4: Keep only the first 5 meaningful rows & 7 meaningful cols ===
    df_final = df_cleaned.iloc[:5, :7]
    df_final.columns = [f"Column_{i+1}" for i in range(df_final.shape[1])]

    print("\n📋 Final Trimmed Table (5 rows × 7 columns):\n")
    print(df_final)

    # === Step 5: Save output ===
    df_final.to_excel("assignment3_output_filtered.xlsx", index=False)
    print("\n✅ Saved smart-trimmed result to → assignment3_output_filtered.xlsx")

except FileNotFoundError:
    print(f"❌ Missing file: {EXCEL_FILE}")
except Exception as e:
    print(f"❌ Error processing file:", e)
