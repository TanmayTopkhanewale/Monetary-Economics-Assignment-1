"""
Assignment 1 - Part 3: RBI Money Stock Analysis
Downloads RBI Money Stock (Table 6) and plots M3 trends
Note: 10-year G-sec yield data needs to be added separately
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def load_rbi_table6(filepath):
    """Load RBI Table 6 - Money Stock"""
    try:
        # Read CSV with proper encoding
        data = pd.read_csv(filepath, skiprows=0, encoding='latin-1')
        
        # Parse dates
        data['Date'] = pd.to_datetime(data['Date'], format='%d-%b-%y', errors='coerce')
        data = data.set_index('Date')
        
        # Clean numeric columns - remove commas
        for col in data.columns:
            if col != 'Date':
                data[col] = data[col].astype(str).str.replace(',', '').replace('-', np.nan)
                data[col] = pd.to_numeric(data[col], errors='coerce')
        
        return data
    except Exception as e:
        print(f"Error loading Table 6: {e}")
        return None

def load_yield_data(filepath=None):
    """
    Load 10-year G-sec yield data
    This needs to be downloaded separately from RBI or other sources
    """
    if filepath is None:
        print("\nNote: 10-year G-sec yield data not provided.")
        print("You can download this from:")
        print("- RBI Database: https://dbie.rbi.org.in/DBIE/dbie.rbi?site=publications")
        print("- Or search for 'India 10-year government bond yield' data")
        return None
    
    try:
        yield_data = pd.read_csv(filepath, index_col=0, parse_dates=True)
        return yield_data
    except Exception as e:
        print(f"Error loading yield data: {e}")
        return None

def extract_money_stock(table6_data):
    """Extract M3 from Table 6"""
    components = {}
    
    # Look for M3 column
    if 'M3' in table6_data.columns:
        components['M3'] = table6_data['M3']
        print(f"✓ Found M3 with {len(table6_data['M3'].dropna())} data points")
    
    # Look for M3 (Excluding Merger) as backup
    if 'M3 (Excluding Merger)' in table6_data.columns:
        components['M3_excl_merger'] = table6_data['M3 (Excluding Merger)']
    
    return components

def normalize_series(series):
    """Normalize a series to start at 100 for comparison"""
    if series is None or len(series) == 0:
        return None
    
    # Remove NaN values and get first valid value
    series_clean = series.dropna()
    if len(series_clean) == 0:
        return None
    
    first_value = series_clean.iloc[0]
    if first_value == 0 or pd.isna(first_value):
        return None
    
    return (series / first_value) * 100

def plot_money_stock(money_components, yields=None):
    """Plot money stock components with optional treasury yields"""
    
    if yields is not None and '10_year_gsec' in yields:
        # Create figure with 2 subplots if yields available
        fig, axes = plt.subplots(2, 1, figsize=(18, 10))
        
        # Plot 1: M3 with 10-Year G-Sec Yield
        ax1 = axes[0]
        
        if 'M3' in money_components:
            m3_normalized = normalize_series(money_components['M3'])
            if m3_normalized is not None:
                ax1_twin = ax1.twinx()
                ax1.plot(m3_normalized.index, m3_normalized.values,
                        label='M3 (Broad Money)', linewidth=2.5, color='red')
                ax1.set_ylabel('M3 Index (Base = 100)', fontsize=12, color='red', fontweight='bold')
                ax1.tick_params(axis='y', labelcolor='red')
                
                ax1_twin.plot(yields['10_year_gsec'].index, yields['10_year_gsec'].values,
                             label='10-Year G-Sec Yield', linewidth=2.5, 
                             color='darkgreen', linestyle='--')
                ax1_twin.set_ylabel('10-Year G-Sec Yield (%)', fontsize=12, 
                                   color='darkgreen', fontweight='bold')
                ax1_twin.tick_params(axis='y', labelcolor='darkgreen')
                
                ax1.set_title('M3 Money Stock vs 10-Year G-Sec Yield', 
                             fontsize=15, fontweight='bold', pad=20)
                ax1.set_xlabel('Date', fontsize=12)
                ax1.grid(True, alpha=0.3)
                
                # Combine legends
                lines1, labels1 = ax1.get_legend_handles_labels()
                lines2, labels2 = ax1_twin.get_legend_handles_labels()
                ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=11)
        
        # Plot 2: 10-Year G-Sec Yield separately
        ax2 = axes[1]
        ax2.plot(yields['10_year_gsec'].index, yields['10_year_gsec'].values,
                label='10-Year G-Sec Yield', linewidth=2.5, color='darkgreen')
        ax2.fill_between(yields['10_year_gsec'].index, yields['10_year_gsec'].values, 
                         alpha=0.3, color='darkgreen')
        ax2.set_title('10-Year G-Sec Yield Trend', fontsize=15, fontweight='bold', pad=20)
        ax2.set_xlabel('Date', fontsize=12)
        ax2.set_ylabel('Yield (%)', fontsize=12, fontweight='bold')
        ax2.legend(fontsize=11, loc='upper left')
        ax2.grid(True, alpha=0.3)
        
    else:
        # Create single plot for M3 only
        fig, ax = plt.subplots(1, 1, figsize=(18, 8))
        
        if 'M3' in money_components:
            # Plot absolute values
            m3_data = money_components['M3'].dropna()
            ax.plot(m3_data.index, m3_data.values / 100000,  # Convert to lakhs
                   label='M3 (Broad Money)', linewidth=2.5, color='red')
            ax.fill_between(m3_data.index, m3_data.values / 100000, alpha=0.2, color='red')
            
            ax.set_title('M3 Money Stock - India (RBI Data)', 
                        fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Date', fontsize=13)
            ax.set_ylabel('M3 (₹ Lakh Crore)', fontsize=13, fontweight='bold')
            ax.legend(fontsize=12, loc='upper left')
            ax.grid(True, alpha=0.3)
            
            # Add secondary axis with normalized values
            ax2 = ax.twinx()
            m3_normalized = normalize_series(money_components['M3'])
            ax2.plot(m3_normalized.index, m3_normalized.values,
                    label='M3 Normalized (Base = 100)', linewidth=2, 
                    color='blue', linestyle='--', alpha=0.7)
            ax2.set_ylabel('Index (Base = 100)', fontsize=13, color='blue', fontweight='bold')
            ax2.tick_params(axis='y', labelcolor='blue')
            
            # Combine legends
            lines1, labels1 = ax.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=11)
    
    plt.tight_layout()
    plt.savefig('money_stock_analysis.png', dpi=300, bbox_inches='tight')
    print("\n✓ Plot saved as 'money_stock_analysis.png'")
    
    return fig

def create_summary_statistics(money_components):
    """Create summary statistics for M3"""
    stats = {}
    
    if 'M3' in money_components:
        m3 = money_components['M3'].dropna()
        
        stats['Latest M3 (₹ Lakh Crore)'] = m3.iloc[0] / 100000
        stats['Earliest M3 (₹ Lakh Crore)'] = m3.iloc[-1] / 100000
        stats['Total Growth (₹ Lakh Crore)'] = (m3.iloc[0] - m3.iloc[-1]) / 100000
        stats['Growth Rate (%)'] = ((m3.iloc[0] / m3.iloc[-1]) - 1) * 100
        stats['Latest Date'] = m3.index[0].strftime('%Y-%m-%d')
        stats['Earliest Date'] = m3.index[-1].strftime('%Y-%m-%d')
        stats['Number of Observations'] = len(m3)
        
    return stats

def main():
    print("=" * 80)
    print("RBI Money Stock Analysis - M3 Trends")
    print("=" * 80)
    
    # File paths
    table6_path = 'rbi_money_stock.csv'
    
    print("\nLoading RBI Table 6 (Money Stock)...")
    table6_data = load_rbi_table6(table6_path)
    
    if table6_data is None:
        print("\nERROR: Could not load money stock data")
        return
    
    print(f"✓ Loaded data with {len(table6_data)} rows")
    print(f"  Date range: {table6_data.index[-1]} to {table6_data.index[0]}")
    
    print("\nExtracting money stock components...")
    money_components = extract_money_stock(table6_data)
    
    if not money_components:
        print("\nERROR: Could not extract M3 data")
        return
    
    # Try to load yield data (optional)
    yields = load_yield_data()  # Will print message about where to get data
    
    # Create plots
    print("\nCreating plots...")
    plot_money_stock(money_components, yields)
    
    # Calculate statistics
    print("\nCalculating summary statistics...")
    stats = create_summary_statistics(money_components)
    
    # Save comprehensive analysis
    print("\nSaving analysis to Excel...")
    with pd.ExcelWriter('rbi_money_stock_analysis.xlsx', 
                        engine='openpyxl') as writer:
        # Save M3 data
        if 'M3' in money_components:
            m3_df = pd.DataFrame({
                'M3 (₹ Crore)': money_components['M3'],
                'M3 (₹ Lakh Crore)': money_components['M3'] / 100000
            })
            m3_df.to_excel(writer, sheet_name='M3 Data', index=True)
        
        # Save statistics
        stats_df = pd.DataFrame([stats]).T
        stats_df.columns = ['Value']
        stats_df.to_excel(writer, sheet_name='Summary Statistics', index=True)
        
        # Analysis notes
        analysis = """
