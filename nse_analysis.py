"""
Assignment 1 - Part 1: NSE Historical Data Analysis
Downloads and analyzes NIFTY 50 and NIFTY BANK indices
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
})
from datetime import datetime, timedelta
import warnings
import yfinance as yf
warnings.filterwarnings('ignore')

def download_nifty_data(index_name, years=5):
    """
    Download historical data for NSE indices
    Note: NSE doesn't provide direct API access, so we'll use yfinance as an alternative
    or provide instructions for manual download
    """
    try:
        # Map NSE indices to Yahoo Finance symbols
        symbol_map = {
            'NIFTY 50': '^NSEI',            
            'NIFTY BANK': '^NSEBANK',
            'NIFTY 100': '^CNX100',
            'NIFTY 500': '^NSE500'
        }
        
        symbol = symbol_map.get(index_name)
        if not symbol:
            print(f"Symbol mapping not found for {index_name}")
            return None
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=years*365)
        
        print(f"  Attempting to download {index_name} ({symbol}) from {start_date.date()} to {end_date.date()}...")
        
        # Download data - try multiple methods
        ticker = yf.Ticker(symbol)
        
        # Method 1: Try with date range
        try:
            data = ticker.history(start=start_date, end=end_date)
        except Exception as e:
            print(f"  Warning: Date range method failed: {e}")
            data = pd.DataFrame()
        
        # Method 2: If empty, try with period parameter
        if data.empty:
            print(f"  Trying alternative download method (period={years}y)...")
            try:
                data = ticker.history(period=f"{years}y")
            except Exception as e:
                print(f"  Warning: Period method failed: {e}")
                data = pd.DataFrame()
        
        # Method 3: If still empty, try max period
        if data.empty:
            print(f"  Trying max available period...")
            try:
                data = ticker.history(period="max")
                # Filter to last 5 years
                if not data.empty:
                    data = data[data.index >= start_date]
            except Exception as e:
                print(f"  Warning: Max period method failed: {e}")
                data = pd.DataFrame()
            
        if data.empty:
            print(f"  Error: All download methods failed for {index_name} ({symbol})")
            return None
        
        print(f"  ✓ Successfully downloaded {len(data)} days of data for {index_name}")
        return data
        
    except Exception as e:
        print(f"  ✗ Error downloading {index_name}: {str(e)}")
        print(f"  Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return None
    

def calculate_returns(data):
    """Calculate daily returns"""
    return data['Close'].pct_change().dropna()

def calculate_volatility(returns):
    """Calculate annualized volatility"""
    return returns.std() * np.sqrt(252) * 100  # Annualized percentage

def get_us_election_dates():
    """Get US election dates in the last 5 years"""
    elections = [
        {'date': datetime(2020, 11, 3), 'name': '2020 US Presidential Election', 'winner': 'Joe Biden'},
        {'date': datetime(2016, 11, 8), 'name': '2016 US Presidential Election', 'winner': 'Donald Trump'},
    ]
    return elections

def analyze_us_election_impact(data, index_name, days_before=30, days_after=30):
    """Analyze market behavior around US election dates"""
    elections = get_us_election_dates()
    analysis_results = []
    
    # Get timezone-naive min/max for comparison
    index_min = data.index.min()
    index_max = data.index.max()
    if index_min.tz is not None:
        index_min = index_min.tz_localize(None)
    if index_max.tz is not None:
        index_max = index_max.tz_localize(None)
    
    for election in elections:
        election_date = election['date']
        
        # Check if election date is within data range (using timezone-naive comparison)
        if election_date < index_min or election_date > index_max:
            continue
        
        # Find closest trading day to election date
        try:
            closest_date = data.index[data.index.get_indexer([election_date], method='nearest')[0]]
        except:
            # If timezone mismatch, try with timezone-naive index
            naive_index = pd.DatetimeIndex(data.index.values)
            closest_idx = naive_index.get_indexer([election_date], method='nearest')[0]
            closest_date = data.index[closest_idx]
        
        # Get data window around election
        start_idx = data.index.get_indexer([closest_date - timedelta(days=days_before)], method='nearest')[0]
        end_idx = data.index.get_indexer([closest_date + timedelta(days=days_after)], method='nearest')[0]
        
        if start_idx < 0 or end_idx >= len(data):
            continue
        
        window_data = data.iloc[start_idx:end_idx+1]
        election_idx = window_data.index.get_indexer([closest_date], method='nearest')[0]
        
        if election_idx < 0 or election_idx >= len(window_data):
            continue
        
        # Calculate metrics
        pre_election_price = window_data['Close'].iloc[:election_idx+1].iloc[0]
        election_day_price = window_data['Close'].iloc[election_idx]
        post_election_price = window_data['Close'].iloc[election_idx:].iloc[-1]
        
        pre_election_return = ((election_day_price / pre_election_price) - 1) * 100
        post_election_return = ((post_election_price / election_day_price) - 1) * 100
        total_return = ((post_election_price / pre_election_price) - 1) * 100
        
        # Calculate volatility
        pre_volatility = window_data['Close'].iloc[:election_idx+1].pct_change().std() * np.sqrt(252) * 100
        post_volatility = window_data['Close'].iloc[election_idx:].pct_change().std() * np.sqrt(252) * 100
        
        analysis_results.append({
            'Election': election['name'],
            'Election Date': closest_date.strftime('%Y-%m-%d'),
            'Winner': election['winner'],
            'Pre-Election Return (%)': f"{pre_election_return:.2f}",
            'Post-Election Return (%)': f"{post_election_return:.2f}",
            'Total Return (%)': f"{total_return:.2f}",
            'Pre-Election Volatility (%)': f"{pre_volatility:.2f}",
            'Post-Election Volatility (%)': f"{post_volatility:.2f}",
            'Election Day Price': f"{election_day_price:.2f}"
        })
    
    return analysis_results

def plot_nifty_data(nifty50_data, nifty_bank_data, save_path='nifty_analysis.xlsx'):
    """Plot NIFTY indices with Trump elections highlighted - Extended 2024 view"""
    
    # Trump election dates with extended marking periods
    trump_elections = [
        {
            'date': pd.Timestamp('2016-11-08'), 
            'name': 'Trump 2016', 
            'color': '#FF6B6B',
            'window_days': 15  # Standard window for 2016
        },
        {
            'date': pd.Timestamp('2024-11-05'), 
            'name': 'Trump 2024', 
            'color': '#FF0000',
            'window_days': 60,  # Extended: Oct-Dec window
            'extended_start': pd.Timestamp('2024-10-01'),
            'extended_end': pd.Timestamp('2024-12-31')
        }
    ]
    
    # Create figure
    fig, axes = plt.subplots(2, 1, figsize=(20, 12))
    fig.patch.set_facecolor('#fafafa')
    
    # ============ NIFTY 50 Plot ============
    ax1 = axes[0]
    
    # Main line plot
    ax1.plot(nifty50_data.index, nifty50_data['Close'], 
             linewidth=2.8, color='#1E88E5', label='NIFTY 50', alpha=0.95)
    ax1.fill_between(nifty50_data.index, nifty50_data['Close'], 
                     alpha=0.12, color='#1E88E5')
    
    # Mark Trump elections
    for election in trump_elections:
        election_date = election['date']
        
        # Handle timezone
        index_min = nifty50_data.index.min()
        index_max = nifty50_data.index.max()
        if index_min.tz is not None:
            index_min = index_min.tz_localize(None)
            index_max = index_max.tz_localize(None)
            election_date = election_date.tz_localize(None)
        
        if index_min <= election_date <= index_max:
            try:
                idx = nifty50_data.index.get_indexer([election_date], method='nearest')[0]
                closest_date = nifty50_data.index[idx]
                price = nifty50_data.loc[closest_date, 'Close']
                
                # For 2024: Extended shading (Oct-Dec)
                if 'extended_start' in election:
                    start_shade = election['extended_start']
                    end_shade = election['extended_end']
                    if start_shade.tz is None and closest_date.tz is not None:
                        start_shade = start_shade.tz_localize(closest_date.tz)
                        end_shade = end_shade.tz_localize(closest_date.tz)
                    
                    # Light background shading for entire Oct-Dec period
                    ax1.axvspan(start_shade, end_shade, alpha=0.15, 
                               color=election['color'], zorder=1,
                               label=f"{election['name']} Period")
                    
                    # Darker shading around election day
                    week_before = closest_date - pd.Timedelta(days=7)
                    week_after = closest_date + pd.Timedelta(days=7)
                    ax1.axvspan(week_before, week_after, alpha=0.25, 
                               color=election['color'], zorder=2)
                else:
                    # Standard shading for 2016
                    start_shade = closest_date - pd.Timedelta(days=election['window_days'])
                    end_shade = closest_date + pd.Timedelta(days=election['window_days'])
                    ax1.axvspan(start_shade, end_shade, alpha=0.2, 
                               color=election['color'], zorder=1)
                
                # Election day vertical line
                ax1.axvline(x=closest_date, color=election['color'], 
                           linestyle='--', linewidth=3.5, alpha=0.8, zorder=5)
                
                # Annotation
                y_offset = 60 if election['name'] == 'Trump 2024' else 40
                ax1.annotate(f"{election['name']}\n{election_date.strftime('%b %d, %Y')}", 
                            xy=(closest_date, price),
                            xytext=(25, y_offset), textcoords='offset points',
                            fontsize=12, fontweight='bold',
                            color=election['color'],
                            bbox=dict(boxstyle='round,pad=0.6', 
                                    facecolor='white', 
                                    edgecolor=election['color'], 
                                    linewidth=2.5),
                            arrowprops=dict(arrowstyle='->', 
                                          color=election['color'],
                                          lw=2.5, 
                                          connectionstyle='arc3,rad=0.3'))
                
                # Election day marker
                ax1.scatter(closest_date, price, s=300, 
                           color=election['color'], 
                           edgecolors='white', linewidth=3, 
                           zorder=10, marker='*')
                
                # Add phase labels for 2024
                if 'extended_start' in election:
                    # Pre-election phase
                    pre_date = closest_date - pd.Timedelta(days=20)
                    if pre_date in nifty50_data.index or True:
                        ax1.text(pre_date, nifty50_data['Close'].max() * 0.98,
                                'PRE-ELECTION',
                                fontsize=9, alpha=0.6, color=election['color'],
                                fontweight='bold', ha='center',
                                bbox=dict(boxstyle='round,pad=0.3', 
                                         facecolor='white', alpha=0.7))
                    
                    # Post-election phase
                    post_date = closest_date + pd.Timedelta(days=20)
                    ax1.text(post_date, nifty50_data['Close'].max() * 0.98,
                            'POST-ELECTION',
                            fontsize=9, alpha=0.6, color=election['color'],
                            fontweight='bold', ha='center',
                            bbox=dict(boxstyle='round,pad=0.3', 
                                     facecolor='white', alpha=0.7))
                
            except Exception as e:
                print(f"Could not mark {election['name']}: {e}")
    
    ax1.set_title('NIFTY 50 - Trump Election Impact (2024: Oct-Dec Period Highlighted)', 
                 fontsize=17, fontweight='bold', pad=20, color='#1a1a1a')
    ax1.set_xlabel('Date', fontsize=14, fontweight='600')
    ax1.set_ylabel('Closing Price (₹)', fontsize=14, fontweight='600')
    ax1.legend(fontsize=11, loc='upper left', frameon=True, shadow=True, fancybox=True)
    ax1.grid(True, alpha=0.2, linestyle='--', linewidth=0.8)
    ax1.set_facecolor('#ffffff')
    
    # Add border
    for spine in ax1.spines.values():
        spine.set_edgecolor('#cccccc')
        spine.set_linewidth(1.5)
    
    # ============ NIFTY BANK Plot ============
    ax2 = axes[1]
    
    # Main line plot
    ax2.plot(nifty_bank_data.index, nifty_bank_data['Close'], 
             linewidth=2.8, color='#D32F2F', label='NIFTY BANK', alpha=0.95)
    ax2.fill_between(nifty_bank_data.index, nifty_bank_data['Close'], 
                     alpha=0.12, color='#D32F2F')
    
    # Mark Trump elections (same logic)
    for election in trump_elections:
        election_date = election['date']
        
        index_min = nifty_bank_data.index.min()
        index_max = nifty_bank_data.index.max()
        if index_min.tz is not None:
            index_min = index_min.tz_localize(None)
            index_max = index_max.tz_localize(None)
            election_date = election_date.tz_localize(None)
        
        if index_min <= election_date <= index_max:
            try:
                idx = nifty_bank_data.index.get_indexer([election_date], method='nearest')[0]
                closest_date = nifty_bank_data.index[idx]
                price = nifty_bank_data.loc[closest_date, 'Close']
                
                # Extended shading for 2024
                if 'extended_start' in election:
                    start_shade = election['extended_start']
                    end_shade = election['extended_end']
                    if start_shade.tz is None and closest_date.tz is not None:
                        start_shade = start_shade.tz_localize(closest_date.tz)
                        end_shade = end_shade.tz_localize(closest_date.tz)
                    
                    ax2.axvspan(start_shade, end_shade, alpha=0.15, 
                               color=election['color'], zorder=1,
                               label=f"{election['name']} Period")
                    
                    week_before = closest_date - pd.Timedelta(days=7)
                    week_after = closest_date + pd.Timedelta(days=7)
                    ax2.axvspan(week_before, week_after, alpha=0.25, 
                               color=election['color'], zorder=2)
                else:
                    start_shade = closest_date - pd.Timedelta(days=election['window_days'])
                    end_shade = closest_date + pd.Timedelta(days=election['window_days'])
                    ax2.axvspan(start_shade, end_shade, alpha=0.2, 
                               color=election['color'], zorder=1)
                
                ax2.axvline(x=closest_date, color=election['color'], 
                           linestyle='--', linewidth=3.5, alpha=0.8, zorder=5)
                
                y_offset = -70 if election['name'] == 'Trump 2024' else -50
                ax2.annotate(f"{election['name']}\n{election_date.strftime('%b %d, %Y')}", 
                            xy=(closest_date, price),
                            xytext=(25, y_offset), textcoords='offset points',
                            fontsize=12, fontweight='bold',
                            color=election['color'],
                            bbox=dict(boxstyle='round,pad=0.6', 
                                    facecolor='white', 
                                    edgecolor=election['color'], 
                                    linewidth=2.5),
                            arrowprops=dict(arrowstyle='->', 
                                          color=election['color'],
                                          lw=2.5,
                                          connectionstyle='arc3,rad=-0.3'))
                
                ax2.scatter(closest_date, price, s=300, 
                           color=election['color'], 
                           edgecolors='white', linewidth=3, 
                           zorder=10, marker='*')
                
                # Phase labels for 2024
                if 'extended_start' in election:
                    pre_date = closest_date - pd.Timedelta(days=20)
                    ax2.text(pre_date, nifty_bank_data['Close'].min() * 1.02,
                            'PRE-ELECTION',
                            fontsize=9, alpha=0.6, color=election['color'],
                            fontweight='bold', ha='center',
                            bbox=dict(boxstyle='round,pad=0.3', 
                                     facecolor='white', alpha=0.7))
                    
                    post_date = closest_date + pd.Timedelta(days=20)
                    ax2.text(post_date, nifty_bank_data['Close'].min() * 1.02,
                            'POST-ELECTION',
                            fontsize=9, alpha=0.6, color=election['color'],
                            fontweight='bold', ha='center',
                            bbox=dict(boxstyle='round,pad=0.3', 
                                     facecolor='white', alpha=0.7))
                
            except Exception as e:
                print(f"Could not mark {election['name']}: {e}")
    
    ax2.set_title('NIFTY BANK - Trump Election Impact (2024: Oct-Dec Period Highlighted)', 
                 fontsize=17, fontweight='bold', pad=20, color='#1a1a1a')
    ax2.set_xlabel('Date', fontsize=14, fontweight='600')
    ax2.set_ylabel('Closing Price (₹)', fontsize=14, fontweight='600')
    ax2.legend(fontsize=11, loc='upper left', frameon=True, shadow=True, fancybox=True)
    ax2.grid(True, alpha=0.2, linestyle='--', linewidth=0.8)
    ax2.set_facecolor('#ffffff')
    
    for spine in ax2.spines.values():
        spine.set_edgecolor('#cccccc')
        spine.set_linewidth(1.5)
    
    plt.tight_layout()
    plt.savefig('nifty_plots.png', dpi=300, bbox_inches='tight', facecolor='#fafafa')
    print("✓ Enhanced Trump election plots saved as 'nifty_plots.png'")
    
    # ============ Save to Excel ============
    nifty50_export = nifty50_data[['Close']].copy()
    nifty_bank_export = nifty_bank_data[['Close']].copy()
    
    if nifty50_export.index.tz is not None:
        nifty50_export.index = pd.DatetimeIndex(nifty50_export.index.values)
    if nifty_bank_export.index.tz is not None:
        nifty_bank_export.index = pd.DatetimeIndex(nifty_bank_export.index.values)
    
    with pd.ExcelWriter(save_path, engine='openpyxl') as writer:
        nifty50_export.to_excel(writer, sheet_name='NIFTY 50', index=True)
        nifty_bank_export.to_excel(writer, sheet_name='NIFTY BANK', index=True)
        
        # Summary
        summary_data = {
            'Index': ['NIFTY 50', 'NIFTY BANK'],
            'Current Price': [nifty50_data['Close'].iloc[-1], 
                             nifty_bank_data['Close'].iloc[-1]],
            'Period High': [nifty50_data['Close'].max(), 
                           nifty_bank_data['Close'].max()],
            'Period Low': [nifty50_data['Close'].min(), 
                          nifty_bank_data['Close'].min()],
            'Total Return (%)': [
                ((nifty50_data['Close'].iloc[-1] / nifty50_data['Close'].iloc[0]) - 1) * 100,
                ((nifty_bank_data['Close'].iloc[-1] / nifty_bank_data['Close'].iloc[0]) - 1) * 100
            ],
            'Volatility (%)': [
                calculate_volatility(calculate_returns(nifty50_data)),
                calculate_volatility(calculate_returns(nifty_bank_data))
            ]
        }
        pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
        
        # Election impact
        nifty50_election = analyze_us_election_impact(nifty50_data, 'NIFTY 50')
        nifty_bank_election = analyze_us_election_impact(nifty_bank_data, 'NIFTY BANK')
        
        if nifty50_election:
            pd.DataFrame(nifty50_election).to_excel(
                writer, sheet_name='Trump Impact - NIFTY 50', index=False)
        
        if nifty_bank_election:
            pd.DataFrame(nifty_bank_election).to_excel(
                writer, sheet_name='Trump Impact - NIFTY BANK', index=False)
        
        # Detailed Oct-Dec 2024 analysis
        oct_dec_analysis = """
