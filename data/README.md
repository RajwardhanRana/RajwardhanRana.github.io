# India inflation data

- Indicator: FP.CPI.TOTL.ZG, Inflation, consumer prices (annual %).
- Source: World Bank World Development Indicators; IMF International Financial Statistics.
- Series: https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG?locations=IN
- API: https://api.worldbank.org/v2/country/IND/indicator/FP.CPI.TOTL.ZG?format=json&per_page=100
- Downloaded: 2026-10-15. API last updated: 2026-10-08.
- Licence shown by the World Bank: CC BY 4.0.
- Original response retained in india_inflation_source.json.
- Cleaned CSV: 26 annual observations, 2000-2025.
- Keep India, indicator FP.CPI.TOTL.ZG, years >= 2000 and non-null observations. Sort ascending. No interpolation or imputation. Preserve source precision.
- Date is YYYY-01-01 for plotting an annual observation; it is not January-only inflation. Year is an integer, Inflation a numeric annual percentage change (e.g. 5 means 5%, not 500%).
- Prepared with Python rather than Excel. To practise the seminar's Excel steps, open the CSV, verify the three column types, format Date as yyyy-mm-dd and save a separate CSV copy.
- Both charts use a saved snapshot; source revisions require refreshing the data.
