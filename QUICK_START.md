# Quick Start Guide - Monetary Economics Assignment 1

## Step-by-Step Instructions

### Prerequisites
1. Install Python 3.7 or higher
2. Install required packages:
```bash
pip install -r requirements.txt
```

### Part 1: NSE Analysis (30 minutes)

#### Basic Analysis (1a):
```bash
python nse_analysis.py
```
- Automatically downloads NIFTY 50 and NIFTY BANK data
- Creates `nifty_analysis.xlsx` with plots and data
- Generates `nifty_plots.png` visualization
- **Answer questions:** Check the console output and Excel file

#### Challenging Problem (1b):
```bash
python nse_challenging.py
```
- Downloads NIFTY 50, 100, and 500 data
- Creates returns comparison plot
- Saves to `nifty_returns_analysis.xlsx`

### Part 2: INR/USD Analysis (45 minutes)

#### Option A: Automatic Download (Requires FRED API Key)
1. Get free API key from: https://fred.stlouisfed.org/docs/api/api_key.html
2. Set environment variable:
   - Windows: `set FRED_API_KEY=your_key_here`
   - Linux/Mac: `export FRED_API_KEY=your_key_here`
3. Run:
```bash
python inr_usd_analysis.py
```

#### Option B: Manual Download (Recommended)
1. Go to: https://fred.stlouisfed.org/series/CCUSMA02INM618N
2. Click "Download" → "CSV"
3. Save as `CCUSMA02INM618N.csv` in the project folder
4. Run:
```bash
python inr_usd_analysis.py
```

**Output:**
- `inr_usd_analysis.xlsx` - Contains data, biggest jumps, and analysis
- `inr_usd_plots.png` - Visualization with highlighted jumps

**Next Steps:**
- Research historical events for the 5 dates identified
- Update the analysis sheet with specific events

### Part 3: RBI Money Stock Analysis (60 minutes)

#### Basic Analysis (3a-c):

1. **Download RBI Data:**
   - Go to: https://dbie.rbi.org.in/DBIE/dbie.rbi?site=publications
   - Navigate: Time-Series Publications → Weekly Statistical Supplement
   - Find: Table No. 6 - Money Stock: Components and Sources
   - Download and save as `rbi_money_stock.xlsx`

2. **Run Analysis:**
```bash
python rbi_money_stock.py
```

**Output:**
- `rbi_money_stock_analysis.xlsx` - Components, documentation, correlation
- `money_stock_components.png` - Plot of M1, M2, M3, M4

#### Challenging Problem (3d):

1. **Download Additional Data:**
   - From same RBI location, download Table No. 5 - Ratios and Rates
   - Save as `rbi_ratios_rates.xlsx`

2. **Run Analysis:**
```bash
python rbi_challenging.py
```

**Output:**
- `rbi_comprehensive_analysis.xlsx` - Money stock with treasury yields
- `money_stock_with_yields.png` - Comprehensive visualization

## Troubleshooting

### Issue: "Module not found"
**Solution:** Install missing packages
```bash
pip install -r requirements.txt
```

### Issue: NSE data download fails
**Solution:** 
- Check internet connection
- yfinance uses Yahoo Finance as data source
- If fails, manually download from NSE website

### Issue: FRED data download fails
**Solution:**
- Use manual download method (Option B above)
- Ensure CSV file is named exactly `CCUSMA02INM618N.csv`

### Issue: RBI data not loading
**Solution:**
- Ensure Excel file is named correctly
- Check that columns are named M1, M2, M3, M4 (or similar)
- Verify date column is in first column or properly formatted

### Issue: Plots not showing
**Solution:**
- Plots are saved as PNG files automatically
- Check the current directory for image files
- If using Jupyter, add `plt.show()` at the end

## Expected Timeline

- **Part 1:** 30-45 minutes (including challenging)
- **Part 2:** 45-60 minutes (including research)
- **Part 3:** 60-90 minutes (including data download)
- **Total:** 2.5-3.5 hours

## File Checklist

After running all scripts, you should have:

### Part 1:
- [ ] `nifty_analysis.xlsx`
- [ ] `nifty_plots.png`
- [ ] `nifty_returns_analysis.xlsx` (challenging)
- [ ] `nifty_returns_comparison.png` (challenging)

### Part 2:
- [ ] `inr_usd_analysis.xlsx`
- [ ] `inr_usd_plots.png`
- [ ] `CCUSMA02INM618N.csv` (if manual download)

### Part 3:
- [ ] `rbi_money_stock.xlsx` (downloaded from RBI)
- [ ] `rbi_money_stock_analysis.xlsx`
- [ ] `money_stock_components.png`
- [ ] `rbi_ratios_rates.xlsx` (downloaded from RBI, challenging)
- [ ] `rbi_comprehensive_analysis.xlsx` (challenging)
- [ ] `money_stock_with_yields.png` (challenging)

## Tips for Success

1. **Start Early:** Data downloads may take time
2. **Read Outputs:** Excel files contain detailed analysis
3. **Check Plots:** Visualizations help understand trends
4. **Research Events:** For Part 2, research actual historical events
5. **Verify Data:** Ensure downloaded data matches expected format
6. **Backup Work:** Keep copies of all generated files

## Getting Help

- Check `ASSIGNMENT_ANSWERS.md` for detailed answers
- Review `README.md` for comprehensive documentation
- Check console output for error messages
- Verify data file formats match expected structure
