import pandas as pd
from pathlib import Path
import sys

# --- Constants ---
INPUT_DIR = Path('sources')
OUTPUT_DIR = Path('script_output')

TARGET_SICS = ['6021', '6022']

FLOW_TAGS = [
    'NetIncomeLoss',
    'EarningsPerShareBasic',
    'InterestAndDividendIncomeOperating',
    'InterestIncomeOperating'
]

STOCK_TAGS = [
    'Assets',
    'Liabilities',
    'StockholdersEquity'
]


def read_files(input_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Reads data with correct col tags"""
    try:
        sub = pd.read_csv(
            input_dir / 'sub.txt',
            sep='\t',
            header=0,
            usecols=['adsh', 'cik', 'name', 'sic', 'form', 'fye', 'period'],
            dtype={'cik': str, 'sic': str, 'form': 'category'},
            on_bad_lines='warn'
        )

        num = pd.read_csv(
            input_dir / 'num.txt',
            sep='\t',
            header=0,
            usecols=['adsh', 'tag', 'version', 'coreg', 'segments', 'ddate', 'qtrs', 'uom', 'value'],
            dtype={'qtrs': 'Int8'}, # Use nullable integer for missing values
            on_bad_lines='warn'
        )
        return sub, num
        
    except FileNotFoundError as e:
        print(f"Error: Could not find required input files. {e}")
        sys.exit(1)


def sub_filter(target_sics: list[str], sub: pd.DataFrame) -> pd.DataFrame:
    """Filters the submission dataframe for specific SICs and 10-K forms."""
    return sub[sub['sic'].isin(target_sics) & (sub['form'] == '10-K')].copy()

   
def num_filter(
    target_adsh: list[str], 
    flow_tags: list[str], 
    stock_tags: list[str], 
    num: pd.DataFrame, 
    sub_filtered: pd.DataFrame
) -> pd.DataFrame:
    """
    Filters the numbers dataframe for specific flow/stock tags and merges with sub dates.
    """
    # Create base mask for common filters
    base_mask = (
        num['adsh'].isin(target_adsh) & 
        num['coreg'].isna() & 
        num['segments'].isna()
    )

    # Filter flows and stocks
    flow_mask = base_mask & num['tag'].isin(flow_tags) & (num['qtrs'] == 4)
    stock_mask = base_mask & num['tag'].isin(stock_tags) & (num['qtrs'] == 0)

    # Combine and merge
    num_filtered = num[flow_mask | stock_mask].copy()
    num_filtered = num_filtered.merge(
        sub_filtered[['adsh', 'period']], 
        on='adsh', 
        how='left'
    )

    # Standardize types for date comparison
    num_filtered['ddate'] = num_filtered['ddate'].astype(str)
    
    # Safely handle potential NaNs in 'period' before conversion
    num_filtered['period'] = pd.to_numeric(num_filtered['period'], errors='coerce')
    num_filtered = num_filtered.dropna(subset=['period'])
    num_filtered['period'] = num_filtered['period'].astype(int).astype(str)

    # Filter matching dates and clean up
    num_filtered = num_filtered[num_filtered['ddate'] == num_filtered['period']]
    
    return num_filtered.drop(columns=['period'])


def main():
    # 1. Read Data
    sub, num = read_files(INPUT_DIR)

    # 2. Filter Sub (Banks)
    sub_filtered = sub_filter(TARGET_SICS, sub)

    # 3. Filter Num
    target_adsh = sub_filtered['adsh'].unique()
    num_filtered = num_filter(target_adsh, FLOW_TAGS, STOCK_TAGS, num, sub_filtered)
    
    # 4. Export (ensure output directory exists)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    sub_filtered.to_csv(OUTPUT_DIR / 'companies.csv', index=False)
    num_filtered.to_csv(OUTPUT_DIR / 'financials.csv', index=False)
    
    print("Processing complete. Files saved to output directory.")


if __name__ == "__main__":
    main()
