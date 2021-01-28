import dash as dash
import dash_html_components as html
import pandas as pd
import dash_core_components as dcc
from dash.dependencies import Input, Output

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

# Dates limites pour le dateRangePicker
minDate = df.index.min()
maxDate = df.index.max()

app = dash.Dash(__name__)

@app.callback(
    sectionEvolutionGraphs.output(),
    [
        Input("date-picker", "start_date"),
        Input("date-picker", "end_date")
    ]
)
def onDatePickerChange(startDate, endDate):
    return sectionEvolutionGraphs.update(df, startDate, endDate)


app.layout = html.Div([
    dcc.DatePickerRange(
        id='date-picker',
        min_date_allowed=minDate,
        max_date_allowed=maxDate,
        start_date=minDate,
        end_date=maxDate,
    ),
    sectionTotals.build(df),
    sectionEvolutionGraphs.build(df),
    sectionMapGraph.build(df)
])

if __name__ == '__main__':
    app.run_server(debug=True)
