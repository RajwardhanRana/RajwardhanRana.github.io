# Class 4 World Bank API

## Live website chart
- Indicator SP.DYN.TFRT.IN: total fertility rate, births per woman.
- Countries: KOR, IND, JPN, GBR. Default selector: South Korea.
- Endpoint: https://api.worldbank.org/v2/country/kor;ind;jpn;gbr/indicator/SP.DYN.TFRT.IN?format=json&per_page=1000
- Format: JSON array [metadata, observations]. Vega-Lite property: [1].
- Access-Control-Allow-Origin was * when checked on 2026-10-23. No API key required.
- Current response: 264 observations, 260 non-null country-year observations. Metadata last updated: 2026-10-08.
- Chart filters null values, uses UTC year parsing, chronological line ordering and a zero y baseline. Country selection filters the fetched rows; it does not send personal data.
- API data are requested on page load. Provider releases, revisions, availability and caching govern freshness. No snapshot fallback is silently substituted.

## Snapshot outputs
- worldbank_fertility_kor.csv: cleaned seminar example.
- worldbank_fertility_comparison.csv: four countries, null observations removed, ISO dates sorted by country/year.
- worldbank_fertility_api_snapshot.json: original response for validation.
- worldbank_life_expectancy_ind.csv: the notebook's different-indicator experiment. Indicator SP.DYN.LE00.IN, years of life expectancy at birth.
- CSV dates represent annual observations at January 1, not January-only measurements. Missing values remain distinct from zero.
- Snapshots prepared on 2026-10-23. The notebook refreshes them when rerun; they are not the live chart's data source.

## Provenance
- World Bank WDI: https://data.worldbank.org/indicator/SP.DYN.TFRT.IN
- Upstream sources listed: UN World Population Prospects, national statistical offices and Eurostat. CC BY 4.0 shown on the indicator page.
- API documentation: https://datahelpdesk.worldbank.org/knowledgebase/articles/898581
- Based on the teaching team's DS4_2_API_WorldBank notebook. Original teaching notebooks are stored outside the repository in ../Class4_materials.
- Period total fertility is based on age-specific fertility rates; it is not an individual forecast. Cross-country source methods and revisions affect comparisons.
