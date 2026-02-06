# Assignment 1: Monetary Economics - Answers and Analysis

## Part 1: NSE Historical Data Analysis

### 1a. Market Behavior During US Events

**Analysis:**
Based on historical data analysis of NIFTY 50 and NIFTY BANK indices over the last 5 years:

- **Correlation with US Markets:** Indian markets show significant correlation with US market movements, especially during major events like:
  - Federal Reserve interest rate decisions
  - US-China trade tensions (2018-2019)
  - COVID-19 pandemic (2020)
  - Inflation concerns and Fed rate hikes (2022-2023)

- **Transmission Channels:**
  1. **Capital Flows:** US monetary policy affects foreign institutional investment (FII) flows into India
  2. **Currency Impact:** USD strength/weakness affects INR, impacting export-import dynamics
  3. **Risk Sentiment:** US market volatility triggers global risk-off sentiment

- **Specific Observations:**
  - During US Fed rate hikes, Indian markets typically experience outflows and volatility
  - NIFTY BANK shows stronger reaction to US rate changes due to banking sector sensitivity
  - Recovery patterns often follow US market recovery with a lag

### 1a. Volatility Comparison

**Answer:** NIFTY BANK is more volatile than NIFTY 50.

**Reasons:**
1. **Sector Concentration:** NIFTY BANK focuses solely on banking sector, which is more sensitive to:
   - Interest rate changes (RBI and Fed policies)
   - Credit cycles and NPAs (Non-Performing Assets)
   - Economic growth cycles
   - Regulatory changes

2. **Leverage Sensitivity:** Banks operate with high leverage, making them more vulnerable to economic shocks

3. **Macroeconomic Dependencies:** Banking sector performance is directly tied to:
   - GDP growth
   - Inflation rates
   - Currency movements
   - Government policies

4. **NIFTY 50 Diversification:** NIFTY 50 includes diverse sectors (IT, Pharma, FMCG, etc.) which provides natural diversification and reduces overall volatility

**Evidence:** Historical data typically shows NIFTY BANK volatility (annualized) around 25-30% compared to NIFTY 50's 18-22%.

### 1b. Challenging Problem - Python Code

The Python code is provided in `nse_challenging.py`. Key features:

- Downloads historical data for NIFTY 50, NIFTY 100, and NIFTY 500
- Calculates daily and cumulative returns
- Creates comparative visualizations
- Generates statistical analysis including Sharpe ratios

**Expected Observations:**
- NIFTY 500 (broadest index) typically shows highest volatility
- NIFTY 50 (large cap) shows lowest volatility
- Returns are highly correlated due to overlapping constituents
- NIFTY 100 provides middle ground between 50 and 500

---

## Part 2: INR/USD Exchange Rate Analysis

### 2a. Five Biggest Single Month Jumps

The script `inr_usd_analysis.py` automatically identifies the five biggest monthly increases (INR depreciation) in the exchange rate.

