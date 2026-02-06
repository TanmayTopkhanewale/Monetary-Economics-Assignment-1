"""
Assignment 1 - Part 3: RBI Money Stock Analysis
Downloads and analyzes M3 money stock component
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def download_rbi_data():
    """
    Download RBI money stock data
    Note: RBI DBIE doesn't provide direct API access
    This script provides structure for manual download and analysis
    """
    print("=" * 80)
    print("RBI Money Stock Data Download Instructions")
    print("=" * 80)
    print("\nRBI DBIE doesn't provide direct API access.")
    print("Please follow these steps:")
    print("\n1. Go to: https://dbie.rbi.org.in/DBIE/dbie.rbi?site=publications")
    print("2. Navigate to: Time-Series Publications -> Weekly Statistical Supplement")
    print("3. Find Table No. 6 - Money Stock: Components and Sources")
    print("4. Download the data (usually available as Excel/CSV)")
    print("5. Save as 'rbi_money_stock.csv' or 'rbi_money_stock.xlsx'")
    print("\nFor Table No. 5 - Ratios and Rates:")
    print("- Download from the same location")
    print("- Save as 'rbi_ratios_rates.csv' or 'rbi_ratios_rates.xlsx'")
    print("\nReference: https://www.rbi.org.in/Scripts/PublicationReportDetails.aspx?ID=293")
    
    return None

def load_money_stock_data(filepath=r'C:\Users\hp\Desktop\Monetary Economics\rbi_money_stock.csv'):
    """Load money stock data from Excel or CSV file"""
    import os
    
    def _flatten_columns(df):
        if isinstance(df.columns, pd.MultiIndex):
            flat_cols = []
            for parts in df.columns:
                cleaned = [str(p).strip() for p in parts if p is not None and str(p).strip() != '' and 'UNNAMED' not in str(p).upper()]
                flat_cols.append(" ".join(cleaned).strip())
            df.columns = flat_cols
        return df
    
    # Check file extension to determine file type
    file_ext = os.path.splitext(filepath)[1].lower()
    
    if file_ext in ['.xlsx', '.xls']:
        # Try Excel
        try:
            data = pd.read_excel(filepath, sheet_name=None, header=[0, 1])  # Try multi-row header
            # Flatten MultiIndex headers if present
            if isinstance(data, dict):
                data = {k: _flatten_columns(v) for k, v in data.items()}
            else:
                data = _flatten_columns(data)
            return data
        except Exception as e:
            print(f"Error loading Excel file: {e}")
            return None
    else:
        # Try CSV with different encodings
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252', 'windows-1252']
        
        for encoding in encodings:
            try:
                # Read CSV - try with header detection
                # First, try reading with header=0 (first row as header)
                try:
                    data = pd.read_csv(filepath, encoding=encoding, header=[0, 1], thousands=',')
                except:
                    # If that fails, try without thousands parameter
                    data = pd.read_csv(filepath, encoding=encoding, header=[0, 1])
                
                # Flatten multi-row headers if present
                data = _flatten_columns(data)
                
                # Try to identify date column (usually first column)
                date_col = data.columns[0]
                print(f"  Date column identified: '{date_col}'")
                
                # Convert date column - handle DD-Mon-YY format
                try:
                    # Try parsing with dayfirst=True for DD-Mon-YY format
                    data[date_col] = pd.to_datetime(data[date_col], dayfirst=True, errors='coerce')
                except:
                    # If that fails, try standard parsing
                    try:
                        data[date_col] = pd.to_datetime(data[date_col], errors='coerce')
                    except:
                        # If still fails, keep as is
                        pass
                
                # Set date as index
                data = data.set_index(date_col)
                
                # Remove rows where date is NaT (invalid dates) - but keep numeric index if dates failed
                if data.index.dtype == 'object' or pd.api.types.is_datetime64_any_dtype(data.index):
                    data = data[data.index.notna()]
                else:
                    # If index is numeric, it might be row numbers - try to find date column
                    print("  Warning: Date column might not be properly parsed")
                
                # Convert numeric columns (handle Indian numbering with commas)
                for col in data.columns:
                    if data[col].dtype == 'object':
                        # Remove commas, spaces, and other non-numeric chars except decimal point
                        data[col] = data[col].astype(str).str.replace(',', '').str.replace(' ', '')
                        # Remove any trailing hyphens or special chars
                        data[col] = data[col].str.rstrip(' -')
                        # Convert to numeric
                        data[col] = pd.to_numeric(data[col], errors='coerce')
                
                print(f"✓ Successfully loaded CSV file with {encoding} encoding")
                print(f"  Date range: {data.index.min()} to {data.index.max()}")
                print(f"  Number of rows: {len(data)}")
                print(f"  Sample data types: {dict(data.dtypes.head(5))}")
                return data
            except UnicodeDecodeError:
                continue
            except Exception as e:
                # If it's not an encoding error, try next encoding or return None
                if 'codec' not in str(e).lower() and 'decode' not in str(e).lower():
                    print(f"Error loading CSV file: {e}")
                    # Try one more time with simpler approach
                    try:
                        data = pd.read_csv(filepath, encoding=encoding)
                        print(f"✓ Loaded CSV with basic parsing (encoding: {encoding})")
                        return data
                    except:
                        continue
                continue
        
        print(f"Error: Could not decode CSV file with any of the tried encodings: {encodings}")
        return None

def extract_money_components(data):
    """
    Extract M0, M1, M3 components from RBI data.
    Handles both direct columns and component-based structure.
    """
    components = {}
    
    if isinstance(data, dict):
        # Multiple sheets - process each sheet
        for sheet_name, sheet_data in data.items():
            print(f"Processing sheet: {sheet_name}")
            result = _extract_from_dataframe(sheet_data)
            components.update(result)
    else:
        # Single DataFrame
        components = _extract_from_dataframe(data)
    
    return components

def _extract_from_dataframe(df):
    """Helper function to extract M0, M1, M3 from a single DataFrame"""
    components = {}
    
    print(f"  Available columns: {list(df.columns)[:15]}...")  # Show first 15 columns
    
    def _norm(col):
        return " ".join(str(col).replace("\n", " ").replace("\r", " ").strip().upper().split())
    
    def _to_numeric(series):
        s = series.copy()
        if s.dtype == 'object':
            s = s.astype(str)
            s = s.str.replace(',', '', regex=False)
            s = s.str.replace(' ', '', regex=False)
            s = s.str.rstrip(' -')
        return pd.to_numeric(s, errors='coerce')
    
    def _find_col_by_keywords(include_any=None, include_all=None, exclude_any=None, startswith=None):
        include_any = [k.upper() for k in (include_any or [])]
        include_all = [k.upper() for k in (include_all or [])]
        exclude_any = [k.upper() for k in (exclude_any or [])]
        startswith = startswith.upper() if startswith else None
        for col in df.columns:
            n = _norm(col)
            if startswith and not n.startswith(startswith):
                continue
            if include_any and not any(k in n for k in include_any):
                continue
            if include_all and not all(k in n for k in include_all):
                continue
            if exclude_any and any(k in n for k in exclude_any):
                continue
            return col
        return None

    def _find_col_by_prefix(prefix):
        p = prefix.strip()
        for col in df.columns:
            c = str(col).strip()
            if c.startswith(p):
                return col
        return None
    
    # Direct columns first (M0/M1/M3)
    direct_m0 = _find_col_by_keywords(include_any=["M0", "M 0", "RESERVE MONEY"])
    direct_m1 = _find_col_by_keywords(include_any=["M1", "M 1", "NARROW MONEY"])
    direct_m3 = _find_col_by_keywords(include_any=["M3", "M 3", "BROAD MONEY"], exclude_any=["EXCLUDING", "M30"])
    
    if direct_m0:
        m0_data = _to_numeric(df[direct_m0])
        if m0_data.notna().sum() > 0:
            components['M0'] = m0_data
            print(f"  ✓ Extracted M0 from column: '{direct_m0}'")
    
    if direct_m1:
        m1_data = _to_numeric(df[direct_m1])
        if m1_data.notna().sum() > 0:
            components['M1'] = m1_data
            print(f"  ✓ Extracted M1 from column: '{direct_m1}'")
    
    if direct_m3:
        m3_data = _to_numeric(df[direct_m3])
        if m3_data.notna().sum() > 0:
            components['M3'] = m3_data
            print(f"  ✓ Extracted M3 from column: '{direct_m3}'")
    
    # Compute M0 if not found: Currency in Circulation + Bankers' Deposits with RBI + Other Deposits with RBI
    if 'M0' not in components:
        col_currency_circ = _find_col_by_keywords(include_all=["CURRENCY", "CIRCULATION"])
        col_bankers_dep = _find_col_by_keywords(include_all=["BANKERS", "DEPOSITS", "RBI"])
        col_other_dep_rbi = _find_col_by_keywords(include_all=["OTHER", "DEPOSITS", "RBI"])
        # Fall back to numbered components if present (typically in "1 Components" table)
        if not col_currency_circ:
            col_currency_circ = _find_col_by_prefix("1.1")
        if not col_other_dep_rbi:
            col_other_dep_rbi = _find_col_by_prefix("1.4")
        if col_currency_circ and col_bankers_dep and col_other_dep_rbi:
            components['M0'] = (
                _to_numeric(df[col_currency_circ]) +
                _to_numeric(df[col_bankers_dep]) +
                _to_numeric(df[col_other_dep_rbi])
            )
            print("  ✓ Calculated M0 = Currency in Circulation + Bankers' Deposits with RBI + Other Deposits with RBI")
        else:
            missing = []
            if not col_currency_circ:
                missing.append("Currency in Circulation")
            if not col_bankers_dep:
                missing.append("Bankers' Deposits with RBI")
            if not col_other_dep_rbi:
                missing.append("Other Deposits with RBI")
            if missing:
                print(f"  ⚠ Cannot calculate M0 - missing components: {', '.join(missing)}")
    
    # Compute M1 if not found:
    # M1 = Currency with the Public + Demand Deposits with the Banking System + Other Deposits with RBI
    # or Currency with the Public + Current Deposits + Demand Liabilities Portion of Savings Deposits + Other Deposits with RBI
    if 'M1' not in components:
        col_currency_public = _find_col_by_keywords(include_all=["CURRENCY", "PUBLIC"])
        col_demand_deposits = _find_col_by_keywords(include_all=["DEMAND", "DEPOSITS", "BANKING SYSTEM"])
        col_other_dep_rbi = _find_col_by_keywords(include_all=["OTHER", "DEPOSITS", "RBI"])
        
        # Fall back to numbered components if present (1.1, 1.2, 1.4)
        if not col_currency_public:
            col_currency_public = _find_col_by_prefix("1.1")
        if not col_demand_deposits:
            col_demand_deposits = _find_col_by_prefix("1.2")
        if not col_other_dep_rbi:
            col_other_dep_rbi = _find_col_by_prefix("1.4")
        
        if col_currency_public and col_demand_deposits and col_other_dep_rbi:
            components['M1'] = (
                _to_numeric(df[col_currency_public]) +
                _to_numeric(df[col_demand_deposits]) +
                _to_numeric(df[col_other_dep_rbi])
            )
            print("  ✓ Calculated M1 = Currency with Public + Demand Deposits + Other Deposits with RBI")
        else:
            # Try expanded definition
            col_current_dep = _find_col_by_keywords(include_all=["CURRENT", "DEPOSITS", "BANKING SYSTEM"])
            col_savings_demand_liab = _find_col_by_keywords(
                include_all=["SAVINGS", "DEPOSITS"],
                include_any=["DEMAND LIABILITIES", "DEMAND PORTION", "DEMAND LIAB"]
            )
            if col_currency_public and col_current_dep and col_savings_demand_liab and col_other_dep_rbi:
                components['M1'] = (
                    _to_numeric(df[col_currency_public]) +
                    _to_numeric(df[col_current_dep]) +
                    _to_numeric(df[col_savings_demand_liab]) +
                    _to_numeric(df[col_other_dep_rbi])
                )
                print("  ✓ Calculated M1 = Currency with Public + Current Deposits + Demand Liabilities of Savings Deposits + Other Deposits with RBI")
            else:
                missing = []
                if not col_currency_public:
                    missing.append("Currency with Public")
                if not col_demand_deposits and not col_current_dep:
                    missing.append("Demand Deposits or Current Deposits")
                if not col_other_dep_rbi:
                    missing.append("Other Deposits with RBI")
                if missing:
                    print(f"  ⚠ Cannot calculate M1 - missing components: {', '.join(missing)}")
    
    # Compute M3 if not found:
    # M3 = M2 + Term Deposits (over 1 year) + Call/Term borrowings from 'non-depository' financial corporations
    if 'M3' not in components:
        col_m2 = _find_col_by_keywords(include_any=["M2", "M 2"])
        col_term_over_1y = _find_col_by_keywords(include_all=["TERM", "DEPOSITS", "OVER ONE YEAR"])
        col_call_term_borrowings = _find_col_by_keywords(include_all=["CALL/TERM", "BORROWINGS"], include_any=["NON-DEPOSITORY", "NON DEPOSITORY"])
        
        if col_m2 and col_term_over_1y and col_call_term_borrowings:
            components['M3'] = (
                _to_numeric(df[col_m2]) +
                _to_numeric(df[col_term_over_1y]) +
                _to_numeric(df[col_call_term_borrowings])
            )
            print("  ✓ Calculated M3 = M2 + Term Deposits (over 1 year) + Call/Term Borrowings (non-depository financial corporations)")
        else:
            missing = []
            if not col_m2:
                missing.append("M2")
            if not col_term_over_1y:
                missing.append("Term Deposits over 1 year")
            if not col_call_term_borrowings:
                missing.append("Call/Term Borrowings from non-depository financial corporations")
            if missing:
                print(f"  ⚠ Cannot calculate M3 - missing components: {', '.join(missing)}")
    
    return components

def plot_money_components(components, save_path='rbi_money_stock_analysis.xlsx'):
    """Plot M0, M1, M3 on a graph"""
    if not components:
        print("No money stock components found to plot")
        return None
    
    fig, ax = plt.subplots(figsize=(16, 8))
    
    plot_order = [
        ("M0", "M0 (Reserve Money)", "#1f77b4"),
        ("M1", "M1 (Narrow Money)", "#2ca02c"),
        ("M3", "M3 (Broad Money)", "#d62728"),
    ]
    
    plotted = False
    for key, label, color in plot_order:
        if key in components and components[key] is not None and len(components[key]) > 0:
            ax.plot(components[key].index, components[key].values,
                    label=label, linewidth=2, color=color)
            plotted = True
    
    if not plotted:
        print("No usable series found to plot")
        return None
    
    ax.set_title('Money Stock: M0, M1, M3', fontsize=16, fontweight='bold')
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Amount (in Crores)', fontsize=12)
    ax.legend(fontsize=11, loc='upper left')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('money_stock_components.png', dpi=300, bbox_inches='tight')
    print("Plot saved as 'money_stock_components.png'")
    
    return fig

def calculate_correlation(components):
    """Calculate correlation between money stock components"""
    # Combine all components into a single DataFrame
    df = pd.DataFrame(components)
    
    # Calculate correlation matrix
    corr_matrix = df.corr()
    
    return corr_matrix

def document_components():
    """Document the RBI money stock components (M0, M1, M3)"""
    documentation = """
    MONEY STOCK COMPONENTS (RBI - New Monetary Aggregates):
    
    M0 (Reserve Money):
    = Currency in Circulation
    + Bankers' Deposits with the RBI
    + Other Deposits with the RBI
    
    M1 (Narrow Money):
    = Currency with the Public
    + Demand Deposits with the Banking System
    + Other Deposits with the RBI
    
    Alternate breakdown of M1:
    = Currency with the Public
    + Current Deposits with the Banking System
    + Demand Liabilities Portion of Savings Deposits with the Banking System
    + Other Deposits with the RBI
    
    M3 (Broad Money):
    = M2
    + Term Deposits of residents with contractual maturity of over one year with the Banking System
    + Call/Term borrowings from 'Non-depository' financial corporations by the Banking System
    
    CHARACTERISTICS:
    - M3 is the most commonly used measure of money supply in India
    - It includes both transaction money and savings
    - Used as a key indicator for monetary policy decisions
    - Better predictor of economic activity than narrower measures
    - More stable than narrower money measures
    
    POLICY RELEVANCE:
    - M3 growth is a key indicator for inflation targeting
    - RBI uses M3 growth rate for monetary policy decisions
    - M3 growth reflects both liquidity and savings in the economy
    
    REFERENCE:
    RBI Handbook of Statistics on Indian Economy
    https://www.rbi.org.in/Scripts/PublicationReportDetails.aspx?ID=293
    """
    return documentation

def main():
    print("=" * 80)
    print("RBI Money Stock Analysis - Assignment 1, Part 3")
    print("=" * 80)
    
    # Show download instructions
    download_rbi_data()
    
    # Try to load data
    print("\n" + "=" * 80)
    print("Attempting to load data from file...")
    print("=" * 80)
    
    data = load_money_stock_data()
    
    if data is None:
        print("\nNo data file found. Please download the data first.")
        print("\nCreating template structure...")
        
        # Create template Excel file with structure
        # Generate date range first to get exact length
        date_range = pd.date_range(start='2020-01-01', end='2024-12-31', freq='W')
        num_dates = len(date_range)
        
        template_data = {
            'Date': date_range,
            'M3': np.random.uniform(150000000, 200000000, num_dates)  # Broad Money
        }
        template_df = pd.DataFrame(template_data)
        template_df.to_excel('rbi_money_stock_template.xlsx', index=False)
        print("Template file created: 'rbi_money_stock_template.xlsx'")
        print("Please replace with actual RBI data.")
        print("Expected: M3 column or components 1.1, 1.2, 1.3 to calculate M3")
        return
    
    # Extract components
    print("\nExtracting money stock components...")
    components = extract_money_components(data)
    
    if not components:
        print("Could not extract any money stock components. Please check data format.")
        return
    
    print(f"\n✓ Found {len(components)} components: {list(components.keys())}")
    
    # Document components
    doc = document_components()
    print("\n" + "=" * 80)
    print("MONEY STOCK COMPONENTS DOCUMENTATION")
    print("=" * 80)
    print(doc)
    
    # Plot components
    print("\nCreating plots...")
    plot_money_components(components)
    
    # Calculate basic statistics for M0/M1/M3
    stats_rows = []
    for comp_name in ["M0", "M1", "M3"]:
        if comp_name in components:
            series = components[comp_name]
            if series is not None and len(series) > 0:
                print("\n" + "=" * 80)
                print(f"{comp_name} STATISTICS")
                print("=" * 80)
                print(f"Current {comp_name}: {series.iloc[-1]:,.0f} Crores")
                print(f"Minimum {comp_name}: {series.min():,.0f} Crores")
                print(f"Maximum {comp_name}: {series.max():,.0f} Crores")
                print(f"Average {comp_name}: {series.mean():,.0f} Crores")
                
                growth_rate = None
                if len(series) > 1 and series.iloc[0] != 0:
                    growth_rate = ((series.iloc[-1] / series.iloc[0]) - 1) * 100
                    print(f"Total Growth: {growth_rate:.2f}%")
                print(f"Date Range: {series.index.min()} to {series.index.max()}")
                
                stats_rows.append({
                    "Component": comp_name,
                    "Current": f"{series.iloc[-1]:,.0f}",
                    "Minimum": f"{series.min():,.0f}",
                    "Maximum": f"{series.max():,.0f}",
                    "Average": f"{series.mean():,.0f}",
                    "Total Growth (%)": f"{growth_rate:.2f}" if growth_rate is not None else "N/A",
                })
    
    # Save analysis
    with pd.ExcelWriter('rbi_money_stock_analysis.xlsx', engine='openpyxl') as writer:
        # Save components
        components_df = pd.DataFrame(components)
        components_df.to_excel(writer, sheet_name='Money Stock Components', index=True)
        
        # Save documentation
        doc_df = pd.DataFrame({'Documentation': [doc]})
        doc_df.to_excel(writer, sheet_name='Components Documentation', index=False)
        
        # Save M0/M1/M3 statistics if available
        if stats_rows:
            stats_df = pd.DataFrame(stats_rows)
            stats_df.to_excel(writer, sheet_name='Money Stock Statistics', index=False)
        
        # Analysis sheet
        analysis = """
        MONEY STOCK ANALYSIS (M0, M1, M3):
        
        OVERVIEW:
        - M0 (Reserve Money) reflects high-powered money created by the RBI and is the base for credit creation.
        - M1 (Narrow Money) captures money most readily available for transactions.
        - M3 (Broad Money) includes longer-term savings and is the standard policy aggregate in India.
        
        WHY THESE MEASURES MATTER:
        1. TRANSACTION VS. SAVINGS:
           - M1 is most sensitive to immediate spending and liquidity conditions.
           - M3 reflects both transaction money and longer-term deposits.
        
        2. POLICY SIGNALS:
           - M0 signals RBI liquidity operations and reserve money creation.
           - M3 growth is commonly used in monetary policy assessment and inflation analysis.
        
        3. COMPREHENSIVE COVERAGE:
           - Together, M0/M1/M3 provide a layered view of liquidity from base money to broad money.
        
        COMPONENTS SUMMARY:
        - M0 = Currency in Circulation + Bankers' Deposits with RBI + Other Deposits with RBI
        - M1 = Currency with Public + Demand Deposits + Other Deposits with RBI
        - M3 = M2 + Term Deposits (over 1 year) + Call/Term Borrowings (non-depository financial corporations)
        
        CONCLUSION:
        Using M0, M1, and M3 together provides a clearer picture of liquidity creation,
        transaction money, and savings in the economy than any single measure alone.
        """
        analysis_df = pd.DataFrame({'Analysis': [analysis]})
        analysis_df.to_excel(writer, sheet_name='Best Measure Analysis', index=False)
    
    print("\n" + "=" * 80)
    print("Analysis saved to 'rbi_money_stock_analysis.xlsx'")
    print("=" * 80)

if __name__ == "__main__":
    main()
