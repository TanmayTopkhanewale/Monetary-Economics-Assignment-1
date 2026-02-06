"""
Assignment 1 - Part 2: INR/USD Exchange Rate Analysis
Downloads data from FRED and analyzes biggest monthly jumps
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def download_fred_data(series_id='CCUSMA02INM618N'):
    """
    Download INR/USD exchange rate data from FRED
    Series: CCUSMA02INM618N - Indian Rupee to U.S. Dollar Spot Exchange Rate
    """
    try:
        import fredapi
        from fredapi import Fred
        
        try:
            from fredapi import Fred
            import os
            api_key = "2cfb19b1c2dbf27ec1a7831223f74a6a"
            
            fred = Fred(api_key=api_key)
            data = fred.get_series(series_id)
            data = pd.DataFrame(data, columns=['Rate'])
            data.index.name = 'Date'
            return data
        except:
            # Alternative: Use pandas_datareader
            try:
                import pandas_datareader.data as web
                from datetime import datetime
                start = datetime(1970, 1, 1)
                end = datetime.now()
                data = web.DataReader(series_id, 'fred', start, end)
                return data
            except:
                print("\nCould not download automatically. Please download manually from:")
                print("https://fred.stlouisfed.org/series/CCUSMA02INM618N")
                print("Save as CSV and update the code to read from file.")
                return None
    except ImportError:
        print("Required packages not installed. Installing...")
        import subprocess
        try:
            subprocess.check_call(['pip', 'install', 'fredapi', 'pandas-datareader'])
            return download_fred_data(series_id)
        except:
            print("Please install manually: pip install fredapi pandas-datareader")
            return None

def load_data_from_file(filepath='CCUSMA02INM618N.csv'):
    """Load data from manually downloaded CSV file"""
    try:
        data = pd.read_csv(filepath, index_col=0, parse_dates=True)
        return data
    except FileNotFoundError:
        print(f"File {filepath} not found.")
        return None

def calculate_monthly_changes(data):
    """Calculate month-over-month percentage changes"""
    monthly_pct_change = data.pct_change() * 100
    return monthly_pct_change.dropna()

def find_biggest_jumps(data, n=5):
    """Find the n biggest single month jumps (positive changes)"""
    monthly_changes = calculate_monthly_changes(data)
    
    # Convert to Series if DataFrame (take first column)
    if isinstance(monthly_changes, pd.DataFrame):
        if len(monthly_changes.columns) > 0:
            monthly_changes = monthly_changes.iloc[:, 0]
        else:
            return pd.Series(dtype=float)
    
    # Get biggest positive changes (INR depreciation)
    biggest_jumps = monthly_changes.nlargest(n)
    
    return biggest_jumps

def get_historical_context(date):
    """Provide historical context for significant dates"""
    # This is a simplified version - you should research actual events
    context_map = {
        # Add specific dates and events here
    }
    return context_map.get(date.strftime('%Y-%m'), "Research historical events for this period")

def plot_exchange_rate(data, save_path='inr_usd_analysis.xlsx'):
    """Simple INR/USD exchange rate plots"""
    
    monthly_changes = calculate_monthly_changes(data)
    biggest_jumps = find_biggest_jumps(data, n=5)
    
    # Create figure with larger middle section for monthly changes
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 2, height_ratios=[1, 1.5, 1], hspace=0.3, wspace=0.3)
    
    # ============ Plot 1: Exchange Rate ============
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(data.index, data.iloc[:, 0], linewidth=2, color='steelblue')
    
    # Mark biggest jumps
    for date in biggest_jumps.index:
        if date in data.index:
            ax1.axvline(x=date, color='red', linestyle='--', alpha=0.5)
    
    ax1.set_title('INR/USD Exchange Rate', fontsize=14, fontweight='bold')
    ax1.set_ylabel('₹ per $', fontsize=12)
    ax1.grid(True, alpha=0.3)
    
    # ============ Plot 2: MAGNIFIED Monthly Changes ============
    ax2 = fig.add_subplot(gs[1, :])
    colors = ['green' if x < 0 else 'red' for x in monthly_changes.iloc[:, 0]]
    ax2.bar(monthly_changes.index, monthly_changes.iloc[:, 0], 
            width=15, color=colors, alpha=0.7, edgecolor='black', linewidth=0.5)
    
    # Highlight biggest jumps with markers
    for date, value in biggest_jumps.items():
        ax2.scatter(date, value, s=250, color='gold', 
                   edgecolor='black', linewidth=2, zorder=5, marker='*')
        ax2.text(date, value + (0.3 if value > 0 else -0.3), 
                f'{value:.2f}%', ha='center', fontsize=10, 
                fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', 
                facecolor='yellow', alpha=0.7))
    
    ax2.axhline(y=0, color='black', linewidth=1.5)
    ax2.set_title('Monthly % Changes (MAGNIFIED)', fontsize=15, fontweight='bold', pad=15)
    ax2.set_xlabel('Date', fontsize=12)
    ax2.set_ylabel('Change (%)', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # ============ Plot 3: Distribution ============
    ax3 = fig.add_subplot(gs[2, 0])
    ax3.hist(monthly_changes.iloc[:, 0].dropna(), bins=20, 
            color='purple', alpha=0.6, edgecolor='black')
    ax3.axvline(monthly_changes.iloc[:, 0].mean(), 
               color='red', linestyle='--', linewidth=2, 
               label=f'Mean: {monthly_changes.iloc[:, 0].mean():.2f}%')
    ax3.set_title('Change Distribution', fontsize=13, fontweight='bold')
    ax3.set_xlabel('Monthly Change (%)', fontsize=11)
    ax3.set_ylabel('Frequency', fontsize=11)
    ax3.legend(fontsize=10)
    ax3.grid(True, alpha=0.3)
    
    # ============ Plot 4: Top Volatility Events ============
    ax4 = fig.add_subplot(gs[2, 1])
    ax4.axis('off')
    
    # Simple text display
    y_start = 0.95
    ax4.text(0.5, y_start, 'Top 5 Volatility Events', 
            ha='center', fontsize=13, fontweight='bold',
            transform=ax4.transAxes)
    
    y_pos = y_start - 0.15
    for idx, (date, value) in enumerate(biggest_jumps.items(), 1):
        arrow = '↑' if value > 0 else '↓'
        color = 'red' if value > 0 else 'green'
        text = f"{idx}. {date.strftime('%b %Y')}: {arrow} {abs(value):.2f}%"
        ax4.text(0.1, y_pos, text, fontsize=11, color=color,
                transform=ax4.transAxes, fontweight='bold')
        y_pos -= 0.15
    
    # Add summary stats
    y_pos -= 0.05
    ax4.text(0.1, y_pos, f"Current: ₹{data.iloc[0, 0]:.2f}", 
            fontsize=10, transform=ax4.transAxes, fontweight='600')
    ax4.text(0.1, y_pos - 0.08, f"Average: ₹{data.iloc[:, 0].mean():.2f}", 
            fontsize=10, transform=ax4.transAxes, fontweight='600')
    ax4.text(0.1, y_pos - 0.16, f"Peak: ₹{data.iloc[:, 0].max():.2f}", 
            fontsize=10, transform=ax4.transAxes, fontweight='600')
    ax4.text(0.1, y_pos - 0.24, f"Low: ₹{data.iloc[:, 0].min():.2f}", 
            fontsize=10, transform=ax4.transAxes, fontweight='600')
    
    plt.suptitle('INR/USD Exchange Rate Analysis', 
                fontsize=16, fontweight='bold', y=0.995)
    
    plt.savefig('inr_usd_plots.png', dpi=300, bbox_inches='tight')
    print("✓ Plots saved as 'inr_usd_plots.png'")
    
    return fig
def main():
    print("=" * 80)
    print("INR/USD Exchange Rate Analysis - Assignment 1, Part 2")
    print("=" * 80)
    
    # Try to download data
    data = download_fred_data()
    
    # If download fails, try to load from file
    if data is None or data.empty:
        print("\nTrying to load from local file...")
        data = load_data_from_file()
    
    if data is None or data.empty:
        print("\n" + "=" * 80)
        print("ERROR: Could not load data.")
        print("=" * 80)
        print("\nPlease download the data manually:")
        print("1. Go to: https://fred.stlouisfed.org/series/CCUSMA02INM618N")
        print("2. Click 'Download' -> 'CSV'")
        print("3. Save as 'CCUSMA02INM618N.csv' in the same directory")
        print("4. Run this script again")
        return
    
    print(f"\n✓ Successfully loaded {len(data)} months of data")
    print(f"  Date range: {data.index.min()} to {data.index.max()}")
    
    # Calculate monthly changes
    monthly_changes = calculate_monthly_changes(data)
    
    # Find biggest jumps (positive = INR depreciation)
    biggest_jumps = find_biggest_jumps(data, n=5)
    
    print("\n" + "=" * 80)
    print("FIVE BIGGEST SINGLE MONTH JUMPS (INR Depreciation)")
    print("=" * 80)
    
    jump_data = []
    for date, change in biggest_jumps.items():
        change_value = change  # Now it's a scalar value from Series
        # Get exchange rate for this date
        if date in data.index:
            if isinstance(data.loc[date], pd.Series):
                rate_value = data.loc[date].iloc[0]
            else:
                rate_value = data.loc[date]
        else:
            rate_value = None
        
        jump_data.append({
            'Date': date.strftime('%Y-%m'),
            'Monthly Change (%)': f"{change_value:.2f}",
            'Exchange Rate (INR/USD)': f"{rate_value:.2f}" if rate_value is not None else "N/A"
        })
        print(f"\n{date.strftime('%Y-%m')}: {change_value:.2f}% increase")
        print(f"  Exchange Rate: {rate_value:.2f} INR/USD" if rate_value is not None else "")
    
    # Create plots
    plot_exchange_rate(data)
    
    # Save to Excel
    # Remove timezone information if present (Excel doesn't support timezone-aware datetimes)
    data_export = data.copy()
    monthly_changes_export = monthly_changes.copy()
    
    if data_export.index.tz is not None:
        data_export.index = pd.DatetimeIndex(data_export.index.values)
    if monthly_changes_export.index.tz is not None:
        monthly_changes_export.index = pd.DatetimeIndex(monthly_changes_export.index.values)
    
    with pd.ExcelWriter('inr_usd_analysis.xlsx', engine='openpyxl') as writer:
        data_export.to_excel(writer, sheet_name='Exchange Rate Data', index=True)
        monthly_changes_export.to_excel(writer, sheet_name='Monthly Changes', index=True)
        pd.DataFrame(jump_data).to_excel(writer, sheet_name='Biggest Jumps', index=False)
        
        # Add analysis sheet
        analysis_text = """
        ANALYSIS OF BIGGEST JUMPS:
        
        Note: Positive percentage change means INR depreciated (weaker) against USD.
        
        HISTORICAL EVENTS ASSOCIATION:
        (Research and fill in based on the dates found above)
        
        Common causes of INR depreciation:
        1. US Federal Reserve interest rate hikes
        2. Global risk-off sentiment (flight to safety)
        3. High oil prices (India imports oil)
        4. Current account deficit concerns
        5. Foreign capital outflows
        6. Domestic economic/political uncertainty
        
        IS DROP IN INR GOOD FOR INDIAN HOUSEHOLDS?
        
        Mixed Impact:
        
        NEGATIVE EFFECTS:
        - Imported goods become more expensive (electronics, fuel, etc.)
        - Foreign travel becomes costlier
        - Education abroad becomes more expensive
        - Inflationary pressure on imported goods
        
        POSITIVE EFFECTS:
        - Exporters benefit (IT services, textiles, etc.)
        - Remittances from abroad worth more in INR
        - Tourism industry benefits (cheaper for foreigners)
        - Export-oriented industries create jobs
        
        NET EFFECT:
        - Generally negative for most households due to:
          * Higher fuel prices (affects everything)
          * Higher prices of imported consumer goods
          * Inflationary impact on overall cost of living
        - Benefits are concentrated in export sectors and remittance-receiving families
        """
        
        analysis_df = pd.DataFrame({'Analysis': [analysis_text]})
        analysis_df.to_excel(writer, sheet_name='Analysis', index=False)
    
    print("\n" + "=" * 80)
    print("Analysis saved to 'inr_usd_analysis.xlsx'")
    print("=" * 80)
    print("\nNext Steps:")
    print("1. Research historical events for the dates identified above")
    print("2. Common periods to check:")
    print("   - 2008 Financial Crisis")
    print("   - 2013 Taper Tantrum")
    print("   - 2018 US-China Trade War")
    print("   - 2020 COVID-19 pandemic")
    print("   - 2022 Fed rate hikes")
    print("3. Update the analysis sheet with specific events")

if __name__ == "__main__":
    main()