RELATIONSHIP BETWEEN MONEY STOCK AND 10-YEAR G-SEC YIELD:

ABOUT M3 (BROAD MONEY):
- M3 includes: Currency with public + Demand deposits + Time deposits + Other deposits
- M3 is the most comprehensive measure of money supply in India
- RBI monitors M3 growth as a key indicator of liquidity and monetary policy effectiveness

EXPECTED RELATIONSHIPS WITH 10-YEAR G-SEC YIELD:

1. MONEY STOCK GROWTH vs LONG-TERM YIELDS:
   - Higher money supply → Lower interest rates (liquidity effect)
   - But can also lead to inflation expectations → Higher yields
   - Long-term yields reflect market expectations of future inflation

2. 10-YEAR G-SEC YIELD SIGNIFICANCE:
   - Reflects long-term inflation expectations
   - Affected by fiscal policy and government borrowing programs
   - More stable than short-term rates
   - Benchmark for corporate bond yields and loan pricing

3. M3 GROWTH IMPLICATIONS:
   - High M3 growth → Potential inflation → Higher long-term yields
   - RBI uses M3 growth as a key monetary indicator
   - Rapid expansion may signal loose monetary policy
   - Contraction may indicate tight monetary conditions

4. POLICY IMPLICATIONS:
   - Rapid M3 expansion with stable/falling yields → Accommodative policy working
   - Rising M3 with rising yields → Inflation concerns or fiscal dominance
   - Stable M3 with rising yields → External factors or risk premium increase

