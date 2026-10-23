# Class 3 Shiller data

Robert Shiller monthly US stock-market data, supplied by the LSE PP434 teaching team in DataCodeHandout.zip. Raw and cleaned CSVs match the linked course data.

- Original source: https://shillerdata.com/
- Course copy: https://raw.githubusercontent.com/jhellingsdata/LSE-PP434/main/weeks/week03/data/data_shiller.csv
- Raw SHA-256: d77861ce8e5981ebb3a916b197fcf372a7dea0b15c709a44d1d4b639891f10e2
- Snapshot downloaded/verified: 2026-10-23.
- Raw rows: 1870. Valid monthly P/E rows: 1866. Removed: 4 missing ratios.
- Coverage: January 1871 to June 2026; four subsequent months have no usable earnings.
- P/E = P divided by E; no CAPE substitution. Source precision retained, dates parsed from strings with %Y.%m.
- data_shiller_clean.csv preserves every original column plus PE_ratio and Date_iso. Missing early CAPE is retained.
- data_shiller_pe.csv contains Date_iso and PE_ratio only, without a pandas index.
- Mean = arithmetic mean across all valid monthly observations, including the 2009 spike. No interpolation, smoothing or outlier deletion was added by this project. Some source earnings are interpolated by Shiller; see original source methodology.
- The notebook and scripts/build_week3.py reproduce the data and Altair JSON. Original teaching files are preserved outside the repository in ../Class3_materials.
- Both chart layers use the same data and full time range. The CSV is a static course snapshot; it does not auto-update with current markets.
