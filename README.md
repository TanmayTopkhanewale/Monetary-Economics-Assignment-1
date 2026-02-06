# Monetary Economics Assignment 1 (HSN-302)

This repository contains Python scripts and analysis for Assignment 1 in Monetary Economics.

## Assignment Overview

**Total Marks:** 3  
**Submission Date:** 6 February 2026, 3 PM

## Structure

### Part 1: NSE Historical Data Analysis
- `nse_analysis.py` - Main script for NIFTY 50 and NIFTY BANK analysis (5 years)
- `nse_challenging.py` - Challenging problem: Compare NIFTY 50/100/500 returns (3 years)

### Part 2: INR/USD Exchange Rate Analysis
- `inr_usd_analysis.py` - Downloads FRED data and analyzes biggest monthly jumps

### Part 3: RBI Money Stock Analysis
- `rbi_money_stock.py` - Main script for M1, M2, M3, M4 analysis
- `rbi_challenging.py` - Challenging problem: Plot money stock with treasury yields

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. For FRED data (Part 2), get a free API key:
   - Visit: https://fred.stlouisfed.org/docs/api/api_key.html
   - Set environment variable: `FRED_API_KEY=your_key_here`

## Usage

### Part 1: NSE Analysis

**Basic Analysis:**
```bash
python nse_analysis.py
```
This will:
- Download NIFTY 50 and NIFTY BANK data (last 5 years)
- Create plots and save to `nifty_analysis.xlsx`
- Calculate volatility and provide analysis

**Challenging Problem:**
```bash
python nse_challenging.py
```
This will:
- Download NIFTY 50, 100, and 500 data (last 3 years)
- Compare returns and create visualization
- Save to `nifty_returns_analysis.xlsx`

### Part 2: INR/USD Analysis

```bash
python inr_usd_analysis.py
```

**Note:** If automatic download fails:
1. Manually download from: https://fred.stlouisfed.org/series/CCUSMA02INM618N
2. Save as `CCUSMA02INM618N.csv` in the same directory
3. Run the script again

This will:
- Find 5 biggest monthly jumps
- Create plots highlighting these events
- Save analysis to `inr_usd_analysis.xlsx`

### Part 3: RBI Money Stock Analysis

**Basic Analysis:**
```bash
python rbi_money_stock.py
```

**Manual Download Required:**
1. Go to: https://dbie.rbi.org.in/DBIE/dbie.rbi?site=publications
2. Navigate to: Time-Series Publications → Weekly Statistical Supplement
3. Download Table No. 6 - Money Stock: Components and Sources
4. Save as `rbi_money_stock.xlsx`

**Challenging Problem:**
```bash
python rbi_challenging.py
```

**Additional Download Required:**
1. Download Table No. 5 - Ratios and Rates from the same location
2. Save as `rbi_ratios_rates.xlsx`

## Output Files

### Part 1:
- `nifty_analysis.xlsx` - NIFTY 50 and BANK data with summary
- `nifty_plots.png` - Visualization plots
- `nifty_returns_analysis.xlsx` - Returns comparison (challenging)
- `nifty_returns_comparison.png` - Returns visualization

### Part 2:
- `inr_usd_analysis.xlsx` - Exchange rate data and analysis
- `inr_usd_plots.png` - Visualization plots

### Part 3:
- `rbi_money_stock_analysis.xlsx` - Money stock components analysis
- `money_stock_components.png` - Components plot
- `rbi_comprehensive_analysis.xlsx` - Money stock with yields (challenging)
- `money_stock_with_yields.png` - Comprehensive visualization

## Assignment Questions & Answers

### Part 1a:
- **Market behavior during US events:** See analysis in `nifty_analysis.py` output
- **Volatility comparison:** NIFTY BANK is typically more volatile due to sensitivity to interest rates

### Part 1b (Challenging):
- Python code provided in `nse_challenging.py`
- Returns comparison plot generated automatically

### Part 2:
- **5 biggest jumps:** Identified automatically in `inr_usd_analysis.py`
- **Historical events:** Research required for specific dates
- **Impact on households:** Analysis provided in Excel output

### Part 3:
- **Components documentation:** Provided in script output
- **Movement analysis:** Correlation calculated automatically
- **Best measure:** M3 is recommended (analysis in Excel)
- **Challenging:** Code in `rbi_challenging.py` with comprehensive plots

## Notes

1. **Data Sources:**
   - NSE: Uses yfinance (Yahoo Finance) as NSE doesn't provide direct API
   - FRED: Requires API key or manual download
   - RBI: Manual download required (no public API)

2. **Data Format:**
   - Ensure Excel files have proper column headers
   - Date columns should be in first column or properly formatted
   - Column names should match expected patterns (M1, M2, M3, M4, etc.)

3. **Troubleshooting:**
   - If downloads fail, check internet connection
   - For FRED, ensure API key is set correctly
   - For RBI data, verify column names match expected format

## References

- NSE Historical Data: https://www.niftyindices.com/reports/historical-data
- FRED Exchange Rate: https://fred.stlouisfed.org/series/CCUSMA02INM618N
- RBI DBIE: https://dbie.rbi.org.in/DBIE/dbie.rbi?site=publications
- Money Stock Definition: https://www.rbi.org.in/Scripts/PublicationReportDetails.aspx?ID=293
- Textbook: Mishkin - The Economics of Money, Banking and Financial Markets, 11th Edition

## Author

Created for Monetary Economics Assignment 1 (HSN-302)
