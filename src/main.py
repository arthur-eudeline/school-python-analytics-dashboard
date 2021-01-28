import dash as dash
import dash_html_components as html
import pandas as pd
import dash_core_components as dcc
from dash.dependencies import Input

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


# Callback pour mettre à jour les graphiques et les totaux
# La fonction associée est celle juste en dessous de l'annotation soit : onDatePickerChange
@app.callback(
    # On déclare les différents output depuis les fichiers sources
    # pour moins s'y perdre
    sectionEvolutionGraphs.output()
    + sectionTotals.output(),

    # Les inputs seront passés à la fonction callback (start_date et le end_date)
    [
        Input("date-picker", "start_date"),
        Input("date-picker", "end_date")
    ]
)
def onDatePickerChange(startDate, endDate):
    return \
        sectionEvolutionGraphs.update(df, startDate, endDate) \
        + sectionTotals.update(df, startDate, endDate)


# Callback pour isoler les régions sur la carte
@app.callback(
    sectionMapGraph.output(),
    Input("map-region-selector", "value")
)
def onDropdownChange(options):
    return sectionMapGraph.update(df, options)


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
