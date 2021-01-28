import dash as dash
import dash_html_components as html
import pandas as pd

import sectionTotals
import sectionEvolutionGraphs
import sectionMapGraph

df = pd.read_csv(
    '../include/tp-google-analytics.tsv',
    sep='\t',
    encoding="utf16",
    index_col='ga:date',
    parse_dates=True
)

app = dash.Dash(__name__)

app.layout = html.Div([
    sectionTotals.build(df),
    sectionEvolutionGraphs.build(df),
    sectionMapGraph.build(df)
])

if __name__ == '__main__':
    app.run_server(debug=True)