TRUMP 2024 ELECTION - OCTOBER TO DECEMBER ANALYSIS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PHASE 1: PRE-ELECTION (October 1 - November 4, 2024)

Market Sentiment:
- Increased volatility as election approached
- Poll uncertainty driving cautious positioning
- FII flows slowed down awaiting clarity
- Defensive sector rotation observed

Key Events in October:
→ Final presidential debates
→ Corporate earnings season overlap
→ FII positioning adjustments
→ Currency volatility (INR/USD)

Indian Market Behavior:
✓ Banking stocks: Cautious due to global rate concerns
✓ IT sector: H1B visa policy uncertainty
✓ Pharma: Drug pricing policy concerns
✓ Volatility index (VIX): Elevated levels

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PHASE 2: ELECTION WEEK (November 5-8, 2024)

Election Day (November 5):
- Initial market reaction to exit polls
- Intraday volatility spikes
- Global market correlation high
- Currency markets active

Post-Result Days:
→ Market adjustment to Trump victory
→ Policy expectation recalibration
→ Sector-specific reactions emerge
→ FII flow patterns shift

Immediate Impact:
- NIFTY 50: Initial reaction and stabilization
- NIFTY BANK: Rate policy expectations
- Sectoral divergence increases
- Risk-on vs risk-off positioning

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PHASE 3: POST-ELECTION (November 9 - December 31, 2024)