INTERPRETATION GUIDE:
- If M3 grows faster than yields increase → Expansionary monetary policy effective
- If yields rise faster than M3 → Tightening policy or inflation concerns
- Negative correlation suggests liquidity effect dominates
- Positive correlation suggests inflation expectations dominate
- Divergence indicates changing market expectations or policy shifts

HOW TO ADD 10-YEAR G-SEC YIELD DATA:
1. Download yield data from RBI Database or financial data providers
2. Format as CSV with Date and Yield columns
3. Update the script to load your yield data file
4. The script will automatically create combined plots

DATA SOURCES:
- RBI Database: https://dbie.rbi.org.in/DBIE/dbie.rbi?site=publications
- Look for "Government Securities Market" or "Interest Rates" sections
        """
        analysis_df = pd.DataFrame({'Analysis': [analysis]})
        analysis_df.to_excel(writer, sheet_name='Analysis Notes', index=False)
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print("\nOutput files saved:")
    print("  1. money_stock_analysis.png - Visualization")
    print("  2. rbi_money_stock_analysis.xlsx - Detailed data and statistics")
    
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:,.2f}")
        else:
            print(f"  {key}: {value}")
    
    print("\n" + "=" * 80)
    print("NOTE: To include 10-year G-sec yield analysis:")
    print("  - Download yield data from RBI or other sources")
    print("  - The script will automatically create combined visualizations")
    print("=" * 80)

if __name__ == "__main__":
    main()