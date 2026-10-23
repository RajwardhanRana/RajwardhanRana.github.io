"""Class 4: reproduce the World Bank API data checks and chart specification.
Run from the project root after installing scripts/requirements-week3.txt.
This refreshes the snapshot CSVs; the website chart uses the live API directly.
"""
import importlib.util
import subprocess
import sys
needed = [p for p in ['requests', 'pandas', 'altair'] if importlib.util.find_spec(p) is None]
# Colab may already have Altair 5. Upgrade before importing it.
from importlib.metadata import version
if importlib.util.find_spec('altair') is not None and int(version('altair').split('.')[0]) < 6:
    needed.append('altair>=6,<7')
if needed:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', *needed])
import requests
import pandas as pd
import altair as alt
import json
from pathlib import Path
root = Path.cwd()
if root.name in ('notebooks', 'scripts') and (root.parent / 'index.html').exists():
    root = root.parent
data_dir = root / 'data'
data_dir.mkdir(exist_ok=True)


url = 'https://api.worldbank.org/v2/country/kor/indicator/SP.DYN.TFRT.IN?format=json&per_page=1000'
response = requests.get(url, timeout=60)
response.raise_for_status()
data = response.json()
assert isinstance(data, list) and len(data) == 2 and isinstance(data[1], list)
metadata = data[0]
assert int(metadata['pages']) == 1
assert len(data[1]) == int(metadata['total'])
print('Status:', response.status_code)
print('Metadata:', metadata)
print('First record:', data[1][0])


df = pd.json_normalize(data[1])
df = df[['country.value', 'date', 'value']].copy()
missing = int(df.value.isna().sum())
df = df.dropna(subset=['value']).copy()
df['date'] = pd.to_datetime(df['date'], format='%Y', errors='raise')
df = df.sort_values('date').reset_index(drop=True)
assert not df.date.duplicated().any()
assert df.value.ge(0).all()
df.to_csv(data_dir / 'worldbank_fertility_kor.csv', index=False, date_format='%Y-%m-%d')
print('Missing observations excluded:', missing)
print(df.tail().to_string(index=False))


snapshot_chart = alt.Chart(df).mark_line(color='#087f8c', strokeWidth=2.5).encode(
    x=alt.X('date:T', title='Year', axis=alt.Axis(grid=False, format='%Y')),
    y=alt.Y('value:Q', title='Births per woman', scale=alt.Scale(zero=True)),
    tooltip=[alt.Tooltip('date:T', title='Year', format='%Y'), alt.Tooltip('value:Q', title='Births per woman', format='.3f')]
).properties(width=500, height=280, title='South Korea: total fertility rate')
snapshot_chart


comparison_url = 'https://api.worldbank.org/v2/country/kor;ind;jpn;gbr/indicator/SP.DYN.TFRT.IN?format=json&per_page=1000'
comparison_response = requests.get(comparison_url, timeout=60)
comparison_response.raise_for_status()
comparison = comparison_response.json()
assert int(comparison[0]['pages']) == 1
assert len(comparison[1]) == int(comparison[0]['total'])
(data_dir / 'worldbank_fertility_api_snapshot.json').write_text(json.dumps(comparison, indent=2) + '\n', encoding='utf-8')
multi = pd.json_normalize(comparison[1])
multi = multi[['countryiso3code', 'country.value', 'date', 'value']].dropna(subset=['value']).copy()
multi['date'] = pd.to_datetime(multi['date'], format='%Y', errors='raise')
multi = multi.sort_values(['countryiso3code', 'date']).reset_index(drop=True)
assert not multi.duplicated(['countryiso3code', 'date']).any()
assert set(multi.countryiso3code) == {'KOR','IND','JPN','GBR'}
multi.to_csv(data_dir / 'worldbank_fertility_comparison.csv', index=False, date_format='%Y-%m-%d')
print(multi.groupby('countryiso3code').size().to_string())