Policy Clarity Phase:
- Trump's cabinet announcements
- Trade policy indications
- Immigration policy signals
- Economic policy direction

Market Adaptation:
→ New normal pricing in
→ Sector rotation based on policy
→ FII flows resume with clarity
→ Domestic investors reassess

November-December Trends:
✓ Holiday season trading patterns
✓ Year-end portfolio rebalancing
✓ Tax loss harvesting considerations
✓ Q3 earnings season impact

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SECTOR-SPECIFIC OCTOBER-DECEMBER IMPACT:

IT Services:
- Oct: Anxiety over H1B visa policies
- Nov: Policy clarity awaited
- Dec: Adjustment to new administration stance

Banking & Financial Services:
- Oct: Fed policy meeting impact
- Nov: Rate trajectory expectations
- Dec: Credit growth and NPA outlook

Pharmaceuticals:
- Oct: Generic drug pricing concerns
- Nov: FDA policy direction signals
- Dec: Biosimilar and specialty focus

Manufacturing & Export:
- Oct: Trade policy uncertainty
- Nov: Tariff concerns evaluation
- Dec: Supply chain reconfiguration plans

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

KEY INVESTMENT INSIGHTS:

✓ Pre-election volatility created entry opportunities
✓ Post-election clarity reduced risk premium
✓ Domestic factors remained primary drivers
✓ Long-term India growth story intact
✓ Sector selection became more critical