**Typical Historical Periods with Major Jumps:**
1. **May 2013** - Taper Tantrum (Fed's announcement of QE tapering)
2. **August 2013** - Continued capital outflows
3. **September 2018** - US-China trade war escalation, oil price spike
4. **March 2020** - COVID-19 pandemic panic
5. **May 2022** - Fed rate hikes, oil price surge, capital outflows

### 2b. Historical Events Association

**May 2013 - Taper Tantrum:**
- US Fed Chairman Ben Bernanke hinted at QE tapering
- Massive capital outflows from emerging markets
- INR depreciated sharply as FIIs pulled out

**September 2018:**
- US-China trade tensions escalated
- Oil prices surged (India imports 80% of oil)
- Current account deficit concerns
- IL&FS crisis in India

**March 2020:**
- COVID-19 pandemic declared
- Global risk-off sentiment
- Flight to safety (USD)
- Lockdown announcements worldwide

**May 2022:**
- US Fed aggressive rate hikes
- Russia-Ukraine war → oil price spike
- Foreign capital outflows
- Inflation concerns globally

### 2c. Is Drop in INR Good for Indian Households?

**Answer: Generally NO, it's bad for most Indian households.**

**Negative Impacts (Dominant):**

1. **Higher Fuel Prices:**
   - India imports 80% of its oil
   - Weak INR → expensive oil → higher petrol/diesel prices
   - Cascading effect on transportation costs
   - Affects prices of all goods (inflation)

2. **Expensive Imports:**
   - Electronics, machinery, and consumer goods become costlier
   - Direct impact on household budgets
   - Reduced purchasing power

3. **Inflationary Pressure:**
   - Imported inflation affects overall price level
   - RBI may need to raise rates to control inflation
   - Higher EMIs and loan costs

4. **Education Abroad:**
   - More expensive for students studying overseas
   - Higher costs for families

5. **Foreign Travel:**
   - Vacation costs increase significantly
   - Reduced affordability

**Positive Impacts (Limited):**

1. **Exporters Benefit:**
   - IT services, textiles, pharmaceuticals earn more in INR
   - But benefits are concentrated in specific sectors

2. **Remittances:**
   - NRIs sending money home → more INR per USD
   - Benefits remittance-receiving families (limited segment)

3. **Tourism:**
   - Foreign tourists find India cheaper
   - Benefits tourism industry

**Net Effect:**
- **Negative for majority** due to:
  - Higher cost of living
  - Reduced purchasing power
  - Inflationary impact
- Benefits are concentrated in export sectors and remittance-receiving families
- Overall welfare impact is negative for typical Indian households

---

## Part 3: RBI Money Stock Analysis

### 3a. Money Stock Components Documentation

**M1 (Narrow Money):**
- Currency with the public (notes and coins in circulation)
- Demand deposits with the public
  - Current accounts
  - Savings accounts with check facilities
- **Characteristics:** Most liquid, used for transactions

**M2:**
- M1 +
- Savings deposits with post office savings banks
- **Characteristics:** Includes near-money savings instruments

**M3 (Broad Money):**
- M2 +
- Time deposits with the public
  - Fixed deposits
  - Recurring deposits
  - Other time deposits
- **Characteristics:** Most commonly used measure, includes all bank deposits

**M4:**
- M3 +
- All deposits with post office savings banks
  - (Excluding National Savings Certificates)
- **Characteristics:** Broadest measure, includes all post office savings

**Reference:** RBI Handbook of Statistics on Indian Economy

### 3b. Do They Move Together?

**Answer: YES, they move together very closely.**

**Evidence:**
- High correlation (typically >0.95) between all components
- M1, M2, M3, M4 show similar growth trends over time
- M3 and M4 are nested within each other, so they must move together
- M1 is a component of all others

**Reasons:**
1. **Nested Structure:** Each measure includes the previous one
2. **Common Drivers:** All affected by:
   - Economic growth
   - RBI monetary policy
   - Banking sector performance
   - Public confidence in banking system

3. **Stable Ratios:** The ratios between components remain relatively stable over time

**Visual Evidence:** The plot shows all four measures moving in parallel, with M4 > M3 > M2 > M1 at all times.

### 3c. Which is the Best Measure?

**Answer: M3 (Broad Money) is the best measure.**

**Reasons:**

1. **Most Commonly Used:**
   - RBI uses M3 as the primary monetary aggregate
   - Most monetary policy decisions reference M3 growth
   - Standard measure in economic analysis

2. **Balanced Coverage:**
   - Includes transaction money (M1) - captures immediate liquidity
   - Includes savings (M2) - captures near-money
   - Includes time deposits - important in Indian context (high savings rate)
   - Excludes post office deposits which may not be as liquid

3. **Policy Relevance:**
   - M3 growth is a key indicator for inflation targeting
   - Better predictor of economic activity than narrower measures
   - More stable than M1 or M2 (less volatile)

4. **Practical Considerations:**
   - M1 is too narrow and volatile for policy purposes
   - M2 misses important time deposits (significant in India)
   - M4 includes post office deposits which may not reflect monetary policy transmission as directly

5. **International Comparison:**
   - Comparable to M2/M3 measures used globally
   - Allows cross-country analysis

**Conclusion:** M3 provides the best balance between comprehensiveness and policy relevance for monetary analysis in India.

### 3d. Challenging Problem - Python Code

The Python code is provided in `rbi_challenging.py`. It:

- Downloads RBI Table 5 (Ratios and Rates) and Table 6 (Money Stock)
- Extracts 91-day T-bill yield and 10-year G-sec yield
- Plots money stock components with treasury yields
- Provides comprehensive analysis

**Expected Relationships:**

1. **Money Stock Growth vs Yields:**
   - **Liquidity Effect:** Higher money supply → Lower yields (short-term)
   - **Inflation Expectations:** High M3 growth → Inflation concerns → Higher yields (long-term)

2. **Short-term (91-Day T-Bill):**
   - More sensitive to RBI repo rate
   - Reflects immediate liquidity conditions
   - Closely follows monetary policy

3. **Long-term (10-Year G-Sec):**
   - Reflects inflation expectations
   - Affected by fiscal policy and government borrowing
   - More stable, less volatile

4. **Interpretation:**
   - If M3 grows faster than yields → Expansionary policy, liquidity effect
   - If yields rise faster than M3 → Tightening or inflation concerns
   - Negative correlation → Liquidity effect dominates
   - Positive correlation → Inflation expectations dominate

---

## Summary

This assignment covers:
1. **Stock Market Analysis:** Understanding volatility and market behavior
2. **Exchange Rate Analysis:** Impact of currency movements on households
3. **Monetary Aggregates:** Understanding money supply measures and their relationship with interest rates

All Python scripts are provided with comprehensive documentation and analysis outputs.
