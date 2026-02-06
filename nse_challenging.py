"""
Assignment 1 - Part 1 (Challenging): Download all NSE indices and compare returns
Compares NIFTY 50, NIFTY 100, and NIFTY 500 returns for last 3 years
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

def download_nifty_index(index_name, years=3):
    """Download historical data for specific NIFTY indices"""
    try:
        import yfinance as yf
        # Map NSE indices to Yahoo Finance symbols
        # Try multiple symbol variations for NIFTY 500
        symbol_map = {
            'NIFTY 50': ['^NSEI'],
            'NIFTY 100': ['^CNX100'],
            'NIFTY 500': ['NIFTY500.NS', '^NSE500', 'NIFTY500.BO']  # Try multiple symbols
        }
        
        symbols = symbol_map.get(index_name)
        if not symbols:
            print(f"Symbol mapping not found for {index_name}")
            return None
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=years*365)
        
        # Try each symbol until one works
        data = pd.DataFrame()
        for symbol in symbols:
            try:
                print(f"  Trying symbol: {symbol}")
                ticker = yf.Ticker(symbol)
                data = ticker.history(start=start_date, end=end_date)
                
                if data.empty:
                    # Try with period parameter
                    data = ticker.history(period=f"{years}y")
                
                if not data.empty:
                    print(f"  ✓ Successfully downloaded using {symbol}")
                    break
            except Exception as e:
                print(f"  ✗ Failed with {symbol}: {str(e)[:50]}")
                continue
        
        if data.empty:
            print(f"  Error: All symbol variations failed for {index_name}")
            print(f"  Note: NIFTY 500 may not be available on Yahoo Finance.")
            print(f"  Please download manually from: https://www.niftyindices.com/reports/historical-data")
            return None
        
        return data
    except ImportError:
        print("yfinance not installed. Installing...")
        import subprocess
        subprocess.check_call(['pip', 'install', 'yfinance'])
        return download_nifty_index(index_name, years)

def calculate_daily_returns(data):
    """Calculate daily returns"""
    return data['Close'].pct_change().dropna()

def calculate_cumulative_returns(returns):
    """Calculate cumulative returns"""
    return (1 + returns).cumprod() - 1

def plot_returns_comparison(nifty50_data, nifty100_data, nifty500_data):
    """Plot and compare returns of NIFTY 50, 100, and 500"""
    
    # Calculate returns
    nifty50_returns = calculate_daily_returns(nifty50_data)
    nifty100_returns = calculate_daily_returns(nifty100_data)
    nifty500_returns = calculate_daily_returns(nifty500_data)
    
    # Calculate cumulative returns
    nifty50_cumret = calculate_cumulative_returns(nifty50_returns)
    nifty100_cumret = calculate_cumulative_returns(nifty100_returns)
    nifty500_cumret = calculate_cumulative_returns(nifty500_returns)
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 1, figsize=(16, 10))
    
    # Plot 1: Daily Returns Comparison
    axes[0].plot(nifty50_returns.index, nifty50_returns * 100, 
                 label='NIFTY 50', alpha=0.7, linewidth=1)
    axes[0].plot(nifty100_returns.index, nifty100_returns * 100, 
                 label='NIFTY 100', alpha=0.7, linewidth=1)
    axes[0].plot(nifty500_returns.index, nifty500_returns * 100, 
                 label='NIFTY 500', alpha=0.7, linewidth=1)
    axes[0].set_title('Daily Returns Comparison - Last 3 Years', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Date', fontsize=12)
    axes[0].set_ylabel('Daily Returns (%)', fontsize=12)
    axes[0].legend(fontsize=11)
    axes[0].grid(True, alpha=0.3)
    axes[0].axhline(y=0, color='black', linestyle='--', linewidth=0.8)
    
    # Plot 2: Cumulative Returns Comparison
    axes[1].plot(nifty50_cumret.index, nifty50_cumret * 100, 
                 label='NIFTY 50', linewidth=2)
    axes[1].plot(nifty100_cumret.index, nifty100_cumret * 100, 
                 label='NIFTY 100', linewidth=2)
    axes[1].plot(nifty500_cumret.index, nifty500_cumret * 100, 
                 label='NIFTY 500', linewidth=2)
    axes[1].set_title('Cumulative Returns Comparison - Last 3 Years', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Date', fontsize=12)
    axes[1].set_ylabel('Cumulative Returns (%)', fontsize=12)
    axes[1].legend(fontsize=11)
    axes[1].grid(True, alpha=0.3)
    axes[1].axhline(y=0, color='black', linestyle='--', linewidth=0.8)
    
    plt.tight_layout()
    plt.savefig('nifty_returns_comparison.png', dpi=300, bbox_inches='tight')
    print("Returns comparison plot saved as 'nifty_returns_comparison.png'")
    
    # Calculate statistics
    stats = {
        'Index': ['NIFTY 50', 'NIFTY 100', 'NIFTY 500'],
        '3-Year Total Return (%)': [
            nifty50_cumret.iloc[-1] * 100,
            nifty100_cumret.iloc[-1] * 100,
            nifty500_cumret.iloc[-1] * 100
        ],
        'Annualized Return (%)': [
            ((1 + nifty50_cumret.iloc[-1]) ** (252 / len(nifty50_returns)) - 1) * 100,
            ((1 + nifty100_cumret.iloc[-1]) ** (252 / len(nifty100_returns)) - 1) * 100,
            ((1 + nifty500_cumret.iloc[-1]) ** (252 / len(nifty500_returns)) - 1) * 100
        ],
        'Volatility (%)': [
            nifty50_returns.std() * np.sqrt(252) * 100,
            nifty100_returns.std() * np.sqrt(252) * 100,
            nifty500_returns.std() * np.sqrt(252) * 100
        ],
        'Sharpe Ratio (assume 5% risk-free)': [
            ((nifty50_returns.mean() * 252 - 0.05) / (nifty50_returns.std() * np.sqrt(252))),
            ((nifty100_returns.mean() * 252 - 0.05) / (nifty100_returns.std() * np.sqrt(252))),
            ((nifty500_returns.mean() * 252 - 0.05) / (nifty500_returns.std() * np.sqrt(252)))
        ]
    }
    
    stats_df = pd.DataFrame(stats)
    print("\n" + "=" * 80)
    print("RETURNS COMPARISON STATISTICS (Last 3 Years)")
    print("=" * 80)
    print(stats_df.to_string(index=False))
    
    # Save to Excel
    # Align returns to common dates (all three indices must have data for the same dates)
    common_dates = nifty50_returns.index.intersection(nifty100_returns.index).intersection(nifty500_returns.index)
    
    if len(common_dates) == 0:
        print("Warning: No common dates found between all indices. Using intersection of available dates.")
        # Use intersection of all three
        common_dates = nifty50_returns.index.intersection(nifty100_returns.index)
        if len(common_dates) > 0:
            common_dates = common_dates.intersection(nifty500_returns.index)
    
    if len(common_dates) > 0:
        nifty50_aligned = nifty50_returns.loc[common_dates]
        nifty100_aligned = nifty100_returns.loc[common_dates]
        nifty500_aligned = nifty500_returns.loc[common_dates]
    else:
        # Fallback: use the shortest series and reindex others
        min_len = min(len(nifty50_returns), len(nifty100_returns), len(nifty500_returns))
        if len(nifty50_returns) == min_len:
            base_index = nifty50_returns.index
        elif len(nifty100_returns) == min_len:
            base_index = nifty100_returns.index
        else:
            base_index = nifty500_returns.index
        
        nifty50_aligned = nifty50_returns.reindex(base_index, fill_value=np.nan)
        nifty100_aligned = nifty100_returns.reindex(base_index, fill_value=np.nan)
        nifty500_aligned = nifty500_returns.reindex(base_index, fill_value=np.nan)
        common_dates = base_index
    
    # Remove timezone information if present (Excel doesn't support timezone-aware datetimes)
    returns_dates = common_dates
    if returns_dates.tz is not None:
        returns_dates = pd.DatetimeIndex(returns_dates.values)
    
    with pd.ExcelWriter('nifty_returns_analysis.xlsx', engine='openpyxl') as writer:
        stats_df.to_excel(writer, sheet_name='Statistics', index=False)
        pd.DataFrame({
            'Date': returns_dates,
            'NIFTY 50 Returns': nifty50_aligned.values,
            'NIFTY 100 Returns': nifty100_aligned.values,
            'NIFTY 500 Returns': nifty500_aligned.values
        }).to_excel(writer, sheet_name='Daily Returns', index=False)
    
    print("\nData saved to 'nifty_returns_analysis.xlsx'")
    
    return fig, stats_df

def main():
    print("=" * 80)
    print("NSE Indices Returns Comparison - Challenging Problem")
    print("=" * 80)
    
    indices = ['NIFTY 50', 'NIFTY 100', 'NIFTY 500']
    data_dict = {}
    
    for index_name in indices:
        print(f"\nDownloading {index_name} data (last 3 years)...")
        data = download_nifty_index(index_name, years=3)
        if data is not None:
            data_dict[index_name] = data
            print(f"✓ Successfully downloaded {len(data)} days of data")
        else:
            print(f"✗ Failed to download {index_name} data")
    
    if len(data_dict) < 2:
        print("\nError: Could not download at least 2 required indices.")
        print("Please check your internet connection and try again.")
        return
    
    # If NIFTY 500 is missing, proceed with available indices
    if 'NIFTY 500' not in data_dict:
        print("\nWarning: NIFTY 500 data not available. Proceeding with NIFTY 50 and NIFTY 100.")
        print("Note: NIFTY 500 may not be available on Yahoo Finance.")
        print("You can download it manually from: https://www.niftyindices.com/reports/historical-data")
        
        if 'NIFTY 50' in data_dict and 'NIFTY 100' in data_dict:
            # Create a modified comparison with just 2 indices
            print("\nCreating comparison with NIFTY 50 and NIFTY 100...")
            # We'll need to modify the plot function to handle 2 indices
            # For now, let's create a simple comparison
            nifty50_returns = calculate_daily_returns(data_dict['NIFTY 50'])
            nifty100_returns = calculate_daily_returns(data_dict['NIFTY 100'])
            
            # Create a simple comparison plot
            fig, axes = plt.subplots(2, 1, figsize=(16, 10))
            
            # Daily returns
            axes[0].plot(nifty50_returns.index, nifty50_returns * 100, 
                        label='NIFTY 50', alpha=0.7, linewidth=1)
            axes[0].plot(nifty100_returns.index, nifty100_returns * 100, 
                        label='NIFTY 100', alpha=0.7, linewidth=1)
            axes[0].set_title('Daily Returns Comparison - Last 3 Years', fontsize=14, fontweight='bold')
            axes[0].set_xlabel('Date', fontsize=12)
            axes[0].set_ylabel('Daily Returns (%)', fontsize=12)
            axes[0].legend(fontsize=11)
            axes[0].grid(True, alpha=0.3)
            axes[0].axhline(y=0, color='black', linestyle='--', linewidth=0.8)
            
            # Cumulative returns
            nifty50_cumret = (1 + nifty50_returns).cumprod() - 1
            nifty100_cumret = (1 + nifty100_returns).cumprod() - 1
            
            axes[1].plot(nifty50_cumret.index, nifty50_cumret * 100, 
                        label='NIFTY 50', linewidth=2)
            axes[1].plot(nifty100_cumret.index, nifty100_cumret * 100, 
                        label='NIFTY 100', linewidth=2)
            axes[1].set_title('Cumulative Returns Comparison - Last 3 Years', fontsize=14, fontweight='bold')
            axes[1].set_xlabel('Date', fontsize=12)
            axes[1].set_ylabel('Cumulative Returns (%)', fontsize=12)
            axes[1].legend(fontsize=11)
            axes[1].grid(True, alpha=0.3)
            axes[1].axhline(y=0, color='black', linestyle='--', linewidth=0.8)
            
            plt.tight_layout()
            plt.savefig('nifty_returns_comparison.png', dpi=300, bbox_inches='tight')
            print("Returns comparison plot saved as 'nifty_returns_comparison.png'")
            
            # Save statistics
            stats = {
                'Index': ['NIFTY 50', 'NIFTY 100'],
                '3-Year Total Return (%)': [
                    nifty50_cumret.iloc[-1] * 100,
                    nifty100_cumret.iloc[-1] * 100
                ],
                'Annualized Return (%)': [
                    ((1 + nifty50_cumret.iloc[-1]) ** (252 / len(nifty50_returns)) - 1) * 100,
                    ((1 + nifty100_cumret.iloc[-1]) ** (252 / len(nifty100_returns)) - 1) * 100
                ],
                'Volatility (%)': [
                    nifty50_returns.std() * np.sqrt(252) * 100,
                    nifty100_returns.std() * np.sqrt(252) * 100
                ]
            }
            stats_df = pd.DataFrame(stats)
            print("\n" + "=" * 80)
            print("RETURNS COMPARISON STATISTICS (Last 3 Years)")
            print("=" * 80)
            print(stats_df.to_string(index=False))
            
            # Save to Excel
            # Align returns to common dates
            common_dates = nifty50_returns.index.intersection(nifty100_returns.index)
            
            if len(common_dates) == 0:
                print("Warning: No common dates found between indices. Using individual date ranges.")
                # Use the shorter series as base
                if len(nifty50_returns) <= len(nifty100_returns):
                    common_dates = nifty50_returns.index
                    nifty50_aligned = nifty50_returns
                    nifty100_aligned = nifty100_returns.reindex(nifty50_returns.index, fill_value=np.nan)
                else:
                    common_dates = nifty100_returns.index
                    nifty50_aligned = nifty50_returns.reindex(nifty100_returns.index, fill_value=np.nan)
                    nifty100_aligned = nifty100_returns
            else:
                nifty50_aligned = nifty50_returns.loc[common_dates]
                nifty100_aligned = nifty100_returns.loc[common_dates]
            
            # Remove timezone if present
            returns_dates = common_dates
            if returns_dates.tz is not None:
                returns_dates = pd.DatetimeIndex(returns_dates.values)
            
            with pd.ExcelWriter('nifty_returns_analysis.xlsx', engine='openpyxl') as writer:
                stats_df.to_excel(writer, sheet_name='Statistics', index=False)
                pd.DataFrame({
                    'Date': returns_dates,
                    'NIFTY 50 Returns': nifty50_aligned.values,
                    'NIFTY 100 Returns': nifty100_aligned.values
                }).to_excel(writer, sheet_name='Daily Returns', index=False)
            
            print("\nData saved to 'nifty_returns_analysis.xlsx'")
            return
    
    # Plot comparison with all 3 indices
    plot_returns_comparison(
        data_dict['NIFTY 50'],
        data_dict['NIFTY 100'],
        data_dict['NIFTY 500']
    )
    
    print("\n" + "=" * 80)
    print("Analysis complete!")
    print("=" * 80)
    print("\nKey Observations:")
    print("- NIFTY 500 (broadest index) typically shows higher volatility")
    print("- NIFTY 50 (large cap) tends to be more stable")
    print("- Returns correlation is high due to overlapping constituents")
    print("- Check the plots for detailed visual comparison")

if __name__ == "__main__":
    main()
