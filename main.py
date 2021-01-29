from datetime import date, timedelta

import dash as dash
import dash_html_components as html
import pandas as pd
import dash_core_components as dcc
from dash.dependencies import Input

from src import sectionTotals
from src import sectionEvolutionGraphs
from src import sectionMapGraph

df = pd.read_csv(
    'include/tp-google-analytics.tsv',
    sep='\t',
    encoding="utf16",
    index_col='ga:date',
    parse_dates=True
)

# Dates limites pour le dateRangePicker
minDate = df.index.min()
maxDate = df.index.max()

app = dash.Dash(
    __name__,
    assets_folder='assets/'
)


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


app.layout = html.Div(
    [
        html.Div([
            dcc.DatePickerRange(
                id='date-picker',
                min_date_allowed=minDate,
                max_date_allowed=pd.to_datetime(maxDate) + pd.DateOffset(days=1),
                start_date=minDate,
                end_date=maxDate,
                display_format="DD/MM/YYYY",
                end_date_id="end-date-el",
                start_date_id="start-date-el"
            ),
        ], className="datepicker-wrapper"),
        sectionTotals.build(df),
        sectionEvolutionGraphs.build(df),
        sectionMapGraph.build(df)
    ],
    className="container-fluid"
)

if __name__ == '__main__':
    app.run_server(debug=True)
