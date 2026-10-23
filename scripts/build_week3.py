"""Reproduce Class 3 data cleaning and Altair JSON export.
Run from the project root: python scripts/build_week3.py
Install requirements-week3.txt first. The supplied snapshot is checked by SHA-256.
"""
from pathlib import Path
import hashlib
import io
import requests
import pandas as pd
import altair as alt

# Works from the project root, its notebooks folder, or a fresh Colab session.
root = Path.cwd()
if root.name in ('notebooks', 'scripts') and (root.parent / 'index.html').exists():
    root = root.parent
data_dir = root / 'data'
data_dir.mkdir(exist_ok=True)
csv_url = 'https://raw.githubusercontent.com/jhellingsdata/LSE-PP434/main/weeks/week03/data/data_shiller.csv'
response = requests.get(csv_url, timeout=60)
response.raise_for_status()
expected_hash = 'd77861ce8e5981ebb3a916b197fcf372a7dea0b15c709a44d1d4b639891f10e2'
if hashlib.sha256(response.content).hexdigest() != expected_hash:
    # The teaching source may have been updated: retain our checked snapshot.
    snapshot_url = 'https://raw.githubusercontent.com/RajwardhanRana/RajwardhanRana.github.io/main/data/data_shiller.csv'
    response = requests.get(snapshot_url, timeout=60)
    response.raise_for_status()
    if hashlib.sha256(response.content).hexdigest() != expected_hash:
        raise ValueError('Source snapshot changed. Review the data before regenerating charts.')
(data_dir / 'data_shiller.csv').write_bytes(response.content)
df = pd.read_csv(io.StringIO(response.text), dtype={'Date': str})
print('Raw data shape:', df.shape)
print(df[['Date', 'P', 'E']].head(12).to_string(index=False))


import numpy as np
df['PE_ratio'] = df['P'] / df['E']
usable = np.isfinite(df['PE_ratio'])
df_clean = df.loc[usable].copy()
print('Rows removed for missing or non-finite P/E:', int((~usable).sum()))
print('Cleaned rows:', len(df_clean))
assert np.isfinite(df_clean['PE_ratio']).all()


df_clean['Date_iso'] = pd.to_datetime(df_clean['Date'], format='%Y.%m', errors='raise')
df_clean = df_clean.sort_values('Date_iso').reset_index(drop=True)
assert not df_clean['Date_iso'].duplicated().any()
assert df_clean.loc[df_clean['Date'].eq('1871.10'), 'Date_iso'].iloc[0] == pd.Timestamp('1871-10-01')
assert len(pd.period_range(df_clean.Date_iso.min(), df_clean.Date_iso.max(), freq='M')) == len(df_clean)
df_clean.to_csv(data_dir / 'data_shiller_clean.csv', index=False, date_format='%Y-%m-%d')
df_out = df_clean[['Date_iso', 'PE_ratio']].copy()
df_out.to_csv(data_dir / 'data_shiller_pe.csv', index=False, date_format='%Y-%m-%d')
print(df_out.head(12).to_string(index=False))
print('Period:', df_out.Date_iso.min().date(), 'to', df_out.Date_iso.max().date())


mean_pe = float(df_out.PE_ratio.mean())
latest = df_out.iloc[-1]
peak = df_out.loc[df_out.PE_ratio.idxmax()]
print(f'Mean monthly P/E: {mean_pe:.2f}')
print(f'Latest usable observation: {latest.Date_iso:%B %Y}, P/E {latest.PE_ratio:.2f}')
print(f'Highest observed P/E: {peak.PE_ratio:.2f}, {peak.Date_iso:%B %Y}')


def build_chart(source):
    series = alt.Chart(source).mark_line(color='#087f8c', strokeWidth=2).encode(
        x=alt.X('Date_iso:T', title='Year', axis=alt.Axis(grid=False, format='%Y', tickCount=7)),
        y=alt.Y('PE_ratio:Q', title='Price / earnings (times)', scale=alt.Scale(zero=True)),
        tooltip=[alt.Tooltip('Date_iso:T', title='Month', format='%b %Y'),
                 alt.Tooltip('PE_ratio:Q', title='P/E (times)', format='.2f')]
    )
    average = alt.Chart(source).mark_rule(color='#a56316', strokeDash=[6, 4], strokeWidth=1.5).encode(
        y=alt.Y('mean(PE_ratio):Q', title='Price / earnings (times)'),
        tooltip=[alt.Tooltip('mean(PE_ratio):Q', title='Sample mean P/E', format='.2f')]
    )
    return (series + average).properties(
        width='container', height=320,
        title=alt.Title(text='US stock prices relative to earnings',
                        subtitle=['Monthly S&P composite P/E; dashed line = sample mean',
                                  'Source: Robert Shiller, via the course data snapshot'],
                        anchor='start', fontSize=18, subtitleFontSize=11)
    ).configure_view(stroke=None).configure_axis(
        labelFontSize=12, titleFontSize=13, titlePadding=12,
        gridColor='#e8edf0', domainColor='#b8c4cc'
    ).configure(font='Arial', background='white')

# A DataFrame embeds values and is convenient for the notebook preview.
chart = build_chart(df_out)
chart


web_chart = build_chart('data/data_shiller_pe.csv')
web_chart.save(str(root / 'wk3_pe_ratio_chart.json'))
spec = web_chart.to_dict(validate=True)
assert spec['data']['url'] == 'data/data_shiller_pe.csv'
assert 'datasets' not in spec
print('Saved:', root / 'wk3_pe_ratio_chart.json')
print('Raw data URL: https://raw.githubusercontent.com/RajwardhanRana/RajwardhanRana.github.io/main/data/data_shiller_pe.csv')