live_spec = {'$schema': 'https://vega.github.io/schema/vega-lite/v6.json', 'description': 'Class 4: a live World Bank API chart. Reads the second JSON array, removes null observations and uses UTC dates. No API key or CSV is used for this chart.', 'width': 'container', 'height': 310, 'title': {'text': 'Fertility rates from the World Bank API', 'subtitle': ['Annual total fertility rate, births per woman', 'South Korea is the class example; use the selector to explore'], 'anchor': 'start', 'fontSize': 18, 'subtitleFontSize': 11}, 'data': {'url': 'https://api.worldbank.org/v2/country/kor;ind;jpn;gbr/indicator/SP.DYN.TFRT.IN?format=json&per_page=1000', 'format': {'type': 'json', 'property': '[1]'}}, 'params': [{'name': 'Country_choice', 'value': 'KOR', 'bind': {'input': 'select', 'options': ['KOR', 'IND', 'JPN', 'GBR', 'ALL'], 'labels': ['South Korea', 'India', 'Japan', 'United Kingdom', 'Compare all four'], 'name': 'Country: '}}], 'transform': [{'filter': 'isValid(datum.value) && isFinite(datum.value)'}, {'calculate': "utcParse(datum.date, '%Y')", 'as': 'YearDate'}, {'calculate': "datum.countryiso3code === 'KOR' ? 'South Korea' : datum.countryiso3code === 'IND' ? 'India' : datum.countryiso3code === 'JPN' ? 'Japan' : 'United Kingdom'", 'as': 'Country'}, {'filter': "Country_choice === 'ALL' || datum.countryiso3code === Country_choice"}], 'mark': {'type': 'line', 'strokeWidth': 2.5}, 'encoding': {'x': {'field': 'YearDate', 'type': 'temporal', 'title': 'Year', 'scale': {'type': 'utc'}, 'axis': {'format': '%Y', 'tickCount': 7, 'grid': False}}, 'y': {'field': 'value', 'type': 'quantitative', 'title': 'Births per woman', 'scale': {'zero': True}, 'axis': {'format': '.1f'}}, 'color': {'field': 'Country', 'type': 'nominal', 'title': None, 'scale': {'domain': ['South Korea', 'India', 'Japan', 'United Kingdom'], 'range': ['#087f8c', '#ba5a16', '#3566a3', '#80519c']}, 'legend': {'orient': 'bottom', 'columns': 2, 'labelFontSize': 11}}, 'tooltip': [{'field': 'Country', 'type': 'nominal'}, {'field': 'date', 'type': 'ordinal', 'title': 'Year'}, {'field': 'value', 'type': 'quantitative', 'title': 'Births per woman', 'format': '.3f'}]}, 'config': {'font': 'Arial', 'background': 'white', 'view': {'stroke': None}, 'axis': {'labelFontSize': 12, 'titleFontSize': 13, 'titlePadding': 12, 'gridColor': '#e8edf0', 'domainColor': '#b8c4cc'}}}
# Validate the manually authored Vega-Lite spec using Altair's schema.
alt.Chart.from_dict(live_spec, validate=True)
(root / 'wk4_worldbank_live.json').write_text(json.dumps(live_spec, indent=2) + '\n', encoding='utf-8')
assert live_spec['data']['url'].startswith('https://api.worldbank.org/')
assert live_spec['data']['format']['property'] == '[1]'
print('Saved live chart specification; API URL, no embedded data and no API key.')


life_url = 'https://api.worldbank.org/v2/country/ind/indicator/SP.DYN.LE00.IN?format=json&per_page=1000'
life_response = requests.get(life_url, timeout=60)
life_response.raise_for_status()
life_data = life_response.json()
assert int(life_data[0]['pages']) == 1
life = pd.json_normalize(life_data[1])[['country.value','date','value']].dropna(subset=['value']).copy()
life['date'] = pd.to_datetime(life['date'], format='%Y', errors='raise')
life = life.sort_values('date')
assert not life.date.duplicated().any()
life.to_csv(data_dir / 'worldbank_life_expectancy_ind.csv', index=False, date_format='%Y-%m-%d')
life_chart = alt.Chart(life).mark_line(color='#ba5a16').encode(
    x=alt.X('date:T', title='Year'), y=alt.Y('value:Q', title='Life expectancy at birth (years)', scale=alt.Scale(zero=True))
).properties(width=500, height=280, title='India: life expectancy at birth')
life_chart