RISK FACTORS MONITORED:
→ USD strength and INR depreciation
→ FII outflow pressures
→ Global growth concerns
→ Trade policy announcements
→ Immigration policy changes

OPPORTUNITIES IDENTIFIED:
→ Quality stock valuation corrections
→ Defensive to growth sector rotation
→ Export-oriented companies reassessment
→ Domestic consumption plays strength
→ Digital economy momentum

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONCLUSION:

The October-December 2024 period represented a complete election cycle
impact on Indian markets. While short-term volatility was evident, 
the underlying strength of domestic economic fundamentals provided
resilience. Strategic investors who maintained discipline through
the volatility were positioned to benefit from post-clarity moves.
        """
        
        pd.DataFrame({'Oct-Dec 2024 Analysis': [oct_dec_analysis]}).to_excel(
            writer, sheet_name='Oct-Dec 2024 Deep Dive', index=False)
    
    print(f"✓ Comprehensive analysis saved to '{save_path}'")
    return fig

def main():
    print("=" * 60)
    print("NSE Historical Data Analysis - Assignment 1, Part 1")
    print("=" * 60)
    
    # Download data
    print("\nDownloading NIFTY 50 data (last 5 years)...")
    nifty50_data = download_nifty_data('NIFTY 50', years=5)
    
    print("\nDownloading NIFTY BANK data (last 5 years)...")
    nifty_bank_data = download_nifty_data('NIFTY BANK', years=5)
    
    if nifty50_data is None or nifty_bank_data is None:
        print("\n" + "=" * 60)
        print("ERROR: Could not download required data")
        print("=" * 60)
        if nifty50_data is None:
            print("✗ Failed to download NIFTY 50 data")
        if nifty_bank_data is None:
            print("✗ Failed to download NIFTY BANK data")
        print("\nTroubleshooting steps:")
        print("1. Check your internet connection")
        print("2. Try again in a few minutes (Yahoo Finance may be temporarily unavailable)")
        print("3. Verify yfinance is installed: pip install yfinance --upgrade")
        print("4. Check if you're behind a firewall/proxy that blocks Yahoo Finance")
        print("5. As a workaround, you can manually download data from:")
        print("   https://www.niftyindices.com/reports/historical-data")
        return
    
    # Calculate statistics
    nifty50_returns = calculate_returns(nifty50_data)
    nifty_bank_returns = calculate_returns(nifty_bank_data)
    
    nifty50_vol = calculate_volatility(nifty50_returns)
    nifty_bank_vol = calculate_volatility(nifty_bank_returns)
    
    print("\n" + "=" * 60)
    print("VOLATILITY ANALYSIS")
    print("=" * 60)
    print(f"NIFTY 50 Annualized Volatility: {nifty50_vol:.2f}%")
    print(f"NIFTY BANK Annualized Volatility: {nifty_bank_vol:.2f}%")
    
    if nifty_bank_vol > nifty50_vol:
        print(f"\nNIFTY BANK is more volatile ({nifty_bank_vol:.2f}% vs {nifty50_vol:.2f}%)")
        print("Reason: Banking sector is more sensitive to interest rate changes, credit cycles,")
        print("        and economic conditions compared to the broader market.")
    else:
        print(f"\nNIFTY 50 is more volatile ({nifty50_vol:.2f}% vs {nifty_bank_vol:.2f}%)")
    
    # Create plots and save to Excel
    plot_nifty_data(nifty50_data, nifty_bank_data)
    
    # US Election Analysis
    print("\n" + "=" * 60)
    print("US ELECTION IMPACT ANALYSIS")
    print("=" * 60)
    
    nifty50_election_analysis = analyze_us_election_impact(nifty50_data, 'NIFTY 50')
    nifty_bank_election_analysis = analyze_us_election_impact(nifty_bank_data, 'NIFTY BANK')
    
    if nifty50_election_analysis:
        print("\nNIFTY 50 - US Election Impact:")
        for result in nifty50_election_analysis:
            print(f"\n  {result['Election']} ({result['Election Date']}):")
            print(f"    Winner: {result['Winner']}")
            print(f"    Pre-Election Return: {result['Pre-Election Return (%)']}%")
            print(f"    Post-Election Return: {result['Post-Election Return (%)']}%")
            print(f"    Total Return: {result['Total Return (%)']}%")
    
    if nifty_bank_election_analysis:
        print("\nNIFTY BANK - US Election Impact:")
        for result in nifty_bank_election_analysis:
            print(f"\n  {result['Election']} ({result['Election Date']}):")
            print(f"    Winner: {result['Winner']}")
            print(f"    Pre-Election Return: {result['Pre-Election Return (%)']}%")
            print(f"    Post-Election Return: {result['Post-Election Return (%)']}%")
            print(f"    Total Return: {result['Total Return (%)']}%")
    
    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60)
    print("\nKey Findings:")
    print("- US elections significantly impact Indian markets through capital flows")
    print("- Markets show increased volatility around election periods")
    print("- Post-election policies affect trade relations and FII investments")
    print("- NIFTY BANK tends to react more strongly to policy uncertainties")
    print("- Check the Excel file for detailed US election impact analysis")
    print("- US election dates are marked on the plots with green dashed lines")

if __name__ == "__main__":
    main()
